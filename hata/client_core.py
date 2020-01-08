# -*- coding: utf-8 -*-
__all__ = ('CACHE_PRESENCE', 'CACHE_USER', 'CHANNELS', 'CLIENTS', 'EMOJIS',
    'GUILDS', 'INTEGRATIONS', 'KOKORO', 'MESSAGES', 'ROLES', 'TEAMS', 'USERS',
    'start_clients', 'stop_clients', )

import sys
from time import perf_counter
from weakref import WeakValueDictionary

from .futures import Future, sleep, CancelledError, future_or_timeout, Task
from .eventloop import EventThread

from .doct import DOC_default_id_cont

CACHE_USER      = not (('no_user_cache'     in sys.argv) or ('no-user-cache'        in sys.argv))
CACHE_PRESENCE  = not (('no_presence_cache' in sys.argv) or ('no-presence-cache'    in sys.argv))
#You cannot store presences of not loaded users.
if (not CACHE_USER):
    CACHE_PRESENCE=False

CHANNELS    = WeakValueDictionary()
CLIENTS     = DOC_default_id_cont()
EMOJIS      = WeakValueDictionary()
GUILDS      = WeakValueDictionary()
INTEGRATIONS= WeakValueDictionary()
MESSAGES    = WeakValueDictionary()
ROLES       = WeakValueDictionary()
TEAMS       = WeakValueDictionary()
USERS       = WeakValueDictionary()

del WeakValueDictionary
del DOC_default_id_cont

Client=NotImplemented

def start_clients():
    for client in CLIENTS:
        if client.running:
            continue
            
        Task(client.connect(),KOKORO)
        KOKORO.wakeup()
        return

def stop_clients():
    for client in CLIENTS:
        if client.running:
            Task(client.disconnect(),KOKORO)
            KOKORO.wakeup()
    
KOKORO=EventThread(daemon=False,name='KOKORO')

GC_cycler=KOKORO.cycle(1200.)

HEARTBEAT_TIMEOUT=20.0

