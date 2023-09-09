import vampytest

from ....core import BUILTIN_EMOJIS
from ....message import Message
from ....user import ClientUserBase, User

from ...emoji import Emoji
from ...reaction import ReactionType

from ..add import ReactionAddEvent
from ..delete import ReactionDeleteEvent


def _assert_fields_set(event, event_type):
    """
    Asserts whether every fields are set of the given event.
    
    Parameters
    ----------
    event : `instance<event_type>`
        The event to check.
    event_type : `type<ReactionAddEvent>`
        The event's expected type.
    """
    vampytest.assert_instance(event, event_type)
    vampytest.assert_instance(event.emoji, Emoji)
    vampytest.assert_instance(event.message, Message)
    vampytest.assert_instance(event.type, ReactionType)
    vampytest.assert_instance(event.user, ClientUserBase)



@vampytest.call_with(ReactionAddEvent)
@vampytest.call_with(ReactionDeleteEvent)
def test__Event__new__minimal(event_type):
    """
    Tests whether `.__new__` works as intended.
    
    Case: Minimal amount of fields.
    
    Parameters
    ----------
    event_type : `type<ReactionAddEvent>`
        The event's type.
    """
    emoji = BUILTIN_EMOJIS['x']
    message = Message.precreate(202301030000)
    user = User.precreate(202301030001)
    
    event = event_type(message, emoji, user)
    _assert_fields_set(event, event_type)
    
    vampytest.assert_is(event.emoji, emoji)
    vampytest.assert_is(event.message, message)
    vampytest.assert_is(event.type, ReactionType.standard)
    vampytest.assert_is(event.user, user)


@vampytest.call_with(ReactionAddEvent)
@vampytest.call_with(ReactionDeleteEvent)
def test__Event__new__maximal(event_type):
    """
    Tests whether `.__new__` works as intended.
    
    Case: maximal amount of fields.
    
    Parameters
    ----------
    event_type : `type<ReactionAddEvent>`
        The event's type.
    """
    emoji = BUILTIN_EMOJIS['x']
    message = Message.precreate(202309040000)
    user = User.precreate(202309040001)
    reaction_type = ReactionType.burst
    
    event = event_type(message, emoji, user, reaction_type = reaction_type)
    _assert_fields_set(event, event_type)
    
    vampytest.assert_is(event.emoji, emoji)
    vampytest.assert_is(event.message, message)
    vampytest.assert_is(event.type, reaction_type)
    vampytest.assert_is(event.user, user)



@vampytest.call_with(ReactionAddEvent)
@vampytest.call_with(ReactionDeleteEvent)
def test__Event__from_fields(event_type):
    """
    Tests whether `.from_fields` works as intended.
    
    Parameters
    ----------
    event_type : `type<ReactionAddEvent>`
        The event's type.
    """
    emoji = BUILTIN_EMOJIS['x']
    message = Message.precreate(202301030002)
    user = User.precreate(202301030003)
    reaction_type = ReactionType.burst
    
    event = event_type.from_fields(message, emoji, user, reaction_type)
    _assert_fields_set(event, event_type)
    
    vampytest.assert_is(event.emoji, emoji)
    vampytest.assert_is(event.message, message)
    vampytest.assert_is(event.type, reaction_type)
    vampytest.assert_is(event.user, user)
