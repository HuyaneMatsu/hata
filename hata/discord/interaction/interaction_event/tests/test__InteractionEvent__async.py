import vampytest
from scarletio import Task, future_or_timeout, skip_poll_cycle, skip_ready_cycle

from ....core import KOKORO, INTERACTION_EVENT_MESSAGE_WAITERS
from ....message import Message

from ..interaction_event import InteractionEvent


async def test__InteractionEvent__wait_for_response_message__0():
    """
    Tests whether ``InteractionEvent.wait_for_response_message`` works as intended.
    
    Case: instant pass.
    """
    message = Message.precreate(202211070047)
    
    interaction_event = InteractionEvent(message = message)
    
    task = Task(interaction_event.wait_for_response_message(), KOKORO)
    future_or_timeout(task, 0.015)
    output = await task
    
    vampytest.assert_is(output, message)


async def test__InteractionEvent__wait_for_response_message__1():
    """
    Tests whether ``InteractionEvent.wait_for_response_message`` works as intended.
    
    Case: set message.
    """
    message = Message.precreate(202211070048)
    
    interaction_event = InteractionEvent()
    
    task = Task(interaction_event.wait_for_response_message(), KOKORO)
    await skip_ready_cycle()
    
    INTERACTION_EVENT_MESSAGE_WAITERS[interaction_event].set_result(None)
    interaction_event.message = message
    
    future_or_timeout(task, 0.015)
    output = await task
    
    vampytest.assert_is(output, message)


async def test__InteractionEvent__wait_for_response_message__2():
    """
    Tests whether ``InteractionEvent.wait_for_response_message`` works as intended.
    
    Case: timeout.
    """
    interaction_event = InteractionEvent()
    
    task = Task(interaction_event.wait_for_response_message(timeout = 0), KOKORO)
    
    await skip_poll_cycle()
    await skip_ready_cycle()
    
    with vampytest.assert_raises(TimeoutError):
        task.get_result()
