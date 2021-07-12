# -*- coding: utf-8 -*-
__all__ = ('ClaimedExecutor', 'Executor', 'ExecutorThread', 'SyncQueue', 'SyncWait', )

import sys
from threading import Lock as SyncLock, Event as SyncEvent, Thread, current_thread
from collections import deque

from .export import include
from .futures import Future, _ignore_frame, render_exc_to_list, CancelledError

EventThread = include('EventThread')

_ignore_frame(__spec__.origin, 'wait', 'raise exception', )
_ignore_frame(__spec__.origin, 'result_no_wait', 'raise exception', )
_ignore_frame(__spec__.origin, 'run', 'result=func()', )

class SyncWait:
    """
    Blocking waiter, what's result or exception can be set.
    
    Attributes
    ----------
    _exception : `None` or `BaseException` instance
        The waiter's exception if applicable. defaults to `None`.
    _result : `Any`
        The waiter's result if applicable. Defaults to `None`.
    _waiter : `threading.SyncEvent`
        Threading event, what is set, when the waiter's result is set.
    """
    __slots__ = ('_exception', '_result', '_waiter',)
    def __init__(self):
        """
        Creates a new ``SyncWait`` instance.
        """
        self._exception = None
        self._result = None
        self._waiter = SyncEvent()
    
    def set_exception(self, exception):
        """
        Sets an exception as the waiter's result.
        
        Parameters
        ----------
        exception : `BaseException`
            The exception to set as the future's exception.
        
        Raises
        ------
        TypeError
            If `StopIteration` is given as `exception`.
        """
        if isinstance(exception, type):
            exception = exception()
        
        if type(exception) is StopIteration:
             raise TypeError(f'{exception} cannot be raised to a {self.__class__.__name__}: {self!r}')
        
        if self._exception is None:
            self._exception = exception
            self._waiter.set()
        else:
            if type(exception) is CancelledError and type(self._exception) is not CancelledError:
                self._exception = exception
    
    def set_result(self, result):
        """
        Sets the waiter's result.
        
        Parameters
        ----------
        result : `Any`
            The object to set as result.
        """
        self._result = result
        self._waiter.set()
    
    def wait(self):
        """
        Waits till the waiter's result is set, then returns it.
        
        Returns
        -------
        result : `Any`
        
        Raises
        ------
        TypeError
            The set exception is not a  `BaseException` instance.
        BaseException
            The set exception.
        """
        self._waiter.wait()
        exception = self._exception
        if exception is None:
            return self._result
        raise exception
    
    def cancel(self):
        """
        Cancels the waiter by setting it's exception as ``CancelledError`` if not yet set.
        """
        exception = self._exception
        if exception is None:
            self._waiter.set()
        else:
            if type(exception) is CancelledError:
                return
        
        self._exception = CancelledError()
        

