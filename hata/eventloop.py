# -*- coding: utf-8 -*-
__all__ = ('Cycler', 'EventThread', 'ThreadSyncerCTX', )

import sys, errno, weakref, subprocess, os
import socket as module_socket
import time as module_time
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ
from threading import current_thread, Thread, Event
from heapq import heappop, heappush
from collections import deque

from .dereaddons_local import alchemy_incendiary
from .futures import Future, Task, gather, render_exc_to_list, iscoroutine, \
    FutureAsyncWrapper, WaitTillFirst
from .py_transprotos import SSLProtocol, _SelectorSocketTransport
from .executor import Executor

import threading
from .futures import _ignore_frame
_ignore_frame(__spec__.origin           , '_run'            , 'self.func(*self.args)'           ,)
_ignore_frame(__spec__.origin           , 'run'             , 'handle._run()'                   ,)
_ignore_frame(threading.__spec__.origin , '_bootstrap'      , 'self._bootstrap_inner()'         ,)
_ignore_frame(threading.__spec__.origin , '_bootstrap_inner', 'self.run()'                      ,)
del threading, _ignore_frame

class Handle(object):
    __slots__ = ('func', 'args', 'cancelled',)

    def __init__(self, func, args):
        self.func       = func
        self.args       = args
        self.cancelled  = False

    def __repr__(self):
        if self.cancelled:
            return f'<{self.__class__.__name__} cancelled>'
        return f'<{self.__class__.__name__} function={self.func!r}({", ".join([repr(arg) for arg in self.args])})>'

    def cancel(self):
        if not self.cancelled:
            self.cancelled  = True
            self.func       = None
            self.args       = None

    def _run(self):
        try:
            self.func(*self.args)
        except BaseException as err:
            current_thread().render_exc_async(err,[
                'Exception occured at ',
                self.__class__.__name__,
                '._run\nAt running ',
                repr(self.func),
                '\n',
                    ])

        self = None  # Needed to break cycles when an exception occurs.

class TimerHandle(Handle):
    __slots__ = ('when',)

    def __init__(self, when, func, args):
        self.func       = func
        self.args       = args
        self.cancelled  = False
        self.when       = when

    def __repr__(self):
        if self.cancelled:
            return f'<{self.__class__.__name__} cancelled>'
        return f'<{self.__class__.__name__} function={self.func!r}({", ".join([repr(arg) for arg in self.args])}) when={self.when}>'

    def __hash__(self):
        return hash(self.when)

    def __gt__(self, other):
        return self.when>other.when

    def __ge__(self, other):
        if self.when>other.when:
            return True
        return self.__eq__(other)

    def __eq__(self, other):
        if type(self) is type(other):
            return (self.when       == other.when       and
                    self.func       == other.func       and
                    self.args       == other.args       and
                    self.cancelled  == other.cancelled      )
        return NotImplemented

    def __ne__(self, other):
        if type(self) is type(other):
            return (self.when       != other.when       or
                    self.func       != other.func       or
                    self.args       != other.args       or
                    self.cancelled  != other.cancelled      )
        return NotImplemented

    def __le__(self,other):
        if self.when<other.when:
            return True
        return self.__eq__(other)

    def __lt__(self,other):
        return self.when<other.when

class Cycler(object):
    __slots__=('cycletime', 'funcs', 'handle', 'loop',)
    def __init__(self,loop,cycletime,*funcs):
        if not loop.running:
            raise RuntimeError('Event loop is closed.')
        self.loop=loop
        self.funcs=list(funcs)
        self.cycletime=cycletime
        if current_thread() is loop:
            self.handle=self.loop.call_later(cycletime,self._run)
            return
        
        self.handle=None
        loop.call_soon(self._start_handle_threadsafe)
        loop.wakeup()

    def _start_handle_threadsafe(self):
        self.handle=self.loop.call_later(self.cycletime,self._run)

    def _run(self):
        for func in self.funcs:
            try:
                func(self)
            except BaseException as err:
                self.loop.render_exc_async(err,[
                    self.__class__.__name__,
                    ' exception occured\nat calling ',
                    repr(func),
                    '\n',
                        ])
        
        self.handle=self.loop.call_later(self.cycletime,self._run)

    def __repr__(self):
        result=[self.__class__.__name__,'(',repr(self.loop),', ',str(self.cycletime)]
        for func in self.funcs:
            result.append(', ')
            result.append(repr(func))
        return ''.join(result)

    def cancel(self):
        loop=self.loop
        if current_thread() is loop:
            self._cancel()
            return
        
        loop.call_soon_threadsafe(self._cancel)

    def _cancel(self):
        handle=self.handle
        if handle is None:
            return
        handle.cancel()
        self.handle=None

    def call_now(self):
        loop=self.loop
        if current_thread() is loop:
            self._call_now()
            return
        
        loop.call_soon_threadsafe(self._call_now)

    def _call_now(self):
        handle=self.handle
        if handle is not None:
            handle.cancel()
        self._run()

    def call_now_threadsafe(self):
        self.loop.call_soon_threadsafe(self.call_now)

    def reschedule(self):
        loop=self.loop
        if current_thread() is loop:
            self._reschedule()
            return
        
        loop.call_soon_threadsafe(self._reschedule)

    def _reschedule(self):
        handle=self.handle
        if handle is not None:
            handle.cancel()
        self.handle=self.loop.call_later(self.cycletime,self._run)

    def reschedule_threadsafe(self):
        self.loop.call_soon_threadsafe(self.reschedule)

    @property
    def running(self):
        return (self.handle is not None)

    def set_cycletime(self,value):
        if type(value) is not float:
            value=float(value)
        if value<=0.:
            raise ValueError('cycletime cannot be 0. or less')
        self.cycletime=value

    def append(self,obj):
        loop=self.loop
        if current_thread() is loop:
            self.funcs.append(obj)
            return
        
        loop.call_soon_threadsafe(self.funcs.append,obj)

    def remove(self,obj):
        loop=self.loop
        if current_thread() is loop:
            self.funcs.remove(obj)
            return
        
        loop.call_soon_threadsafe(self.funcs.remove,obj)

    def time_left(self):
        handle=self.handle
        if handle is None:
            return -1. #wont be be called
        at=handle.when-self.loop.time()
        if at<0.:
            return 0. #right now
        return at

