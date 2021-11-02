# -*- coding: utf-8 -*-
__all__ = ('AsyncLifoQueue', 'AsyncQueue', 'CancelledError', 'Event', 'Future', 'FutureAsyncWrapper',
    'FutureSyncWrapper', 'FutureWM', 'Gatherer', 'InvalidStateError', 'Lock', 'ScarletExecutor', 'ScarletLock', 'Task',
    'WaitContinuously', 'WaitTillAll', 'WaitTillExc', 'WaitTillFirst', 'enter_executor', 'future_or_timeout',
    'is_awaitable', 'is_coroutine', 'is_coroutine_function', 'is_coroutine_generator',
    'is_coroutine_generator_function', 'shield', 'skip_ready_cycle', 'sleep', )

import sys, reprlib, linecache
from types import GeneratorType, CoroutineType, AsyncGeneratorType, MethodType, FunctionType

from collections import deque
from threading import current_thread, Lock as SyncLock, Event as SyncEvent

from .utils import alchemy_incendiary, copy_func, copy_docs, set_docs
from .analyzer import CO_ASYNC_GENERATOR, CO_COROUTINE_ALL, CO_GENERATOR, CO_ITERABLE_COROUTINE
from .export import export, include

EventThread = include('EventThread')


class CancelledError(BaseException):
    """The Future or Task was cancelled."""

class InvalidStateError(Exception):
    """
    The operation is not allowed in this state.
    
    Attributes
    ----------
    future : ``Future`` instance.
        The future, from what's method the exception was raised.
    func_name : `str`
        The future's function's name, from where the exception was raised.
    _message : `None` or `str`
        Internal cache for the ``.message`` property.
    """
    def __init__(self, future, func_name, message=None):
        """
        Creates a new ``InvalidStateError`` instance.
        
        Parameters
        ----------
        future : ``Future`` instance.
            The future, from what's method the exception was raised.
        func_name : `str`
            The future's function's name, from where the exception was raised.
        message : `str`
            The exception's message. If not defined, then the exception will generate it by itself.
        """
        self.future = future
        self.func_name = func_name
        self._message = message
    
    def __repr__(self):
        """Returns the exception's representation."""
        return f'{self.__class__.__name__}: {self.message}'
    
    __str__ = __repr__
    
    @property
    def message(self):
        """
        Returns the exception's message.
        
        Returns
        -------
        message : `str`
        
        Notes
        -----
        If the exception was created wia ``.__init__``, without giving defining the `message` parameter, then the
        exception's message is generated only when this property is retrieved for the first time.
        """
        message = self._message
        if message is None:
            future = self.future
            message = (f'`{future.__class__.__name__}.{self.func_name}` was called, when `.state` is {future._state} '
               f'of {future!r}')
            self._message = message
        
        return message


@export
def is_coroutine_function(func):
    """
    Returns whether the given `obj` is a coroutine function, so is created with `async def`.
    
    Parameters
    ----------
    func : `Any`
    
    Returns
    -------
    is_coroutine_function : `bool`
    """
    if isinstance(func, (FunctionType, MethodType)) and func.__code__.co_flags&CO_COROUTINE_ALL:
        return True
    else:
        return False


@export
def is_coroutine_generator_function(func):
    """
    Returns whether the given `obj` is a coroutine generator function, so is created with `async def` and uses `yield`
    statement.
    
    Parameters
    ----------
    func : `Any`
    
    Returns
    -------
    is_coroutine_function_generator : `bool`
    """
    if isinstance(func, (FunctionType, MethodType)) and func.__code__.co_flags&CO_ASYNC_GENERATOR:
        return True
    else:
        return False


def is_coroutine(obj):
    """
    Returns whether the given `obj` is a coroutine created by an `async def` function.
    
    Parameters
    ----------
    obj : `Any`
    
    Returns
    -------
    is_coroutine : `bool`
    """
    return isinstance(obj, (CoroutineType, GeneratorType))


def is_awaitable(obj):
    """
    Returns whether the given `obj` can be used in `await` expression.
    
    Parameters
    ----------
    obj : `Any`
    
    Returns
    -------
    is_awaitable : `bool`
    """
    if isinstance(obj, (CoroutineType, GeneratorType)):
        return True
        
    if isinstance(obj, Future):
        return True
    
    if hasattr(obj.__class__, '__await__'):
        return True
    
    return False


def is_coroutine_generator(obj):
    """
    Returns whether the given `obj` is a coroutine generator created by an `async def` function, and can be used inside
    of an `async for` loop.
    
    Returns
    -------
    is_coroutine_generator : `bool`
    """
    if isinstance(obj, AsyncGeneratorType):
        code = obj.ag_code
    elif isinstance(obj, CoroutineType):
        code = obj.cr_code
    elif isinstance(obj, GeneratorType):
        code = obj.gi_code
    else:
        return False
    
    if code.co_flags&CO_ASYNC_GENERATOR:
        return True
    
    return False


if sys.version_info >= (3, 8, 0):
    def to_coroutine(function):
        if not isinstance(function, FunctionType):
            raise TypeError(f'`function` can only be `{FunctionType.__name__}`, got {function.__class__.__name__}; '
                f'{function!r}.')
        
        code_object = function.__code__
        code_flags = code_object.co_flags
        if code_flags&CO_COROUTINE_ALL:
            return function
        
        if not code_flags&CO_GENERATOR:
            raise TypeError(f'`function` can only be given as generator or as coroutine type, got {function!r}, '
                f'co_flags={code_flags!r}.')
        
        function.__code__ = type(code_object)(
            code_object.co_argcount,
            code_object.co_posonlyargcount,
            code_object.co_kwonlyargcount,
            code_object.co_nlocals,
            code_object.co_stacksize,
            code_flags | CO_ITERABLE_COROUTINE,
            code_object.co_code,
            code_object.co_consts,
            code_object.co_names,
            code_object.co_varnames,
            code_object.co_filename,
            code_object.co_name,
            code_object.co_firstlineno,
            code_object.co_lnotab,
            code_object.co_freevars,
            code_object.co_cellvars,
        )
        
        return function
else:
    def to_coroutine(function):
        if not isinstance(function, FunctionType):
            raise TypeError(f'`function` can only be `{FunctionType.__name__}`, got {function.__class__.__name__}; '
                f'{function!r}.')
        
        code_object = function.__code__
        code_flags = code_object.co_flags
        if code_flags&CO_COROUTINE_ALL:
            return function
        
        if not code_flags&CO_GENERATOR:
            raise TypeError(f'`function` can only be given as generator or as coroutine type, got {function!r}, '
                f'co_flags={code_flags!r}.')
        
        function.__code__ = type(code_object)(
            code_object.co_argcount,
            code_object.co_kwonlyargcount,
            code_object.co_nlocals,
            code_object.co_stacksize,
            code_flags | CO_ITERABLE_COROUTINE,
            code_object.co_code,
            code_object.co_consts,
            code_object.co_names,
            code_object.co_varnames,
            code_object.co_filename,
            code_object.co_name,
            code_object.co_firstlineno,
            code_object.co_lnotab,
            code_object.co_freevars,
            code_object.co_cellvars,
        )
        
        return function

set_docs(to_coroutine,
    """
    Transforms the given generator function to coroutine function.
    
    Parameters
    ----------
    function : ``FunctionType``
        The generator function.
    
    Returns
    -------
    function : ``FunctionType``
    
    Raises
    ------
    TypeError
        - `function`'s type is incorrect.
        - `Function` cannot be turned to coroutine.
    """)

# future states

PENDING = 'PENDING'
CANCELLED = 'CANCELLED'
FINISHED = 'FINISHED'
RETRIEVED = 'RETRIEVED'

# If we run without `-o` or -oo` flag, we have 4 future states instead of the regular 3. Well, we have 4 anyways, we
# just wont use it. The only exceptions are the `__repr__` methods, where we still check it's existence. These flags 
# also remove the `__del__` notifications and the `__silence__` methods too. Also bad Task awaiting cases are removed
# too. That's why more methods, which interact with these variables have 2 versions. 1 optimized and 1 debug :^)


def try_get_raw_exception_representation(exception):
    """
    Tries to get raw exception representation.
    
    Parameters
    ----------
    exception : ``BaseException``
        The respective exception instance.
    
    Returns
    -------
    raw_exception_representation : `str`
    """
    raw_exception_representation_parts = [
        '> repr(exception) raised, trying to get raw representation.\n'
    ]
    
    exception_name = getattr(type(exception), '__name__')
    if type(exception_name) is str:
        pass
    elif isinstance(exception_name, str):
        try:
            exception_name = str(exception_name)
        except:
            exception_name = '<Exception>'
    else:
        exception_name = '<Exception>'
    
    raw_exception_representation_parts.append(exception_name)
    raw_exception_representation_parts.append('(')
    
    try:
        args = getattr(exception, 'args', None)
    except:
        pass
    else:
        if (args is not None) and (type(args) is tuple):
            length = len(args)
            if length:
                index = 0
                while True:
                    element = args[index]
                    
                    try:
                        element_representation = repr(element)
                    except:
                        element_representation = f'<parameter_{index}>'
                    else:
                        if type(element_representation) is not str:
                            try:
                                element_representation = str(element_representation)
                            except:
                                element_representation = f'<parameter_{index}>'
                    
                    raw_exception_representation_parts.append(element_representation)
                    
                    index += 1
                    if index == length:
                        break
                    
                    raw_exception_representation_parts.append(', ')
                    continue
        
    
    raw_exception_representation_parts.append(')')
    return ''.join(raw_exception_representation_parts)


def get_exception_representation(exception):
    """
    Gets the exception's representation.
    
    Parameters
    ----------
    exception : ``BaseException``
        The respective exception instance.
    
    Returns
    -------
    exception_representation : `str`
    """
    try:
        exception_representation = repr(exception)
    except:
        exception_representation = try_get_raw_exception_representation(exception)
    
    return exception_representation


_IGNORED_FRAME_INFOS = {}
def _ignore_frame(file, name, line):
    """
    When rendering an exception traceback, specified frames can be added to being stopped from rendering.
    
    Parameters
    ----------
    file : `str`
        The name of the respective file.
    name : `str`
        The name of the respective function.
    line : `str`
        The respective line's stripped content.
    """
    try:
        file_s = _IGNORED_FRAME_INFOS[file]
    except KeyError:
        file_s = {}
        _IGNORED_FRAME_INFOS[file] = file_s

    try:
        name_s = file_s[name]
    except KeyError:
        name_s = set()
        file_s[name] = name_s

    name_s.add(line)
        
def _should_ignore_frame(file, name, line):
    """
    Returns whether the given frame should be ignored from rending.
    
    Parameters
    ----------
    file : `str`
        The frame's respective file's name.
    name : `str`
        The frame's respective function's name.
    line : `str`
        The frame's respective stripped line.
    
    Returns
    -------
    should_ignore : `bool`
    """
    try:
        file_s = _IGNORED_FRAME_INFOS[file]
    except KeyError:
        return False

    try:
        name_s = file_s[name]
    except KeyError:
        return False
    
    return (line in name_s)

_ignore_frame(__spec__.origin, 'result', 'raise exception', )
_ignore_frame(__spec__.origin, 'result_no_wait', 'raise exception', )
_ignore_frame(__spec__.origin, '__call__', 'raise exception', )
_ignore_frame(__spec__.origin, '_step', 'result = coro.throw(exception)', )
_ignore_frame(__spec__.origin, '__iter__', 'yield self', )
_ignore_frame(__spec__.origin, '_step', 'result = coro.send(None)', )
_ignore_frame(__spec__.origin, '_wake_up', 'future.result()', )
_ignore_frame(__spec__.origin, 'wait', 'return self.result()', )
_ignore_frame(__spec__.origin, '__call__', 'future.result()', )
_ignore_frame(__spec__.origin, '__aexit__', 'raise exception', )


from . import utils
_ignore_frame(utils.__spec__.origin, '__call__', 'return self.func(*self.args)', )
_ignore_frame(utils.__spec__.origin, '__call__', 'return self.func(*self.args, **kwargs)', )
del utils

def render_frames_to_list(frames, extend=None):
    """
    Renders the given frames into a list of strings.
    
    Parameters
    ----------
    frames : `list` of (`frame` or ``_EXCFrameType``)
        The frames to render.
    extend : `None` or `list` of `str`
        Whether the frames should be rendered into an already existing list.
    
    Returns
    -------
    extend : `list` of `str`
        The rendered frames as a `list` of it's string parts.
    """
    if extend is None:
        extend = []
    checked = set()
    
    last_file_name = ''
    last_line_number = ''
    last_name = ''
    count = 0
    
    for frame in frames:
        line_number = frame.f_lineno
        code = frame.f_code
        file_name = code.co_filename
        name = code.co_name
        
        if last_file_name == file_name and last_line_number == line_number and last_name == name:
            count += 1
            if count > 2:
                continue
        else:
            if count > 3:
                count -= 3
                extend.append('  [Previous line repeated ')
                extend.append(str(count))
                extend.append(' more times]\n')
            count = 0
        
        if file_name not in checked:
            checked.add(file_name)
            linecache.checkcache(file_name)
        
        line = linecache.getline(file_name, line_number, None)
        line = line.strip()
        
        if _should_ignore_frame(file_name, name, line):
            continue
        
        last_file_name = file_name
        last_line_number = line_number
        last_name = code.co_name
        
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
        
    if count > 3:
        count -= 3
        extend.append('  [Previous line repeated ')
        extend.append(str(count))
        extend.append(' more times]\n')
    
    return extend

class _EXCFrameType:
    """
    Wraps a `traceback` object to be `frame` compatible.
    
    Attributes
    ----------
    tb : `traceback`
        The wrapped traceback frame.
    """
    __slots__ = ('tb',)
    
    def __init__(self, tb):
        """
        Creates a new ``_EXCFrameType`` instance with the given traceback.
        
        tb : `traceback`
            The traceback to wrap.
        """
        self.tb = tb
    
    @property
    def f_builtins(self):
        """
        Returns the traceback's frame's builtins.
        
        Returns
        -------
        f_builtins : `dict` of (`str`, `Any`) items
        """
        return self.tb.tb_frame.f_builtins
    
    @property
    def f_code(self):
        """
        Returns the traceback's frame's code.
        
        Returns
        -------
        f_code : `code`
        """
        return self.tb.tb_frame.f_code
    
    @property
    def f_globals(self):
        """
        Returns the traceback's frame's globals.
        
        Returns
        -------
        f_globals : `dict` of (`str`, `Any`)
        """
        return self.tb.tb_frame.f_globals
    
    @property
    def f_lasti(self):
        """
        Returns the traceback's frame's last attempted instruction index in the bytecode.
        
        Returns
        -------
        f_lasti : `int`
        """
        return self.tb.tb_frame.f_lasti
    
    @property
    def f_lineno(self):
        """
        Returns the traceback's frame's current line number in Python source code.
        
        Returns
        -------
        f_lineno : `int`
        """
        return self.tb.tb_lineno
    
    @property
    def f_locals(self):
        """
        Returns the local variables, what the traceback's frame can see.
        
        Returns
        -------
        f_locals : `dict` of (`str`, `Any`)
        """
        return self.tb.tb_frame.f_locals
    
    @property
    def f_trace(self):
        """
        Tracing function for the traceback's frame.
        
        Returns
        -------
        f_trace : `Any`
            Defaults to `None`.
        """
        return self.tb.tb_frame.f_trace

def _get_exc_frames(exception):
    """
    Gets the frames of the given exception.
    
    Parameters
    ----------
    exception : `BaseException` instance
        The exception to trace back.
    
    Returns
    -------
    frames : `list` of ``_EXCFrameType``
        A list of `frame` compatible exception frames.
    """
    frames = []
    tb = exception.__traceback__
    
    while True:
        if tb is None:
            break
        frame = _EXCFrameType(tb)
        frames.append(frame)
        tb = tb.tb_next
    
    return frames

def render_exc_to_list(exception, extend=None):
    """
    Renders the given exception's frames into a list of strings.
    
    Parameters
    ----------
    exception : `BaseException` instance
        The exception to render.
    extend : `None` or `list` of `str`
        Whether the frames should be rendered into an already existing list.
    
    Returns
    -------
    extend : `list` of `str`
        The rendered frames as a `list` of it's string parts.
    """
    if extend is None:
        extend = []
    
    exceptions = []
    reason_type = 0
    while True:
        exceptions.append((exception, reason_type))
        cause_exception = exception.__cause__
        if (cause_exception is not None):
            exception = cause_exception
            reason_type = 1
            continue
        
        context_exception = exception.__context__
        if (context_exception is not None):
            exception = context_exception
            reason_type = 2
            continue
        
        # no other cases
        break
    
    for exception, reason_type in reversed(exceptions):
        frames = _get_exc_frames(exception)
        extend.append('Traceback (most recent call last):\n')
        extend = render_frames_to_list(frames, extend=extend)
        extend.append(get_exception_representation(exception))
        extend.append('\n')
        
        if reason_type == 0:
            break
        
        if reason_type == 1:
            extend.append('\nThe above exception was the direct cause of the following exception:\n\n')
            continue
        
        if reason_type == 2:
            extend.append('\nDuring handling of the above exception, another exception occurred:\n\n')
            continue
        
        # no more cases
        continue
    
    return extend

def format_callback(func, args=None, kwargs=None):
    """
    Formats the given callback to a more user friendly representation.
    
    Parameters
    ----------
    func : `callable`
        The callback to format.
    args : `None` or `iterable` of `Any`, Optional
        Additional parameters to call the `func` with.
    kwargs : `None` or `dict` of (`str`, `Any`) items, Optional
        Additional keyword parameters to call the `func` with.
    
    Returns
    -------
    result : `str`
        The formatted callback.
    """
    result = []
    # un-warp the wrappers
    while True:
        if not (None is args is kwargs):
            sub_result = ['(']
            if (args is not None) and args:
                for arg in args:
                    sub_result.append(reprlib.repr(arg))
                    sub_result.append(', ')
            
            if (kwargs is not None) and kwargs:
                for key, arg in kwargs.items():
                    sub_result.append(str(key)) # never trust
                    sub_result.append('=')
                    sub_result.append(reprlib.repr(arg))
                    sub_result.append(', ')
            
            if len(sub_result) > 1:
                del sub_result[-1]
            
            sub_result.append(')')
            result.append(''.join(sub_result))
        
        try:
            wrapped = func.func
        except AttributeError:
            if type(func) is MethodType and func.__self__.__class__ is Task:
                coro = func.__self__._coro
                coro_repr = getattr(coro, '__qualname__', None)
                if coro_repr is None:
                    coro_repr = getattr(coro, '__name__', None)
                    if coro_repr is None:
                        coro_repr = repr(coro)
                func_repr = f'<Bound method {func.__func__.__name__} of Task {coro_repr}>'
            else:
                func_repr = getattr(func, '__qualname__', None)
                if func_repr is None:
                    func_repr = getattr(func, '__name__', None)
                    if func_repr is None:
                        func_repr = repr(func)
            
            result.insert(0, func_repr)
            break
        
        args = getattr(func, 'args', None)
        kwargs = getattr(func, 'kwargs', None)
        func = wrapped
    
    return ''.join(result)

def format_coroutine(coro):
    """
    Formats the given coroutine to a more user friendly representation.
    
    Parameters
    ----------
    coro : `coroutine` or `generator` (or any compatible cyi or builtin)
    
    Returns
    -------
    result : `str`
        The formatted coroutine.
    """
    if not (hasattr(coro, 'cr_code') or hasattr(coro, 'gi_code')):
        # Cython or builtin
        name = getattr(coro, '__qualname__', None)
        if name is None:
            name = getattr(coro, '__name__', None)
            if name is None: # builtins might reach this part
                name = coro.__class__.__name__
        
        if type(coro) is GeneratorType:
            running = coro.gi_running
        elif type(coro) is CoroutineType:
            running = coro.cr_running
        else:
            running = False
        
        if running:
            state = 'running'
        else:
            state = 'done'
        
        return f'{name}() {state}'
    
    name = format_callback(coro)
    
    if type(coro) is GeneratorType:
        code = coro.gi_code
        frame = coro.gi_frame
    else:
        code = coro.cr_code
        frame = coro.cr_frame
    
    file_name = code.co_filename
    
    if frame is None:
        line_number = code.co_firstlineno
        state = 'done'
    else:
        line_number = frame.f_lineno
        state = 'running'
    
    return f'{name} {state} defined at {file_name}:{line_number}'

