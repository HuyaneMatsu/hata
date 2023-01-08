import vampytest

from ....core import BUILTIN_EMOJIS
from ....message import Message
from ....user import User

from ..add import ReactionAddEvent
from ..delete import ReactionDeleteEvent


@vampytest.call_with(ReactionAddEvent)
@vampytest.call_with(ReactionDeleteEvent)
def test__Event__repr(event_type):
    """
    Tests whether `.__repr__` works as intended.
    
    Parameters
    ----------
    event_type : `type<ReactionAddEvent>`
        The event's type.
    """
    emoji = BUILTIN_EMOJIS['x']
    message = Message.precreate(202301030012)
    user = User.precreate(202301030013)
    
    event = event_type(message, emoji, user)
    
    vampytest.assert_instance(repr(event), str)


@vampytest.call_with(ReactionAddEvent)
@vampytest.call_with(ReactionDeleteEvent)
def test__Event__hash(event_type):
    """
    Tests whether `.__hash__` works as intended.
    
    Parameters
    ----------
    event_type : `type<ReactionAddEvent>`
        The event's type.
    """
    emoji = BUILTIN_EMOJIS['x']
    message = Message.precreate(202301030014)
    user = User.precreate(202301030015)
    
    event = event_type(message, emoji, user)
    
    vampytest.assert_instance(hash(event), int)


@vampytest.call_with(ReactionAddEvent)
@vampytest.call_with(ReactionDeleteEvent)
def test__Event__unpack(event_type):
    """
    Tests whether unpacking works as intended.
    
    Parameters
    ----------
    event_type : `type<ReactionAddEvent>`
        The event's type.
    """
    emoji = BUILTIN_EMOJIS['x']
    message = Message.precreate(202301030016)
    user = User.precreate(202301030017)
    
    event = event_type(message, emoji, user)
    
    expected_length = len(event)
    vampytest.assert_instance(expected_length, int)
    
    unpacked = [*event]
    vampytest.assert_eq(len(unpacked), expected_length)


@vampytest.call_with(ReactionAddEvent)
@vampytest.call_with(ReactionDeleteEvent)
def test__Event__hash(event_type):
    """
    Tests whether `.__eq__` works as intended.
    
    Parameters
    ----------
    event_type : `type<ReactionAddEvent>`
        The event's type.
    """
    emoji = BUILTIN_EMOJIS['x']
    message = Message.precreate(202301030018)
    user = User.precreate(202301030019)
    
    keyword_parameters = {
        'emoji': emoji,
        'message': message,
        'user': user,
    }
    
    event = event_type(**keyword_parameters)
    vampytest.assert_eq(event, event)
    
    for field_name, field_value in (
        ('emoji', BUILTIN_EMOJIS['heart']),
        ('message', Message.precreate(202301030020)),
        ('user', User.precreate(202301030021)),
    ):
        test_event = event_type(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(event, test_event)
