import vampytest

from ....message import Message

from ..add import PollVoteAddEvent
from ..delete import PollVoteDeleteEvent


def _assert_fields_set(event, event_type):
    """
    Asserts whether every fields are set of the given event.
    
    Parameters
    ----------
    event : `instance<event_type>`
        The event to check.
    event_type : `type<PollVoteAddEvent>`
        The event's expected type.
    """
    vampytest.assert_instance(event, event_type)
    vampytest.assert_instance(event.answer_id, int)
    vampytest.assert_instance(event.message, Message)
    vampytest.assert_instance(event.user_id, int)


@vampytest.call_with(PollVoteAddEvent)
@vampytest.call_with(PollVoteDeleteEvent)
def test__Event__new__minimal(event_type):
    """
    Tests whether `.__new__` works as intended.
    
    Case: Minimal amount of fields.
    
    Parameters
    ----------
    event_type : `type<PollVoteAddEvent>`
        The event's type.
    """
    answer_id = 202404030010
    message = Message.precreate(202404030011)
    user_id = 202404030012
    
    event = event_type(message, answer_id, user_id)
    _assert_fields_set(event, event_type)
    
    vampytest.assert_eq(event.answer_id, answer_id)
    vampytest.assert_is(event.message, message)
    vampytest.assert_eq(event.user_id, user_id)


@vampytest.call_with(PollVoteAddEvent)
@vampytest.call_with(PollVoteDeleteEvent)
def test__Event__from_fields(event_type):
    """
    Tests whether `.from_fields` works as intended.
    
    Parameters
    ----------
    event_type : `type<PollVoteAddEvent>`
        The event's type.
    """
    answer_id = 202404030013
    message = Message.precreate(202404030014)
    user_id = 202404030015
    
    event = event_type.from_fields(message, answer_id, user_id)
    _assert_fields_set(event, event_type)
    
    vampytest.assert_eq(event.answer_id, answer_id)
    vampytest.assert_is(event.message, message)
    vampytest.assert_eq(event.user_id, user_id)
