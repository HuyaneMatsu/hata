from types import FunctionType

import vampytest

from scarletio import get_event_loop, skip_ready_cycle

from ....soundboard import SoundboardSoundsEvent

from ..soundboard_sounds_event_handler import SoundboardSoundsEventHandler
from ..soundboard_sounds_event_waiter import SoundboardSoundsEventWaiter


def _assert_fields_set(handler):
    """
    Asserts whether every fields are set of the given event handler.
    
    
    Parameters
    ----------
    handler : ``SoundboardSoundsEventHandler``
        The handler to check.
    """
    vampytest.assert_instance(handler, SoundboardSoundsEventHandler)
    vampytest.assert_instance(handler.waiters, dict)


def test__SoundboardSoundsEventHandler__event_name():
    """
    Tests whether ``SoundboardSoundsEventHandler.__event_name__`` is set.
    """
    vampytest.assert_instance(SoundboardSoundsEventHandler.__event_name__, str)


def test__SoundboardSoundsEventHandler__new():
    """
    Tests whether ``SoundboardSoundsEventHandler.__new__`` works as intended.
    """
    handler = SoundboardSoundsEventHandler()
    _assert_fields_set(handler)


def test__SoundboardSoundsEventHandler__repr():
    """
    Tests whether ``SoundboardSoundsEventHandler.__repr__`` works as intended.
    """
    handler = SoundboardSoundsEventHandler()
    vampytest.assert_instance(repr(handler), str)


async def test__SoundboardSoundsEventHandler__call__0():
    """
    Tests whether ``SoundboardSoundsEventHandler.__call__`` works as intended.
    
    Case: No water -> should do nothing.
    
    This function is a coroutine.
    """
    handler = SoundboardSoundsEventHandler()
    guild_id = 202305280000
    
    event = SoundboardSoundsEvent(guild_id = guild_id)
    
    await handler(NotImplemented, event)


async def test__SoundboardSoundsEventHandler__call__1():
    """
    Tests whether ``SoundboardSoundsEventHandler.__call__`` works as intended.
    
    Case: Has water -> should set result.
    
    This function is a coroutine.
    """
    handler = SoundboardSoundsEventHandler()
    waiter = SoundboardSoundsEventWaiter()
    guild_id = 202305280001
    handler.waiters[guild_id] = waiter
    
    event = SoundboardSoundsEvent(guild_id = guild_id)
    
    await handler(NotImplemented, event)
    
    vampytest.assert_false(handler.waiters)
    vampytest.assert_true(waiter.future.is_done())
    vampytest.assert_eq(waiter.future.get_result(), event)


async def test__SoundboardSoundsEventHandler__wait_for_events_in_guilds__0():
    """
    Tests whether ``SoundboardSoundsEventHandler.wait_for_events_in_guilds`` works as intended.
    
    Case: Passing.
    
    This function is a coroutine.
    """
    handler = SoundboardSoundsEventHandler()
    guild_id_0 = 202305280002
    guild_id_1 = 202305280003
    
    event_0 = SoundboardSoundsEvent(guild_id = guild_id_0)
    event_1 = SoundboardSoundsEvent(guild_id = guild_id_1)
    
    task = get_event_loop().create_task(handler.wait_for_events_in_guilds([guild_id_0, guild_id_1]))
    task.apply_timeout(0.01)
    
    await skip_ready_cycle()
    await handler(NotImplemented, event_0)
    await handler(NotImplemented, event_1)
    
    result = await task
    
    vampytest.assert_eq({*result}, {event_0, event_1})
    vampytest.assert_false(handler.waiters)


async def test__SoundboardSoundsEventHandler__wait_for_events_in_guilds__1():
    """
    Tests whether ``SoundboardSoundsEventHandler.wait_for_events_in_guilds`` works as intended.
    
    Case: One result timeouts.
    
    This function is a coroutine.
    """
    handler = SoundboardSoundsEventHandler()
    guild_id_0 = 202305280004
    guild_id_1 = 202305280005
    
    timeout = 0.005
    
    event_0 = SoundboardSoundsEvent(guild_id = guild_id_0)
    
    original = type(handler).wait_for_events_in_guilds
    copy = FunctionType(
        original.__code__,
        {**original.__globals__, 'SOUNDBOARD_SOUNDS_TIMEOUT': timeout},
        original.__name__,
        original.__defaults__,
        original.__closure__,
    )
    
    task = get_event_loop().create_task(copy(handler, [guild_id_0, guild_id_1]))
    task.apply_timeout(0.01)
    
    await skip_ready_cycle()
    await handler(NotImplemented, event_0)
    
    result = await task
    
    vampytest.assert_eq({*result}, {event_0})
    vampytest.assert_false(handler.waiters)


async def test__SoundboardSoundsEventHandler__wait_for_events_in_guilds__2():
    """
    Tests whether ``SoundboardSoundsEventHandler.wait_for_events_in_guilds`` works as intended.
    
    Case: Cancelled.
    
    This function is a coroutine.
    """
    handler = SoundboardSoundsEventHandler()
    guild_id_0 = 202305280006
    guild_id_1 = 202305280007
    
    task = get_event_loop().create_task(handler.wait_for_events_in_guilds([guild_id_0, guild_id_1]))
    await skip_ready_cycle()
    task.cancel()
    await skip_ready_cycle()
    
    vampytest.assert_false(handler.waiters)


async def test__SoundboardSoundsEventHandler__wait_for_events_in_guilds__3():
    """
    Tests whether ``SoundboardSoundsEventHandler.wait_for_events_in_guilds`` works as intended.
    
    Case: one of 2 waiters cancelled.
    
    This function is a coroutine.
    """
    handler = SoundboardSoundsEventHandler()
    guild_id_0 = 202305280008
    guild_id_1 = 202305280009
    
    event_0 = SoundboardSoundsEvent(guild_id = guild_id_0)
    event_1 = SoundboardSoundsEvent(guild_id = guild_id_1)
    
    task_0 = get_event_loop().create_task(handler.wait_for_events_in_guilds([guild_id_0, guild_id_1]))
    
    task_1 = get_event_loop().create_task(handler.wait_for_events_in_guilds([guild_id_0, guild_id_1]))
    task_1.apply_timeout(0.01)
    
    await skip_ready_cycle()
    task_0.cancel()
    await skip_ready_cycle()
    vampytest.assert_true(handler.waiters)

    await handler(NotImplemented, event_0)
    await handler(NotImplemented, event_1)
    
    result = await task_1
    
    vampytest.assert_eq({*result}, {event_0, event_1})
    vampytest.assert_false(handler.waiters)
