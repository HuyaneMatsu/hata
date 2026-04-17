from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...message import Message

from ..message_pin import MessagePin


def _assert_fields_set(message_pin):
    """
    Asserts whether every fields of the given instance are set correctly.
    
    Parameters
    ----------
    message_pin : ``MessagePin``
        The instance to check.
    """
    vampytest.assert_instance(message_pin, MessagePin)
    vampytest.assert_instance(message_pin.message, Message, nullable = True)
    vampytest.assert_instance(message_pin.pinned_at, DateTime)


def test__MessagePin__new__no_fields():
    """
    Tests whether ``MessagePin.__new__`` works as intended.
    
    Case: no fields given.
    """
    message_pin = MessagePin()
    _assert_fields_set(message_pin)


def test__MessagePin__new__all_fields():
    """
    Tests whether ``MessagePin.__new__`` works as intended.
    
    Case: all fields given.
    """
    message = Message.precreate(202511070010)
    pinned_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    message_pin = MessagePin(
        message = message,
        pinned_at = pinned_at,
    )
    _assert_fields_set(message_pin)
    
    vampytest.assert_is(message_pin.message, message)
    vampytest.assert_eq(message_pin.pinned_at, pinned_at)
