import vampytest

from ....core import BUILTIN_EMOJIS
from ....message import Message
from ....user import User

from ..add import ReactionAddEvent
from ..delete import ReactionDeleteEvent

from .test__shared__constructor import _assert_fields_set


@vampytest.call_with(ReactionAddEvent)
@vampytest.call_with(ReactionDeleteEvent)
def test__Event__from_data(event_type):
    """
    Tests whether `.from_data` works as intended.
    
    Parameters
    ----------
    event_type : `type<ReactionAddEvent>`
        The event's type.
    """
    emoji = BUILTIN_EMOJIS['x']
    channel_id = 202301030004
    guild_id = 202301030005
    message_id = 202301030006
    user_id = 202301030007
    
    data = {
        'emoji': {'name': emoji.unicode},
        'channel_id': str(channel_id),
        'guild_id': str(guild_id),
        'message_id': str(message_id),
        'user_id': str(user_id),
    }
    
    event = event_type.from_data(data)
    _assert_fields_set(event_type, event)
    
    
    vampytest.assert_is(event.emoji, emoji)
    vampytest.assert_eq(event.message.id, message_id)
    vampytest.assert_eq(event.message.channel_id, channel_id)
    vampytest.assert_eq(event.message.guild_id, guild_id)
    vampytest.assert_eq(event.user.id, user_id)


@vampytest.call_with(ReactionAddEvent)
@vampytest.call_with(ReactionDeleteEvent)
def test__Event__to_data(event_type):
    """
    Tests whether `.to_data` works as intended.
    
    Case: Include internals.
    
    Parameters
    ----------
    event_type : `type<ReactionAddEvent>`
        The event's type.
    """
    emoji = BUILTIN_EMOJIS['x']
    channel_id = 202301030008
    guild_id = 202301030009
    message_id = 202301030010
    user_id = 202301030011
    
    message = Message.precreate(message_id, channel_id = channel_id, guild_id = guild_id)
    user = User.precreate(user_id)
    
    event = event_type(message, emoji, user)
    
    expected_output = {
        'emoji': {'name': emoji.unicode},
        'channel_id': str(channel_id),
        'guild_id': str(guild_id),
        'message_id': str(message_id),
        'user_id': str(user_id),
    }
    
    vampytest.assert_eq(
        event.to_data(defaults = True),
        expected_output,
    )
