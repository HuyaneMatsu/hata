import vampytest
from scarletio import Task, TaskGroup, skip_ready_cycle

from ...core import KOKORO

from ..client_sharder import _connect_gateway_batch

from .helpers_gateway_shard import TestGatewayShard


async def test__connect_gateway_batch__success():
    """
    Tests whether ``_connect_gateway_batch`` works as intended.
    
    Case: success.
    
    This function is a coroutine.
    """
    task_group = TaskGroup(KOKORO)
    task = None
    
    try:
        gateways = [TestGatewayShard(), TestGatewayShard(), TestGatewayShard(), TestGatewayShard()]
        
        task = Task(KOKORO, _connect_gateway_batch(task_group, gateways))
        
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        vampytest.assert_false(task.is_done())
        vampytest.assert_eq(len(task_group.pending), 8)
        for gateway in gateways:
            vampytest.assert_is_not(gateway.waiter, None)
        
        # set waiters
        for gateway in gateways[:2]:
            gateway.set_waiter(False, True)
        
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        vampytest.assert_false(task.is_done())
        vampytest.assert_eq(len(task_group.pending), 6)
        
        # set waiters (second part)
        for gateway in gateways[2:]:
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
        


async def test__connect_gateway_batch__failing_return():
    """
    Tests whether ``_connect_gateway_batch`` works as intended.
    
    Case: Fails (by return).
    
    This function is a coroutine.
    """
    task_group = TaskGroup(KOKORO)
    task = None
    
    try:
        gateways = [TestGatewayShard(), TestGatewayShard(), TestGatewayShard(), TestGatewayShard()]
        
        task = Task(KOKORO, _connect_gateway_batch(task_group, gateways))
        
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        vampytest.assert_false(task.is_done())
        vampytest.assert_eq(len(task_group.pending), 8)
        for gateway in gateways:
            vampytest.assert_is_not(gateway.waiter, None)
        
        # set waiter to False now
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


async def test__connect_gateway_batch__failing_exception():
    """
    Tests whether ``_connect_gateway_batch`` works as intended.
    
    Case: Fails (by return).
    
    This function is a coroutine.
    """
    task_group = TaskGroup(KOKORO)
    task = None
    
    try:
        gateways = [TestGatewayShard(), TestGatewayShard(), TestGatewayShard(), TestGatewayShard()]
        exception = RuntimeError('hey mister')
        
        task = Task(KOKORO, _connect_gateway_batch(task_group, gateways))
        
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        vampytest.assert_false(task.is_done())
        vampytest.assert_eq(len(task_group.pending), 8)
        for gateway in gateways:
            vampytest.assert_is_not(gateway.waiter, None)
        
        # set waiter to False now
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
