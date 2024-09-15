__all__ = ()

from time import perf_counter

from scarletio import CancelledError, RichAttributeErrorBaseType, Task, sleep

from ..core import KOKORO

from .constants import HEARTBEAT_TIMEOUT, INTERVAL_DEFAULT, LATENCY_DEFAULT


class Kokoro(RichAttributeErrorBaseType):
    """
    A beater for Discord gateways.
    
    Attributes
    ----------
    beat_task : `None`, ``Task``
        The beat task of kokoro's gateway. Set by ``._task`` meanwhile it's gateway is connected.
    beat_waiter : `None`, ``Future``
        `.runner` task's waiter. Sleeps `.runner` between two beat.
    gateway : ``DiscordGatewayBase``
        Kokoro's owner gateway.
    interval : `float`
        The time needed to be waited between two beats.
    last_answer : `float`
        The time of the last answered heartbeat event in `perf_counter` time.
    last_send : `float`
        The last time when kokoro sent a heartbeat event in `last_send` time.
    latency : `float`
        The time interval between the last beat and the response's time.
    runner : `None | Task`
        The main keep alive task of kokoro.
    should_run : `bool`
        Whether the kokoro should run and restart itself.
    """
    __slots__ = (
        'beat_task', 'beat_waiter', 'gateway', 'interval', 'last_answer', 'last_send', 'latency', 'runner',
        'should_run'
    )
    
    def __new__(cls, gateway):
        """
        Creates a ``Kokoro`` bound to it's gateway.
        
        Parameters
        ----------
        gateway : ``DiscordGateway``, ``DiscordGatewayVoice``
            The gateway of kokoro.
        
        Returns
        -------
        kokoro : ``Kokoro``
        """
        now_ = perf_counter()
        
        self = object.__new__(cls)
        
        self.beat_task = None
        self.beat_waiter = None
        self.gateway = gateway
        self.interval = INTERVAL_DEFAULT # we set it from outside
        self.last_answer = now_
        self.last_send = now_
        self.latency = LATENCY_DEFAULT
        self.runner = None
        self.should_run = False
        
        return self
    
    
    def __repr__(self):
        """Returns kokoro's representation."""
        repr_parts = ['<', type(self).__name__,]
        
        repr_parts.append(' gateway = ')
        repr_parts.append(repr(self.gateway))
        
        if self.runner is None:
            state = 'dormant'
        else:
            state = 'beating'
        
        repr_parts.append(', state = ')
        repr_parts.append(state)
        repr_parts.append('>')
        
        return ''.join(repr_parts)


    def start(self):
        """
        Starts kokoro.
        
        Returns
        -------
        started : `bool`
            Whether the gateway was started.
        """
        # Are we running or starting?
        if (self.runner is not None):
            return False
        
        self.runner = Task(KOKORO, self._run())
        return True
    
    
    def stop(self):
        """
        Stops kokoro. Called when it's gateway is closing or is scheduled for resuming.
        """
        # Set should_run
        self.should_run = False
        
        # Stop running.
        runner = self.runner
        if (runner is not None):
            self.runner = None
            runner.cancel()
    
    
    def restart(self):
        """
        Starts kokoro's beating. Handles all the cases around the board to do so.
        """
        # First the cancel task will go through, then the start, so nothing to worry about.
        self.stop()
        self.start()
    
    
    async def _run(self):
        """
        The main keep alive task of kokoro.
        
        The control flow of the method is the following:
        
        - If `.should_run` is not `True`, break out.
        - Wait `.interval` time and set the waiting ``Future`` to `self.beat_waiter`.
            If its cancelled we already beat, continue loop.
        - If we did not get answer since last beating (what is triggered first from outside), then we stop the
            gateway. We also break out from the loop to terminate the beating state and we will wait for the
            web socket to connect again.
        - We beat one with starting `gateway.beat` as a ``Task`` and setting it to `.beat_task`. If the task is
            not completed before it's respective timeout, we stop the gateway here as well. We also break out
            from the loop to terminate the beating state and we will wait for the web socket to connect again.
            This task can also be cancelled. If cancellation occurs, we repeat the loop.
        - If the beating task is done, we update `.last_send` to the current `perf_counter` time. Repeat the loop.
        
        This method is a coroutine.
        """
        try:
            self.last_answer = perf_counter()
            gateway = self.gateway
            self.should_run = True
            
            while self.should_run:
                beat_waiter = sleep(self.interval, KOKORO)
                self.beat_waiter = beat_waiter
                try:
                    await beat_waiter.wait_for_completion()
                finally:
                    self.beat_waiter = None
                
                # Were we cancelled? If yes continue with next iteration and check whether we are should_run.
                cancellation_exception = beat_waiter.get_cancellation_exception()
                if (cancellation_exception is not None) and isinstance(cancellation_exception, CancelledError):
                    self.last_send = perf_counter()
                    continue
                
                if (self.last_answer + self.interval + HEARTBEAT_TIMEOUT) - perf_counter() <= 0.0:
                    self.should_run = False
                    Task(KOKORO, gateway.terminate())
                    break
                
                beat_task = Task(KOKORO, gateway.beat())
                beat_task.apply_timeout(HEARTBEAT_TIMEOUT)
                self.beat_task = beat_task
                try:
                    await beat_task.wait_for_completion()
                finally:
                    self.beat_task = None
                
                # Check cancellation exception. If it was timeout error we should stop beating.
                cancellation_exception = beat_task.get_cancellation_exception()
                if (cancellation_exception is None):
                    self.last_send = perf_counter()
                    continue
                
                if isinstance(cancellation_exception, TimeoutError):
                    self.should_run = False
                    Task(KOKORO, gateway.terminate())
                    break
                
                # cancelled case -> resume and check `.should_run`
                continue
        
        finally:
            # Only cancel if we have not restarted yet
            if KOKORO.current_task is self.runner:
                self.should_run = False
                self.runner = None
    
    
    def answered(self):
        """
        When gateway received answer after beating, it's gateway calls this method.
        
        This method updates `.last_answer` and `.latency` as well. Because of the updated `.last_answer`,
        ``._keep_beating`` task will know that it's gateway is still connected.
        """
        now_ = perf_counter()
        self.last_answer = now_
        self.latency = now_ - self.last_send
    
    
    async def beat_now(self):
        """
        Sends a heartbeat event now. If kokoro is not at beating state, or anywhere in between, resets itself as it just
        received a heartbeat answer right now.
        
        This method is a coroutine.
        """
        while True: # GOTO
            # case 1 : we are not running:
            if self.start():
                should_beat_now = True # True = send beat data
                break
            
            # case 2 : we wait to beat
            beat_waiter = self.beat_waiter
            if (beat_waiter is not None):
                # better skip a beat
                beat_waiter.cancel()
                should_beat_now = True # True = send beat data
                break
            
#            # case 3 : we already beat
#            beat_task = self.beat_task
#            if (beat_task is not None):
#                should_beat_now = False
#                break
            
            should_beat_now = False
            break
        
        if should_beat_now:
            await self.gateway.beat()
        else:
            self.answered()
