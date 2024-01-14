import vampytest
from scarletio import Future, Task, skip_poll_cycle, skip_ready_cycle

from ...core import KOKORO

from ..base import DiscordGatewayBase
from ..heartbeat import Kokoro


class TestGateway(DiscordGatewayBase):
    __slots__ = ('actions', 'freeze_on_beat')
    
    def __new__(cls, *, freeze_on_beat = False):
        self = object.__new__(cls)
        self.actions = []
        self.freeze_on_beat = freeze_on_beat
        return self
    
    
    async def beat(self):
        self.actions.append('beat')
        
        if self.freeze_on_beat:
            await Future(KOKORO)
    
    
    async def terminate(self):
        self.actions.append('terminate')


def _assert_fields_set(kokoro):
    """
    Asserts whether every fields are set of the given instance.
    
    Parameters
    ----------
    kokoro : ``Kokoro``
        The instance to check.
    """
    vampytest.assert_instance(kokoro, Kokoro)
    vampytest.assert_instance(kokoro.beat_task, Task, nullable = True)
    vampytest.assert_instance(kokoro.gateway, DiscordGatewayBase)
    vampytest.assert_instance(kokoro.interval, float)
    vampytest.assert_instance(kokoro.last_answer, float)
    vampytest.assert_instance(kokoro.last_send, float)
    vampytest.assert_instance(kokoro.latency, float)
    vampytest.assert_instance(kokoro.runner, Task, nullable = True)
    vampytest.assert_instance(kokoro.should_run, bool)


def test__Kokoro__new():
    """
    Tests whether ``Kokoro.__new__`` works as intended.
    """
    gateway = TestGateway()
    
    kokoro = Kokoro(gateway)
    _assert_fields_set(kokoro)
    
    vampytest.assert_is(kokoro.gateway, gateway)


def test__Kokoro__repr():
    """
    Tests whether ``Kokoro.__repr__`` works as intended.
    """
    gateway = TestGateway()
    
    kokoro = Kokoro(gateway)
    
    output = repr(kokoro)
    vampytest.assert_instance(output, str)


async def test__Kokoro__start__fresh_run():
    """
    Tests whether ``Kokoro.run`` works as intended.
    
    Case: fresh run.
    
    This function is a coroutine.
    """
    gateway = TestGateway()
    kokoro = Kokoro(gateway)
    
    try:
        output = kokoro.start()
        
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, True)
        
        vampytest.assert_instance(kokoro.runner, Task)
        
        await skip_ready_cycle()
        
        vampytest.assert_instance(kokoro.should_run, bool)
        vampytest.assert_eq(kokoro.should_run, True)
    
    finally:
        kokoro.stop()
    
    await skip_ready_cycle()


async def test__Kokoro__start__repeated_run():
    """
    Tests whether ``Kokoro.run`` works as intended.
    
    Case: repeated run call.
    
    This function is a coroutine.
    """
    gateway = TestGateway()
    kokoro = Kokoro(gateway)
    
    try:
        kokoro.start()
        runner_before = kokoro.runner
        
        output = kokoro.start()
        runner_after = kokoro.runner
        
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, False)
        
        vampytest.assert_is(runner_before, runner_after)
    finally:
        kokoro.stop()
    
    await skip_ready_cycle()


async def test__Kokoro__cancel__not_running():
    """
    Tests whether ``Kokoro.cancel`` works as intended.
    
    Case: Not running.
    
    This function is a coroutine.
    """
    gateway = TestGateway()
    kokoro = Kokoro(gateway)
    
    kokoro.stop()
    
    vampytest.assert_is(kokoro.runner, None)
    vampytest.assert_instance(kokoro.should_run, bool)
    vampytest.assert_eq(kokoro.should_run, False)


async def test__Kokoro__cancel__running():
    """
    Tests whether ``Kokoro.cancel`` works as intended.
    
    Case: running.
    
    This function is a coroutine.
    """
    gateway = TestGateway()
    kokoro = Kokoro(gateway)
    
    try:
        kokoro.start()
        kokoro.stop()
        
        vampytest.assert_is(kokoro.runner, None)
        vampytest.assert_instance(kokoro.should_run, bool)
        vampytest.assert_eq(kokoro.should_run, False)
    finally:
        # make sure
        kokoro.stop()
    
    await skip_ready_cycle()


async def test__Kokoro__restart__not_running():
    """
    Tests whether ``Kokoro.restart`` works as intended.
    
    Case: running.
    
    This function is a coroutine.
    """
    gateway = TestGateway()
    kokoro = Kokoro(gateway)
    
    try:
        kokoro.restart()
        
        vampytest.assert_instance(kokoro.runner, Task)
        
        await skip_ready_cycle()
        
        vampytest.assert_instance(kokoro.should_run, bool)
        vampytest.assert_eq(kokoro.should_run, True)
    finally:
        kokoro.stop()
    
    await skip_ready_cycle()


async def test__Kokoro__restart__running():
    """
    Tests whether ``Kokoro.restart`` works as intended.
    
    Case: running.
    
    This function is a coroutine.
    """
    gateway = TestGateway()
    kokoro = Kokoro(gateway)
    
    try:
        kokoro.start()
        runner_before = kokoro.runner
        vampytest.assert_instance(kokoro.runner, Task)
        
        kokoro.restart()
        runner_after = kokoro.runner
        vampytest.assert_instance(kokoro.runner, Task)
        
        vampytest.assert_is_not(runner_before, runner_after)
        
        await skip_ready_cycle()
        
        vampytest.assert_instance(kokoro.should_run, bool)
        vampytest.assert_eq(kokoro.should_run, True)
    finally:
        kokoro.stop()
    
    await skip_ready_cycle()


