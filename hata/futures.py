# -*- coding: utf-8 -*-
__all__ = ('AsyncQue', 'CancelledError', 'Future', 'FutureAsyncWrapper',
    'FutureG', 'FutureSyncWrapper', 'FutureWM', 'InvalidStateError', 'Lock',
    'Task', 'WaitTillAll', 'WaitTillExc', 'WaitTillFirst', 'enter_executor',
    'future_or_timeout', 'gather', 'iscoroutine', 'iscoroutinefunction',
    'shield', 'sleep', )

import sys, reprlib, linecache
from types import GeneratorType, CoroutineType, MethodType as method, FunctionType as function
from collections import deque
from threading import current_thread, Lock as SyncLock, Event as SyncEvent

from .dereaddons_local import alchemy_incendiary

class CancelledError(BaseException):
    """The Future or Task was cancelled."""

class InvalidStateError(Exception):
    """The operation is not allowed in this state."""
    
    def __init__(self,future,func_name):
        self.future     = future
        self.func_name  = func_name
        self._message   = None
        
    def __repr__(self):
        return f'{self.__class__.__name__}: {self.message}'

    __str__=__repr__
    
    @property
    def message(self):
        message=self._message
        if message is None:
            future=self.future
            message=f'`{future.__class__.__name__}.{self.func_name}` was called, when `.state` is {future._state} of {future!r}'
            self._message=message
        
        return message
    
    @classmethod
    def with_message(cls,future,func_name,message):
        self=Exception.__new__(cls)
        self.future     = future
        self.func_name  = func_name
        self._message   = message
        
def iscoroutinefunction(func):
    if isinstance(func,(function,method)) and func.__code__.co_flags&0x180:
        return True #the result MUST be converted to `1`
    return (getattr(func,'__async_call__',False)==True)

def iscoroutine(obj):
    return isinstance(obj,(CoroutineType,GeneratorType))

EventThread = NotImplemented

#future states

PENDING     = 'PENDING'
CANCELLED   = 'CANCELLED'
FINISHED    = 'FINISHED'
RETRIEVED   = 'RETRIEVED'

#If we run without `-o` or -oo` flag, we have 4 future states instead of the
#regular 3. Well, we have 4 anyways, we just wont use it. The only exceptions
#are the `__repr__` methods, where we still check it's existence.
#These flags also remove the `__del__` notifications and the
# `__silence__` methods too. Also bad Task awaiting cases are removed too.
#Thats why more methods, which interact with these variables have 2 versions.
#1 optimalized and 1 debug :^)

_IGNORED_FRAME_INFOS={}
def _ignore_frame(file,name,line):
    try:
        file_s=_IGNORED_FRAME_INFOS[file]
    except KeyError:
        file_s={}
        _IGNORED_FRAME_INFOS[file]=file_s

    try:
        name_s=file_s[name]
    except KeyError:
        name_s=set()
        file_s[name]=name_s

    name_s.add(line)
        
def _should_ignore_frame(file,name,line):
    try:
        file_s=_IGNORED_FRAME_INFOS[file]
    except KeyError:
        return False

    try:
        name_s=file_s[name]
    except KeyError:
        return False
    
    return (line in name_s)

_ignore_frame(__spec__.origin   , 'result'          , 'raise exception'                 ,)
_ignore_frame(__spec__.origin   , 'result_no_wait'  , 'raise exception'                 ,)
_ignore_frame(__spec__.origin   , '__call__'        , 'raise exception'                 ,)
_ignore_frame(__spec__.origin   , '__step'          , 'result=coro.throw(exception)'    ,)
_ignore_frame(__spec__.origin   , '__iter__'        , 'yield self'                      ,)
_ignore_frame(__spec__.origin   , '__step'          , 'result=coro.send(None)'          ,)
_ignore_frame(__spec__.origin   , '__wakeup'        , 'future.result()'                 ,)
_ignore_frame(__spec__.origin   , 'wait'            , 'return self.result()'            ,)

from . import dereaddons_local
_ignore_frame(dereaddons_local.__spec__.origin  , '__call__', 'return self.func(*self.args)'            ,)
_ignore_frame(dereaddons_local.__spec__.origin  , '__call__', 'return self.func(*self.args,**kwargs)'   ,)
del dereaddons_local

def render_frames_to_list(frames,extend=None):
    if extend is None:
        extend  = []
    checked     = set()

    last_file_name  = ''
    last_line_number= ''
    last_name       = ''
    count           = 0
    
    for frame in frames:
        line_number = frame.f_lineno
        code        = frame.f_code
        file_name   = code.co_filename
        name        = code.co_name

        if last_file_name==file_name and last_line_number==line_number and last_name==name:
            count=count+1
            if count>2:
                continue
        else:
            if count>3:
                count=count-3
                extend.append('  [Previous line repeated ')
                extend.append(str(count))
                extend.append(' more times]\n')
            count=0
        
        if file_name not in checked:
            checked.add(file_name)
            linecache.checkcache(file_name)
        
        line=linecache.getline(file_name,line_number,None)
        line=line.strip()
        
        if _should_ignore_frame(file_name,name,line):
            continue

        last_file_name  = file_name
        last_line_number= line_number
        last_name       = code.co_name
        
        extend.append('  File \"')
        extend.append(file_name)
        extend.append('\", line ')
        extend.append(str(line_number))
        extend.append(', in ')
        extend.append(name)
        if (line is not None) and line:
            extend.append('\n    ')
            extend.append(line)
        extend.append('\n')
        
    if count>3:
        count=count-3
        extend.append('  [Previous line repeated ')
        extend.append(str(count))
        extend.append(' more times]\n')
        
    return extend

class _EXCFrameType(object):
    __slots__=('tb',)
    
    def __init__(self,tb):
        self.tb=tb
    
    @property
    def f_builtins(self):
        return self.tb.tb_frame.f_builtins
    
    @property
    def f_code(self):
        return self.tb.tb_frame.f_code

    @property
    def f_globals(self):
        return self.tb.tb_frame.f_globals

    @property
    def f_lasti(self):
        return self.tb.tb_frame.f_lasti
    
    @property
    def f_lineno(self):
        return self.tb.tb_lineno
    
    @property
    def f_locals(self):
        return self.tb.tb_frame.f_locals
    
    @property
    def f_trace(self):
        return self.tb.tb_frame.f_trace
    
def _get_exc_frames(exception):
    frames=[]
    tb=exception.__traceback__

    while True:
        if tb is None:
            break
        frame=_EXCFrameType(tb)
        frames.append(frame)
        tb=tb.tb_next
    
    return frames

def render_exc_to_list(exception,extend=None):
    if extend is None:
        extend=[]
    
    exceptions=[]
    while True:
        exceptions.append(exception)
        exception=exception.__cause__
        if exception is None:
            break
    
    index=len(exceptions)
    while True:
        index=index-1
        exception=exceptions[index]
        frames=_get_exc_frames(exception)
        extend.append('Traceback (most recent call last):\n')
        extend=render_frames_to_list(frames,extend=extend)
        extend.append(exception.__repr__())
        extend.append('\n')
        if index==0:
            break
            
        extend.append('\nThe above exception was the direct cause of the following exception:\n\n')
        continue
    
    return extend

def format_callback(func, args=None, kwargs=None):
    result=[]
    #unwarp the wrappers
    while True:
        if not (None is args is kwargs):
            sub_result=['(']
            if (args is not None) and args:
                for arg in args:
                    sub_result.append(reprlib.repr(arg))
                    sub_result.append(', ')
            if kwargs is not None and kwargs:
                for key,arg in kwargs.items():
                    sub_result.append(f'{key}={reprlib.repr(arg)}')
                    sub_result.append(', ')

            if len(sub_result)>1:
                del sub_result[-1]
            sub_result.append(')')
            result.append(''.join(sub_result))

        try:
            wrapped=func.func
        except AttributeError:
            if type(func) is method and func.__self__.__class__ is Task:
                coro=func.__self__._coro
                coro_repr=getattr(coro,'__qualname__',None)
                if coro_repr is None:
                    coro_repr=getattr(coro,'__name__',None)
                    if coro_repr is None:
                        coro_repr=coro.__repr__()
                func_repr=f'<Bound method {func.__func__.__name__} of Task {coro_repr}>'
            else:
                func_repr=getattr(func,'__qualname__',None)
                if func_repr is None:
                    func_repr=getattr(func,'__name__',None)
                    if func_repr is None:
                        func_repr=func.__repr__()

            result.insert(0,func_repr)
            break

        args=getattr(func,'args',None)
        kwargs=getattr(func,'kwargs',None)
        func=wrapped

    return ''.join(result)