class SyncQueue:
    """
    Synchronous queue for retrieving set elements outside of an event loop.
    
    Attributes
    ----------
    _cancelled : `bool`
        Whether the queue is cancelled.
    _lock : `threading.SyncLock`
        Threading lock to grant exclusive access to the queue.
    _results : `deque`
        A deque of the results set to the queue.
    _waiter : `None` or ``SyncWait``
        Result waiter of the queue.
    """
    __slots__ = ('_cancelled', '_lock', '_results', '_waiter',)
    
    def __init__(self, iterable=None, max_length=None, cancelled=False):
        """
        Creates a new ``SyncQueue`` instance with the given parameters.
        
        Parameters
        ----------
        iterable : `iterable` of `Any`
            Iterable to set the queue's results initially from.
        max_length : `int`
            Maximal length of the queue. If the queue would pass it's maximal length, it's oldest results are popped.
        cancelled : `bool`
            Whether the queue should be initially cancelled.
        """
        self._results = deque(maxlen=max_length) if iterable is None else deque(iterable, maxlen=max_length)
        self._waiter = None
        self._cancelled = cancelled
        self._lock = SyncLock()
    
    def set_result(self, result):
        """
        Sets an element to the sync queue, what can be retrieved by ``.result`` or  by ``.result_no_wait``.
        
        Parameters
        ----------
        result : `Any`
            Sets a result to the sync queue.
        """
        with self._lock:
            # Should we raise InvalidStateError?
            waiter = self._waiter
            if waiter is None:
                self._results.append(result)
            else:
                waiter.set_result(result)
                self._waiter = None
    
    def cancel(self):
        """
        Cancels the sync-queue and it's waiter as well.
        """
        if self._cancelled:
            return
        
        with self._lock:
            # Should we raise InvalidStateError?
            self._cancelled = True
            
            waiter = self._waiter
            if waiter is not None:
                waiter.cancel()
                self._waiter = None
    
    def result(self):
        """
        Gets the next result of the sync queue. If the queue is empty, blocks till a new result is set with
        ``.set_result``.
        
        Returns
        -------
        result : `Any`
        """
        with self._lock:
            results = self._results
            if results:
                return results.popleft()
            
            waiter = self._waiter
            if waiter is None:
                if self._cancelled:
                    raise CancelledError()
                
                waiter = SyncWait()
                self._waiter = waiter
        
        return waiter.wait()
    
    def result_no_wait(self):
        """
        Gets the next result of the sync queue instantly.
        
        Returns
        -------
        result : `Any`
        
        Raises
        ------
        CancelledError
            If the queue is empty and cancelled.
        IndexError
            If the queue is empty, but not cancelled.
        """
        with self._lock:
            results = self._results
            if results:
                return results.popleft()
            
            if self._cancelled:
                exception = CancelledError()
            else:
                raise IndexError('The queue is empty.')
            
            raise exception
    
    wait = result
    
    def __repr__(self):
        """Returns the sync queue's representation."""
        with self._lock:
            result = [
                self.__class__.__name__,
                '([',
            ]
            
            results = self._results
            
            limit = len(results)
            if limit:
                index = 0
                while True:
                    element = results[index]
                    index += 1
                    
                    results.append(repr(element))
                    if index == limit:
                        break
                    
                    result.append(', ')
                    continue
            
            result.append(']')
            
            max_length = results.maxlen
            if (max_length is not None):
                result.append(', max_length=')
                result.append(repr(max_length))
            
            if self._cancelled:
                result.append(', cancelled')
            
            result.append(')')
            return ''.join(result)
    
    __str__ = __repr__
    
    # deque operations
    
    @property
    def max_length(self):
        """
        The maximal length of the queue if applicable.
        
        Returns
        -------
        max_length : `None` or `int`
        """
        return self._results.maxlen
    
    def clear(self):
        """
        Clears the queue.
        """
        self._results.clear()
    
    def copy(self):
        """
        Copies the queue.
        
        Returns
        -------
        new : ``SyncQueue``
        """
        with self._lock:
            new = object.__init__(type(self))
            
            new._results = self._results.copy()
            new._waiter = None
            new._cancelled = self._cancelled
            new._lock = SyncLock()
            
        return new
    
    def reverse(self):
        """
        Reverses the queue.
        """
        with self._lock:
            self._results.reverse()
    
    def __len__(self):
        """Returns the queue's length."""
        with self._lock:
            return len(self._results)
    
    def __bool__(self):
        """Returns `True` if the queue has any elements."""
        with self._lock:
            if self._results:
                result = True
            else:
                result = False
        
        return result

EXECUTOR_THREAD_CREATED = 0
EXECUTOR_THREAD_RUNNING = 1
EXECUTOR_THREAD_STOPPED = 2