async def test__Kokoro__run__termination_on_beat_waiter():
    """
    Tests whether ``Kokoro.run`` works as intended.
    
    Case: Terminate gateway while waiting for beat waiter.
    """
    gateway = TestGateway()
    kokoro = Kokoro(gateway)
    kokoro.interval = -1000.0
    
    try:
        kokoro.start()
        
        await skip_poll_cycle()
        
        vampytest.assert_is(kokoro.runner, None)
        vampytest.assert_instance(kokoro.should_run, bool)
        vampytest.assert_eq(kokoro.should_run, False)
        vampytest.assert_eq(gateway.actions, ['terminate'])
        
    finally:
        kokoro.stop()
    
    await skip_ready_cycle()


async def test__Kokoro__run__termination_on_beat_task():
    """
    Tests whether ``Kokoro.run`` works as intended.
    
    Case: Terminate gateway while waiting for beat task.
    """
    gateway = TestGateway()
    kokoro = Kokoro(gateway)
    
    try:
        kokoro.start()
        
        await skip_ready_cycle()
        vampytest.assert_instance(kokoro.beat_waiter, Future)
        kokoro.beat_waiter.set_result_if_pending(None)
        await skip_ready_cycle()
        vampytest.assert_instance(kokoro.beat_task, Task)
        kokoro.beat_task.apply_timeout(0.0)
        await skip_poll_cycle()
        
        vampytest.assert_is(kokoro.runner, None)
        vampytest.assert_instance(kokoro.should_run, bool)
        vampytest.assert_eq(kokoro.should_run, False)
        vampytest.assert_eq(gateway.actions, ['terminate'])
        
    finally:
        kokoro.stop()
    
    await skip_ready_cycle()


async def test__Kokoro__run__full_cycle():
    """
    Tests whether ``Kokoro.run`` works as intended.
    
    Case: Full cycle done
    """
    gateway = TestGateway()
    kokoro = Kokoro(gateway)
    
    try:
        kokoro.start()
        
        await skip_ready_cycle()
        vampytest.assert_instance(kokoro.beat_waiter, Future)
        kokoro.beat_waiter.set_result_if_pending(None)
        await skip_ready_cycle()
        
        vampytest.assert_instance(kokoro.beat_task, Task)
        await skip_poll_cycle()
        
        vampytest.assert_eq(gateway.actions, ['beat'])
        
    finally:
        kokoro.stop()
    
    await skip_ready_cycle()


def test__Kokoro__answered():
    """
    Tests whether ``Kokoro.answered`` works as intended.
    """
    gateway = TestGateway()
    
    now = 1.0
    
    def perf_counter_mock():
        nonlocal perf_counter_mock
        return now
    
    mocked_new = vampytest.mock_globals(Kokoro.__new__, perf_counter = perf_counter_mock)
    
    kokoro = mocked_new(Kokoro, gateway)
    
    mocked_answered = vampytest.mock_globals(Kokoro.answered, perf_counter = perf_counter_mock)
    
    now = 3.0
    
    mocked_answered(kokoro)
    
    vampytest.assert_eq(kokoro.last_answer, 3.0)
    vampytest.assert_eq(kokoro.last_send, 1.0)
    vampytest.assert_eq(kokoro.latency, 2.0)


async def test__Kokoro__beat_now__not_running():
    """
    Tests whether ``Kokoro.beat_now`` works as intended.
    
    Case: not running.
    
    This function is a coroutine.
    """
    gateway = TestGateway()
    kokoro = Kokoro(gateway)
    
    try:
        await kokoro.beat_now()
        
        await skip_poll_cycle()
        
        vampytest.assert_instance(kokoro.runner, Task)
        vampytest.assert_instance(kokoro.should_run, bool)
        vampytest.assert_eq(kokoro.should_run, True)
        vampytest.assert_eq(gateway.actions, ['beat'])
    finally:
        kokoro.stop()


async def test__Kokoro__beat_now__waiting_for_beat():
    """
    Tests whether `Kokoro.beat_now`` works as intended.
    
    Case: running, waiting for beat.
    
    This function is a coroutine.
    """
    gateway = TestGateway()
    kokoro = Kokoro(gateway)
    
    try:
        kokoro.start()
        await skip_ready_cycle()
        
        await kokoro.beat_now()
        await skip_poll_cycle()
        
        vampytest.assert_eq(gateway.actions, ['beat'])
    finally:
        kokoro.stop()
    

async def test__Kokoro__beat_now__beating():
    """
    Tests whether `Kokoro.beat_now`` works as intended.
    
    Case: running, beating.
    
    This function is a coroutine.
    """
    gateway = TestGateway(freeze_on_beat = True)
    kokoro = Kokoro(gateway)
    
    try:
        kokoro.start()
        await skip_ready_cycle()
        vampytest.assert_instance(kokoro.beat_waiter, Future)
        kokoro.beat_waiter.set_result_if_pending(None)
        await skip_ready_cycle()
        
        # If something goes wrong since we are freezing on `.beat`, we apply timeout.
        task = Task(KOKORO, kokoro.beat_now())
        task.apply_timeout(0.01)
        await task
        
        await skip_poll_cycle()
        
        vampytest.assert_eq(gateway.actions, ['beat'])
    finally:
        kokoro.stop()
