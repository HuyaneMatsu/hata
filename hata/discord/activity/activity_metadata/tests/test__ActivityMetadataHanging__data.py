from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....emoji import Emoji, create_partial_emoji_data
from ....utils import datetime_to_millisecond_unix_time

from ..hanging import ActivityMetadataHanging
from ..preinstanced import HangType

from .test__ActivityMetadataHanging__constructor import _assert_fields_set


def test__ActivityMetadataHanging__from_data():
    """
    Tests whether ``ActivityMetadataHanging.from_data`` works as intended.
    
    Case: All fields given.
    """
    created_at = DateTime(2014, 9, 16, tzinfo = TimeZone.utc)
    details = 'details'
    emoji = Emoji.precreate(202408310005, name = 'Code49')
    hang_type = HangType.custom
    
    data = {
        'created_at': datetime_to_millisecond_unix_time(created_at),
        'details': details,
        'emoji': create_partial_emoji_data(emoji),
        'state': hang_type.value,
    }
    
    activity_metadata = ActivityMetadataHanging.from_data(data)
    _assert_fields_set(activity_metadata)
    
    vampytest.assert_eq(activity_metadata.created_at, created_at)
    vampytest.assert_eq(activity_metadata.details, details)
    vampytest.assert_is(activity_metadata.emoji, emoji)
    vampytest.assert_is(activity_metadata.hang_type, hang_type)


def test__ActivityMetadataHanging__to_data():
    """
    Tests whether ``ActivityMetadataHanging.to_data`` works as intended.
    """
    created_at = DateTime(2014, 9, 16, tzinfo = TimeZone.utc)
    details = 'details'
    emoji = Emoji.precreate(202408310006, name = 'Code49')
    hang_type = HangType.custom
    
    activity_metadata = ActivityMetadataHanging(
        created_at = created_at,
        details = details,
        emoji = emoji,
        hang_type = hang_type,
    )
    
    expected_output = {
        'state': hang_type.value,
    }
    
    vampytest.assert_eq(
        activity_metadata.to_data(),
        expected_output,
    )


def test__ActivityMetadataHanging__to_data__user():
    """
    Tests whether `ActivityMetadataHanging.to_data(user = True)` works as intended.
    """
    created_at = DateTime(2014, 9, 16, tzinfo = TimeZone.utc)
    details = 'details'
    emoji = Emoji.precreate(202408310007, name = 'Code49')
    hang_type = HangType.custom
    
    activity_metadata = ActivityMetadataHanging(
        created_at = created_at,
        details = details,
        emoji = emoji,
        hang_type = hang_type,
    )
    
    expected_output = {
        'details': details,
        'emoji': create_partial_emoji_data(emoji),
        'state': hang_type.value,
    }
    
    vampytest.assert_eq(
        activity_metadata.to_data(defaults = True, user = True),
        expected_output,
    )


def test__ActivityMetadataHanging__to_data__include_internals():
    """
    Tests whether `ActivityMetadataHanging.to_data(include_internals = True)` works as intended.
    """
    created_at = DateTime(2014, 9, 16, tzinfo = TimeZone.utc)
    details = 'details'
    emoji = Emoji.precreate(202408310008, name = 'Code49')
    hang_type = HangType.custom
    
    activity_metadata = ActivityMetadataHanging(
        created_at = created_at,
        details = details,
        emoji = emoji,
        hang_type = hang_type,
    )
    
    expected_output = {
        'created_at': datetime_to_millisecond_unix_time(created_at),
        'details': details,
        'emoji': create_partial_emoji_data(emoji),
        'name': 'Hang Status',
        'state': hang_type.value,
    }
    
    vampytest.assert_eq(
        activity_metadata.to_data(defaults = True, include_internals = True),
        expected_output,
    )


def test__ActivityMetadataHanging__update_attributes():
    """
    Tests whether ``ActivityMetadataHanging._update_attributes`` works as intended.
    """
    old_created_at = DateTime(2014, 9, 16, tzinfo = TimeZone.utc)
    old_details = 'details'
    old_emoji = Emoji.precreate(202408310009, name = 'Code49')
    old_hang_type = HangType.custom
    
    new_created_at = DateTime(2014, 9, 17, tzinfo = TimeZone.utc)
    new_details = 'remilia'
    new_emoji = Emoji.precreate(2024083100010, name = 'Howling')
    new_hang_type = HangType.gaming
    
    activity_metadata = ActivityMetadataHanging(
        created_at = old_created_at,
        details = old_details,
        emoji = old_emoji,
        hang_type = old_hang_type,
    )
    
    activity_metadata._update_attributes({
        'created_at': datetime_to_millisecond_unix_time(new_created_at),
        'details': new_details,
        'emoji': create_partial_emoji_data(new_emoji),
        'state': new_hang_type.value,
    })
    
    vampytest.assert_eq(activity_metadata.created_at, new_created_at)
    vampytest.assert_eq(activity_metadata.details, new_details)
    vampytest.assert_is(activity_metadata.emoji, new_emoji)
    vampytest.assert_is(activity_metadata.hang_type, new_hang_type)


def test__ActivityMetadataHanging__difference_update_attributes():
    """
    Tests whether ``ActivityMetadataHanging._difference_update_attributes`` works as intended.
    """
    old_created_at = DateTime(2014, 9, 16, tzinfo = TimeZone.utc)
    old_details = 'details'
    old_emoji = Emoji.precreate(202408310011, name = 'Code49')
    old_hang_type = HangType.custom
    
    new_created_at = DateTime(2014, 9, 17, tzinfo = TimeZone.utc)
    new_details = 'remilia'
    new_emoji = Emoji.precreate(202408310012, name = 'Howling')
    new_hang_type = HangType.gaming
    
    activity_metadata = ActivityMetadataHanging(
        created_at = old_created_at,
        details = old_details,
        emoji = old_emoji,
        hang_type = old_hang_type,
    )
    
    old_attributes = activity_metadata._difference_update_attributes({
        'emoji': create_partial_emoji_data(new_emoji),
        'details': new_details,
        'created_at': datetime_to_millisecond_unix_time(new_created_at),
        'state': new_hang_type.value,
    })

    vampytest.assert_eq(activity_metadata.created_at, new_created_at)
    vampytest.assert_eq(activity_metadata.details, new_details)
    vampytest.assert_is(activity_metadata.emoji, new_emoji)
    
    vampytest.assert_eq(
        old_attributes,
        {
            'created_at': old_created_at,
            'details': old_details,
            'emoji': old_emoji,
            'hang_type': old_hang_type,
        }
    )