class ExecutorThread(Thread):
    """
    A `threading.Thread` subclass for executing blocking code as an executor.
    
    Attributes
    ----------
    state : `int`
        Whether the executor thread is currently running.
        
        Can be on of the following:
        +---------------------------+-------+
        | Respective name           | Value |
        +===========================+=======+
        | EXECUTOR_THREAD_CREATED   | 0     |
        +---------------------------+-------+
        | EXECUTOR_THREAD_RUNNING   | 1     |
        +---------------------------+-------+
        | EXECUTOR_THREAD_STOPPED   | 2     |
        +---------------------------+-------+
    
    queue : ``SyncQueue`` of ``ExecutionPair``
        Synchronous queue of functions to execute and of their waiter future.
    """
    __slots__ = ('state', 'queue',)
    def __init__(self):
        """
        Creates and start a ``ExecutorThread``.
        """
        self.state = EXECUTOR_THREAD_CREATED
        self.queue = SyncQueue()
        Thread.__init__(self, daemon=True)
        self.start()
        
    def run(self):
        """
        The main runner of an ``ExecutorThread``.
        """
        if self.state != EXECUTOR_THREAD_CREATED:
            return
            
        self.state = EXECUTOR_THREAD_RUNNING
        
        queue = self.queue
        
        while self.state == EXECUTOR_THREAD_RUNNING:
            try:
                try:
                    pair = queue.wait()
                except CancelledError:
                    return
                
                future = pair.future
                if future.done():
                    future = None
                    continue
                
                func = pair.func
                try:
                    result = func()
                except BaseException as err:
                    if isinstance(err, StopIteration):
                        exception = RuntimeError(f'{err.__class__.__name__} cannot be raised to a Future')
                        exception.__cause__ = err
                        err = exception
                        exception = None
                    
                    future._loop.call_soon_thread_safe(future.__class__.set_exception_if_pending, future, err)
                else:
                    future._loop.call_soon_thread_safe(future.__class__.set_result_if_pending, future, result)
                    result = None
                
                future = None
                func = None
            
            except BaseException as err:
                extracted = [
                    self.__class__.__name__,
                    ' exception occurred\n',
                    repr(self),
                    '\n',
                        ]
                render_exc_to_list(err, extend=extracted)
                sys.stderr.write(''.join(extracted))
    
    def execute(self, func, future=None):
        """
        Executes the given `func` on the executor thread.
        
        Parameters
        ----------
        func : `callable`
            The function to execute.
        future : `None` or ``Future``, Optional
            A future, what's result is set, when the `func` finishes it's execution.
            
            If not given a new future is created. Defaults to `None`
        
        Returns
        -------
        future : ``Future``
            Result waiter future.
        
        Raises
        ------
        RuntimeError
            `future` parameter is not given an the method was not called from an event thread.
        """
        if future is None:
            loop = current_thread()
            if not isinstance(loop, EventThread):
                raise RuntimeError(f'`future` parameter is not given and `{self!r}.execute` was not called '
                    f'from an{EventThread.__name__} either.')
            
            future = Future(loop)
        
        self.queue.set_result(ExecutionPair(func, future,),)
        return future
    
    def cancel(self):
        """
        Cancels all the pending elements on the executor thread's queue, then cancels the queue itself as well.
        """
        self.state = EXECUTOR_THREAD_STOPPED
        queue = self.queue
        while queue:
            future = queue.result_no_wait().future
            future._loop.call_soon_thread_safe(future.cancel)
        
        queue.cancel()
    
    def release(self):
        """
        Cancels the executor thread's queue.
        """
        self.queue.cancel()
    
    def _shrink_queue(self):
        """
        Removes all the done elements from the executor's queue.
        """
        results = self.queue._results
        
        index = 0
        limit = len(results)
        while index < limit:
            future = results[index]
            if future.done():
                del results[index]
                limit -= 1
            else:
                index += 1

class ExecutionPair:
    """
    Stores a function to execute and it's future, to what the function's result or exception is set when done.
    
    Attributes
    ----------
    func : `callable`
        The function to execute.
    future : ``Future``
        The result waiter future to what ``.func``'s result or exception is set.
    """
    __slots__ = ('func', 'future', )
    
    def __init__(self,func,future):
        """
        Creates a new ``ExecutionPair`` instance.
        
        Parameters
        ----------
        func : `callable`
            The function to execute.
        future : ``Future``
            The result waiter future to what ``.func``'s result or exception is set.
        """
        self.func = func
        self.future = future
    
    def __repr__(self):
        """Returns the execution pair's representation."""
        return f'{self.__class__.__name__}(func={self.func!r}, future={self.future!r})'