def format_coroutine(coro):
    if not (hasattr(coro,'cr_code') or hasattr(coro,'gi_code')):
        #Cython or builtin
        name=getattr(coro,'__qualname__',None)
        if name is None:
            name=getattr(coro,'__name__',None)
            if name is None: #builtins might reach this part
                name=coro.__class__.__name__

        if type(coro) is GeneratorType:
            running=coro.gi_running
        elif type(coro) is CoroutineType:
            running=coro.cr_running
        else:
            running=False

        return f'{name}(){" running" if running else ""}'

    name=format_callback(coro)

    if type(coro) is GeneratorType:
        code=coro.gi_code
        frame=coro.gi_frame
    else:
        code=coro.cr_code
        frame=coro.cr_frame

    file_name=code.co_filename

    if frame is None:
        line_number=code.co_firstlineno
        state='done'
    else:
        line_number=frame.f_lineno
        state='running'

    return f'{name} {state} defined at {file_name}:{line_number}'

class Future(object):
    __slots__=('_blocking', '_callbacks', '_exception', '_loop', '_result',
        '_state')

    #if arguments are not passed will not call `__del__`
    def __new__(cls,loop):
        self=object.__new__(cls)
        self._loop      = loop
        self._state     = PENDING

        self._result    = None
        self._exception = None
        
        self._callbacks = []
        self._blocking  = False

        return self

    def __repr__(self):
        result=['<',self.__class__.__name__,' ',self._state]
        if self._state is FINISHED or self._state is RETRIEVED:
            if self._exception is None:
                result.append(' result=')
                result.append(reprlib.repr(self._result))
            else:
                result.append(' exception=')
                result.append(self._exception.__repr__())
        
        if self._callbacks:
            result.append(' callbacks=[')
            result.append(', '.join([format_callback(callback) for callback in self._callbacks]))
            result.append(']')
        result.append('>')

        return ''.join(result)
    
    if __debug__:
        def cancel(self):
            state=self._state
            
            if state is not PENDING:
                # If the future is cancelled, we should not show up not retrieved
                # message at `.__del__`
                if state is FINISHED:
                    self._state=RETRIEVED
                return 0
            
            self._state=CANCELLED
            self._loop._schedule_callbacks(self)
            return 1
    else:
        def cancel(self):
            if self._state is not PENDING:
                return 0
                
            self._state=CANCELLED
            self._loop._schedule_callbacks(self)
            return 1
            
    def cancelled(self):
        return (self._state is CANCELLED)
            
    def done(self):
        return (self._state is not PENDING)

    def pending(self):
        return (self._state is PENDING)

    if __debug__:
        def result(self):
            state=self._state
            
            if state is FINISHED:
                self._state=RETRIEVED
                exception=self._exception
                if exception is None:
                    return self._result
                raise exception

            if state is RETRIEVED:
                exception=self._exception
                if exception is None:
                    return self._result
                raise exception
            
            if state is CANCELLED:
                raise CancelledError
            
            #PENDING
            raise InvalidStateError(self,'result')
    else:
        def result(self):
            state=self._state

            if state is FINISHED:
                exception=self._exception
                if exception is None:
                    return self._result
                raise exception

            if state is CANCELLED:
                raise CancelledError
            
            #PENDING
            raise InvalidStateError(self,'result')

    if __debug__:
        def exception(self):
            state=self._state
            if state is FINISHED:
                self._state=RETRIEVED
                return self._exception

            if state is RETRIEVED:
                return self._exception
            
            if state is CANCELLED:
                raise CancelledError
            
            #PENDING
            raise InvalidStateError(self,'exception')
        
    else:
        def exception(self):
            state=self._state

            if state is FINISHED:
                return self._exception
            
            if state is CANCELLED:
                raise CancelledError
            
            #PENDING
            raise InvalidStateError(self,'exception')

    def add_done_callback(self,func):
        if self._state is PENDING:
            self._callbacks.append(func)
        else:
            self._loop.call_soon(func,self)

    def remove_done_callback(self,func):
        callbacks=self._callbacks
        count=0
        index=len(callbacks)
        while index:
            index-=1
            if callbacks[index] is func:
                del callbacks[index]
                count+=1
    
        return count
    
    def set_result(self,result):
        if self._state is not PENDING:
            raise InvalidStateError(self,'set_result')
            
        self._result    = result
        self._state     = FINISHED
        self._loop._schedule_callbacks(self)

    def set_result_if_pending(self,result):
        if self._state is not PENDING:
            return 0

        self._result    = result
        self._state     = FINISHED
        self._loop._schedule_callbacks(self)
        return 1
        
    def set_exception(self,exception):
        if self._state is not PENDING:
            raise InvalidStateError(self,'set_exception')
            
        if isinstance(exception,type):
            exception=exception()
            
        if type(exception) is StopIteration:
             raise TypeError(f'{exception} cannot be raised to a {self.__class__.__name__}: {self!r}')
        
        self._exception = exception
        self._state     = FINISHED
        self._loop._schedule_callbacks(self)

    def set_exception_if_pending(self,exception):
        if self._state is not PENDING:
            return 0

        if isinstance(exception,type):
            exception=exception()
            
        if type(exception) is StopIteration:
             raise TypeError(f'{exception} cannot be raised to a {self.__class__.__name__}: {self!r}')
        
        self._exception = exception
        self._state     = FINISHED
        self._loop._schedule_callbacks(self)
        return 1
        
    def __iter__(self):
        if self._state is PENDING:
            self._blocking=True
            yield self
        
        return self.result()

    __await__=__iter__

    if __debug__:
        def __del__(self):
            if not self._loop.running:
                return

            state=self._state
            if state is PENDING:
                if self._callbacks:

                    #ignore being silenced
                    silence_cb=type(self).__silence_cb__
                    for callback in self._callbacks:
                        if callback is silence_cb:
                            return

                    sys.stderr.write(f'{self.__class__.__name__} is not finished, but still pending!\n{self!r}\n')
                return

            if state is FINISHED:
                if (self._exception is not None):
                    self._loop.render_exc_maybe_async(self._exception,[
                        self.__class__.__name__,
                        ' exception was never retrieved\n',
                        self.__repr__(),
                        '\n',])
                return

            #no more notify case

        def __silence__(self):
            state=self._state
            if state is PENDING:
                self._callbacks.append(type(self).__silence_cb__)
                return

            if state is FINISHED:
                self._state=RETRIEVED
                return

        def __silence_cb__(self):
            if self._state is FINISHED:
                self._state=RETRIEVED

    def cancel_handles(self):
        callbacks=self._callbacks
        if callbacks:
            for index in range(len(callbacks)-1,-1,-1,):
                callback=callbacks[index]
                if isinstance(callback,_handle_base):
                    del callbacks[index]
                    callback.cancel()
                    
    def clear(self):
        self._state     = PENDING
        self._exception = None
        self._result    = None
        self.cancel_handles()
        self._blocking  = False

    def syncwrap(self):
        return FutureSyncWrapper(self)

    def asyncwrap(self,loop):
        return FutureAsyncWrapper(self,loop)

