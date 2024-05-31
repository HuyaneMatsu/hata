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


def test__MessageCall__copy_with__no_fields():
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


def test__MessageCall__copy_with__all_fields():
    """
    Tests whether ``MessageCall.copy_with`` works as intended.
    
    Case: all fields given.
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


def _iter_options__iter_user_ids():
    user_id_0 = 202304280022
    user_id_1 = 202304280023
    
    yield None, []
    yield [user_id_0], [user_id_0]
    yield [user_id_0, user_id_1], [user_id_0, user_id_1]


@vampytest._(vampytest.call_from(_iter_options__iter_user_ids()).returning_last())
def test__MessageCall__iter_user_ids(input_value):
    """
    Tests whether ``MessageCall.iter_user_ids`` works as intended.
    
    Parameters
    ----------
    user_ids : `None | list<int>`
        User identifiers to create instance with.
    
    Returns
    -------
    output : `list<int>`
    """
    message_call = MessageCall(user_ids = input_value)
    return [*message_call.iter_user_ids()]
