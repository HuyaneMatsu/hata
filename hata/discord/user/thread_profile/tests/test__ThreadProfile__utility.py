from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..flags import ThreadProfileFlag
from ..thread_profile import ThreadProfile

from .test__ThreadProfile__constructor import _assert_fields_set


def test__ThreadProfile__copy():
    """
    Tests whether ``ThreadProfile.copy`` works as intended.
    """
    flags = ThreadProfileFlag(2)
    joined_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    
    
    thread_profile = ThreadProfile(
        flags = flags,
        joined_at = joined_at,
    )
    copy = thread_profile.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_not_is(thread_profile, copy)
    vampytest.assert_eq(thread_profile, copy)


def test__ThreadProfile__copy_with__0():
    """
    Tests whether ``ThreadProfile.copy_with`` works as intended.
    
    Case: No fields given.
    """
    flags = ThreadProfileFlag(2)
    joined_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    
    
    thread_profile = ThreadProfile(
        flags = flags,
        joined_at = joined_at,
    )

    copy = thread_profile.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_not_is(thread_profile, copy)
    vampytest.assert_eq(thread_profile, copy)


def test__ThreadProfile__copy_with__1():
    """
    Tests whether ``ThreadProfile.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_flags = ThreadProfileFlag(2)
    new_flags = ThreadProfileFlag(4)
    old_joined_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    new_joined_at = DateTime(2017, 5, 15, tzinfo = TimeZone.utc)

    
    thread_profile = ThreadProfile(
        flags = old_flags,
        joined_at = old_joined_at,
    )
    copy = thread_profile.copy_with(
        flags = new_flags,
        joined_at = new_joined_at,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_not_is(thread_profile, copy)

    vampytest.assert_eq(copy.flags, new_flags)
    vampytest.assert_eq(copy.joined_at, new_joined_at)


def test__ThreadProfile__created_at():
    """
    Tests whether ``ThreadProfile.created_at`` works as intended.
    
    Case: no roles cached.
    """
    joined_at = DateTime(2020, 5, 14, tzinfo = TimeZone.utc)
    thread_profile = ThreadProfile(joined_at = joined_at)
    vampytest.assert_eq(thread_profile.created_at, joined_at)