class FutureSyncWrapper(object):
    __slots__=('_exception', '_future', '_lock', '_result', '_state', '_waiter')
    def __new__(cls,future):
        self=object.__new__(cls)
        self._future    = future
        self._lock      = SyncLock()
        self._waiter    = SyncEvent()
        self._state     = PENDING
        self._result    = None
        self._exception = None

        loop=future._loop
        loop.call_soon(future.add_done_callback,self._done_callback)
        loop.wakeup()

        return self

    def __call__(self,future):
        with self._lock:
            old_future=self._future

            if old_future is not None:
                loop=old_future._loop
                loop.call_soon(self._remove_callback,old_future)
                loop.wakeup()

            self._future    = future
            self._state     = PENDING
            self._result    = None
            self._exception = None
            self._waiter.clear()

            loop=future._loop
            loop.call_soon(future.add_done_callback,self._done_callback)
            loop.wakeup()

        return self

    def __repr__(self):
        result=['<',self.__class__.__name__,' ',self._state]
        if self._state is FINISHED or self._state is RETRIEVED:
            if self._exception is None:
                result.append(' result=')
                result.append(reprlib.repr(self._result))
            else:
                result.append(' exception=')
                result.append(self._exception.__repr__())

        future=self._future
        if future is not None:
            #we do not want to repr it, keep it threadsafe
            result.append(' future=')
            result.append(future.__class__.__name__)
            result.append('(...)')
        result.append('>')

        return ''.join(result)
    
    if __debug__:
        def cancel(self):
            state=self._state
            if state is not PENDING:
                if state is FINISHED:
                    self._state=RETRIEVED
                
                return 0
    
            future=self._future
            if future is None:
                self._state=CANCELLED
                self._waiter.set()
                return 1
    
            loop=future._loop
            loop.call_soon(future.cancel)
            loop.wakeup()
            return 1
        
    else:
        def cancel(self):
            if self._state is not PENDING:
                return 0
    
            future=self._future
            if future is None:
                self._state=CANCELLED
                self._waiter.set()
                return 1
    
            loop=future._loop
            loop.call_soon(future.cancel)
            loop.wakeup()
            return 1

    def cancelled(self):
        return (self._state is CANCELLED)

    def done(self):
        return (self._state is not PENDING)

    def pending(self):
        return (self._state is PENDING)

    if __debug__:
        def result(self):
            with self._lock:
                state=self._state

                if state is FINISHED:
                    self._state=RETRIEVED
                    exception=self._exception
                    if exception is None:
                        return self._result
                    raise exception

                if state is RETRIEVED:
                    exception=self._exception
                    if exception is None:
                        return self._result
                    raise exception

                if state is CANCELLED:
                    raise CancelledError

            #PENDING
            raise InvalidStateError(self,'result')

    else:
        def result(self):
            with self._lock:
                if self._state is FINISHED:
                    exception=self._exception
                    if exception is None:
                        return self._result
                    raise exception

                if self._state is CANCELLED:
                    raise CancelledError

            #PENDING
            raise InvalidStateError(self,'result')

    if __debug__:
        def exception(self):
            with self._lock:
                state=self._state
                if state is FINISHED:
                    self._state=RETRIEVED
                    return self._exception

                if state is RETRIEVED:
                    return self._exception

                if state is CANCELLED:
                    raise CancelledError

            #PENDING
            raise InvalidStateError(self,'exception')

    else:
        def exception(self):
            with self._lock:
                if self._state is FINISHED:
                    return self._exception

                if self._state is CANCELLED:
                    raise CancelledError

            #PENDING
            raise InvalidStateError(self,'exception')

    if __debug__:
        def _done_callback(self,future):
            with self._lock:
                if (self._future is not future):
                    return

                state=future._state
                if state is FINISHED:
                    future._state=RETRIEVED
                elif state is RETRIEVED:
                    state=FINISHED

                self._state     = state
                self._result    = future._result
                self._exception = future._exception
                self._future    = None
                self._waiter.set()
    else:
        def _done_callback(self,future):
            with self._lock:
                if (self._future is not future):
                    return

                self._state     = future._state
                self._result    = future._result
                self._exception = future._exception
                self._future    = None
                self._waiter.set()

    def _remove_callback(self,future):
        callbacks=future._callbacks
        ln=len(callbacks)
        if ln==0:
            return
        for index in range(ln):
            callback=callbacks[index]
            if (type(callback) is method) and (callback.__self__ is self):
                del callbacks[index]
                break

    def wait(self,timeout=None):
        self._waiter.wait(timeout)
        return self.result()

    def _set_future_result(self,future,result):
        try:
            future.set_result(result)
        except (RuntimeError,InvalidStateError): #the future does not supports this operation
            pass

        with self._lock:
            if self._future is future:
                self._state     = RETRIEVED
                self._future    = None

    def set_result(self,result):
        with self._lock:
            if self._state is not PENDING:
                raise InvalidStateError(self,'set_result')

            future=self._future

            if future is None:
                self._result    = result
                self._state     = FINISHED
                self._waiter.set()
                return

        loop=future._loop
        loop.call_soon(self._set_future_result,future,result)
        loop.wakeup()

    def set_result_if_pending(self,result):
        with self._lock:
            if self._state is not PENDING:
                return 0
            
            future=self._future

            if future is None:
                self._result    = result
                self._state     = FINISHED
                self._waiter.set()
                return 2

        loop=future._loop
        loop.call_soon(self._set_future_result,future,result)
        loop.wakeup()
        return 1
        
    def _set_future_exception(self,future,exception):
        try:
            future.set_exception(exception)
        except (RuntimeError,InvalidStateError): #the future does not supports this operation
            pass

        with self._lock:
            if self._future is future:
                self._state     = RETRIEVED
                self._future    = None

    def set_exception(self,exception):
        with self._lock:
            if self._state is not PENDING:
                raise InvalidStateError(self,'set_exception')

            if isinstance(exception,type):
                exception=exception()
            
            if type(exception) is StopIteration:
                 raise TypeError(f'{exception} cannot be raised to a {self.__class__.__name__}: {self!r}')

            future=self._future
            if future is None:
                self._exception = exception
                self._state     = FINISHED
                self._waiter.set()
                return

        loop=future._loop
        loop.call_soon(self._set_future_exception,future,exception)
        loop.wakeup()

    def set_exception_if_pending(self,exception):
        with self._lock:
            if self._state is not PENDING:
                return 0
            
            if isinstance(exception,type):
                exception=exception()
            
            if type(exception) is StopIteration:
                 raise TypeError(f'{exception} cannot be raised to a {self.__class__.__name__}: {self!r}')

            future=self._future
            if future is None:
                self._exception = exception
                self._state     = FINISHED
                self._waiter.set()
                return 2

        loop=future._loop
        loop.call_soon(self._set_future_exception,future,exception)
        loop.wakeup()
        return 1
    
    if __debug__:
        def __del__(self):
            if self._state is PENDING:
                if self._future is not None:
                    sys.stderr.write(f'{self.__class__.__name__} is not finished, but still pending!\n{self!r}\n')
                return

            if self._state is FINISHED:
                if (self._exception is not None):
                    extracted=[
                        self.__class__.__name__,
                        ' exception was never retrieved\n',
                        self.__repr__(),
                        '\n',]
                    render_exc_to_list(self._exception,extend=extracted)
                    sys.stderr.write(''.join(extracted))
                return

            #no more notify case

        def __silence__(self):
            self._state=RETRIEVED

    def clear(self):
        with self._lock:
            future=self._future
            if future is not None:
                loop=future._loop
                loop.call_soon(self._remove_callback,future)
                loop.wakeup()
                self._future=None

            self._waiter.clear()
            self._state     = PENDING
            self._exception = None
            self._result    = None