class Future:
    """
    A Future represents an eventual result of an asynchronous operation.
    
    Future is an awaitable object. Coroutines can await on ``Future`` objects until they either have a result or an
    exception set, or until they are cancelled.
    
    Attributes
    ----------
    _blocking : `bool`
        Whether the future is already being awaited, so it blocks the respective coroutine.
    _callbacks : `list` of `callable`
        The callbacks of the future, which are queued up on the respective event loop to be called, when the future is
        finished. These callback should accept `1` parameter, the future itself.
        
        Note, if the future is already done, then the newly added callbacks are queued up instantly on the respective
        event loop to be called.
    
    _exception : `None` or `BaseException` instance
        The exception set to the future as it's result. Defaults to `None`.
    _loop : ``EventThread``
        The loop to what the created future is bound.
    _result : `None` or `Any`
        The result of the future. Defaults to `None`.
    _state : `str`
        The state of the future.
        
        Can be set as one of the following:
        
        +-----------------+---------------+
        | Respective name | Value         |
        +=================+===============+
        | PENDING         | `'PENDING'`   |
        +-----------------+---------------+
        | CANCELLED       | `'CANCELLED'` |
        +-----------------+---------------+
        | FINISHED        | `'FINISHED'`  |
        +-----------------+---------------+
        | RETRIEVED       | `'RETRIEVED'` |
        +-----------------+---------------+
        
        Note, that states are checked by memory address and not by equality. Also ``RETRIEVED`` is used only if
        `__debug__` is set as `True`.
    """
    __slots__ = ('_blocking', '_callbacks', '_exception', '_loop', '_result', '_state')
    
    # If parameters are not passed will not call `__del__`
    def __new__(cls, loop):
        """
        Creates a new ``Future`` object bound to the given `loop`.
        
        Parameters
        ----------
        loop : ``EventThread``
            The loop to what the created future will be bound to.
        """
        self = object.__new__(cls)
        self._loop = loop
        self._state = PENDING

        self._result = None
        self._exception = None
        
        self._callbacks = []
        self._blocking = False

        return self

    def __repr__(self):
        """Returns the future's representation."""
        result = ['<', self.__class__.__name__, ' ']
        
        state = self._state
        result.append(state)
        
        if state is FINISHED or state is RETRIEVED:
            exception = self._exception
            if exception is None:
                result.append(', result=')
                result.append(reprlib.repr(self._result))
            else:
                result.append(', exception=')
                result.append(repr(exception))
        
        callbacks = self._callbacks
        limit = len(callbacks)
        if limit:
            result.append(', callbacks=[')
            index = 0
            while True:
                callback = callbacks[index]
                result.append(format_callback(callback))
                index += 1
                if index == limit:
                    break
                
                result.append(', ')
                continue
            
            result.append(']')
        
        result.append('>')
        
        return ''.join(result)
    
    if __debug__:
        def cancel(self):
            state = self._state
            
            if state is not PENDING:
                # If the future is cancelled, we should not show up not retrieved message at `.__del__`
                if state is FINISHED:
                    self._state = RETRIEVED
                return 0
            
            self._state = CANCELLED
            self._loop._schedule_callbacks(self)
            return 1
    else:
        def cancel(self):
            if self._state is not PENDING:
                return 0
            
            self._state = CANCELLED
            self._loop._schedule_callbacks(self)
            return 1
    
    set_docs(cancel,
        """
        Cancels the future if it is pending.
        
        Returns
        -------
        cancelled : `int` (`0`, `1`)
            If the future is already done, returns `0`, if it got cancelled, returns `1`-
        
        Notes
        -----
        If `__debug__` is set as `True`, then `.cancel()` also marks the future as retrieved, causing it to not render
        non-retrieved exceptions.
        """
    )
    
    def cancelled(self):
        """
        Returns whether the future is cancelled.
        
        Returns
        -------
        cancelled : `bool`
        """
        return (self._state is CANCELLED)
    
    def done(self):
        """
        Returns whether the future is done.
        
        Returns
        -------
        done : `bool`
        """
        return (self._state is not PENDING)
    
    def pending(self):
        """
        Returns whether the future is pending.
        
        Returns
        -------
        pending : `bool`
        """
        return (self._state is PENDING)
    
    if __debug__:
        def result(self):
            state = self._state
            
            if state is FINISHED:
                self._state = RETRIEVED
                exception = self._exception
                if exception is None:
                    return self._result
                raise exception
            
            if state is RETRIEVED:
                exception = self._exception
                if exception is None:
                    return self._result
                raise exception
            
            if state is CANCELLED:
                raise CancelledError
            
            # still pending
            raise InvalidStateError(self, 'result')
    else:
        def result(self):
            state = self._state
            
            if state is FINISHED:
                exception = self._exception
                if exception is None:
                    return self._result
                raise exception
            
            if state is CANCELLED:
                raise CancelledError
            
            # still pending
            raise InvalidStateError(self, 'result')
    
    set_docs(result,
        """
        Returns the result of the future.
        
        If the future is cancelled, raises ``CancelledError``.
        
        If the future has exception set with `.set_exception` or `.set_exception_if_pending` successfully, then raises
        the given exception.
        
        If the future has result set with `.set_result` or `.set_result_if_pending` successfully, then returns the
        given object.
        
        If the future is not done yet, raises ``InvalidStateError``.
        
        Returns
        -------
        result : `Any`
        
        Raises
        ------
        CancelledError
            The future is cancelled.
        InvalidStateError
            The futures is not done yet.
        TypeError
            The future has non `BaseException` instance set as exception.
        BaseException
            The future's set exception.
        """
    )
    
    if __debug__:
        def exception(self):
            state = self._state
            if state is FINISHED:
                self._state = RETRIEVED
                return self._exception

            if state is RETRIEVED:
                return self._exception
            
            if state is CANCELLED:
                raise CancelledError
            
            # still pending
            raise InvalidStateError(self, 'exception')
        
    else:
        def exception(self):
            state = self._state

            if state is FINISHED:
                return self._exception
            
            if state is CANCELLED:
                raise CancelledError
            
            # still pending
            raise InvalidStateError(self, 'exception')
    
    set_docs(exception,
        """
        Returns the future's exception.
        
        If the future is done, returns it's exception. (Cab be `None`)
        
        If the future is cancelled, raises ``CancelledError``.
        
        If the future is not done yet, raises ``InvalidStateError``.
        
        Returns
        -------
        exception : `Any`
        
        Raises
        ------
        CancelledError
            The future is cancelled.
        InvalidStateError
            The futures is not done yet.
        """
    )
    
    def add_done_callback(self, func):
        """
        Adds the given `func` as a callback of the future.
        
        Parameters
        ----------
        `func` : `callable`
            A callback, what is queued up on the respective event loop, when the future is done. These callback should
            accept `1` parameter, the future itself.
            
        Notes
        -----
        If the future is already done, then the newly added callbacks are queued up instantly on the respective
        event loop to be called.
        """
        if self._state is PENDING:
            self._callbacks.append(func)
        else:
            self._loop.call_soon(func, self)
    
    def remove_done_callback(self, func):
        """
        Removes the given `func` from the future's ``._callbacks``.
        
        Parameters
        ----------
        func : `Any`
            The callback to remove.
        
        Returns
        -------
        count : `int`
            The total count of the removed callbacks.
        """
        callbacks = self._callbacks
        count = 0
        index = len(callbacks)
        while index:
            index -= 1
            if callbacks[index] is func:
                del callbacks[index]
                count += 1
        
        return count
    
    def set_result(self, result):
        """
        Marks the future as done and set's it's result.
        
        Parameters
        ----------
        result : `Any`
            The object to set as result.
        
        Raises
        ------
        InvalidStateError
            If the future is already done.
        """
        if self._state is not PENDING:
            raise InvalidStateError(self, 'set_result')
            
        self._result = result
        self._state = FINISHED
        self._loop._schedule_callbacks(self)
    
    def set_result_if_pending(self, result):
        """
        Marks the future as done and set's it's result. Not like ``.set_result``, this method will not raise
        ``InvalidStateError`` if the future is already done.
        
        Parameters
        ----------
        result : `Any`
            The object to set as result.
        
        Returns
        ------
        set_result : `int` (`0`, `1`)
            If the future is already done, returns `0`, else `1`.
        """
        if self._state is not PENDING:
            return 0
        
        self._result = result
        self._state = FINISHED
        self._loop._schedule_callbacks(self)
        return 1
    
    def set_exception(self, exception):
        """
        Marks the future as done and set's it's exception.
        
        Parameters
        ----------
        exception : `BaseException`
            The exception to set as the future's exception.
        
        Raises
        ------
        InvalidStateError
            If the future is already done.
        TypeError
            If `StopIteration` is given as `exception`.
        """
        if self._state is not PENDING:
            raise InvalidStateError(self, 'set_exception')
        
        if isinstance(exception, type):
            exception = exception()
        
        if type(exception) is StopIteration:
             raise TypeError(f'{exception} cannot be raised to a {self.__class__.__name__}: {self!r}')
        
        self._exception = exception
        self._state = FINISHED
        self._loop._schedule_callbacks(self)
    
    def set_exception_if_pending(self, exception):
        """
        Marks the future as done and set's it's exception. Not like ``.set_exception``, this method will not raise
        ``InvalidStateError`` if the future is already done.
        
        Parameters
        ----------
        exception : `BaseException`
            The exception to set as the future's exception.
        
        Returns
        ------
        set_result : `int` (`0`, `1`)
            If the future is already done, returns `0`, else `1`.
        
        Raises
        ------
        TypeError
            If `StopIteration` is given as `exception`.
        """
        if self._state is not PENDING:
            return 0
        
        if isinstance(exception, type):
            exception = exception()
        
        if type(exception) is StopIteration:
             raise TypeError(f'{exception} cannot be raised to a {self.__class__.__name__}: {self!r}')
        
        self._exception = exception
        self._state = FINISHED
        self._loop._schedule_callbacks(self)
        return 1
    
    def __iter__(self):
        """
        Awaits the future till it is done.
        
        This method is a generator. Should be used with `await` expression.
        """
        if self._state is PENDING:
            self._blocking = True
            yield self
        
        return self.result()
    
    __await__ = __iter__
    
    if __debug__:
        def __del__(self):
            """
            If the future is pending, but it's result was not set, meanwhile anything awaits at it, notifies it.
            
            Also notifies if the future's result was set with ``.set_exception``, or with
            ``.set_exception_if_pending``, and it was not retrieved.
            
            Notes
            -----
            This method is present only if `__debug__` is set as `True`.
            """
            if not self._loop.running:
                return
            
            state = self._state
            if state is PENDING:
                if self._callbacks:
                    
                    # ignore being silenced
                    silence_cb = type(self).__silence_cb__
                    for callback in self._callbacks:
                        if callback is silence_cb:
                            return
                    
                    sys.stderr.write(f'{self.__class__.__name__} is not finished, but still pending!\n{self!r}\n')
                return
            
            if state is FINISHED:
                if (self._exception is not None):
                    self._loop.render_exc_maybe_async(self._exception, [
                        self.__class__.__name__,
                        ' exception was never retrieved\n',
                        repr(self),
                        '\n',])
                return
            
            # no more notify case
        
        def __silence__(self):
            """
            Silences the future's `__del__`, so it will not notify if it would.
            
            Notes
            -----
            This method is present only if `__debug__` is set as `True`.
            """
            state = self._state
            if state is PENDING:
                self._callbacks.append(type(self).__silence_cb__)
                return
            
            if state is FINISHED:
                self._state = RETRIEVED
        
        def __silence_cb__(self):
            """
            Callback added to the future, when ``.__silence__`` is called, when the future is still pending.
            
            Notes
            -----
            This method is present only if `__debug__` is set as `True`.
            """
            if self._state is FINISHED:
                self._state = RETRIEVED
    
    def cancel_handles(self):
        """
        Cancels the handles (``_HandleCancellerBase`` instances) added as callbacks to the future.
        """
        callbacks = self._callbacks
        if callbacks:
            for index in reversed(range(len(callbacks))):
                callback = callbacks[index]
                if isinstance(callback, _HandleCancellerBase):
                    del callbacks[index]
                    callback.cancel()
    
    def clear(self):
        """
        Clears the future, making it reusable.
        """
        self._state = PENDING
        self._exception = None
        self._result = None
        self.cancel_handles()
        self._blocking = False
    
    def sync_wrap(self):
        """
        Wraps the future, so it's result can be retrieved from a sync thread.
        
        Returns
        -------
        future_wrapper : ``FutureSyncWrapper``
            A future awaitable from sync threads.
        """
        return FutureSyncWrapper(self)
    
    def async_wrap(self, loop):
        """
        Wraps the future, so it's result can be retrieved from an other async thread.
        
        Parameters
        ----------
        loop : ``EventThread``
            The event loop, from where the future would be awaited.
        
        Returns
        -------
        future_wrapper : ``FutureAsyncWrapper``
            An awaitable future from the given event loop.
        """
        return FutureAsyncWrapper(self, loop)

