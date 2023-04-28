from datetime import datetime as DateTime

import vampytest

from ..message_call import MessageCall

from .test__MessageCall__constructor import _assert_fields_set


def test__MessageCall__copy():
    """
    Tests whether ``MessageCall.copy`` works as intended.
    """
    ended_at = DateTime(2016, 5, 14)
    user_ids = [202304280014, 202304280015]
    
    message_call = MessageCall(
        ended_at = ended_at,
        user_ids = user_ids,
    )
    copy = message_call.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(message_call, copy)
    
    vampytest.assert_eq(message_call, copy)


def test__MessageCall__copy_with__0():
    """
    Tests whether ``MessageCall.copy_with`` works as intended.
    
    Case: no fields given.
    """
    ended_at = DateTime(2016, 5, 14)
    user_ids = [202304280016, 202304280017]
    
    message_call = MessageCall(
        ended_at = ended_at,
        user_ids = user_ids,
    )
    copy = message_call.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(message_call, copy)
    
    vampytest.assert_eq(message_call, copy)


def test__MessageCall__copy_with__1():
    """
    Tests whether ``MessageCall.copy_with`` works as intended.
    
    Case: all no fields given.
    """
    old_ended_at = DateTime(2016, 5, 14)
    old_user_ids = [202304280018, 202304280019]
    
    new_ended_at = DateTime(2016, 5, 15)
    new_user_ids = [202304280020, 202304280021]
    
    message_call = MessageCall(
        ended_at = old_ended_at,
        user_ids = old_user_ids,
    )
    copy = message_call.copy_with(
        ended_at = new_ended_at,
        user_ids = new_user_ids,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(message_call, copy)
    
    vampytest.assert_eq(copy.ended_at, new_ended_at)
    vampytest.assert_eq(copy.user_ids, tuple(new_user_ids))


def test__MessageCall__iter_user_ids():
    """
    Tests whether ``MessageCall.iter_user_ids`` works as intended.
    """
    for input_value, expected_output in (
        (None, []),
        ([202304280022], [202304280022]),
        ([202304280023, 202304280024], [202304280023, 202304280024])
    ):
        message_call = MessageCall(user_ids = input_value)
        output = [*message_call.iter_user_ids()]
        vampytest.assert_eq(output, expected_output)
