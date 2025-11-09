from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...message import Message

from ..message_pin import MessagePin


def test__MessagePin__repr():
    """
    Tests whether ``MessagePin.__repr__`` works as intended.
    """
    message = Message.precreate(202511070013)
    pinned_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    message_pin = MessagePin(
        message = message,
        pinned_at = pinned_at,
    )
    
    output = repr(message_pin)
    vampytest.assert_instance(output, str)


def test__MessagePin__hash():
    """
    Tests whether ``MessagePin.__repr__`` works as intended.
    """
    message = Message.precreate(202511070014)
    pinned_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    message_pin = MessagePin(
        message = message,
        pinned_at = pinned_at,
    )
    
    output = hash(message_pin)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    message = Message.precreate(202511070015)
    pinned_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    keyword_parameters = {
        'message': message,
        'pinned_at': pinned_at,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'message': Message.precreate(202511070016),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'pinned_at': DateTime(2016, 5, 15, tzinfo = TimeZone.utc),
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__MessagePin__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``MessagePin.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    message_pin_0 = MessagePin(**keyword_parameters_0)
    message_pin_1 = MessagePin(**keyword_parameters_1)
    
    output = message_pin_0 == message_pin_1
    vampytest.assert_instance(output, bool)
    return output
