from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....emoji import Emoji, create_partial_emoji_data
from ....utils import datetime_to_millisecond_unix_time

from ..custom import ActivityMetadataCustom

from .test__ActivityMetadataCustom__constructor import _assert_fields_set


def test__ActivityMetadataCustom__from_data__1():
    """
    Tests whether ``ActivityMetadataCustom.from_data`` works as intended.
    
    Case: All fields given.
    """
    state = 'state'
    emoji = Emoji.precreate(202209060003, name = 'Code49')
    created_at = DateTime(2014, 9, 16, tzinfo = TimeZone.utc)
    
    data = {
        'state': state,
        'emoji': create_partial_emoji_data(emoji),
        'created_at': datetime_to_millisecond_unix_time(created_at),
    }
    
    activity_metadata = ActivityMetadataCustom.from_data(data)
    _assert_fields_set(activity_metadata)
    
    vampytest.assert_eq(activity_metadata.state, state)
    vampytest.assert_is(activity_metadata.emoji, emoji)
    vampytest.assert_eq(activity_metadata.created_at, created_at)


def test__ActivityMetadataCustom__to_data():
    """
    Tests whether ``ActivityMetadataCustom.to_data`` works as intended.
    """
    state = 'state'
    emoji = Emoji.precreate(202209060004, name = 'Code49')
    created_at = DateTime(2014, 9, 16, tzinfo = TimeZone.utc)
    
    activity_metadata = ActivityMetadataCustom(
        created_at = created_at,
        emoji = emoji,
        state = state,
    )
    
    expected_output = {
        'state': state,
    }
    
    vampytest.assert_eq(
        activity_metadata.to_data(),
        expected_output,
    )


def test__ActivityMetadataCustom__to_data__user():
    """
    Tests whether `ActivityMetadataCustom.to_data(user = True)` works as intended.
    """
    state = 'state'
    emoji = Emoji.precreate(202209060005, name = 'Code49')
    created_at = DateTime(2014, 9, 16, tzinfo = TimeZone.utc)
    
    activity_metadata = ActivityMetadataCustom(
        created_at = created_at,
        emoji = emoji,
        state = state,
    )
    
    expected_output = {}
    
    vampytest.assert_eq(
        activity_metadata.to_data(defaults = True, user = True),
        expected_output,
    )


def test__ActivityMetadataCustom__to_data__include_internals():
    """
    Tests whether `ActivityMetadataCustom.to_data(include_internals = True)` works as intended.
    """
    state = 'state'
    emoji = Emoji.precreate(202209060006, name = 'Code49')
    created_at = DateTime(2014, 9, 16, tzinfo = TimeZone.utc)
    
    activity_metadata = ActivityMetadataCustom(
        created_at = created_at,
        emoji = emoji,
        state = state,
    )
    
    expected_output = {
        'name': 'Custom Status',
        'state': state,
        'emoji': create_partial_emoji_data(emoji),
        'created_at': datetime_to_millisecond_unix_time(created_at),
    }
    
    vampytest.assert_eq(
        activity_metadata.to_data(defaults = True, include_internals = True),
        expected_output,
    )


def test__ActivityMetadataCustom__update_attributes():
    """
    Tests whether ``ActivityMetadataCustom._update_attributes`` works as intended.
    """
    old_state = 'state'
    new_state = 'remilia'
    old_emoji = Emoji.precreate(202209060007, name = 'Code49')
    new_emoji = Emoji.precreate(202209060008, name = 'Howling')
    old_created_at = DateTime(2014, 9, 16, tzinfo = TimeZone.utc)
    new_created_at = DateTime(2014, 9, 17, tzinfo = TimeZone.utc)
    
    activity_metadata = ActivityMetadataCustom(
        created_at = old_created_at,
        emoji = old_emoji,
        state = old_state,
    )
    
    activity_metadata._update_attributes({
        'state': new_state,
        'emoji': create_partial_emoji_data(new_emoji),
        'created_at': datetime_to_millisecond_unix_time(new_created_at),
    })

    vampytest.assert_eq(activity_metadata.state, new_state)
    vampytest.assert_is(activity_metadata.emoji, new_emoji)
    vampytest.assert_eq(activity_metadata.created_at, new_created_at)


def test__ActivityMetadataCustom__difference_update_attributes():
    """
    Tests whether ``ActivityMetadataCustom._difference_update_attributes`` works as intended.
    """
    old_state = 'state'
    new_state = 'remilia'
    old_emoji = Emoji.precreate(202209060007, name = 'Code49')
    new_emoji = Emoji.precreate(202209060008, name = 'Howling')
    old_created_at = DateTime(2014, 9, 16, tzinfo = TimeZone.utc)
    new_created_at = DateTime(2014, 9, 17, tzinfo = TimeZone.utc)
    
    activity_metadata = ActivityMetadataCustom(
        created_at = old_created_at,
        emoji = old_emoji,
        state = old_state,
    )
    
    old_attributes = activity_metadata._difference_update_attributes({
        'state': new_state,
        'emoji': create_partial_emoji_data(new_emoji),
        'created_at': datetime_to_millisecond_unix_time(new_created_at),
    })

    vampytest.assert_eq(activity_metadata.state, new_state)
    vampytest.assert_is(activity_metadata.emoji, new_emoji)
    vampytest.assert_eq(activity_metadata.created_at, new_created_at)
    
    vampytest.assert_eq(
        old_attributes,
        {
            'state': old_state,
            'emoji': old_emoji,
            'created_at': old_created_at,
        }
    )
