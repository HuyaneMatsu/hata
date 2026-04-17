import vampytest
from scarletio import TaskGroup, Task, skip_poll_cycle, skip_ready_cycle

from ...core import KOKORO

from ..client_sharder import _connect_gateways

from .helpers_gateway_shard import TestGatewayShard


async def test__connect_gateways__success__single_batch():
    """
    Tests whether ``_connect_gateways`` works as intended.
    
    Case: success, single batch.
    
    This function is a coroutine.
    """
    task_group = TaskGroup(KOKORO)
    task = None
    
    try:
        max_concurrency = 4
        gateways = (TestGatewayShard(), TestGatewayShard(), TestGatewayShard(), TestGatewayShard())
        
        sleep_counter = 0
        
        async def mock_sleep(duration, loop = None):
            nonlocal sleep_counter
            sleep_counter += 1
            return
        
        
        mocked = vampytest.mock_globals(
            _connect_gateways,
            sleep = mock_sleep,
        )
        
        task = Task(KOKORO, mocked(task_group, gateways, max_concurrency))
        
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        vampytest.assert_false(task.is_done())
        vampytest.assert_eq(len(task_group.pending), 8)
        for gateway in gateways:
            vampytest.assert_is_not(gateway.waiter, None)
        
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        for gateway in gateways:
            gateway.set_waiter(False, True)
        
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        vampytest.assert_true(task.is_done())
        vampytest.assert_eq(len(task_group.pending), 4)
        
        output = task.get_result()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, True)
    
    finally:
        task_group.cancel_all()
        
        if (task is not None):
            task.cancel()


async def test__connect_gateways__success__more_batch():
    """
    Tests whether ``_connect_gateways`` works as intended.
    
    Case: success, more batch.
    
    This function is a coroutine.
    """
    task_group = TaskGroup(KOKORO)
    task = None
    
    try:
        max_concurrency = 2
        gateways = (TestGatewayShard(), TestGatewayShard(), TestGatewayShard(), TestGatewayShard())
        
        sleep_counter = 0
        
        async def mock_sleep(duration, loop = None):
            nonlocal sleep_counter
            await skip_poll_cycle()
            sleep_counter += 1
            return
        
        
        mocked = vampytest.mock_globals(
            _connect_gateways,
            sleep = mock_sleep,
        )
        
        task = Task(KOKORO, mocked(task_group, gateways, max_concurrency))
        
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        vampytest.assert_false(task.is_done())
        vampytest.assert_eq(len(task_group.pending), 4)
        for gateway in gateways[0 : max_concurrency]:
            vampytest.assert_is_not(gateway.waiter, None)
        
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        for gateway in gateways[0 : max_concurrency]:
            gateway.set_waiter(False, True)
        
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        vampytest.assert_false(task.is_done())
        vampytest.assert_eq(len(task_group.pending), 2)
        
        vampytest.assert_eq(sleep_counter, 0)
        await skip_poll_cycle()
        await skip_ready_cycle()
        vampytest.assert_eq(sleep_counter, 1)
        
        vampytest.assert_false(task.is_done())
        vampytest.assert_eq(len(task_group.pending), 6)
        for gateway in gateways[max_concurrency : max_concurrency << 1]:
            vampytest.assert_is_not(gateway.waiter, None)
        
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        for gateway in gateways[max_concurrency : max_concurrency << 1]:
            gateway.set_waiter(False, True)
        
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        vampytest.assert_true(task.is_done())
        vampytest.assert_eq(len(task_group.pending), 4)
        vampytest.assert_eq(sleep_counter, 1)
        
        output = task.get_result()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, True)
    
    finally:
        task_group.cancel_all()
        
        if (task is not None):
            task.cancel()


async def test__connect_gateways__failure_return():
    """
    Tests whether ``_connect_gateways`` works as intended.
    
    Case: failing on a return.
    
    This function is a coroutine.
    """
    task_group = TaskGroup(KOKORO)
    task = None
    
    try:
        max_concurrency = 4
        gateways = (TestGatewayShard(), TestGatewayShard(), TestGatewayShard(), TestGatewayShard())
        
        sleep_counter = 0
        
        async def mock_sleep(duration, loop = None):
            nonlocal sleep_counter
            sleep_counter += 1
            return
        
        
        mocked = vampytest.mock_globals(
            _connect_gateways,
            sleep = mock_sleep,
        )
        
        task = Task(KOKORO, mocked(task_group, gateways, max_concurrency))
        
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        vampytest.assert_false(task.is_done())
        vampytest.assert_eq(len(task_group.pending), 8)
        for gateway in gateways:
            vampytest.assert_is_not(gateway.waiter, None)
        
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        gateways[2].set_waiter(False, False)
        
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        vampytest.assert_true(task.is_done())
        vampytest.assert_eq(len(task_group.pending), 7)
        
        output = task.get_result()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, False)
    
    finally:
        task_group.cancel_all()
        
        if (task is not None):
            task.cancel()
        

async def test__connect_gateways__failure_exception():
    """
    Tests whether ``_connect_gateways`` works as intended.
    
    Case: failing on an exception.
    
    This function is a coroutine.
    """
    task_group = TaskGroup(KOKORO)
    task = None
    
    try:
        max_concurrency = 4
        gateways = (TestGatewayShard(), TestGatewayShard(), TestGatewayShard(), TestGatewayShard())
        
        sleep_counter = 0
        
        async def mock_sleep(duration, loop = None):
            nonlocal sleep_counter
            sleep_counter += 1
            return
        
        exception = RuntimeError('hey mister')
        
        mocked = vampytest.mock_globals(
            _connect_gateways,
            sleep = mock_sleep,
        )
        
        task = Task(KOKORO, mocked(task_group, gateways, max_concurrency))
        
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        vampytest.assert_false(task.is_done())
        vampytest.assert_eq(len(task_group.pending), 8)
        for gateway in gateways:
            vampytest.assert_is_not(gateway.waiter, None)
        
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        gateways[2].set_waiter(True, exception)
        
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        vampytest.assert_true(task.is_done())
        vampytest.assert_eq(len(task_group.pending), 7)
        
        with vampytest.assert_raises(exception):
            task.get_result()
    
    finally:
        task_group.cancel_all()
        
        if (task is not None):
            task.cancel()
