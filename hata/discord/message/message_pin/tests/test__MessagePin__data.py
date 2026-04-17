from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_timestamp

from ...message import Message

from ..message_pin import MessagePin

from .test__MessagePin__constructor import _assert_fields_set


def test__MessagePin__from_data():
    """
    Tests whether ``MessagePin.__new__`` works as intended.
    """
    message = Message.precreate(202511070011)
    pinned_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    data = {
        'message': message.to_data(include_internals = True),
        'pinned_at': datetime_to_timestamp(pinned_at),
    }
    
    message_pin = MessagePin.from_data(data)
    
    _assert_fields_set(message_pin)
    
    vampytest.assert_is(message_pin.message, message)
    vampytest.assert_eq(message_pin.pinned_at, pinned_at)


def test__MessagePin__to_data():
    """
    Tests whether ``MessagePin.__new__`` works as intended.
    """
    message = Message.precreate(202511070012)
    pinned_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    message_pin = MessagePin(
        message = message,
        pinned_at = pinned_at,
    )
    
    vampytest.assert_eq(
        message_pin.to_data(defaults = True),
        {
            'message': message.to_data(defaults = True, include_internals = True),
            'pinned_at': datetime_to_timestamp(pinned_at),
        },
    )
