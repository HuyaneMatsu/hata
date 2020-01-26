# -*- coding: utf-8 -*-
__all__ = ('ClaimedExecutor', 'Executor', 'ExecutorThread', 'SyncQue',
    'SyncWait', )

import sys
from threading import Lock, Event, Thread, current_thread
from collections import deque

from .futures import Future, _ignore_frame, render_exc_to_list

_ignore_frame(__spec__.origin,  'wait'          , 'raise exception'     ,)
_ignore_frame(__spec__.origin,  'result_no_wait', 'raise exception'     ,)
_ignore_frame(__spec__.origin,  'run'           , 'result=func()'       ,)


class SyncWait(object):
    __slots__=('_exception', '_result', '_waiter',)
    def __init__(self):
        self._exception = None
        self._result    = None
        self._waiter    = Event()

    def set_exception(self,exception):
        if isinstance(exception,type):
            exception=exception()
        self._exception=exception
        self._waiter.set()

    def set_result(self,result):
        self._result=result
        self._waiter.set()

    def wait(self):
        self._waiter.wait()
        exception=self._exception
        if exception is None:
            return self._result
        raise exception
        
class SyncQue(object):
    __slots__=('_exception', '_lock', '_results', '_waiter',)

    def __init__(self,iterable=None,maxlen=None,exception=None):
        self._results=deque(maxlen=maxlen) if iterable is None else deque(iterable,maxlen=maxlen)
        self._waiter    = None
        self._exception = exception
        self._lock      = Lock()

    def set_result(self,element):
        with self._lock:
            #should we raise InvalidStateError?
            waiter=self._waiter
            if waiter is None:
                self._results.append(element)
            else:
                waiter.set_result(element)
                self._waiter=None

    def set_exception(self,exception):
        with self._lock:
            #should we raise InvalidStateError?
            self._exception=exception
            
            waiter=self._waiter
            if waiter is not None:
                waiter.set_exception(exception)
                self._waiter=None

    def result(self):
        with self._lock:
            if self._results:
                return self._results.popleft()

            waiter=self._waiter
            if waiter is None:
                waiter=SyncWait()
                self._waiter=waiter
        
        return waiter.wait()

    def result_no_wait(self):
        with self._lock:
            results=self._results
            if results:
                return results.popleft()
            
            exception=self._exception
            if exception is None:
                raise IndexError('The queue is empty')
            
            raise exception

    wait=result

    def __repr__(self):
        with self._lock:
            results=self._results
            maxlen=results.maxlen
            exception=self._exception
            return f'{self.__class__.__name__}([{", ".join([repr(element) for element in results])}]{"" if maxlen is None else f", maxlen={maxlen}"} {"" if exception is None else f", exception={exception}"})'

    __str__=__repr__

    #deque operations
    
    @property
    def maxlen(self):
        return self._results.maxlen
    
    def clear(self):
        self._results.clear()

    def copy(self):
        with self._lock:
            new=object.__init__(type(self))
            
            new._results    = self._results.copy()
            new._waiter     = None
            new._exception  = self._exception
            new._lock       = Lock()
            
        return new

    def reverse(self):
        with self._lock:
            self._results.reverse()

    def __len__(self):
        with self._lock:
            return self._results.__len__()

class ExecutorThread(Thread):
    __slots__=('running', 'queue',)
    def __init__(self):
        self.running=False
        self.queue=SyncQue()
        Thread.__init__(self,daemon=True)
        self.start()
        
    def run(self):
        self.running=True
        queue=self.queue

        while self.running:
            try:
                try:
                    pair=queue.wait()
                except InterruptedError:
                    return
                
                future=pair.future
                if future.done():
                    future=None
                    continue
                
                func=pair.func
                try:
                    result=func()
                except BaseException as err:
                    future._loop.call_soon_threadsafe(type(future).set_exception_if_pending,future,err)
                else:
                    future._loop.call_soon_threadsafe(type(future).set_result_if_pending,future,result)
                    result=None
                
                future  = None
                func    = None
                
            except BaseException as err:
                extracted=[
                    self.__class__.__name__,
                    ' exception occured\n',
                    self.__repr__(),
                    '\n',
                        ]
                render_exc_to_list(err,extend=extracted)
                sys.stderr.write(''.join(extracted))
                
    def execute(self,func,future=None):
        if future is None:
            future=Future(current_thread())
        self.queue.set_result(ExecutionPair(func,future,),)
        return future
        
    def cancel(self):
        self.running=False
        queue=self.queue
        while queue:
            future=queue.result_no_wait().future
            future._loop.call_soon_threadsafe(future.cancel)
            
        self.queue.set_exception(InterruptedError)

    def release(self):
        self.queue.set_exception(InterruptedError)

class ExecutionPair(object):
    __slots__=('func', 'future', )
    
    def __init__(self,func,future):
        self.func   = func
        self.future = future
        
    def __repr__(self):
        return f'{self.__class__.__name__}(func={self.func!r}, future={self.future!r})'

class _claim_ended_cb(object):
    __slots__=('executor', 'parent',)
    def __init__(self,parent,executor):
        self.parent=parent
        self.executor=executor
    
    def __call__(self,future):
        future._loop.call_soon_threadsafe(self.parent._claim_ended,self.executor)
        
    def __eq__(self,other):
        if type(self) is type(other):
            return self.executor is other.executor
        return NotImplemented
    
    def __ne__(self,other):
        if type(self) is type(other):
            return self.executor is not other.executor
        return NotImplemented
    
