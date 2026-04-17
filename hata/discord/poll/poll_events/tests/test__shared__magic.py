import vampytest

from ....message import Message

from ..add import PollVoteAddEvent
from ..delete import PollVoteDeleteEvent


@vampytest.call_with(PollVoteAddEvent)
@vampytest.call_with(PollVoteDeleteEvent)
def test__Event__repr(event_type):
    """
    Tests whether `.__repr__` works as intended.
    
    Parameters
    ----------
    event_type : `type<PollVoteAddEvent>`
        The event's type.
    """
    answer_id = 202404030026
    message = Message.precreate(202404030027)
    user_id = 202404030028
    
    event = event_type(message, answer_id, user_id)
    
    vampytest.assert_instance(repr(event), str)


@vampytest.call_with(PollVoteAddEvent)
@vampytest.call_with(PollVoteDeleteEvent)
def test__Event__hash(event_type):
    """
    Tests whether `.__hash__` works as intended.
    
    Parameters
    ----------
    event_type : `type<PollVoteAddEvent>`
        The event's type.
    """
    answer_id = 202404030029
    message = Message.precreate(202404030030)
    user_id = 202404030031
    
    event = event_type(message, answer_id, user_id)
    
    vampytest.assert_instance(hash(event), int)


@vampytest.call_with(PollVoteAddEvent)
@vampytest.call_with(PollVoteDeleteEvent)
def test__Event__unpack(event_type):
    """
    Tests whether unpacking works as intended.
    
    Parameters
    ----------
    event_type : `type<PollVoteAddEvent>`
        The event's type.
    """
    answer_id = 202404030032
    message = Message.precreate(202404030033)
    user_id = 202404030034
    
    event = event_type(message, answer_id, user_id)
    
    expected_length = len(event)
    vampytest.assert_instance(expected_length, int)
    
    unpacked = [*event]
    vampytest.assert_eq(len(unpacked), expected_length)


@vampytest.call_with(PollVoteAddEvent)
@vampytest.call_with(PollVoteDeleteEvent)
def test__Event__eq(event_type):
    """
    Tests whether `.__eq__` works as intended.
    
    Parameters
    ----------
    event_type : `type<PollVoteAddEvent>`
        The event's type.
    """
    answer_id = 202404030035
    message = Message.precreate(202404030036)
    user_id = 202404030037
    
    keyword_parameters = {
        'answer_id': answer_id,
        'message': message,
        'user_id': user_id,
    }
    
    event = event_type(**keyword_parameters)
    vampytest.assert_eq(event, event)
    
    for field_name, field_value in (
        ('answer_id', 202404030064),
        ('message', Message.precreate(202404030038)),
        ('user_id', 202404030039),
    ):
        test_event = event_type(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(event, test_event)
