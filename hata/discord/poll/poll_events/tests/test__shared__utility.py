import vampytest

from ....message import Message
from ....user import ClientUserBase

from ..add import PollVoteAddEvent
from ..delete import PollVoteDeleteEvent

from .test__shared__constructor import _assert_fields_set


@vampytest.call_with(PollVoteAddEvent)
@vampytest.call_with(PollVoteDeleteEvent)
def test__Event__copy(event_type):
    """
    Tests whether `.copy` works as intended.
    
    Parameters
    ----------
    event_type : `type<PollVoteAddEvent>`
        The event's type.
    """
    answer_id = 202404030040
    message = Message.precreate(202404030041)
    user_id = 202404030042
    
    event = event_type(message, answer_id, user_id)
    copy = event.copy()
    _assert_fields_set(copy, event_type)
    vampytest.assert_is_not(event, copy)
    
    vampytest.assert_eq(event, copy)


@vampytest.call_with(PollVoteAddEvent)
@vampytest.call_with(PollVoteDeleteEvent)
def test__Event__copy_with__no_fields(event_type):
    """
    Tests whether `.copy_with` works as intended.
    
    Case: No fields given.
    
    Parameters
    ----------
    event_type : `type<PollVoteAddEvent>`
        The event's type.
    """
    answer_id = 202404030043
    message = Message.precreate(202404030044)
    user_id = 202404030045
    
    event = event_type(message, answer_id, user_id)
    copy = event.copy_with()
    _assert_fields_set(copy, event_type)
    vampytest.assert_is_not(event, copy)
    
    vampytest.assert_eq(event, copy)


@vampytest.call_with(PollVoteAddEvent)
@vampytest.call_with(PollVoteDeleteEvent)
def test__Event__copy_with__all_fields(event_type):
    """
    Tests whether `.copy_with` works as intended.
    
    Case: All fields given.
    
    Parameters
    ----------
    event_type : `type<PollVoteAddEvent>`
        The event's type.
    """
    old_answer_id = 202404030046
    old_message = Message.precreate(202404030047)
    old_user_id = 202404030048
    
    new_answer_id = 202404030049
    new_message = Message.precreate(202404030050)
    new_user_id = 202404030051
    
    event = event_type(old_message, old_answer_id, old_user_id)
    copy = event.copy_with(answer_id = new_answer_id, message = new_message, user_id = new_user_id)
    _assert_fields_set(copy, event_type)
    vampytest.assert_is_not(event, copy)
    
    vampytest.assert_eq(copy.answer_id, new_answer_id)
    vampytest.assert_is(copy.message, new_message)
    vampytest.assert_eq(copy.user_id, new_user_id)


@vampytest.call_with(PollVoteAddEvent)
@vampytest.call_with(PollVoteDeleteEvent)
def test__Event__user(event_type):
    """
    Tests whether `.user` works as intended.
    
    Parameters
    ----------
    event_type : `type<PollVoteAddEvent>`
        The event's type.
    """
    answer_id = 202404030052
    message = Message.precreate(202404030053)
    user_id = 202404030054
    
    event = event_type(message, answer_id, user_id)
    
    user = event.user
    vampytest.assert_instance(user, ClientUserBase)
    vampytest.assert_eq(user.id, user_id)