class FutureAsyncWrapper(Future):
    __slots__=('_blocking', '_callbacks', '_exception', '_future', '_loop',
        '_result', '_state',)

    def __new__(cls,future,loop):
        if future._loop is loop:
            return future

        if isinstance(future,FutureAsyncWrapper):
            future=future._future
            if future._loop is loop:
                return future

        self=object.__new__(cls)
        self._future    = future
        self._loop      = loop
        self._state     = PENDING
        self._result    = None
        self._exception = None

        self._callbacks = []
        self._blocking  = False

        loop=future._loop
        loop.call_soon(future.add_done_callback,self._done_callback)
        loop.wakeup()

        return self

    def __call__(self,future):
        old_future=self._future
        if old_future is not None:
            loop=old_future._loop
            loop.call_soon(self._remove_callback,old_future)
            loop.wakeup()

        self._future    = future
        self._state     = PENDING
        self._result    = None
        self._exception = None
        self._blocking  = False

        loop=future._loop
        loop.call_soon(future.add_done_callback,self._done_callback)
        loop.wakeup()

    def __repr__(self):
        result=['<',self.__class__.__name__,' ',self._state]
        if self._state is FINISHED or self._state is RETRIEVED:
            if self._exception is None:
                result.append(' result=')
                result.append(reprlib.repr(self._result))
            else:
                result.append(' exception=')
                result.append(self._exception.__repr__())

        if self._callbacks:
            result.append(' callbacks=[')
            result.append(', '.join([format_callback(callback) for callback in self._callbacks]))
            result.append(']')

        future=self._future
        if future is not None:
            #we do not want to repr it, keep it threadsafe
            result.append(' future=')
            result.append(future.__class__.__name__)
            result.append('(...)')
        result.append('>')

        return ''.join(result)
    
    if __debug__:
        def cancel(self):
            state=self._state
            if state is not PENDING:
                if state is FINISHED:
                    self._state=RETRIEVED
                
                return 0
    
            future=self._future
            if future is None:
                self._state=CANCELLED
                self._loop._schedule_callbacks(self)
                return 1
    
            loop=future._loop
            loop.call_soon(future.cancel)
            loop.wakeup()
            return 1
        
    else:
        def cancel(self):
            if self._state is not PENDING:
                return 0
    
            future=self._future
            if future is None:
                self._state=CANCELLED
                self._loop._schedule_callbacks(self)
                return 1
    
            loop=future._loop
            loop.call_soon(future.cancel)
            loop.wakeup()
            return 1

    if __debug__:
        def _done_callback(self,future):
            if self._future is not future:
                return

            state=future._state
            if state is FINISHED:
                future._state=RETRIEVED
            elif state is RETRIEVED:
                state=FINISHED

            loop=self._loop
            loop.call_soon(self._done_callback_re,state,future._result,future._exception)
            loop.wakeup()
    else:
        def _done_callback(self,future):
            if (self._future is not future):
                return

            loop=self._loop
            loop.call_soon(self._done_callback_re,future._state,future._result,future._exception)
            loop.wakeup()

    def _done_callback_re(self,state,result,exception):
        self._state     = state
        self._result    = result
        self._exception = exception

        self._loop._schedule_callbacks(self)

    def _remove_callback(self,future):
        callbacks=future._callbacks
        ln=len(callbacks)
        if ln==0:
            return
        for index in range(ln):
            callback=callbacks[index]
            if (type(callback) is method) and (callback.__self__ is self):
                del callbacks[index]
                break

    def _set_future_result(self,future,result):
        try:
            future.set_result(result)
        except (RuntimeError,InvalidStateError): #the future does not supports this operation
            pass

        loop=self._loop
        loop.call_soon(self._set_future_any_re,future)
        loop.wakeup()

    def _set_future_any_re(self,future):
        if self._future is future:
            self._state=RETRIEVED
            self._future=None

    def set_result(self,result):
        if self._state is not PENDING:
            raise InvalidStateError(self,'set_result')

        future=self._future

        if future is None:
            self._result=result
            self._state=FINISHED
            self._loop._schedule_callbacks(self)
            return

        loop=future._loop
        loop.call_soon(self._set_future_result,future,result)
        loop.wakeup()

    def set_result_if_pending(self,result):
        if self._state is not PENDING:
            return 1
        
        future=self._future

        if future is None:
            self._result=result
            self._state=FINISHED
            self._loop._schedule_callbacks(self)
            return 2

        loop=future._loop
        loop.call_soon(self._set_future_result,future,result)
        loop.wakeup()
        return 1
        
    def _set_future_exception(self,future,exception):
        try:
            future.set_exception(exception)
        except (RuntimeError,InvalidStateError): #the future does not supports this operation
            pass

        loop=self._loop
        loop.call_soon(self._set_future_any_re,future)
        loop.wakeup()

    def set_exception(self,exception):
        if self._state is not PENDING:
            raise InvalidStateError(self,'set_exception')

        if isinstance(exception,type):
            exception=exception()
        
        if type(exception) is StopIteration:
             raise TypeError(f'{exception} cannot be raised to a {self.__class__.__name__}: {self!r}')

        future=self._future
        if future is None:
            self._exception=exception
            self._state=FINISHED
            self._loop._schedule_callbacks(self)
            return

        loop=future._loop
        loop.call_soon(self._set_future_exception,future,exception)
        loop.wakeup()

    def set_exception_if_pending(self,exception):
        if self._state is not PENDING:
            return 0
        
        if isinstance(exception,type):
            exception=exception()
        
        if type(exception) is StopIteration:
             raise TypeError(f'{exception} cannot be raised to a {self.__class__.__name__}: {self!r}')

        future=self._future
        if future is None:
            self._exception=exception
            self._state=FINISHED
            self._loop._schedule_callbacks(self)
            return 2

        loop=future._loop
        loop.call_soon(self._set_future_exception,future,exception)
        loop.wakeup()
        return 1
        
    def __iter__(self):
        if self._state is PENDING:
            self._blocking=True
            yield self

        return self.result()

    __await__=__iter__

    if __debug__:
        def __del__(self):
            if not self._loop.running:
                return

            state=self._state
            if state is PENDING:
                if (self._future is not None) or self._callbacks:

                    #ignore being silenced
                    silence_cb=type(self).__silence_cb__
                    for callback in self._callbacks:
                        if callback is silence_cb:
                            return

                    sys.stderr.write(f'{self.__class__.__name__} is not finished, but still pending!\n{self!r}\n')
                return

            if state is FINISHED:
                if (self._exception is not None):
                    self._loop.render_exc_maybe_async(self._exception,[
                        self.__class__.__name__,
                        ' exception was never retrieved\n',
                        self.__repr__(),
                        '\n',])
                return

            #no more notify case

        def __silence__(self):
            state=self._state
            if state is PENDING:
                self._callbacks.append(type(self).__silence_cb__)
                return

            if state is FINISHED:
                self._state=RETRIEVED
                return

        def __silence_cb__(self):
            if self._state is FINISHED:
                self._state=RETRIEVED

    def clear(self):
        future=self._future
        if future is not None:
            loop=future._loop
            loop.call_soon(self._remove_callback,future)
            loop.wakeup()
            self._future=None

        self._state     = PENDING
        self._exception = None
        self._result    = None
        self.cancel_handles()
        self._blocking  = False

class FutureWM(Future):
    __slots__=('_count',)

    def __new__(cls,loop,count):
        self=object.__new__(cls)
        self._loop      = loop
        self._count     = count
        self._state     = PENDING

        self._result    = []
        self._exception = None
        
        self._callbacks = []
        self._blocking=False

        return self

    def __repr__(self):
        result=['<',self.__class__.__name__,' ',self._state]
        if self._state is FINISHED or self._state is RETRIEVED:
            if self._exception is None:
                for index,result_ in enumerate(self._result):
                    result.append(f' result_{index}=')
                    result.append(reprlib.repr(result_))
                result.append(' needed=')
                result.append(str(self._count-len(self._result)))
            else:
                result.append(' exception=')
                result.append(self._exception.__repr__())
        if self._callbacks:
            result.append(' callbacks=[')
            result.append(', '.join([format_callback(callback) for callback in self._callbacks]))
            result.append(']')
        result.append('>')

        return ''.join(result)

    def set_result(self,result):
        if self._state is not PENDING:
            raise InvalidStateError(self,'set_result')
        
        self._result.append(result)
        if self._count!=len(self._result):
            return
            
        self._state=FINISHED
        self._loop._schedule_callbacks(self)

    def set_result_if_pending(self,result):
        if self._state is not PENDING:
            return 0
        
        self._result.append(result)
        if self._count!=len(self._result):
            return 2
            
        self._state=FINISHED
        self._loop._schedule_callbacks(self)
        return 1
        
    def clear(self):
        self._state     = PENDING
        self._exception = None
        self._result.clear()
        self.cancel_handles()
        self._blocking  = False