class ThreadSyncerCTX(object):
    __slots__=('loop', 'enter_event', 'exit_event')

    def __init__(self,loop):
        self.loop       = loop
        self.enter_event= Event()
        self.exit_event = Event()

    def __enter__(self):
        loop=self.loop
        if loop.running:
            handle=Handle(self._give_control_cb,())
            loop._ready.append(handle)
            loop.wakeup()
            self.enter_event.wait()
        
        return self

    def __exit__(self,exc_type,exc_val,exc_tb):
        self.exit_event.set()

    def _give_control_cb(self):
        self.enter_event.set()
        self.exit_event.wait()

_HAS_IPv6=hasattr(module_socket,'AF_INET6')

def _ipaddr_info(host, port, family, type, proto):
    # Try to skip getaddrinfo if "host" is already an IP. Users might have
    # handled name resolution in their own code and pass in resolved IPs.
    if not hasattr(module_socket, 'inet_pton'):
        return
    
    if proto not in (0,module_socket.IPPROTO_TCP,module_socket.IPPROTO_UDP) or (host is None):
        return
    
    if type == module_socket.SOCK_STREAM:
        proto = module_socket.IPPROTO_TCP
    elif type == module_socket.SOCK_DGRAM:
        proto = module_socket.IPPROTO_UDP
    else:
        return
    
    if port is None:
        port = 0
    elif isinstance(port,bytes) and port==b'':
        port = 0
    elif isinstance(port,str) and port=='':
        port = 0
    else:
        # If port's a service name like "http", don't skip getaddrinfo.
        try:
            port=int(port)
        except (TypeError,ValueError):
            return
    
    if family==module_socket.AF_UNSPEC:
        afs=[module_socket.AF_INET]
        if _HAS_IPv6:
            afs.append(module_socket.AF_INET6)
    else:
        afs=[family]
    
    if isinstance(host, bytes):
        host = host.decode('idna')
    
    if '%' in host:
        return
    
    for af in afs:
        try:
            module_socket.inet_pton(af,host)
            # The host has already been resolved.
            return af,type,proto,'',(host,port)
        except OSError:
            pass
    # "host" is not an IP address.

def _is_dgram_socket(sock):
    return (sock.type&module_socket.SOCK_DGRAM)==module_socket.SOCK_DGRAM

def _is_stream_socket(sock):
    return (sock.type&module_socket.SOCK_STREAM)==module_socket.SOCK_STREAM


_OLD_AGEN_HOOKS=sys.get_asyncgen_hooks()

def _asyncgen_firstiter_hook(self,agen):
    try:
        loop=current_thread()
    except AttributeError:
        firstiter=_OLD_AGEN_HOOKS.firstiter
        if firstiter is not None:
            firstiter(agen)
    else:
        if loop._asyncgens_shutdown_called:
            pass
        
        loop._asyncgens.add(agen)

def _asyncgen_finalizer_hook(agen):
    try:
        loop=current_thread()
    except AttributeError:
        finalizer=_OLD_AGEN_HOOKS.finalizer
        if finalizer is not None:
            finalizer(agen)
    else:
        loop._asyncgens.discard(agen)
        if loop.running:
            Task(agen.aclose(),loop)
            loop.wakeup()

sys.set_asyncgen_hooks(firstiter=_asyncgen_firstiter_hook,
                       finalizer=_asyncgen_finalizer_hook)


