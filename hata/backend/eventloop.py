﻿# -*- coding: utf-8 -*-
__all__ = ('Cycler', 'EventThread', 'LOOP_TIME', 'LOOP_TIME_RESOLUTION', 'ThreadSyncerCTX', )

import sys, errno, weakref, subprocess, os
import socket as module_socket
import time as module_time
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ
from threading import current_thread, Thread, Event
from heapq import heappop, heappush
from collections import deque

from .dereaddons_local import alchemy_incendiary, WeakReferer, weakmethod, method, WeakCallable, DocProperty, \
    WeakValueDictionary, DOCS_ENABLED
from .futures import Future, Task, Gatherer, render_exc_to_list, iscoroutine, FutureAsyncWrapper, WaitTillFirst, \
    CancelledError
from .transprotos import SSLProtocol, _SelectorSocketTransport
from .executor import Executor
from .analyzer import CallableAnalyzer

IS_UNIX = (sys.platform != 'win32')

if IS_UNIX:
    from .subprocess import UnixReadPipeTransport, UnixWritePipeTransport, AsyncProcess

import threading
from .futures import _ignore_frame
_ignore_frame(__spec__.origin           , '_run'            , 'self.func(*self.args)'           ,)
_ignore_frame(__spec__.origin           , 'run'             , 'handle._run()'                   ,)
_ignore_frame(threading.__spec__.origin , '_bootstrap'      , 'self._bootstrap_inner()'         ,)
_ignore_frame(threading.__spec__.origin , '_bootstrap_inner', 'self.run()'                      ,)
del threading, _ignore_frame

from . import executor, futures

LOOP_TIME = module_time.monotonic
LOOP_TIME_RESOLUTION = module_time.get_clock_info('monotonic').resolution