class Task(Future):
    __slots__=('_coro', '_fut_waiter', '_must_cancel',)

    def __new__(cls,coro,loop):
        self=object.__new__(cls)
        self._loop      = loop
        self._state     = PENDING

        self._result    = None
        self._exception = None
        
        self._callbacks = []
        self._blocking  = False

        self._must_cancel=False
        self._fut_waiter= None
        self._coro      = coro

        loop.call_soon(self.__step)

        return self

    def get_stack(self,limit=-1):
        frames=[]
        
        coro=self._coro
        if isinstance(coro,GeneratorType):
            frame=coro.gi_frame
        elif isinstance(coro,CoroutineType):
            frame=coro.cr_frame
        else:
            frame=None
        
        if frame is None:
            return frames

        while limit:
            limit-=1
            
            if frame in frames:
                frames.append(frame)
                frames.append(None)
                return frames
            
            frames.append(frame)
            
            if isinstance(coro,GeneratorType):
                coro=coro.gi_yieldfrom
            elif isinstance(coro,CoroutineType):
                coro=coro.cr_await
            else:
                coro=None
            
            if coro is not None:
                if isinstance(coro,GeneratorType):
                    frame=coro.gi_frame
                elif isinstance(coro,CoroutineType):
                    frame=coro.cr_frame
                else:
                    frame=None
                
                if frame is not None:
                    continue
            
            self=self._fut_waiter
            if self is None:
                break
            
            del frames[-1]
            if not isinstance(self,Task):
                break
            
            coro=self._coro
            
            if isinstance(coro,GeneratorType):
                frame=coro.gi_frame
            elif isinstance(coro, CoroutineType):
                frame=coro.cr_frame
            else:
                frame=None
                
            if frame is None:
                break
        
        return frames

    def __repr__(self):
        result=['<',self.__class__.__name__,' ',self._state]
        if self._must_cancel:
            result.append(' cancelling')
            
        result.append(' coro=')
        result.append(format_coroutine(self._coro))
        fut_waiter=self._fut_waiter
        if fut_waiter is not None:
            result.append(' wait_for=')
            if type(fut_waiter) is type(self):
                result.append(fut_waiter.qualname)
            else:
                result.append(fut_waiter.__repr__())
        
        if (not self._must_cancel) and (self._state is FINISHED or self._state is RETRIEVED):
            if self._exception is None:
                result.append(' result=')
                result.append(reprlib.repr(self._result))
            else:
                result.append(' exception=')
                result.append(self._exception.__repr__())
                
        if self._callbacks:
            result.append(' callbacks=[')
            result.append(', '.join([format_callback(callback) for callback in self._callbacks]))
            result.append(']')
            
        result.append('>')

        return ''.join(result)
    
    def print_stack(self,limit=-1,file=None):
        local_thread=current_thread()
        if isinstance(local_thread,EventThread):
            return local_thread.run_in_executor(alchemy_incendiary(self._print_stack,(self,limit,file),))
        else:
            self._print_stack(self,limit,file)
    
    @staticmethod
    def _print_stack(self,limit,file):
        if file is None:
            file=sys.stdout

        exception=self._exception
        
        if exception is None:
            frames=self.get_stack(limit)
            if frames:
                recursive = (frames[-1] is None)
                if recursive:
                    del frames[-1]

                extracted=['Stack for ',self.__repr__(),' (most recent call last):\n']
                extracted=render_frames_to_list(frames,extend=extracted)
                if recursive:
                    extracted.append('Last frame is a repeat from a frame above. Rest of the recursive part is not rendered.')
            else:
                extracted=['No stack for ',self.__repr__(),'\n']
        else:
            extracted=render_exc_to_list(exception)
            extracted[0]=f'Traceback for {self!r} (most recent call last):\n'

        file.write(''.join(extracted))
    
    if __debug__:
        def cancel(self):
            state=self._state
            if state is not PENDING:
                if state is FINISHED:
                    self._state=RETRIEVED
                
                return 0
            
            fut_waiter=self._fut_waiter
            if (fut_waiter is None) or (not fut_waiter.cancel()):
                self._must_cancel=True
            
            return 1
        
    else:
        def cancel(self):
            if self._state is not PENDING:
                return 0
            
            fut_waiter=self._fut_waiter
            if (fut_waiter is None) or (not fut_waiter.cancel()):
                self._must_cancel=True
            
            return 1

    @property
    def name(self):
        coro=self._coro
        try:
            return coro.__name__
        except AttributeError:
            return coro.__class__.__name__

    @property
    def qualname(self):
        coro=self._coro
        try:
            return coro.__qualname__
        except AttributeError:
            return coro.__class__.__qualname__
        
    def set_result(self,result):
        raise RuntimeError(f'{self.__class__.__name__} does not support `.set_result` operation')
    
    def set_result_if_pending(self,result):
        raise RuntimeError(f'{self.__class__.__name__} does not support `.set_result_if_pending` operation')
        
    # We will not send an exception to a task, but we will cancel it.
    # The exception will show up as `._exception` tho.
    # We also wont change the state of the Task, it will be changed, when the
    # next `.__step` is done with the cancelling.
    def set_exception(self,exception):
        if self._state is not PENDING:
            raise InvalidStateError(self,'set_exception')
    
        if (self._fut_waiter is None) or self._fut_waiter.pending():
            self._must_cancel=True

        if isinstance(exception,type):
            exception=exception()
            
        if type(exception) is StopIteration:
             raise TypeError(f'{exception} cannot be raised to a {self.__class__.__name__}: {self!r}')
        
        self._exception = exception

    def set_exception_if_pending(self,exception):
        if self._state is not PENDING:
            return 0
        
        if (self._fut_waiter is None) or self._fut_waiter.pending():
            self._must_cancel=True

        if isinstance(exception,type):
            exception=exception()
            
        if type(exception) is StopIteration:
             raise TypeError(f'{exception} cannot be raised to a {self.__class__.__name__}: {self!r}')
        
        self._exception = exception
        return 1

    def clear(self):
        raise RuntimeError(f'{self.__class__.__name__} does not support `.clear` operation')
    
    if __debug__:
        def __step(self,exception=None):
            if self._state is not PENDING:
                raise InvalidStateError.with_message(self,'__step',f'`{self.__class__.__name__}.__step` already done of {self!r}, exception={exception!r}')

            if self._must_cancel:
                exception=self._must_exception(exception)
                
            coro=self._coro
            self._fut_waiter=None

            self._loop.current_task=self
            
            #call either coro.throw(err) or coro.send(None).
            try:
                if exception is None:
                    result=coro.send(None)
                else:
                    result=coro.throw(exception)
            except StopIteration as exception:
                if self._must_cancel:
                    #the task is cancelled meanwhile
                    self._must_cancel=False
                    Future.set_exception(self,CancelledError())
                else:
                    Future.set_result(self,exception.value)
            except CancelledError:
                Future.cancel(self)
            except BaseException as exception:
                Future.set_exception(self,exception)
            else:
                try:
                    if result._blocking:
                        if self._loop is not result._loop:
                            new_exception=RuntimeError(f'{self.__class__.__name__} {self!r} got a Future {result!r} attached to a different loop')
                            self._loop.call_soon(self.__step,new_exception)
                        elif result is self:
                            new_exception=RuntimeError(f'{self.__class__.__name__} cannot await on itself: {self!r}')
                            self._loop.call_soon(self.__step,new_exception)
                        else:
                            result._blocking=False
                            result.add_done_callback(self.__wakeup)
                            self._fut_waiter=result
                            if self._must_cancel:
                                if result.cancel():
                                    self._must_cancel=False
                    else:
                        new_exception=RuntimeError(f'`yield` was used instead of `yield from` in task {self!r} with {result!r}')
                        self._loop.call_soon(self.__step,new_exception)
                except AttributeError:
                    if result is None:
                        #Bare yield relinquishes control for one event loop iteration.
                        self._loop.call_soon(self.__step)
                    elif isinstance(result,GeneratorType):
                        #Yielding a generator is just wrong.
                        new_exception=RuntimeError(f'`yield` was used instead of `yield from` in {self.__class__.__name__} {self!r} with `{result!r}`')
                        self._loop.call_soon(self.__step,new_exception)
                    else:
                        #Yielding something else is an error.
                        new_exception=RuntimeError(f'{self.__class__.__name__} got bad yield: `{result!r}`')
                        self._loop.call_soon(self.__step,new_exception)
            finally:
                self._loop.current_task=None
                self=None #said needed if exception occurs.
    else:
        def __step(self,exception=None):
            if self._state is not PENDING:
                raise InvalidStateError.with_message(self,'__step',f'`{self.__class__.__name__}.__step` already done of {self!r}, exception={exception!r}')

            if self._must_cancel:
                exception=self._must_exception(exception)
                
            coro=self._coro
            self._fut_waiter=None

            self._loop.current_task=self
            
            #call either coro.throw(err) or coro.send(None).
            try:
                if exception is None:
                    result=coro.send(None)
                else:
                    result=coro.throw(exception)
            except StopIteration as exception:
                if self._must_cancel:
                    #the task is cancelled meanwhile
                    self._must_cancel=False
                    Future.set_exception(self,CancelledError())
                else:
                    Future.set_result(self,exception.value)
            except CancelledError:
                Future.cancel(self)
            except BaseException as exception:
                Future.set_exception(self,exception)
            else:
                if hasattr(result,'_blocking'):
                    result._blocking=False
                    result.add_done_callback(self.__wakeup)
                    self._fut_waiter=result
                    if self._must_cancel:
                        if self._fut_waiter.cancel():
                            self._must_cancel=False
                else:
                    self._loop.call_soon(self.__step)

            finally:
                self._loop.current_task=None
                self=None #said needed if exception occurs.
    
    def __wakeup(self,future):
        try:
            future.result()
        except BaseException as err:
            self.__step(err)
        else:
            self.__step()
        self=None

    def _must_exception(self,exception):
        if self._exception is None:
            if (exception is None) or (not isinstance(exception,CancelledError)):
                exception=CancelledError()
        else:
            exception=self._exception
            
        self._must_cancel=False
        return exception

