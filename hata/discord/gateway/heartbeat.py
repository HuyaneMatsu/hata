__all__ = ()

from time import perf_counter

from ...backend.futures import sleep, Task, future_or_timeout, Future, CancelledError, skip_ready_cycle

from ..core import KOKORO

HEARTBEAT_TIMEOUT = 20.0


class Kokoro:
    """
    A beater for Discord gateways.
    
    Attributes
    ----------
    beat_task : `None` or ``Task``
        The beat task of kokoro's gateway. Set by ``._task`` meanwhile it's gateway is connected.
    beat_waiter : `None` or ``Future``
        `.beater` task's waiter. Sleeps `.beater` between two beat.
    beater : `None` or ``Task`` of ``._keep_beating``
        A task what sends a beating payload to Discord. Set only meanwhile kokoro is in the middle of a beat.
    gateway : ``DiscordGateway`` or ``DiscordGatewayVoice``
        Kokoro's owner gateway.
    interval : `float`
        The time needed to be waited between two beats.
    last_answer : `float`
        The time of the last answered heartbeat event in `perf_counter` time.
    last_send : `float`
        The last time when kokoro sent a heartbeat event in `last_send` time.
    latency : `float`
        The time interval between the last beat and the response's time. Defaults to `.DEFAULT_LATENCY` if no beat was
        done yet.
    running : `bool`
        Whether the kokoro should run and restart itself.
    should_beat : `bool`
        Whether the kokoro should keep beating.
    task : `None` or ``Task`` of ``._start``
        The main keep alive task of kokoro.
    ws_waiter : `None` or ``Future``
        The waiter of kokoro, what waits for it's gateway to connect it's websocket.
    
    Class Attributes
    ----------------
    DEFAULT_LATENCY : `float` = `9999.0`
        The default latency of kokoro. Better than using `inf`.
    """
    __slots__ = ('beat_task', 'beat_waiter', 'beater', 'gateway', 'interval', 'last_answer', 'last_send', 'latency',
        'running', 'should_beat', 'task', 'ws_waiter')
    
    DEFAULT_LATENCY = 9999.0
    
    async def __new__(cls, gateway):
        """
        Creates a ``Kokoro`` instance bound to it's gateway.
        
        This method is a coroutine.
        
        Parameters
        ----------
        gateway : ``DiscordGateway`` or ``DiscordGatewayVoice``
            The gateway of kokoro.
        
        Returns
        -------
        kokoro : ``Kokoro``
        
        Notes
        -----
        Before the coroutine returns a full loop is done to ensure `._start` is already started up.
        """
        self = object.__new__(cls)
        
        self.gateway = gateway
        self.interval = 40.0 # we set it from outside
        self.running = False
        now_ = perf_counter()
        self.last_answer = now_
        self.last_send = now_
        self.latency = self.DEFAULT_LATENCY
        self.ws_waiter = None
        self.beater = None
        self.beat_task = None
        self.beat_waiter = None
        self.task = Task(self._start(), KOKORO)
        
        #skip 1 loop
        await skip_ready_cycle()
        
        return self
    
    
    async def restart(self):
        """
        Restarts kokoro.
        
        This method is a coroutine.
        """
        self.cancel()
        # skip 1 loop
        await skip_ready_cycle()
        self.task = Task(self._start(), KOKORO)
        # skip 1 loop
        await skip_ready_cycle()
    
    
    async def _start(self):
        """
        The main keep alive task of kokoro.
        
        The control flow of the method is the following:
            - Set `.ws_waiter` and wait till it is done. If it is done, means that kokoro's gateway is connected.
                If it was cancelled meanwhile, means the beat task should stop.
            - Sets `.beater` to ``._keep_beating`` and awaits it. This is the main beater of kokoro and runs meanwhile
                it's gateway is connected. This task can be cancelled, but we ignore that case.
            - If `.running` is still `True`, repeat.
        
        This method is a coroutine.
        """
        try:
            self.running = True
            while True:
                #wait for start
                try:
                    waiter = Future(KOKORO)
                    self.ws_waiter = waiter
                    await waiter
                except CancelledError:
                    #kokoro cancelled, client shuts down
                    break
                finally:
                    self.ws_waiter = None
                
                #keep beating
                try:
                    beater = Task(self._keep_beating(), KOKORO)
                    self.beater = beater
                    await beater
                except CancelledError:
                    #connection cancelled, lets wait for it
                    pass
                finally:
                    #make sure
                    self.beater = None
                
                if self.running:
                    continue
                
                break
        finally:
            if self.task is KOKORO.current_task:
                self.task = None
    
    
    async def _keep_beating(self):
        """
        The beater task of kokoro.
        
        The control flow of tze method is the following:
            - If `.should_beat` is not `True`, break out.
            - Wait `.interval` time and set the waiting ``Future`` to `self.beat_waiter`. If kokoro is cancelled, or
                if it should beat now, it is cancelled and we repeat the loop.
            - If we did not get answer since last beating (what is triggered first from outside), then we stop the
                gateway. We also break out from the loop to terminate the beating state and we will wait for the
                websocket to connect again.
            - We beat one with starting `gateway._beat` as a ``Task`` and setting it to `.beat_task`. If the task is
                not completed before it's respective timeout, we stop the gateway here as well. We also break out
                from the loop to terminate the beating state and we will wait for the websocket to connect again.
                This task can also be cancelled. If cancellation occurs, we repeat the loop.
            - If the beating task is done, we update `.last_send` to the current `perf_counter` time. Repeat the loop.
        
        This method is a coroutine.
        """
        self.last_answer = perf_counter()
        gateway = self.gateway
        self.should_beat = True
        while self.should_beat:
            waiter = sleep(self.interval, KOKORO)
            self.beat_waiter = waiter
            try:
                await waiter
            except CancelledError:
                self.last_send = perf_counter()
                continue
            finally:
                self.beat_waiter = None
            
            if (self.last_answer+self.interval+HEARTBEAT_TIMEOUT)-perf_counter() <= 0.0:
                self.should_beat = False
                Task(gateway.terminate(), KOKORO)
                break
            
            try:
                task = Task(gateway._beat(), KOKORO)
                future_or_timeout(task, HEARTBEAT_TIMEOUT)
                self.beat_task = task
                await task
            except TimeoutError:
                self.should_beat = False
                Task(gateway.terminate(), KOKORO)
                break
            except CancelledError:
                continue
            finally:
                self.beat_task = None
            
            self.last_send = perf_counter()
    
    
    def start_beating(self):
        """
        Starts kokoro's beating. Handles all the cases around the board to do so.
        """
        # case 1 : we are not running
        if not self.running:
            Task(self._start_beating(), KOKORO)
            return
        
        #case 2 : we wait for ws
        waiter = self.ws_waiter
        if (waiter is not None):
            self.ws_waiter = None
            waiter.set_result(None)
            return
        
        #case 3 : we wait for beat response
        waiter = self.beat_waiter
        if (waiter is not None):
            self.beat_waiter = None
            waiter.cancel()
            return
        
        #case 4 : we are beating
        task = self.beat_task
        if (task is not None):
            self.beat_waiter = None
            task.cancel()
            return
    
    
    async def _start_beating(self):
        """
        Internal method to start beating when kokoro is not running.
        
        This method is a coroutine.
        """
        # starts kokoro, then beating
        self.task = Task(self._start(), KOKORO)
        # skip 1 loop
        await skip_ready_cycle()
        
        waiter = self.ws_waiter
        if (waiter is not None):
            self.ws_waiter = None
            waiter.set_result(None)
    
    
    def answered(self):
        """
        When gateway received answer after beating, it's gateway calls this method.
        
        This method updates `.last_answer` and `.latency` as well. Because of the updated `.last_answer`,
        ``._keep_beating`` task will know that it's gateway is still connected.
        """
        now_ = perf_counter()
        self.last_answer = now_
        self.latency = now_-self.last_send
    
    
    def terminate(self):
        """
        Terminates kokoro till restart. Called when it's gateway will resume it's connection.
        """
        #case 1 : we are not running
        if not self.running:
            return
        
        #case 2 : we are waiting for ws
        waiter = self.ws_waiter
        if (waiter is not None):
            # it is fine, it is what we should do
            return
        
        #case 2 : we are beating
        beater = self.beater
        if (beater is not None):
            self.should_beat = False
            
            #case 3.1 : we wait to beat
            waiter = self.beat_waiter
            if (waiter is not None):
                self.beat_waiter = None
                waiter.cancel()
                return
            
            #case 3.2: we are beating
            task = self.beat_task
            if (task is not None):
                self.beat_task = None
                task.cancel()
                return
    
    
    def cancel(self):
        """
        Stops kokoro. Called when it's gateway is closing.
        """
        #case 1 : we are not running
        if not self.running:
            return
        self.running = False
        
        #case 2 : we are waiting for ws
        waiter = self.ws_waiter
        if (waiter is not None):
            self.ws_waiter = None
            waiter.cancel()
            return
        
        #case 3 : we are beating
        beater = self.beater
        if beater is not None:
            self.should_beat = False
            
            #case 3.1 : we wait to beat
            waiter = self.beat_waiter
            if (waiter is not None):
                self.beat_waiter = None
                waiter.cancel()
                return
            
            #case 3.2: we are beating
            task = self.beat_task
            if (task is not None):
                self.beat_task = None
                task.cancel()
                return
    
    
    async def beat_now(self):
        """
        Sends a heartbeat event now. If kokoro is not at beating state, or anywhere in between, resets itself as it just
        received a heartbeat answer right now.
        
        This method is a coroutine.
        """
        while True: #GOTO
            #case 1 : we are not running:
            if not self.running:
                Task(self._start_beating(), KOKORO)
                should_beat_now = True # True = send beat data
                break
            
            # case 2 : we wait for ws
            waiter = self.ws_waiter
            if (waiter is not None):
                self.ws_waiter = None
                waiter.set_result(None)
                should_beat_now = True # True = send beat data
                break
            
            # case 3 : we wait to beat
            waiter = self.beat_waiter
            if (waiter is not None):
                # better skip a beat
                self.beat_waiter = None
                waiter.cancel()
                should_beat_now = True # True = send beat data
                break
            
            # case 4 : we already beat
#            task = self.beat_task
#            if (task is not None):
#                should_beat_now = False
#                break
            
            should_beat_now = False
            break
        
        if should_beat_now:
            await self.gateway._beat()
        else:
            self.answered()
    
    # Fixed?
    """
    if __debug__:
        def __del__(self):
            # bug?
            waiter = self.ws_waiter
            if (waiter is not None):
                waiter.__silence__()
            
            # despair?
            waiter = self.beat_waiter
            if (waiter is not None):
                waiter.__silence__()
    """
    
    def __repr__(self):
        """Returns kokoro's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
            ' client=',
            repr(self.gateway.client.full_name),
            ' state=',
        ]
        
        if self.task is None:
            state = 'stopped'
        elif self.beater is None:
            state = 'waiting for websocket'
        else:
            state = 'beating'
        
        repr_parts.append(state)
        repr_parts.append('>')
        
        return ''.join(repr_parts)