if sys.platform == 'win32':
    #If windows select raises OSError, we cacnnot do anything, but
    #if it it raises ValueError, we can increases windows select()
    #from 500~ till tze hard limit, with sharding up it's polls
    
    from select import select
    MAX_FD_S    = 500 #512 is the actual amount?
    MAX_SLEEP   = 0.001
    EMPTY       = []
    
    class DefaultSelector(DefaultSelector):
        def _select(self,r,w,_,timeout=None):
            try:
                result_r,result_w,result_x = select(r,w,w,timeout)
            except ValueError:
                default_reader=current_thread()._ssock
                r.remove(default_reader.fileno())
                
                sharded_r=[]
                sharded_w=[]
                
                sharded=[(sharded_r,sharded_w,),]
                
                count=0
                for reader in r:
                    if count==MAX_FD_S:
                        sharded_r=[reader]
                        sharded_w=[]
                        sharded.append((sharded_r,sharded_w),)
                        count=1
                    else:
                        sharded_r.append(reader)
                        count=count+1
                
                for writer in w:
                    if count==MAX_FD_S:
                        sharded_r=[]
                        sharded_w=[writer]
                        sharded.append((sharded_r,sharded_w),)
                        count=1
                    else:
                        sharded_w.append(writer)
                        count=count+1
                
                collected_r=[]
                collected_w=[]
                
                r.add(default_reader.fileno())
                
                for iter_r,iter_w in sharded:
                    try:
                        result_r,result_w,result_x=select(iter_r,iter_w,iter_w,0.0)
                    except OSError:
                        remove=[]
                        for reader in iter_r:
                            try:
                                l=[reader]
                                result_r,result_w,result_x=select(l,EMPTY,EMPTY,0.0)
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
                                l=[writer]
                                result_r,result_w,result_x=select(EMPTY,l,l,0.0)
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
                        timeout=MAX_SLEEP
                    elif timeout<0.0:
                        timeout=0.0
                    elif timeout>MAX_SLEEP:
                        timeout=MAX_SLEEP
                    
                    result_r,result_w,result_x=select([default_reader],EMPTY,EMPTY,timeout)
                    collected_r.extend(result_r)
                
                return collected_r,collected_w,EMPTY
            
            except OSError:
                collected_r=[]
                collected_w=[]
                do_later_r=[]
                do_later_w=[]
                remove=[]
                for reader in r:
                    try:
                        l=[reader]
                        result_r,result_w,result_x=select(l,EMPTY,EMPTY,0.0)
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
                        l=[writer]
                        result_r,result_w,result_x=select(EMPTY,l,l,0.0)
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
                    return collected_r,collected_w,EMPTY
                
                result_r,result_w,result_x = select(r,w,w,timeout)
                result_w.extend(result_x)
                return result_r,result_w,EMPTY
            else:
                result_w.extend(result_x)
                return result_r,result_w,EMPTY

class Server(object):
    __slots__ = ('active_count', 'backlog', 'loop', 'protocol_factory',
        'serving', 'sockets', 'ssl_context', 'waiters')
    
    def __init__(self, loop, sockets, protocol_factory, ssl_context, backlog):
        self.loop               = loop
        self.sockets            = sockets
        self.active_count       = 0
        self.waiters            = []
        self.protocol_factory   = protocol_factory
        self.backlog            = backlog
        self.ssl_context        = ssl_context
        self.serving            = False
    
    def __repr__(self):
        return f'<{self.__class__.__name__} sockets={self.sockets!r}>'

    def _attach(self):
        self.active_count += 1

    def _detach(self):
        active_count=self.active_count-1
        self.active_count=active_count
        if active_count:
            return
        
        if (self.sockets is None):
            self._wakeup()

    def _wakeup(self):
        waiters = self.waiters
        self.waiters = None
        for waiter in waiters:
            if not waiter.done():
                waiter.set_result(waiter)

    def close(self):
        sockets = self.sockets
        if sockets is None:
            return
        
        self.sockets=None
        
        loop=self.loop
        for sock in sockets:
            loop._stop_serving(sock)
        
        self.serving=False
        
        if self.active_count==0:
            self._wakeup()

    async def start(self):
        if self.serving:
            return
        
        self.serving = True
        
        protocol_factory=self.protocol_factory
        ssl_context=self.ssl_context
        backlog=self.backlog
        loop=self.loop
        
        for sock in self.sockets:
            sock.listen(backlog)
            loop._start_serving(protocol_factory,sock,ssl_context,self,backlog)
        
        # Skip ready ietration cycle, so all the callbacks added up ^ will run down
        future=Future(loop)
        future.set_result(None)
        await future

    async def wait_closed(self):
        if self.sockets is None:
            return
        
        waiters=self.waiters
        if waiters is None:
            return
        
        waiter = Future(self.loop)
        waiters.append(waiter)
        await waiter

class EventThreadCTXManager(object):
    __slots__=('thread', 'waiter',)
    def __init__(self,thread):
        self.thread=thread
        self.waiter=Event()

    def __enter__(self):
        thread=self.thread
        thread.running = True
        
        ssock,csock=module_socket.socketpair()
        ssock.setblocking(False)
        csock.setblocking(False)
        thread._ssock=ssock
        thread._csock=csock
        thread._internal_fds+=1
        thread.add_reader(ssock.fileno(),thread._read_from_self)
        
        self.waiter.set()

    def __exit__(self,exc_type,exc_val,exc_tb):
        thread=self.thread
        self.thread=None
        
        thread.running = False
        thread.remove_reader(thread._ssock.fileno())
        thread._ssock.close()
        thread._ssock = None
        thread._csock.close()
        thread._csock = None
        thread._internal_fds -= 1
        
        thread._ready.clear()
        thread._scheduled.clear()
        
        thread.cancel_executors()
        
        selector=thread.selector
        if selector is not None:
            selector.close()
            thread.selector = None

class EventThreadType(type):
    def __call__(cls,daemon=False,name=None):
        obj=Thread.__new__(cls)
        cls.__init__(obj)
        Thread.__init__(obj,daemon=daemon,name=name)
        obj.ctx=EventThreadCTXManager(obj)
        Thread.start(obj)
        obj.ctx.waiter.wait()
        return obj