class _claim_ended_cb:
    """
    Future callback set to result waiter futures when calling ``ClaimedExecutor.release``.
    
    Gives back the executor thread, when it's queue becomes empty.
    
    Parameters
    ----------
    parent : ``Executor`` instance
        The parent executor
    executor : ``ExecutorThread``
        The executor thread, what is given to the parent executor when all of it's tasks are done.
    """
    __slots__ = ('executor', 'parent',)
    def __init__(self, parent, executor):
        """
        Creates a new ``_claim_ended_cb`` instance with the given parameters.
        
        Parameters
        ----------
        parent : ``Executor`` instance
            The parent executor
        executor : ``ExecutorThread``
            The executor thread, what is given to the parent executor when all of it's tasks are done.
        """
        self.parent = parent
        self.executor = executor
    
    def __call__(self, future):
        """Gives back the executor thread, when it's queue becomes empty."""
        loop = future._loop
        executor = self.executor
        executor._shrink_queue()
        if not executor.queue:
            parent = self.parent
            loop.call_soon_thread_safe(parent.__class__._claim_ended, parent, executor)
    
    def __eq__(self, other):
        """Returns whether the two claim ended callbacks are the same."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self.executor is other.executor
    
class ClaimedExecutor:
    """
    Wrapper for claimed executor threads.
    
    Attributes
    ----------
    executor : ``ExecutorThread``
        The claimed executor thread.
    parent : ``Executor``
        The parent executor from where the ``.executor`` is claimed.
    """
    __slots__ = ('executor', 'parent',)
    def __init__(self, parent, executor):
        """
        Creates a new claimed executor instance which will wrap the given executor thread of it's executor.
        
        Parameters
        ----------
        parent : ``Executor``
            The parent executor from where the ``.executor`` is claimed.
        executor : ``ExecutorThread``
            The claimed executor thread.
        """
        self.parent = parent
        self.executor = executor
        
    def execute(self, func):
        """
        Runs the given function in an executor thread. When the function is done, it's result or exception is set to
        the returned future.
        
        Parameters
        ----------
        func : ``Callable``
            The function to run inside of an executor thread.
        
        Returns
        -------
        future : ``Future``
            The future, to what the returned value or the raised exception of `func` is set.
        
        Raises
        ------
        RuntimeError
            The claimed executor is closed.
        """
        executor = self.executor
        if executor is None:
            raise RuntimeError(f'Executing on an already closed {self.__class__.__name__}.')
        
        future = self.parent.create_future()
        
        executor.queue.set_result(ExecutionPair(func, future,),)
        
        return future

    def release(self):
        """
        Releases the claimed executor. Gives back it's executor thread to the parent executor, when all of it's
        tasks finish.
        """
        executor = self.executor
        if executor is None:
            return
        
        executor._shrink_queue()
        
        results = executor.queue._results
        if results:
            callback = _claim_ended_cb(self.parent, executor)
            for element in results:
                future = element.future
                if future.done():
                    continue
                
                future.add_done_callback(callback)
        else:
            self.parent._claim_ended(executor)
        
        self.executor = None
    
    __del__ = release
    
    def __enter__(self):
        """Entering a claimed executor returns itself."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Releases the claimed executor."""
        self.release()
    
