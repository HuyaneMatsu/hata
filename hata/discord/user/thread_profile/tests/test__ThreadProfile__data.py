from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..flags import ThreadProfileFlag
from ..thread_profile import ThreadProfile

from .test__ThreadProfile__constructor import _check_is_all_fields_set


def test__ThreadProfile__from_data():
    """
    Tests whether ``ThreadProfile.from_data`` works as intended.
    """
    flags = ThreadProfileFlag(2)
    joined_at = DateTime(2016, 5, 15)
    
    data = {
        'flags': int(flags),
        'joined_at': datetime_to_timestamp(joined_at),
    }
    
    thread_profile = ThreadProfile.from_data(data)
    _check_is_all_fields_set(thread_profile)
    
    vampytest.assert_eq(thread_profile.flags, flags)
    vampytest.assert_eq(thread_profile.joined_at, joined_at)


def test__ThreadProfile__to_data():
    """
    Tests whether ``ThreadProfile.to_data`` works as intended.
    """
    flags = ThreadProfileFlag(2)
    joined_at = DateTime(2016, 5, 15)
    
    thread_profile = ThreadProfile(
        flags = flags,
        joined_at = joined_at,
    )
    
    vampytest.assert_eq(
        thread_profile.to_data(
            defaults = True,
            include_internals = True,
        ),
        {
            'flags': int(flags),
            'joined_at': datetime_to_timestamp(joined_at),
        },
    )


def test__ThreadProfile__update_attributes():
    """
    Tests whether ``ThreadProfile._update_attributes`` works as intended.
    """
    flags = ThreadProfileFlag(2)
    
    data = {
        'flags': int(flags),
    }
    
    thread_profile = ThreadProfile()
    thread_profile._update_attributes(data)
    
    vampytest.assert_eq(thread_profile.flags, flags)


def test__ThreadProfile__difference_update_attributes():
    """
    Tests whether ``ThreadProfile._difference_update_attributes`` works as intended.
    """
    old_flags = ThreadProfileFlag(2)
    new_flags = ThreadProfileFlag(4)
    
    data = {
        'flags': int(new_flags),
    }
    
    thread_profile = ThreadProfile(
        flags = old_flags,
    )
    
    old_attributes = thread_profile._difference_update_attributes(data)
    
    vampytest.assert_eq(thread_profile.flags, new_flags)
    
    vampytest.assert_in('flags', old_attributes)
    
    vampytest.assert_eq(old_attributes['flags'], old_flags)