class EventThread(Executor,Thread,metaclass=EventThreadType):
    time=module_time.monotonic
    _clock_resolution = module_time.get_clock_info('monotonic').resolution
    __slots__=('__dict__', '__weakref__', '_asyncgens',
        '_asyncgens_shutdown_called', '_csock', '_internal_fds', '_ready',
        '_scheduled', '_ssock', 'ctx', 'current_task', 'running', 'selector',
        'should_run', 'transports',)

    def __init__(self):
        Executor.__init__(self)
        self.should_run = True
        self.running    = False
        self.selector   = DefaultSelector()
        
        self._ready = deque()
        self._scheduled = []
        self.current_task=None
        self._internal_fds = 0
        
        self._asyncgens = weakref.WeakSet()
        self._asyncgens_shutdown_called=False
        self.transports = weakref.WeakValueDictionary()
        
        self._ssock=None
        self._csock=None

    def __repr__(self):
        result=['<',self.__class__.__name__,'(',self._name]
        self.is_alive() # easy way to get ._is_stopped set when appropriate
        if self._is_stopped:
            result.append(' stopped')
        else:
            result.append(' started')
        
        if self._daemonic:
            result.append(' daemon')
        
        ident=self._ident
        if ident is not None:
            result.append(' ident=')
            result.append(str(ident))

        frees=len(self.free_executors)
        used=len(self.running_executors)+len(self.running_id_executors)+len(self.claimed_executors)
        
        result.append(' executor info: free=')
        result.append(str(self.free_executor_count))
        result.append(', used=')
        result.append(str(self.used_executor_count))
        result.append(', keep=')
        result.append(str(self.keep_executor_count))
        result.append(')>')

        return ''.join(result)


    def call_later(self,delay,callback,*args):
        if self.running:
            handle=TimerHandle(self.time()+delay,callback,args)
            heappush(self._scheduled,handle)
            return handle

    def call_at(self,when,callback,*args):
        if self.running:
            handle=TimerHandle(when,callback,args)
            heappush(self._scheduled,handle)
            return handle

    def call_soon(self,func,*args):
        if self.running:
            handle=Handle(func,args)
            self._ready.append(handle)
            return handle

    def call_soon_threadsafe(self,func,*args):
        if self.running:
            handle=Handle(func,args)
            self._ready.append(handle)
            self.wakeup()
            return handle

    def cycle(self,cycletime,*funcs):
        return Cycler(self,cycletime,*funcs)

    def _add_callback(self,handle):
        if handle.cancelled:
            return
        self._ready.append(handle)

    def _schedule_callbacks(self,future):
        if self.running:
            callbacks=future._callbacks
            
            while callbacks:
                handle=Handle(callbacks.pop(),(future,))
                self._ready.append(handle)

    def create_future(self):
        return Future(self)

    def create_task(self,coro):
        return Task(coro,self)

    def create_task_threadsafe(self,coro):
        task=Task(coro,self)
        self.wakeup()
        return task

    def enter(self):
        return ThreadSyncerCTX(self)

    # Ensures a future, coroutine, or an awaitable on this loop.
    # Returns a Future or a Task bound to this thread.
    def ensure_future(self,coro_or_future):
        if iscoroutine(coro_or_future):
            return Task(coro_or_future,self)
        
        if isinstance(coro_or_future,Future):
            if coro_or_future._loop is not self:
                coro_or_future=FutureAsyncWrapper(coro_or_future,self)
            return coro_or_future
        
        type_=type(coro_or_future)
        if hasattr(type_,'__await__'):
            return Task(type_.__await__(coro_or_future),self)

        raise TypeError('A Future, a coroutine or an awaitable is required.')

    # Ensures a future, coroutine, or an awaitable on this loop.
    # If the future is bound to an another thread, it wakes self up.
    # Returns a Future or a Task bound to this thread.
    def ensure_future_threadsafe(self,coro_or_future):
        if iscoroutine(coro_or_future):
            task=Task(coro_or_future,self)
            self.wakeup()
            return task

        if isinstance(coro_or_future,Future):
            if coro_or_future._loop is not self:
                coro_or_future=FutureAsyncWrapper(coro_or_future,self)
            return coro_or_future

        type_=type(coro_or_future)
        if hasattr(type_,'__await__'):
            task=Task(type_.__await__(coro_or_future),self)
            self.wakeup()
            return task

        raise TypeError('A Future, a coroutine or an awaitable is required.')
    
    def run(self):
        with self.ctx:
            key     = None
            fileobj = None
            reader  = None
            writer  = None
            
            ready       = self._ready #use thread safe type with no lock
            scheduled   = self._scheduled #these can be added only from this thread
            
            while self.should_run:
                timeout=self.time()+self._clock_resolution #calculate limit
                while scheduled: #handle 'later' callbacks that are ready.
                    handle=scheduled[0]
                    if handle.cancelled:
                        heappop(scheduled)
                        continue
                    
                    if handle.when>=timeout:
                        break
                    
                    ready.append(handle)
                    heappop(scheduled)
                
                if ready:
                    timeout=0.
                elif scheduled:
                    #compute the desired timeout.
                    timeout=scheduled[0].when-self.time()
                else:
                    timeout=None
                
                event_list=self.selector.select(timeout)
                if event_list:
                    for key,mask in event_list:
                        fileobj=key.fileobj
                        reader,writer=key.data
                        if (reader is not None) and (mask&EVENT_READ):
                            if reader.cancelled:
                                self.remove_reader(fileobj)
                            else:
                                self._add_callback(reader)
                        if (writer is not None) and (mask&EVENT_WRITE):
                            if writer.cancelled:
                                self.remove_writer(fileobj)
                            else:
                                self._add_callback(writer)
                    
                    key     = None
                    fileobj = None
                    reader  = None
                    writer  = None
                    
                event_list=None
                
                #process callbacks
                for _ in range(len(ready)):
                    handle=ready.popleft()
                    if not handle.cancelled:
                        handle._run()
                handle=None  #remove from locals (they said needed)

    if __debug__:
        def render_exc_async(self,exception,before=None,after=None,file=None):
            future=self.run_in_executor(alchemy_incendiary(self._render_exc_sync,(exception,before,after,file),))
            future.__silence__()
            return future

        def render_exc_maybe_async(self,exception,before=None,after=None,file=None):
            if isinstance(current_thread(),EventThread):
                future=self.run_in_executor(alchemy_incendiary(self._render_exc_sync,(exception,before,after,file),))
                future.__silence__()
            else:
                self._render_exc_sync(exception,before,after,file)

    else:
        def render_exc_async(self,exception,before=None,after=None,file=None):
            return self.run_in_executor(alchemy_incendiary(self._render_exc_sync,(exception,before,after,file),))

        def render_exc_maybe_async(self,exception,before=None,after=None,file=None):
            if isinstance(current_thread(),EventThread):
                self.run_in_executor(alchemy_incendiary(self._render_exc_sync,(exception,before,after,file),))
            else:
                self._render_exc_sync(exception,before,after,file)


    @staticmethod
    def _render_exc_sync(exception,before,after,file):
        if before is None:
            extracted=[]
        elif type(before) is str:
            extracted=[before]
        elif type(before) is list:
            extracted=before
        else:
            # ignore exception cases
            extracted=[before.__repr__()]
        
        render_exc_to_list(exception,extend=extracted)
        
        if after is None:
            pass
        elif type(after) is str:
            extracted.append(after)
        elif type(after) is list:
            extracted.extend(after)
        else:
            extracted.append(repr(after))
        
        if file is None:
            # ignore exception cases
            file=sys.stderr
        
        file.write(''.join(extracted))

    def stop(self):
        if self.should_run:
            if current_thread() is self:
                self._stop()
            else:
                self.call_soon(self._stop)
                self.wakeup()

    def _stop(self):
        self.release_executors()
        self.should_run=False

    async def shutdown_asyncgens(self):
        self._asyncgens_shutdown_called = True
        
        if not len(self._asyncgens):
            return
        
        closing_agens=list(self._asyncgens)
        self._asyncgens.clear()
        
        results = await gather((ag.aclose() for ag in closing_agens),self)
        
        for result,agen in zip(results,closing_agens):
            exception=result.exception
            if exception is not None:
                extracted=[
                    'Exception occured during shutting down asyncgen:\n',
                    repr(agen),
                        ]
                render_exc_to_list(exception,extend=extracted)
                sys.stderr.write(''.join(extracted))

    def _asyncgen_finalizer_hook(self,agen):
        self._asyncgens.discard(agen)
        if self.running:
            Task(agen.aclose(),self)
            self.wakeup()

    def _asyncgen_firstiter_hook(self,agen):
        if self._asyncgens_shutdown_called:
            pass #remove it later
        
        self._asyncgens.add(agen)

    def _make_socket_transport(self,sock,protocol,waiter=None,*,extra=None,server=None):
        return _SelectorSocketTransport(self,sock,protocol,waiter,extra,server)

    def _make_ssl_transport(self, rawsock, protocol, sslcontext, waiter=None,
                            *, server_side=False, server_hostname=None,
                            extra=None, server=None):

        ssl_protocol = SSLProtocol(self,protocol,sslcontext,waiter,server_side,server_hostname)
        _SelectorSocketTransport(self,rawsock,ssl_protocol,extra=extra,server=server)
        return ssl_protocol.app_transport

    def _process_self_data(self, data):
        pass

    def _read_from_self(self):
        while True:
            try:
                data=self._ssock.recv(4096)
                if not data:
                    break
                self._process_self_data(data)
            except InterruptedError:
                continue
            except BlockingIOError:
                break

    #_write_to_self, but wakeup is way more correct name
    def wakeup(self):
        #called from different threads, to wake up this one
        csock=self._csock
        if csock is not None:
            try:
                csock.send(b'\0')
            except OSError:
                pass

    def _start_serving(self,protocol_factory,sock,sslcontext=None,server=None,backlog=100):
        self.add_reader(sock.fileno(),self._accept_connection,protocol_factory,sock,sslcontext,server,backlog)

    def _stop_serving(self,sock):
        self.remove_reader(sock.fileno())
        sock.close()

    def _accept_connection(self, protocol_factory, sock,
                           sslcontext=None, server=None, backlog=100):
        # This method is only called once for each event loop tick where the
        # listening socket has triggered an EVENT_READ. There may be multiple
        # connections waiting for an .accept() so it is called in a loop.
        # See https://bugs.python.org/issue27906 for more details.
        for _ in range(backlog):
            try:
                conn,addr = sock.accept()
                conn.setblocking(False)
            except (BlockingIOError, InterruptedError, ConnectionAbortedError):
                # Early exit because the socket accept buffer is empty.
                return None
            except OSError as err:
                # There's nowhere to send the error, so just log it.
                if err.errno in (errno.EMFILE,errno.ENFILE,errno.ENOBUFS,errno.ENOMEM):
                    # Some platforms (e.g. Linux keep reporting the FD as
                    # ready, so we remove the read handler temporarily.
                    # We'll try again in a while.
                    self.render_exc_async(err,before=[
                        'Exception occured at',
                        repr(self),
                        '._accept_connection\n',
                            ])
                    
                    self.remove_reader(sock.fileno())
                    self.call_later(1.,self._start_serving,protocol_factory,sock,sslcontext,server,backlog)
                else:
                    raise  # The event loop will catch, log and ignore it.
            else:
                extra = {'peername': addr}
                coro = self._accept_connection2(protocol_factory,conn,extra,sslcontext,server)
                Task(coro,self)

    async def _accept_connection2(self,protocol_factory,conn,extra,sslcontext=None,server=None):
        try:
            protocol = protocol_factory()
            waiter   = Future(self)
            if sslcontext:
                transport=self._make_ssl_transport(conn,protocol,sslcontext,waiter=waiter,server_side=True,extra=extra,server=server)
            else:
                transport=self._make_socket_transport(conn,protocol,waiter=waiter,extra=extra,server=server)
            
            try:
                await waiter
            except:
                transport.close()
                raise
        
        except BaseException as err:
            self.render_exc_async(err,[
                'Exception occured at ',
                self.__class__.__name__,
                '._accept_connection2\n',
                    ])

    def _add_reader(self,fd,callback,*args):
        if not self.running:
            raise RuntimeError('Event loop is cancelled.')
        
        handle=Handle(callback,args)
        try:
            key = self.selector.get_key(fd)
        except KeyError:
            self.selector.register(fd,EVENT_READ,(handle,None))
        else:
            mask=key.events
            reader,writer=key.data
            self.selector.modify(fd,mask|EVENT_READ,(handle, writer))
            if reader is not None:
                reader.cancel()

    def remove_reader(self,fd):
        if not self.running:
            return False
        try:
            key=self.selector.get_key(fd)
        except KeyError:
            return False

        mask=key.events
        reader,writer=key.data
        mask &= ~EVENT_READ
        
        if mask:
            self.selector.modify(fd,mask,(None,writer))
        else:
            self.selector.unregister(fd)
        
        if reader is not None:
            reader.cancel()
            return True
        
        return False

    def _add_writer(self,fd,callback,*args):
        if not self.running:
            raise RuntimeError('Event loop is cancelled.')
        
        handle=Handle(callback,args)
        try:
            key=self.selector.get_key(fd)
        except KeyError:
            self.selector.register(fd,EVENT_WRITE,(None,handle))
            return

        mask=key.events
        reader,writer=key.data
        
        self.selector.modify(fd,mask|EVENT_WRITE,(reader,handle))
        if writer is not None:
            writer.cancel()

    def remove_writer(self, fd):
        if not self.running:
            return False
        try:
            key = self.selector.get_key(fd)
        except KeyError:
            return False
        
        mask=key.events
        reader,writer=key.data
        #remove both writer and connector.
        mask &= ~EVENT_WRITE
        if mask:
            self.selector.modify(fd,mask,(reader,None))
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

        def add_reader(self,fd,callback,*args):
            self._ensure_fd_no_transport(fd)
            return self._add_reader(fd,callback,*args)

        def add_writer(self,fd,callback,*args):
            self._ensure_fd_no_transport(fd)
            return self._add_writer(fd,callback,*args)

    else:
        add_writer=_add_writer
        add_reader=_add_reader

    async def connect_accepted_socket(self,protocol_factory,sock,*,ssl=None):
        if not _is_stream_socket(sock):
            raise ValueError(f'A Stream Socket was expected, got {sock!r}')
        
        transport,protocol = await self._create_connection_transport(sock,protocol_factory,ssl,'',server_side=True)
        return transport,protocol
    
    async def create_connection(self,protocol_factory,host=None,port=None,*,
            ssl=None,family=0,proto=0,flags=0,sock=None,local_addr=None,
            server_hostname=None):
        
        if (server_hostname is not None) and (not ssl):
            raise ValueError('server_hostname is only meaningful with ssl')
        
        if (server_hostname is None) and ssl:
            # Use host as default for server_hostname.  It is an error
            # if host is empty or not set, e.g. when an
            # already-connected socket was passed or when only a port
            # is given.  To avoid this error, you can pass
            # server_hostname='' -- this will bypass the hostname
            # check.  (This also means that if host is a numeric
            # IP/IPv6 address, we will attempt to verify that exact
            # address; this will probably fail, but it is possible to
            # create a certificate for a specific IP address, so we
            # don't judge it here.)
            if not host:
                raise ValueError('You must set server_hostname when using ssl without a host')
            server_hostname = host

        if (host is not None) or (port is not None):
            if (sock is not None):
                raise ValueError('host/port and sock can not be specified at the same time')
            
            f1=self._ensure_resolved((host,port),family=family,type=module_socket.SOCK_STREAM,proto=proto,flags=flags)
            fs=[f1]
            if local_addr is not None:
                f2=self._ensure_resolved(local_addr,family=family,type=module_socket.SOCK_STREAM,proto=proto,flags=flags)
                fs.append(f2)
            else:
                f2=None
            
            await gather(fs,self)
            
            infos = f1.result()
            if not infos:
                raise OSError('getaddrinfo() returned empty list')
            if (f2 is not None):
                laddr_infos=f2.result()
                if not laddr_infos:
                    raise OSError('getaddrinfo() returned empty list')
            
            exceptions = []
            for family,type,proto,cname,address in infos:
                try:
                    sock=module_socket.socket(family=family,type=type,proto=proto)
                    sock.setblocking(False)
                    if (f2 is not None):
                        for element in laddr_infos:
                            laddr=element[4]
                            try:
                                sock.bind(laddr)
                                break
                            except OSError as err:
                                err=OSError(err.errno,f'error while attempting to bind on address {laddr!r}: {err.strerror.lower()}')
                                exceptions.append(err)
                        else:
                            sock.close()
                            sock=None
                            continue
                    
                    await self.sock_connect(sock,address)
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
                if len(exceptions)==1:
                    raise exceptions[0]
                else:
                    # If they all have the same str(), raise one.
                    model=repr(exceptions[0])
                    all_exception=[repr(exception) for exception in exceptions]
                    if all(element==model for element in all_exception):
                        raise exceptions[0]
                    # Raise a combined exception so the user can see all
                    # the various error messages.
                    raise OSError(f'Multiple exceptions: {", ".join(all_exception)}')
        
        else:
            if sock is None:
                raise ValueError('host and port was not specified and no sock specified')
            if not _is_stream_socket(sock):
                # We allow AF_INET, AF_INET6, AF_UNIX as long as they
                # are SOCK_STREAM.
                # We support passing AF_UNIX sockets even though we have
                # a dedicated API for that: create_unix_connection.
                # Disallowing AF_UNIX in this method, breaks backwards
                # compatibility.
                raise ValueError(f'A Stream Socket was expected, got {sock!r}')
        
        transport,protocol = await self._create_connection_transport(sock,protocol_factory,ssl,server_hostname)
        
        return transport,protocol


    async def _create_connection_transport(self,sock,protocol_factory,ssl,server_hostname,server_side=False):
        
        sock.setblocking(False)
        
        protocol= protocol_factory()
        waiter  = Future(self)
        
        if ssl:
            sslcontext = None if isinstance(ssl,bool) else ssl
            transport  = self._make_ssl_transport(sock,protocol,sslcontext,waiter,server_side=server_side,server_hostname=server_hostname)
        else:
            transport = self._make_socket_transport(sock,protocol,waiter)
        
        try:
            await waiter
        except:
            transport.close()
            raise
        
        return transport,protocol

    #await it
    def getaddrinfo(self,host,port,*,family=0,type=0,proto=0,flags=0):
        return self.run_in_executor(alchemy_incendiary(
            module_socket.getaddrinfo,(host,port,family,type,proto,flags,),))

    #await it
    def getnameinfo(self,sockaddr,flags=0):
        return self.run_in_executor(alchemy_incendiary(
            module_socket.getnameinfo,(sockaddr,flags,),))

    def _ensure_resolved(self,address,*,family=0,type=module_socket.SOCK_STREAM,proto=0,flags=0):
        host=address[0]
        port=address[1]
        #adress might have more elements than 2
        info=_ipaddr_info(host,port,family,type,proto)
        if info is None:
            return self.getaddrinfo(host,port,family=family,type=type,proto=proto,flags=flags)
        
        # "host" is already a resolved IP.
        future=Future(self)
        future.set_result([info])
        return future

    #await it
    def sock_accept(self,sock):
        future=Future(self)
        self._sock_accept(future,False,sock)
        return future

    def _sock_accept(self,future,registered,sock):
        fd=sock.fileno()
        if registered:
            self.remove_reader(fd)
        if future.cancelled():
            return
        try:
            conn,address=sock.accept()
            conn.setblocking(False)
        except (BlockingIOError,InterruptedError):
            self.add_reader(fd,self._sock_accept,future,True,sock)
        except BaseException as err:
            future.set_exception(err)
        else:
            future.set_result((conn, address))
            
    async def sock_connect(self,sock,address):
        if not hasattr(module_socket,'AF_UNIX') or sock.family!=module_socket.AF_UNIX:
            resolved=self._ensure_resolved(address,family=sock.family,proto=sock.proto)
            if not resolved.done():
                await resolved
            address=resolved.result()[0][4]

        future=Future(self)
        self._sock_connect(future,sock,address)
        return (await future)

    def _sock_connect(self,future,sock,address):
        fd=sock.fileno()
        try:
            sock.connect(address)
        except (BlockingIOError, InterruptedError):
            # Issue #23618: When the C function connect() fails with EINTR, the
            # connection runs in background. We have to wait until the socket
            # becomes writable to be notified when the connection succeed or
            # fails.
            self.add_writer(fd,self._sock_connect_cb,future,sock,address)
            future.add_done_callback(self._sock_connect_one(fd),)
        except BaseException as err:
            future.set_exception(err)
        else:
            future.set_result(None)
    
    class _sock_connect_one(object):
        __slots__=('fd',)
        def __init__(self,fd):
            self.fd=fd
        def __call__(self,future):
            future._loop.remove_writer(self.fd)
    
    def _sock_connect_cb(self,future,sock,address):
        if future.done():
            return

        try:
            err_number=sock.getsockopt(module_socket.SOL_SOCKET,module_socket.SO_ERROR)
            if err_number!=0:
                raise OSError(err_number,f'Connect call failed {address}')
        except (BlockingIOError, InterruptedError):
            # socket is still registered, the callback will be retried later
            pass
        except BaseException as err:
            future.set_exception(err)
        else:
            future.set_result(None)

    #await it
    def sock_recv(self,sock,n):
        future=Future(self)
        self._sock_recv(future,False,sock,n)
        return future

    def _sock_recv(self,future,registered,sock,n):
        fd=sock.fileno()
        if registered:
            self.remove_reader(fd)
        if future.cancelled():
            return
        try:
            data=sock.recv(n)
        except (BlockingIOError,InterruptedError):
            self.add_reader(fd,self._sock_recv,future,True,sock,n)
        except BaseException as err:
            future.set_exception(err)
        else:
            future.set_result(data)

    #await it 
    def sock_sendall(self,sock,data):
        future=Future(self)
        if data:
            self._sock_sendall(future,False,sock,data)
        else:
            future.set_result(None)
        return future

    def _sock_sendall(self,future,registered,sock,data):
        fd=sock.fileno()
        
        if registered:
            self.remove_writer(fd)
        if future.cancelled():
            return
        
        try:
            n=sock.send(data)
        except (BlockingIOError,InterruptedError):
            n=0
        except BaseException as err:
            future.set_exception(err)
            return
        
        if n==len(data):
            future.set_result(None)
        else:
            if n:
                data=data[n:]
            self.add_writer(fd,self._sock_sendall,future,True,sock,data)

    #should be async
    def connect_read_pipe(self,protocol_factory,pipe):
        raise NotImplementedError

    #should be async
    def connect_write_pipe(self,protocol_factory,pipe):
        raise NotImplementedError
    
    #should be async
    def create_datagram_endpoint(self,protocol_factory,local_addr=None,remote_addr=None,*,family=0,proto=0,flags=0,reuse_address=None,reuse_port=None,allow_broadcast=None,sock=None):
        raise NotImplementedError

    def _create_server_getaddrinfo(self, host, port, family, flags):
        return self._ensure_resolved((host,port),family=family,type=module_socket.SOCK_STREAM,flags=flags)
    
    async def create_server(self,protocol_factory,host=None,port=None,*,family=module_socket.AF_UNSPEC,flags=module_socket.AI_PASSIVE,sock=None,backlog=100,ssl=None,reuse_address=None,reuse_port=None):
        if type(ssl) is bool:
            raise TypeError('ssl argument must be an SSLContext or None')

        if (host is not None) or (port is not None):
            if (sock is not None):
                raise ValueError('host/port and sock can not be specified at the same time')
            
            if (reuse_address is None):
                reuse_address = (os.name=='posix' and sys.platform!='cygwin')
            else:
                if (type(reuse_address) is not bool):
                    raise TypeError(f'`reuse_address` can be `None` or type bool ,got `{reuse_address!r}`')
            
            if reuse_port and (not hasattr(module_socket,'SO_REUSEPORT')):
                raise ValueError('reuse_port not supported by socket module')
            
            hosts=[]
            if (host is None) or (host==''):
                 hosts.append(None)
            elif isinstance(host,str):
                hosts.append(hosts)
            elif hasattr(type(host),'__iter__'):
                for host in host:
                    if (host is None) or (host==''):
                        hosts.append(None)
                        continue
                    
                    if isinstance(host,str):
                        hosts.append(host)
                        continue
                    
                    raise TypeError(f'`host` is passed as iterable, but it yielded at least 1 not `None`, or `str` instance; `{host!r}`')
            else:
                raise TypeError(f'`host` should be `None`, `str` instance or iterable of `None` or of `str` instances, got {host!r}')
            
            sockets = []
            
            futures = {self._create_server_getaddrinfo(host,port,family=family,flags=flags) for host in hosts}
            
            try:
                while True:
                    done, pending = await WaitTillFirst(futures,self)
                    for future in done:
                        futures.remove(future)
                        infos = future.result()
                        
                        for info in infos:
                            af, socktype, proto, canonname, sa = info
                            
                            try:
                                sock = module_socket.socket(af,socktype,proto)
                            except module_socket.error:
                                continue
                            
                            sockets.append(sock)
                            
                            if reuse_address:
                                sock.setsockopt(module_socket.SOL_SOCKET, module_socket.SO_REUSEADDR, True)
                            
                            if reuse_port:
                                try:
                                    sock.setsockopt(module_socket.SOL_SOCKET, module_socket.SO_REUSEPORT, 1)
                                except OSError as err:
                                    raise ValueError('reuse_port not supported by socket module, SO_REUSEPORT defined but not implemented.') from err

                            if (_HAS_IPv6 and af==module_socket.AF_INET6 and hasattr(module_socket,'IPPROTO_IPV6')):
                                sock.setsockopt(module_socket.IPPROTO_IPV6, module_socket.IPV6_V6ONLY, True)
                            try:
                                sock.bind(sa)
                            except OSError as err:
                                raise OSError(err.errno, f'error while attempting to bind on address {sa!r}: {err.strerror.lower()!s}') from None
                    
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
    def create_unix_connection(self,protocol_factory,path,*,ssl=None,sock=None,server_hostname=None):
        raise NotImplementedError

    #should be async
    def create_unix_server(self,protocol_factory,path=None,*,sock=None,backlog=100,ssl=None):
        raise NotImplementedError
    
    #should be async
    def subprocess_exec(self,protocol_factory,program,*args,
                        stdin=subprocess.PIPE,stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,universal_newlines=False,
                        shell=False,bufsize=0,**kwargs):
        
        raise NotImplementedError

    #should be async
    def subprocess_shell(self,protocol_factory,cmd,*,stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                         universal_newlines=False,shell=True,bufsize=0,**kwargs):
        
        raise NotImplementedError

del module_time
del subprocess

from . import futures
futures.EventThread=EventThread
del futures
