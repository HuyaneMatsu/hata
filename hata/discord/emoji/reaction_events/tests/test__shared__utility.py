import vampytest

from ....core import BUILTIN_EMOJIS
from ....message import Message
from ....user import User

from ...reaction import Reaction, ReactionType

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
    reaction_type = ReactionType.burst
    
    event = event_type(message, emoji, user, reaction_type = reaction_type)
    copy = event.copy()
    _assert_fields_set(copy, event_type)
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
    reaction_type = ReactionType.burst
    
    event = event_type(message, emoji, user, reaction_type = reaction_type)
    copy = event.copy_with()
    _assert_fields_set(copy, event_type)
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
    old_reaction_type = ReactionType.standard
    
    new_emoji = BUILTIN_EMOJIS['heart']
    new_message = Message.precreate(202301030028)
    new_user = User.precreate(202301030029)
    new_reaction_type = ReactionType.burst
    
    event = event_type(old_message, old_emoji, old_user, reaction_type = old_reaction_type)
    copy = event.copy_with(emoji = new_emoji, message = new_message, user = new_user, reaction_type = new_reaction_type)
    _assert_fields_set(copy, event_type)
    vampytest.assert_is_not(event, copy)
    
    vampytest.assert_is(copy.emoji, new_emoji)
    vampytest.assert_is(copy.message, new_message)
    vampytest.assert_is(copy.type, new_reaction_type)
    vampytest.assert_is(copy.user, new_user)


@vampytest.call_with(ReactionAddEvent)
@vampytest.call_with(ReactionDeleteEvent)
def test__Event__reaction(event_type):
    """
    Tests whether `.reaction` works as intended.
    
    Parameters
    ----------
    event_type : `type<ReactionAddEvent>`
        The event's type.
    """
    emoji = BUILTIN_EMOJIS['x']
    message = Message.precreate(202301030024)
    user = User.precreate(202301030025)
    reaction_type = ReactionType.burst
    
    event = event_type(message, emoji, user, reaction_type = reaction_type)
    
    reaction = event.reaction
    vampytest.assert_instance(reaction, Reaction)
    vampytest.assert_is(reaction.emoji, emoji)
    vampytest.assert_is(reaction.type, reaction_type)


# Skip this one till client testing is added.
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