class FutureSyncWrapper:
    """
    Sync wrapper for ``Future`` instances enabling them to be waited from a sync threads.
    
    Attributes
    ----------
    _exception : `None` or `BaseException` instance
        The exception set to the future as it's result. Defaults to `None`.
    _future : `None` or ``Future`` instance
        The waited future. If the future's state is modified by the sync wrapper, then ``._future`` is set as `None`,
        to not retrieve the result again.
    _lock : `threading.Lock`
        Threading lock to disable concurrent access to the future.
    _result : `None` or `Any`
        The result of the future. Defaults to `None`.
    _state : `str`
        The state of the future.
        
        Can be set as one of the following:
        
        +-----------------+---------------+
        | Respective name | Value         |
        +=================+===============+
        | PENDING         | `'PENDING'`   |
        +-----------------+---------------+
        | CANCELLED       | `'CANCELLED'` |
        +-----------------+---------------+
        | FINISHED        | `'FINISHED'`  |
        +-----------------+---------------+
        | RETRIEVED       | `'RETRIEVED'` |
        +-----------------+---------------+
        
        Note, that states are checked by memory address and not by equality. Also ``RETRIEVED`` is used only if
        `__debug__` is set as `True`.
    _waiter : `threading.Event`
        An event, what is set, when the waited future is done.
    """
    __slots__ = ('_exception', '_future', '_lock', '_result', '_state', '_waiter')
    
    def __new__(cls, future):
        """
        Creates a new ``FutureSyncWrapper`` instance wrapping the given `future`
        
        Parameters
        ----------
        future : ``Future`` instance
            The future on what we would want to wait from a sync thread.
        """
        self = object.__new__(cls)
        self._future = future
        self._lock = SyncLock()
        self._waiter = SyncEvent()
        self._state = PENDING
        self._result = None
        self._exception = None
        
        loop = future._loop
        loop.call_soon(future.add_done_callback, self._done_callback)
        loop.wake_up()
        
        return self
    
    def __call__(self, future):
        """
        By calling a ``FutureSyncWrapper`` you can make it bound to an other future.
        
        Parameters
        ----------
        future : ``Future`` instance
            The future on what you would want to wait from a sync thread.
        
        Returns
        -------
        self : ``FutureSyncWrapper``
        """
        with self._lock:
            old_future = self._future

            if old_future is not None:
                loop = old_future._loop
                loop.call_soon(self._remove_callback, old_future)
                loop.wake_up()

            self._future = future
            self._state = PENDING
            self._result = None
            self._exception = None
            self._waiter.clear()

            loop = future._loop
            loop.call_soon(future.add_done_callback, self._done_callback)
            loop.wake_up()

        return self
    
    def __repr__(self):
        """Returns the future sync wrapper's representation."""
        result = ['<', self.__class__.__name__, ' ', ]
        
        state = self._state
        result.append(state)
        
        if state is FINISHED or state is RETRIEVED:
            
            exception = self._exception
            if exception is None:
                result.append(' result=')
                result.append(reprlib.repr(self._result))
            else:
                result.append(' exception=')
                result.append(repr(exception))
        
        future = self._future
        if future is not None:
            # we do not want to repr it, keep it thread safe
            result.append(' future=')
            result.append(future.__class__.__name__)
            result.append('(...)')
        result.append('>')
        
        return ''.join(result)
    
    if __debug__:
        def cancel(self):
            state = self._state
            if state is not PENDING:
                if state is FINISHED:
                    self._state = RETRIEVED
                
                return 0
            
            future = self._future
            if future is None:
                self._state = CANCELLED
                self._waiter.set()
                return 1
            
            loop = future._loop
            loop.call_soon(future.cancel)
            loop.wake_up()
            return 1
        
    else:
        def cancel(self):
            if self._state is not PENDING:
                return 0
            
            future = self._future
            if future is None:
                self._state = CANCELLED
                self._waiter.set()
                return 1
            
            loop = future._loop
            loop.call_soon(future.cancel)
            loop.wake_up()
            return 1
    
    set_docs(cancel,
        """
        Cancels the future if it is pending.
        
        Returns
        -------
        cancelled : `int` (`0`, `1`)
            If the future is already done, returns `0`, if it got cancelled, returns `1`-
        
        Notes
        -----
        If `__debug__` is set as `True`, then `.cancel()` also marks the future as retrieved, causing it to not render
        non-retrieved exceptions.
        """
    )
    
    def cancelled(self):
        """
        Returns whether the future is cancelled.
        
        Returns
        -------
        cancelled : `bool`
        """
        return (self._state is CANCELLED)
    
    def done(self):
        """
        Returns whether the future is done.
        
        Returns
        -------
        done : `bool`
        """
        return (self._state is not PENDING)
    
    def pending(self):
        """
        Returns whether the future is pending.
        
        Returns
        -------
        pending : `bool`
        """
        return (self._state is PENDING)
    
    if __debug__:
        def result(self):
            with self._lock:
                state = self._state
                
                if state is FINISHED:
                    self._state = RETRIEVED
                    exception = self._exception
                    if exception is None:
                        return self._result
                    raise exception
                
                if state is RETRIEVED:
                    exception = self._exception
                    if exception is None:
                        return self._result
                    raise exception
                
                if state is CANCELLED:
                    raise CancelledError
            
            # still pending
            raise InvalidStateError(self, 'result')
    
    else:
        def result(self):
            with self._lock:
                if self._state is FINISHED:
                    exception = self._exception
                    if exception is None:
                        return self._result
                    raise exception
                
                if self._state is CANCELLED:
                    raise CancelledError
            
            # still pending
            raise InvalidStateError(self, 'result')
    
    set_docs(result,
        """
        Returns the result of the future.
        
        If the waited future, or this one is cancelled, raises ``CancelledError``.
        
        If the waiter future or this one has exception set with `.set_exception` or `.set_exception_if_pending`
        successfully, then raises the given exception.
        
        If the waited future or this one has result set with `.set_result` or `.set_result_if_pending` successfully,
        then returns the given object.
        
        If the future is not done yet, raises ``InvalidStateError``.
        
        Returns
        -------
        result : `Any`
        
        Raises
        ------
        CancelledError
            The future is cancelled.
        InvalidStateError
            The futures is not done yet.
        TypeError
            The future has non `BaseException` instance set as exception.
        BaseException
            The future's set exception.
        """
    )
    
    if __debug__:
        def exception(self):
            with self._lock:
                state = self._state
                if state is FINISHED:
                    self._state = RETRIEVED
                    return self._exception

                if state is RETRIEVED:
                    return self._exception

                if state is CANCELLED:
                    raise CancelledError

            # still pending
            raise InvalidStateError(self, 'exception')

    else:
        def exception(self):
            with self._lock:
                if self._state is FINISHED:
                    return self._exception

                if self._state is CANCELLED:
                    raise CancelledError

            # still pending
            raise InvalidStateError(self, 'exception')
    
    set_docs(exception,
        """
        Returns the future's exception.
        
        If the waited future or this one is done, returns it's exception. (Cab be `None`)
        
        If the waited future or this one is cancelled, raises ``CancelledError``.
        
        If the waited future or this one is not done yet, raises ``InvalidStateError``.
        
        Returns
        -------
        exception : `Any`
        
        Raises
        ------
        CancelledError
            The future is cancelled.
        InvalidStateError
            The futures is not done yet.
        """
    )
    
    if __debug__:
        def _done_callback(self, future):
            with self._lock:
                if (self._future is not future):
                    return
                
                state = future._state
                if state is FINISHED:
                    future._state = RETRIEVED
                elif state is RETRIEVED:
                    state = FINISHED
                
                self._state = state
                self._result = future._result
                self._exception = future._exception
                self._future = None
                self._waiter.set()
    else:
        def _done_callback(self, future):
            with self._lock:
                if (self._future is not future):
                    return
                
                self._state = future._state
                self._result = future._result
                self._exception = future._exception
                self._future = None
                self._waiter.set()
    
    set_docs(_done_callback,
        """
        Callback added to the waited future to retrieve it's result.
        
        Parameters
        ----------
        future : ``Future`` instance
            The waited future.
        
        Notes
        -----
        If a different future is given as parameter than the currently waited one, then wont do anything.
        
        If `_debug__` is set as `True`, then this callback also marks the waited future as retrieved.
        """
    )
    
    def _remove_callback(self, future):
        """
        Removes ``._done_callback`` callback from the given `future`'s callbacks.
        
        Parameters
        ----------
        future : ``Future`` instance
            The future, from what's callbacks the own one will be removed.
        """
        callbacks = future._callbacks
        if callbacks:
            for index in range(len(callbacks)):
                callback = callbacks[index]
                if (type(callback) is MethodType) and (callback.__self__ is self):
                    del callbacks[index]
                    break
    
    def wait(self, timeout=None):
        """
        Waits till the waited future's result or exception is set.
        
        If the future is cancelled, raises ``CancelledError``.
        
        If the future has exception set with `.set_exception` or `.set_exception_if_pending` successfully, then raises
        the given exception.
        
        If the future has result set with `.set_result` or `.set_result_if_pending` successfully, then returns the
        given object.
        
        If the future is not done yet, raises ``InvalidStateError``.
        
        Parameters
        ----------
        timeout : `None` or `float`, Optional
            Timeout in seconds till the waited future's result should be set. Giving it as `None`, means no time limit.
        
        Raises
        ------
        TimeoutError
            If `timeout` is over and the waited future is still pending.
        CancelledError
            The future is cancelled.
        InvalidStateError
            The futures is not done yet.
        TypeError
            The future has non `BaseException` instance set as exception.
        BaseException
            The future's set exception.
        """
        if self._waiter.wait(timeout):
            return self.result()
        else:
            raise CancelledError
    
    def _set_future_result(self, future, result):
        """
        Sets the given `result` as the `future`'s result if applicable.
        
        This method is put on the respective event loop to be called, by ``.set_result`` or by
        ``.set_result_if_pending``, if the future's result can be set.
        
        Parameters
        ----------
        future : ``Future`` instance
            The future to set the result to.
        result : `Any`
            The result to set as the future's.
        """
        try:
            future.set_result(result)
        except (RuntimeError, InvalidStateError): # the future does not support this operation
            pass
        
        with self._lock:
            if self._future is future:
                self._state = RETRIEVED
                self._future = None
    
    def set_result(self, result):
        """
        Marks the waited future and this as done and set their result.
        
        Parameters
        ----------
        result : `Any`
            The object to set as result.
        
        Raises
        ------
        InvalidStateError
            If the future is already done.
        """
        with self._lock:
            if self._state is not PENDING:
                raise InvalidStateError(self, 'set_result')
            
            future = self._future
            
            if future is None:
                self._result = result
                self._state = FINISHED
                self._waiter.set()
                return
        
        loop = future._loop
        loop.call_soon(self.__class__._set_future_result, self, future, result)
        loop.wake_up()
    
    def set_result_if_pending(self, result):
        """
        Marks the waited future and this as done and set their result. Not like ``.set_result``, this method will not
        raise ``InvalidStateError`` if the future is already done.
        
        Parameters
        ----------
        result : `Any`
           The object to set as result.
        
        Returns
        ------
        set_result : `int` (`0`, `1`, `2`)
            If the future is already done, returns `0`. If `self` not bound to any other futures, returns `2`. If
            self's and the waited future's result can be set, returns `1`.
        """
        with self._lock:
            if self._state is not PENDING:
                return 0
            
            future = self._future

            if future is None:
                self._result = result
                self._state = FINISHED
                self._waiter.set()
                return 2

        loop = future._loop
        loop.call_soon(self.__class__._set_future_result, self, future, result)
        loop.wake_up()
        return 1
    
    def _set_future_exception(self, future, exception):
        """
        Sets the given `exception` as the `future`'s exception if applicable.
        
        This method is put on the respective event loop to be called, by ``.set_exception`` or by
        ``.set_exception_if_pending``, if the future's result can be set.
        
        Parameters
        ----------
        future : ``Future`` instance
            The future to set the exception to.
        exception : `Any`
            The exception to set as the future's.
        """
        try:
            future.set_exception(exception)
        except (RuntimeError, InvalidStateError): # the future does not supports this operation
            pass
        
        with self._lock:
            if self._future is future:
                self._state = RETRIEVED
                self._future = None

    def set_exception(self, exception):
        """
        Marks the waited future and this as done and set's it's exception.
        
        Parameters
        ----------
        exception : `BaseException`
            The exception to set as the future's exception.
        
        Raises
        ------
        InvalidStateError
            If the future is already done.
        TypeError
            If `StopIteration` is given as `exception`.
        """
        with self._lock:
            if self._state is not PENDING:
                raise InvalidStateError(self, 'set_exception')
            
            if isinstance(exception, type):
                exception = exception()
            
            if type(exception) is StopIteration:
                 raise TypeError(f'{exception} cannot be raised to a {self.__class__.__name__}: {self!r}')
            
            future = self._future
            if future is None:
                self._exception = exception
                self._state = FINISHED
                self._waiter.set()
                return
        
        loop = future._loop
        loop.call_soon(self._set_future_exception, future, exception)
        loop.wake_up()
    
    def set_exception_if_pending(self, exception):
        """
        Marks the waited future and this as done and set's it's exception. Not like ``.set_exception``, this method
        will not raise ``InvalidStateError`` if the future is already done.
        
        Parameters
        ----------
        exception : `BaseException`
            The exception to set as the future's exception.
        
        Returns
        ------
        set_result : `int` (`0`, `1`, `2`)
            If the future is already done, returns `0`. If `self` not bound to any other futures, returns `2`. If
            self's and the waited future's exception can be set, returns `1`.
        
        Raises
        ------
        TypeError
            If `StopIteration` is given as `exception`.
        """
        with self._lock:
            if self._state is not PENDING:
                return 0
            
            if isinstance(exception, type):
                exception = exception()
            
            if type(exception) is StopIteration:
                 raise TypeError(f'{exception} cannot be raised to a {self.__class__.__name__}: {self!r}')
            
            future = self._future
            if future is None:
                self._exception = exception
                self._state = FINISHED
                self._waiter.set()
                return 2
        
        loop = future._loop
        loop.call_soon(self._set_future_exception, future, exception)
        loop.wake_up()
        return 1
    
    if __debug__:
        def __del__(self):
            """
            If the future is pending, but it's result was not set, meanwhile anything waits at it, notifies it.
            
            Also notifies if the future's result was set with ``.set_exception``, or with
            ``.set_exception_if_pending``, and it was not retrieved.
            
            Notes
            -----
            This method is present only if `__debug__` is set as `True`.
            """
            if self._state is PENDING:
                if self._future is not None:
                    sys.stderr.write(f'{self.__class__.__name__} is not finished, but still pending!\n{self!r}\n')
                return

            if self._state is FINISHED:
                if (self._exception is not None):
                    self._future._loop.render_exc_maybe_async(self._exception, [
                        self.__class__.__name__,
                        ' exception was never retrieved\n',
                        repr(self),
                        '\n',])
                return
            
            # no more notify case
        
        def __silence__(self):
            """
            Silences the future's `__del__`, so it will not notify if it would.
            
            Notes
            -----
            This method is present only if `__debug__` is set as `True`.
            """
            self._state = RETRIEVED
    
    def clear(self):
        """
        Clears the future, making it reusable.
        """
        with self._lock:
            future = self._future
            if future is not None:
                loop = future._loop
                loop.call_soon(self._remove_callback, future)
                loop.wake_up()
                self._future = None
            
            self._waiter.clear()
            self._state = PENDING
            self._exception = None
            self._result = None


class FutureAsyncWrapper(Future):
    """
    Async wrapper for ``Future`` instances enabling them to be awaited from an another event loop.
    
    Attributes
    ----------
    _blocking : `bool`
        Whether the future is already being awaited, so it blocks the respective coroutine.
    _callbacks : `list` of `callable`
        The callbacks of the future, which are queued up on the respective event loop to be called, when the future is
        finished. These callback should accept `1` parameter, the future itself.
        
        Note, if the future is already done, then the newly added callbacks are queued up instantly on the respective
        event loop to be called.
    
    _exception : `None` or `BaseException` instance
        The exception set to the future as it's result. Defaults to `None`.
    _future : `None` or ``Future`` instance
        The waited future. If the future's state is modified by the sync wrapper, then ``._future`` is set as `None`,
        to not retrieve the result again.
    _loop : ``EventThread``
        The loop to what the async future wrapper is bound to.
    _result : `None` or `Any`
        The result of the future. Defaults to `None`.
    _state : `str`
        The state of the future.
        
        Can be set as one of the following:
        
        +-----------------+---------------+
        | Respective name | Value         |
        +=================+===============+
        | PENDING         | `'PENDING'`   |
        +-----------------+---------------+
        | CANCELLED       | `'CANCELLED'` |
        +-----------------+---------------+
        | FINISHED        | `'FINISHED'`  |
        +-----------------+---------------+
        | RETRIEVED       | `'RETRIEVED'` |
        +-----------------+---------------+
        
        Note, that states are checked by memory address and not by equality. Also ``RETRIEVED`` is used only if
        `__debug__` is set as `True`.
    """
    __slots__ = ('_blocking', '_callbacks', '_exception', '_future', '_loop', '_result', '_state',)

    def __new__(cls, future, loop):
        """
        Creates a new ``FutureAsyncWrapper`` object bound to the given `loop` and `future`.
        
        If the given `future` is an ``FutureAsyncWrapper`` instance, then will wrap it's future instead.
        
        Parameters
        ----------
        loop : ``EventThread``
            The loop from where the created wrapper futures can be awaited.
        future : ``Future`` or ``FutureAsyncWrapper`` instance
            The future to wrap.
        
        Returns
        -------
        self : ``Future`` or ``FutureAsyncWrapper`` instance
            If the given `future` is bound to the given loop, returns the `future` itself instead of async wrapping it.
        """
        if future._loop is loop:
            return future
        
        if isinstance(future, cls):
            future = future._future
            if future._loop is loop:
                return future
        
        self = object.__new__(cls)
        self._future = future
        self._loop = loop
        self._state = PENDING
        self._result = None
        self._exception = None
        
        self._callbacks = []
        self._blocking = False
        
        loop = future._loop
        loop.call_soon(future.add_done_callback, self._done_callback)
        loop.wake_up()
        
        return self
    
    def __call__(self, future):
        """
        By calling a ``FutureAsyncWrapper`` you can make it bound to an other future.
        
        Parameters
        ----------
        future : ``Future`` instance
            The future on what you would want to wait from the other event loop.
        
        Returns
        -------
        self : ``FutureAsyncWrapper``
        """
        old_future = self._future
        if old_future is not None:
            loop = old_future._loop
            loop.call_soon(self._remove_callback, old_future)
            loop.wake_up()
        
        self._future = future
        self._state = PENDING
        self._result = None
        self._exception = None
        self._blocking = False
        
        loop = future._loop
        loop.call_soon(future.add_done_callback, self._done_callback)
        loop.wake_up()
    
    def __repr__(self):
        """Returns the future async wrapper's representation."""
        result = ['<', self.__class__.__name__, ' ']
        
        state = self._state
        result.append(state)
        
        if state is FINISHED or state is RETRIEVED:
            exception = self._exception
            if exception is None:
                result.append(', result=')
                result.append(reprlib.repr(self._result))
            else:
                result.append(', exception=')
                result.append(repr(exception))
        
        callbacks = self._callbacks
        limit = len(callbacks)
        if limit:
            result.append(', callbacks=[')
            index = 0
            while True:
                callback = callbacks[index]
                result.append(format_callback(callback))
                index += 1
                if index == limit:
                    break
                
                result.append(', ')
                continue
            
            result.append(']')
        
        future = self._future
        if future is not None:
            # we do not want to repr it, keep it thread safe
            result.append(', future=')
            result.append(future.__class__.__name__)
            result.append('(...)')
        result.append('>')
        
        return ''.join(result)
    
    if __debug__:
        def cancel(self):
            state = self._state
            if state is not PENDING:
                if state is FINISHED:
                    self._state = RETRIEVED
                
                return 0
            
            future = self._future
            if future is None:
                self._state = CANCELLED
                self._loop._schedule_callbacks(self)
                return 1
            
            loop = future._loop
            loop.call_soon(future.cancel)
            loop.wake_up()
            return 1
        
    else:
        def cancel(self):
            if self._state is not PENDING:
                return 0
            
            future = self._future
            if future is None:
                self._state = CANCELLED
                self._loop._schedule_callbacks(self)
                return 1
            
            loop = future._loop
            loop.call_soon(future.cancel)
            loop.wake_up()
            return 1
    
    set_docs(cancel,
        """
        Cancels the future if it is pending.
        
        Returns
        -------
        cancelled : `int` (`0`, `1`)
            If the future is already done, returns `0`, if it got cancelled, returns `1`-
        
        Notes
        -----
        If `__debug__` is set as `True`, then `.cancel()` also marks the future as retrieved, causing it to not render
        non-retrieved exceptions.
        """
    )
    
    if __debug__:
        def _done_callback(self, future):
            if self._future is not future:
                return
            
            state = future._state
            if state is FINISHED:
                future._state = RETRIEVED
            elif state is RETRIEVED:
                state = FINISHED
            
            loop = self._loop
            loop.call_soon(self.__class__._done_callback_re, self, state, future._result, future._exception)
            loop.wake_up()
    else:
        def _done_callback(self, future):
            if (self._future is not future):
                return
            
            loop = self._loop
            loop.call_soon(self.__class__._done_callback_re, self, future._state, future._result, future._exception)
            loop.wake_up()
    
    set_docs(_done_callback,
        """
        Callback added to the waited future to retrieve it's result.
        
        Parameters
        ----------
        future : ``Future`` instance
            The waited future.
        
        Notes
        -----
        If a different future is given as parameter than the currently waited one, then wont do anything.
        
        If `_debug__` is set as `True`, then this callback also marks the waited future as retrieved.
        """
    )
    
    def _done_callback_re(self, state, result, exception):
        """
        Function queued up on the wrapper future's loop, by ``._done_callback``, marking this future as done.
        
        Parameters
        ----------
        state : `str`
            The future's new state.
        result : `Any`
            The future's new result.
        exception : `Any`
            The future's new exception.
        """
        self._state = state
        self._result = result
        self._exception = exception
        
        self._loop._schedule_callbacks(self)
    
    def _remove_callback(self, future):
        """
        Removes ``._done_callback`` callback from the given `future`'s callbacks.
        
        Parameters
        ----------
        future : ``Future`` instance
            The future, from what's callbacks the own one will be removed.
        """
        callbacks = future._callbacks
        if callbacks:
            for index in range(len(callbacks)):
                callback = callbacks[index]
                if (type(callback) is MethodType) and (callback.__self__ is self):
                    del callbacks[index]
                    break
    
    def _set_future_result(self, future, result):
        """
        Sets the given `result` as the `future`'s result if applicable.
        
        This method is put on the respective event loop to be called, by ``.set_result`` or by
        ``.set_result_if_pending``, if the future's result can be set.
        
        Parameters
        ----------
        future : ``Future`` instance
            The future to set the result to.
        result : `Any`
            The result to set as the future's.
        """
        try:
            future.set_result(result)
        except (RuntimeError, InvalidStateError): # the future does not support this operation
            pass
        
        loop = self._loop
        loop.call_soon(self.__class__._set_future_any_re, self, future)
        loop.wake_up()
    
    def _set_future_any_re(self, future):
        """
        If self is still waiting on the given future, marks self as retrieved and removes `._future`, so further results
        wont be retrieved.
        
        Parameters
        ----------
        future : ``Future`` instance.
        """
        if self._future is future:
            self._state = RETRIEVED
            self._future = None
    
    def set_result(self, result):
        """
        Marks the waited future and this as done and set their result.
        
        Parameters
        ----------
        result : `Any`
            The object to set as result.
        
        Raises
        ------
        InvalidStateError
            If the future is already done.
        """
        if self._state is not PENDING:
            raise InvalidStateError(self, 'set_result')
        
        future = self._future
        
        if future is None:
            self._result = result
            self._state = FINISHED
            self._loop._schedule_callbacks(self)
            return
        
        loop = future._loop
        loop.call_soon(self._set_future_result, future, result)
        loop.wake_up()
    
    def set_result_if_pending(self, result):
        """
        Marks the waited future and this as done and set their result. Not like ``.set_result``, this method will
        not raise ``InvalidStateError`` if the future is already done.
        
        Parameters
        ----------
        result : `Any`
            The object to set as result.
        
        Returns
        ------
        set_result : `int` (`0`, `1`, `2`)
            If the future is already done, returns `0`. If `self` not bound to any other futures, returns `2`. If
            self's and the waited future's result can be set, returns `1`.
        """
        if self._state is not PENDING:
            return 1
        
        future = self._future
        
        if future is None:
            self._result = result
            self._state = FINISHED
            self._loop._schedule_callbacks(self)
            return 2
        
        loop = future._loop
        loop.call_soon(self._set_future_result, future, result)
        loop.wake_up()
        return 1
    
    def _set_future_exception(self, future, exception):
        """
        Sets the given `exception` as the `future`'s exception if applicable.
        
        This method is put on the respective event loop to be called, by ``.set_exception`` or by
        ``.set_exception_if_pending``, if the future's result can be set.
        
        Parameters
        ----------
        future : ``Future`` instance
            The future to set the result to.
        exception : `Any`
            The exception to set as the future's.
        """
        try:
            future.set_exception(exception)
        except (RuntimeError, InvalidStateError): #the future does not supports this operation
            pass
        
        loop = self._loop
        loop.call_soon(self._set_future_any_re, future)
        loop.wake_up()
    
    def set_exception(self, exception):
        """
        Marks the waited future and this as done and set's it's exception.
        
        Parameters
        ----------
        exception : `BaseException`
            The exception to set as the future's exception.
        
        Raises
        ------
        InvalidStateError
            If the future is already done.
        TypeError
            If `StopIteration` is given as `exception`.
        """
        if self._state is not PENDING:
            raise InvalidStateError(self, 'set_exception')
        
        if isinstance(exception, type):
            exception = exception()
        
        if type(exception) is StopIteration:
             raise TypeError(f'{exception} cannot be raised to a {self.__class__.__name__}: {self!r}')
        
        future = self._future
        if future is None:
            self._exception = exception
            self._state = FINISHED
            self._loop._schedule_callbacks(self)
            return
        
        loop = future._loop
        loop.call_soon(self._set_future_exception, future, exception)
        loop.wake_up()
    
    def set_exception_if_pending(self, exception):
        """
        Marks the waited future and this as done and set's it's exception. Not like ``.set_exception``, this method
        will not raise ``InvalidStateError`` if the future is already done.
        
        Parameters
        ----------
        exception : `BaseException`
            The exception to set as the future's exception.
        
        Returns
        ------
        set_result : `int` (`0`, `1`, `2`)
            If the future is already done, returns `0`. If `self` not bound to any other futures, returns `2`. If
            self's and the waited future's exception can be set, returns `1`.
        
        Raises
        ------
        TypeError
            If `StopIteration` is given as `exception`.
        """
        if self._state is not PENDING:
            return 0
        
        if isinstance(exception, type):
            exception = exception()
        
        if type(exception) is StopIteration:
             raise TypeError(f'{exception} cannot be raised to a {self.__class__.__name__}: {self!r}')
        
        future = self._future
        if future is None:
            self._exception = exception
            self._state = FINISHED
            self._loop._schedule_callbacks(self)
            return 2
        
        loop = future._loop
        loop.call_soon(self._set_future_exception, future, exception)
        loop.wake_up()
        return 1
    
    def clear(self):
        """
        Clears the future, making it reusable.
        """
        future = self._future
        if future is not None:
            loop = future._loop
            loop.call_soon(self._remove_callback, future)
            loop.wake_up()
            self._future = None

        self._state = PENDING
        self._exception = None
        self._result = None
        self.cancel_handles()
        self._blocking = False

