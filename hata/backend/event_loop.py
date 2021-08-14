__all__ = ('Cycler', 'EventThread', 'LOOP_TIME', 'LOOP_TIME_RESOLUTION', 'ThreadSyncerCTX', )

import sys, errno, weakref, subprocess, os
import socket as module_socket
import time as module_time
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ
from threading import current_thread, Thread, Event
from heapq import heappop, heappush
from collections import deque
from ssl import SSLContext, create_default_context
from stat import S_ISSOCK

from .export import export
from .utils import alchemy_incendiary, WeakReferer, weakmethod, MethodType, WeakCallable, doc_property, DOCS_ENABLED, \
    set_docs, IS_UNIX
from .futures import Future, Task, Gatherer, render_exc_to_list, is_coroutine, FutureAsyncWrapper, WaitTillFirst, \
    CancelledError, skip_ready_cycle
from .transprotos import SSLProtocol, _SelectorSocketTransport, _SelectorDatagramTransport
from .executor import Executor
from .analyzer import CallableAnalyzer
from .protocol import ProtocolBase

if IS_UNIX:
    from .subprocess import UnixReadPipeTransport, UnixWritePipeTransport, AsyncProcess

import threading
from .futures import _ignore_frame
_ignore_frame(__spec__.origin, '_run', 'self.func(*self.args)', )
_ignore_frame(__spec__.origin, 'run', 'handle._run()', )
_ignore_frame(threading.__spec__.origin, '_bootstrap', 'self._bootstrap_inner()', )
_ignore_frame(threading.__spec__.origin, '_bootstrap_inner', 'self.run()', )
del threading, _ignore_frame


LOOP_TIME = module_time.monotonic
LOOP_TIME_RESOLUTION = module_time.get_clock_info('monotonic').resolution
del module_time

class Handle:
    """
    Object returned by a callback registration method:
    - ``EventThread.call_soon``
    - ``EventThread.call_soon_thread_safe``.
    
    Attributes
    ----------
    func : `callable`
        The wrapped function.
    args : `tuple` of `Any`
        Parameters to call ``.func`` with.
    cancelled : `bool`
        Whether the handle is cancelled.
    """
    __slots__ = ('func', 'args', 'cancelled',)
    
    def __init__(self, func, args):
        """
        Creates a new ``Handle`` with the given parameters.
        
        Parameters
        ----------
        func : `callable`
            The function. to wrap.
        args : `tuple` of `Any`
            Parameters to call `func` with.
        """
        self.func = func
        self.args = args
        self.cancelled = False
    
    def __repr__(self):
        """Returns the handle's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
        ]
        
        if self.cancelled:
            repr_parts.append(' cancelled')
        else:
            repr_parts.append(' func=')
            repr_parts.append(repr(self.func))
            repr_parts.append('(')
            
            args = self.args
            limit = len(args)
            if limit:
                index = 0
                while True:
                    arg = args[index]
                    repr_parts.append(repr(arg))
                    
                    index += 1
                    if index == limit:
                        break
                    
                    repr_parts.append(', ')
                    continue
            
            repr_parts.append(')')
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    def cancel(self):
        """Cancels the handle if not yet cancelled."""
        if not self.cancelled:
            self.cancelled = True
            self.func = None
            self.args = None
    
    def _run(self):
        """
        Calls the handle's function with it's parameters. If exception occurs meanwhile, renders it.
        
        Notes
        -----
        This method should be called only inside of an ``EventThread``.
        """
        try:
            self.func(*self.args)
        except BaseException as err:
            current_thread().render_exc_async(err, [
                'Exception occurred at ',
                self.__class__.__name__,
                '._run\nAt running ',
                repr(self.func),
                '\n',
            ])
        
        self = None  # Needed to break cycles when an exception occurs.

class TimerHandle(Handle):
    """
    Object returned by a callback registration method:
    - ``EventThread.call_later``
    - ``EventThread.call_at``.
    
    Attributes
    ----------
    func : `callable`
        The wrapped function.
    args : `tuple` of `Any`
        Parameters to call ``.func`` with.
    cancelled : `bool`
        Whether the handle is cancelled.
    when : `float`
        The respective loop's time, when the handle should be called.
    """
    __slots__ = ('when',)
    
    def __init__(self, when, func, args):
        """
        Creates a new ``TimerHandle`` with the given parameters.
        
        Parameters
        ----------
        when : `float`
            The respective loop's time, when the handle should be called.
        func : `callable`
            The function. to wrap.
        args : `tuple` of `Any`
            Parameters to call `func` with.
        """
        self.func = func
        self.args = args
        self.cancelled = False
        self.when = when
    
    def __repr__(self):
        """Returns the timer handle's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
        ]
        
        if self.cancelled:
            repr_parts.append(' cancelled')
        else:
            repr_parts.append(' func=')
            repr_parts.append(repr(self.func))
            repr_parts.append('(')
            
            args = self.args
            limit = len(args)
            if limit:
                index = 0
                while True:
                    arg = args[index]
                    repr_parts.append(repr(arg))
                    
                    index += 1
                    if index == limit:
                        break
                    
                    repr_parts.append(', ')
                    continue
            
            repr_parts.append(')')
            repr_parts.append(', when=')
            repr_parts.append(repr(self.when))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    def __hash__(self):
        """Returns the hash of the time, when the handle will be called."""
        return hash(self.when)
    
    def __gt__(self, other):
        """Returns whether this timer handle should be called later than the other."""
        return self.when > other.when
    
    def __ge__(self, other):
        """Returns whether this timer handle should be called later than the other, or whether the two are equal."""
        if self.when > other.when:
            return True
        
        return self.__eq__(other)
    
    def __eq__(self, other):
        """Returns whether the two timer handles are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return (self.when       == other.when       and
                self.func       == other.func       and
                self.args       == other.args       and
                self.cancelled  == other.cancelled      )
    
    def __ne__(self, other):
        """Returns whether the two timer handles are not equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return (self.when       != other.when       or
                self.func       != other.func       or
                self.args       != other.args       or
                self.cancelled  != other.cancelled      )
    
    def __le__(self, other):
        """Returns whether this timer handle should be called earlier than the other, or whether the two are equal."""
        if self.when < other.when:
            return True
        
        return self.__eq__(other)
    
    def __lt__(self, other):
        """Returns whether this timer handle should be called earlier than the other."""
        return self.when < other.when

class TimerWeakHandle(TimerHandle):
    """
    Object returned by a callback registration method:
    - ``EventThread.call_later_weak``
    - ``EventThread.call_at_weak``.
    
    Used when the respective `func`, might be garbage collected before it callback would run.
    
    Attributes
    ----------
    func : `callable`
        The wrapped function.
    args : `tuple` of `Any`
        Parameters to call ``.func`` with.
    cancelled : `bool`
        Whether the handle is cancelled.
    when : `float`
        The respective loop's time, when the handle should be called.
    
    Notes
    -----
    This class also supports weakreferencing.
    """
    __slots__ = ('__weakref__', )
    
    def __init__(self, when, func, args):
        """
        Creates a new ``TimerWeakHandle`` with the given parameters.
        
        Parameters
        ----------
        when : `float`
            The respective loop's time, when the handle should be called.
        func : `callable`
            The function. to wrap.
        args : `tuple` of `Any`
            Parameters to call `func` with.
        
        Raises
        ------
        TypeError
            `func` is not weakreferable.
        """
        self.when = when
        callback = self._callback(self)
        try:
            if type(func) is MethodType:
                func = weakmethod.from_method(func, callback)
            else:
                func = WeakCallable(func, callback)
        except:
            # never leave a half finished object behind
            self.func = None
            self.args = None
            self.cancelled = True
            raise
        else:
            self.func = func
            self.args = args
            self.cancelled = False
        
    class _callback:
        """
        Weakreference callback used by ``TimerWeakHandle`` to cancel the respective handle, when it's `func` gets
        garbage collected.
        
        Attributes
        ----------
        handle : ``WeakReferer`` (``TimerWeakHandle``)
            The respective handle.
        """
        __slots__ = ('handle', )
        
        def __init__(self, handle):
            """
            Creates a new weakreference callback used by ``TimerWeakHandle``.
            
            Parameters
            ----------
            handle : ``TimerWeakHandle``
                The respective handle.
            """
            self.handle = WeakReferer(handle)
        
        def __call__(self, reference):
            """
            Called, when the respective `TimerWeakHandle.func` is garbage collected.
            
            Parameters
            ----------
            reference : ``WeakReferer`` instance
                Weakreference to the dead `func`.
            """
            handle = self.handle()
            if (handle is not None):
                handle.cancel()

class CyclerCallable:
    """
    An element of a ``Cycler``, which describes whether the stored callable is sync or async and what is it's ordering
    priority.
    
    Attributes
    ----------
    func : `callable`
        The function to call.
    is_async : `bool`
        Whether `func` is async.
    priority : `int`
        Call order priority inside of a ``Cycler``.
    """
    __slots__ = ('func', 'is_async', 'priority')
    
    def __new__(cls, func, priority):
        """
        Creates a new ``CyclerCallable`` instance with the given parameters.
        
        Parameters
        ----------
        func : `callable`
            The function to call.
        priority : `int`
            Call order priority inside of a ``Cycler``.
        
        Raises
        ------
        TypeError
            - `priority` is not `int` instance, neither other numeric convertable to it.
            - `func` is not `callable`.
            - `func` accepts less or more reserved positional parameters than `1`.
        """
        if type(func) is cls:
            return func
        
        priority_type = type(priority)
        if (priority_type is not int):
            try:
                __int__ = getattr(priority, '__int__')
            except AttributeError:
                raise TypeError(f'The given `priority` is not `int`, neither other numeric convertable to it, got '
                    f'{priority_type.__name__}.') from None
            
            priority = __int__(priority)
        
        analyzer = CallableAnalyzer(func)
        min_, max_ = analyzer.get_non_reserved_positional_parameter_range()
        if min_ > 1:
            raise TypeError(f'`{func!r}` excepts at least `{min_!r}` non reserved parameters, meanwhile `1` would be '
                'passed to it.')
        
        if not ((min_ == 1) or max_ >= 1 or analyzer.accepts_args()):
            raise TypeError(f'`{func!r}` expects maximum `{max_!r}` non reserved parameters, meanwhile the event '
                'expects to pass `1`.')
        
        is_async = analyzer.is_async()
        
        self = object.__new__(cls)
        self.func = func
        self.is_async = is_async
        self.priority = priority
        
        return self
    
    def __repr__(self):
        """Returns the cycler callable's representation."""
        return f'{self.__class__.__name__}(func={self.func!r}, priority={self.priority!r})'
    
    def __gt__(self, other):
        """Returns whether the priority of this cycler callable is greater than the other's."""
        return self.priority > other.priority
    
    def __ge__(self, other):
        """
        Returns whether the priority of this cycler callable is greater than the other's, or if both instance is equal.
        """
        self_priority = self.priority
        other_priority = other.priority
        if self_priority > other_priority:
            return True
        
        if other_priority == other_priority:
            if self.func == other.func:
                return True
        
        return False
    
    def __eq__(self, other):
        """Returns whether this cycler callable equals to the other."""
        if self.priority != other.priority:
            return False
        
        if self.func != other.func:
            return False
        
        return True
    
    def __ne__(self, other):
        """Returns whether this cycler callable not equals to the other."""
        if self.priority != other.priority:
            return True
        
        if self.func != other.func:
            return True
        
        return False
    
    def __le__(self, other):
        """
        Returns whether the priority of this cycler callable is less than the other's, or if both instance is equal.
        """
        self_priority = self.priority
        other_priority = other.priority
        if self_priority < other_priority:
            return True
        
        if other_priority == other_priority:
            if self.func == other.func:
                return True
        
        return False

    def __lt__(self, other):
        """Returns whether the priority of this cycler callable is less than the other's."""
        return self.priority < other.priority