class ClaimedExecutor(object):
    __slots__=('executor', 'future', 'parent',)
    def __init__(self,parent,executor):
        self.parent=parent
        self.executor=executor
        self.future=None
        
    def execute(self,func):
        executor=self.executor
        if executor is None:
            raise RuntimeError(f'Executing on an already closed {self.__class__.__name__}.')
        
        future=self.parent.create_future()
        self.future=future
        
        executor.queue.set_result(ExecutionPair(func,future,),)
        
        return future

    def release(self):
        executor=self.executor
        if executor is None:
            return

        if executor.queue:
            self.future.add_done_callback(_claim_ended_cb(self.parent,executor))
        else:
            self.parent._claim_ended(executor)

        self.executor=None

    __del__=release
            
    def __enter__(self):
        return self

    def __exit__(self,exc_type,exc_val,exc_tb):
        self.release()

    def __await__(self):
        future=self.future
        if future is None:
            return None
        return (yield from future)

class _execution_ended_cb(object):
    __slots__=('executor', 'parent',)
    
    def __init__(self,parent,executor):
        self.parent=parent
        self.executor=executor
        
    def __call__(self,future):
        future._loop.call_soon_threadsafe(self.parent._execution_ended,self.executor)
        
    def __eq__(self,other):
        if type(self) is not type(other):
            return NotImplemented
        
        return self.executor is other.executor

    
class _id_execution_ended_cb(object):
    __slots__=('id', 'parent',)
    def __init__(self,parent,id_):
        self.parent=parent
        self.id=id_
    
    def __call__(self,future):
        future._loop.call_soon_threadsafe(self.parent._id_execution_ended,self.id)
        
    def __eq__(self,other):
        if type(self) is type(other):
            return self.id==other.id
        return NotImplemented

    def __ne__(self,other):
        if type(self) is type(other):
            return self.id!=other.id
        return NotImplemented

class Executor(object):
    __slots__=('claimed_executors', 'free_executors', 'keep_executor_count',
        'running_executors', 'running_id_executors',)
    
    def __init__(self,keep_executor_count=1):
        self.free_executors=deque()
        self.running_executors={}
        self.running_id_executors={}
        self.claimed_executors={}
        self.keep_executor_count=keep_executor_count

    def __repr__(self):
        return f'<{self.__class__.__name__} free={self.free_executor_count}, used={self.used_executor_count}, keep={self.keep_executor_count}>'
    
    @property
    def used_executor_count(self):
        return len(self.running_executors)+len(self.running_id_executors)+len(self.claimed_executors)
    
    @property
    def free_executor_count(self):
        return len(self.free_executors)
    
    def cancel_executors(self):
        self.keep_executor_count=0
        for executor in self.free_executors:
            executor.release()
        self.free_executors.clear()
        for executor in self.running_executors.values():
            executor.cancel()
        for executor in self.running_id_executors.values():
            executor.cancel()
        for executor in self.claimed_executors.values():
            executor.cancel()

    def release_executors(self):
        self.keep_executor_count=0
        for executor in self.free_executors:
            executor.release()
        self.free_executors.clear()
        for executor in self.running_executors.values():
            executor.release()
        for executor in self.running_id_executors.values():
            executor.release()
        for executor in self.claimed_executors.values():
            executor.release()

    __del__=release_executors

    def create_future(self):
        return Future(current_thread())
    
    def run_in_executor(self,func):
        future=self.create_future()
        executor=self._get_free_executor()
        self.running_executors[executor._ident]=executor
        future.add_done_callback(_execution_ended_cb(self,executor))
        executor.queue.set_result(ExecutionPair(func,future,),)
        return future

    def _execution_ended(self,executor):
        try:
            del self.running_executors[executor._ident]
        except KeyError:
            return
        self._sync_keep(executor)
    
    def run_in_id_executor(self,func,id_):
        future=self.create_future()
        if id_ in self.running_id_executors:
            future.set_exception(ReferenceError)
            return future

        executor=self._get_free_executor()
        self.running_id_executors[id_]=executor
        future.add_done_callback(_id_execution_ended_cb(self,id_))
        executor.queue.set_result(ExecutionPair(func,future,),)

        return future
    
    def _id_execution_ended(self,id_):
        try:
            executor=self.running_id_executors.pop(id_)
        except KeyError:
            return
        self._sync_keep(executor)

    def claim_executor(self):
        executor=self._get_free_executor()
        self.claimed_executors[executor._ident]=executor
        wrapped=ClaimedExecutor(self,executor)
        return wrapped
            
    def _claim_ended(self,executor):
        try:
            del self.claimed_executors[executor._ident]
        except KeyError:
            return

        self._sync_keep(executor)
    
    def _get_free_executor(self):
        executors=self.free_executors
        if executors:
            executor=executors.pop()
        else:
            executor=ExecutorThread()
        
        return executor

    def _sync_keep(self,executor):
        executors=self.free_executors
        if len(executors)<self.keep_executor_count:
            executors.append(executor)
            return
        executor.release()

    def _stopping(self):
        executors=self.free_executors
        while executors:
            executors.popleft().release()
            
del _ignore_frame