class FutureWM(Future):
    """
    A Future subclass, which yields after it's result was set a set amount of times with ``.set_result``, or with
    ``.set_result_if_pending``, or till an exception is set to with ``.set_exception``, or with
    ``.set_exception_if_pending``.
    
    Attributes
    ----------
    _blocking : `bool`
        Whether the future is already being awaited, so it blocks the respective coroutine.
    _callbacks : `list` of `callable`
        The callbacks of the future, which are queued up on the respective event loop to be called, when the future is
        finished. These callback should accept `1` parameter, the future itself.
        
        Note, if the future is already done, then the newly added callbacks are queued up instantly on the respective
        event loop to be called.
    
    _exception : `None` or `BaseException` instance
        The exception set to the future as it's result. Defaults to `None`.
    _loop : ``EventThread``
        The loop to what the created future is bound.
    _result : `list` of `Any`
        The results of the future.
    _state : `str`
        The state of the future.
        
        Can be set as one of the following:
        
        +-----------------+---------------+
        | Respective name | Value         |
        +=================+===============+
        | PENDING         | `'PENDING'`   |
        +-----------------+---------------+
        | CANCELLED       | `'CANCELLED'` |
        +-----------------+---------------+
        | FINISHED        | `'FINISHED'`  |
        +-----------------+---------------+
        | RETRIEVED       | `'RETRIEVED'` |
        +-----------------+---------------+
        
        Note, that states are checked by memory address and not by equality. Also ``RETRIEVED`` is used only if
        `__debug__` is set as `True`.
    _count : `int`
        The amount, how much times the future's result need to be set, because it will yield.
    """
    __slots__ = ('_count',)
    
    def __new__(cls, loop, count):
        """
        Creates a new ``FutureWM`` object bound to the given `loop`, which will be marked as done, only if `count`
        results are set to it with ``.set_result``, or with ``.set_result_if_pending``.
        
        Parameters
        ----------
        loop : ``EventThread``
            The loop to what the created future will be bound to.
        count : `int`
            The amount of times, the future's result need to be set, because becoming done.
        """
        self = object.__new__(cls)
        self._loop = loop
        self._count = count
        self._state = PENDING
        
        self._result = []
        self._exception = None
        
        self._callbacks = []
        self._blocking = False
        
        return self
    
    def __repr__(self):
        """Returns the future's representation."""
        result = ['<', self.__class__.__name__, ' ']
        
        state = self._state
        result.append(state)
        
        if state is FINISHED or state is RETRIEVED:
            exception = self._exception
            if exception is None:
                results = self._result
                for index, result_ in enumerate(results):
                    result.append(f', result[')
                    result.append(repr(index))
                    result.append(']=')
                    result.append(reprlib.repr(result_))
                
                result.append(', needed=')
                result.append(str(self._count-len(results)))
            else:
                result.append(', exception=')
                result.append(repr(exception))
        
        callbacks = self._callbacks
        limit = len(callbacks)
        if limit:
            result.append(', callbacks=[')
            index = 0
            while True:
                callback = callbacks[index]
                result.append(format_callback(callback))
                index += 1
                if index == limit:
                    break
                
                result.append(', ')
                continue
            
            result.append(']')
        
        result.append('>')
        
        return ''.join(result)
    
    def set_result(self, result):
        """
        Sets the future result, and if it waits for no more results, marks it as done as well.
        
        Parameters
        ----------
        result : `Any`
            The object to set as result.
        
        Raises
        ------
        InvalidStateError
            If the future is already done.
        """
        if self._state is not PENDING:
            raise InvalidStateError(self, 'set_result')
        
        results = self._result
        results.append(result)
        if self._count != len(results):
            return
        
        self._state = FINISHED
        self._loop._schedule_callbacks(self)

    def set_result_if_pending(self, result):
        """
        Sets the future result, and if it waits for no more results, marks it as done as well. Not like
        ``.set_result``, this method will not raise ``InvalidStateError`` if the future is already done.
        d
        Parameters
        ----------
        result : `Any`
            The object to set as result.
        
        Returns
        ------
        set_result : `int` (`0`, `1`, `2`)
            If the future is already done, returns `0`. If the future's result was successfully set, returns `1`,
            meanwhile if the future was marked as done as well, returns `2`.
        """
        if self._state is not PENDING:
            return 0
        
        results = self._result
        results.append(result)
        if self._count != len(results):
            return 1
            
        self._state = FINISHED
        self._loop._schedule_callbacks(self)
        return 2
        
    def clear(self):
        """
        Clears the future making it reusable.
        """
        self._state = PENDING
        self._exception = None
        self._result.clear()
        self.cancel_handles()
        self._blocking = False

class Task(Future):
    """
    A Future-like object that runs a Python coroutine.
    
    Tasks are used to run coroutines in event loops. If a coroutine awaits on a ``Future`, the ``Task`` suspends the
    execution of the coroutine and waits for the completion of the ``Future``. When the ``Future`` is done, the
    execution of the wrapped coroutine resumes.
    
    Attributes
    ----------
    _blocking : `bool`
        Whether the task is already being awaited, so it blocks the respective coroutine.
    _callbacks : `list` of `callable`
        The callbacks of the task, which are queued up on the respective event loop to be called, when the task is
        finished. These callback should accept `1` parameter, the task itself.
        
        Note, if the task is already done, then the newly added callbacks are queued up instantly on the respective
        event loop to be called.
    
    _exception : `None` or `BaseException` instance
        The exception raised by task's internal coroutine. Defaults to `None`.
    _loop : ``EventThread``
        The loop to what the created task is bound.
    _result : `None` or `Any`
        The result of the task. Defaults to `None`.
    _state : `str`
        The state of the task.
        
        Can be set as one of the following:
        
        +-----------------+---------------+
        | Respective name | Value         |
        +=================+===============+
        | PENDING         | `'PENDING'`   |
        +-----------------+---------------+
        | CANCELLED       | `'CANCELLED'` |
        +-----------------+---------------+
        | FINISHED        | `'FINISHED'`  |
        +-----------------+---------------+
        | RETRIEVED       | `'RETRIEVED'` |
        +-----------------+---------------+
        
        Note, that states are checked by memory address and not by equality. Also ``RETRIEVED`` is used only if
        `__debug__` is set as `True`.
    
    _coro : `coroutine` or `generator`
        The wrapped coroutine.
    _fut_waiter : `None` or ``Future`` instance
        The future on what's result the future is waiting right now.
    _must_cancel : `bool`
        Whether the task is cancelled, and at it's next step a ``CancelledError`` would be raised into it's coroutine.
    """
    __slots__ = ('_coro', '_fut_waiter', '_must_cancel')
    
    def __new__(cls, coro, loop):
        """
        Creates a new ``Task`` object running the given coroutine on the given event loop.
        
        Parameters
        ----------
        coro : `coroutine` or `generator`
            The coroutine, what the task will on the respective event loop.
        loop : ``EventThread``
            The event loop on what the coroutine will run.
        """
        self = object.__new__(cls)
        self._loop = loop
        self._state = PENDING

        self._result = None
        self._exception = None
        
        self._callbacks = []
        self._blocking = False

        self._must_cancel = False
        self._fut_waiter = None
        self._coro = coro
        
        loop.call_soon(self._step)

        return self
    
    def get_stack(self, limit=-1):
        """
        Return the list of stack frames for the task. If the task is already done, returns an empty list.
        
        Parameters
        ----------
        limit : `int`, Optional
            The maximal amount of stacks to fetch. By giving it as negative integer, there will be no stack limit
            to fetch back, Defaults to `-1`.
        
        Returns
        -------
        frames : `list` of `frame`
            The stack frames of the task.
        """
        frames = []
        
        coro = self._coro
        if isinstance(coro, GeneratorType):
            frame = coro.gi_frame
        elif isinstance(coro, CoroutineType):
            frame = coro.cr_frame
        else:
            frame = None
        
        if frame is None:
            return frames
        
        while limit:
            limit -= 1
            
            if frame in frames:
                frames.append(frame)
                frames.append(None)
                return frames
            
            frames.append(frame)
            
            if isinstance(coro, GeneratorType):
                coro = coro.gi_yieldfrom
            elif isinstance(coro, CoroutineType):
                coro = coro.cr_await
            else:
                coro = None
            
            if coro is not None:
                if isinstance(coro, GeneratorType):
                    frame = coro.gi_frame
                elif isinstance(coro, CoroutineType):
                    frame = coro.cr_frame
                else:
                    frame = None
                
                if frame is not None:
                    continue
            
            self = self._fut_waiter
            if self is None:
                break
            
            del frames[-1]
            if not isinstance(self, Task):
                break
            
            coro = self._coro
            
            if isinstance(coro, GeneratorType):
                frame = coro.gi_frame
            elif isinstance(coro, CoroutineType):
                frame = coro.cr_frame
            else:
                frame = None
                
            if frame is None:
                break
        
        return frames
    
    def __repr__(self):
        """Returns the task's representation."""
        result = ['<', self.__class__.__name__, ' ']
        
        state = self._state
        result.append(state)
        
        if self._must_cancel:
            result.append(' (cancelling)')
        
        result.append(' coro=')
        result.append(format_coroutine(self._coro))
        
        fut_waiter = self._fut_waiter
        if fut_waiter is not None:
            result.append(', waits for=')
            if type(fut_waiter) is type(self):
                result.append(fut_waiter.qualname)
            else:
                result.append(repr(fut_waiter))
        
        if (not self._must_cancel) and (state is FINISHED or state is RETRIEVED):
            exception = self._exception
            if exception is None:
                result.append(', result=')
                result.append(reprlib.repr(self._result))
            else:
                result.append(', exception=')
                result.append(repr(exception))
        
        callbacks = self._callbacks
        limit = len(callbacks)
        if limit:
            result.append(', callbacks=[')
            index = 0
            while True:
                callback = callbacks[index]
                result.append(format_callback(callback))
                index += 1
                if index == limit:
                    break
                
                result.append(', ')
                continue
            
            result.append(']')
        
        result.append('>')
        
        return ''.join(result)
    
    def print_stack(self, limit=-1, file=None):
        """
        Prints the stack or traceback of the task.
        
        Parameters
        ----------
        limit : `int`, Optional
            The maximal amount of stacks to print. By giving it as negative integer, there will be no stack limit
            to print out, Defaults to `-1`.
        file : `None` or `I/O stream`, Optional
            The file to print the stack to. Defaults to `sys.stderr`.
        
        Notes
        -----
        If the task is finished with an exception, then `limit` is ignored when printing traceback.
        """
        local_thread = current_thread()
        if isinstance(local_thread, EventThread):
            return local_thread.run_in_executor(alchemy_incendiary(self._print_stack,(self, limit, file),))
        else:
            self._print_stack(self, limit, file)
    
    @staticmethod
    def _print_stack(self, limit, file):
        """
        Prints the stack or traceback of the task to the given `file`.
        
        Parameters
        ----------
        limit : `int`, Optional
            The maximal amount of stacks to print. By giving it as negative integer, there will be no stack limit
            to print out,
        file : `None` or `I/O stream`
            The file to print the stack to. Defaults to `sys.stderr`.
        
        Notes
        -----
        This function calls blocking operations and should not run inside of an event loop.
        
        If the task is finished with an exception, then `limit` is ignored when printing traceback.
        """
        if file is None:
            file = sys.stdout
        
        exception = self._exception
        
        if exception is None:
            frames = self.get_stack(limit)
            if frames:
                recursive = (frames[-1] is None)
                if recursive:
                    del frames[-1]

                extracted = ['Stack for ', repr(self), ' (most recent call last):\n']
                extracted = render_frames_to_list(frames, extend=extracted)
                if recursive:
                    extracted.append('Last frame is a repeat from a frame above. Rest of the recursive part is not rendered.')
            else:
                extracted = ['No stack for ', repr(self), '\n']
        else:
            extracted = render_exc_to_list(exception)
            extracted[0] = f'Traceback for {self!r} (most recent call last):\n'

        file.write(''.join(extracted))
    
    if __debug__:
        def cancel(self):
            state = self._state
            if state is not PENDING:
                if state is FINISHED:
                    self._state = RETRIEVED
                
                return 0
            
            fut_waiter = self._fut_waiter
            if (fut_waiter is None) or (not fut_waiter.cancel()):
                self._must_cancel = True
            
            return 1
        
    else:
        def cancel(self):
            if self._state is not PENDING:
                return 0
            
            fut_waiter = self._fut_waiter
            if (fut_waiter is None) or (not fut_waiter.cancel()):
                self._must_cancel = True
            
            return 1
    
    set_docs(cancel,
        """
        Cancels the waited future of the task, if it is still pending, causing the task to be cancelled as well.
        
        Returns
        -------
        cancelled : `int` (`0`, `1`)
            If the task is already done, returns `0`, if it got cancelled, returns `1`-
        
        Notes
        -----
        A task can be cancelled instantly, a step of it need run down, before the operation is done.
        
        If `__debug__` is set as `True`, then `.cancel()` also marks the task as retrieved, causing it to not render
        non-retrieved exceptions.
        """
    )
    
    @property
    def name(self):
        """
        Returns the task's wrapped coroutine's name.
        
        Returns
        -------
        name : `str`
        """
        coro = self._coro
        try:
            return coro.__name__
        except AttributeError:
            return coro.__class__.__name__
    
    @property
    def qualname(self):
        """
        Returns the task's wrapped coroutine's qualname.
        
        Returns
        -------
        qualname : `str`
        """
        coro = self._coro
        try:
            return coro.__qualname__
        except AttributeError:
            return coro.__class__.__qualname__
        
    def set_result(self, result):
        """
        Tasks do not support `.set_result` operation.
        
        Parameters
        ----------
        result : `Any`
            The object to set as result.
        
        Raises
        ------
        RuntimeError
            Tasks do not support `.set_result` operation.
        """
        raise RuntimeError(f'{self.__class__.__name__} does not support `.set_result` operation')
    
    def set_result_if_pending(self, result):
        """
        Tasks do not support `.set_result_if_pending` operation.
        
        Parameters
        ----------
        result : `Any`
            The object to set as result.
        
        Raises
        ------
        RuntimeError
            Tasks do not support `.set_result_if_pending` operation.
        """
        raise RuntimeError(f'{self.__class__.__name__} does not support `.set_result_if_pending` operation')
    
    # We will not send an exception to a task, but we will cancel it.
    # The exception will show up as `._exception` tho.
    # We also wont change the state of the Task, it will be changed, when the
    # next `._step` is done with the cancelling.
    def set_exception(self, exception):
        """
        Cancels the task and sets the given exception as it's.
        
        Parameters
        ----------
        exception : `BaseException`
            The exception to set as the task's exception.
        
        Raises
        ------
        InvalidStateError
            If the task is already done.
        TypeError
            If `StopIteration` is given as `exception`.
        """
        if self._state is not PENDING:
            raise InvalidStateError(self, 'set_exception')
    
        if (self._fut_waiter is None) or self._fut_waiter.cancel():
            self._must_cancel=True

        if isinstance(exception, type):
            exception = exception()
            
        if type(exception) is StopIteration:
             raise TypeError(f'{exception} cannot be raised to a {self.__class__.__name__}: {self!r}')
        
        self._exception = exception
    
    def set_exception_if_pending(self, exception):
        """
        Cancels the task and sets the given exception as it's. Not like ``.set_exception``, this method will not raise
        ``InvalidStateError`` if the task is already done.
        
        Parameters
        ----------
        exception : `BaseException`
            The exception to set as the task's exception.
        
        Returns
        ------
        set_result : `int` (`0`, `1`)
            If the task is already done, returns `0`, else `1`.
        
        Raises
        ------
        TypeError
            If `StopIteration` is given as `exception`.
        """
        if self._state is not PENDING:
            return 0
        
        if (self._fut_waiter is None) or self._fut_waiter.cancel():
            self._must_cancel=True
        
        if isinstance(exception, type):
            exception = exception()
        
        if type(exception) is StopIteration:
             raise TypeError(f'{exception} cannot be raised to a {self.__class__.__name__}: {self!r}')
        
        self._exception = exception
        return 1
    
    def clear(self):
        """
        Tasks do not support `.clear` operation.
        
        Raises
        ------
        RuntimeError
            Tasks do not support `.clear` operation.
        """
        raise RuntimeError(f'{self.__class__.__name__} does not support `.clear` operation')
    
    def _step(self, exception=None):
        """
        Does a step, by giving control to the wrapped coroutine by the task.
        
        If `exception` is given, then that exception will be raised to the internal coroutine, exception if the task
        is already cancelled, because, then the exception to raise will be decided by ``._must_exception``.
        
        Parameters
        ----------
        exception : `None` or `BaseException`
            Exception to raise into the wrapped coroutine.
        
        Raises
        ------
        InvalidStateError
            If the task is already done.
        """
        if self._state is not PENDING:
            raise InvalidStateError(self, '_step', message = \
                f'`{self.__class__.__name__}._step` already done of {self!r}, exception={exception!r}')
        
        if self._must_cancel:
            exception = self._must_exception(exception)
        
        coro = self._coro
        self._fut_waiter = None
        
        self._loop.current_task = self
        
        # call either coro.throw(err) or coro.send(None).
        try:
            if exception is None:
                result = coro.send(None)
            else:
                result = coro.throw(exception)
        except StopIteration as exception:
            if self._must_cancel:
                # the task is cancelled meanwhile
                self._must_cancel = False
                Future.set_exception(self, CancelledError())
            else:
                Future.set_result(self, exception.value)
        except CancelledError:
            Future.cancel(self)
        except BaseException as exception:
            Future.set_exception(self, exception)
        else:
            if isinstance(result, Future) and result._blocking:
                result._blocking = False
                result.add_done_callback(self._wake_up)
                self._fut_waiter = result
                if self._must_cancel:
                    if result.cancel():
                        self._must_cancel = False
            else:
                self._loop.call_soon(self._step)
        finally:
            self._loop.current_task = None
            self = None # Need to set `self` as `None`, or `self` might never get garbage collected.
    
    
    def _wake_up(self, future):
        """
        Callback used by ``._step``, when the wrapped coroutine waits on a future to be marked as done.
        
        Parameters
        ----------
        future : ``Future`` instance
            The future for what's completion the task is waiting for.
        """
        try:
            future.result()
        except BaseException as err:
            self._step(err)
        else:
            self._step()
        
        self = None # set self as `None`, so when exception occurs, self can be garbage collected.
    
    def _must_exception(self, exception):
        """
        Returns the exception, what should be raised into the tasks's wrapped coroutine.
        
        Parameters
        ----------
        exception : `None` or `BaseException`
            The exception, what would be preferable raised into the task.
        
        Returns
        -------
        exception : `BaseException`
            If task has already `˙._exception`˙ set, returns that. If `exception` is given as `None`, or as non
            ``CancelledError`` instance, will create a new ``CancelledError`` instance and return that.
        """
        self_exception = self._exception
        if self_exception is None:
            if (exception is None) or (not isinstance(exception, CancelledError)):
                exception = CancelledError()
        else:
            exception = self_exception
        
        self._must_cancel = False
        return exception

