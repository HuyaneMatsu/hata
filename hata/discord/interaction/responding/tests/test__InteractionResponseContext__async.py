import vampytest
from scarletio import Task, skip_poll_cycle

from ...interaction_event import InteractionEvent

from ..constants import (
    RESPONSE_FLAG_DEFERRED, RESPONSE_FLAG_DEFERRING, RESPONSE_FLAG_EPHEMERAL, RESPONSE_FLAG_RESPONDED,
    RESPONSE_FLAG_RESPONDING
)
from ..context import InteractionResponseContext


async def test__InteractionResponseContext__ensure__0():
    """
    Tests whether ``InteractionResponseContext.ensure`` works as intended.
    
    Case: Runs the ensured coroutine.
    """
    ran = False
    
    async def to_ensure():
        nonlocal ran
        await skip_poll_cycle()
        ran = True
    
    deferring = False
    ephemeral = False
    interaction_event = InteractionEvent()
    
    context = InteractionResponseContext(
        interaction_event,
        deferring,
        ephemeral,
    )
    
    vampytest.assert_is(interaction_event._async_task, None)
    await context.ensure(to_ensure())
    vampytest.assert_instance(interaction_event._async_task, Task)
    
    await skip_poll_cycle()
    
    vampytest.assert_is(interaction_event._async_task, None)
    vampytest.assert_true(ran)


async def test__InteractionResponseContext__ensure__1():
    """
    Tests whether ``InteractionResponseContext.ensure`` works as intended.
    
    Case: handles exceptions.
    """
    async def to_ensure():
        await skip_poll_cycle()
        raise ValueError()
    
    deferring = False
    ephemeral = False
    interaction_event = InteractionEvent()
    
    context = InteractionResponseContext(
        interaction_event,
        deferring,
        ephemeral,
    )
    
    await context.ensure(to_ensure())
    
    with vampytest.assert_raises(ValueError):
        await interaction_event._async_task
    
    vampytest.assert_is(interaction_event._async_task, None)


async def test__InteractionResponseContext__context__0():
    """
    Tests whether ``InteractionResponseContext.ensure`` works as intended.
    
    Case: Whether entering waits for already running task.
    """
    ran = False
    
    async def to_ensure():
        nonlocal ran
        
        await skip_poll_cycle()
        
        ran = True
    
    deferring = False
    ephemeral = False
    interaction_event = InteractionEvent()
    
    context = InteractionResponseContext(
        interaction_event,
        deferring,
        ephemeral,
    )
    
    await context.ensure(to_ensure())
    
    async with context:
        vampytest.assert_true(ran)


async def test__InteractionResponseContext__context__1():
    """
    Tests whether ``InteractionResponseContext.ensure`` works as intended.
    
    Case: Whether response flags are set correctly: success.
    """
    deferring = False
    ephemeral = False
    interaction_event = InteractionEvent()
    
    context = InteractionResponseContext(
        interaction_event,
        deferring,
        ephemeral,
    )
    
    async with context:
        vampytest.assert_true(interaction_event._response_flag & RESPONSE_FLAG_RESPONDING)
        
    vampytest.assert_true(interaction_event._response_flag & RESPONSE_FLAG_RESPONDED)
    vampytest.assert_false(interaction_event._response_flag & RESPONSE_FLAG_RESPONDING)


async def test__InteractionResponseContext__context__2():
    """
    Tests whether ``InteractionResponseContext.ensure`` works as intended.
    
    Case: Whether response flags are set correctly: deferring + ephemeral + success.
    """
    deferring = True
    ephemeral = True
    interaction_event = InteractionEvent()
    
    context = InteractionResponseContext(
        interaction_event,
        deferring,
        ephemeral,
    )
    
    async with context:
        vampytest.assert_true(interaction_event._response_flag & RESPONSE_FLAG_DEFERRING)
        
    vampytest.assert_true(interaction_event._response_flag & RESPONSE_FLAG_DEFERRED)
    vampytest.assert_false(interaction_event._response_flag & RESPONSE_FLAG_DEFERRING)
    vampytest.assert_true(interaction_event._response_flag & RESPONSE_FLAG_EPHEMERAL)


async def test__InteractionResponseContext__context__3():
    """
    Tests whether ``InteractionResponseContext.ensure`` works as intended.
    
    Case: Whether response flags are set correctly: failure.
    """
    deferring = False
    ephemeral = False
    interaction_event = InteractionEvent()
    
    context = InteractionResponseContext(
        interaction_event,
        deferring,
        ephemeral,
    )
    
    with vampytest.assert_raises(ValueError):
        async with context:
            vampytest.assert_true(interaction_event._response_flag & RESPONSE_FLAG_RESPONDING)
            raise ValueError()
    
    vampytest.assert_false(interaction_event._response_flag & RESPONSE_FLAG_RESPONDED)
    vampytest.assert_false(interaction_event._response_flag & RESPONSE_FLAG_RESPONDING)
