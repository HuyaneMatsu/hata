import vampytest

from ....channel import Channel, ChannelType
from ....core import BUILTIN_EMOJIS
from ....guild import Guild
from ....message import Message
from ....user import User

from ..add import ReactionAddEvent
from ..delete import ReactionDeleteEvent

from .test__shared__constructor import _assert_fields_set


@vampytest.call_with(ReactionAddEvent)
@vampytest.call_with(ReactionDeleteEvent)
def test__Event__copy(event_type):
    """
    Tests whether `.copy` works as intended.
    
    Parameters
    ----------
    event_type : `type<ReactionAddEvent>`
        The event's type.
    """
    emoji = BUILTIN_EMOJIS['x']
    message = Message.precreate(202301030022)
    user = User.precreate(202301030023)
    
    event = event_type(message, emoji, user)
    copy = event.copy()
    _assert_fields_set(event_type, copy)
    vampytest.assert_is_not(event, copy)
    
    vampytest.assert_eq(event, copy)


@vampytest.call_with(ReactionAddEvent)
@vampytest.call_with(ReactionDeleteEvent)
def test__Event__copy_with__0(event_type):
    """
    Tests whether `.copy_with` works as intended.
    
    Case: No fields given.
    
    Parameters
    ----------
    event_type : `type<ReactionAddEvent>`
        The event's type.
    """
    emoji = BUILTIN_EMOJIS['x']
    message = Message.precreate(202301030024)
    user = User.precreate(202301030025)
    
    event = event_type(message, emoji, user)
    copy = event.copy_with()
    _assert_fields_set(event_type, copy)
    vampytest.assert_is_not(event, copy)
    
    vampytest.assert_eq(event, copy)


@vampytest.call_with(ReactionAddEvent)
@vampytest.call_with(ReactionDeleteEvent)
def test__Event__copy_with__1(event_type):
    """
    Tests whether `.copy_with` works as intended.
    
    Case: All fields given.
    
    Parameters
    ----------
    event_type : `type<ReactionAddEvent>`
        The event's type.
    """
    old_emoji = BUILTIN_EMOJIS['x']
    old_message = Message.precreate(202301030026)
    old_user = User.precreate(202301030027)
    new_emoji = BUILTIN_EMOJIS['heart']
    new_message = Message.precreate(202301030028)
    new_user = User.precreate(202301030029)
    
    event = event_type(old_message, old_emoji, old_user)
    copy = event.copy_with(emoji = new_emoji, message = new_message, user = new_user)
    _assert_fields_set(event_type, copy)
    vampytest.assert_is_not(event, copy)
    
    vampytest.assert_is(copy.emoji, new_emoji)
    vampytest.assert_is(copy.message, new_message)
    vampytest.assert_is(copy.user, new_user)

# SKip this one till client testing is added.
'''
@vampytest.call_with(ReactionAddEvent)
@vampytest.call_with(ReactionDeleteEvent)
async def test__Event__delete_reaction_with(event_type):
    """
    Tests whether `.copy_with` works as intended.
    
    Case: All fields given.
    
    Parameters
    ----------
    event_type : `type<ReactionAddEvent>`
        The event's type.
    """
'''