class AsyncQueue:
    """
    An asynchronous FIFO queue.
    
    ``AsyncQueue`` is async iterable, so if you iterate over it inside of an `async for` loop do
    `.set_exception(CancelledError())` to stop it without any specific exception.
    
    Attributes
    ----------
    _exception : `None` or `BaseException` instance
        The exception set as the queue's result to raise, when the queue gets empty.
    _loop : ``EventThread``
        The loop to what the queue is bound to.
    _results : `deque`
        The results of the queue, which can be retrieved by ``.result``, ``.result_no_wait``, or by awaiting it.
    _waiter : `None` or ``Future``
        If the queue is empty and it's result is already waited, then this future is set. It's result is set, by the
        first ``.set_result``, or ``.set_exception`` call.
    """
    __slots__ = ('_exception', '_loop', '_results', '_waiter',)
    def __new__(cls, loop, iterable=None, max_length=None, exception=None):
        """
        Creates a new ``AsyncQueue`` instance with the given parameter.
        
        Parameters
        ----------
        loop : ``EventThread``
            The loop to what the created queue will be bound to.
        max_length : `None` or `int`, Optional
            The maximal length of the queue.
        exception : `None` or `BaseException` instance
            Exception to raise when the queue is empty.
        
        Raises
        ------
        TypeError
            If `StopIteration` is given as `exception`.
        """
        if (exception is not None):
            if isinstance(exception, type):
                exception = exception()
            
            if type(exception) is StopIteration:
                 raise TypeError(f'{exception} cannot be raised to a {cls.__name__}')
        
        if iterable is None:
            results = deque(maxlen=max_length)
        else:
            results = deque(iterable, maxlen=max_length)
        
        self = object.__new__(cls)
        self._loop = loop
        self._results = results
        self._waiter = None
        self._exception = exception
        
        return self
    
    def set_result(self, element):
        """
        Puts the given `element` on the queue. If the queue is empty and it's result is already waited, feeds it to
        ``._waiter`` instead.
        
        Parameters
        ----------
        element : `Any`
            The object to put on the queue.
        """
        # should we raise InvalidStateError?
        waiter = self._waiter
        if waiter is None:
            self._results.append(element)
        else:
            self._waiter = None
            waiter.set_result_if_pending(element)
    
    def set_exception(self, exception):
        """
        Sets the given `exception` to raise, when it's queue gets empty. If the queue is empty and it's result is
        already waited, feeds it to ``._waiter`` instead.
        
        Parameters
        ----------
        exception : `None` or `BaseException` instance
            Exception to raise when the queue is empty.
        
        Raises
        ------
        TypeError
            If `StopIteration` is given as `exception`.
        """
        # should we raise InvalidStateError?
        if isinstance(exception, type):
            exception = exception()
        
        if type(exception) is StopIteration:
             raise TypeError(f'{exception} cannot be raised to a {self.__class__.__name__}: {self!r}')
        
        self._exception = exception
        
        waiter = self._waiter
        if waiter is not None:
            self._waiter = None
            waiter.set_exception_if_pending(exception)
    
    def __await__(self):
        """
        Waits till the next element of the queue is set. If the queue has elements set, yields the next of them, or if
        the queue has exception set, raises it.
        
        This method is a generator. Should be used with `await` expression.
        
        Returns
        -------
        result : `Any`
            The next element on the queue.
        
        Raises
        ------
        BaseException
            Exception set to the queue, to raise when it is empty.
        """
        results = self._results
        if results:
            return results.popleft()
        
        exception = self._exception
        if exception is not None:
            raise exception
        
        waiter = self._waiter
        if waiter is None:
            waiter = Future(self._loop)
            self._waiter = waiter
        
        return (yield from waiter)
    
    result = to_coroutine(copy_func(__await__))
    
    def result_no_wait(self):
        """
        Returns the queue's next element if applicable.
        Waits till the next element of the queue is set. If the queue has elements set, yields the next of them, or if
        the queue has exception set, raises it.
        
        Returns
        -------
        result : `Any`
            The next element on the queue.
        
        Raises
        ------
        IndexError
            The queue is empty.
        BaseException
            Exception set to the queue, to raise when it is empty.
        """
        results = self._results
        if results:
            return results.popleft()
        
        exception = self._exception
        if exception is None:
            raise IndexError('The queue is empty')
        
        raise exception
    
    def __repr__(self):
        """Returns the async queue's representation."""
        repr_parts = [
            self.__class__.__name__,
            '([',
        ]
        
        results = self._results
        limit = len(results)
        if limit:
            index = 0
            while True:
                element = results[index]
                repr_parts.append(repr(element))
                index += 1
                if index == limit:
                    break
                
                repr_parts.append(', ')
            
        repr_parts.append(']')
        
        max_length = results.maxlen
        if (max_length is not None):
            repr_parts.append(', max_length=')
            repr_parts.append(repr(max_length))
        
        exception = self._exception
        if (exception is not None):
            repr_parts.append(', exception=')
            repr_parts.append(str(exception))
        
        repr_parts.append(')')
        return ''.join(repr_parts)
    
    __str__ = __repr__
    
    def __aiter__(self):
        """
        Async iterating over an ``AsyncQueue``, returns itself
        
        Returns
        -------
        self : ``AsyncQueue``
        """
        return self
    
    async def __anext__(self):
        """
        Waits till the next element of the queue is set. If the queue has elements set, yields the next of them, or if
        the queue has exception set, raises it.
        
        If the queue has ``CancelledError`` set as ``._exception``, then raises ``StopAsyncIteration`` to stop the queue
        instead.
        
        This method is a coroutine.
        
        Returns
        -------
        result : `Any`
            The next element on the queue.
        
        Raises
        ------
        StopAsyncIteration
            If the queue was cancelled with ``CancelledError``.
        BaseException
            Exception set to the queue, to raise when it is empty.
        """
        results = self._results
        if results:
            return results.popleft()
        
        exception = self._exception
        if exception is not None:
            if type(exception) is CancelledError:
                raise StopAsyncIteration from CancelledError
            
            raise exception
        
        waiter = self._waiter
        if waiter is None:
            waiter = Future(self._loop)
            self._waiter = waiter
        
        try:
            return (await waiter)
        except CancelledError as err:
            raise StopAsyncIteration from err
    
    # deque operations
    
    @property
    def max_length(self):
        """
        Returns the queue's max length.
        
        Returns
        -------
        max_length: `int`
        """
        return self._results.maxlen
    
    def clear(self):
        """
        Clears the queue's results.
        """
        self._results.clear()
    
    def copy(self):
        """
        Copies the queue.
        
        Returns
        -------
        new : ``AsyncQueue``
        """
        new = object.__new__(type(self))
        new._loop = self._loop
        new._results = self._results.copy()
        new._waiter = None
        new._exception = self._exception
        
        return new
    
    def reverse(self):
        """
        Reverses the queue's actual results.
        """
        self._results.reverse()
    
    def __len__(self):
        """
        Returns the queue's actual length.
        """
        return len(self._results)
    
    if __debug__:
        def __del__(self):
            """
            If the queue has ``_waiter`` set, silences it.
            
            Notes
            -----
            This function is only present, when `__debug__` is set as `True`.
            """
            waiter = self._waiter
            if waiter is not None:
                waiter.__silence__()


class AsyncLifoQueue(AsyncQueue):
    """
    An asynchronous LIFO queue.
    
    ``AsyncLifoQueue`` is async iterable, so if you iterate over it inside of an `async for` loop do
    `.set_exception(CancelledError())` to stop it without any specific exception.
    
    Attributes
    ----------
    _exception : `None` or `BaseException` instance
        The exception set as the queue's result to raise, when the queue gets empty.
    _loop : ``EventThread``
        The loop to what the queue is bound to.
    _results : `deque`
        The results of the queue, which can be retrieved by ``.result``, ``.result_no_wait``, or by awaiting it.
    _waiter : `None` or ``Future``
        If the queue is empty and it's result is already waited, then this future is set. It's result is set, by the
        first ``.set_result``, or ``.set_exception`` call.
    """
    __slots__ = ()
    
    @copy_docs(AsyncQueue.__await__)
    def __await__(self):
        results = self._results
        if results:
            return results.pop()
        
        exception = self._exception
        if exception is not None:
            raise exception
        
        waiter = self._waiter
        if waiter is None:
            waiter = Future(self._loop)
            self._waiter = waiter
        
        return (yield from waiter)
    
    @copy_docs(AsyncQueue.result_no_wait)
    def result_no_wait(self):
        results = self._results
        if results:
            return results.pop()
        
        exception = self._exception
        if exception is None:
            raise IndexError('The queue is empty')
        
        raise exception
    
    @copy_docs(AsyncQueue.__anext__)
    async def __anext__(self):
        results = self._results
        if results:
            return results.pop()
        
        exception = self._exception
        if exception is not None:
            if type(exception) is CancelledError:
                raise StopAsyncIteration from CancelledError
            
            raise exception
        
        waiter = self._waiter
        if waiter is None:
            waiter = Future(self._loop)
            self._waiter = waiter
        
        try:
            return (await waiter)
        except CancelledError as err:
            raise StopAsyncIteration from err


class FGElement:
    """
    An element of a ``FutureG`` results.
    
    Attributes
    ----------
    result : `Any`
        The result of a gathered future.
    exception : `None` or `BaseException`
        The exception of a gathered exception.
    """
    __slots__ = ('exception', 'result',)
    def __init__(self, result, exception):
        """
        Creates a new ``FGElement`` with the given parameters.
        
        Parameters
        ----------
        result : `Any`
            The result of a gathered future.
        exception : `None` or `BaseException`
            The exception of a gathered exception.
        """
        self.result = result
        self.exception = exception
    
    def __call__(self):
        """
        Returns a gathered future's result or raises it's exception.
        
        Returns
        -------
        result : `Any`
            A gathered future's result.
        
        Raises
        ------
        BaseException
            A gathered future's exception.
        """
        exception = self.exception
        if exception is None:
            return self.result
        raise exception

class FGCallback:
    """
    Callback of ``FutureG`` to set a waited future's result or exception to itself.
    
    Attributes
    ----------
    parent : ``FutureG``
        The gathering future
    """
    __slots__ = ('parent',)
    def __init__(self, parent):
        """
        Creates a new gathering future callback.
        
        Parameters
        ----------
        parent : ``FutureG``
            The gathering future
        """
        self.parent = parent
    
    def __call__(self, future):
        """
        Sets a result of an exception to the parent gatherer future.
        
        Parameters
        ----------
        future : ``Future`` instance
            A waited future.
        """
        parent = self.parent
        try:
            result = future.result()
        except BaseException as err:
            parent.set_exception_if_pending(err)
        else:
            parent.set_result_if_pending(result)


class Gatherer(FutureWM):
    """
    A ``Future`` subclass to gather more future's results and their exceptions.
    
    Attributes
    ----------
    _blocking : `bool`
        Whether the future is already being awaited, so it blocks the respective coroutine.
    _callbacks : `list` of `callable`
        The callbacks of the future, which are queued up on the respective event loop to be called, when the future is
        finished. These callback should accept `1` parameter, the future itself.
        
        Note, if the future is already done, then the newly added callbacks are queued up instantly on the respective
        event loop to be called.
    
    _exception : `None` or `BaseException` instance
        The exception set to the future as it's result. Defaults to `None`.
    _loop : ``EventThread``
        The loop to what the created future is bound.
    _result : `list` of ``FGElement``
        The already gathered future's results.
    _state : `str`
        The state of the future.
        
        Can be set as one of the following:
        
        +-----------------+---------------+
        | Respective name | Value         |
        +=================+===============+
        | PENDING         | `'PENDING'`   |
        +-----------------+---------------+
        | CANCELLED       | `'CANCELLED'` |
        +-----------------+---------------+
        | FINISHED        | `'FINISHED'`  |
        +-----------------+---------------+
        | RETRIEVED       | `'RETRIEVED'` |
        +-----------------+---------------+
        
        Note, that states are checked by memory address and not by equality. Also ``RETRIEVED`` is used only if
        `__debug__` is set as `True`.
    _count : `int`
        The amount, for how much future's result the gatherer waits.
    """
    __slots__ = ()
    
    def __new__(cls, loop, coros_or_futures):
        """
        Creates a new gatherer bound to the given `loop`, waiting for the given `coros_or_futures`-s results.
        
        Parameters
        ----------
        loop : ``EventThread``
            The loop to what the created future will be bound to.
        coros_or_futures : `iterable` of `awaitable`
            Awaitables, which result will be gathered.
        
        Raises
        ------
        TypeError
            Any of the given `coros_or_futures` is not awaitable.
        """
        awaitables = set()
        for awaitable in coros_or_futures:
            if not is_awaitable(awaitable):
                raise TypeError(f'Cannot await on {awaitable.__class__.__name__}: {awaitable!r}')
            awaitables.add(awaitable)
        
        self = object.__new__(cls)
        self._loop = loop
        self._count = len(awaitables)
        
        self._result = []
        self._exception = None
        
        self._callbacks = []
        self._blocking = False
        
        if awaitables:
            self._state = PENDING
            
            callback = FGCallback(self)
            
            for awaitable in awaitables:
                task = loop.ensure_future(awaitable)
                task.add_done_callback(callback)
        else:
            self._state = FINISHED
        
        return self
    
    def set_result(self, result):
        """
        Sets a result to the gatherer. if all the expected results of the gatherer are retrieved already, marks it as
        done as well.
        
        Parameters
        ----------
        result : `Any`
            The object to set as result.
        
        Raises
        ------
        InvalidStateError
            If the gatherer is already done.
        """
        if self._state is not PENDING:
            raise InvalidStateError(self, 'set_result')
        
        results = self._result
        results.append(FGElement(result, None))
        if self._count != len(results):
            return
        
        self._state = FINISHED
        self._loop._schedule_callbacks(self)

    def set_result_if_pending(self, result):
        """
        Sets a result to the gatherer. If all the expected results of the gatherer are retrieved already, marks it as
        done as well. Not like ``.set_result``, this method will not raise ``InvalidStateError`` if the future is
        already done.
        
        Parameters
        ----------
        result : `Any`
            The object to set as result.
        
        Returns
        ------
        set_result : `int` (`0`, `1`, `2`)
            If the gatherer is already done, returns `0`. If the gatherer's result was successfully set, returns `1`,
            meanwhile if the gatherer was marked as done as well, returns `2`.
        """
        if self._state is not PENDING:
            return 0
        
        results = self._result
        results.append(FGElement(result, None))
        if self._count != len(results):
            return 2
        
        self._state = FINISHED
        self._loop._schedule_callbacks(self)
        return 1
    
    def set_exception(self, exception):
        """
        Sets an exception to the gatherer. If all the expected results of the gatherer are retrieved already, marks it
        as done as well.
        
        Parameters
        ----------
        exception : `BaseException`
            The exception to set as a result of the gatherer.
        
        Raises
        ------
        InvalidStateError
            If the gatherer is already done.
        TypeError
            If `StopIteration` is given as `exception`.
        """
        if self._state is not PENDING:
            raise InvalidStateError(self, 'set_exception')
        
        if isinstance(exception, type):
            exception = exception()
        
        if type(exception) is StopIteration:
             raise TypeError(f'{exception} cannot be raised to a {self.__class__.__name__}: {self!r}')
        
        results = self._result
        results.append(FGElement(None, exception))
        if self._count != len(results):
            return
        
        self._state = FINISHED
        self._loop._schedule_callbacks(self)

    def set_exception_if_pending(self, exception):
        """
        Sets an exception to the gatherer. If all the expected results of the gatherer are retrieved already, marks it
        as done as well. Not like ``.set_exception``, this method will not raise ``InvalidStateError`` if the future is
        already done.
        
        Parameters
        ----------
        exception : `BaseException`
            The exception to set as a result of the gatherer.
        
        Returns
        ------
        set_result : `int` (`0`, `1`, `2`)
            If the gatherer is already done, returns `0`. If the exception was set successfully as a gatherer result,
            returns `1`, meanwhile if the gatherer was marked as done as well, returns `2`.
        
        Raises
        ------
        TypeError
            If `StopIteration` is given as `exception`.
        """
        if self._state is not PENDING:
            return 0
        
        results = self._result
        results.append(FGElement(None, exception))
        if self._count != len(results):
            return 1
        
        self._state = FINISHED
        self._loop._schedule_callbacks(self)
        return 2

class _HandleCancellerBase:
    """
    ``Future`` callback-base to cancel a respective ``Handle`` instance when the future is marked as done before the
    handle, or if the handler runs first, then sets the future result or exception.
    
    This class do not implements ``.__call__`. Subclasses should implement that.
    
    Attributes
    ----------
    handler : `None` or ``Handle``
        The handle to cancel, when the future is marked as done before the respective handle ran.
    """
    __slots__ = ('handler',)
    def __init__(self):
        """
        Creates a new handle canceller.
        
        Note, that a handle canceller is created with empty ``.handle``, because it is a callback and a ``Handle``'s
        function at the same time, so ``.handle`` is needed to be set from outside.
        """
        self.handler = None
    
    def __call__(self, future):
        """
        Called by the respective ``Future`` instance as callback, or by the respective handle.
        
        Subclasses should overwrite this method.
        
        Parameters
        ----------
        future : ``Future`` instance
            The respective future to what the handle canceller was added as callback.
        """
        pass
    
    def cancel(self):
        """
        Cancels the handle.
        
        This method is usually called when the respective future's handles are cleared.
        """
        handler = self.handler
        if handler is None:
            return
         
        self.handler = None
        handler.cancel()

class _SleepHandleCanceller(_HandleCancellerBase):
    """
    ``Future`` callback to cancel a respective ``Handle`` instance when the future is marked as done before the
    handle, or if the handler runs first, then sets the future result as `None˛.
    
    Attributes
    ----------
    handler : `None` or ``Handle``
        The handle to cancel, when the future is marked as done before the respective handle ran.
    """
    __slots__ = ()
    def __call__(self, future):
        """
        Called by the respective ``Future`` instance as callback, or by the respective handle. Sets the given
        `future`'s result as `None` if applicable.
        
        Sets ``._handle`` as `None`, marking the canceller as it ran already.
        
        Parameters
        ----------
        future : ``Future`` instance
            The respective future to what the handle canceller was added as callback.
        """
        handler = self.handler
        if handler is None:
            return
        
        self.handler = None
        handler.cancel()
        future.set_result_if_pending(None)


def sleep(delay, loop=None):
    """
    Suspends the current task, allowing other tasks to run.
    
    Parameters
    ----------
    delay : `float`
        The time to block sleep in seconds.
    loop : `None` or ``EventThread``, Optional
        The event loop to which the returned `future` will be bound to. If not given, or given as `None`, then the
        current event loop will be used.
    
    Returns
    -------
    future : ``Future``
        Future, what can be awaited, to suspend a task.
    
    Raises
    ------
    RuntimeError
        The given or the local event loop is already stopped.
    """
    if loop is None:
        loop = current_thread()
        if not isinstance(loop, EventThread):
            raise RuntimeError(f'`sleep` called without passing `loop` parameter from a non {EventThread.__name__}: '
                f'{loop!r}.')
    
    future = Future(loop)
    if delay <= 0.:
        future.set_result(None)
        return future
    
    callback = object.__new__(_SleepHandleCanceller)
    handler = loop.call_later(delay, callback, future)
    if handler is None:
        raise RuntimeError(f'`sleep` was called with future with a stopped loop {loop!r}')
    
    future._callbacks.append(callback)
    callback.handler = handler
    return future


@to_coroutine
def skip_ready_cycle():
    """
    Skips a ready cycle.
    
    This function is a coroutine.
    """
    yield


class _TimeoutHandleCanceller(_HandleCancellerBase):
    """
    ``Future`` callback to cancel a respective ``Handle`` instance when the future is marked as done before the
    handle, or if the handler runs first, then sets the future's exception to `TimeoutError`.
    
    Attributes
    ----------
    handler : `None` or ``Handle``
        The handle to cancel, when the future is marked as done before the respective handle ran.
    """
    __slots__ = ('handler',)
    
    def __call__(self, future):
        """
        Called by the respective ``Future`` instance as callback, or by the respective handle. Sets the given
        `future`'s exception to `TimeoutError` if applicable.
        
        Sets ``._handle`` as `None`, marking the canceller as it ran already.
        
        Parameters
        ----------
        future : ``Future`` instance
            The respective future to what the handle canceller was added as callback.
        """
        handler = self.handler
        if handler is None:
            return
        
        handler.cancel()
        self.handler = None
        future.set_exception_if_pending(TimeoutError())

def future_or_timeout(future, timeout):
    """
    If the given ``Future`` is not done till the given `timeout` occurs, set `TimeoutError` as it's exception.
    
    Parameters
    ----------
    future : ``future`` instance
        The future to set the timeout to.
    timeout : `float`
        The time after the given `future`'s exception is set as `TimeoutError`.
    
    Raises
    ------
    RuntimeError
        The future's event loop is already stopped.
    
    Notes
    -----
    For futures, which wait for more results and exceptions like ``Gatherer``, `TimeoutError` gives only 1 result,
    rigging it's results. This is not the case of ``FutureWM``, because that stops when the first exception is received.
    
    If `future_or_timeout` is used on ``WaitTillFirst``, ``WaitTillAll`` or on ``WaitTillAll``, then they stop
    collecting their result at the point, when the timeout occurs and they yield their actual result at that point
    without any specific exception.
    
    At the case of ``WaitContinuously``, when the timeout occurs the next yielded result will be `None` instead of a
    ``Future`` instance.
    """
    loop = future._loop
    callback = _TimeoutHandleCanceller()
    handler = loop.call_later(timeout, callback, future)
    if handler is None:
        raise RuntimeError(f'`future_or_timeout` was called with future with a stopped loop {loop!r}')
    
    callback.handler = handler
    future.add_done_callback(callback)

