from datetime import datetime as DateTime

import vampytest

from ..flags import ThreadProfileFlag
from ..thread_profile import ThreadProfile


def test__ThreadProfile__repr():
    """
    Tests whether ``ThreadProfile.__repr__`` works as intended.
    """
    flags = ThreadProfileFlag(2)
    joined_at = DateTime(2016, 5, 15)
    
    
    thread_profile = ThreadProfile(
        flags = flags,
        joined_at = joined_at,
    )
    
    vampytest.assert_instance(repr(thread_profile), str)


def test__ThreadProfile__hash():
    """
    Tests whether ``ThreadProfile.__hash__`` works as intended.
    """
    flags = ThreadProfileFlag(2)
    joined_at = DateTime(2016, 5, 15)
    

    thread_profile = ThreadProfile(
        flags = flags,
        joined_at = joined_at,
    )
    
    vampytest.assert_instance(hash(thread_profile), int)


def test__ThreadProfile__eq():
    """
    Tests whether ``ThreadProfile.__eq__`` works as intended.
    """
    flags = ThreadProfileFlag(2)
    joined_at = DateTime(2016, 5, 15)

    
    keyword_parameters = {
        'flags': flags,
        'joined_at': joined_at,
    }
    
    thread_profile = ThreadProfile(**keyword_parameters)
    
    vampytest.assert_eq(thread_profile, thread_profile)
    vampytest.assert_ne(thread_profile, object())
    
    for field_name, field_value in (
        ('flags', ThreadProfileFlag(4)),
        ('joined_at', None),
    ):
        test_thread_profile = ThreadProfile(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(thread_profile, test_thread_profile)