class Kokoro(object):
    __slots__ = ('beat_task', 'beat_waiter', 'beater', 'gateway', 'interval',
        'last_answer', 'last_send', 'latency', 'loop', 'running',
        'should_beat', 'task', 'ws_waiter')
    
    DEFAULT_LATENCY=9999.0
    
    async def __new__(cls,gateway,loop):
        self=object.__new__(cls)
        
        self.gateway    = gateway
        self.interval   = 40.0 #we set it from outside
        self.running    = False
        now_            = perf_counter()
        self.last_answer= now_
        self.last_send  = now_
        self.latency    = self.DEFAULT_LATENCY
        self.ws_waiter  = None
        self.loop       = loop
        self.beater     = None
        self.beat_task  = None
        self.beat_waiter= None
        self.task       = Task(self._start(),loop)
        
        #skip 1 loop
        future=Future(loop)
        future.set_result(None)
        await future
        
        return self
        
    async def restart(self):
        self.cancel()
        future=Future(self.loop)
        future.set_result(None)
        await future #skip 1 loop
        self.task=Task(self._start(),self.loop)
        await future #skip 1 loop

    async def _start(self):
        self.running=True
        while self.running:
            #wait for start
            try:
                waiter=Future(self.loop)
                self.ws_waiter=waiter
                await waiter
            except CancelledError:
                #kokoro cancelled, client shuts down
                return
            finally:
                self.ws_waiter=None
            
            #keep beating
            try:
                beater=Task(self._keep_beating(),self.loop)
                self.beater=beater
                await beater
            except CancelledError:
                #connection cancelled, lets wait for it
                pass
            finally:
                #make sure
                self.beater=None
        
    async def _keep_beating(self):
        self.last_answer=perf_counter()
        gateway=self.gateway
        self.should_beat=True
        while self.should_beat:
            waiter=sleep(self.interval,self.loop)
            self.beat_waiter=waiter
            try:
                await waiter
            except CancelledError:
                self.last_send=perf_counter()
                continue
            
            self.beat_waiter=None

            if (self.last_answer+self.interval+HEARTBEAT_TIMEOUT)-perf_counter()<=0.:
                client=gateway.client
                if type(client) is Client:
                    client._freeze_voice_for(gateway)
                Task(gateway.close(4000),self.loop)
                break
            
            try:
                task=Task(gateway._beat(),self.loop)
                future_or_timeout(task,HEARTBEAT_TIMEOUT)
                self.beat_task=task
                await task
            except TimeoutError:
                client=gateway.client
                if type(client) is Client:
                    client._freeze_voice_for(gateway)
                Task(gateway.close(4000),self.loop)
                break
            except CancelledError:
                continue
            finally:
                self.beat_task=None
            
            self.last_send=perf_counter()
            
    def start_beating(self):
        # case 1 : we are not running
        if not self.running:
            Task(self._start_beating(),self.loop)
            return
        
        #case 2 : we wait for ws
        waiter=self.ws_waiter
        if waiter is not None:
            waiter.set_result(None)
            return
        
        #case 3 : we wait for beat response
        waiter=self.beat_waiter
        if waiter is not None:
            waiter.cancel()
            return
        
        #case 4 : we are beating
        task=self.beat_task
        if task is not None:
            task.cancel()
            return
        
    
    async def _start_beating(self):
        #starts kokoro, then beating
        self.task=Task(self._start(),self.loop)
        #skip 1 loop
        future=Future(self.loop)
        future.set_result(None)
        await future
        
        waiter=self.ws_waiter
        if waiter is not None:
            waiter.set_result(None)
    
    def answered(self):
        now_=perf_counter()
        self.last_answer=now_
        self.latency=now_-self.last_send
        
    def terminate(self):
        #case 1 : we are not running
        if not self.running:
            return

        #case 2 : we are waiting for ws
        waiter=self.ws_waiter
        if waiter is not None:
            #it is fine, that is what we should do
            return
        
        #case 2 : we are beating
        beater=self.beater
        if beater is not None:
            self.should_beat=False
            
            #case 3.1 : we wait to beat
            waiter=self.beat_waiter
            if waiter is not None:
                waiter.cancel()
                return
            
            #case 3.2: we are beating
            task=self.beat_task
            if task is not None:
                task.cancel()
                return
            
    def cancel(self):
        #case 1 : we are not running
        if not self.running:
            return
        self.running=False
        
        #case 2 : we are waiting for ws
        waiter=self.ws_waiter
        if waiter is not None:
            waiter.cancel()
            return
        
        #case 3 : we are beating
        beater=self.beater
        if beater is not None:
            self.should_beat=False
            
            #case 3.1 : we wait to beat
            waiter=self.beat_waiter
            if waiter is not None:
                waiter.cancel()
                return
            
            #case 3.2: we are beating
            task=self.beat_task
            if task is not None:
                task.cancel()
                return
            
    async def beat_now(self):
        while True: #GOTO
            #case 1 : we are not running:
            if not self.running:
                Task(self._start_beating(),self.loop)
                should_beat_now=True # True = send beat data
                break
            
            # case 2 : we wait for ws
            waiter=self.ws_waiter
            if waiter is not None:
                waiter.set_result(None)
                should_beat_now=True # True = send beat data
                break
            
            # case 3 : we wait to beat
            waiter=self.beat_waiter
            if waiter is not None:
                # better skip a beat
                waiter.cancel()
                should_beat_now=True # True = send beat data
                break
            
            # case 4 : we aready beat
##            task=self.beat_task
##            if task is not None:
##                should_beat_now=False
##                break
            
            should_beat_now=False
            break
        
        if should_beat_now:
            await self.gateway._beat()
        else:
            self.answered()
            
    if __debug__:
        def __del__(self):
            # bug?
            waiter=self.ws_waiter
            if waiter is not None:
                waiter.__silence__()
            
            # despair?
            waiter=self.beat_waiter
            if waiter is not None:
                waiter.__silence__()
            
    def __repr__(self):
        return f'<{self.__class__.__name__} client={self.gateway.client!r} state=\'{("beating","waiting for websocket","stopped")[(self.task is None)+(self.beater is None)]}\'>'