class _FutureChainer:
    """
    Chains a future's result into an other one used as a callback of the source future.
    
    Attributes
    ----------
    target : ``Future``
        The target future to chain the result into if applicable.
    """
    __slots__ = ('target',)
    def __init__(self, target):
        """
        Creates a new ``_FutureChainer`` instance with the given target future.
        
        Parameters
        ----------
        target : ``Future``
            The target future to chain the result into if applicable.
        """
        self.target = target
    
    if __debug__:
        def __call__(self, future):
            # remove chain remover
            target = self.target
            callbacks = target._callbacks
            for index in range(len(callbacks)):
                callback = callbacks[index]
                if (type(callback) is _ChainRemover) and (callback.target is future):
                    del callbacks[index]
                    break
            
            # set result
            state = future._state
            if state is FINISHED:
                future._state = RETRIEVED
                if future._exception is None:
                    target.set_result(future._result)
                else:
                    target.set_exception(future._exception)
                return
            
            if state is RETRIEVED:
                if future._exception is None:
                    target.set_result(future._result)
                else:
                    target.set_exception(future._exception)
                return
            
            # if state is CANCELLED: normally, but the future can be cleared as well.
            target.cancel()
    
    else:
        def __call__(self, future):
            # remove chain remover
            target = self.target
            callbacks = target._callbacks
            for index in range(len(callbacks)):
                callback = callbacks[index]
                if type(callback) is _ChainRemover and callback.target is future:
                    del callbacks[index]
                    break
            
            # set result
            if future._state is FINISHED:
                exception = future._exception
                if exception is None:
                    target.set_result(future._result)
                else:
                    target.set_exception(exception)
                return
            
            # if state is CANCELLED: normally, but the future can be cleared as well.
            target.cancel()
    
    set_docs(__call__,
        """
        Chains the source future's result into the target one.
        
        Parameters
        ----------
        future : ``Future`` instance
            The source future to chain it's result from.
        """
    )

class _ChainRemover:
    """
    Removes the ``_FutureChainer`` callback of the source future if the chained target future is marked as done before.
    
    Parameters
    -------
    target : ``Future`` instance
        The source future.
    """
    __slots__ = ('target',)
    def __init__(self, target):
        self.target = target
    
    def __call__(self, future):
        # remove chainer
        callbacks = self.target._callbacks
        for index in range(len(callbacks)):
            callback = callbacks[index]
            if (type(callback) is _FutureChainer) and (callback.target is future):
                del callbacks[index]
                if __debug__:
                    # because this might be the only place, where we retrieve the result, we will just silence it.
                    future.__silence__()
                break

def shield(awaitable, loop):
    """
    Protects the given `awaitable` from being cancelled.
    
    Parameters
    ----------
    awaitable : `awaitable`
        The awaitable object to shield.
    loop : ``EventThread``
        The event loop to run the `awaitable` on.
    
    Returns
    -------
    TypeError
        The given `awaitable` is not `awaitable`.
    
    Returns
    -------
    un_protected : ``Future`` instance
        If the given `awaitable` is a finished task, returns it, else returns a ``Future``, to what the original
        awaitable's result will be chained to.
    """
    protected = loop.ensure_future(awaitable)
    if protected._state is not PENDING:
        return protected # already done, we can return
    
    un_protected = Future(loop)
    protected._callbacks.append(_FutureChainer(un_protected))
    un_protected._callbacks.append(_ChainRemover(protected))
    return un_protected

class WaitTillFirst(Future):
    """
    A future subclass, which waits till the first task or future is completed from the given ones. When finished,
    returns the `done` and the `pending` futures.
    
    Attributes
    ----------
    _blocking : `bool`
        Whether the future is already being awaited, so it blocks the respective coroutine.
    _callbacks : `list` of `callable`
        The callbacks of the future, which are queued up on the respective event loop to be called, when the future is
        finished. These callback should accept `1` parameter, the future itself.
        
        Note, if the future is already done, then the newly added callbacks are queued up instantly on the respective
        event loop to be called.
    
    _exception : `None` or `BaseException` instance
        The exception set to the future as it's result. Defaults to `None`.
    _loop : ``EventThread``
        The loop to what the created future is bound.
    _result : `tuple` (`set` of ``Future`` instances, `set` of ``Future`` instances)
        The result of the future. Defaults to `None`.
    _state : `str`
        The state of the future.
        
        Can be set as one of the following:
        
        +-----------------+---------------+
        | Respective name | Value         |
        +=================+===============+
        | PENDING         | `'PENDING'`   |
        +-----------------+---------------+
        | CANCELLED       | `'CANCELLED'` |
        +-----------------+---------------+
        | FINISHED        | `'FINISHED'`  |
        +-----------------+---------------+
        | RETRIEVED       | `'RETRIEVED'` |
        +-----------------+---------------+
        
        Note, that states are checked by memory address and not by equality. Also ``RETRIEVED`` is used only if
        `__debug__` is set as `True`.
    
    _callback : ``._wait_callback``
        Callback added to the waited futures.
    """
    __slots__ = ('_callback', )
    
    def __new__(cls, futures, loop):
        """
        Creates a new ``WaitTillFirst`` object with the given parameters.
        
        Parameters
        ----------
        futures : `iterable` of ``Future`` instances
            The futures from which we will wait on the first to complete.
        loop : ``EventThread``
            The loop to what the created future will be bound to.
        """
        pending = set(futures)
        done = set()
        
        self = object.__new__(cls)
        self._loop = loop
        
        callback = cls._wait_callback(self)
        self._callback = callback
        
        self._result = (done, pending)
        self._exception = None
        
        self._callbacks = []
        self._blocking = False
        
        if pending:
            try:
                for future in pending:
                    future.add_done_callback(callback)
            finally:
                self._state = PENDING
        else:
            self._state = FINISHED
        
        return self
    
    # `__repr__` is same as ``Future.__repr__``
    
    class _wait_callback:
        """
        ``WaitTillFirst``'s callback put on the future's waited by it.
        
        Attributes
        ----------
        _parent : ``WaitTillFirst``
            The parent future.
        """
        __slots__ = ('_parent',)
        
        def __init__(self, parent):
            """
            Creates a new ``WaitTillFirst`` callback object with the given parent ``WaitTillFirst`` instance.
            
            Parameters
            ----------
            parent : ``WaitTillFirst``
                The parent future.
            """
            self._parent = parent
        
        def __call__(self, future):
            """
            The callback, which runs when a waited future is done.
            
            Removes the done future from the parent's `pending` futures and puts it on the `done` ones. Also marks the
            parent ``WaitTillFirst`` instance as finished.
            
            Parameters
            ----------
            future : ``Future`` instance
                A done waited future.
            """
            parent = self._parent
            if parent is None:
                return
            
            done, pending = parent._result
            
            pending.remove(future)
            done.add(future)
            
            parent._mark_as_finished()
    
    def _mark_as_finished(self):
        """
        Marks self as finished, ensures it's callbacks, stops other waited futures to go to it's `done` result group
        and removes it's callback from the non-yet-done futures as well.
        """
        self._state = FINISHED
        self._loop._schedule_callbacks(self)
        
        callback = self._callback
        callback._parent = None
        
        for future in self._result[1]:
            future.remove_done_callback(callback)
    
    @property
    def futures_done(self):
        """
        Returns the already done futures.
        
        Returns
        -------
        done : `set` of ``Future`` instances.
        """
        return self._result[0]
    
    @property
    def futures_pending(self):
        """
        Returns the yet pending futures.
        
        Returns
        -------
        done : `set` of ``Future`` instances.
        """
        return self._result[1]
    
    # cancels the future, but every pending one as well.
    if __debug__:
        def cancel(self):
            state = self._state
            if state is not PENDING:
                if state is FINISHED:
                    self._state = RETRIEVED
                
                return 0
                
            self._callback._parent = None
            for future in self._result[1]:
                future.cancel()
            
            self._state = CANCELLED
            self._loop._schedule_callbacks(self)
            return 1
    
    else:
        def cancel(self):
            if self._state is not PENDING:
                return 0
            
            self._callback._parent = None
            for future in self._result[1]:
                future.cancel()
            
            self._state = CANCELLED
            self._loop._schedule_callbacks(self)
            return 1
    
    set_docs(cancel,
        """
        Cancels the future if it is pending.
        
        By cancelling the main waiter future, the not yet done futures will be also cancelled as well.
        
        Returns
        -------
        cancelled : `int` (`0`, `1`)
            If the future is already done, returns `0`, if it got cancelled, returns `1`.
        
        Notes
        -----
        If `__debug__` is set as `True`, then `.cancel()` also marks the future as retrieved, causing it to not render
        non-retrieved exceptions.
        """
    )
    
    # `cancelled` is same as ``Future.cancelled``
    # `done` is same as ``Future.done``
    # `pending` is same as ``Future.pending``
    # `result` is same as ``Future.result``
    # `exception` is same as ``Future.exception``
    # `add_done_callback` is same as ``Future.add_done_callback``
    # `remove_done_callback` is same as ``Future.remove_done_callback``
    
    def set_result(self, result):
        """
        Result waiter future types do not support `.set_result` operation.
        
        Parameters
        ----------
        result : `Any`
            The object to set as result.
        
        Raises
        ------
        RuntimeError
            Waiter futures do not support `.set_result` operation.
        """
        raise RuntimeError(f'{self.__class__.__name__} does not support `set_result` operation.')
    
    def set_result_if_pending(self, result):
        """
        Result waiter future types do not support `.set_result_if_pending` operation.
        
        Parameters
        ----------
        result : `Any`
            The object to set as result.
        
        Raises
        ------
        RuntimeError
            Waiter futures do not support `.set_result_if_pending` operation.
        """
        raise RuntimeError(f'{self.__class__.__name__} does not support `set_result_if_pending` operation.')
    
    def set_exception(self, exception):
        """
        Sets an exception as a result of the waiter future.
        
        If `exception` is given as `TimeoutError`, then the waiter will not raise, instead will yield it's `done`
        and `pending` future's current status.
        
        Parameters
        ----------
        exception : `BaseException`
            The exception to set as the future's exception.
        
        Raises
        ------
        InvalidStateError
            If the task is already done.
        TypeError
            If `StopIteration` is given as `exception`.
        """
        if self._state is not PENDING:
            raise InvalidStateError(self, 'set_exception')
        
        if isinstance(exception, type):
            exception = exception()
        
        if type(exception) is StopIteration:
             raise TypeError(f'{exception} cannot be raised to a {self.__class__.__name__}: {self!r}.')
        
        if type(exception) is not TimeoutError:
            self._exception = exception
        
        self._mark_as_finished()
    
    def set_exception_if_pending(self, exception):
        """
        Sets an exception as a result of the waiter future. Not like ``.set_exception``, this method will not raise
        ``InvalidStateError`` if the future is already done.
        
        If `exception` is given as `TimeoutError`, then the waiter will not raise, instead will yield it's `done`
        and `pending` future's current status.
        
        Parameters
        ----------
        exception : `BaseException`
            The exception to set as the future's exception.
        
        Returns
        ------
        set_result : `int` (`0`, `1`)
            If the future is already done, returns `0`. If `exception` is given as `TimeoutError`, returns `2`, else
            `1`.
        
        Raises
        ------
        TypeError
            If `StopIteration` is given as `exception`.
        """
        if self._state is not PENDING:
            return 0
        
        if isinstance(exception, type):
            exception = exception()
        
        if type(exception) is StopIteration:
             raise TypeError(f'{exception} cannot be raised to a {self.__class__.__name__}: {self!r}.')
        
        self._mark_as_finished()
        
        if type(exception) is TimeoutError:
            return 2
        
        self._exception = exception
        return 1
    
    # `__iter__` is same as ``Future.__iter__``
    # `__await__` is same as ``Future.__await__``
    # if __debug__:
    #    `__del__` is same as ``Future.__del__``
    #    `__silence__` is same as ``Future.__silence__``
    #    `__silence_cb__` is same as ``Future.__silence_cb__``
    # `cancel_handles` is same as ``Future.cancel_handles``
    
    def clear(self):
        """
        Waiter futures do not support `.clear` operation.
        
        Raises
        ------
        RuntimeError
            Waiter futures do not support `.clear` operation.
        """
        raise RuntimeError(f'{self.__class__.__name__} does not support `.clear` operation.')
    
    # `sync_wrap` is same as ``Future.sync_wrap``
    # `async_wrap` is same as ``Future.async_wrap``
    
class WaitTillExc(WaitTillFirst):
    """
    A future subclass, which waits till the first task or future raises an exception, or till all of them becomes done.
    When finished, returns the `done` and the `pending` futures.
    
    Attributes
    ----------
    _blocking : `bool`
        Whether the future is already being awaited, so it blocks the respective coroutine.
    _callbacks : `list` of `callable`
        The callbacks of the future, which are queued up on the respective event loop to be called, when the future is
        finished. These callback should accept `1` parameter, the future itself.
        
        Note, if the future is already done, then the newly added callbacks are queued up instantly on the respective
        event loop to be called.
    
    _exception : `None` or `BaseException` instance
        The exception set to the future as it's result. Defaults to `None`.
    _loop : ``EventThread``
        The loop to what the created future is bound.
    _result : `tuple` (`set` of ``Future`` instances, `set` of ``Future`` instances)
        The result of the future. Defaults to `None`.
    _state : `str`
        The state of the future.
        
        Can be set as one of the following:
        
        +-----------------+---------------+
        | Respective name | Value         |
        +=================+===============+
        | PENDING         | `'PENDING'`   |
        +-----------------+---------------+
        | CANCELLED       | `'CANCELLED'` |
        +-----------------+---------------+
        | FINISHED        | `'FINISHED'`  |
        +-----------------+---------------+
        | RETRIEVED       | `'RETRIEVED'` |
        +-----------------+---------------+
        
        Note, that states are checked by memory address and not by equality. Also ``RETRIEVED`` is used only if
        `__debug__` is set as `True`.
    
    _callback : ``._wait_callback``
        Callback added to the waited futures.
    """
    __slots__ = ()
    # `__new__` is same as ``WaitTillFirst.__new__``
    # `__repr__` is same as ``Future.__repr__``
    
    class _wait_callback:
        """
        ``WaitTillExc``'s callback put on the future's waited by it.
        
        Attributes
        ----------
        _parent : ``WaitTillExc``
            The parent future.
        """
        __slots__ = ('_parent',)
        
        def __init__(self, parent):
            """
            Creates a new ``WaitTillExc`` callback object with the given parent ``WaitTillExc`` instance.
            
            Parameters
            ----------
            parent : ``WaitTillExc``
                The parent future.
            """
            self._parent = parent
        
        def __call__(self, future):
            """
            The callback, which runs when a waited future is done.
            
            Removes the done future from the parent's `pending` futures and puts it on the `done` ones. If there is no
            more future to wait for, or if the future ended with an exception, marks the parent ``WaitTillExc``
            as finished as well.
            
            Parameters
            ----------
            future : ``Future`` instance
                A done waited future.
            """
            parent = self._parent
            if parent is None:
                return
            
            done, pending = parent._result
            
            pending.remove(future)
            done.add(future)
            
            if (future._exception is None) and pending:
                return
            
            parent._mark_as_finished()
    
    # `futures_done` is same as ``WaitTillFirst.futures_done``
    # `futures_pending` is same as ``WaitTillFirst.futures_pending``
    # `cancel` is same as ``WaitTillFirst.cancel``
    # `cancelled` is same as ``Future.cancelled``
    # `done` is same as ``Future.done``
    # `pending` is same as ``Future.pending``
    # `result` is same as ``Future.result``
    # `exception` is same as ``Future.exception``
    # `add_done_callback` is same as ``Future.add_done_callback``
    # `remove_done_callback` is same as ``Future.remove_done_callback``
    # `set_result` is same as ``WaitTillFirst.set_result``
    # `set_result_if_pending` is same as ``WaitTillFirst.set_result_if_pending``
    # `set_exception` is same as ``WaitTillFirst.set_exception``
    # `set_exception_if_pending` is same as ``WaitTillFirst.set_exception_if_pending``
    # `__iter__` is same as ``Future.__iter__``
    # `__await__` is same as ``Future.__await__``
    # if __debug__:
    #    `__del__` is same as ``Future.__del__``
    #    `__silence__` is same as ``Future.__silence__``
    #    `__silence_cb__` is same as ``Future.__silence_cb__``
    # `cancel_handles` is same as ``Future.cancel_handles``
    # `clear` is same as ``WaitTillFirst.clear``
    # `sleep` is same as ``WaitTillFirst.clear``
    # `sync_wrap` is same as ``Future.cancel_handles``
    # `async_wrap` is same as ``Future.cancel_handles``

class WaitTillAll(WaitTillFirst):
    """
    A future subclass, which waits till all the given tasks or futures become done. When finished, returns the `done`
    and the `pending` futures.
    
    Attributes
    ----------
    _blocking : `bool`
        Whether the future is already being awaited, so it blocks the respective coroutine.
    _callbacks : `list` of `callable`
        The callbacks of the future, which are queued up on the respective event loop to be called, when the future is
        finished. These callback should accept `1` parameter, the future itself.
        
        Note, if the future is already done, then the newly added callbacks are queued up instantly on the respective
        event loop to be called.
    
    _exception : `None` or `BaseException` instance
        The exception set to the future as it's result. Defaults to `None`.
    _loop : ``EventThread``
        The loop to what the created future is bound.
    _result : `tuple` (`set` of ``Future`` instances, `set` of ``Future`` instances)
        The result of the future. Defaults to `None`.
    _state : `str`
        The state of the future.
        
        Can be set as one of the following:
        
        +-----------------+---------------+
        | Respective name | Value         |
        +=================+===============+
        | PENDING         | `'PENDING'`   |
        +-----------------+---------------+
        | CANCELLED       | `'CANCELLED'` |
        +-----------------+---------------+
        | FINISHED        | `'FINISHED'`  |
        +-----------------+---------------+
        | RETRIEVED       | `'RETRIEVED'` |
        +-----------------+---------------+
        
        Note, that states are checked by memory address and not by equality. Also ``RETRIEVED`` is used only if
        `__debug__` is set as `True`.
    
    _callback : ``._wait_callback``
        Callback added to the waited futures.
    """
    __slots__ = ()
    # `__new__` is same as ``WaitTillFirst.__new__``
    # `__repr__` is same as ``Future.__repr__``

    class _wait_callback:
        """
        ``WaitTillAll``'s callback put on the future's waited by it.
        
        Attributes
        ----------
        _parent : ``WaitTillAll``
            The parent future.
        """
        __slots__ = ('_parent',)
        
        def __init__(self, parent):
            """
            Creates a new ``WaitTillAll`` callback object with the given parent ``WaitTillAll`` instance.
            
            Parameters
            ----------
            parent : ``WaitTillAll``
                The parent future.
            """
            self._parent = parent
            
        def __call__(self, future):
            """
            The callback, which runs when a waited future is done.
            
            Removes the done future from the parent's `pending` futures and puts it on the `done` ones. If there is no
            more future to wait for, marks the parent ``WaitTillAll`` as finished as well.
            
            Parameters
            ----------
            future : ``Future`` instance
                A done waited future.
            """
            parent = self._parent
            if parent is None:
                return
            
            done, pending = parent._result
            
            pending.remove(future)
            done.add(future)
            
            if pending:
                return
            
            parent._mark_as_finished()
    
    # `futures_done` is same as ``WaitTillFirst.futures_done``
    # `futures_pending` is same as ``WaitTillFirst.futures_pending``
    # `cancel` is same as ``WaitTillFirst.cancel``
    # `cancelled` is same as ``Future.cancelled``
    # `done` is same as ``Future.done``
    # `pending` is same as ``Future.pending``
    # `result` is same as ``Future.result``
    # `exception` is same as ``Future.exception``
    # `add_done_callback` is same as ``Future.add_done_callback``
    # `remove_done_callback` is same as ``Future.remove_done_callback``
    # `set_result` is same as ``WaitTillFirst.set_result``
    # `set_result_if_pending` is same as ``WaitTillFirst.set_result_if_pending``
    # `set_exception` is same as ``WaitTillFirst.set_exception``
    # `set_exception_if_pending` is same as ``WaitTillFirst.set_exception_if_pending``
    # `__iter__` is same as ``Future.__iter__``
    # `__await__` is same as ``Future.__await__``
    # if __debug__:
    #    `__del__` is same as ``Future.__del__``
    #    `__silence__` is same as ``Future.__silence__``
    #    `__silence_cb__` is same as ``Future.__silence_cb__``
    # `cancel_handles` is same as ``Future.cancel_handles``
    # `clear` is same as ``WaitTillFirst.clear``
    # `sleep` is same as ``WaitTillFirst.clear``
    # `sync_wrap` is same as ``Future.cancel_handles``
    # `async_wrap` is same as ``Future.cancel_handles``

