from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...message import Message

from ..message_pin import MessagePin

from .test__MessagePin__constructor import _assert_fields_set


def test__MessagePin__copy():
    """
    Tests whether ``MessagePin.copy`` works as intended.
    """
    message = Message.precreate(202511070017)
    pinned_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    message_pin = MessagePin(
        message = message,
        pinned_at = pinned_at,
    )
    
    copy = message_pin.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, message_pin)
    vampytest.assert_eq(copy, message_pin)


def test__MessagePin__copy_with__no_fields():
    """
    Tests whether ``MessagePin.copy_with`` works as intended.
    
    Case: No fields given.
    """
    message = Message.precreate(202511070018)
    pinned_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    message_pin = MessagePin(
        message = message,
        pinned_at = pinned_at,
    )
    
    copy = message_pin.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, message_pin)
    vampytest.assert_eq(copy, message_pin)


def test__MessagePin__copy_with__all_fields():
    """
    Tests whether ``MessagePin.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_message = Message.precreate(202511070019)
    old_pinned_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    new_message = Message.precreate(202511070020)
    new_pinned_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    
    message_pin = MessagePin(
        message = old_message,
        pinned_at = old_pinned_at,
    )
    
    copy = message_pin.copy_with(
        message = new_message,
        pinned_at = new_pinned_at,
        
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, message_pin)
    
    vampytest.assert_is(copy.message, new_message)
    vampytest.assert_eq(copy.pinned_at, new_pinned_at)