class _execution_ended_cb:
    """
    Future callback set to result waiter futures when calling ``Executor.run_in_executor``.
    
    Parameters
    ----------
    parent : ``Executor`` instance
        The parent executor
    executor : ``ExecutorThread``
        The executor thread, what is given to the parent executor when it's current task is done.
    """
    __slots__ = ('executor', 'parent',)
    
    def __init__(self, parent, executor):
        """
        Creates a new ``_execution_ended_cb`` instance with the given parameters.
        
        Parameters
        ----------
        parent : ``Executor`` instance
            The parent executor
        executor : ``ExecutorThread``
            The executor thread, what is given to the parent executor when it's current task is done.
        """
        self.parent = parent
        self.executor = executor
        
    def __call__(self, future):
        """calls the parent executor's ``._execution_ended`` method, giving the executor thread back to it."""
        parent = self.parent
        future._loop.call_soon_thread_safe(parent.__class__._execution_ended, parent, self.executor)
    
    def __eq__(self, other):
        """Returns whether the two execution ended callbacks are the same."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self.executor is other.executor

class Executor:
    """
    Executor enabling running blocking sync code from async.
    
    Attributes
    ----------
    claimed_executors : `set` of ``ExecutorThread``
        Claimed executors, which are given back to the executor on release.
    free_executors : `deque`
        The free (or not used) executors of the executor.
    keep_executor_count : `int`
        The minimal amount of executors to keep alive (or not close).
    running_executors : `set` of ``ExecutorThread``
        The executors under use.
    """
    __slots__ = ('claimed_executors', 'free_executors', 'keep_executor_count', 'running_executors',)
    
    def __init__(self, keep_executor_count=1):
        """
        Initializes the executor.
        
        Parameters
        ----------
        keep_executor_count : `int`, Optional
            The minimal amount of executors to keep alive (or not close).
        """
        self.free_executors = deque()
        self.running_executors = set()
        self.claimed_executors = set()
        self.keep_executor_count = keep_executor_count
    
    def __repr__(self):
        """Returns the executor's representation."""
        return (f'<{self.__class__.__name__} free={self.free_executor_count}, used={self.used_executor_count}, keep='
            f'{self.keep_executor_count}>')
    
    @property
    def used_executor_count(self):
        """
        Returns how much executor threads of the executors are currently under use.
        
        Returns
        -------
        used_executor_count : `int`
        """
        return len(self.running_executors)+len(self.claimed_executors)
    
    @property
    def free_executor_count(self):
        """
        Returns how much free executors
        """
        return len(self.free_executors)
    
    def cancel_executors(self):
        """
        Cancels the executor threads of the executor.
        
        Raises ``CancelledError`` to the not yet started tasks.
        """
        self.keep_executor_count = 0
        executors = self.free_executors
        while executors:
            executor = executors.pop()
            executor.release()
        
        executors = self.running_executors
        while executors:
            executor = executors.pop()
            executor.cancel()
        
        executors = self.claimed_executors
        while executors:
            executor = executors.pop()
            executor.cancel()
    
    def release_executors(self):
        """
        Releases the executor threads of the executor.
        
        Raises no exception to the already started tasks,
        """
        self.keep_executor_count = 0
        executors = self.free_executors
        while executors:
            executor = executors.pop()
            executor.release()
        
        executors = self.running_executors
        while executors:
            executor = executors.pop()
            executor.release()
        
        executors = self.claimed_executors
        while executors:
            executor = executors.pop()
            executor.release()
    
    __del__ = release_executors
    
    def create_future(self):
        """
        Creates a future bound to the respective event loop.
        
        Returns
        -------
        future : ``Future``
            The created future.
        
        Raises
        ------
        RuntimeError
            If the method was not called from an ``SyncEventLoop``.
        """
        local_thread = current_thread()
        if not isinstance(local_thread, EventThread):
            raise RuntimeError(f'{self!r}.create_future was not called from {EventThread.__name__}, but from '
                f'{local_thread.__class__.__name__}')
        
        return Future(local_thread)
    
    def run_in_executor(self, func):
        """
        Runs the given function in an executor thread. When the function is done, it's result or exception is set to
        the returned future.
        
        Parameters
        ----------
        func : ``Callable``
            The function to run inside of an executor thread.
        
        Returns
        -------
        future : ``Future``
            The future, to what the returned value or the raised exception of `func` is set.
            
            If the executor is cancelled, then these futures are cancelled as well.
        """
        future = self.create_future()
        executor = self._get_free_executor()
        self.running_executors.add(executor)
        future.add_done_callback(_execution_ended_cb(self, executor))
        executor.queue.set_result(ExecutionPair(func, future,),)
        return future

    def _execution_ended(self, executor):
        """
        Called when an executed function finishes ensured by ``.run_in_executor``. Used to give back the
        ``ExecutorThread`` to the executor and maybe cancel it.
        
        Parameters
        ----------
        executor : ``ExecutorThread``
            Executor with finished execution.
        """
        try:
            self.running_executors.remove(executor)
        except KeyError:
            return
        
        self._sync_keep(executor)
    
    def claim_executor(self):
        """
        Claims an executor thread from the executor. The thread is given back to the executor, when the returned
        wrapper is cancelled or released.
        
        Returns
        -------
        claimed_executor : ``ClaimedExecutor``
        """
        executor = self._get_free_executor()
        self.claimed_executors.add(executor)
        return ClaimedExecutor(self, executor)
    
    def _claim_ended(self, executor):
        """
        Called when a claimed executor is released and all of it's tasks are done. Used to give back the
        ``ExecutorThread`` to the executor and maybe cancel it.
        
        Parameters
        ----------
        executor : ``ExecutorThread``
            The given back executor.
        """
        try:
            self.claimed_executors.remove(executor)
        except KeyError:
            return
        
        self._sync_keep(executor)
    
    def _get_free_executor(self):
        """
        Gets a free executor thread from the executor. If there are no free executor threads, starts a new one.
        
        Returns
        -------
        executor : ``ExecutorThread``
        """
        executors = self.free_executors
        if executors:
            executor = executors.pop()
        else:
            executor = ExecutorThread()
        
        return executor

    def _sync_keep(self, executor):
        """
        Called when an executor thread is given back to the executor.
        
        The method decides whether the executor should be kept or released.
        
        Parameters
        ----------
        executor : ``ExecutorThread``
            The given back executor.
        """
        executors = self.free_executors
        if len(executors) < self.keep_executor_count:
            executors.append(executor)
            return
        
        executor.release()