class Lock:
    """
    Implements a mutex lock for hata tasks.

    A hata lock can be used to guarantee exclusive access to a shared resource.
    
    The preferred way of using a hata lock is with `async with` statement:
    
    ```py
    lock = Lock(loop)
    
    async with lock:
        # access resources
    ```
    
    You can also manually acquire and release locks, like:
    
    ```py
    lock = Lock(loop)
    
    await lock.acquire()
    try:
        # access resources
    finally:
        lock.release()
    ```
    
    Attributes
    ----------
    _loop : ``EventThread``
        The event loop to what the lock is bound to.
    _waiters : `deque` of ``Future``
        Futures on which the suspended tasks wait.
    """
    __slots__ = ('_loop', '_waiters', )
    def __new__(cls, loop):
        """
        Creates a new lock instance.
        
        loop : ``EventThread``
            The event loop to what the lock will be bound to.
        """
        self = object.__new__(cls)
        self._loop = loop
        self._waiters = deque()
        return self
    
    async def __aenter__(self):
        """
        Acquires the lock.
        
        This method is a coroutine.
        """
        future = Future(self._loop)
        waiters = self._waiters
        waiters.appendleft(future)
        
        if len(waiters) > 1:
            waiter = waiters[1]
            try:
                await waiter
            except:
                try:
                    waiters.remove(waiter)
                except ValueError:
                    pass
                
                raise
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Releases the lock.
        
        This method is a coroutine.
        """
        future = self._waiters.pop()
        future.set_result_if_pending(None)
        return False
    
    def locked(self):
        """
        Returns whether the lock is entered anywhere.
        
        Returns
        -------
        locked: `bool`
        """
        if self._waiters:
            return True
        return False
    

    def __iter__(self):
        """
        Blocks until all the lock is unlocked everywhere. If lock is used meanwhile anywhere meanwhile the we acquire
        it, will await that as well.
        
        This method is a generator. Should be used with `await` expression.
        """
        waiters = self._waiters
        while waiters:
            yield from waiters[0]
    
    __await__ = __iter__
    
    acquire = __aenter__
    
    def release(self):
        """Releases the lock."""
        future = self._waiters.pop()
        future.set_result_if_pending(None)
    
    def __repr__(self):
        """Returns the lock's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
            ' locked=',
        ]
        
        count = len(self._waiters)
        if count:
            repr_parts.append('True, waiting=')
            repr_parts.append(repr(count))
        else:
            repr_parts.append('False')
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)

class ScarletLock(Lock):
    """
    A hata scarlet lock can be used to guarantee access to a shared resource `n` amount of times.
    
    Should be used with `async with` statement
    
    Attributes
    ----------
    _loop : ``EventThread``
        The event loop to what the lock is bound to.
    _waiters : `deque` of ``Future``
        Futures on which the suspended tasks wait.
    _size : `int`
        The maximal amount of parallel entries to this lock.
    """
    __slots__ = ('_size',)
    def __new__(cls, loop, size=1):
        """
        Creates a new lock instance.
        
        loop : ``EventThread``
            The event loop to what the lock will be bound to.
        size : `int`
            The maximal amount of parallel entries to this lock.
        
        Raises
        ------
        TypeError
            `size` is not given as `int` instance.
        ValueError
            `size` is given as non negative `int`.
        """
        size_type = size.__class__
        if size_type is int:
            pass
        elif issubclass(size_type, int):
            size = int(size)
        else:
            raise TypeError(f'`size` can be given as `int` instance, got {size_type.__name__}.')
        
        if size < 1:
            raise ValueError(f'`size` can be given only as positive, got {size!r}.')
        
        self = object.__new__(cls)
        self._loop = loop
        self._waiters = deque()
        self._size = size
        
        return self
    
    async def __aenter__(self):
        """
        Acquires the lock.
        
        This method is a coroutine.
        """
        future = Future(self._loop)
        waiters = self._waiters
        waiters.appendleft(future)
        
        size = self._size
        if len(waiters) > size:
            waiter = waiters[size]
            try:
                await waiter
            except:
                try:
                    waiters.remove(waiter)
                except ValueError:
                    pass
                
                raise
    
    acquire = __aenter__
    
    def get_size(self):
        """
        Returns the size of the ``ScarletLock``
        
        Returns
        -------
        size : `int`
        """
        return self._size
    
    def get_acquired(self):
        """
        Returns how much times the lock is acquired currently. Caps at the size of the lock.
        
        Returns
        --------
        acquired : `int`
        """
        waiter_count = len(self._waiters)
        size = self._size
        if waiter_count > size:
            waiter_count = size
        
        return waiter_count
    
    def get_waiting(self):
        """
        Returns how tasks are waiting to acquire the lock.
        
        Returns
        --------
        waiting : `int`
        """
        waiter_count = len(self._waiters)
        size = self._size
        if waiter_count > size:
            waiting = waiter_count - size
        else:
            waiting = 0
        
        return waiting
    
    # returns True if the Lock is entered anywhere
    def locked(self):
        """
        Returns whether the lock is entered same or more times than ``.size`` is set to.
        
        Returns
        -------
        locked: `bool`
        """
        if len(self._waiters) >= self._size:
            return True
        return False
    
    def __repr__(self):
        """Returns the scarlet lock's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
            ' size=',
        ]
        
        size = self._size
        repr_parts.append(repr(size))
        
        repr_parts.append(', locked=')
        count = len(self._waiters)
        if count >= size:
            repr_parts.append('True')
        else:
            repr_parts.append('False')
        
        if count:
            repr_parts.append(', waiting=')
            repr_parts.append(repr(count))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)


class Event:
    """
    Asynchronous equivalent to `threading.Event`.
    
    Attributes
    ----------
    _loop : ``EventThread``
        The event loop to what the event is bound.
    _value : `bool`
        The internal flag of the event, which defines, whether it is set.
    _waiters : `list` of ``Future``
        A list of futures waiting on the event to be set.
    """
    __slots__ = ('_loop', '_value', '_waiters',)
    def __new__(cls, loop):
        """
        Creates a new event object bound to the given event loop.
        
        Parameters
        ----------
        loop : ``EventThread``
            The event loop to what the event is bound.
        """
        self = object.__new__(cls)
        self._loop = loop
        self._value = False
        self._waiters = []
        return self
    
    def is_set(self):
        """
        Returns whether the event's internal flag is set as `True`.
        
        Returns
        -------
        is_set: `bool`
        """
        return self._value
    
    def set(self):
        """
        Sets the event's internal flag to `True`, waking up all the tasks waiting for it.
        """
        if self._value:
            return
        
        self._value = True
        waiters = self._waiters
        for waiter in waiters:
            waiter.set_result_if_pending(None)
        
        waiters.clear()
    
    def clear(self):
        """
        Clears the internal flag of the event.
        """
        self._value = False
    
    def __iter__(self):
        """
        Waits util the event is set, or if it is already, returns immediately.
        
        This method is a generator. Should be used with `await` expression.
        """
        if self._value:
            return
        
        future = Future(self._loop)
        self._waiters.append(future)
        yield from future
    
    __await__ = __iter__
    
    wait = to_coroutine(copy_func(__iter__))
    
    def __repr__(self):
        """Returns the event's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
            ' ',
        ]
        
        if self._value:
            state = 'set'
        else:
            state = 'unset'
        repr_parts.append(state)
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)


class enter_executor:
    """
    Async context manager for moving a ``Task``'s section's execution to an executor thread.
    
    Usage:
    ```py
    # Do async code
    async with enter_executor():
        # Do blocking stuff
        # Also async operation are still possible, but not recommended, because they cause my thread switch.
    
    # Do async code
    ```
    
    Attributes
    ----------
    _enter_future : `None` or ``Future``
        The future, what blocks the task's the execution, meanwhile the thread switch is taking place.
    _exit_future : `None` or ``Future``
        The future, what blocks the task's execution, meanwhile the thread is switching back.
    _fut_waiter : `None` or ``Future`` instance
        Blocking future used inside of the task, meanwhile it is in executor.
    _task : `None` or ``Task``
    """
    __slots__ = ('_enter_future', '_exit_future', '_fut_waiter', '_task')
    def __init__(self):
        self._enter_future = None
        self._task = None
        self._exit_future=None
        self._fut_waiter = None
    
    async def __aenter__(self):
        """
        Moves the current tasks's execution to an executor thread.
        
        This method is a coroutine.
        
        Raises
        ------
        RuntimeError
            - Called from outside of an ``EventThread``.
            - Called from outside of a ``Task``.
        """
        thread = current_thread()
        if not isinstance(thread, EventThread):
            raise RuntimeError(f'{self.__class__.__name__} used outside of {EventThread.__name__}, at {thread!r}.')
        
        task = thread.current_task
        if task is None:
            raise RuntimeError(f'{self.__class__.__name__} used outside of a {Task.__name__}.')
        
        self._task = task
        loop = task._loop
        future = Future(loop)
        self._enter_future = future
        loop.call_soon(self._enter_executor)
        await future
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Moves the current task's executor back from an executor thread.
        
        This method is a coroutine.
        """
        await self._exit_future
        self._enter_future = None
        self._task = None
        self._exit_future = None
        self._fut_waiter = None
        return False
    
    def _enter_executor(self):
        """
        Moves the task's execution to an executor thread and wakes it up.
        """
        callbacks = self._enter_future._callbacks
        callbacks.clear()
        
        task = self._task
        task.add_done_callback(self._cancel_callback)
        
        task._loop.run_in_executor(self._executor_task)
    
    def _cancel_callback(self, future):
        """
        Callback added to the wrapped task. If the wrapped task is cancelled, then the section running inside of the
        executor will be cancelled as well, whenever it gives back the context with an `await`.
        """
        if future._state is not CANCELLED:
            return
        
        fut_waiter = self._fut_waiter
        if fut_waiter is None:
            return
        
        fut_waiter.cancel()
    
    def _executor_task(self):
        """
        Wraps the tasks's section's running inside of an executor, still allowing it to use `await`-s.
        """
        task = self._task
        # relink future task
        loop = task._loop
        end_future = Future(loop)
        task._fut_waiter = end_future
        self._exit_future = end_future
        
        # Set result to the enter task, so it can be retrieved.
        self._enter_future.set_result(None)
        
        exception = None
        coro = task._coro
        
        # If some1 await at the block, we will sync_wrap it. If the exit future
        # is awaited, then we quit.
        local_fut_waiter = None
        
        try:
            while True:
                if task._must_cancel:
                    exception = task._must_exception(exception)
                    
                if (local_fut_waiter is not None):
                    if local_fut_waiter is end_future:
                        end_future.set_result(None)
                        loop.call_soon_thread_safe(task._step, exception)
                        break
                    
                    try:
                        self._fut_waiter = local_fut_waiter
                        if type(exception) is CancelledError:
                            local_fut_waiter.cancel()
                        local_fut_waiter.sync_wrap().wait()
                    
                    except CancelledError:
                        break
                    except BaseException as err:
                        exception = err
                    finally:
                        local_fut_waiter = None
                        self._fut_waiter = None
                
                if task._state is not PENDING:
                    # there is no reason to raise
                    break
                
                # call either coro.throw(err) or coro.send(None).
                try:
                    if exception is None:
                        result = coro.send(None)
                    else:
                        result = coro.throw(exception)
                
                except StopIteration as exception:
                    if task._must_cancel:
                        # the task is cancelled meanwhile
                        task._must_cancel = False
                        Future.set_exception(task, CancelledError())
                    else:
                        Future.set_result(task, exception.value)
                    
                    loop.wake_up()
                    break
                    
                except CancelledError:
                    Future.cancel(task)
                    loop.wake_up()
                    break
                
                except BaseException as exception:
                    Future.set_exception(task, exception)
                    loop.wake_up()
                    break
                
                else:
                    try:
                        blocking = result._blocking
                    except AttributeError:
                        if result is None:
                            # bare yield relinquishes control for one event loop iteration.
                            continue
                        
                        elif isinstance(result, GeneratorType):
                            #Yielding a generator is just wrong.
                            exception = RuntimeError(f'`yield` was used instead of `yield from` in '
                                f'{self.__class__.__name__} {self!r} with `{result!r}`')
                            continue
                            
                        else:
                            # yielding something else is an error.
                            exception = RuntimeError(f'{self.__class__.__name__} got bad yield: `{result!r}`')
                            continue
                    else:
                        if blocking:
                            if loop is not result._loop:
                                exception = RuntimeError(f'{self.__class__.__name__} {self!r} got a Future {result!r} '
                                    f'attached to a different loop')
                                continue
                                
                            elif result is self:
                                exception = RuntimeError(f'{self.__class__.__name__} cannot await on itself: {self!r}')
                                continue
                            
                            else:
                                result._blocking = False
                                local_fut_waiter = result
                                if task._must_cancel:
                                    if local_fut_waiter.cancel():
                                        task._must_cancel = False
                                
                                continue
                        else:
                            exception = RuntimeError(f'`yield` was used instead of `yield from` in task {self!r} with '
                                f'{result!r}')
                            continue
        finally:
            task.remove_done_callback(self._cancel_callback)
            self = None
            task = None

class ScarletExecutorCB:
    """
    ``ScarletExecutor`` callback's added to futures or tasks waited by it.
    
    Attributes
    ----------
    _parent : ``ScarletExecutor``
        The parent Scarlet executor.
    """
    __slots__ = ('_parent',)
    
    def __init__(self, parent):
        """
        Creates a new scarlet executor with the given parameters.
        
        Parameters
        ----------
        parent : ``ScarletExecutor``
            The parent Scarlet executor.
        """
        self._parent = parent
    
    def __call__(self, future):
        """
        Called as a callback when a waited future or task is finished.
        
        Removes the given `future`'s from the parent's active ones. If the parent Scarlet executor is overloaded with
        tasks, wakes it up.
        
        If the `future` is finished with an exception then propagates it to it's parent to re-raise.
        
        Parameters
        ----------
        future : ``Future`` instance
            A finished future or task.
        """
        parent = self._parent
        if parent is None:
            return
        
        active = parent._active
        
        active.discard(future)
        
        try:
            future.result()
        except CancelledError:
            pass
        except BaseException as err:
            exception = parent._exception
            if exception is None:
                parent._exception = err
        
        parent._waiter.set_result_if_pending(None)
    
class ScarletExecutor:
    """
    Scarlet executor allows the user to limit parallelly running task amount to a set one. Not that, only those tasks
    count, which are added to the executor with it's ``.add`` method.
    
    If an exception (except ``CancelledError``) occurs in any of the added tasks, then that exception is propagated
    and every other task is cancelled.
    
    Should be used, like:
    
    ```py
    from time import perf_counter
    from hata import ScarletExecutor, sleep
    
    async def showcase():
        start = perf_counter()
        
        async with ScarletExecutor(2) as scarlet:
            for sleep_time in range(10):
                await scarlet.add(sleep(sleep_time))
        
        end = perf_counter()
        print(end-start)
    ```
    
    Running showcase will take at least `25` seconds, because ``ScarletExecutor`` will allow only `2` sleeps to run
    at the same time, like:
    
    +---------------+-------------------------------+-----------------------+
    | Time passed   | Slot 1                        | Slot 2                |
    +===============+===============================+=======================+
    | 0 (s)         | N/A -> sleep(0) -> sleep(2)   | N/A -> sleep(1)       |
    +---------------+-------------------------------+-----------------------+
    | 1 (s)         | sleep(2)                      | sleep(1) -> sleep(3)  |
    +---------------+-------------------------------+-----------------------+
    | 2 (s)         | sleep(2) -> sleep(4)          | sleep(3)              |
    +---------------+-------------------------------+-----------------------+
    | 3 (s)         | sleep(4)                      | sleep(3)              |
    +---------------+-------------------------------+-----------------------+
    | 4 (s)         | sleep(4)                      | sleep(3) -> sleep(5)  |
    +---------------+-------------------------------+-----------------------+
    | 5 (s)         | sleep(4)                      | sleep(5)              |
    +---------------+-------------------------------+-----------------------+
    | 6 (s)         | sleep(4) -> sleep(6)          | sleep(5)              |
    +---------------+-------------------------------+-----------------------+
    | 7 (s)         | sleep(6)                      | sleep(5)              |
    +---------------+-------------------------------+-----------------------+
    | 8 (s)         | sleep(6)                      | sleep(5)              |
    +---------------+-------------------------------+-----------------------+
    | 9 (s)         | sleep(6)                      | sleep(5) -> sleep(7)  |
    +---------------+-------------------------------+-----------------------+
    | 10 (s)        | sleep(6)                      | sleep(7)              |
    +---------------+-------------------------------+-----------------------+
    | 11 (s)        | sleep(6)                      | sleep(7)              |
    +---------------+-------------------------------+-----------------------+
    | 12 (s)        | sleep(6) -> sleep(8)          | sleep(7)              |
    +---------------+-------------------------------+-----------------------+
    | 13 (s)        | sleep(8)                      | sleep(7)              |
    +---------------+-------------------------------+-----------------------+
    | 14 (s)        | sleep(8)                      | sleep(7)              |
    +---------------+-------------------------------+-----------------------+
    | 15 (s)        | sleep(8)                      | sleep(7)              |
    +---------------+-------------------------------+-----------------------+
    | 16 (s)        | sleep(8)                      | sleep(7) -> sleep(9)  |
    +---------------+-------------------------------+-----------------------+
    | 17 (s)        | sleep(8)                      | sleep(9)              |
    +---------------+-------------------------------+-----------------------+
    | 18 (s)        | sleep(8)                      | sleep(9)              |
    +---------------+-------------------------------+-----------------------+
    | 19 (s)        | sleep(8)                      | sleep(9)              |
    +---------------+-------------------------------+-----------------------+
    | 20 (s)        | sleep(8) -> N/A               | sleep(9)              |
    +---------------+-------------------------------+-----------------------+
    | 20 (s)        | N/A                           | sleep(9)              |
    +---------------+-------------------------------+-----------------------+
    | 21 (s)        | N/A                           | sleep(9)              |
    +---------------+-------------------------------+-----------------------+
    | 22 (s)        | N/A                           | sleep(9)              |
    +---------------+-------------------------------+-----------------------+
    | 23 (s)        | N/A                           | sleep(9)              |
    +---------------+-------------------------------+-----------------------+
    | 24 (s)        | N/A                           | sleep(9)              |
    +---------------+-------------------------------+-----------------------+
    | 25 (s)        | N/A                           | sleep(9) -> N/A       |
    +---------------+-------------------------------+-----------------------+
    
    By increasing parallelism to `3`, the showcase will take only `18` seconds to finish:
    
    ```py
    async def showcase():
        start = perf_counter()
        
        async with ScarletExecutor(3) as scarlet:
            for sleep_time in range(10):
                await scarlet.add(sleep(sleep_time))
        
        end = perf_counter()
        print(end-start)
    ```
    
    +---------------+-------------------------------+-----------------------+-----------------------+
    | Time passed   | Slot 1                        | Slot 2                | Slot 3                |
    +===============+===============================+=======================+=======================+
    | 0 (s)         | N/A -> sleep(0) -> sleep(3)   | N/A -> sleep(1)       | N/A -> sleep(2)       |
    +---------------+-------------------------------+-----------------------+-----------------------+
    | 1 (s)         | sleep(3)                      | sleep(1) -> sleep(4)  | sleep(2)              |
    +---------------+-------------------------------+-----------------------+-----------------------+
    | 2 (s)         | sleep(3)                      | sleep(4)              | sleep(2) -> sleep(5)  |
    +---------------+-------------------------------+-----------------------+-----------------------+
    | 3 (s)         | sleep(3) -> sleep(6)          | sleep(4)              | sleep(5)              |
    +---------------+-------------------------------+-----------------------+-----------------------+
    | 4 (s)         | sleep(6)                      | sleep(4)              | sleep(5)              |
    +---------------+-------------------------------+-----------------------+-----------------------+
    | 5 (s)         | sleep(6)                      | sleep(4) -> sleep(7)  | sleep(5)              |
    +---------------+-------------------------------+-----------------------+-----------------------+
    | 6 (s)         | sleep(6)                      | sleep(7)              | sleep(5)              |
    +---------------+-------------------------------+-----------------------+-----------------------+
    | 7 (s)         | sleep(6)                      | sleep(7)              | sleep(5) -> sleep(8)  |
    +---------------+-------------------------------+-----------------------+-----------------------+
    | 8 (s)         | sleep(6)                      | sleep(7)              | sleep(8)              |
    +---------------+-------------------------------+-----------------------+-----------------------+
    | 9 (s)         | sleep(6) -> sleep(9)          | sleep(7)              | sleep(8)              |
    +---------------+-------------------------------+-----------------------+-----------------------+
    | 10 (s)        | sleep(9)                      | sleep(7)              | sleep(8)              |
    +---------------+-------------------------------+-----------------------+-----------------------+
    | 11 (s)        | sleep(9)                      | sleep(7)              | sleep(8)              |
    +---------------+-------------------------------+-----------------------+-----------------------+
    | 12 (s)        | sleep(9)                      | sleep(7) -> N/A       | sleep(8)              |
    +---------------+-------------------------------+-----------------------+-----------------------+
    | 13 (s)        | sleep(9)                      | N/A                   | sleep(8)              |
    +---------------+-------------------------------+-----------------------+-----------------------+
    | 14 (s)        | sleep(9)                      | N/A                   | sleep(8)              |
    +---------------+-------------------------------+-----------------------+-----------------------+
    | 15 (s)        | sleep(9)                      | N/A                   | sleep(8) -> N/A       |
    +---------------+-------------------------------+-----------------------+-----------------------+
    | 16 (s)        | sleep(9)                      | N/A                   | N/A                   |
    +---------------+-------------------------------+-----------------------+-----------------------+
    | 17 (s)        | sleep(9)                      | N/A                   | N/A                   |
    +---------------+-------------------------------+-----------------------+-----------------------+
    | 18 (s)        | sleep(9) -> N/A               | N/A                   | N/A                   |
    +---------------+-------------------------------+-----------------------+-----------------------+
    
    Attributes
    ----------
    _active : `set` of ``Future`` instances
        The already running tasks.
    _callback : `None` or ``ScarletExecutorCB``
        Callback set to the parallelly limited tasks.
    _exception : `None` or `BaseException`
        Any exception raised by an added task. ``CancelledError``-s are ignored.
    _limit : `int`
        The maximal amount of parallelism allowed by the Scarlet executor.
    _loop : `None` or ``EventThread``
        The event loop to what the ScarletExecutor is bound to.
    _waiter : `None` or ``Future``
        A future which is used to block the main task's execution if the parallelly running tasks's amount is greater or
        equal to the ``._limit``.
    """
    __slots__ = ('_active', '_callback', '_exception', '_limit', '_loop', '_waiter', )
    def __new__(cls, limit=10):
        """
        Creates a new Scarlet executor instance.
        
        Parameters
        ----------
        limit : `int`, Optional
            The maximal amount of parallelism allowed by the Scarlet executor. Defaults to `10`.
        
        Raises
        ------
        TypeError
            `size` is not given as `int` instance.
        ValueError
            `size` is given as non negative `int`.
        """
        limit_type = limit.__class__
        if limit_type is int:
            pass
        elif issubclass(limit_type, int):
            limit = int(limit)
        else:
            raise TypeError(f'`limit` can be given as `int` instance, got {limit_type.__name__}.')
        
        if limit < 1:
            raise ValueError(f'`limit` can be given only as positive, got {limit!r}.')
        
        self = object.__new__(cls)
        self._limit = limit
        
        self._active = set()
        self._loop = None
        self._callback = None
        self._waiter = None
        self._exception = None
        
        return self
    
    async def __aenter__(self):
        """
        Enters the scarlet executor.
        
        This method is a coroutine.
        
        Raises
        ------
        RuntimeError
            Called from outside of an ``EventThread``.
        """
        loop = current_thread()
        if not isinstance(loop, EventThread):
            raise RuntimeError(f'`{self.__class__.__name__}` used at non {EventThread.__name__}: {loop!r}.')
        
        self._loop = loop
        self._waiter = Future(loop)
        self._callback = ScarletExecutorCB(self)
        
        return self
    
    async def add(self, future):
        """
        Adds a task to the Scarlet executor to execute parallelly with the other added ones. Blocks execution, if the
        amount of added tasks is greater or equal than the set limit.
        
        This method is a coroutine.
        
        Raises
        ------
        RuntimeError
            ``.add`` called when the Scarlet executor is not entered with `async with.`
        CancelledError
            If any of the tasks raised an error, ``CancelledError`` is propagated to quit from the Scarlet executor.
            This exception is catched by ``.__exit__`` and the original exception is reraised.
        """
        callback = self._callback
        if callback is None:
            raise RuntimeError(f'Calling `{self.__class__.__name__}.add` when {self!r} is not entered.')
        
        future = self._loop.ensure_future(future)
        future.add_done_callback(callback)
        
        active = self._active
        active.add(future)
        
        waiter = self._waiter
        
        if waiter.done():
            if self._exception is None:
                waiter.clear()
            else:
                raise CancelledError
        
        limit = self._limit
        while len(active) >= limit:
            await waiter
            if (self._exception is not None):
                raise CancelledError
            
            waiter.clear()
            
            break
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Leaves from the scarlet execution, blocking till all the added tasks are finished.
        
        If any of the added tasks raised an exception, what is not ``CancelledError``, then cancels all of them and
        propagates the given exception.
        
        This method is a coroutine.
        """
        if exc_type is None:
            active = self._active
            waiter = self._waiter
            while active:
                await waiter
                exception = self._exception
                if exception is None:
                    waiter.clear()
                    continue
                
                self._callback._parent = None
                self._callback = None
                
                self._waiter = None
                self._loop = None
                self._exception = None
                
                for future in active:
                    future.cancel()
                
                active.clear()
                
                raise exception
            
            self._callback._parent = None
            self._callback = None
            
            self._waiter = None
            self._loop = None
            self._exception = None
            return False
        
        active = self._active
        for future in active:
            future.cancel()
        
        active.clear()
        
        exception = self._exception
        
        self._callback._parent = None
        self._callback = None
        
        self._waiter = None
        self._loop = None
        self._exception = None
        
        if exception is None:
            if exc_type is CancelledError:
                return True
            else:
                return False
        else:
            raise exception
    
    def __repr__(self):
        """Returns the scarlet executor's representation."""
        result = [
            '<',
            self.__class__.__name__,
            ' limit=',
            repr(self._limit),
                ]
        
        if (self._loop is None):
            result.append(', closed')
        else:
            result.append(', active=')
            result.append(repr(len(self._active)))
        
        result.append('>')
        
        return ''.join(result)