class Cycler:
    """
    Cycles the given functions on an event loop, by calling them after every `n` amount of seconds.
    
    Attributes
    ----------
    cycle_time : `float`
        The time interval of the cycler to call the added functions.
    funcs : `list` of ``CyclerCallable``
        Callables of a cycler containing whether they are sync, async, and what is their priority order.
    handle : ``TimerHandle``
        Handler, what will call the cycler when cycle time is over.
    loop : ``EventThread``
        The async event loop of the cycler, what it uses to ensure itself.
    """
    __slots__ = ('cycle_time', 'funcs', 'handle', 'loop',)
    
    def __new__(cls, loop, cycle_time, *funcs, priority=0):
        """
        Creates a new ``Cycler`` with the given parameters.
        
        Parameters
        ----------
        loop : ``EventThread``
            The async event loop of the cycler, what it uses to ensure itself.
        cycle_time : `float`
            The time interval of the cycler to call the added functions.
        *funcs : `callable`
            Callables, what the cycler will call.
        priority : `int`
            Priority order of the added callables, which define in which order the given `funcs` will be called.
            Defaults to `0`
        
        Raises
        ------
        RuntimeError
            Event loop closed.
        TypeError
            - `cycle_time` is not `float` instance, neither other numeric convertable to it.
            - `priority` is not `int` instance, neither other numeric convertable to it.
            - Any `func` is not `callable`.
            - Any `func` accepts less or more reserved positional parameters than `1`.
        ValueError
            If `cycle_time` is negative or `0`.
        
        Notes
        -----
        If the respective event loop is not running yet, then creating a ``Cycler`` will not start it either.
        """
        if not loop.running and not loop.should_run:
            raise RuntimeError('Event loop is closed.')
        
        cycle_time_type = cycle_time.__class__
        if cycle_time_type is not float:
            try:
                __float__ = getattr(cycle_time_type, '__float__')
            except AttributeError:
                raise TypeError(f'The given `cycle_time` is not `float`, neither other numeric convertable to it, got '
                    f'{cycle_time_type.__name__}.') from None
            
            cycle_time = __float__(cycle_time)
        
        if cycle_time <= 0.0:
            raise ValueError(f'{cycle_time} cannot be `0` or less, got `{cycle_time!r}`.')
        
        priority_type = type(priority)
        if (priority_type is not int):
            try:
                __int__ = getattr(priority, '__int__')
            except AttributeError:
                raise TypeError(f'The given `priority` is not `int`, neither other numeric convertable to it, got '
                    f'{priority_type.__name__}.') from None
            
            priority = __int__(priority)
        
        validated_funcs = []
        
        if funcs:
            for func in funcs:
                validated_func = CyclerCallable(func, priority)
                validated_funcs.append(validated_func)
            
            validated_funcs.sort()
        
        self = object.__new__(cls)
        self.loop = loop
        self.funcs = validated_funcs
        self.cycle_time = cycle_time
        if current_thread() is loop:
            handle = loop.call_later(cycle_time, cls._run, self)
        else:
            handle = loop.call_soon_thread_safe_lazy(loop.__class__.call_later, loop, cycle_time, cls._run, self)
        
        self.handle = handle
        
        return self
    
    def _run(self):
        """
        Runs all the functions added to the cycler.
        """
        for func in self.funcs:
            try:
                result = func.func(self)
                if func.is_async:
                    Task(result, self.loop)
            except BaseException as err:
                self.loop.render_exc_async(err, [
                    self.__class__.__name__,
                    ' exception occurred\nat calling ',
                    repr(func),
                    '\n',
                        ])
        
        self.handle = self.loop.call_later(self.cycle_time, self.__class__._run, self)
    
    def __repr__(self):
        """Returns the cycler's representation."""
        result = [
            self.__class__.__name__,
            '(',
            repr(self.loop),
            ', ',
            str(self.cycle_time)
                ]
        
        funcs = self.funcs
        limit = len(funcs)
        if limit:
            priority = funcs[0].priority
            
            index = 1
            while index < limit:
                func = funcs[index]
                if func.priority == priority:
                    index += 1
                    continue
                
                for func in funcs:
                    result.append(', ')
                    result.append(repr(func))
                break
            
            else:
                for func in funcs:
                    result.append(', ')
                    result.append(repr(func.func))
                
                result.append(', priority=')
                result.append(repr(priority))
        
        return ''.join(result)
    
    def cancel(self):
        """
        Cancels the cycler.
        
        If called from an other thread than it's event loop, then ensures ``._cancel`` on it instead of calling it
        right away.
        """
        loop = self.loop
        if current_thread() is loop:
            self._cancel()
            return
        
        loop.call_soon_thread_safe_lazy(self.__class__._cancel, self)
    
    def _cancel(self):
        """
        Cancels the cycler.
        
        This method always runs on the cycler's event loop.
        """
        handle = self.handle
        if (handle is not None):
            self.handle = None
            handle.cancel()
    
    def call_now(self):
        """
        Calls the cycler now, doing it's cycle.
        
        If called from an other thread than it's event loop, then ensures ``._call_now`` on it instead of calling it
        right away.
        """
        loop = self.loop
        if current_thread() is loop:
            self._call_now()
            return
        
        loop.call_soon_thread_safe_lazy(self.__class__._call_now, self)
    
    def _call_now(self):
        """
        Calls the cycler now, doing it's cycle.
        
        This method always runs on the cycler's event loop.
        """
        handle = self.handle
        if (handle is not None):
            handle.cancel()
        
        self._run()
    
    def reschedule(self):
        """
        Reschedules the cycler, making it's cycle to start since now. If the cycler is not running, also starts it.
        
        If called from an other thread than it's event loop, then ensures ``._reschedule`` on it instead of calling it
        right away.
        """
        loop = self.loop
        if current_thread() is loop:
            self._reschedule()
            return
        
        loop.call_soon_thread_safe_lazy(self.__class__._reschedule, self)
    
    def _reschedule(self):
        """
        Reschedules the cycler, making it's cycle to start since now. If the cycler is not running, also starts it.
        
        This method always runs on the cycler's event loop.
        """
        handle = self.handle
        if (handle is not None):
            handle.cancel()
        
        self.handle = self.loop.call_later(self.cycle_time, self.__class__._run, self)
    
    @property
    def running(self):
        """
        Returns whether the cycler is currently running.
        
        Returns
        -------
        running : `str`
        """
        return (self.handle is not None)
    
    def set_cycle_time(self, cycle_time):
        """
        Sets the cycle time of the cycler to the given value.
        
        Parameters
        ----------
        cycle_time : `float`
            The time interval of the cycler to call the added functions.
        
        Raises
        ------
        TypeError
            `cycle_time` is not `float` instance, neither other numeric convertable to it.
        ValueError
            If `cycle_time` is negative or `0`.
        """
        cycle_time_type = cycle_time.__class__
        if cycle_time_type is not float:
            try:
                __float__ = getattr(cycle_time_type, '__float__')
            except AttributeError:
                raise TypeError(f'The given `cycle_time` is not `float`, neither other numeric convertable to it, got '
                    f'{cycle_time_type.__name__}.') from None
            
            cycle_time = __float__(cycle_time)
        
        if cycle_time <= 0.0:
            raise ValueError(f'{cycle_time} cannot be `0` or less, got `{cycle_time!r}`.')
        
        self.cycle_time = cycle_time
    
    def append(self, func, priority=0):
        """
        Adds the given `func` to the cycler to call.
        
        If called from an other thread than it's event loop, then it will ensure adding the `func` on it's own.
        
        Parameters
        ----------
        func : `callable`
            Callable, what the cycler will call.
        priority : `int`
            Priority order of the added callables, which define in which order the given `funcs` will be called.
        
        Raises
        ------
        TypeError
            - `priority` is not `int` instance, neither other numeric convertable to it.
            - Any `func` is not `callable`.
            - Any `func` accepts less or more reserved positional parameters than `1`.
        """
        validated_func = CyclerCallable(func, priority)
        
        loop = self.loop
        if current_thread() is loop:
            self._append(validated_func)
            return
        
        loop.call_soon_thread_safe_lazy(self.__class__._append, self, validated_func)
    
    def _append(self, validated_func):
        """
        Adds the given `func` to the cycler to call.
        
        This method always runs on the cycler's event loop.
        
        Parameters
        ----------
        validated_func : ``CyclerCallable``
            The already validated function to add.
        """
        funcs = self.funcs
        funcs.append(validated_func)
        funcs.sort()
    
    def remove(self, func):
        """
        Removes the given `func` from the cycler, so it will stop calling it.
        
        If called from an other thread than it's event loop, then ensures ``._remove`` on it instead of calling it
        right away.
        
        Parameters
        ----------
        func : `callable`
            The function to remove.
        """
        loop = self.loop
        if current_thread() is loop:
            self._remove(func)
            return
        
        loop.call_soon_thread_safe_lazy(self.__class__._remove, self, func)
    
    def _remove(self, func):
        """
        Removes the given `func` from the cycler, so it will stop calling it.
        
        This method always runs on the cycler's event loop.
        
        Parameters
        ----------
        func : `callable`
            The function to remove.
        """
        index = 0
        funcs = self.funcs
        limit = len(funcs)
        
        is_cycler_callable = (type(func) is CyclerCallable)
        
        while index < limit:
            to_compare = funcs[index]
            if (not is_cycler_callable):
                to_compare = to_compare.func
            
            if to_compare == func:
                del funcs[index]
                break
            
            index += 1
            continue
    
    def get_time_till_next_call(self):
        """
        Returns how much time is left till the next cycle call.
        
        Might return `-1.` if the cycler is closed, or `0.` if the calls are taking place right now.
        
        Returns
        -------
        time_till_next_call : `float`
        """
        handle = self.handle
        if handle is None:
            return -1. # wont be be called
        
        at = handle.when-LOOP_TIME()
        
        if at < 0.0:
            return 0.0 # right now
        
        return at
    
    def get_time_of_next_call(self):
        """
        Returns when the next cycle call will be.
        
        Might return `-1.` if the cycler is closed.
        
        Returns
        -------
        ime_of_next_call : `float`
        """
        handle = self.handle
        if handle is None:
            return -1. # wont be be called
        return handle.when