class AsyncQue(object):
    __slots__=('_exception', '_loop', '_results', '_waiter',)
    def __new__(cls,loop,iterable=None,maxlen=None,exception=None):
        self=object.__new__(cls)
        self._loop      = loop
        self._results   = deque(maxlen=maxlen) if iterable is None else deque(iterable,maxlen=maxlen)
        self._waiter    = None
        self._exception = exception
        
        return self
    
    def set_result(self,element):
        #should we raise InvalidStateError?
        waiter=self._waiter
        if waiter is None:
            self._results.append(element)
        else:
            waiter.set_result(element)
            self._waiter=None
    
    def set_exception(self,exception):
        #should we raise InvalidStateError?
        self._exception=exception
        
        waiter=self._waiter
        if waiter is not None:
            waiter.set_exception(exception)
            self._waiter=None
    
    async def result(self):
        if self._results:
            return self._results.popleft()
        
        waiter=self._waiter
        if waiter is None:
            waiter=Future(self._loop)
            self._waiter=waiter
        
        return (await waiter)
    
    def result_no_wait(self):
        results=self._results
        if results:
            return results.popleft()
        
        exception=self._exception
        if exception is None:
            raise IndexError('The queue is empty')
        
        raise exception
    
    def __await__(self):
        return self.result().__await__()

    def __repr__(self):
        results=self._results
        maxlen=results.maxlen
        exception=self._exception
        return f'{self.__class__.__name__}([{", ".join([repr(element) for element in results])}]{"" if maxlen is None else f", maxlen={maxlen}"} {"" if exception is None else f", exception={exception}"})'

    __str__=__repr__
    
    def __aiter__(self):
        return self

    #should we raise StopAsyncIteration instead of the set one?
    __anext__=result
    

    #deque operations
    
    @property
    def maxlen(self):
        return self._results.maxlen
    
    def clear(self):
        self._results.clear()
    
    def copy(self):
        new=object.__new__(type(self))
        new._loop       = self._loop
        new._results    = self._results.copy()
        new._waiter     = None
        new._exception  = self._exception
        
        return new
        
    def __iter__(self):
        return self._results.__iter__()
    
    def __reversed__(self):
        return self._results.__reversed__()
    
    def reverse(self):
        self._results.reverse()
    
    def __len__(self):
        return self._results.__len__()
    
    if __debug__:
        def __del__(self):
            waiter=self._waiter
            if waiter is not None:
                waiter.__silence__()

class FutureG(FutureWM):
    __slots__=('_blocking', '_callbacks', '_count', '_exception', '_loop', '_result', '_state',)
    
    class _Element(object):
        __slots__=('exception', 'result',)
        def __init__(self,result,exception):
            self.result=result
            self.exception=exception
        def __call__(self):
            exception=self.exception
            if exception is None:
                return self.result
            raise exception

    def __new__(cls,loop,count):
        self=object.__new__(cls)
        self._loop      = loop
        self._count     = count
        self._state     = PENDING
        
        self._result    = []
        self._exception = None
        
        self._callbacks = []
        self._blocking  = False
        
        return self

    def set_result(self,result):
        if self._state is not PENDING:
            raise InvalidStateError(self,'set_result')
            
        self._result.append(self._Element(result,None))
        if self._count!=len(self._result):
            return
            
        self._state=FINISHED
        self._loop._schedule_callbacks(self)

    def set_result_if_pending(self,result):
        if self._state is not PENDING:
            return 0
        
        self._result.append(self._Element(result,None))
        if self._count!=len(self._result):
            return 2
            
        self._state=FINISHED
        self._loop._schedule_callbacks(self)
        return 1
        
    def set_exception(self,exception):
        if self._state is not PENDING:
            raise InvalidStateError(self,'set_exception')
            
        self._result.append(self._Element(None,exception))
        if self._count!=len(self._result):
            return
            
        self._state=FINISHED
        self._loop._schedule_callbacks(self)

    def set_exception_if_pending(self,exception):
        if self._state is not PENDING:
            return 0
        
        self._result.append(self._Element(None,exception))
        if self._count!=len(self._result):
            return 2
            
        self._state=FINISHED
        self._loop._schedule_callbacks(self)
        return 1
    
class _gather_callback(object):
    __slots__=('target',)
    def __init__(self,target):
        self.target=target
    def __call__(self,future):
        try:
            result=future.result()
        except BaseException as err:
            self.target.set_exception_if_pending(err)
        else:
            self.target.set_result_if_pending(result)

def gather(coros_or_futures,loop):
    gatherer=FutureG(loop,len(coros_or_futures))
    for awaitable in coros_or_futures:
        task=loop.ensure_future(awaitable)
        task.add_done_callback(_gather_callback(gatherer))
    
    return gatherer

class _handle_base(object):
    __slots__=('handler',)
    def __init__(self):
        self.handler=None
    
    def __call__(self,future):
        pass
    
    def cancel(self):
        handler=self.handler
        if handler is None:
            return
            
        handler.cancel()
        self.handler=None

class _cancel_handle(_handle_base):
    __slots__=('handler',)
    def __call__(self,future):
        handler=self.handler
        if handler is None:
            return
        
        handler.cancel()
        self.handler=None
        future.set_result_if_pending(None)

def sleep(delay,loop=None):
    if loop is None:
        loop = current_thread()
        if not isinstance(loop,EventThread):
            raise RuntimeError(f'`sleep` called without passing `loop` argument from a non {EventThread.__name__}: {loop!r}.')
    future=Future(loop)
    if delay<=0.:
        future.set_result(None)
        return future
    callback=object.__new__(_cancel_handle)
    handler=loop.call_later(delay,callback,future)
    future._callbacks.append(callback)
    callback.handler=handler
    return future

class _timeout_handle(_handle_base):
    __slots__=('handler',)
    def __call__(self,future):
        handler=self.handler
        if handler is None:
            return
        
        handler.cancel()
        self.handler=None
        future.set_exception_if_pending(TimeoutError())