class WaitContinuously(WaitTillFirst):
    """
    A future subclass, which allows waiting for future or task results continuously, yielding `1` result, when awaited.
    
    Attributes
    ----------
    _blocking : `bool`
        Whether the future is already being awaited, so it blocks the respective coroutine.
    _callbacks : `list` of `callable`
        The callbacks of the future, which are queued up on the respective event loop to be called, when the future is
        finished. These callback should accept `1` parameter, the future itself.
        
        Note, if the future is already done, then the newly added callbacks are queued up instantly on the respective
        event loop to be called.
    
    _exception : `None` or `BaseException` instance
        The exception set to the future as it's result. Defaults to `None`.
    _loop : ``EventThread``
        The loop to what the created future is bound.
    _result : `tuple` (`set` of ``Future`` instances, `set` of ``Future`` instances)
        The result of the future. Defaults to `None`.
    _state : `str`
        The state of the future.
        
        Can be set as one of the following:
        
        +-----------------+---------------+
        | Respective name | Value         |
        +=================+===============+
        | PENDING         | `'PENDING'`   |
        +-----------------+---------------+
        | CANCELLED       | `'CANCELLED'` |
        +-----------------+---------------+
        | FINISHED        | `'FINISHED'`  |
        +-----------------+---------------+
        | RETRIEVED       | `'RETRIEVED'` |
        +-----------------+---------------+
        
        Note, that states are checked by memory address and not by equality. Also ``RETRIEVED`` is used only if
        `__debug__` is set as `True`.
    
    _callback : ``._wait_callback``
        Callback added to the waited futures.
    _last_done : `None` or ``Future`` instance
        The last done future or task of the ``WaitContinuously`` instance.
    """
    __slots__ = ('_last_done')
    
    def __new__(cls, futures, loop):
        """
        Creates a new ``WaitContinuously`` from the given `futures` bound to the given `loop`.
        
        Parameters
        ----------
        futures : `None` or `iterable` of ``Future`` instances
            The futures from which the ``WaitContinuously`` instance will yield the done ones. Can be given as `None`.
        loop : ``EventThread``
            The loop to what the created future will be bound to.
        """
        if (futures is None):
            pending = set()
        else:
            pending = set(futures)
        
        done = set()
        
        self = object.__new__(cls)
        self._loop = loop
        
        callback = cls._wait_callback(self)
        self._callback = callback
        
        self._result = (done, pending)
        self._exception = None
        
        self._callbacks = []
        self._blocking = False
        
        self._last_done = None
        
        if pending:
            try:
                for future in pending:
                    future.add_done_callback(callback)
            finally:
                self._state = PENDING
        else:
            self._state = FINISHED
        
        return self
    
    # `__repr__` is same as ``Future.__repr__``
    
    class _wait_callback:
        """
        ``WaitContinuously``'s callback put on the future's waited by it.
        
        Attributes
        ----------
        _parent : ``WaitContinuously``
            The parent future.
        """
        __slots__ = ('_parent',)
        
        def __init__(self, parent):
            """
            Creates a new ``WaitContinuously`` callback object with the given parent ``WaitContinuously`` instance.
            
            Parameters
            ----------
            parent : ``WaitContinuously``
                The parent future.
            """
            self._parent = parent
        
        def __call__(self, future):
            """
            The callback, which runs when a waited future is done.
            
            Removes the done future from the parent's `pending` futures and puts it on the `done` ones. Also marks the
            parent ``WaitContinuously`` instance as finished if it is pending.
            
            Parameters
            ----------
            future : ``Future`` instance
                A done waited future.
            """
            parent = self._parent
            if parent is None:
                return
            
            done, pending = parent._result
            
            pending.remove(future)
            done.add(future)
            
            if parent._state is PENDING:
                parent._state = FINISHED
                parent._last_done = future
                parent._loop._schedule_callbacks(parent)
    
    def add(self, future):
        """
        Adds a new future to the ``WaitContinuously`` to wait for.
        
        Parameters
        ----------
        future : ``Future`` instance
            A task or future to the ``WaitContinuously`` to wait for.
        
        Raises
        ------
        RuntimeError
            If the ``WaitContinuously`` instance has exception set, or if it is cancelled already. At this case the
            added `future` is cancelled instantly.
        """
        state = self._state
        if state is PENDING:
            if future.done():
                self._result[0].add(future)
                self._state = FINISHED
                self._loop._schedule_callbacks(self)
                self._last_done = future
                return
            
            pending = self._result[1]
            pending_count = len(pending)
            pending.add(future)
            if pending_count != pending:
                future.add_done_callback(self._callback)
            
            return
        
        if state is FINISHED:
            exception = self._exception
            if (exception is not None):
                future.cancel()
                raise RuntimeError(f'`{self.__class__.__name__}.add` called, when {self.__class__.__name__} is already '
                    f'finished with an exception : {exception!r}') from exception
            
            if future.done():
                self._result[0].add(future)
                return
            
            pending = self._result[1]
            pending_count = len(pending)
            pending.add(future)
            if pending_count != len(pending):
                future.add_done_callback(self._callback)
            
            self._state = PENDING
            return
        
        if __debug__:
            if state is RETRIEVED:
                exception = self._exception
                if (exception is not None):
                    future.cancel()
                    raise RuntimeError(f'`{self.__class__.__name__}.add` called, when {self.__class__.__name__} is '
                        f'already finished with an exception : {exception!r}') from exception
                
                if future.done():
                    self._result[0].append(future)
                    self._state = FINISHED
                    return
                
                pending = self._result[1]
                pending_count = len(pending)
                pending.add(future)
                if pending_count != len(pending):
                    future.add_done_callback(self._callback)
                
                self._state = PENDING
                return
        
        future.cancel()
        raise RuntimeError(f'`{self.__class__.__name__}.add` called, when {self.__class__.__name__} is already '
               f'cancelled.')
    
    def _mark_as_finished(self):
        """
        Marks self as finished, ensures it's callbacks, and cancels all the added futures.
        """
        self._state = FINISHED
        self._loop._schedule_callbacks(self)
        
        self._callback._parent = None
        
        done, pending = self._result
        # silence them
        if __debug__:
            for future in done:
                future.cancel()
        
        callback = self._callback
        callback._parent = None
        
        while pending:
            future = pending.pop()
            future.remove_done_callback(callback)
            future.cancel()
            done.add(future)
    
    # `futures_done` same as ``WaitTillFirst.futures_done``
    # `futures_pending` same as ``WaitTillFirst.futures_pending``
    
    def cancel(self):
        """
        Cancels the ``WaitContinuously`` instance.
        
        By calling it, also cancels all the waited futures as well.
        
        Returns
        -------
        cancelled : `int` (`0`, `1`)
            If the future is already done, returns `0`, if it got cancelled, returns `1`-
        
        Notes
        -----
        If `__debug__` is set as `True`, then `.cancel()` also marks the future and all the waited-done futures as well
        as retrieved, causing them to not render non-retrieved exceptions.
        """
        state = self._state
        if state is CANCELLED:
            return 0
        
        if (self._exception is not None):
            if __debug__:
                if state is FINISHED:
                    self._state = RETRIEVED
                    return 0
                
                if state is RETRIEVED:
                    return 0
            
            else:
                if state is FINISHED:
                    return 0
        
        done, pending = self._result
        # silence them
        if __debug__:
            for future in done:
                future.cancel()
        
        callback = self._callback
        callback._parent = None
        
        while pending:
            future = pending.pop()
            future.remove_done_callback(callback)
            future.cancel()
            done.add(future)
        
        if state is PENDING:
            self._loop._schedule_callbacks(self)
            self._state = CANCELLED
        else:
            if __debug__:
                if state is FINISHED:
                    self._state = RETRIEVED
            
        return 1
    
    # `cancelled` is same as ``Future.cancelled``
    # `done` is same as ``Future.done``
    # `pending` is same as ``Future.pending``
    
    def result(self):
        """
        Returns the last done future.
        
        Returns
        -------
        last_done : `None` or ``Future`` instance.
            The last future, what finished. Defaults to `None`.
        
        Raises
        ------
        CancelledError
            The future is cancelled.
        InvalidStateError
            The futures is not done yet.
        TypeError
            The future has non `BaseException` instance set as exception.
        BaseException
            The future's set exception.
        """
        state = self._state
        
        if state is FINISHED:
            if __debug__:
                self._state = RETRIEVED
            
            exception = self._exception
            if (exception is not None):
                raise exception
            
            return self._last_done
        
        if __debug__:
            if state is RETRIEVED:
                exception = self._exception
                if (exception is not None):
                    raise exception
                
                return self._last_done
        
        if state is CANCELLED:
            raise CancelledError
        
        # still pending
        raise InvalidStateError(self, 'result')
    
    def reset(self):
        """
        Resets the future if applicable enabling it to yield the next done future.
        
        Returns
        -------
        reset : `int` (`0`, `1`, `2`, `3`)
            - Returns `0` if the future is unable to reset. For example, there is an exception set to it, or it is
                cancelled.
            - If the future has nothing more to await on, returns `1`.
            - If there are futures to wait for, and there is no other done yet, returns `2`.
            - If there are futures to wait for, and there is at least one already other done, returns `3`.
        """
        state = self._state
        if state is FINISHED:
            if (self._exception is not None):
                return 0
            
            done, pending = self._result
            if done:
                last_done = self._last_done
                if (last_done is not None):
                    try:
                        done.remove(last_done)
                    except KeyError:
                        pass
            
            if done:
                self._last_done = done.pop()
                return 3
            
            if pending:
                self._state = PENDING
                return 2
            
            return 1
        
        if __debug__:
            if state is RETRIEVED:
                if (self._exception is not None):
                    return 0
                
                done, pending = self._result
                last_done = self._last_done
                if (last_done is not None):
                    try:
                        done.remove(last_done)
                    except KeyError:
                        pass
                
                if done:
                    self._state = FINISHED
                    self._last_done = done.pop()
                    return 3
                
                if pending:
                    self._state = PENDING
                    return 2
                
                return 1
        
        if state is PENDING:
            if self._result[1]:
                return 2
            
            return 1
        
        # cancelled
        return 0
    
    # `exception` is same as ``Future.exception``
    # `add_done_callback` is same as ``Future.add_done_callback``
    # `remove_done_callback` is same as ``Future.remove_done_callback``
    # `set_result` is same as ``WaitTillFirst.set_result``
    # `set_result_if_pending` is same as ``WaitTillFirst.set_result_if_pending``
    
    def set_exception(self, exception):
        """
        Marks the future as done and set's it's exception. If the exception is `TimeoutError`, then will not cancel it,
        but it will yield it's next result as `None` instead.
        
        Parameters
        ----------
        exception : `BaseException`
            The exception to set as the future's exception.
        
        Raises
        ------
        InvalidStateError
            If the future is already done by being cancelled, or it has exception set.
        TypeError
            If `StopIteration` is given as `exception`.
        """
        state = self._state
        if (state is CANCELLED) or ((state is FINISHED or state is RETRIEVED) and self._exception is not None):
            raise InvalidStateError(self, 'set_exception')
        
        if isinstance(exception, type):
            exception = exception()
        
        if type(exception) is StopIteration:
             raise TypeError(f'{exception} cannot be raised to a {self.__class__.__name__}: {self!r}')
        
        if type(exception) is TimeoutError:
            self._state = FINISHED
            self._last_done = None
            self._loop._schedule_callbacks(self)
        else:
            self._mark_as_finished()
            self._exception = exception
    
    def set_exception_if_pending(self, exception):
        """
        Marks the future as done and set's it's exception. If the exception is `TimeoutError`, then will not cancel it,
        but it will yield it's next result as `None` instead. Not like ``.set_exception``, this method will not raise
        ``InvalidStateError`` if the future is already done.
        
        Parameters
        ----------
        exception : `BaseException`
            The exception to set as the future's exception.
        
        Returns
        ------
        set_result : `int` (`0`, `1`, `2`)
            If the future is already done, returns `0`. If `exception` is given as `TimeoutError`, returns `2`, else
            `1`.
        
        Raises
        ------
        TypeError
            If `StopIteration` is given as `exception`.
        """
        state = self._state
        if (state is CANCELLED) or ((state is FINISHED or state is RETRIEVED) and self._exception is not None):
            return 0
        
        if isinstance(exception, type):
            exception = exception()
        
        if type(exception) is StopIteration:
             raise TypeError(f'{exception} cannot be raised to a {self.__class__.__name__}: {self!r}')
        
        if type(exception) is TimeoutError:
            self._state = FINISHED
            self._last_done = None
            self._loop._schedule_callbacks(self)
            return 2
        
        self._mark_as_finished()
        self._exception = exception
        return 1
    
    # `__iter__` is same as ``Future.__iter__``
    # `__await__` is same as ``Future.__await__``
    # if __debug__:
    #    `__del__` is same as ``Future.__del__``
    #    `__silence__` is same as ``Future.__silence__``
    #    `__silence_cb__` is same as ``Future.__silence_cb__``
    # `cancel_handles` is same as ``Future.cancel_handles``
    # `clear` same as ``WaitTilLFirst.clear``
    # `sync_wrap` is same as ``Future.sync_wrap``
    # `async_wrap` is same as ``Future.async_wrap``
