import vampytest
from scarletio import Future

from ....core import INTERACTION_EVENT_MESSAGE_WAITERS, INTERACTION_EVENT_RESPONSE_WAITERS, KOKORO
from ....interaction import InteractionEvent

from ...message_interaction import MessageInteraction

from ..message import Message
from ..utils import try_resolve_interaction_message


def test__try_resolve_interaction_message__miss():
    """
    Tests whether ``try_resolve_interaction_message`` works as intended.
    
    Case: miss.
    """
    interaction_id = 202305060002
    message_id = 202305060003
    
    message_interaction = MessageInteraction.precreate(interaction_id)
    message = Message.precreate(message_id)
    
    try_resolve_interaction_message(message, message_interaction)


def test__try_resolve_interaction_message__hit_no_waiter():
    """
    Tests whether ``try_resolve_interaction_message`` works as intended.
    
    Case: hit, but no waiter.
    """
    interaction_id = 202305060003
    message_id = 202305060004
    
    message_interaction = MessageInteraction.precreate(interaction_id)
    message = Message.precreate(message_id)
    interaction_event = InteractionEvent.precreate(interaction_id)
    INTERACTION_EVENT_RESPONSE_WAITERS[interaction_id] = interaction_event
    
    try_resolve_interaction_message(message, message_interaction)
    
    vampytest.assert_not_in(interaction_id, INTERACTION_EVENT_RESPONSE_WAITERS)
    vampytest.assert_is(interaction_event.message, message)


def test__try_resolve_interaction_message__hit_with_waiter():
    """
    Tests whether ``try_resolve_interaction_message`` works as intended.
    
    Case: hit with waiter.
    """
    interaction_id = 202305060005
    message_id = 202305060006
    
    message_interaction = MessageInteraction.precreate(interaction_id)
    message = Message.precreate(message_id)
    interaction_event = InteractionEvent.precreate(interaction_id)
    INTERACTION_EVENT_RESPONSE_WAITERS[interaction_id] = interaction_event
    waiter = Future(KOKORO)
    INTERACTION_EVENT_MESSAGE_WAITERS[interaction_event] = waiter
    
    try_resolve_interaction_message(message, message_interaction)
    
    vampytest.assert_not_in(interaction_id, INTERACTION_EVENT_RESPONSE_WAITERS)
    vampytest.assert_not_in(interaction_event, INTERACTION_EVENT_MESSAGE_WAITERS)
    vampytest.assert_is(interaction_event.message, message)
    vampytest.assert_true(waiter.is_done())