def future_or_timeout(future,timeout):
    loop=future._loop
    callback=_timeout_handle()
    handler=loop.call_later(timeout,callback,future)
    if handler is None:
        raise RuntimeError(f'`future_or_timeout` was called with future with a closed loop {loop!r}')
    callback.handler=handler
    future.add_done_callback(callback)

class _future_chainer(object):
    __slots__=('target',)
    def __init__(self,target):
        self.target=target
    
    if __debug__:
        def __call__(self,future):
            #remove chain remover
            callbacks=self.target._callbacks
            for index in range(len(callbacks)):
                callback=callbacks[index]
                if (type(callback) is _chain_remover) and (callback.target is future):
                    del callbacks[index]
                    break
            #set result
            state=future._state
            if state is FINISHED:
                future._state=RETRIEVED
                if future._exception is None:
                    self.target.set_result(future._result)
                else:
                    self.target.set_exception(future._exception)
                return
            if state is RETRIEVED:
                if future._exception is None:
                    self.target.set_result(future._result)
                else:
                    self.target.set_exception(future._exception)
                return
            #if state is CANCELLED: normally, but the future can be cleared as well.
            self.target.cancel()
    
    else:
        def __call__(self,future):
            #remove chain remover
            callbacks=self.target._callbacks
            for index in range(len(callbacks)):
                callback=callbacks[index]
                if type(callback) is _chain_remover and callback.target is future:
                    del callbacks[index]
                    break
            #set result
            if future._state is FINISHED:
                if future._exception is None:
                    self.target.set_result(future._result)
                else:
                    self.target.set_exception(future._exception)
                return
            #if state is CANCELLED: normally, but the future can be cleared as well.
            self.target.cancel()

class _chain_remover(object):
    __slots__=('target',)
    def __init__(self,target):
        self.target=target

    def __call__(self,future):
        #remove chainer
        callbacks=self.target._callbacks
        for index in range(len(callbacks)):
            callback=callbacks[index]
            if (type(callback) is _future_chainer) and (callback.target is future):
                del callbacks[index]
                if __debug__:
                    # because this is might be the only place, where we
                    # retrieve the result, we will just silence it.
                    future.__silence__()
                break

def shield(awaitable,loop):
    protected=loop.ensure_future(awaitable)
    if protected._state is not PENDING:
        return protected #already done, we can return

    un_protected=Future(loop)
    protected._callbacks.append(_future_chainer(un_protected))
    un_protected._callbacks.append(_chain_remover(protected))
    return un_protected

class WaitTillFirst(Future):
    __slots__=('_callback')
    
    def __new__(cls,futures,loop):
        pending         = set(futures)
        done            = set()
        
        self            = object.__new__(cls)
        self._loop      = loop
        
        callback        = cls._wait_callback(self)
        self._callback  = callback
        
        if pending:
            for future in pending:
                future.add_done_callback(callback)
            
            self._state = PENDING
        else:
            self._state = FINISHED
        
        self._result    = (done,pending)
        self._exception = None
        
        self._callbacks = []
        self._blocking  = False

        return self
    
    # `__repr__` is same as `Future.__repr__`

    class _wait_callback(object):
        __slots__=('_parent',)
        
        def __init__(self,parent):
            self._parent=parent
            
        def __call__(self,future):
            parent=self._parent
            if parent is None:
                return
            
            done,pending=parent._result
            
            pending.remove(future)
            done.add(future)
            
            parent._state=FINISHED
            parent._loop._schedule_callbacks(parent)
            self._parent=None
        
    @property
    def futures_done(self):
        return self._result[0]
    
    @property
    def futures_pending(self):
        return self._result[1]
    
    # cancels the future, but every pending one as well.
    if __debug__:
        def cancel(self):
            state=self._state
            if state is not PENDING:
                if state is FINISHED:
                    self._state=RETRIEVED
                
                return 0
                
            self._callback._parent=None
            for future in self._result[1]:
                future.cancel()
            
            self._state=CANCELLED
            self._loop._schedule_callbacks(self)
            return 1
    
    else:
        def cancel(self):
            if self._state is not PENDING:
                return 0
                
            self._callback._parent=None
            for future in self._result[1]:
                future.cancel()
            
            self._state=CANCELLED
            self._loop._schedule_callbacks(self)
            return 1
    
    # `cancelled` is same as `Future.cancelled`
    # `done` is same as `Future.done`
    # `pending` is same as `Future.pending`
    # `result` is same as `Future.result`
    # `exception` is same as `Future.exception`
    # `add_done_callback` is same as `Future.add_done_callback`
    # `remove_done_callback` is same as `Future.remove_done_callback`

    def set_result(self,result):
        raise RuntimeError(f'{self.__class__.__name__} does not support `set_result` operation')

    def set_result_if_pending(self,result):
        raise RuntimeError(f'{self.__class__.__name__} does not support `set_result_if_pending` operation')
    
    def set_exception(self,exception):
        if self._state is not PENDING:
            raise InvalidStateError(self,'set_exception')
        
        if isinstance(exception,type):
            exception=exception()
        
        if type(exception) is StopIteration:
             raise TypeError(f'{exception} cannot be raised to a {self.__class__.__name__}: {self!r}')
            
        self._callback._parent=None
        self._state     = FINISHED
        self._loop._schedule_callbacks(self)

        if type(exception) is not TimeoutError:
            self._exception = exception
        
    def set_exception_if_pending(self,exception):
        if self._state is not PENDING:
            return 0
        
        if isinstance(exception,type):
            exception=exception()
        
        if type(exception) is StopIteration:
             raise TypeError(f'{exception} cannot be raised to a {self.__class__.__name__}: {self!r}')
            
        self._callback._parent=None
        self._state     = FINISHED
        self._loop._schedule_callbacks(self)

        if type(exception) is TimeoutError:
            return 2
            
        self._exception = exception
        return 1
    
    # `__iter__` is same as `Future.__iter__`
    # `__await__` is same as `Future.__await__`
    # if __debug__:
    #    `__del__` is same as `Future.__del__`
    #    `__silence__` is same as `Future.__silence__`
    #    `__silence_cb__` is same as `Future.__silence_cb__`
    # `cancel_handles` is same as `Future.cancel_handles`
    
    def clear(self):
        raise RuntimeError(f'{self.__class__.__name__} does not support `.clear` operation')
    
    # `syncwrap` is same as `Future.syncwrap`
    # `asyncwrap` is same as `Future.asyncwrap`
    
class WaitTillExc(WaitTillFirst):
    __slots__=()
    # `__new__` is same as `WaitTillFirst.__new__`
    # `__repr__` is same as `Future.__repr__`

    class _wait_callback(object):
        __slots__=('_parent',)
        
        def __init__(self,parent):
            self._parent=parent
        
        def __call__(self,future):
            parent=self._parent
            if parent is None:
                return
            
            done,pending=parent._result
            
            pending.remove(future)
            done.add(future)
            
            if (future._exception is None) and pending:
                return
            
            parent._state=FINISHED
            parent._loop._schedule_callbacks(parent)
            self._parent=None
    
    # `futures_done` is same as `WaitTillFirst.futures_done`
    # `futures_pending` is same as `WaitTillFirst.futures_pending`
    # `cancel` is same as `WaitTillFirst.cancel`
    # `cancelled` is same as `Future.cancelled`
    # `done` is same as `Future.done`
    # `pending` is same as `Future.pending`
    # `result` is same as `Future.result`
    # `exception` is same as `Future.exception`
    # `add_done_callback` is same as `Future.add_done_callback`
    # `remove_done_callback` is same as `Future.remove_done_callback`
    # `set_result` is same as `WaitTillFirst.set_result`
    # `set_result_if_pending` is same as `WaitTillFirst.set_result_if_pending`
    # `set_exception` is same as `WaitTillFirst.set_exception`
    # `set_exception_if_pending` is same as `WaitTillFirst.set_exception_if_pending`
    # `__iter__` is same as `Future.__iter__`
    # `__await__` is same as `Future.__await__`
    # if __debug__:
    #    `__del__` is same as `Future.__del__`
    #    `__silence__` is same as `Future.__silence__`
    #    `__silence_cb__` is same as `Future.__silence_cb__`
    # `cancel_handles` is same as `Future.cancel_handles`
    # `clear` is same as `WaitTillFirst.clear`
    # `sleep` is same as `WaitTillFirst.clear`
    # `syncwrap` is same as `Future.cancel_handles`
    # `asyncwrap` is same as `Future.cancel_handles`

