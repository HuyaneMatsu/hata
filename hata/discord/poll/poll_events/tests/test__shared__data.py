import vampytest

from ....message import Message

from ..add import PollVoteAddEvent
from ..delete import PollVoteDeleteEvent

from .test__shared__constructor import _assert_fields_set


@vampytest.call_with(PollVoteAddEvent)
@vampytest.call_with(PollVoteDeleteEvent)
def test__Event__from_data(event_type):
    """
    Tests whether `.from_data` works as intended.
    
    Parameters
    ----------
    event_type : `type<PollVoteAddEvent>`
        The event's type.
    """
    answer_id = 202404030016
    channel_id = 202404030017
    guild_id = 202404030018
    message_id = 202404030019
    user_id = 202404030020
    
    data = {
        'answer_id': str(answer_id),
        'channel_id': str(channel_id),
        'guild_id': str(guild_id),
        'message_id': str(message_id),
        'user_id': str(user_id),
    }
    
    event = event_type.from_data(data)
    _assert_fields_set(event, event_type)
    
    
    vampytest.assert_eq(event.answer_id, answer_id)
    vampytest.assert_eq(event.message.id, message_id)
    vampytest.assert_eq(event.message.channel_id, channel_id)
    vampytest.assert_eq(event.message.guild_id, guild_id)
    vampytest.assert_eq(event.user_id, user_id)


@vampytest.call_with(PollVoteAddEvent)
@vampytest.call_with(PollVoteDeleteEvent)
def test__Event__to_data(event_type):
    """
    Tests whether `.to_data` works as intended.
    
    Case: Include internals.
    
    Parameters
    ----------
    event_type : `type<PollVoteAddEvent>`
        The event's type.
    """
    answer_id = 202404030021
    channel_id = 202404030022
    guild_id = 202404030023
    message_id = 202404030024
    user_id = 202404030025
    
    message = Message.precreate(message_id, channel_id = channel_id, guild_id = guild_id)
    
    event = event_type(message, answer_id, user_id)
    
    expected_output = {
        'answer_id': str(answer_id),
        'channel_id': str(channel_id),
        'guild_id': str(guild_id),
        'message_id': str(message_id),
        'user_id': str(user_id),
    }
    
    vampytest.assert_eq(
        event.to_data(defaults = True),
        expected_output,
    )
