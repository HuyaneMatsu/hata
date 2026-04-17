from collections import deque

import vampytest
from scarletio import Task, TimerHandle, skip_ready_cycle, sleep

from ...core import KOKORO

from ..rate_limit import GatewayRateLimiter


def _assert_fields_set(rate_limiter):
    """
    Tests whether the given gateway rate limiter has all of its attributes set as intended.
    
    Parameters
    ----------
    rate_limiter : ``GatewayRateLimiter``
        The rate limiter to test.
    """
    vampytest.assert_instance(rate_limiter, GatewayRateLimiter)
    vampytest.assert_instance(rate_limiter.queue, deque)
    vampytest.assert_instance(rate_limiter.remaining, int)
    vampytest.assert_instance(rate_limiter.resets_at, float)
    vampytest.assert_instance(rate_limiter.wake_up_handle, TimerHandle, nullable = True)


def test__GatewayRateLimiter__new():
    """
    Tests whether ``GatewayRateLimiter.__new__`` works as intended.
    """
    rate_limiter = GatewayRateLimiter()
    _assert_fields_set(rate_limiter)



def test__GatewayRateLimiter__repr():
    """
    Tests whether ``GatewayRateLimiter.__repr__`` works as intended.
    """
    rate_limiter = GatewayRateLimiter()
    
    output = repr(rate_limiter)
    vampytest.assert_instance(output, str)


async def test__GatewayRateLimiter__await__no_limit_hit():
    """
    Tests whether ``GatewayRateLimiter.__await__`` works as intended.
    
    Case: Limit not hit.
    
    This function is a coroutine.
    """
    rate_limiter = GatewayRateLimiter()
    
    task = Task(KOKORO, rate_limiter.__await__())
    try:
        await skip_ready_cycle()
        
        vampytest.assert_true(task.is_done())
        
        output = task.get_result()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, True)
    finally:
        task.cancel()


async def test__GatewayRateLimiter__await__limit_hit():
    """
    Tests whether ``GatewayRateLimiter.__await__`` works as intended.
    
    Case: Limit hit.
    
    This function is a coroutine.
    """
    rate_limiter = GatewayRateLimiter()
    gateway_rate_limit_reset = 0.000000001
    
    mocked = vampytest.mock_globals(
        GatewayRateLimiter.__await__,
        GATEWAY_RATE_LIMIT_RESET = gateway_rate_limit_reset,
        GATEWAY_RATE_LIMIT_LIMIT = 0,
    )
    task = Task(KOKORO, mocked(rate_limiter))
    try:
        await skip_ready_cycle()
        
        vampytest.assert_false(task.is_done())
        
        await sleep(gateway_rate_limit_reset, KOKORO)
        vampytest.assert_true(task.is_done())
        
        output = task.get_result()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, True)
    finally:
        task.cancel()


async def test__GatewayRateLimiter__wake_up__single_loop():
    """
    Tests whether ``GatewayRateLimiter.wake_up`` works as intended.
    
    Case: single loop.
    
    This function is a coroutine.
    """
    rate_limiter = GatewayRateLimiter()
    gateway_rate_limit_reset = 0.000000001
    
    mocked = vampytest.mock_globals(
        GatewayRateLimiter.__await__,
        GATEWAY_RATE_LIMIT_RESET = gateway_rate_limit_reset,
        GATEWAY_RATE_LIMIT_LIMIT = 0,
    )
    task = Task(KOKORO, mocked(rate_limiter))
    
    try:
        await skip_ready_cycle()
        
        rate_limiter.wake_up()
        await skip_ready_cycle()
        
        vampytest.assert_true(task.is_done())
        
        output = task.get_result()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, True)
    finally:
        rate_limiter.cancel()


async def test__GatewayRateLimiter__wake_up__multiple_loops():
    """
    Tests whether ``GatewayRateLimiter.wake_up`` works as intended.
    
    Case: multiple loops.
    
    This function is a coroutine.
    """
    rate_limiter = GatewayRateLimiter()
    gateway_rate_limit_reset = 0.000000001
    
    mocked = vampytest.mock_globals(
        GatewayRateLimiter.__await__,
        GATEWAY_RATE_LIMIT_RESET = gateway_rate_limit_reset,
        GATEWAY_RATE_LIMIT_LIMIT = 0,
    )
    
    task_0 = Task(KOKORO, mocked(rate_limiter))
    task_1 = Task(KOKORO, mocked(rate_limiter))
    
    try:
        await skip_ready_cycle()
        
        mocked = vampytest.mock_globals(
            GatewayRateLimiter.wake_up,
            GATEWAY_RATE_LIMIT_RESET = gateway_rate_limit_reset,
            GATEWAY_RATE_LIMIT_LIMIT = 1,
        )
        mocked(rate_limiter)
        
        await skip_ready_cycle()
        
        vampytest.assert_true(task_0.is_done())
        vampytest.assert_false(task_1.is_done())
        
        output = task_0.get_result()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, True)
    finally:
        rate_limiter.cancel()


async def test__GatewayRateLimiter__cancel():
    """
    Tests whether ``GatewayRateLimiter.close`` works as intended.
    
    This function is a coroutine.
    """
    rate_limiter = GatewayRateLimiter()
    gateway_rate_limit_reset = 0.000000001
    
    mocked = vampytest.mock_globals(
        GatewayRateLimiter.__await__,
        GATEWAY_RATE_LIMIT_RESET = gateway_rate_limit_reset,
        GATEWAY_RATE_LIMIT_LIMIT = 0,
    )
    
    task_0 = Task(KOKORO, mocked(rate_limiter))
    task_1 = Task(KOKORO, mocked(rate_limiter))
    
    try:
        await skip_ready_cycle()
        
        rate_limiter.cancel()
        
        await skip_ready_cycle()
        
        vampytest.assert_true(task_0.is_done())
        vampytest.assert_true(task_1.is_done())
        
        output = task_0.get_result()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, False)
        
        output = task_1.get_result()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, False)
        
        vampytest.assert_is(rate_limiter.wake_up_handle, None)
    finally:
        rate_limiter.cancel()