class Handle(object):
    """
    Object returned by a callback registration method:
    - ``EventThread.call_soon``
    - ``EventThread.call_soon_threadsafe``.
    
    Attributes
    ----------
    func : `callable`
        The wrapped function.
    args : `tuple` of `Any`
        Arguments to call ``.func`` with.
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
            Arguments to call `func` with.
        """
        self.func = func
        self.args = args
        self.cancelled = False
    
    def __repr__(self):
        """Returns the handle's representation."""
        result = [
            '<',
            self.__class__.__name__,
                ]
        
        if self.cancelled:
            result.append(' cancelled')
        else:
            result.append(' func=')
            result.append(repr(self.func))
            result.append('(')
            
            args = self.args
            limit = len(args)
            if limit:
                index = 0
                while True:
                    arg = args[index]
                    result.append(repr(arg))
                    
                    index += 1
                    if index == limit:
                        break
                    
                    result.append(', ')
                    continue
            
            result.append(')')
        
        result.append('>')
        
        return ''.join(result)
    
    def cancel(self):
        """Cancels the handle if not yet cancelled."""
        if not self.cancelled:
            self.cancelled = True
            self.func = None
            self.args = None
    
    def _run(self):
        """
        Calls the handle's function with it's arguments. If exception occurs meanwhile, renders it.
        
        Notes
        -----
        This method should be called only inside of an ``EventThread``.
        """
        try:
            self.func(*self.args)
        except BaseException as err:
            current_thread().render_exc_async(err, [
                'Exception occured at ',
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
        Arguments to call ``.func`` with.
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
            Arguments to call `func` with.
        """
        self.func = func
        self.args = args
        self.cancelled = False
        self.when = when
    
    def __repr__(self):
        """Returns the timer handle's representation."""
        result = [
            '<',
            self.__class__.__name__,
                ]
        
        if self.cancelled:
            result.append(' cancelled')
        else:
            result.append(' func=')
            result.append(repr(self.func))
            result.append('(')
            
            args = self.args
            limit = len(args)
            if limit:
                index = 0
                while True:
                    arg = args[index]
                    result.append(repr(arg))
                    
                    index += 1
                    if index == limit:
                        break
                    
                    result.append(', ')
                    continue
            
            result.append(')')
            result.append(', when=')
            result.append(repr(self.when))
        
        result.append('>')
        
        return ''.join(result)
    
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
        Arguments to call ``.func`` with.
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
            Arguments to call `func` with.
        
        Raises
        ------
        TypeError
            `func` is not weakreferable.
        """
        self.when = when
        callback = self._callback(self)
        try:
            if type(func) is method:
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
        
    class _callback(object):
        """
        Weakreference callback used by ``TimerWeakHandle`` to cancel the respective handle, when it's `func` gets
        gargabe collected.
        
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

class CyclerCallable(object):
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
            - `func` accepts less or more reserved positional arguments than `1`.
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
        min_, max_ = analyzer.get_non_reserved_positional_argument_range()
        if min_ > 1:
            raise TypeError(f'`{func!r}` excepts at least `{min_!r}` non reserved arguments, meanwhile `1` would be '
                'passed to it.')
        
        if not ((min_ == 1) or max_ >= 1 or analyzer.accepts_args()):
            raise TypeError(f'`{func!r}` expects maximum `{max_!r}` non reserved arguments, meanwhile the event '
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


class Cycler(object):
    """
    Cycles the given functions on an eventloop, by calling them after every `n` amount of seconds.
    
    Attributes
    ----------
    cycle_time : `float`
        The time interval of the cycler to call the added functions.
    funcs : `list` of ``CyclerCallable``
        Callables of a cycler containing whether they are sync, async, and what is their priority order.
    handle : ``TimerHandle``
        Hanlder, what will call the cycler when cycle time is over.
    loop : ``EventTHread``
        The async event loop of the cycler, what it uses to ensure itself.
    """
    __slots__ = ('cycle_time', 'funcs', 'handle', 'loop',)
    
    def __new__(cls, loop, cycle_time, *funcs, priority=0):
        """
        Creates a new ``Cycler`` with the given parameters.
        
        Parameters
        ----------
        loop : ``EventTHread``
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
            - Any `func` accepts less or more reserved positional arguments than `1`.
        ValueError
            If `cycle_time` is negative or `0`.
        """
        if not loop.running:
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
            self.handle = None
            
            with ThreadSyncerCTX(loop):
                handle = loop.call_later(cycle_time, cls._run, self)
        
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
                self.loop.render_exc_async(err,[
                    self.__class__.__name__,
                    ' exception occured\nat calling ',
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
        if funcs:
            priority = funcs[0].priority
            
            index = 1
            limit = len(priority)
            while index < limit:
                func = funcs[index]
                if func.priority == priority:
                    index +=1
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
        
        loop.call_soon_threadsafe(self.__class__._cancel, self)
    
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
        
        loop.call_soon_threadsafe(self.__class__._call_now, self)
    
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
        
        loop.call_soon_threadsafe(self.__class__._reschedule, self)
    
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
        Sets the cycle time of the cycler to teh gvien value.
        
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
            - Any `func` accepts less or more reserved positional arguments than `1`.
        """
        validated_func = CyclerCallable(func, priority)
        
        loop = self.loop
        if current_thread() is loop:
            self._append(validated_func)
            return
        
        loop.call_soon_threadsafe(self.__class__._append, self, validated_func)
    
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
        
        loop.call_soon_threadsafe(self.__class__._remove, self, func)
    
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
            to_comapre = funcs[index]
            if (not is_cycler_callable):
                to_comapre = to_comapre.func
            
            if to_comapre == func:
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
            return -1. #w ont be be called
        
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


class ThreadSyncerCTX(object):
    """
    Thread syncer for ``EventThead``-s, to stop their execution, meanwhile they are used inside of a a `with` block.
    The local thread's exection is stopped, meanwhile it waits for the ``EventThead`` top pause.
    
    Can be used as a context manager, like:
    
    ```
    with ThreadSyncerCTX(LOOP):
        # The eventloop is paused inside here.
    ```
    
    Or, can be used with ``EventThead.enter()`` as well, like:
    
    ```
    with LOOP.enter():
        # The eventloop is paused inside here.
    ```
    
    Attributes
    ----------
    loop : ``EventThread``
        The respective eventloop.
    enter_event : `threading.Event`
        Threading event, which blocks the local thread, till the respective eventloop pauses.
    exit_event : `threading.Event`
        Blocks the respective eventloop, till the local thread gives the control back to it with exisint the `with`
        block.
    """
    __slots__ = ('loop', 'enter_event', 'exit_event')
    
    def __init__(self, loop):
        """
        Creates a new ``ThreadSyncerCTX`` bound to the given eventloop.
        
        Parameters
        ----------
        loop : ``EventThread``
            The eventloop to pause.
        """
        self.loop = loop
        self.enter_event = Event()
        self.exit_event = Event()

    def __enter__(self):
        """
        Blocks the local thread, till the respective ``EventThead`` pauses. If the ``EventThead`` is stopped already,
        does nothing.
        """
        loop = self.loop
        if loop.running:
            handle = Handle(self._give_control_cb, ())
            loop._ready.append(handle)
            loop.wakeup()
            self.enter_event.wait()
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Unpauses the respective ``EventThead``."""
        self.exit_event.set()
        return False
    
    def _give_control_cb(self):
        """
        Callback used to pause the respective ``EventThread`` and give control to the other one.
        """
        self.enter_event.set()
        self.exit_event.wait()

_HAS_IPv6 = hasattr(module_socket, 'AF_INET6')

def _ipaddr_info(host, port, family, type_, proto):
    """
    Gets the addres info for the given parmeters.
    
    Parameters
    ----------
    host : `str` or `bytes`
        The host ip adress
    port : `int`
        The host port.
    family : `AddressFamily` or `int`
        Address family.
    type_ : `SocketKind` or `int`
        Socket type.
    proto : `int`
        Protocol type.
    
    Returns
    -------
    result : `None` or `tuple` (`AddressFamily` or `int`, `SocketKind` or `int`, `int`, `str`, `tuple` (`str, `int`))
        If everything is correct, returns a `tuple` of 5 elements:
        - family : Address family.
        - type_ : Socket type.
        - proto : Protocol type.
        - cname : Represents the canonical name of the host. (Always empty string.)
        - sockaddr : Socket address contianing the host and the port.
    """
    # Try to skip getaddrinfo if `host`koish is already an IP. Users might have handled name resolution in their own code
    # and pass in resolved IPs.
    if not hasattr(module_socket, 'inet_pton'):
        return
    
    if proto not in (0, module_socket.IPPROTO_TCP, module_socket.IPPROTO_UDP) or (host is None):
        return
    
    if type_ == module_socket.SOCK_STREAM:
        proto = module_socket.IPPROTO_TCP
    elif type_ == module_socket.SOCK_DGRAM:
        proto = module_socket.IPPROTO_UDP
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
        # If port's a service name like "http", don't skip getaddrinfo.
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
            return family, type_, proto,'', (host, port)
    
    # `host` is not an IP address.
    return None

def _is_dgram_socket(socket):
    """
    Returns whether the given socket is dgram scoket.
    
    Parameters
    ----------
    socket : `socket.socket`
        The socket to check.
    
    Returns
    -------
    is_dgram_socket : `bool`
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

_OLD_AGEN_HOOKS = sys.get_asyncgen_hooks()

def _asyncgen_firstiter_hook(agen):
    """
    Adds asyncgens to their respective eventloop. These async gens are stut down, when the loop is stopped.
    
    Parameters
    ----------
    agen : `async_generator`
    """
    loop = current_thread()
    if isinstance(loop, EventThread):
        if loop._asyncgens_shutdown_called:
            return
        
        loop._asyncgens.add(agen)
        return
    
    firstiter = _OLD_AGEN_HOOKS.firstiter
    if firstiter is not None:
        firstiter(agen)

def _asyncgen_finalizer_hook(agen):
    """
    Removes asyncgens from their respective eventloop.
    
    Parameters
    ----------
    agen : `async_generator`
    """
    loop = current_thread()
    if isinstance(loop, EventThread):
        loop._asyncgens.discard(agen)
        if not loop.running:
            return
            
        Task(agen.aclose(), loop)
        loop.wakeup()
        return
    
    finalizer = _OLD_AGEN_HOOKS.finalizer
    if finalizer is not None:
        finalizer(agen)

sys.set_asyncgen_hooks(firstiter=_asyncgen_firstiter_hook, finalizer=_asyncgen_finalizer_hook)


if sys.platform == 'win32':
    #If windows select raises OSError, we cacnnot do anything, but
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
        
        I do not take credit for any missbehaviour.
        """
        def _select(self, r, w, _, timeout=None):
            try:
                result_r, result_w, result_x = select(r, w, w, timeout)
            except ValueError:
                default_reader = current_thread()._selfread_socket
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
                                try:
                                    r.remove(reader)
                                except KeyError:
                                    pass
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
                                try:
                                    w.remove(writer)
                                except KeyError:
                                    pass
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
                        try:
                            r.remove(reader)
                        except KeyError:
                            pass
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
                        try:
                            w.remove(writer)
                        except KeyError:
                            pass
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

class Server(object):
    """
    Server returned by ``EventThread.create_server``.
    
    Attributes
    ----------
    active_count : `int`
        The amount of active connections bount to the server.
    backlog : `int`
        The maximum number of queued connections passed to ˙`listen()` (defaults to 100).
    close_waiters : `None` or `list` of ``Future``
        Futures, which are waiting for the server to close. If the server is already closed, set as `None`.
    loop : ``EventThread``
        The eventloop to what the server is bound to.
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
        Creates a new serevr with the given parameters.
        
        Parameters
        ----------
        loop : ``EventThread``
            The eventloop to what the server will be bound to.
        sockets : `list` of `socket.socket`
            The sockets to serve by the server.
        protocol_factory : `callable`
            Factory function for creating a protocols.
        ssl_context : `None` or `ssl.SSLContext`
            To enable ssl for the connections, give it as  `ssl.SSLContext`.
        backlog : `int`
            The maximum number of queued connections passed to ˙`listen()` (defaults to 100).
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
            self._wakeup_close_waiters()

    def _wakeup_close_waiters(self):
        """
        Wakes up the server's clsoe waiters.
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
        for sock in sockets:
            loop._stop_serving(sock)
        
        self.serving = False
        
        if self.active_count == 0:
            self._wakeup_close_waiters()
    
    async def start(self):
        """
        Starts the server by starting serving it's sockets.
        """
        if self.serving:
            return
        
        self.serving = True
        
        protocol_factory = self.protocol_factory
        ssl_context = self.ssl_context
        backlog = self.backlog
        loop = self.loop
        
        for sock in self.sockets:
            sock.listen(backlog)
            loop._start_serving(protocol_factory, sock, ssl_context, self, backlog)
        
        # Skip one eventloop cycle, so all the callbacks added up ^ will run nefore returning.
        future = Future(loop)
        future.set_result(None)
        await future

    async def wait_closed(self):
        """
        Blocks the task, till the sever is closes.
        """
        if self.sockets is None:
            return
        
        close_waiters = self.close_waiters
        if close_waiters is None:
            return
        
        close_waiter = Future(self.loop)
        close_waiters.append(close_waiter)
        await close_waiter

class EventThreadCTXManager(object):
    """
    Context manager of an ``EventThread``, which wraps it's runner. Whne the runner is started up, set it's ``waiter.``
    allowing the strarter thread to continue.
    
    Attributes
    ----------
    thread : `None` or ``EventThread``
        The wrapped eventloop.
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
        thread_waiter = Event()
        
        self = object.__new__(cls)
        self.thread = thread
        self.thread_waiter = thread_waiter
        return self, thread_waiter
    
    def __enter__(self):
        """
        Called, when the respective eventloop's runner started up.
        
        Enters the eventloop runner setting it's waiter and finishes the loop's initialization.
        
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
            raise RuntimeError(f'{EventThreadCTXManager.__class__.__name__}.__enter__ called with thread waiter lock set.')
        
        try:
            thread = self.thread
            if (thread is not current_thread()):
                raise RuntimeError(f'{thread!r}.run called from an other thread: {current_thread()!r}')
            
            if (thread.running):
                raise RuntimeError(f'{thread!r}.run called when the thread is already running.')
            
            if (thread._is_stopped):
                raise RuntimeError(f'{thread!r}.run called when the thread is already stopped.')
            
            thread.running = True
            
            selfread_socket, selfwrite_socket = module_socket.socketpair()
            selfread_socket.setblocking(False)
            selfwrite_socket.setblocking(False)
            thread._selfread_socket = selfread_socket
            thread._selfwrite_socket = selfwrite_socket
            thread._internal_fds += 1
            thread.add_reader(selfread_socket.fileno(), thread.emptyselfsocket)
        finally:
            thread_waiter.set()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        When the eventloop's runner stops, it's context closes it.
        """
        thread = self.thread
        self.thread = None
        
        thread.running = False
        thread.remove_reader(thread._selfread_socket.fileno())
        thread._selfread_socket.close()
        thread._selfread_socket = None
        thread._selfwrite_socket.close()
        thread._selfwrite_socket = None
        thread._internal_fds -= 1
        
        thread._ready.clear()
        thread._scheduled.clear()
        
        thread.cancel_executors()
        
        selector = thread.selector
        if (selector is not None):
            thread.selector = None
            selector.close()
        
        return False


class EventThreadRunDescriptor(object):
    __class_doc__ = ("""
    Descriptor which desides, exactly which function of the ``EventThread`` is called, when using it's `.run` method.
    
    If called from class, returns `self`. If called from a non yet running eventloop, returns that's `.runner`. If
    called from an already stopped eventloop, raises `RuntimeError`.
    """)
    
    __instance_doc__ = ("""
    `EventThread.run` is an overloaded method, with two usages. The first is when the thread starts up, it will run the
    thread's "runner", ``EvenThread.runner``. The other one usage is, when the eventloop is running, then it returns
    it's "caller", ``EvenThread.caller``.
    
    If the eventloop is already closed, raises ``RuntimeError``.
    """)
    
    def __get__(self, obj, type_):
        if obj is None:
            return self
        
        if obj.running:
            return obj.caller
        elif not obj._is_stopped:
            return obj.runner
        else:
            raise RuntimeError(f'The {obj.__class__.__name__} is already stopped.')
    
    def __set__(self, obj, value):
        raise AttributeError('can\'t set attribute')
    
    def __delete__(self, obj):
        raise AttributeError('can\'t delete attribute')
    
    __doc__ = DocProperty()

class EventThreadType(type):
    """
    Type of even thread, which manages their instances creation.
    """
    def __call__(cls, daemon=False, name=None, **kwargs):
        """
        Creates a new ``EventThread`` instance with the given parameters.
        
        Parameters
        ----------
        daemon : ``bool``
            Whether the created thread should be daemon.
        name : `str`
            The created threa's name.
        kwargs : keyword arguments
            Additional event thread specific parameters.
        
        Other Parameters
        ----------------
        keep_executor_count : `int`
            The minimal amount of executors, what the event thread should keep alive. Defaults to `1`.
        
        Returns
        -------
        obj : ``EventThread``
            The created eventloop.
        
        Notes
        -----
        ``EventThread`` supports only an additional, `keep_executor_count` parameter, but it's subclasse's might
        support other ones as well.
        """
        obj = Thread.__new__(cls)
        cls.__init__(obj, **kwargs)
        Thread.__init__(obj, daemon=daemon, name=name)
        
        ctx, thread_waiter = EventThreadCTXManager(obj)
        try:
            obj.ctx = ctx
            Thread.start(obj)
        except:
            thread_waiter.set()
            raise
        
        thread_waiter.wait()
        
        return obj

class EventThread(Executor, Thread, metaclass=EventThreadType):
    time = LOOP_TIME
    time_resolution = LOOP_TIME_RESOLUTION
    __slots__ = ('__dict__', '__weakref__', '_asyncgens', '_asyncgens_shutdown_called', '_selfwrite_socket',
        '_internal_fds', '_ready', '_scheduled', '_selfread_socket', 'ctx', 'current_task', 'running', 'selector',
        'should_run', 'transports',)
    
    def __init__(self, keep_executor_count=1):
        """
        Creates a new ``EventThread`` with the given parameters.
        
        Parameters
        ----------
        keep_executor_count : `int`
            The minimal amount of executors, what the event thread should keep alive. Defaults to `1`.
        
        Notes
        -----
        This magic method is called by ``EventThreadType.__call__``, what does the other steps of the inilitation.
        """
        Executor.__init__(self, keep_executor_count)
        self.should_run = True
        self.running = False
        self.selector = DefaultSelector()
        
        self._ready = deque()
        self._scheduled = []
        self.current_task = None
        self._internal_fds = 0
        
        self._asyncgens = weakref.WeakSet()
        self._asyncgens_shutdown_called = False
        self.transports = WeakValueDictionary()
        
        self._selfread_socket = None
        self._selfwrite_socket = None
    
    def __repr__(self):
        """Returns the event thread's representation."""
        result = ['<', self.__class__.__name__, '(', self._name]
        self.is_alive() # easy way to get ._is_stopped set when appropriate
        if self._is_stopped or (not self.running):
            state = ' stopped'
        else:
            state = ' started'
        result.append(state)
        
        if self._daemonic:
            result.append(' daemon')
        
        ident = self._ident
        if ident is not None:
            result.append(' ident=')
            result.append(str(ident))
        
        result.append(' executor info: free=')
        result.append(str(self.free_executor_count))
        result.append(', used=')
        result.append(str(self.used_executor_count))
        result.append(', keep=')
        result.append(str(self.keep_executor_count))
        result.append(')>')

        return ''.join(result)
    
    
    def call_later(self, delay, callback, *args):
        """
        Schedule callback to be called after the given delay.
        
        Parameters
        ----------
        delay : `float`
            The delay after the `callback` whould be called.
        callback : `callable`
            The function to call later.
        args : arguments
            The arguments to call the `callback` with.
        
        Returns
        -------
        handle : `None` or ``TimerHandle``
            The created handle is returned, what can be used to cancel it. If the eventloop is stopped, returns `None`.
        """
        if self.running:
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
        args : arguments
            The arguments to call the `callback` with.
        
        Returns
        -------
        handle : `None` or ``TimerHandle``
            The created handle is returned, what can be used to cancel it. If the eventloop is stopped, returns `None`.
        """
        if self.running:
            handle = TimerHandle(when, callback, args)
            heappush(self._scheduled, handle)
            return handle
    
    def call_later_weak(self, delay, callback, *args):
        """
        Schedule callback with weakreferencing it to be called after the given delay.
        
        Parameters
        ----------
        delay : `float`
            The delay after the `callback` whould be called.
        callback : `callable`
            The function to call later.
        args : arguments
            The arguments to call the `callback` with.
        
        Returns
        -------
        handle : `None` or ``TimerWeakHandle``
            The created handle is returned, what can be used to cancel it. If the eventloop is stopped, returns `None`.
        
        Raises
        ------
        TypeError
            If `callback` cannot be weakreferred.
        """
        if self.running:
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
        args : arguments
            The arguments to call the `callback` with.
        
        Returns
        -------
        handle : `None` or ``TimerWeakHandle``
            The created handle is returned, what can be used to cancel it. If the eventloop is stopped, returns `None`.
        
        Raises
        ------
        TypeError
            If `callback` cannot be weakreferred.
        """
        if self.running:
            handle = TimerWeakHandle(when, callback, args)
            heappush(self._scheduled, handle)
            return handle
    
    def call_soon(self, callback, *args):
        """
        Schedules the callback to be called at the next iteration of the eventloop.
        
        Parameters
        ----------
        callback : `callable`
            The function to call later.
        args : arguments
            The arguments to call the `callback` with.
        
        Returns
        -------
        handle : `None` or ``Handle``
            The created handle is returned, what can be used to cancel it. If the eventloop is stopped, returns `None`.
        """
        if self.running:
            handle = Handle(callback, args)
            self._ready.append(handle)
            return handle
    
    def call_soon_threadsafe(self, callback, *args):
        """
        Schedules the callback to be called at the next iteration of the eventloop. Wakes up the eventloop if sleeping,
        so can be used from other threads as well.
        
        Parameters
        ----------
        callback : `callable`
            The function to call later.
        args : arguments
            The arguments to call the `callback` with.
        
        Returns
        -------
        handle : `None` or ``Handle``
            The created handle is returned, what can be used to cancel it. If the eventloop is stopped, returns `None`.
        """
        if self.running:
            handle = Handle(callback, args)
            self._ready.append(handle)
            self.wakeup()
            return handle
    
    def cycle(self, cycle_time, *funcs, priority=0):
        """
        Cycles the given functions on an eventloop, by calling them after every `n` amount of seconds.
        
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
        If the eventloop is not running, clears the callback instead of scheduling them.
        """
        callbacks = future._callbacks
        if self.running:
            while callbacks:
                handle = Handle(callbacks.pop(), (future,))
                self._ready.append(handle)
        else:
            callbacks.clear()
        
    def create_future(self):
        """
        Creates a future bound to the eventloop.
        
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
    
    def create_task_threadsafe(self, coro):
        """
        Creates a task wrapping the given coroutine and wakes up the eventloop. Wakes up the eventloop if sleeping, so
        can be used from other threads as well.
        
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
        self.wakeup()
        return task
    
    def enter(self):
        """
        Can be used to pause the eventloop. Check ``ThreadSyncerCTX`` for more details.
        
        Returns
        -------
        thread_syncer : ``ThreadSyncerCTX``
        """
        return ThreadSyncerCTX(self)

    # Ensures a future, coroutine, or an awaitable on this loop.
    # Returns a Future or a Task bound to this thread.
    def ensure_future(self, coro_or_future):
        if iscoroutine(coro_or_future):
            return Task(coro_or_future, self)
        
        if isinstance(coro_or_future, Future):
            if coro_or_future._loop is not self:
                coro_or_future = FutureAsyncWrapper(coro_or_future, self)
            return coro_or_future
        
        type_ = type(coro_or_future)
        if hasattr(type_, '__await__'):
            return Task(type_.__await__(coro_or_future), self)
        
        raise TypeError('A Future, a coroutine or an awaitable is required.')

    # Ensures a future, coroutine, or an awaitable on this loop.
    # If the future is bound to an another thread, it wakes self up.
    # Returns a Future or a Task bound to this thread.
    def ensure_future_threadsafe(self, coro_or_future):
        if iscoroutine(coro_or_future):
            task = Task(coro_or_future, self)
            self.wakeup()
            return task
        
        if isinstance(coro_or_future, Future):
            if coro_or_future._loop is not self:
                coro_or_future=FutureAsyncWrapper(coro_or_future, self)
            return coro_or_future
        
        type_ = type(coro_or_future)
        if hasattr(type_, '__await__'):
            task = Task(type_.__await__(coro_or_future), self)
            self.wakeup()
            return task

        raise TypeError('A Future, a coroutine or an awaitable is required.')
    
    run = EventThreadRunDescriptor()
    
    def runner(self):
        """
        Runs the eventloop, until ``.stop`` is called.
        
        Hata ``EventThread`` are created as already running eventloops.
        """
        with self.ctx:
            key = None
            fileobj = None
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
                        fileobj = key.fileobj
                        reader, writer = key.data
                        if (reader is not None) and (mask&EVENT_READ):
                            if reader.cancelled:
                                self.remove_reader(fileobj)
                            else:
                                if not reader.cancelled:
                                    ready.append(reader)
                        if (writer is not None) and (mask&EVENT_WRITE):
                            if writer.cancelled:
                                self.remove_writer(fileobj)
                            else:
                                if not writer.cancelled:
                                    ready.append(writer)
                    
                    key = None
                    fileobj = None
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
        Ensures the given awaitable on the eventloop and returns it's result when done.
        
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
        BaseException
            Any exception raised by `awaitable`.
        """
        return self.ensure_future_threadsafe(awaitable).syncwrap().wait(timeout)
    
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
        
        This method is called from functons or methods, where being on an ``EventThread`` is not guaranteed.
        
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
        elif type(before) is str:
            extracted = before.append(before)
        elif type(before) is list:
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
        elif type(after) is str:
            extracted.append(after)
        elif type(after) is list:
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
        Stops the eventloop. Threadsafe.
        """
        if self.should_run:
            if current_thread() is self:
                self._stop()
            else:
                self.call_soon(self._stop)
                self.wakeup()

    def _stop(self):
        """
        Stops the eventloop. Intrenal function of ``.stop``, called or queued up by it.
        
        Should be called only from the thread of the eventloop.
        """
        self.release_executors()
        self.should_run = False

    async def shutdown_asyncgens(self):
        self._asyncgens_shutdown_called = True
        
        if not len(self._asyncgens):
            return
        
        closing_agens = list(self._asyncgens)
        self._asyncgens.clear()
        
        results = await Gatherer(self, (ag.aclose() for ag in closing_agens))
        
        for result, agen in zip(results, closing_agens):
            exception = result.exception
            if (exception is not None) and (type(exception) is not CancelledError):
                extracted = [
                    'Exception occured during shutting down asyncgen:\n',
                    repr(agen),
                        ]
                render_exc_to_list(exception, extend=extracted)
                sys.stderr.write(''.join(extracted))

    def _make_socket_transport(self, sock, protocol, waiter=None, *, extra=None, server=None):
        return _SelectorSocketTransport(self, sock, protocol, waiter, extra, server)
    
    def _make_ssl_transport(self, rawsock, protocol, sslcontext, waiter=None, *, server_side=False,
            server_hostname=None, extra=None, server=None):
        
        ssl_protocol = SSLProtocol(self, protocol, sslcontext, waiter, server_side, server_hostname)
        _SelectorSocketTransport(self, rawsock, ssl_protocol, extra=extra, server=server)
        return ssl_protocol.app_transport

    def emptyselfsocket(self):
        """
        Reads all the data out from selfsocket.
        
        Familiar to asyncio eventloop's `._read_from_self`.
        """
        while True:
            try:
                data = self._selfread_socket.recv(4096)
                if not data:
                    break
            except InterruptedError:
                continue
            except BlockingIOError:
                break
    
    def wakeup(self):
        """
        Wakes up the eventloop. Threadsafe.
        
        Familiar as asyncio eventloop's `._write_to_self`.
        """
        selfwrite_socket = self._selfwrite_socket
        if selfwrite_socket is not None:
            try:
                selfwrite_socket.send(b'\0')
            except OSError:
                pass

    def _start_serving(self, protocol_factory, sock, sslcontext=None, server=None, backlog=100):
        self.add_reader(sock.fileno(), self._accept_connection, protocol_factory, sock, sslcontext, server, backlog)

    def _stop_serving(self, sock):
        self.remove_reader(sock.fileno())
        sock.close()

    def _accept_connection(self, protocol_factory, sock, sslcontext=None, server=None, backlog=100):
        # This method is only called once for each event loop tick where the
        # listening socket has triggered an EVENT_READ. There may be multiple
        # connections waiting for an .accept() so it is called in a loop.
        # See https://bugs.python.org/issue27906 for more details.
        for _ in range(backlog):
            try:
                conn, addr = sock.accept()
                conn.setblocking(False)
            except (BlockingIOError, InterruptedError, ConnectionAbortedError):
                # Early exit because the socket accept buffer is empty.
                return None
            except OSError as err:
                # There's nowhere to send the error, so just log it.
                if err.errno in (errno.EMFILE, errno.ENFILE, errno.ENOBUFS, errno.ENOMEM):
                    # Some platforms (e.g. Linux keep reporting the FD as
                    # ready, so we remove the read handler temporarily.
                    # We'll try again in a while.
                    self.render_exc_async(err, before=[
                        'Exception occured at',
                        repr(self),
                        '._accept_connection\n',
                            ])
                    
                    self.remove_reader(sock.fileno())
                    self.call_later(1., self._start_serving, protocol_factory, sock, sslcontext, server, backlog)
                else:
                    raise  # The event loop will catch, log and ignore it.
            else:
                extra = {'peername': addr}
                coro = self._accept_connection2(protocol_factory, conn, extra, sslcontext, server)
                Task(coro, self)
    
    async def _accept_connection2(self, protocol_factory, conn, extra, sslcontext=None, server=None):
        try:
            protocol = protocol_factory()
            waiter = Future(self)
            if sslcontext:
                transport = self._make_ssl_transport(conn, protocol, sslcontext, waiter=waiter, server_side=True,
                    extra=extra, server=server)
            else:
                transport = self._make_socket_transport(conn, protocol, waiter=waiter, extra=extra, server=server)
            
            try:
                await waiter
            except:
                transport.close()
                raise
        
        except BaseException as err:
            self.render_exc_async(err, [
                'Exception occured at ',
                self.__class__.__name__,
                '._accept_connection2\n',
                    ])
    
    def _add_reader(self, fd, callback, *args):
        if not self.running:
            raise RuntimeError('Event loop is cancelled.')
        
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
        if not self.running:
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
    
    def _add_writer(self, fd, callback, *args):
        if not self.running:
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
        if not self.running:
            return False
        try:
            key = self.selector.get_key(fd)
        except KeyError:
            return False
        
        mask = key.events
        reader, writer = key.data
        #remove both writer and connector.
        mask &= ~EVENT_WRITE
        if mask:
            self.selector.modify(fd, mask, (reader, None))
        else:
            self.selector.unregister(fd)
            
        if writer is not None:
            writer.cancel()
            return True
        
        return False

    if __debug__:
        def _ensure_fd_no_transport(self, fd):
            try:
                transport = self.transports[fd]
            except KeyError:
                return

            if not transport.is_closing():
                raise RuntimeError(f'File descriptor {fd!r} is used by transport {transport!r}')

        def add_reader(self, fd, callback, *args):
            self._ensure_fd_no_transport(fd)
            return self._add_reader(fd, callback, *args)

        def add_writer(self, fd, callback, *args):
            self._ensure_fd_no_transport(fd)
            return self._add_writer(fd, callback, *args)

    else:
        add_writer = _add_writer
        add_reader = _add_reader

    async def connect_accepted_socket(self, protocol_factory, sock, *, ssl=None):
        if not _is_stream_socket(sock):
            raise ValueError(f'A Stream Socket was expected, got {sock!r}')
        
        transport, protocol = await self._create_connection_transport(sock, protocol_factory, ssl, '', server_side=True)
        return transport, protocol
    
    async def create_connection(self, protocol_factory, host=None, port=None, *, ssl=None, family=0, proto=0, flags=0,
            sock=None, local_addr=None, server_hostname=None):
        
        if (server_hostname is not None) and (not ssl):
            raise ValueError('server_hostname is only meaningful with ssl')
        
        if (server_hostname is None) and ssl:
            # Use host as default for server_hostname. It is an error if host is empty or not set, e.g. when an
            # already-connected socket was passed or when only a port is given.  To avoid this error, you can pass
            # server_hostname='' -- this will bypass the hostname check. (This also means that if host is a numeric
            # IP/IPv6 address, we will attempt to verify that exact address; this will probably fail, but it is
            # possible to create a certificate for a specific IP address, so we don't judge it here.)
            if not host:
                raise ValueError('You must set server_hostname when using ssl without a host')
            server_hostname = host
        
        if (host is not None) or (port is not None):
            if (sock is not None):
                raise ValueError('host/port and sock can not be specified at the same time')
            
            f1 = self._ensure_resolved((host, port), family=family, type=module_socket.SOCK_STREAM, proto=proto,
                flags=flags)
            fs = [f1]
            if local_addr is not None:
                f2 = self._ensure_resolved(local_addr, family=family, type=module_socket.SOCK_STREAM, proto=proto,
                    flags = flags)
                fs.append(f2)
            else:
                f2 = None
            
            await Gatherer(self, fs)
            
            infos = f1.result()
            if not infos:
                raise OSError('getaddrinfo() returned empty list')
            if (f2 is not None):
                laddr_infos = f2.result()
                if not laddr_infos:
                    raise OSError('getaddrinfo() returned empty list')
            
            exceptions = []
            for family, type_, proto, cname, address in infos:
                try:
                    sock = module_socket.socket(family=family, type=type_, proto=proto)
                    sock.setblocking(False)
                    if (f2 is not None):
                        for element in laddr_infos:
                            laddr = element[4]
                            try:
                                sock.bind(laddr)
                                break
                            except OSError as err:
                                err = OSError(err.errno, f'error while attempting to bind on address {laddr!r}: {err.strerror.lower()}')
                                exceptions.append(err)
                        else:
                            sock.close()
                            sock = None
                            continue
                    
                    await self.sock_connect(sock, address)
                except OSError as err:
                    if (sock is not None):
                        sock.close()
                    exceptions.append(err)
                except:
                    if (sock is not None):
                        sock.close()
                    raise
                else:
                    break
            else:
                if len(exceptions) == 1:
                    raise exceptions[0]
                else:
                    # If they all have the same str(), raise one.
                    model = repr(exceptions[0])
                    all_exception=[repr(exception) for exception in exceptions]
                    if all(element == model for element in all_exception):
                        raise exceptions[0]
                    # Raise a combined exception so the user can see all
                    # the various error messages.
                    raise OSError(f'Multiple exceptions: {", ".join(all_exception)}')
        
        else:
            if sock is None:
                raise ValueError('host and port was not specified and no sock specified')
            if not _is_stream_socket(sock):
                # We allow AF_INET, AF_INET6, AF_UNIX as long as they are SOCK_STREAM.
                # We support passing AF_UNIX sockets even though we have
                # a dedicated API for that: create_unix_connection.
                # Disallowing AF_UNIX in this method, breaks backwards
                # compatibility.
                raise ValueError(f'A Stream Socket was expected, got {sock!r}')
        
        transport, protocol = await self._create_connection_transport(sock, protocol_factory, ssl, server_hostname)
        
        return transport, protocol


    async def _create_connection_transport(self, sock, protocol_factory, ssl, server_hostname, server_side=False):
        
        sock.setblocking(False)
        
        protocol = protocol_factory()
        waiter = Future(self)
        
        if ssl:
            sslcontext = None if isinstance(ssl, bool) else ssl
            transport  = self._make_ssl_transport(sock, protocol, sslcontext, waiter, server_side=server_side,
                server_hostname=server_hostname)
        else:
            transport = self._make_socket_transport(sock, protocol, waiter)
        
        try:
            await waiter
        except:
            transport.close()
            raise
        
        return transport, protocol

    # await it
    def getaddrinfo(self, host, port, *, family=0, type=0, proto=0, flags=0):
        return self.run_in_executor(alchemy_incendiary(
            module_socket.getaddrinfo, (host, port, family, type, proto, flags,),))
    
    # await it
    def getnameinfo(self, sockaddr, flags=0):
        return self.run_in_executor(alchemy_incendiary(
            module_socket.getnameinfo, (sockaddr, flags,),))

    def _ensure_resolved(self, address, *, family=0, type=module_socket.SOCK_STREAM, proto=0, flags=0):
        host = address[0]
        port = address[1]
        #adress might have more elements than 2
        info = _ipaddr_info(host, port, family, type, proto)
        if info is None:
            return self.getaddrinfo(host, port, family=family, type=type, proto=proto, flags=flags)
        
        # "host" is already a resolved IP.
        future = Future(self)
        future.set_result([info])
        return future

    # await it
    def sock_accept(self, sock):
        future = Future(self)
        self._sock_accept(future, False, sock)
        return future

    def _sock_accept(self, future, registered, sock):
        fd = sock.fileno()
        if registered:
            self.remove_reader(fd)
        if future.cancelled():
            return
        try:
            conn, address = sock.accept()
            conn.setblocking(False)
        except (BlockingIOError, InterruptedError):
            self.add_reader(fd, self._sock_accept, future, True, sock)
        except BaseException as err:
            future.set_exception(err)
        else:
            future.set_result((conn, address))
            
    async def sock_connect(self, sock, address):
        if not hasattr(module_socket, 'AF_UNIX') or (sock.family != module_socket.AF_UNIX):
            resolved = self._ensure_resolved(address, family=sock.family, proto=sock.proto)
            if not resolved.done():
                await resolved
            address = resolved.result()[0][4]
        
        future = Future(self)
        self._sock_connect(future, sock, address)
        return (await future)

    def _sock_connect(self, future, sock, address):
        fd=sock.fileno()
        try:
            sock.connect(address)
        except (BlockingIOError, InterruptedError):
            # Issue #23618: When the C function connect() fails with EINTR, the
            # connection runs in background. We have to wait until the socket
            # becomes writable to be notified when the connection succeed or
            # fails.
            self.add_writer(fd, self._sock_connect_cb, future, sock, address)
            future.add_done_callback(self._sock_connect_one(fd),)
        except BaseException as err:
            future.set_exception(err)
        else:
            future.set_result(None)
    
    class _sock_connect_one(object):
        __slots__ = ('fd',)
        def __init__(self, fd):
            self.fd=fd
        def __call__(self, future):
            future._loop.remove_writer(self.fd)
    
    def _sock_connect_cb(self, future, sock, address):
        if future.done():
            return
        
        try:
            err_number = sock.getsockopt(module_socket.SOL_SOCKET, module_socket.SO_ERROR)
            if err_number != 0:
                raise OSError(err_number, f'Connect call failed {address}')
        except (BlockingIOError, InterruptedError):
            # socket is still registered, the callback will be retried later
            pass
        except BaseException as err:
            future.set_exception(err)
        else:
            future.set_result(None)
    
    #await it
    def sock_recv(self, sock, n):
        future = Future(self)
        self._sock_recv(future, False, sock, n)
        return future

    def _sock_recv(self, future, registered, sock, n):
        fd = sock.fileno()
        if registered:
            self.remove_reader(fd)
        if future.cancelled():
            return
        try:
            data = sock.recv(n)
        except (BlockingIOError,InterruptedError):
            self.add_reader(fd, self._sock_recv, future,True, sock, n)
        except BaseException as err:
            future.set_exception(err)
        else:
            future.set_result(data)

    #await it 
    def sock_sendall(self, sock, data):
        future = Future(self)
        if data:
            self._sock_sendall(future, False, sock, data)
        else:
            future.set_result(None)
        return future

    def _sock_sendall(self, future, registered, sock, data):
        fd = sock.fileno()
        
        if registered:
            self.remove_writer(fd)
        if future.cancelled():
            return
        
        try:
            n = sock.send(data)
        except (BlockingIOError,InterruptedError):
            n = 0
        except BaseException as err:
            future.set_exception(err)
            return
        
        if n == len(data):
            future.set_result(None)
        else:
            if n:
                data = data[n:]
            self.add_writer(fd, self._sock_sendall, future,True, sock, data)
    
    #should be async
    def create_datagram_endpoint(self, protocol_factory, local_addr=None, remote_addr=None, *, family=0, proto=0,
            flags=0, reuse_address=None, reuse_port=None, allow_broadcast=None, sock=None):
        raise NotImplementedError

    def _create_server_getaddrinfo(self, host, port, family, flags):
        return self._ensure_resolved((host, port), family=family, type=module_socket.SOCK_STREAM, flags=flags)
    
    async def create_server(self, protocol_factory,host=None, port=None, *, family=module_socket.AF_UNSPEC,
            flags=module_socket.AI_PASSIVE, sock=None, backlog=100, ssl=None, reuse_address=None, reuse_port=None):
        if type(ssl) is bool:
            raise TypeError('ssl argument must be an SSLContext or None')

        if (host is not None) or (port is not None):
            if (sock is not None):
                raise ValueError('host/port and sock can not be specified at the same time')
            
            if (reuse_address is None):
                reuse_address = (os.name == 'posix' and sys.platform != 'cygwin')
            else:
                if (type(reuse_address) is not bool):
                    raise TypeError(f'`reuse_address` can be `None` or type bool ,got `{reuse_address!r}`')
            
            if reuse_port and (not hasattr(module_socket,'SO_REUSEPORT')):
                raise ValueError('reuse_port not supported by socket module')
            
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
            
            futures = {self._create_server_getaddrinfo(host, port, family=family, flags=flags) for host in hosts}
            
            try:
                while True:
                    done, pending = await WaitTillFirst(futures, self)
                    for future in done:
                        futures.remove(future)
                        infos = future.result()
                        
                        for info in infos:
                            af, socktype, proto, canonname, sa = info
                            
                            try:
                                sock = module_socket.socket(af, socktype, proto)
                            except module_socket.error:
                                continue
                            
                            sockets.append(sock)
                            
                            if reuse_address:
                                sock.setsockopt(module_socket.SOL_SOCKET, module_socket.SO_REUSEADDR, True)
                            
                            if reuse_port:
                                try:
                                    sock.setsockopt(module_socket.SOL_SOCKET, module_socket.SO_REUSEPORT, 1)
                                except OSError as err:
                                    raise ValueError('reuse_port not supported by socket module, SO_REUSEPORT defined '
                                        'but not implemented.') from err
                            
                            if (_HAS_IPv6 and (af == module_socket.AF_INET6) and \
                                    hasattr(module_socket, 'IPPROTO_IPV6')):
                                sock.setsockopt(module_socket.IPPROTO_IPV6, module_socket.IPV6_V6ONLY, True)
                            try:
                                sock.bind(sa)
                            except OSError as err:
                                raise OSError(err.errno, f'error while attempting to bind on address {sa!r}: '
                                    f'{err.strerror.lower()!s}') from None
                    
                    if futures:
                        continue
                    
                    break
            except:
                for sock in sockets:
                    sock.close()
                    
                for future in futures:
                    future.cancel()
                
                raise
            
        else:
            if sock is None:
                raise ValueError('Neither host/port nor sock were specified')
            
            if sock.type != module_socket.SOCK_STREAM:
                raise ValueError(f'A Stream Socket was expected, got {sock!r}')
            
            sockets = [sock]
        
        for sock in sockets:
            sock.setblocking(False)
        
        return Server(self, sockets, protocol_factory, ssl, backlog)
        
    #should be async
    def create_unix_connection(self, protocol_factory, path, *, ssl=None, sock=None, server_hostname=None):
        raise NotImplementedError
    
    #should be async
    def create_unix_server(self, protocol_factory, path=None, *, sock=None, backlog=100, ssl=None):
        raise NotImplementedError
    
    if IS_UNIX:
        async def connect_read_pipe(self, protocol, pipe):
            return await UnixReadPipeTransport(self, pipe, protocol)
        
        
        async def connect_write_pipe(self, protocol, pipe):
            return await UnixWritePipeTransport(self, pipe, protocol)
        
        async def subprocess_shell(self, cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                **kwargs):
            
            cmd_type = cmd.__class__
            if not issubclass(cmd_type, (bytes, str)):
                raise ValueError(f'`cmd` must be `bytes` or `str` instance, got {cmd_type.__name__}.')
            
            return await AsyncProcess(self, cmd, True, stdin, stdout, stderr, 0, **kwargs)
        
        async def subprocess_exec(self, program, popen_args=(), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, **kwargs):
            
            return await AsyncProcess(self, (program, *popen_args), False, stdin, stdout, stderr, 0, **kwargs)
    
    else:
        def connect_read_pipe(self, protocol, pipe):
            raise NotImplementedError
        
        def connect_write_pipe(self, protocol, pipe):
            raise NotImplementedError
        
        def subprocess_shell(self, protocol_factory, cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, **kwargs):
            raise NotImplementedError
        
        def subprocess_exec(self, protocol_factory, program, popen_args=(), stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs):
            raise NotImplementedError

executor.EventThread = EventThread
futures.EventThread = EventThread

del module_time
del subprocess
del IS_UNIX
del futures
del executor
del DocProperty
del DOCS_ENABLED
