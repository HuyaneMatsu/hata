import vampytest

from ....core import BUILTIN_EMOJIS
from ....message import Message
from ....user import ClientUserBase, User

from ...emoji import Emoji

from ..add import ReactionAddEvent
from ..delete import ReactionDeleteEvent


def _assert_fields_set(event_type, event):
    """
    Asserts whether every fields are set of the given event.
    
    Parameters
    ----------
    event_type : `type<ReactionAddEvent>`
        The event's expected type.
    event : `instance<event_type>`
        The event to check.
    """
    vampytest.assert_instance(event, event_type)
    vampytest.assert_instance(event.emoji, Emoji)
    vampytest.assert_instance(event.message, Message)
    vampytest.assert_instance(event.user, ClientUserBase)



@vampytest.call_with(ReactionAddEvent)
@vampytest.call_with(ReactionDeleteEvent)
def test__Event__new(event_type):
    """
    Tests whether `.__new__` works as intended.
    
    Parameters
    ----------
    event_type : `type<ReactionAddEvent>`
        The event's type.
    """
    emoji = BUILTIN_EMOJIS['x']
    message = Message.precreate(202301030000)
    user = User.precreate(202301030001)
    
    event = event_type(message, emoji, user)
    _assert_fields_set(event_type, event)
    
    vampytest.assert_is(event.emoji, emoji)
    vampytest.assert_is(event.message, message)
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
    
    event = event_type.from_fields(message, emoji, user)
    _assert_fields_set(event_type, event)
    
    vampytest.assert_is(event.emoji, emoji)
    vampytest.assert_is(event.message, message)
    vampytest.assert_is(event.user, user)