class WaitTillAll(WaitTillFirst):
    __slots__=()
    # `__new__` is same as `WaitTillFirst.__new__`
    # `__repr__` is same as `Future.__repr__`

    class _wait_callback(object):
        __slots__=('_parent',)
        
        def __init__(self,parent):
            self._parent=parent
            
        def __call__(self,future):
            parent=self._parent
            if parent is None:
                return
            
            done,pending=parent._result
            
            pending.remove(future)
            done.add(future)
            
            if pending:
                return
            
            parent._state=FINISHED
            parent._loop._schedule_callbacks(parent)
            self._parent=None
    
    # `futures_done` is same as `WaitTillFirst.futures_done`
    # `futures_pending` is same as `WaitTillFirst.futures_pending`
    # `cancel` is same as `WaitTillFirst.cancel`
    # `cancelled` is same as `Future.cancelled`
    # `done` is same as `Future.done`
    # `pending` is same as `Future.pending`
    # `result` is same as `Future.result`
    # `exception` is same as `Future.exception`
    # `add_done_callback` is same as `Future.add_done_callback`
    # `remove_done_callback` is same as `Future.remove_done_callback`
    # `set_result` is same as `WaitTillFirst.set_result`
    # `set_result_if_pending` is same as `WaitTillFirst.set_result_if_pending`
    # `set_exception` is same as `WaitTillFirst.set_exception`
    # `set_exception_if_pending` is same as `WaitTillFirst.set_exception_if_pending`
    # `__iter__` is same as `Future.__iter__`
    # `__await__` is same as `Future.__await__`
    # if __debug__:
    #    `__del__` is same as `Future.__del__`
    #    `__silence__` is same as `Future.__silence__`
    #    `__silence_cb__` is same as `Future.__silence_cb__`
    # `cancel_handles` is same as `Future.cancel_handles`
    # `clear` is same as `WaitTillFirst.clear`
    # `sleep` is same as `WaitTillFirst.clear`
    # `syncwrap` is same as `Future.cancel_handles`
    # `asyncwrap` is same as `Future.cancel_handles`

class Lock(object):
    __slots__ = ('_loop', '_waiters', )
    def __new__(cls, loop):
        self            = object.__new__(cls)
        self._loop      = loop
        self._waiters   = deque()
        return self
    
    async def __aenter__(self):
        future=Future(self._loop)
        waiters=self._waiters
        waiters.appendleft(future)
        if waiters.__len__()>1:
            await waiters[1]

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        future=self._waiters.pop()
        future.set_result_if_pending(None)
    
    # returns True if the Lock is entered anywhere
    def locked(self):
        if self._waiters:
            return True
        return False
    
    # Blocks until all the lock is unlocked everywhere.
    # If lock is used meanwhile, we will await that as well.
    def __iter__(self):
        waiters = self._waiters
        while waiters:
            yield from waiters[0]
    
    __await__=__iter__
    
    def __repr__(self):
        result=['<',self.__class__.__name__,' locked=']
        count=self._waiters.__len__()
        if count:
            result.append('True, waiting=')
            result.append(count.__repr__())
        else:
            result.append('False')
        result.append('>')
        
        return ''.join(result)

class enter_executor(object):
    __slots__= ('_enter_future', '_exit_future', '_fut_waiter', '_task')
    def __init__(self):
        self._enter_future=None
        self._task=None
        self._exit_future=None
        self._fut_waiter=None
        
    async def __aenter__(self):
        thread = current_thread()
        if not isinstance(thread,EventThread):
            raise RuntimeError(f'{self.__class__.__name__} used outside of {EventThread.__name__}, at {thread!r}')
        
        task = thread.current_task
        if task is None:
            raise RuntimeError(f'{self.__class__.__name__} used outside of a {Task.__name__}')
        
        self._task=task
        loop=task._loop
        future = Future(loop)
        self._enter_future = future
        loop.call_soon(self._enter_executor)
        await future
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._exit_future
        return False
    
    def _enter_executor(self):
        callbacks=self._enter_future._callbacks
        callbacks.clear()
        
        task=self._task
        task.add_done_callback(self._cancel_callback)
        
        task._loop.run_in_executor(self._executor_task)
    
    def _cancel_callback(self,future):
        if future._state is not CANCELLED:
            return
        
        fut_waiter=self._fut_waiter
        if fut_waiter is None:
            return
        
        fut_waiter.cancel()
        
    def _executor_task(self):
        task=self._task
        # relink future task
        loop=task._loop
        end_future=Future(loop)
        task._fut_waiter=end_future
        self._exit_future=end_future
        
        # Set result to the enter task, so it can be retrieved.
        self._enter_future.set_result(None)
        
        exception=None
        coro=task._coro

        # If some1 await at the block, we will syncwrap it. If the exit future
        # is awaited, then we quit.
        local_fut_waiter=None
        
        try:
            while True:
                if task._must_cancel:
                    exception=task._must_exception(exception)
                    
                if (local_fut_waiter is not None):
                    if local_fut_waiter is end_future:
                        end_future.set_result(None)
                        loop.call_soon_threadsafe(task._Task__step,exception)
                        break
                    
                    try:
                        self._fut_waiter=local_fut_waiter
                        if type(exception) is CancelledError:
                            local_fut_waiter.cancel()
                        local_fut_waiter.syncwrap().wait()
                    
                    except CancelledError:
                        break
                    except BaseException as err:
                        exception=err
                    finally:
                        local_fut_waiter=None
                        self._fut_waiter=None
                
                if task._state is not PENDING:
                    # there is no reason to raise
                    break
                
                # call either coro.throw(err) or coro.send(None).
                try:
                    if exception is None:
                        result=coro.send(None)
                    else:
                        result=coro.throw(exception)
                
                except StopIteration as exception:
                    if task._must_cancel:
                        #the task is cancelled meanwhile
                        task._must_cancel=False
                        Future.set_exception(task,CancelledError())
                    else:
                        Future.set_result(task,exception.value)
                    
                    loop.wakeup()
                    break
                    
                except CancelledError:
                    Future.cancel(task)
                    loop.wakeup()
                    break
                
                except BaseException as exception:
                    Future.set_exception(task,exception)
                    loop.wakeup()
                    break
                
                else:
                    try:
                        blocking=result._blocking
                    except AttributeError:
                        if result is None:
                            # bare yield relinquishes control for one event loop iteration.
                            continue
                        
                        elif isinstance(result,GeneratorType):
                            #Yielding a generator is just wrong.
                            exception=RuntimeError(f'`yield` was used instead of `yield from` in {self.__class__.__name__} {self!r} with `{result!r}`')
                            continue
                            
                        else:
                            # yielding something else is an error.
                            exception=RuntimeError(f'{self.__class__.__name__} got bad yield: `{result!r}`')
                            continue
                    else:
                        if blocking:
                            if loop is not result._loop:
                                exception=RuntimeError(f'{self.__class__.__name__} {self!r} got a Future {result!r} attached to a different loop')
                                continue
                                
                            elif result is self:
                                exception=RuntimeError(f'{self.__class__.__name__} cannot await on itself: {self!r}')
                                continue
                            
                            else:
                                result._blocking=False
                                local_fut_waiter=result
                                if task._must_cancel:
                                    if local_fut_waiter.cancel():
                                        task._must_cancel=False
                                
                                continue
                        else:
                            exception=RuntimeError(f'`yield` was used instead of `yield from` in task {self!r} with {result!r}')
                            continue
        finally:
            task.remove_done_callback(self._cancel_callback)
            self=None
            task=None
