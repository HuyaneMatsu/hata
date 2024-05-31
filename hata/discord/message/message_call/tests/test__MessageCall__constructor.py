from datetime import datetime as DateTime

import vampytest

from ..message_call import MessageCall


def _assert_fields_set(message_call):
    """
    Tests whether all attributes are set of the given message call.
    
    Parameters
    ----------
    message_call : ``MessageCall``
        The message call to check.
    """
    vampytest.assert_instance(message_call, MessageCall)
    vampytest.assert_instance(message_call.ended_at, DateTime, nullable = True)
    vampytest.assert_instance(message_call.user_ids, tuple, nullable = True)


def test__MessageCall__new__all_fields():
    """
    Tests whether ``MessageCall.__new__`` works as intended.
    
    Case: No fields given.
    """
    message_call = MessageCall()
    _assert_fields_set(message_call)


def test__MessageCall__new__no_fields():
    """
    Tests whether ``MessageCall.__new__`` works as intended.
    
    Case: All fields given.
    """
    ended_at = DateTime(2016, 5, 14)
    user_ids = [202304280000, 202304280001]

    message_call = MessageCall(
        ended_at = ended_at,
        user_ids = user_ids,
    )
    _assert_fields_set(message_call)
    
    vampytest.assert_eq(message_call.ended_at, ended_at)
    vampytest.assert_eq(message_call.user_ids, tuple(user_ids))
