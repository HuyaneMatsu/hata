# -*- coding: utf-8 -*-
__all__ = ('CACHE_PRESENCE', 'CACHE_USER', 'CHANNELS', 'CLIENTS', 'EMOJIS', 'GUILDS', 'INTEGRATIONS', 'KOKORO',
    'MESSAGES', 'ROLES', 'TEAMS', 'USERS', 'start_clients', 'stop_clients', )

import sys
from time import perf_counter
from weakref import WeakValueDictionary
from threading import current_thread

from ..backend.futures import Future, sleep, CancelledError, future_or_timeout, Task
from ..backend.eventloop import EventThread

Client=NotImplemented

CACHE_USER      = not (('no_user_cache'     in sys.argv) or ('no-user-cache'        in sys.argv))
CACHE_PRESENCE  = not (('no_presence_cache' in sys.argv) or ('no-presence-cache'    in sys.argv))
#You cannot store presences of not loaded users.
if (not CACHE_USER):
    CACHE_PRESENCE=False

if (sys.hash_info.width>=64):
    #if we have 64 bit system we can use array instead of list
    from array import array as Array
    def create_array():
        return Array('Q')
else:
    create_array=list
    
if sys.implementation.name=='cpython':
    #on cpython bisect is 4~ times faster.
    import bisect
    _relativeindex=bisect.bisect_left
    del bisect

else:
    def _relativeindex(array,value):
        bot=0
        top=len(array)
        while True:
            if bot<top:
                half=(bot+top)>>1
                if array[half]<value:
                    bot=half+1
                else:
                    top=half
                continue
            break
        return bot

class ClientDictionary(object):
    __slots__=('_elements', '_ids', '_next',)
    
    def __init__(self):
        self._elements  = []
        self._ids       = create_array()
        self._next      = 1
    
    def append(self,obj):
        id_=obj.id
        
        if id_<4194304:
            id_=self._next
            obj.id=id_
            self._next=id_+1
        
        array=self._ids
        index=_relativeindex(array,id_)
        
        if index==len(array): #put it at the last place
            array.append(id_)
            self._elements.append(obj)
            return
        
        if array[index]==id_:  #this object is already at the container, lets check it!
            if self._elements[index] is self._elements[index]:
                return
            #hah, got u!
            raise RuntimeError('Two different objects added with same id')
        
        #insert it at the right place
        array.insert(index,id_)
        self._elements.insert(index,obj)
    
    def remove(self,obj):
        id_=obj.id
        
        if id_==0:
            return #not in the container
        
        array=self._ids
        index=_relativeindex(array,id_)
        
        if index==len(array): #not in the container
            return
        
        if array[index]!=id_:  #this object is not at the container, lets remove it
            return
        
        del array[index]
        del self._elements[index]
    
    #familiar to normal remove
    def remove_by_id(self,id_):
        array=self._ids
        index=_relativeindex(array,id_)

        if index==len(array): #not in the container
            return

        if array[index]!=id_:  #this object is not at the container, lets remove it
            return

        del array[index]
        del self._elements[index]

    def update(self,obj,new_id):
        old_id=obj.id
        obj.id=new_id
        array=self._ids
        old_index=_relativeindex(array,old_id)

        if old_index==len(array) or array[old_index]!=old_id: #not in the container?
            self.append(obj)
            return
        
        new_index=_relativeindex(array,new_id)

        #above or under?
        if old_index<new_index:
            move= 1
            new_index=new_index-1
        elif old_index>new_index:
            move=-1
        else:
            if array[new_index]==new_id:
                #hah, got u!
                raise RuntimeError('Two different objects added with same id')
            return

        #move ids
        index=old_index
        while True:
            if index==new_index:
                break
            array[index]=array[index+move]
            index=index+move
        #put our at the right place
        array[index]=new_id

        elements=self._elements
        #move objest
        index=old_index
        while True:
            if index==new_index:
                break
            elements[index]=elements[index+move]
            index=index+move
        #put our at the right place
        elements[index]=obj

    def __getitem__(self,id_):
        array=self._ids
        index=_relativeindex(array,id_)
        if index==len(array) or array[index]!=id_:
            raise ValueError(f'{id_!r} is not in the {self.__class__.__name__}')
        return self._elements[index]
        
    def __contains__(self,obj):
        id_=obj.id
        array=self._ids
        index=_relativeindex(array,id_)
        if index==len(array):
            return False
        return (array[index]==id_)

    def __len__(self):
        return self._ids.__len__()

    def index(self,obj):
        id_=obj.id
        array=self._ids
        index=_relativeindex(array,id_)
        if index==len(array) or array[index]!=id_:
            raise ValueError(f'{obj!r} is not in the {self.__class__.__name__}')
        return index

    def __iter__(self):
        return self._elements.__iter__()

    def __reversed__(self):
        return self._elements.__reversed__()
    
    def count(self,obj):
        id_=obj.id
        array=self._ids
        index=_relativeindex(array,id_)
        if index==len(array):
            return 0
        if array[index]==id_:
            return 1
        return 0
    
    def copy(self):
        new=list.__new__(type(self))
        new._ids=self._ids.copy()
        new._elements=self._elements.copy()
        new._next=self._next
        return new
    
    def __repr__(self):
        result=[self.__class__.__name__,'([']
        elements=self._elements
        stop=len(elements)
        if stop:
            stop=stop-1
            index=0
            while index<stop:
                result.append(elements[index].__repr__())
                result.append(', ')
                index=index+1
            result.append(elements[index].__repr__())
        result.append('])')
        
        return ''.join(result)


CHANNELS    = WeakValueDictionary()
CLIENTS     = ClientDictionary()
EMOJIS      = WeakValueDictionary()
GUILDS      = WeakValueDictionary()
INTEGRATIONS= WeakValueDictionary()
MESSAGES    = WeakValueDictionary()
ROLES       = WeakValueDictionary()
TEAMS       = WeakValueDictionary()
USERS       = WeakValueDictionary()

def start_clients():
    for client in CLIENTS:
        if client.running:
            continue
        
        Task(client.connect(),KOKORO)
    
    if (current_thread() is not KOKORO):
        KOKORO.wakeup()

def stop_clients():
    for client in CLIENTS:
        if client.running:
            Task(client.disconnect(),KOKORO)
    
    if (current_thread() is not KOKORO):
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

del WeakValueDictionary
del ClientDictionary
del sys
