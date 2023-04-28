from datetime import datetime as DateTime

import vampytest

from ..message_call import MessageCall


def test__MessageCall__repr():
    """
    Tests whether ``MessageCall.__repr__`` works as intended.
    """
    ended_at = DateTime(2016, 5, 14)
    user_ids = [202304280006, 202304280007]
    
    message_call = MessageCall(
        ended_at = ended_at,
        user_ids = user_ids,
    )
    
    vampytest.assert_instance(repr(message_call), str)


def test__MessageCall__hash():
    """
    Tests whether ``MessageCall.__hash__`` works as intended.
    """
    ended_at = DateTime(2016, 5, 14)
    user_ids = [202304280008, 202304280009]
    
    message_call = MessageCall(
        ended_at = ended_at,
        user_ids = user_ids,
    )
    
    vampytest.assert_instance(hash(message_call), int)


def test__MessageCall__eq():
    """
    Tests whether ``MessageCall.__eq__`` works as intended.
    """
    ended_at = DateTime(2016, 5, 14)
    user_ids = [202304280010, 202304280011]
    
    keyword_parameters = {
        'ended_at': ended_at,
        'user_ids': user_ids,
    }
    
    message_call = MessageCall(**keyword_parameters)
    
    vampytest.assert_eq(message_call, message_call)
    vampytest.assert_ne(message_call, object())
    
    for field_name, field_value in (
        ('ended_at', DateTime(2016, 5, 15)),
        ('user_ids', [202304280012, 202304280013]),
    ):
        test_message_call = MessageCall(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(message_call, test_message_call)