class ThreadSyncerCTX:
    """
    Thread syncer for ``EventThread``-s, to stop their execution, meanwhile they are used inside of a a `with` block.
    The local thread's exception is stopped, meanwhile it waits for the ``EventThread`` top pause.
    
    Can be used as a context manager, like:
    
    ```py
    with ThreadSyncerCTX(LOOP):
        # The event loop is paused inside here.
    ```
    
    Or, can be used with ``EventThread.enter()`` as well, like:
    
    ```py
    with LOOP.enter():
        # The event loop is paused inside here.
    ```
    
    Attributes
    ----------
    loop : ``EventThread``
        The respective event loop.
    enter_event : `threading.Event`
        Threading event, which blocks the local thread, till the respective event loop pauses.
    exit_event : `threading.Event`
        Blocks the respective event loop, till the local thread gives the control back to it with exiting the `with`
        block.
    """
    __slots__ = ('loop', 'enter_event', 'exit_event')
    
    def __init__(self, loop):
        """
        Creates a new ``ThreadSyncerCTX`` bound to the given event loop.
        
        Parameters
        ----------
        loop : ``EventThread``
            The event loop to pause.
        """
        self.loop = loop
        self.enter_event = Event()
        self.exit_event = Event()

    def __enter__(self):
        """
        Blocks the local thread, till the respective ``EventThread`` pauses. If the ``EventThread`` is stopped already,
        does nothing.
        """
        loop = self.loop
        if loop.running:
            handle = Handle(self._give_control_cb, ())
            loop._ready.append(handle)
            loop.wake_up()
            self.enter_event.wait()
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Un-pauses the respective ``EventThread``."""
        self.exit_event.set()
        return False
    
    def _give_control_cb(self):
        """
        Callback used to pause the respective ``EventThread`` and give control to the other one.
        """
        self.enter_event.set()
        self.exit_event.wait()

_HAS_IPv6 = hasattr(module_socket, 'AF_INET6')

def _ip_address_info(host, port, family, type_, protocol):
    """
    Gets the address info for the given parameters.
    
    Parameters
    ----------
    host : `str` or `bytes`
        The host ip address.
    port : `int`
        The host port.
    family : `AddressFamily` or `int`
        Address family.
    type_ : `SocketKind` or `int`
        Socket type.
    protocol : `int`
        Protocol type.
    
    Returns
    -------
    result : `None` or `tuple` (`AddressFamily` or `int`, `SocketKind` or `int`, `int`, `str`, `tuple` (`str, `int`))
        If everything is correct, returns a `tuple` of 5 elements:
        - `family` : Address family.
        - `type_` : Socket type.
        - `protocol` : Protocol type.
        - `canonical_name` : Represents the canonical name of the host. (Always empty string.)
        - `socket_address` : Socket address containing the `host` and the `port`.
    """
    # Try to skip get_address_info if `host` is already an IP. Users might have handled name resolution in their own
    # code and pass in resolved IP-s.
    if not hasattr(module_socket, 'inet_pton'):
        return
    
    if protocol not in (0, module_socket.IPPROTO_TCP, module_socket.IPPROTO_UDP) or (host is None):
        return
    
    if type_ == module_socket.SOCK_STREAM:
        protocol = module_socket.IPPROTO_TCP
    elif type_ == module_socket.SOCK_DGRAM:
        protocol = module_socket.IPPROTO_UDP
    else:
        return
    
    if port is None:
        port = 0
    elif type(port) is int:
        # Has the most chance.
        pass
    elif isinstance(port, bytes) and port == b'':
        port = 0
    elif isinstance(port, str) and port == '':
        port = 0
    else:
        # If port's a service name like "http", don't skip get_address_info.
        try:
            port = int(port)
        except (TypeError, ValueError):
            return
    
    if family == module_socket.AF_UNSPEC:
        address_families = [module_socket.AF_INET]
        if _HAS_IPv6:
            address_families.append(module_socket.AF_INET6)
    else:
        address_families = [family]
    
    if isinstance(host, bytes):
        host = host.decode('idna')
    
    if '%' in host:
        return
    
    for family in address_families:
        try:
            module_socket.inet_pton(family, host)
            # The host has already been resolved.
        except OSError:
            pass
        else:
            return family, type_, protocol,'', (host, port)
    
    # `host` is not an IP address.
    return None

def _is_datagram_socket(socket):
    """
    Returns whether the given socket is datagram socket.
    
    Parameters
    ----------
    socket : `socket.socket`
        The socket to check.
    
    Returns
    -------
    is_datagram_socket : `bool`
    """
    return (socket.type&module_socket.SOCK_DGRAM) == module_socket.SOCK_DGRAM

def _is_stream_socket(socket):
    """
    Returns whether the given socket is stream socket.
    
    Parameters
    ----------
    socket : `socket.socket`
        The socket to check.
    
    Returns
    -------
    is_stream_socket : `bool`
    """
    return (socket.type&module_socket.SOCK_STREAM) == module_socket.SOCK_STREAM

def _set_reuse_port(socket):
    """
    Tells to the kernel to allow this endpoint to be bound to the same port as an other existing endpoint already
    might be bound to.
    
    Parameters
    ----------
    socket : `socket.socket`.
        The socket to set reuse to.
    
    Raises
    ------
    ValueError
        `reuse_port` is not supported by socket module.
    """
    if not hasattr(module_socket, 'SO_REUSEPORT'):
        raise ValueError('`reuse_port` not supported by socket module.')
    else:
        try:
            socket.setsockopt(module_socket.SOL_SOCKET, module_socket.SO_REUSEPORT, 1)
        except OSError:
            raise ValueError('`reuse_port` not supported by socket module, `SO_REUSEPORT` defined but not implemented.')

_OLD_ASYNC_GENERATOR_HOOKS = sys.get_asyncgen_hooks()

def _async_generator_first_iteration_hook(async_generator):
    """
    Adds asynchronous generators to their respective event loop. These async gens are shut down, when the loop is
    stopped.
    
    Parameters
    ----------
    async_generator : `async_generator`
    """
    loop = current_thread()
    if isinstance(loop, EventThread):
        if loop._async_generators_shutdown_called:
            return
        
        loop._async_generators.add(async_generator)
        return
    
    first_iteration = _OLD_ASYNC_GENERATOR_HOOKS.firstiter
    if first_iteration is not None:
        first_iteration(async_generator)

def _async_generator_finalizer_hook(async_generator):
    """
    Removes asynchronous generator from their respective event loop.
    
    Parameters
    ----------
    async_generator : `async_generator`
    """
    loop = current_thread()
    if isinstance(loop, EventThread):
        loop._async_generators.discard(async_generator)
        if not loop.running:
            return
            
        Task(async_generator.aclose(), loop)
        loop.wake_up()
        return
    
    finalizer = _OLD_ASYNC_GENERATOR_HOOKS.finalizer
    if finalizer is not None:
        finalizer(async_generator)

sys.set_asyncgen_hooks(firstiter=_async_generator_first_iteration_hook, finalizer=_async_generator_finalizer_hook)


if sys.platform == 'win32':
    #If windows select raises OSError, we cannot do anything, but
    #if it it raises ValueError, we can increases windows select()
    #from 500~ till the hard limit, with sharding up it's polls
    
    from select import select
    MAX_FD_S = 500 #512 is the actual amount?
    MAX_SLEEP = 0.001
    EMPTY = []
    
    class DefaultSelector(DefaultSelector):
        """
        Selector subclass for windows to bypass default limit.
        
        Note, that this selector might become CPU heavy if the limit is passed and the sockets might become closed
        if too much is open.
        
        I do not take credit for any misbehaviour.
        """
        def _select(self, r, w, _, timeout=None):
            try:
                result_r, result_w, result_x = select(r, w, w, timeout)
            except ValueError:
                default_reader = current_thread()._self_read_socket
                r.remove(default_reader.fileno())
                
                sharded_r = []
                sharded_w = []
                
                sharded = [(sharded_r, sharded_w,),]
                
                count = 0
                for reader in r:
                    if count == MAX_FD_S:
                        sharded_r = [reader]
                        sharded_w = []
                        sharded.append((sharded_r, sharded_w),)
                        count = 1
                    else:
                        sharded_r.append(reader)
                        count = count+1
                
                for writer in w:
                    if count == MAX_FD_S:
                        sharded_r = []
                        sharded_w = [writer]
                        sharded.append((sharded_r, sharded_w),)
                        count = 1
                    else:
                        sharded_w.append(writer)
                        count += 1
                
                collected_r = []
                collected_w = []
                
                r.add(default_reader.fileno())
                
                for iter_r, iter_w in sharded:
                    try:
                        result_r, result_w, result_x = select(iter_r, iter_w, iter_w, 0.0)
                    except OSError:
                        remove = []
                        for reader in iter_r:
                            try:
                                l = [reader]
                                result_r, result_w, result_x = select(l, EMPTY, EMPTY, 0.0)
                            except OSError:
                                remove.append(reader)
                            else:
                                if result_r:
                                    collected_r.append(result_r[0])
                        
                        if remove:
                            for reader in remove:
                                r.discard(reader)
                                
                                try:
                                    self.unregister(reader)
                                except KeyError:
                                    pass
                            remove.clear()
                        
                        for writer in iter_w:
                            try:
                                l = [writer]
                                result_r, result_w, result_x=select(EMPTY, l, l, 0.0)
                            except OSError:
                                remove.append(writer)
                            else:
                                if result_w:
                                    collected_w.append(result_w[0])
                                elif result_x:
                                    collected_w.append(result_x[0])
                        
                        if remove:
                            for writer in remove:
                                w.discard(writer)
                                
                                try:
                                    self.unregister(writer)
                                except KeyError:
                                    pass
                            remove.clear()
                    else:
                        collected_r.extend(result_r)
                        collected_w.extend(result_w)
                        collected_w.extend(result_x)

                if (not collected_r) and (not collected_w):
                    if timeout is None:
                        timeout = MAX_SLEEP
                    elif timeout < 0.0:
                        timeout = 0.0
                    elif timeout > MAX_SLEEP:
                        timeout = MAX_SLEEP
                    
                    result_r, result_w, result_x = select([default_reader], EMPTY, EMPTY, timeout)
                    collected_r.extend(result_r)
                
                return collected_r, collected_w, EMPTY
            
            except OSError:
                collected_r = []
                collected_w = []
                do_later_r = []
                do_later_w = []
                remove = []
                for reader in r:
                    try:
                        l = [reader]
                        result_r, result_w, result_x = select(l, EMPTY, EMPTY, 0.0)
                    except OSError:
                        remove.append(reader)
                    else:
                        if result_r:
                            collected_r.append(result_r[0])
                        else:
                            do_later_r.append(reader)
                
                if remove:
                    for reader in remove:
                        r.discard(reader)
                        
                        try:
                            self.unregister(reader)
                        except KeyError:
                            pass
                    remove.clear()
                    
                for writer in w:
                    try:
                        l = [writer]
                        result_r, result_w, result_x = select(EMPTY, l, l, 0.0)
                    except OSError:
                        remove.append(writer)
                    else:
                        if result_w:
                            collected_w.append(result_w[0])
                        elif result_x:
                            collected_w.append(result_x[0])
                        else:
                            do_later_w.append(writer)
                    
                if remove:
                    for writer in remove:
                        w.discard(writer)
                        
                        try:
                            self.unregister(writer)
                        except KeyError:
                            pass
                    remove.clear()
                
                if collected_r or collected_w:
                    return collected_r, collected_w, EMPTY
                
                result_r, result_w, result_x = select(r, w, w, timeout)
                result_w.extend(result_x)
                return result_r, result_w, EMPTY
            else:
                result_w.extend(result_x)
                return result_r, result_w, EMPTY


class Server:
    """
    Server returned by ``EventThread.create_server``.
    
    Attributes
    ----------
    active_count : `int`
        The amount of active connections bound to the server.
    backlog : `int`
        The maximum number of queued connections passed to `listen()` (defaults to 100).
    close_waiters : `None` or `list` of ``Future``
        Futures, which are waiting for the server to close. If the server is already closed, set as `None`.
    loop : ``EventThread``
        The event loop to what the server is bound to.
    protocol_factory : `callable`
        Factory function for creating a protocols.
    serving : `bool`
        Whether the server is serving.
    sockets : `None` or `list` of `socket.socket`
        The sockets served by the server. If the server is closed, then i set as `None`.
    ssl_context : `None` or `ssl.SSLContext`
        If ssl is enabled for the connections, then set as `ssl.SSLContext`.
    """
    __slots__ = ('active_count', 'backlog', 'close_waiters', 'loop', 'protocol_factory', 'serving', 'sockets',
        'ssl_context', )
    
    def __init__(self, loop, sockets, protocol_factory, ssl_context, backlog):
        """
        Creates a new server with the given parameters.
        
        Parameters
        ----------
        loop : ``EventThread``
            The event loop to what the server will be bound to.
        sockets : `list` of `socket.socket`
            The sockets to serve by the server.
        protocol_factory : `callable`
            Factory function for creating a protocols.
        ssl_context : `None` or `ssl.SSLContext`
            To enable ssl for the connections, give it as  `ssl.SSLContext`.
        backlog : `int`
            The maximum number of queued connections passed to `listen()` (defaults to 100).
        """
        self.loop = loop
        self.sockets = sockets
        self.active_count = 0
        self.close_waiters = []
        self.protocol_factory = protocol_factory
        self.backlog = backlog
        self.ssl_context = ssl_context
        self.serving = False
    
    def __repr__(self):
        """Returns the server's representation."""
        return f'<{self.__class__.__name__} sockets={self.sockets!r}>'

    def _attach(self):
        """
        Adds `1` to the server active counter.
        """
        self.active_count += 1

    def _detach(self):
        """
        Removes `1` from the server's active counter. If there no more active sockets of the server, then closes it.
        """
        active_count = self.active_count-1
        self.active_count = active_count
        if active_count:
            return
        
        if (self.sockets is None):
            self._wake_up_close_waiters()

    def _wake_up_close_waiters(self):
        """
        Wakes up the server's close waiters.
        """
        close_waiters = self.close_waiters
        if close_waiters is None:
            return
        
        self.close_waiters = None
        for close_waiter in close_waiters:
            close_waiter.set_result(None)
    
    def close(self):
        """
        Closes the server by stopping serving it's sockets and waking up it's close waiters.
        """
        sockets = self.sockets
        if sockets is None:
            return
        
        self.sockets = None
        
        loop = self.loop
        for socket in sockets:
            loop._stop_serving(socket)
        
        self.serving = False
        
        if self.active_count == 0:
            self._wake_up_close_waiters()
    
    async def start(self):
        """
        Starts the server by starting serving it's sockets.
        
        This method is a coroutine.
        """
        if self.serving:
            return
        
        self.serving = True
        
        protocol_factory = self.protocol_factory
        ssl_context = self.ssl_context
        backlog = self.backlog
        loop = self.loop
        
        for socket in self.sockets:
            socket.listen(backlog)
            loop._start_serving(protocol_factory, socket, ssl_context, self, backlog)
        
        # Skip one event loop cycle, so all the callbacks added up ^ will run before returning.
        await skip_ready_cycle()
    

    async def wait_closed(self):
        """
        Blocks the task, till the sever is closes.
        
        This method is a coroutine.
        """
        if self.sockets is None:
            return
        
        close_waiters = self.close_waiters
        if close_waiters is None:
            return
        
        close_waiter = Future(self.loop)
        close_waiters.append(close_waiter)
        await close_waiter


class EventThreadCTXManager:
    """
    Context manager of an ``EventThread``, which wraps it's runner. when the runner is started up, set it's ``waiter.``
    allowing the starter thread to continue.
    
    Attributes
    ----------
    thread : `None` or ``EventThread``
        The wrapped event loop.
    thread_waiter : `None` or `threading.Event`
       Threading event, what is set, when the thread is started up. Set as `None` after set.
    """
    __slots__ = ('thread', 'thread_waiter',)
    def __new__(cls, thread):
        """
        Creates a new event thread context.
        
        Parameters
        ----------
        thread : ``EventThread``
            The event thread to wrap.
        
        Returns
        -------
        self : ``EventThreadCTXManager``
            The created instance
        thread_waiter : `threading.Event`
            Threading event, what is set, when the thread is started up.
        """
        self = object.__new__(cls)
        self.thread = thread
        self.thread_waiter = Event()
        return self
    
    def __enter__(self):
        """
        Called, when the respective event loop's runner started up.
        
        Enters the event loop runner setting it's waiter and finishes the loop's initialization.
        
        Raises
        ------
        RuntimeError
            - If ``EventThreadCTXManager.__enter__`` was called a second time.
            - If called from a different thread as is bound to.
            - If the ``EventThread`` is already running.
            - If the ``EventThread`` is already stopped.
        """
        thread_waiter = self.thread_waiter
        if thread_waiter is None:
            raise RuntimeError(f'{self.__class__.__name__}.__enter__ called with thread waiter lock set.')
        
        try:
            thread = self.thread
            if (thread is not current_thread()):
                raise RuntimeError(f'{thread!r}.run called from an other thread: {current_thread()!r}')
            
            if (thread.running):
                raise RuntimeError(f'{thread!r}.run called when the thread is already running.')
            
            if (thread._is_stopped):
                raise RuntimeError(f'{thread!r}.run called when the thread is already stopped.')
            
            thread.running = True
            
            self_read_socket, self_write_socket = module_socket.socketpair()
            self_read_socket.setblocking(False)
            self_write_socket.setblocking(False)
            thread._self_read_socket = self_read_socket
            thread._self_write_socket = self_write_socket
            thread.add_reader(self_read_socket.fileno(), thread.empty_self_socket)
        finally:
            thread_waiter.set()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        When the event loop's runner stops, it's context closes it.
        """
        thread = self.thread
        self.thread = None
        
        thread.running = False
        thread.remove_reader(thread._self_read_socket.fileno())
        thread._self_read_socket.close()
        thread._self_read_socket = None
        thread._self_write_socket.close()
        thread._self_write_socket = None
        
        thread._ready.clear()
        thread._scheduled.clear()
        
        thread.cancel_executors()
        
        selector = thread.selector
        if (selector is not None):
            thread.selector = None
            selector.close()
        
        return False


class EventThreadRunDescriptor:
    if DOCS_ENABLED:
        __class_doc__ = ("""
        Descriptor which decides, exactly which function of the ``EventThread`` is called, when using it's `.run`
        method.
        
        If called from class, returns `self`. If called from a non yet running event loop, returns that's `.runner`. If
        called from an already stopped event loop, raises `RuntimeError`.
        """)
        
        __instance_doc__ = ("""
        ``EventThread.run`` is an overloaded method, with two usages. The first is when the thread starts up, it will
        run the thread's "runner", ``EvenThread.runner``. The other one usage is, when the event loop is running, then
        it returns it's "caller", ``EvenThread.caller``.
        
        If the event loop is already closed, raises ``RuntimeError``.
        """)
        
        __doc__ = doc_property()
    
    def __get__(self, obj, type_):
        if obj is None:
            return self
        
        if obj.running:
            return obj.caller
        
        if not obj.started:
            if obj._started.is_set():
                obj.started = True
                return obj.runner
            else:
                obj._do_start()
                return obj.caller
        
        if not obj._is_stopped:
            return obj.caller
        
        raise RuntimeError(f'The {obj.__class__.__name__} is already stopped.')
    
    def __set__(self, obj, value):
        raise AttributeError('can\'t set attribute')
    
    def __delete__(self, obj):
        raise AttributeError('can\'t delete attribute')


class EventThreadType(type):
    """
    Type of even thread, which manages their instances creation.
    """
    def __call__(cls, daemon=False, name=None, start_later=True, **kwargs):
        """
        Creates a new ``EventThread`` instance with the given parameters.
        
        Parameters
        ----------
        daemon : ``bool``
            Whether the created thread should be daemon.
        name : `str`
            The created thread's name.
        start_later : `bool`
            Whether the event loop should be started only later
        kwargs : keyword parameters
            Additional event thread specific parameters.
        
        Other Parameters
        ----------------
        keep_executor_count : `int`
            The minimal amount of executors, what the event thread should keep alive. Defaults to `1`.
        
        Returns
        -------
        obj : ``EventThread``
            The created event loop.
        
        Notes
        -----
        ``EventThread`` supports only an additional, `keep_executor_count` parameter, but it's subclass's might
        support other ones as well.
        """
        obj = Thread.__new__(cls)
        cls.__init__(obj, **kwargs)
        Thread.__init__(obj, daemon=daemon, name=name)
        
        obj.ctx = EventThreadCTXManager(obj)
        
        if not start_later:
            obj._do_start()
        
        return obj


@export
class EventThread(Executor, Thread, metaclass=EventThreadType):
    """
    Event loops run asynchronous tasks and callbacks, perform network IO operations, and runs subprocesses.
    
    At hata event loops are represented by ``EventThread``-s, which do not block the source thread, as they say, they
    use their own thread for it.
    
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
    _async_generators: `WeakSet` of `async_generator`
        The asynchronous generators bound to the event loop.
    _async_generators_shutdown_called : `bool`
        Whether the event loop's asynchronous generators where shut down.
    _self_write_socket : `socket.socket`
        Socket, which can be used to wake up the thread by writing into it.
    _ready : `deque` of ``Handle`` instances
        Ready to run handles of the event loop.
    _scheduled : `list` of ``TimerHandle`` instances
        Scheduled timer handles, which will be moved to ``._ready`` when their `when` becomes lower or equal to the
        respective loop time.
    _self_read_socket : `socket.socket`
        Socket, which reads from ``._self_write_socket``.
    ctx : ``EventThreadCTXManager``
        Context of the event loop to ensure it's safe startup and closing.
    current_task : `None` or ``Task``
        The actually running task of the event thread. Set only meanwhile a task is executed.
    running : `bool`
        Whether the event loop is running.
    selector : `selectors.Default_selector`
        Selector to poll from socket.
    should_run : `bool`
        Whether the event loop should do more loops.
    started : `bool`
        Whether the event loop was already started.
    
    Notes
    -----
    Event threads support weakreferencing and dynamic attribute names as well.
    """
    time = LOOP_TIME
    time_resolution = LOOP_TIME_RESOLUTION
    __slots__ = ('__dict__', '__weakref__', '_async_generators', '_async_generators_shutdown_called',
        '_self_write_socket', '_ready', '_scheduled', '_self_read_socket', 'ctx', 'current_task', 'running',
        'selector', 'should_run', 'started',)
    
    def __init__(self, keep_executor_count=1):
        """
        Creates a new ``EventThread`` with the given parameters.
        
        Parameters
        ----------
        keep_executor_count : `int`
            The minimal amount of executors, what the event thread should keep alive. Defaults to `1`.
        
        Notes
        -----
        This magic method is called by ``EventThreadType.__call__``, what does the other steps of the initialization.
        """
        Executor.__init__(self, keep_executor_count)
        self.should_run = True
        self.running = False
        self.started = False
        self.selector = DefaultSelector()
        
        self._ready = deque()
        self._scheduled = []
        self.current_task = None
        
        self._async_generators = weakref.WeakSet()
        self._async_generators_shutdown_called = False
        
        self._self_read_socket = None
        self._self_write_socket = None
    
    def is_started(self):
        """
        Returns whether the thread was started.
        
        Returns
        -------
        is_started : `bool`
        """
        thread_waiter = self.ctx.thread_waiter
        if thread_waiter is None:
            return True
        
        if thread_waiter.is_set():
            return True
        
        return False
    
    def _maybe_start(self):
        """
        Starts the event loop's thread if not yet started.
        
        Returns
        -------
        started : `bool`
            Whether the thread was started up.
        """
        if self.is_started():
            return False
        
        self._do_start()
        return True
    
    def _do_start(self):
        """
        Starts the event loop's thread.
        
        If the event loop is already started will to start it again.
        """
        thread_waiter = self.ctx.thread_waiter
        # set as `None` if already started.
        if thread_waiter is None:
            return
        
        if not self._started.is_set():
            try:
                Thread.start(self)
            except:
                thread_waiter.set()
                raise
        
        thread_waiter.wait()
    
    def __repr__(self):
        """Returns the event thread's representation."""
        repr_parts = ['<', self.__class__.__name__, '(', self._name]
        self.is_alive() # easy way to get ._is_stopped set when appropriate
        if not self.started:
            state = ' created'
        elif self._is_stopped or (not self.running):
            state = ' stopped'
        else:
            state = ' started'
        repr_parts.append(state)
        
        if self._daemonic:
            repr_parts.append(' daemon')
        
        ident = self._ident
        if (ident is not None):
            repr_parts.append(' ident=')
            repr_parts.append(str(ident))
        
        repr_parts.append(' executor info: free=')
        repr_parts.append(str(self.free_executor_count))
        repr_parts.append(', used=')
        repr_parts.append(str(self.used_executor_count))
        repr_parts.append(', keep=')
        repr_parts.append(str(self.keep_executor_count))
        repr_parts.append(')>')

        return ''.join(repr_parts)
    
    
    def call_later(self, delay, callback, *args):
        """
        Schedule callback to be called after the given delay.
        
        Parameters
        ----------
        delay : `float`
            The delay after the `callback` would be called.
        callback : `callable`
            The function to call later.
        *args : parameters
            The parameters to call the `callback` with.
        
        Returns
        -------
        handle : `None` or ``TimerHandle``
            The created handle is returned, what can be used to cancel it. If the event loop is stopped, returns `None`.
        """
        if not self.running:
            if not self._maybe_start():
                return None
        
        handle = TimerHandle(LOOP_TIME()+delay, callback, args)
        heappush(self._scheduled, handle)
        return handle
    
    def call_at(self, when, callback, *args):
        """
        Schedule callback to be called at the given loop time.
        
        Parameters
        ----------
        when : `float`
            The exact loop time, when the callback should be called.
        callback : `callable`
            The function to call later.
        *args : parameters
            The parameters to call the `callback` with.
        
        Returns
        -------
        handle : `None` or ``TimerHandle``
            The created handle is returned, what can be used to cancel it. If the event loop is stopped, returns `None`.
        """
        if not self.running:
            if not self._maybe_start():
                return None
        
        handle = TimerHandle(when, callback, args)
        heappush(self._scheduled, handle)
        return handle
    
    def call_later_weak(self, delay, callback, *args):
        """
        Schedule callback with weakreferencing it to be called after the given delay.
        
        Parameters
        ----------
        delay : `float`
            The delay after the `callback` would be called.
        callback : `callable`
            The function to call later.
        *args : parameters
            The parameters to call the `callback` with.
        
        Returns
        -------
        handle : `None` or ``TimerWeakHandle``
            The created handle is returned, what can be used to cancel it. If the event loop is stopped, returns `None`.
        
        Raises
        ------
        TypeError
            If `callback` cannot be weakreferred.
        """
        if not self.running:
            if not self._maybe_start():
                return None
        
        handle = TimerWeakHandle(LOOP_TIME()+delay, callback, args)
        heappush(self._scheduled, handle)
        return handle
    
    def call_at_weak(self, when, callback, *args):
        """
        Schedule callback with weakreferencing it to be called at the given loop time.
        
        Parameters
        ----------
        when : `float`
            The exact loop time, when the callback should be called.
        callback : `callable`
            The function to call later.
        *args : parameters
            The parameters to call the `callback` with.
        
        Returns
        -------
        handle : `None` or ``TimerWeakHandle``
            The created handle is returned, what can be used to cancel it. If the event loop is stopped, returns `None`.
        
        Raises
        ------
        TypeError
            If `callback` cannot be weakreferred.
        """
        if not self.running:
            if not self._maybe_start():
                return None
        
        handle = TimerWeakHandle(when, callback, args)
        heappush(self._scheduled, handle)
        return handle
    
    def call_soon(self, callback, *args):
        """
        Schedules the callback to be called at the next iteration of the event loop.
        
        Parameters
        ----------
        callback : `callable`
            The function to call later.
        *args : parameters
            The parameters to call the `callback` with.
        
        Returns
        -------
        handle : `None` or ``Handle``
            The created handle is returned, what can be used to cancel it. If the event loop is stopped, returns `None`.
        """
        if not self.running:
            if not self._maybe_start():
                return None
        
        handle = Handle(callback, args)
        self._ready.append(handle)
        return handle
    
    def call_soon_thread_safe(self, callback, *args):
        """
        Schedules the callback to be called at the next iteration of the event loop. Wakes up the event loop if sleeping,
        so can be used from other threads as well.
        
        Parameters
        ----------
        callback : `callable`
            The function to call later.
        *args : parameters
            The parameters to call the `callback` with.
        
        Returns
        -------
        handle : `None` or ``Handle``
            The created handle is returned, what can be used to cancel it. If the event loop is stopped, returns `None`.
        """
        if not self.running:
            if not self._maybe_start():
                return None
        
        handle = Handle(callback, args)
        self._ready.append(handle)
        self.wake_up()
        return handle
    
    def call_soon_thread_safe_lazy(self, callback, *args):
        """
        Schedules the callback to be called at the next iteration of the event loop. If the event loop is already
        running, wakes it up.
        
        Parameters
        ----------
        callback : `callable`
            The function to call later.
        *args : parameters
            The parameters to call the `callback` with.
        
        Returns
        -------
        handle : `None` or ``Handle``
            The created handle is returned, what can be used to cancel it. If the event loop is stopped, returns `None`.
        """
        if self.running:
            should_wake_up = True
        else:
            if self.is_started():
                should_wake_up = True
            elif self.should_run:
                should_wake_up = False
            else:
                return None
        
        handle = Handle(callback, args)
        self._ready.append(handle)
        
        if should_wake_up:
            self.wake_up()
        
        return handle
        
    def cycle(self, cycle_time, *funcs, priority=0):
        """
        Cycles the given functions on an event loop, by calling them after every `n` amount of seconds.
        
        Parameters
        ----------
        cycle_time : `float`
            The time interval of the cycler to call the added functions.
        *funcs : `callable`
            Callables, what the cycler will call.
        priority : `int`
            Priority order of the added callables, which define in which order the given `funcs` will be called.
            Defaults to `0`
        
        Returns
        -------
        cycler : ``Cycler``
            A cycler with what the added function and the cycling can be managed.
        """
        return Cycler(self, cycle_time, *funcs, priority=priority)
    
    def _schedule_callbacks(self, future):
        """
        Schedules the callbacks of the given future.
        
        Parameters
        ----------
        future : ``Future`` instance
            The future instance, what's callbacks should be ensured.
        
        Notes
        -----
        If the event loop is not running, clears the callback instead of scheduling them.
        """
        callbacks = future._callbacks
        if not self.running:
            if not self._maybe_start():
                callbacks.clear()
                return
        
        while callbacks:
            handle = Handle(callbacks.pop(), (future,))
            self._ready.append(handle)
    
    def create_future(self):
        """
        Creates a future bound to the event loop.
        
        Returns
        -------
        future : ``Future``
            The created future.
        """
        return Future(self)
    
    def create_task(self, coro):
        """
        Creates a task wrapping the given coroutine.
        
        Parameters
        ----------
        coro : `coroutine` or `generator`
            The coroutine, to wrap.
        
        Returns
        -------
        task : ``Task``
            The created task instance.
        """
        return Task(coro, self)
    
    def create_task_thread_safe(self, coro):
        """
        Creates a task wrapping the given coroutine and wakes up the event loop. Wakes up the event loop if sleeping,
        what means it is safe to use from other threads as well.
        
        Parameters
        ----------
        coro : `coroutine` or `generator`
            The coroutine, to wrap.
        
        Returns
        -------
        task : ``Task``
            The created task instance.
        """
        task = Task(coro, self)
        self.wake_up()
        return task
    
    def enter(self):
        """
        Can be used to pause the event loop. Check ``ThreadSyncerCTX`` for more details.
        
        Returns
        -------
        thread_syncer : ``ThreadSyncerCTX``
        """
        return ThreadSyncerCTX(self)
    
    def ensure_future(self, coro_or_future):
        """
        Ensures the given coroutine or future on the event loop. Returns an awaitable ``Future`` instance.
        
        Parameters
        ----------
        coro_or_future : `awaitable`
            The coroutine or future to ensure.
        
        Returns
        -------
        future : ``Future`` instance.
            The return type depends on `coro_or_future`'s type.
            
            - If `coro_or_future` is given as `coroutine` or as `generator`, returns a ``Task`` instance.
            - If `coro_or_future` is given as ``Future`` instance, bound to the current event loop, returns it.
            - If `coro_or_future`is given as ``Future`` instance, bound to an other event loop, returns a
                ``FutureAsyncWrapper``.
            - If `coro_or_future` defines an `__await__` method, then returns a ``Task`` instance.
        
        Raises
        ------
        TypeError
            If `coro_or_future` is not `awaitable`.
        """
        if is_coroutine(coro_or_future):
            return Task(coro_or_future, self)
        
        if isinstance(coro_or_future, Future):
            if coro_or_future._loop is not self:
                coro_or_future = FutureAsyncWrapper(coro_or_future, self)
            return coro_or_future
        
        type_ = type(coro_or_future)
        if hasattr(type_, '__await__'):
            return Task(type_.__await__(coro_or_future), self)
        
        raise TypeError('A Future, a coroutine or an awaitable is required.')
    
    def ensure_future_thread_safe(self, coro_or_future):
        """
        Ensures the given coroutine or future on the event loop. Returns an awaitable ``Future`` instance. Wakes up
        the event loop if sleeping, what means it is safe to use from other threads as well.
        
        Parameters
        ----------
        coro_or_future : `awaitable`
            The coroutine or future to ensure.
        
        Returns
        -------
        future : ``Future`` instance.
            The return type depends on `coro_or_future`'s type.
            
            - If `coro_or_future` is given as `coroutine` or as `generator`, returns a ``Task`` instance.
            - If `coro_or_future` is given as ``Future`` instance, bound to the current event loop, returns it.
            - If `coro_or_future`is given as ``Future`` instance, bound to an other event loop, returns a
                ``FutureAsyncWrapper``.
            - If `coro_or_future` defines an `__await__` method, then returns a ``Task`` instance.
        
        Raises
        ------
        TypeError
            If `coro_or_future` is not `awaitable`.
        """
        if is_coroutine(coro_or_future):
            task = Task(coro_or_future, self)
            self.wake_up()
            return task
        
        if isinstance(coro_or_future, Future):
            if coro_or_future._loop is not self:
                coro_or_future = FutureAsyncWrapper(coro_or_future, self)
            return coro_or_future
        
        type_ = type(coro_or_future)
        if hasattr(type_, '__await__'):
            task = Task(type_.__await__(coro_or_future), self)
            self.wake_up()
            return task

        raise TypeError('A Future, a coroutine or an awaitable is required.')
    
    run = EventThreadRunDescriptor()
    
    def runner(self):
        """
        Runs the event loop, until ``.stop`` is called.
        
        Hata ``EventThread`` are created as already running event loops.
        """
        with self.ctx:
            key = None
            file_object = None
            reader = None
            writer = None
            
            ready = self._ready # use thread safe type with no lock
            scheduled = self._scheduled # these can be added only from this thread
            
            while self.should_run:
                timeout = LOOP_TIME()+LOOP_TIME_RESOLUTION # calculate limit
                while scheduled: # handle 'later' callbacks that are ready.
                    handle = scheduled[0]
                    if handle.cancelled:
                        heappop(scheduled)
                        continue
                    
                    if handle.when >= timeout:
                        break
                    
                    ready.append(handle)
                    heappop(scheduled)
                
                if ready:
                    timeout = 0.
                elif scheduled:
                    # compute the desired timeout.
                    timeout = scheduled[0].when-LOOP_TIME()
                else:
                    timeout = None
                
                event_list = self.selector.select(timeout)
                if event_list:
                    for key, mask in event_list:
                        file_object = key.fileobj
                        reader, writer = key.data
                        if (reader is not None) and (mask&EVENT_READ):
                            if reader.cancelled:
                                self.remove_reader(file_object)
                            else:
                                if not reader.cancelled:
                                    ready.append(reader)
                        if (writer is not None) and (mask&EVENT_WRITE):
                            if writer.cancelled:
                                self.remove_writer(file_object)
                            else:
                                if not writer.cancelled:
                                    ready.append(writer)
                    
                    key = None
                    file_object = None
                    reader = None
                    writer = None
                    
                event_list = None
                
                # process callbacks
                for _ in range(len(ready)):
                    handle = ready.popleft()
                    if not handle.cancelled:
                        handle._run()
                handle = None # remove from locals or the gc derps out.
    
    def caller(self, awaitable, timeout=None):
        """
        Ensures the given awaitable on the event loop and returns it's result when done.
        
        Parameters
        ----------
        awaitable : `awaitable`
            The awaitable to run.
        timeout : `None` or `float`, Optional
            Timeout after the awaitable should be cancelled. Defaults to `None`.

        Returns
        -------
        result : `Any`
            Value returned by `awaitable`.
        
        Raises
        ------
        TypeError
            If `awaitable` is not `awaitable`.
        TimeoutError
             If `awaitable` did not finish before the given `timeout` is over.
        AssertionError
            If called from itself.
        BaseException
            Any exception raised by `awaitable`.
        """
        if __debug__:
            if current_thread() is self:
                raise AssertionError(f'`{self.__class__.__name__}.run` should not be called from itself.')
        
        return self.ensure_future_thread_safe(awaitable).sync_wrap().wait(timeout)
    
    if __debug__:
        def render_exc_async(self, exception, before=None, after=None, file=None):
            future = self.run_in_executor(alchemy_incendiary(self._render_exc_sync, (exception, before, after, file),))
            future.__silence__()
            return future
        
        @classmethod
        def render_exc_maybe_async(cls, exception, before=None, after=None, file=None):
            local_thread = current_thread()
            if isinstance(local_thread, EventThread):
                future = local_thread.run_in_executor(alchemy_incendiary(cls._render_exc_sync,
                    (exception, before, after, file),))
                future.__silence__()
            else:
                cls._render_exc_sync(exception, before, after, file)
    
    else:
        def render_exc_async(self, exception, before=None, after=None, file=None):
            return self.run_in_executor(alchemy_incendiary(self._render_exc_sync, (exception, before, after, file),))
        
        @classmethod
        def render_exc_maybe_async(cls, exception, before=None, after=None, file=None):
            local_thread = current_thread()
            if isinstance(local_thread, EventThread):
                local_thread.run_in_executor(alchemy_incendiary(cls._render_exc_sync,
                    (exception, before, after, file),))
            else:
                cls._render_exc_sync(exception, before, after, file)
    
    if DOCS_ENABLED:
        render_exc_async.__doc__ = (
        """
        Renders the given exception's traceback in a non blocking way.
        
        Parameters
        ----------
        exception : ``BaseException``
            The exception to render.
        before : `None` or `str`, `list` of `str`, Optional
            Any content, what should go before the exception's traceback.
            
            If given as `str`, or if `list`, then the last element of it should end with linebreak.
        after : `None` or `str`, `list` of `str`, Optional
            Any content, what should go after the exception's traceback.
            
            If given as `str`, or if `list`, then the last element of it should end with linebreak.

        file : `None` or `I/O stream`, Optional
            The file to print the stack to. Defaults to `sys.stderr`.
        
        Returns
        -------
        future : ``Future``
            Returns a future, what can be awaited to wait for the rendering to be done.
        """)
    
    if DOCS_ENABLED:
        render_exc_maybe_async.__doc__ = (
        """
        Renders the given exception's traceback. If called from an ``EventThread`` instance, then will not block it.
        
        This method is called from function or methods, where being on an ``EventThread`` is not guaranteed.
        
        Parameters
        ----------
        exception : ``BaseException``
            The exception to render.
        before : `None` or `str`, `list` of `str`, Optional
            Any content, what should go before the exception's traceback.
            
            If given as `str`, or if `list`, then the last element of it should end with linebreak.
        after : `None` or `str`, `list` of `str`, Optional
            Any content, what should go after the exception's traceback.
            
            If given as `str`, or if `list`, then the last element of it should end with linebreak.

        file : `None` or `I/O stream`, Optional
            The file to print the stack to. Defaults to `sys.stderr`.
        """)
    
    @staticmethod
    def _render_exc_sync(exception, before, after, file):
        """
        Renders the given exception in a blocking way.
        
        Parameters
        ----------
        exception : ``BaseException``
            The exception to render.
        before : `str`, `list` of `str`
            Any content, what should go before the exception's traceback.
            
            If given as `str`, or if `list`, then the last element of it should end with linebreak.
        after : `str`, `list` of `str`
            Any content, what should go after the exception's traceback.
            
            If given as `str`, or if `list`, then the last element of it should end with linebreak.
        file : `None` or `I/O stream`
            The file to print the stack to. Defaults to `sys.stderr`.
        """
        extracted = []
        
        if before is None:
            pass
        elif isinstance(before, str):
            extracted.append(before)
        elif isinstance(before, list):
            for element in before:
                if type(element) is str:
                    extracted.append(element)
                else:
                    extracted.append(repr(element))
                    extracted.append('\n')
        else:
            # ignore exception cases
            extracted.append(repr(before))
            extracted.append('\n')
        
        render_exc_to_list(exception, extend=extracted)
        
        if after is None:
            pass
        elif isinstance(after, str):
            extracted.append(after)
        elif isinstance(after, list):
            for element in after:
                if type(element) is str:
                    extracted.append(element)
                else:
                    extracted.append(repr(element))
                    extracted.append('\n')
        else:
            extracted.append(repr(after))
            extracted.append('\n')
        
        if file is None:
            # ignore exception cases
            file = sys.stderr
        
        file.write(''.join(extracted))
    
    def stop(self):
        """
        Stops the event loop. Thread safe.
        """
        if self.should_run:
            if current_thread() is self:
                self._stop()
            else:
                self.call_soon(self._stop)
                self.wake_up()

    def _stop(self):
        """
        Stops the event loop. Internal function of ``.stop``, called or queued up by it.
        
        Should be called only from the thread of the event loop.
        """
        self.release_executors()
        self.should_run = False

    async def shutdown_async_generators(self):
        """
        Shuts down the asynchronous generators running on the event loop.
        
        This method is a coroutine.
        """
        self._async_generators_shutdown_called = True
        
        async_generators = self._async_generators
        if async_generators:
            return
        
        closing_async_generators = list(async_generators)
        async_generators.clear()
        
        results = await Gatherer(self, (ag.aclose() for ag in closing_async_generators))
        
        for result, async_generator in zip(results, closing_async_generators):
            exception = result.exception
            if (exception is not None) and (type(exception) is not CancelledError):
                extracted = [
                    'Exception occurred during shutting down async generator:\n',
                    repr(async_generator),
                        ]
                render_exc_to_list(exception, extend=extracted)
                sys.stderr.write(''.join(extracted))
    
    def _make_socket_transport(self, socket, protocol, waiter=None, *, extra=None, server=None):
        """
        Creates a socket transport with the given parameters.
        
        Parameters
        ----------
        socket : `socket.socket`
            The socket, what the transport will use.
        protocol : `Any`
            The protocol of the transport.
        waiter : `None` or ``Future``, Optional
            Waiter, what's result should be set, when the transport is ready to use.
        extra : `None` or `dict` of (`str`, `Any`) item, Optional (Keyword only)
            Optional transport information.
        server : `None` or ``Server``, Optional (Keyword only)
            The server to what the created socket will be attached to.
        
        Returns
        -------
        transport : ``_SelectorSocketTransport``
        """
        return _SelectorSocketTransport(self, socket, protocol, waiter, extra, server)
    
    def _make_ssl_transport(self, socket, protocol, ssl, waiter=None, *, server_side=False, server_hostname=None,
            extra=None, server=None):
        """
        Creates an ssl transport with the given parameters.
        
        Parameters
        ----------
        socket : `socket.socket`
            The socket, what the transport will use.
        protocol : `Any`
            Asynchronous protocol implementation for the transport. The given protocol is wrapped into an ``SSLProtocol``
        ssl : ``ssl.SSLContext``
            Ssl context of the respective connection.
        waiter : `None` or ``Future``, Optional
            Waiter, what's result should be set, when the transport is ready to use.
        server_side : `bool`, Optional (Keyword only)
            Whether the created ssl transport is a server side. Defaults to `False`.
        server_hostname : `None` or `str`, Optional (Keyword only)
            Overwrites the hostname that the target server’s certificate will be matched against.
            By default the value of the host parameter is used. If host is empty, there is no default and you must pass
            a value for `server_hostname`. If `server_hostname` is an empty string, hostname matching is disabled
            (which is a serious security risk, allowing for potential man-in-the-middle attacks).
        extra : `None` or `dict` of (`str`, `Any`) item, Optional (Keyword only)
            Optional transport information.
        server : `None` or ``Server``, Optional (Keyword only)
            The server to what the created socket will be attached to.
        
        Returns
        -------
        transport : ``_SSLProtocolTransport``
            The created ssl transport.
        """
        ssl_protocol = SSLProtocol(self, protocol, ssl, waiter, server_side, server_hostname)
        _SelectorSocketTransport(self, socket, ssl_protocol, extra=extra, server=server)
        return ssl_protocol.app_transport
    
    def empty_self_socket(self):
        """
        Reads all the data out from self socket.
        
        Familiar to async-io event loop's `._read_from_self`.
        """
        while True:
            try:
                data = self._self_read_socket.recv(4096)
                if not data:
                    break
            except InterruptedError:
                continue
            except BlockingIOError:
                break
    
    def wake_up(self):
        """
        Wakes up the event loop. Thread safe.
        
        Familiar as async-io event loop's `._write_to_self`.
        """
        self_write_socket = self._self_write_socket
        if self_write_socket is None:
            if self.running:
                return
            
            # If we start it not needed to wake_up. If we don't, we wont wake_up anyway.
            self._maybe_start()
            return
        
        try:
            self_write_socket.send(b'\0')
        except OSError:
            pass

    def _start_serving(self, protocol_factory, socket, ssl=None, server=None, backlog=100):
        """
        Starts serving the given socket on the event loop. Called by ``Server.start``. Adds a reader callback for the
        socket, what will call ``._accept_connection``. (At edge cases ``._accept_connection`` might call this
        method as well for repeating itself after a a delay.)
        
        Parameters
        ----------
        protocol_factory : `callable`
            Factory function for creating an asynchronous compatible protocol.
        socket : `socket.socket`
            The sockets to serve by the respective server if applicable.
        ssl : `None` or `ssl.SSLContext`, Optional
            To enable ssl for the connections, give it as  `ssl.SSLContext`.
        server : `None` or ``Server``, Optional
            The respective server, what started to serve if applicable.
        backlog : `int`, Optional
            The maximum number of queued connections passed to `listen()` (defaults to 100).
        """
        self.add_reader(socket.fileno(), self._accept_connection, protocol_factory, socket, ssl, server, backlog)
    
    def _stop_serving(self, socket):
        """
        Stops serving the given socket. by removing it's reader callback and closing it.
        
        Parameters
        ----------
        socket : `socket.socket`
            The socket, what's respective reader callback will be removed if applicable.
        """
        self.remove_reader(socket.fileno())
        socket.close()
    
    def _accept_connection(self, protocol_factory, socket, ssl, server, backlog):
        """
        Callback added by ``._start_serving``, what is triggered by a read event. This method is only called once for
        each event loop tick. There may be multiple connections waiting for an `.accept()` so it is called in a loop.
        See `https://bugs.python.org/issue27906` for more details.
        
        Parameters
        ----------
        protocol_factory : `callable`
            Factory function for creating an asynchronous compatible protocol.
        socket : `socket.socket`
            The sockets to serve by the respective server if applicable.
        ssl : `None` or `ssl.SSLContext`
            The ssl type of the connection if any.
        server : `None` or ``Server``
            The respective server if applicable.
        backlog : `int`, Optional
            The maximum number of queued connections passed to `listen()`.
        """
        for _ in range(backlog):
            try:
                connection_socket, address = socket.accept()
                connection_socket.setblocking(False)
            except (BlockingIOError, InterruptedError, ConnectionAbortedError):
                # Early exit because the socket accept buffer is empty.
                return None
            except OSError as err:
                # There's nowhere to send the error, so just log it.
                if err.errno in (errno.EMFILE, errno.ENFILE, errno.ENOBUFS, errno.ENOMEM):
                    # Some platforms (e.g. Linux keep reporting the FD as ready, so we remove the read handler
                    # temporarily. We'll try again in a while.
                    self.render_exc_async(err, before=[
                        'Exception occurred at',
                        repr(self),
                        '._accept_connection\n',
                            ])
                    
                    self.remove_reader(socket.fileno())
                    self.call_later(1., self._start_serving, protocol_factory, socket, ssl, server, backlog)
                else:
                    raise # The event loop will catch and log it.
            else:
                extra = {'peername': address}
                coro = self._accept_connection_task(protocol_factory, connection_socket, extra, ssl, server)
                Task(coro, self)
    
    async def _accept_connection_task(self, protocol_factory, connection_socket, extra, ssl, server):
        """
        Called by ``._accept_connection``, when a connection is accepted.
        
        Because ``._accept_connection`` might have more connections to accept, multiple tasks are launched up from
        this method to run parallelly.
        
        This method is a coroutine.
        
        Parameters
        ----------
        protocol_factory : `callable`
            Factory function for creating an asynchronous compatible protocol.
        connection_socket : `socket.socket`
            The accepted connection.
        extra : `None` or `dict` of (`str`, `Any`) item
            Optional transport information.
        ssl : `None` or `ssl.SSLContext`
            The ssl type of the connection if any.
        server : `None` or ``Server``
            The respective server if applicable.
        """
        try:
            protocol = protocol_factory()
            waiter = Future(self)
            if (ssl is None):
                transport = self._make_socket_transport(connection_socket, protocol, waiter=waiter, extra=extra,
                    server=server)
            else:
                transport = self._make_ssl_transport(connection_socket, protocol, ssl, waiter=waiter, server_side=True,
                    extra=extra, server=server)
            
            try:
                await waiter
            except:
                transport.close()
                raise
        
        except BaseException as err:
            self.render_exc_async(err, [
                'Exception occurred at ',
                self.__class__.__name__,
                '._accept_connection2\n',
                    ])
    
    def add_reader(self, fd, callback, *args):
        """
        Registers read callback for the given fd.
        
        Parameters
        ----------
        fd : `int`
            The respective file descriptor.
        callback : `callable`
            The function, what is called, when data is received on the respective file descriptor.
        *args : Parameters
            Parameters to call `callback` with.
        """
        if not self.running:
            if not self._maybe_start():
                raise RuntimeError('Event loop stopped.')
        
        handle = Handle(callback, args)
        try:
            key = self.selector.get_key(fd)
        except KeyError:
            self.selector.register(fd, EVENT_READ, (handle, None))
        else:
            mask = key.events
            reader, writer = key.data
            self.selector.modify(fd, mask|EVENT_READ, (handle, writer))
            if reader is not None:
                reader.cancel()
    
    def remove_reader(self, fd):
        """
        Removes a read callback for the given fd.
        
        Parameters
        ----------
        fd : `int`
            The respective file descriptor.
        
        Returns
        -------
        removed : `bool`
            Whether a reader callback was removed.
        """
        if not self.running:
            if not self._maybe_start():
                return False
        
        try:
            key = self.selector.get_key(fd)
        except KeyError:
            return False
        
        mask = key.events
        reader, writer = key.data
        mask &= ~EVENT_READ
        
        if mask:
            self.selector.modify(fd, mask, (None, writer))
        else:
            self.selector.unregister(fd)
        
        if reader is not None:
            reader.cancel()
            return True
        
        return False
    
    def add_writer(self, fd, callback, *args):
        """
        Registers a write callback for the given fd.
        
        Parameters
        ----------
        fd : `int`
            The respective file descriptor.
        callback : `callable`
            The function, what is called, when data the respective file descriptor becomes writable.
        *args : Parameters
            Parameters to call `callback` with.
        """
        if not self.running:
            if not self._maybe_start():
                raise RuntimeError('Event loop is cancelled.')
        
        handle = Handle(callback, args)
        try:
            key = self.selector.get_key(fd)
        except KeyError:
            self.selector.register(fd, EVENT_WRITE, (None, handle))
            return
        
        mask = key.events
        reader, writer = key.data
        
        self.selector.modify(fd, mask|EVENT_WRITE, (reader, handle))
        if writer is not None:
            writer.cancel()
    
    def remove_writer(self, fd):
        """
        Removes a write callback for the given fd.
        
        Parameters
        ----------
        fd : `int`
            The respective file descriptor.
        
        Returns
        -------
        removed : `bool`
            Whether a writer callback was removed.
        """
        if not self.running:
            if not self._maybe_start():
                return False
        
        try:
            key = self.selector.get_key(fd)
        except KeyError:
            return False
        
        mask = key.events
        reader, writer = key.data
        # remove both writer and connector.
        mask &= ~EVENT_WRITE
        if mask:
            self.selector.modify(fd, mask, (reader, None))
        else:
            self.selector.unregister(fd)
            
        if writer is not None:
            writer.cancel()
            return True
        
        return False
    
    async def connect_accepted_socket(self, protocol_factory, socket, *, ssl=None):
        """
        Wrap an already accepted connection into a transport/protocol pair.
        
        This method can be used by servers that accept connections outside of hata but use it to handle them.
        
        This method is a coroutine.
        
        Parameters
        ----------
        protocol_factory : `callable`.
            Callable returning an asynchronous protocol implementation.
        socket : `socket.socket`
            A preexisting socket object returned from `socket.accept`.
        ssl : `None` or `ssl.SSLContext`, Optional (Keyword only)
            Whether ssl should be enabled.
        
        Returns
        -------
        transport : ``_SSLProtocolTransport`` or ``_SelectorSocketTransport``
            The created transport. If `ssl` is enabled, creates ``_SSLProtocolTransport``, else
            ``_SelectorSocketTransport``.
        protocol : `Any`
            The protocol returned by `protocol_factory`.
        
        Raises
        ------
        ValueError
            If `socket` is not a stream socket.
        """
        if not _is_stream_socket(socket):
            raise ValueError(f'A stream socket was expected, got {socket!r}.')
        
        return await self._create_connection_transport(socket, protocol_factory, ssl, '', True)
    
    async def create_connection(self, protocol_factory, host=None, port=None, *, ssl=None, family=0, protocol=0,
            flags=0, socket=None, local_address=None, server_hostname=None):
        """
        Open a streaming transport connection to a given address specified by `host` and `port`.
        
        This method is a coroutine.
        
        Parameters
        ----------
        protocol_factory : `callable`.
            Callable returning an asynchronous protocol implementation.
        host : `None` or `str`, Optional
            To what network interfaces should the connection be bound.
            
            Mutually exclusive with the `socket` parameter.
        port : `None` or `int`, Optional
            The port of the `host`.
            
            Mutually exclusive with the `socket` parameter.
        ssl : `None`, `bool` or `ssl.SSLContext`, Optional (Keyword only)
            Whether ssl should be enabled.
        family : `AddressFamily` or `int`, Optional (Keyword only)
            Can be either `AF_INET`, `AF_INET6` or `AF_UNIX`.
        protocol : `int`, Optional (Keyword only)
            Can be used to narrow host resolution. Is passed to ``.get_address_info``.
        flags : `int`, Optional (Keyword only)
            Can be used to narrow host resolution. Is passed to ``.get_address_info``.
        socket : `None` or `socket.socket`, Optional (Keyword only)
            Whether should use an existing, already connected socket.
            
            Mutually exclusive with the `host` and the `port` parameters.
        local_address : `tuple` of (`None` or  `str`, `None` or `int`), Optional (Keyword only)
            Can be given as a `tuple` (`local_host`, `local_port`) to bind the socket locally. The `local_host` and
            `local_port` are looked up by ``.get_address_info``.
        server_hostname : `None` or `str`, Optional (Keyword only)
            Overwrites the hostname that the target server’s certificate will be matched against.
            Should only be passed if `ssl` is not `None`. By default the value of the host parameter is used. If host
            is empty, there is no default and you must pass a value for `server_hostname`. If `server_hostname` is an
            empty string, hostname matching is disabled (which is a serious security risk, allowing for potential
            man-in-the-middle attacks).
        
        Returns
        -------
        transport : ``_SSLProtocolTransport`` or ``_SelectorSocketTransport``
            The created transport. If `ssl` is enabled, creates ``_SSLProtocolTransport``, else
            ``_SelectorSocketTransport``.
        protocol : `Any`
            The protocol returned by `protocol_factory`.
        
        Raises
        ------
        ValueError
            - If `host` or `port` is given meanwhile `socket` is also specified.
            - If `server_hostname` is not set, meanwhile using `ssl` without `host`.
            - If `server_hostname` is set, but `ssl` is.
            - If neither `host`, `port` or `socket` are specified.
            - `socket` is given, but not as a stream socket.
        OSError
            - `get_address_info()` returned empty list.
            - Error while attempting to bind to address.
            - Cannot open connection to any address.
        """
        if isinstance(ssl, bool):
            if ssl:
                ssl = create_default_context()
            else:
                ssl = None
        
        if (server_hostname is None):
            if (ssl is not None):
                # Use host as default for server_hostname. It is an error if host is empty or not set, e.g. when an
                # already-connected socket was passed or when only a port is given.  To avoid this error, you can pass
                # server_hostname='' -- this will bypass the hostname check. (This also means that if host is a numeric
                # IP/IPv6 address, we will attempt to verify that exact address; this will probably fail, but it is
                # possible to create a certificate for a specific IP address, so we don't judge it here.)
                if host is None:
                    raise ValueError('You must set `server_hostname` when using `ssl` without a `host`.')
                server_hostname = host
        else:
            if ssl is None:
                raise ValueError('`server_hostname` is only meaningful with `ssl`.')
        
        if (host is not None) or (port is not None):
            if (socket is not None):
                raise ValueError('`host`, `port` and `socket` can not be specified at the same time.')
            
            f1 = self._ensure_resolved((host, port), family=family, type=module_socket.SOCK_STREAM, protocol=protocol,
                flags=flags)
            fs = [f1]
            if local_address is not None:
                f2 = self._ensure_resolved(local_address, family=family, type=module_socket.SOCK_STREAM,
                    protocol=protocol, flags=flags)
                fs.append(f2)
            else:
                f2 = None
            
            await Gatherer(self, fs)
            
            infos = f1.result()
            if not infos:
                raise OSError('`get_address_info` returned empty list')
            if (f2 is not None):
                local_address_infos = f2.result()
                if not local_address_infos:
                    raise OSError('`get_address_info` returned empty list')
            
            exceptions = []
            for family, type_, protocol, canonical_name, address in infos:
                try:
                    socket = module_socket.socket(family=family, type=type_, proto=protocol)
                    socket.setblocking(False)
                    if (f2 is not None):
                        for element in local_address_infos:
                            local_address = element[4]
                            try:
                                socket.bind(local_address)
                                break
                            except OSError as err:
                                err = OSError(err.errno, f'Error while attempting to bind on address '
                                    f'{local_address!r}: {err.strerror.lower()}.')
                                exceptions.append(err)
                        else:
                            socket.close()
                            socket = None
                            continue
                    
                    await self.socket_connect(socket, address)
                except OSError as err:
                    if (socket is not None):
                        socket.close()
                    exceptions.append(err)
                except:
                    if (socket is not None):
                        socket.close()
                    raise
                else:
                    break
            else:
                if len(exceptions) == 1:
                    raise exceptions[0]
                else:
                    # If they all have the same str(), raise one.
                    model = repr(exceptions[0])
                    all_exception = [repr(exception) for exception in exceptions]
                    if all(element == model for element in all_exception):
                        raise exceptions[0]
                    # Raise a combined exception so the user can see all the various error messages.
                    raise OSError(f'Multiple exceptions: {", ".join(all_exception)}')
        
        else:
            if socket is None:
                raise ValueError('`host` and `port`, neither `socket` was given.')
            
            if not _is_stream_socket(socket):
                raise ValueError(f'A stream socket was expected, got {socket!r}.')
        
        return await self._create_connection_transport(socket, protocol_factory, ssl, server_hostname, False)
    
    
    async def _create_connection_transport(self, socket, protocol_factory, ssl, server_hostname, server_side):
        """
        Open a streaming transport connection to a given address specified by `host` and `port`.
        
        This method is a coroutine.
        
        Parameters
        ----------
        protocol_factory : `callable`.
            Callable returning an asynchronous protocol implementation.
        ssl : `None`, `ssl.SSLContext`
            Whether ssl should be enabled.
        socket : `socket.socket`
            The socket to what the created transport should be connected to.
        server_hostname : `None` or `str`
            Overwrites the hostname that the target server’s certificate will be matched against.
            Should only be passed if `ssl` is not `None`. By default the value of the host parameter is used. If host
            is empty, there is no default and you must pass a value for `server_hostname`. If `server_hostname` is an
            empty string, hostname matching is disabled (which is a serious security risk, allowing for potential
            man-in-the-middle attacks).
        server_side : `bool`
            Whether the server or the client creates the connection transport.
        
        Returns
        -------
        transport : ``_SSLProtocolTransport`` or ``_SelectorSocketTransport``
            The created transport. If `ssl` is enabled, creates ``_SSLProtocolTransport``, else
            ``_SelectorSocketTransport``.
        protocol : `Any`
            The protocol returned by `protocol_factory`.
        """
        socket.setblocking(False)
        
        protocol = protocol_factory()
        waiter = Future(self)
        
        if ssl is None:
            transport = self._make_socket_transport(socket, protocol, waiter)
        else:
            transport = self._make_ssl_transport(socket, protocol, ssl, waiter, server_side=server_side,
                server_hostname=server_hostname)
        
        try:
            await waiter
        except:
            transport.close()
            raise
        
        return transport, protocol
    
    if IS_UNIX:
        async def create_unix_connection(self, protocol_factory, path=None, *, socket=None, ssl=None,
                server_hostname=None):
            if (ssl is None):
                if server_hostname is not None:
                    raise ValueError('`server_hostname` is only meaningful with `ssl`.')
            else:
                if server_hostname is None:
                    raise ValueError('`server_hostname` parameter is required with `ssl`.')
            
            if path is not None:
                if socket is not None:
                    raise ValueError('`path` and `socket` parameters are mutually exclusive.')
                
                path = os.fspath(path)
                socket = module_socket.socket(module_socket.AF_UNIX, module_socket.SOCK_STREAM, 0)
                
                try:
                    socket.setblocking(False)
                    await self.socket_connect(socket, path)
                except:
                    socket.close()
                    raise
            
            else:
                if socket is None:
                    raise ValueError('Either `socket` or `path` parameters are required.')
                
                if socket.family not in (module_socket.AF_UNIX, module_socket.SOCK_STREAM):
                    raise ValueError(f'A UNIX Domain Stream Socket was expected, got {socket!r}.')
                
                socket.setblocking(False)
            
            return await self._create_connection_transport(socket, protocol_factory, ssl, server_hostname, False)
        
        
        async def open_unix_connection(self, path=None, **kwargs):
            protocol = ProtocolBase(self)
            await self.create_unix_connection(protocol, path, **kwargs)
            return protocol
        
        
        async def create_unix_server(self, protocol_factory, path=None, *, socket=None, backlog=100, ssl=None,):
            if (ssl is not None) and (not isinstance(ssl, ssl.SSlContext)):
                raise TypeError(f'`ssl` can be given as `None` or as ``SSLContext``, got {ssl.__class__.__name__}.')
            
            if path is not None:
                if socket is not None:
                    raise ValueError('`path` and `socket` parameters are mutually exclusive.')
                
                path = os.fspath(path)
                socket = module_socket.socket(module_socket.AF_UNIX, module_socket.SOCK_STREAM)
                
                # Check for abstract socket.
                if not path.startswith('\x00'):
                    try:
                        if S_ISSOCK(os.stat(path).st_mode):
                            os.remove(path)
                    except FileNotFoundError:
                        pass
                
                try:
                    socket.bind(path)
                except OSError as exc:
                    socket.close()
                    if exc.errno == errno.EADDRINUSE:
                        # Let's improve the error message by adding  with what exact address it occurs.
                        raise OSError(errno.EADDRINUSE, f'Address {path!r} is already in use.') from None
                    else:
                        raise
                except:
                    socket.close()
                    raise
            else:
                if socket is None:
                    raise ValueError('Either `path` or `socket` parameter is required.')
                
                if socket.family not in (module_socket.AF_UNIX, module_socket.SOCK_STREAM):
                    raise ValueError(f'A UNIX Domain Stream Socket was expected, got {socket!r}.')
            
            socket.setblocking(False)
            
            return Server(self, [socket], protocol_factory, ssl, backlog)
        
    else:
        async def create_unix_connection(self, protocol_factory, path=None, *, socket=None, ssl=None,
                server_hostname=None):
            raise NotImplementedError
        
        
        async def open_unix_connection(self, path=None, **kwargs):
            raise NotImplementedError
    
    
        async def create_unix_server(self, protocol_factory, path=None, *, socket=None, backlog=100, ssl=None,):
            raise NotImplementedError
    
    
    set_docs(create_unix_connection,
        """
        Establish a unix socket connection.
        
        This method is a coroutine.
        
        Parameters
        ----------
        protocol_factory : `callable`.
            Callable returning an asynchronous protocol implementation.
        path : `None` or `str`, Optional
            The path to open connection to.
        socket : `socket.socket`, Optional (Keyword only)
            A preexisting socket object to use up.
            
            Mutually exclusive with the `path` parameter.
        ssl : `None` or `ssl.SSLContext`, Optional (Keyword only)
            Whether ssl should be enabled.
        server_hostname : `None` or `str`
            Overwrites the hostname that the target server’s certificate will be matched against.
            Should only be passed if `ssl` is not `None`. By default the value of the host parameter is used. If hos
            is empty, there is no default and you must pass a value for `server_hostname`. If `server_hostname` is an
            empty string, hostname matching is disabled (which is a serious security risk, allowing for potential
            man-in-the-middle attacks).
        
        Returns
        -------
        transport : ``_SSLProtocolTransport`` or ``_SelectorSocketTransport``
            The created transport. If `ssl` is enabled, creates ``_SSLProtocolTransport``, else
            ``_SelectorSocketTransport``.
        protocol : `Any`
            The protocol returned by `protocol_factory`.
        
        Raises
        ------
        ValueError
            - If `server_hostname` parameter is given, but `ssl` isn't.
            - If `ssl` parameter is given, but `server_hostname` is not.
            - If `path` parameter is given, when `socket` is defined as well.
            - If neither `path` and `socket` parameters are given.
            - If `socket`'s is not an unix domain stream socket.
        NotImplementedError
            Not supported on windows by the library.
        """)
    
    set_docs(open_unix_connection,
        """
        Creates an unix connection.
        
        This method is a coroutine.
        
        Parameters
        ----------
        path : `None` or `str`, Optional
            The path to open connection to.
        **kwargs : Keyword parameters
            Additional keyword parameters to pass to ``.create_unix_connection``.
        
        Other Parameters
        ----------------
        socket : `socket.socket`, Optional (Keyword only)
            A preexisting socket object to use up.
            
            Mutually exclusive with the `path` parameter.
        ssl : `None` or `ssl.SSLContext`, Optional (Keyword only)
            Whether ssl should be enabled.
        server_hostname : `None` or `str`
            Overwrites the hostname that the target server’s certificate will be matched against.
            Should only be passed if `ssl` is not `None`. By default the value of the host parameter is used. If hos
            is empty, there is no default and you must pass a value for `server_hostname`. If `server_hostname` is an
            empty string, hostname matching is disabled (which is a serious security risk, allowing for potential
            man-in-the-middle attacks).
        
        Returns
        -------
        protocol : ``BaseProtocol``
            The connected read and write protocol.
        
        Raises
        ------
        ValueError
            - If `server_hostname` parameter is given, but `ssl` isn't.
            - If `ssl` parameter is given, but `server_hostname` is not.
            - If `path` parameter is given, when `socket` is defined as well.
            - If neither `path` and `socket` parameters are given.
            - If `socket`'s is not an unix domain stream socket.
        NotImplementedError
            Not supported on windows by the library.
        """)
    
    set_docs(create_unix_server,
        """
        Creates an unix server (socket type AF_UNIX) listening on the given path.
        
        This method is a coroutine.
        
        Parameters
        ----------
        protocol_factory : `callable`
            Factory function for creating a protocols.
        path : `None` or `str`
            The path to open connection to.
        socket : `None` or `socket.socket`, Optional (Keyword only)
            Can be specified in order to use a preexisting socket object.
            
            Mutually exclusive with the `path` parameter.
        backlog : `int`, Optional (Keyword only)
            The maximum number of queued connections passed to `listen()` (defaults to 100).
        ssl : `None` or ``SSLContext``, Optional (Keyword only)
            Whether and what ssl is enabled for the connections.
        
        Returns
        -------
        server : ``Server``
            The created server instance.
        
        Raises
        ------
        TypeError
            - If `ssl` is not given neither as `None` nor as `ssl.SSLContext` instance.
        ValueError
            - If both `path` and `socket` parameters are given.ó
            - If neither `path` nor `socket` were given.
            - If `socket` is given, but it's type is not `module_socket.SOCK_STREAM`.
        FileNotFoundError:
            The given `path` do not exists.
        OsError
            - Path already in use.
            - Error while attempting to connect to `path`.
        NotImplementedError
            Not supported on windows by the library.
        """)
    
    
    # await it
    def get_address_info(self, host, port, *, family=0, type=0, protocol=0, flags=0):
        """
        Asynchronous version of `socket.getaddrinfo()`.
        
        Parameters
        ----------
        host : `None` or `str`
            To respective network interface.
        port : `None` or `int`
            The port of the `host`.
        family :  `AddressFamily` or `int`, Optional (Keyword only)
            The address family.
        type : `SocketKind` or `int`, Optional (Keyword only)
            Socket type.
        protocol : `int`, Optional (Keyword only)
            Protocol type. Can be used to narrow host resolution.
        flags : `int`, Optional (Keyword only)
            Can be used to narrow host resolution.
        
        Returns
        -------
        future : ``Future``
            An awaitable future, what will yield the lookup's result.
            
            Might raise `OSError` or return a `list` of `tuple`-s with the following elements:
            - `family` : `AddressFamily` or `int`. Address family.
            - `type` : `SocketKind` or `int`. Socket type.
            - `protocol` : `int`. Protocol type.
            - `canonical_name` : `str`. Represents the canonical name of the host.
            - `socket_address` : `tuple` (`str, `int`). Socket address containing the `host` and the `port`.
        """
        return self.run_in_executor(alchemy_incendiary(
            module_socket.getaddrinfo, (host, port, family, type, protocol, flags,),))
    
    # await it
    def get_name_info(self, socket_address, flags=0):
        """
        Asynchronous version of `socket.getnameinfo()`.
        
        Parameters
        ----------
        socket_address : `tuple` (`str`, `int`)
             Socket address as a tuple of `host` and `port`.
        flags : `int`, Optional
            Can be used to narrow host resolution.
        
        Returns
        -------
        future : ``Future``
            An awaitable future, what will yield the lookup's result.
        """
        return self.run_in_executor(alchemy_incendiary(module_socket.getnameinfo, (socket_address, flags,),))
    
    def _ensure_resolved(self, address, *, family=0, type=module_socket.SOCK_STREAM, protocol=0, flags=0):
        """
        Ensures, that the given address is already a resolved IP. If not, gets it's address.
        
        Parameters
        ----------
        address : `tuple` (`None` or `str`, `None` or `int`)
            Address as a tuple of `host` and `port`.
        type : `SocketKind` or `int`, Optional
            Socket type.
        protocol : `int`, Optional
            Protocol type. Can be used to narrow host resolution.
        flags : `int`, Optional
            Can be used to narrow host resolution.
        
        Returns
        -------
        future : ``Future``
            An awaitable future, what returns a `list` of `tuples` with the following elements:
            
            - `family` : `AddressFamily` or `int`. Address family.
            - `type` : `SocketKind` or `int`. Socket type.
            - `protocol` : `int`. Protocol type.
            - `canonical_name` : `str`. Represents the canonical name of the host.
            - `socket_address` : `tuple` (`str, `int`). Socket address containing the `host` and the `port`.
            
            Might raise `OSError` as well.
        """
        # Address might have more than 2 elements?
        host = address[0]
        port = address[1]
        
        info = _ip_address_info(host, port, family, type, protocol)
        if info is None:
            return self.get_address_info(host, port, family=family, type=type, protocol=protocol, flags=flags)
        
        # "host" is already a resolved IP.
        future = Future(self)
        future.set_result([info])
        return future
    
    async def socket_accept(self, socket):
        """
        Accept a connection. Modeled after the blocking `socket.accept()` method.
        
        The socket must be bound to an address and listening for connections.
        
        This method is a coroutine.
        
        Parameters
        ----------
        socket : `socket.socket`
            Must be a non-blocking socket.
        
        Returns
        -------
        conn : `socket.socket`
            The connected socket.
        address : `tuple` (`str`, `int`)
            The address to what the connection is connected to.
        """
        future = Future(self)
        self._socket_accept(future, False, socket)
        return await future

    def _socket_accept(self, future, registered, socket):
        """
        Method used by ``.socket_accept`` to check whether the respective socket can be accepted already.
        
        If the respective socket is already connected, then sets the waiter future's result instantly, else adds itself
        as a reader callback.
        
        Parameters
        ----------
        future : ``Future``
            Waiter future, what's result or exception is set, when the socket can be accepted or when an exception
            occurs.
        registered : `bool`
            Whether the given `socket is registered as a reader and should be removed.
        socket : `socket.socket`
            The respective socket, what's is listening for a connection.
        """
        fd = socket.fileno()
        if registered:
            self.remove_reader(fd)
            
            # First time `registered` is given as `False` and at the case, the `future` can not be cancelled yet.
            # Later it is called with `True`.
            if future.cancelled():
                return
        
        try:
            conn, address = socket.accept()
            conn.setblocking(False)
        except (BlockingIOError, InterruptedError):
            self.add_reader(fd, self._socket_accept, future, True, socket)
        except BaseException as err:
            future.set_exception(err)
        else:
            future.set_result((conn, address))
            
    async def socket_connect(self, socket, address):
        """
        Connect the given socket to a remote socket at address.
        
        Asynchronous version of `socket.connect`.
        
        This method is a coroutine.
        
        Parameters
        ----------
        socket : `socket.socket`
            Must be a non-blocking socket.
        address : `tuple` (`str`, `int`)
            The address to connect to.
        """
        if not hasattr(module_socket, 'AF_UNIX') or (socket.family != module_socket.AF_UNIX):
            resolved = self._ensure_resolved(address, family=socket.family, protocol=socket.proto)
            if not resolved.done():
                await resolved
            address = resolved.result()[0][4]
        
        future = Future(self)
        
        fd = socket.fileno()
        try:
            socket.connect(address)
        except (BlockingIOError, InterruptedError):
            # Cpython issue #23618: When the C function connect() fails with EINTR, the connection runs in background.
            # We have to wait until the socket becomes writable to be notified when the connection succeed or fails.
            self.add_writer(fd, self._socket_connect_cb, future, socket, address)
            future.add_done_callback(self._socket_connect_done(fd),)
        except BaseException as err:
            future.set_exception(err)
        else:
            future.set_result(None)
        
        await future
    
    class _socket_connect_done:
        """
        Callback added to the waited future by ``EventThread.socket_connect`` to remove the respective socket from the
        writers by it's file descriptor.
        
        Attributes
        ----------
        fd : `int`
            The respective socket's file descriptor's identifier.
        """
        __slots__ = ('fd',)
        
        def __init__(self, fd):
            """
            Creates a new ``_socket_connect_done`` instance with the given fd.
            
            Parameters
            ----------
            fd : `int`
                The respective socket's file descriptor's identifier.
            """
            self.fd = fd
        
        def __call__(self, future):
            """
            Callback what runs when the respective waiter future is marked as done.
            
            Removes the respective socket from writers.
            
            Parameters
            ----------
            future : ``Future``
                The respective future, what's result is set, when the respective connected.
            """
            future._loop.remove_writer(self.fd)
    
    def _socket_connect_cb(self, future, socket, address):
        """
        Reader callback, what is called, when the respective socket is connected. Added by ``.socket_connect``, when the
        socket is not yet connected.
        
        Parameters
        ----------
        future : ``Future``
            Waiter future, what's result is set, when the socket is connected.
        socket : `socket.socket`
            The respective socket, on what's connection we are waiting for.
        address : `tuple` (`str`, `int`)
            The address to connect to.
        """
        if future.done():
            return
        
        try:
            err_number = socket.getsockopt(module_socket.SOL_SOCKET, module_socket.SO_ERROR)
            if err_number != 0:
                raise OSError(err_number, f'Connect call failed {address!r}.')
        except (BlockingIOError, InterruptedError):
            # socket is still registered, the callback will be retried later
            pass
        except BaseException as err:
            future.set_exception(err)
        else:
            future.set_result(None)
    
    async def socket_receive(self, socket, n):
        """
        Receive up to `n` from the given socket. Asynchronous version of `socket.recv()`.
        
        This method is a coroutine.
        
        Parameters
        ----------
        socket : `socket.socket`
            The socket to receive the data from. Must be a non-blocking socket.
        n : `int`
            The amount of data to receive in bytes.
        
        Returns
        -------
        data : `bytes`
            The received data.
        
        Notes
        -----
        There is no way to determine how much data, if any was successfully received on the other end of the connection.
        """
        future = Future(self)
        self._socket_receive(future, False, socket, n)
        return await future

    def _socket_receive(self, future, registered, socket, n):
        """
        Added reader callback by ``.socket_receive``. This method is repeated till the data is successfully polled.
        
        Parameters
        ----------
        future : ``Future``
            Waiter future, what's result or exception will be set.
        registered : `bool`
            Whether `socket` is registered as a reader and should be removed.
        socket : `socket.socket`
            The socket from what we read.
        n : `int`
            The amount of data to receive in bytes.
        """
        fd = socket.fileno()
        if registered:
            self.remove_reader(fd)
        
        if future.cancelled():
            return
        
        try:
            data = socket.recv(n)
        except (BlockingIOError,InterruptedError):
            self.add_reader(fd, self._socket_receive, future, True, socket, n)
        except BaseException as err:
            future.set_exception(err)
        else:
            future.set_result(data)
    
    async def socket_send_all(self, socket, data):
        """
        Send data to the socket. Asynchronous version of `socket.sendall`.
        
        Continues sending to the socket until all data is sent or an error occurs.
        
        This method is a coroutine.
        
        Parameters
        ----------
        socket : `socket.socket`
            The socket to send the data to. Must be a non-blocking socket.
        data : `bytes-like`
            The data to send.
        
        Notes
        -----
        There is no way to determine how much data, if any was successfully received on the other end of the connection.
        """
        if type(data) is not memoryview:
            data = memoryview(data)
        
        if data:
            future = Future(self)
            self._socket_send_all(future, False, socket, data)
            await future
    
    def _socket_send_all(self, future, registered, socket, data):
        """
        Added writer callback by ``.socket_send_all``. This method is repeated till the whole data is exhausted.
        
        Parameters
        ----------
        future : ``Future``
            Waiter future, what's result or exception will be set.
        registered : `bool`
            Whether `socket` is registered as a writer and should be removed.
        socket : `socket.socket`
            The socket to what the data is sent to.
        data : `memoryview`
            Memoryview on the data to send.
        """
        fd = socket.fileno()
        
        if registered:
            self.remove_writer(fd)
        
        if future.done():
            return
        
        try:
            n = socket.send(data)
        except (BlockingIOError, InterruptedError):
            n = 0
        except BaseException as err:
            future.set_exception(err)
            return
        
        if n == len(data):
            future.set_result(None)
        else:
            if n:
                data = data[n:]
            
            self.add_writer(fd, self._socket_send_all, future, True, socket, data)
    
    async def create_datagram_endpoint(self, protocol_factory, local_address=None, remote_address=None, *, family=0,
            protocol=0, flags=0, reuse_port=False, allow_broadcast=False, socket=None):
        """
        Creates a datagram connection. The socket type will be `SOCK_DGRAM`.
        
        This method is a coroutine.
        
        Parameters
        ----------
        protocol_factory : `callable`
            Factory function for creating a protocols.
        local_address : `None`, `tuple` of (`None` or  `str`, `None` or `int`), `str`, `bytes`, Optional
            Can be given as a `tuple` (`local_host`, `local_port`) to bind the socket locally. The `local_host` and
            `local_port` are looked up by ``.get_address_info``.
            
            If `family` is given as `AF_UNIX`, then also can be given as path of a file or a file descriptor.
            
            Mutually exclusive with the `socket` parameter.
        remote_address : `None`, `tuple` of (`None` or  `str`, `None` or `int`), `str`, `bytes`, Optional
            Can be given as a `tuple` (`remote_host`, `remote_port`) to connect the socket to remove address. The
            `remote_host` and `remote_port` are looked up by ``.get_address_info``.
            
            If `family` is given as `AF_UNIX`, then also can be given as path of a file or a file descriptor.
            
            Mutually exclusive with the `socket` parameter.
        family : `AddressFamily` or `int`, Optional (Keyword only)
            Can be either `AF_INET`, `AF_INET6` or `AF_UNIX`.
            
            Mutually exclusive with the `socket` parameter.
        protocol : `int`, Optional (Keyword only)
            Can be used to narrow host resolution. Is passed to ``.get_address_info``.
            
            Mutually exclusive with the `socket` parameter.
        flags : `int`, Optional (Keyword only)
            Can be used to narrow host resolution. Is passed to ``.get_address_info``.
            
            Mutually exclusive with the `socket` parameter.
        reuse_port : `bool`, Optional (Keyword only)
            Tells to the kernel to allow this endpoint to be bound to the same port as an other existing endpoint
            already might be bound to.
            
            Not supported on Windows.
        allow_broadcast : `bool`, Optional (Keyword only)
            Tells the kernel to allow this endpoint to send messages to the broadcast address.
        socket : `None` or `socket.socket`, Optional (Keyword only)
            Can be specified in order to use a preexisting socket object.
            
            Mutually exclusive with `host` and `port` parameters.
        
        Returns
        -------
        transport : ``_SelectorDatagramTransport``
            The created datagram transport.
        protocol : `Any`
            The protocol returned by `protocol_factory`.
        """
        if socket is not None:
            if socket.type != module_socket.SOCK_DGRAM:
                raise ValueError(f'A UDP socket was expected, got {socket!r}.')
            
            if (local_address is not None) or (remote_address is not None) or family  or protocol or flags or \
                    reuse_port or allow_broadcast:
                
                collected = []
                if (local_address is not None):
                    collected.append(('local_address', local_address))
                
                if (remote_address is not None):
                    collected.append(('remote_address', remote_address))
                    
                if family:
                    collected.append(('family', family))
                
                if protocol:
                    collected.append(('protocol', protocol))
                
                if flags:
                    collected.append(('flags', flags))
                
                if reuse_port:
                    collected.append(('reuse_port', reuse_port))
                
                if allow_broadcast:
                    collected.append(('allow_broadcast', allow_broadcast))
                
                error_message_parts = ['Socket modifier keyword parameters can not be used when `socket` is given: ']
                
                index = 0
                limit = len(error_message_parts)
                while True:
                    name, value = collected[index]
                    error_message_parts.append(name)
                    error_message_parts.append('=')
                    error_message_parts.append(repr(value))
                    
                    index += 1
                    if index == limit:
                        break
                    
                    error_message_parts.append(', ')
                    continue
                
                error_message_parts.append('.')
                
                raise ValueError(''.join(error_message_parts))
            
            socket.setblocking(False)
            remote_address = None
        else:
            address_info = []
            
            if (local_address is None) and (remote_address is None):
                if family == 0:
                    raise ValueError(f'Unexpected address family: {family!r}.')
                
                address_info.append((family, protocol, None, None))
            
            elif hasattr(module_socket, 'AF_UNIX') and family == module_socket.AF_UNIX:
                if __debug__:
                    if (local_address is not None):
                        if not isinstance(local_address, (str, bytes)):
                            raise TypeError('`local_address` should be given as `None` or as `str` or `bytes` '
                                f'instance, if `family` is given as ``AF_UNIX`, got '
                                f'{local_address.__class__.__name__}')
                    
                    if (remote_address is not None):
                        if not isinstance(remote_address, (str, bytes)):
                            raise TypeError('`remote_address` should be given as `None` or as `str` or `bytes` '
                                f'instance, if `family` is given as ``AF_UNIX`, got '
                                f'{remote_address.__class__.__name__}')
                
                if (local_address is not None) and local_address and \
                        (local_address[0] != (0 if isinstance(local_address, bytes) else '\x00')):
                    try:
                        if S_ISSOCK(os.stat(local_address).st_mode):
                            os.remove(local_address)
                    except FileNotFoundError:
                        pass
                    except OSError as err:
                        # Directory may have permissions only to create socket.
                        sys.stderr.write(f'Unable to check or remove stale UNIX socket {local_address!r}: {err!s}.\n')
                
                address_info.append((family, protocol, local_address, remote_address))
            
            else:
                # join address by (family, protocol)
                address_infos = {}
                if (local_address is not None):
                    infos = await self._ensure_resolved(local_address, family=family, type=module_socket.SOCK_DGRAM,
                        protocol=protocol, flags=flags)
                    
                    if not infos:
                        raise OSError('`get_address_info` returned empty list')
                    
                    for it_family, it_type, it_protocol, it_canonical_name, it_socket_address in infos:
                        address_infos[(it_family, it_protocol)] = (it_socket_address, None)
                
                if (remote_address is not None):
                    infos = await self._ensure_resolved(remote_address, family=family, type=module_socket.SOCK_DGRAM,
                        protocol=protocol, flags=flags)
                    
                    if not infos:
                        raise OSError('`get_address_info` returned empty list')
                    
                    
                    for it_family, it_type, it_protocol, it_canonical_name, it_socket_address in infos:
                        key = (it_family, it_protocol)
                        
                        try:
                            value = address_infos[key]
                        except KeyError:
                            address_value_local = None
                        else:
                            address_value_local = value[0]
                        
                        address_infos[key] = (address_value_local, it_socket_address)
                
                for key, (address_value_local, address_value_remote) in address_infos.items():
                    if (local_address is not None) and (address_value_local is None):
                        continue
                    
                    if (remote_address is not None) and (address_value_remote is None):
                        continue
                    
                    address_info.append((*key, address_value_local, address_value_remote))
                
                if not address_info:
                    raise ValueError('Can not get address information.')
            
            exception = None
            
            for family, protocol, local_address, remote_address in address_info:
                try:
                    socket = module_socket.socket(family=family, type=module_socket.SOCK_DGRAM, proto=protocol)
                    
                    if reuse_port:
                        _set_reuse_port(socket)
                    
                    if allow_broadcast:
                        socket.setsockopt(module_socket.SOL_SOCKET, module_socket.SO_BROADCAST, 1)
                    
                    socket.setblocking(False)
                    
                    if (local_address is not None):
                        socket.bind(local_address)
                    
                    if (remote_address is not None):
                        if not allow_broadcast:
                            await self.socket_connect(socket, remote_address)
                
                except BaseException as err:
                    if (socket is not None):
                        socket.close()
                        socket = None
                    
                    if not isinstance(err, OSError):
                        raise
                    
                    if (exception is None):
                        exception = err
                    
                else:
                    break
            
            else:
                raise exception
        
        protocol = protocol_factory()
        waiter = Future(self)
        transport = _SelectorDatagramTransport(self, socket, protocol, remote_address, waiter, None)
        
        try:
            await waiter
        except:
            transport.close()
            raise
        
        return transport, protocol
    
    def _create_server_get_address_info(self, host, port, family, flags):
        """
        Gets address info for the given parameters. This method is used by ``.create_server``, when resolving hosts.
        
        Parameters
        ----------
        host : `None` or `str`, `iterable` of (`None` or `str`)
            Network interfaces should the server be bound.
        port : `None` or `int`
            The port to use by the `host`.
        family : `AddressFamily` or `int`
            The family of the address.
        flags : `int`
            Bit-mask for `get_address_info`.
        
        Returns
        -------
        future : ``Future``
            A future, what's result is set, when the address is dispatched.
        """
        return self._ensure_resolved((host, port), family=family, type=module_socket.SOCK_STREAM, flags=flags)
    
    async def create_server(self, protocol_factory, host=None, port=None, *, family=module_socket.AF_UNSPEC,
            flags=module_socket.AI_PASSIVE, socket=None, backlog=100, ssl=None,
            reuse_address=(os.name == 'posix' and sys.platform != 'cygwin'), reuse_port=False):
        """
        Creates a TCP server (socket type SOCK_STREAM) listening on port of the host address.
        
        This method is a coroutine.
        
        Parameters
        ----------
        protocol_factory : `callable`
            Factory function for creating a protocols.
        host : `None` or `str`, `iterable` of (`None` or `str`), Optional
            To what network interfaces should the server be bound.
            
            Mutually exclusive with the `socket` parameter.
        port : `None` or `int`, Optional
            The port to use by the `host`(s).
            
            Mutually exclusive with the `socket` parameter.
        family : `AddressFamily` or `int`, Optional (Keyword only)
            Can be given either as `socket.AF_INET` or `socket.AF_INET6` to force the socket to use `IPv4` or `IPv6`.
            If not given, then  will be determined from host name.
        flags : `int`, Optional (Keyword only)
            Bit-mask for `get_address_info`.
        socket : `None` or `socket.socket`, Optional (Keyword only)
            Can be specified in order to use a preexisting socket object.
            
            Mutually exclusive with `host` and `port` parameters.
        backlog : `int`, Optional (Keyword only)
            The maximum number of queued connections passed to `listen()` (defaults to 100).
        ssl : `None` or ``SSLContext``, Optional (Keyword only)
            Whether and what ssl is enabled for the connections.
        reuse_address : `bool`, Optional (Keyword only)
            Tells the kernel to reuse a local socket in `TIME_WAIT` state, without waiting for its natural timeout to
            expire. If not specified will automatically be set to True on Unix.
        reuse_port : `bool`, Optional (Keyword only)
            Tells to the kernel to allow this endpoint to be bound to the same port as an other existing endpoint
            already might be bound to.
            
            Not supported on Windows.
        
        Returns
        -------
        server : ``Server``
            The created server instance.
        
        Raises
        ------
        TypeError
            - If `ssl` is not given either as `None` or as `ssl.SSLContext` instance.
            - If `reuse_port` is given as non `bool`.
            - If `reuse_address` is given as non `bool`.
            - If `reuse_port` is given as non `bool`.
            - If `host` is not given as `None`, `str` and neither as `iterable` of `None` or `str`.
        ValueError
            - If `host` or `port` parameter is given, when `socket` is defined as well.
            - If `reuse_port` is given as `True`, but not supported.
            - If neither `host`, `port` nor `socket` were given.
            - If `socket` is given, but it's type is not `module_socket.SOCK_STREAM`.
        OsError
            Error while attempting to binding to address.
        """
        if (ssl is not None) and (type(ssl) is not SSLContext):
            raise TypeError(f'`ssl` can be given as `None` or as ``SSLContext``, got {ssl.__class__.__name__}.')
        
        if (host is not None) or (port is not None):
            if (socket is not None):
                raise ValueError('`host` and `port` parameters are mutually exclusive with `socket`.')
            
            if (type(reuse_address) is not bool):
                raise TypeError('`reuse_address` can be `None` or type `bool`, got '
                    f'`{reuse_address.__class__.__name__}`.')
            
            if type(reuse_port) is not bool:
                raise TypeError('`reuse_address` can be `None` or type `bool`, got '
                    f'`{reuse_port.__class__.__name__}`.')
            
            if reuse_port and (not hasattr(module_socket, 'SO_REUSEPORT')):
                raise ValueError('`reuse_port` not supported by the socket module.')
            
            hosts = []
            if (host is None) or (host == ''):
                 hosts.append(None)
            elif isinstance(host, str):
                hosts.append(hosts)
            elif hasattr(type(host), '__iter__'):
                for host in host:
                    if (host is None) or (host == ''):
                        hosts.append(None)
                        continue
                    
                    if isinstance(host, str):
                        hosts.append(host)
                        continue
                    
                    raise TypeError('`host` is passed as iterable, but it yielded at least 1 not `None`, or `str` '
                        f'instance; `{host!r}`')
            else:
                raise TypeError('`host` should be `None`, `str` instance or iterable of `None` or of `str` instances, '
                    f'got {host!r}')
            
            sockets = []
            
            futures = {self._create_server_get_address_info(host, port, family, flags) for host in hosts}
            
            try:
                while True:
                    done, pending = await WaitTillFirst(futures, self)
                    for future in done:
                        futures.remove(future)
                        infos = future.result()
                        
                        for info in infos:
                            socket_family, socket_type, socket_protocol, canonical_name, socket_address = info
                            
                            try:
                                socket = module_socket.socket(socket_family, socket_type, socket_protocol)
                            except module_socket.error:
                                continue
                            
                            sockets.append(socket)
                            
                            if reuse_address:
                                socket.setsockopt(module_socket.SOL_SOCKET, module_socket.SO_REUSEADDR, True)
                            
                            if reuse_port:
                                try:
                                    socket.setsockopt(module_socket.SOL_SOCKET, module_socket.SO_REUSEPORT, 1)
                                except OSError as err:
                                    raise ValueError('reuse_port not supported by socket module, SO_REUSEPORT defined '
                                        'but not implemented.') from err
                            
                            if (_HAS_IPv6 and (socket_family == module_socket.AF_INET6) and \
                                    hasattr(module_socket, 'IPPROTO_IPV6')):
                                socket.setsockopt(module_socket.IPPROTO_IPV6, module_socket.IPV6_V6ONLY, True)
                            try:
                                socket.bind(socket_address)
                            except OSError as err:
                                raise OSError(err.errno, f'Error while attempting to bind on address '
                                    f'{socket_address!r}: {err.strerror.lower()!s}.') from None
                    
                    if futures:
                        continue
                    
                    break
            except:
                for socket in sockets:
                    socket.close()
                    
                for future in futures:
                    future.cancel()
                
                raise
            
        else:
            if socket is None:
                raise ValueError('Neither `host`, `port` nor `socket` were given.')
            
            if socket.type != module_socket.SOCK_STREAM:
                raise ValueError(f'A stream socket was expected, got {socket!r}.')
            
            sockets = [socket]
        
        for socket in sockets:
            socket.setblocking(False)
        
        return Server(self, sockets, protocol_factory, ssl, backlog)
    
    if IS_UNIX:
        async def connect_read_pipe(self, protocol, pipe):
            return await UnixReadPipeTransport(self, pipe, protocol)
        
        async def connect_write_pipe(self, protocol, pipe):
            return await UnixWritePipeTransport(self, pipe, protocol)
        
        async def subprocess_shell(self, command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                *, extra=None, preexecution_function=None, close_fds=True, cwd=None, startup_info=None,
                creation_flags=0, restore_signals=True, start_new_session=False, pass_fds=()):
            
            if not isinstance(command, (bytes, str)):
                raise TypeError(f'`cmd` must be `bytes` or `str` instance, got {command.__class__.__name__}.')
            
            process_open_kwargs = {
                'preexec_fn' : preexecution_function,
                'close_fds' : close_fds,
                'cwd' : cwd,
                'startupinfo' : startup_info,
                'creationflags' : creation_flags,
                'restore_signals' : restore_signals,
                'start_new_session' : start_new_session,
                'pass_fds' : pass_fds,
                    }
            
            return await AsyncProcess(self, command, True, stdin, stdout, stderr, 0, extra, process_open_kwargs)
        
        async def subprocess_exec(self, program, *args, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,  extra=None, preexecution_function=None, close_fds=True, cwd=None,
                startup_info=None, creation_flags=0, restore_signals=True, start_new_session=False, pass_fds=()):
            
            process_open_kwargs = {
                'preexec_fn' : preexecution_function,
                'close_fds' : close_fds,
                'cwd' : cwd,
                'startupinfo' : startup_info,
                'creationflags' : creation_flags,
                'restore_signals' : restore_signals,
                'start_new_session' : start_new_session,
                'pass_fds' : pass_fds,
                    }
            
            return await AsyncProcess(self, (program, *args), False, stdin, stdout, stderr, 0, extra,
                process_open_kwargs)
    
    else:
        async def connect_read_pipe(self, protocol, pipe):
            raise NotImplementedError
        
        async def connect_write_pipe(self, protocol, pipe):
            raise NotImplementedError
        
        async def subprocess_shell(self, cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, *,
                extra=None, preexecution_function=None, close_fds=True, cwd=None, startup_info=None, creation_flags=0,
                restore_signals=True, start_new_session=False, pass_fds=()):
            raise NotImplementedError
        
        async def subprocess_exec(self, program, *args, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, extra=None, preexecution_function=None, close_fds=True, cwd=None,
                startup_info=None, creation_flags=0, restore_signals=True, start_new_session=False, pass_fds=()):
            raise NotImplementedError
    
    set_docs(connect_read_pipe,
        """
        Register the read end of the given pipe in the event loop.
        
        This method is a coroutine.
        
        Parameters
        ----------
        protocol : `Any`
            An async-io protocol implementation to use as the transport's protocol.
        pipe : `file-like` object
            The pipe to connect to on read end.
            
            Is set to non-blocking mode.
        
        Returns
        -------
        transport : ``UnixReadPipeTransport``
            The created transport.
        
        Raises
        ------
        ValueError
            Pipe transport is only for pipes, sockets and character devices.'
        NotImplementedError
            Not supported on windows by the library.
        """)
    
    set_docs(connect_write_pipe,
        """
        Register the write end of the given pipe in the event loop.
        
        This method is a coroutine.
        
        Parameters
        ----------
        protocol : `Any`
            An async-io protocol implementation to use as the transport's protocol.
        pipe : `file-like` object
            The pipe to connect to on write end.
            
            Is set to non-blocking mode.
        
        Returns
        -------
        transport : ``UnixReadPipeTransport``
            The created transport.
        
        Raises
        ------
        ValueError
            Pipe transport is only for pipes, sockets and character devices.'
        NotImplementedError
            Not supported on windows by the library.
        """)
        
    set_docs(subprocess_shell,
        """
        Create a subprocess from cmd.
        
        This is similar to the standard library `subprocess.Popen` class called with `shell=True`.
        
        This method is a coroutine.
        
        Parameters
        ----------
        cmd : `str` or `bytes`
            The command to execute. Should use the platform’s “shell” syntax.
        stdin : `file-like`, `subprocess.PIPE`, `subprocess.DEVNULL`, Optional
            Standard input for the created shell. Defaults to `subprocess.PIPE`.
        stdout : `file-like`, `subprocess.PIPE`, `subprocess.DEVNULL`, Optional
            Standard output for the created shell. Defaults to `subprocess.PIPE`.
        stderr : `file-like`, `subprocess.PIPE`, `subprocess.DEVNULL`, `subprocess.STDOUT`, Optional
            Standard error for the created shell. Defaults to `subprocess.PIPE`.
        extra : `None` or `dict` of (`str`, `Any`) items, Optional (Keyword only)
            Optional transport information.
        preexecution_function : `None` or `callable`, Optional (Keyword only)
            This object is called in the child process just before the child is executed. POSIX only, defaults to
            `None`.
        close_fds : `bool`, Optional (Keyword only)
            Defaults to `True`
            
            If `close_fds` is True, all file descriptors except `0`, `1` and `2` will be closed before the child
            process is executed. Otherwise when `close_fds` is False, file descriptors obey their inheritable flag as
            described in Inheritance of File Descriptors.
        cwd : `str`, `bytes`, `path-like` or `None`, Optional (Keyword only)
            If `cwd` is not `None`, the function changes the working directory to cwd before executing the child.
            Defaults to `None`
        startup_info : `subprocess.STARTUPINFO` or `None`, Optional (Keyword only)
            Is passed to the underlying `CreateProcess` function.
        creation_flags : `int`, Optional (Keyword only)
            Can be given as 1 of the following flags:
            
            - `CREATE_NEW_CONSOLE`
            - `CREATE_NEW_PROCESS_GROUP`
            - `ABOVE_NORMAL_PRIORITY_CLASS`
            - `BELOW_NORMAL_PRIORITY_CLASS`
            - `HIGH_PRIORITY_CLASS`
            - `IDLE_PRIORITY_CLASS`
            - `NORMAL_PRIORITY_CLASS`
            - `REALTIME_PRIORITY_CLASS`
            - `CREATE_NO_WINDOW`
            - `DETACHED_PROCESS`
            - `CREATE_DEFAULT_ERROR_MODE`
            - `CREATE_BREAKAWAY_FROM_JOB`
            
            Defaults to `0`.
        restore_signals : `bool`, Optional
            If given as `True`, so by default, all signals that Python has set to `SIG_IGN` are restored to `SIG_DFL`
            in the child process before the exec. Currently this includes the `SIGPIPE`, `SIGXFZ` and `SIGXFSZ`
            signals. POSIX only.
        start_new_session : `bool`, Optional
            If given as `True` the `setsid()` system call will be made in the child process prior to the execution of
            the subprocess. POSIX only, defaults to `False`.
        pass_fds : `tuple`, Optional
            An optional sequence of file descriptors to keep open between the parent and the child. Providing any
            `pass_fds` forces `close_fds` to be `True`. POSIX only, defaults to empty tuple.
        
        Returns
        -------
        process : ``AsyncProcess``
        
        Raises
        ------
        TypeError
            If `cmd` is not given as `str` not `bytes` object.
        NotImplementedError
            Not supported on windows by the library.
        """)
    
    set_docs(subprocess_exec,
        """
        Create a subprocess from one or more string parameters specified by args.
        
        This is similar to the standard library `subprocess.Popen` class called with `shell=False`.
        
        This method is a coroutine.
        
        Parameters
        ----------
        program : `str`
            The program executable.
        *args : `str`
            Parameters to open the `program` with.
        stdin : `file-like`, `subprocess.PIPE`, `subprocess.DEVNULL`, Optional (Keyword only)
            Standard input for the created shell. Defaults to `subprocess.PIPE`.
        stdout : `file-like`, `subprocess.PIPE`, `subprocess.DEVNULL`, Optional (Keyword only)
            Standard output for the created shell. Defaults to `subprocess.PIPE`.
        stderr : `file-like`, `subprocess.PIPE`, `subprocess.DEVNULL`, `subprocess.STDOUT`, Optional (Keyword only)
            Standard error for the created shell. Defaults to `subprocess.PIPE`.
        extra : `None` or `dict` of (`str`, `Any`) items, Optional (Keyword only)
            Optional transport information.
        preexecution_function : `None` or `callable`, Optional (Keyword only)
            This object is called in the child process just before the child is executed. POSIX only, defaults to
            `None`.
        close_fds : `bool`, Optional (Keyword only)
            Defaults to `True`
            
            If `close_fds` is True, all file descriptors except `0`, `1` and `2` will be closed before the child
            process is executed. Otherwise when `close_fds` is False, file descriptors obey their inheritable flag as
            described in Inheritance of File Descriptors.
        cwd : `str`, `bytes`, `path-like` or `None`, Optional (Keyword only)
            If `cwd` is not `None`, the function changes the working directory to cwd before executing the child.
            Defaults to `None`
        startup_info : `subprocess.STARTUPINFO` or `None`, Optional (Keyword only)
            Is passed to the underlying `CreateProcess` function.
        creation_flags : `int`, Optional (Keyword only)
            Can be given as 1 of the following flags:
            
            - `CREATE_NEW_CONSOLE`
            - `CREATE_NEW_PROCESS_GROUP`
            - `ABOVE_NORMAL_PRIORITY_CLASS`
            - `BELOW_NORMAL_PRIORITY_CLASS`
            - `HIGH_PRIORITY_CLASS`
            - `IDLE_PRIORITY_CLASS`
            - `NORMAL_PRIORITY_CLASS`
            - `REALTIME_PRIORITY_CLASS`
            - `CREATE_NO_WINDOW`
            - `DETACHED_PROCESS`
            - `CREATE_DEFAULT_ERROR_MODE`
            - `CREATE_BREAKAWAY_FROM_JOB`
            
            Defaults to `0`.
        restore_signals : `bool`, Optional (Keyword only)
            If given as `True`, so by default, all signals that Python has set to `SIG_IGN` are restored to `SIG_DFL`
            in the child process before the exec. Currently this includes the `SIGPIPE`, `SIGXFZ` and `SIGXFSZ`
            signals. POSIX only.
        start_new_session : `bool`, Optional (Keyword only)
            If given as `True` the `setsid()` system call will be made in the child process prior to the execution of
            the subprocess. POSIX only, defaults to `False`.
        pass_fds : `tuple`, Optional (Keyword only)
            An optional sequence of file descriptors to keep open between the parent and the child. Providing any
            `pass_fds` forces `close_fds` to be `True`. POSIX only, defaults to empty tuple.
        
        Returns
        -------
        process : ``AsyncProcess``
        
        Raises
        ------
        NotImplementedError
            Not supported on windows by the library.
        """)
