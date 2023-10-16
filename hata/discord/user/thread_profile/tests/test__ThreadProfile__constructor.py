from datetime import datetime as DateTime

import vampytest

from ..flags import ThreadProfileFlag
from ..thread_profile import ThreadProfile


def _check_is_all_fields_set(thread_profile):
    """
    Asserts whether all fields of the given thread profiles are set.
    
    Parameters
    ----------
    thread_profile : ``ThreadProfile``
    """
    vampytest.assert_instance(thread_profile, ThreadProfile)
    vampytest.assert_instance(thread_profile.flags, ThreadProfileFlag)
    vampytest.assert_instance(thread_profile.joined_at, DateTime, nullable = True)


def test__ThreadProfile__new__0():
    """
    Tests whether ``ThreadProfile.__new__`` works as intended.
    
    Case: No parameters.
    """
    thread_profile = ThreadProfile()
    _check_is_all_fields_set(thread_profile)



def test__ThreadProfile__new__1():
    """
    Tests whether ``ThreadProfile.__new__`` works as intended.
    
    Case: all fields.
    """
    flags = ThreadProfileFlag(24)
    joined_at = DateTime(2016, 5, 15)
    
    thread_profile = ThreadProfile(
        flags = flags,
        joined_at = joined_at,
    )
    _check_is_all_fields_set(thread_profile)
    
    vampytest.assert_eq(thread_profile.flags, flags)
    vampytest.assert_eq(thread_profile.joined_at, joined_at)
