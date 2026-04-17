from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....core import BUILTIN_EMOJIS
from ....emoji import Emoji

from ..hanging import ActivityMetadataHanging
from ..preinstanced import HangType

from .test__ActivityMetadataHanging__constructor import _assert_fields_set


def test__ActivityMetadataHanging__name__no_fields():
    """
    Tests whether ``ActivityMetadataHanging.name`` works as intended.
    
    Case: No fields given.
    """
    activity_metadata = ActivityMetadataHanging()
    
    vampytest.assert_instance(activity_metadata.name, str)


def test__ActivityMetadataHanging__name__all_fields():
    """
    Tests whether ``ActivityMetadataHanging.name`` works as intended.
    
    Case: All fields given.
    """
    created_at = DateTime(2014, 9, 16, tzinfo = TimeZone.utc)
    details = 'details'
    emoji = Emoji.precreate(202408310015, name = 'Code49')
    hang_type = HangType.custom
    
    activity_metadata = ActivityMetadataHanging(
        created_at = created_at,
        details = details,
        emoji = emoji,
        hang_type = hang_type,
    )
    
    vampytest.assert_instance(activity_metadata.name, str)


def test__ActivityMetadataHanging__copy():
    """
    Tests whether ``ActivityMetadataHanging.copy`` works as intended.
    """
    created_at = DateTime(2014, 9, 16, tzinfo = TimeZone.utc)
    details = 'details'
    emoji = BUILTIN_EMOJIS['x']
    hang_type = HangType.custom
    
    activity_metadata = ActivityMetadataHanging(
        created_at = created_at,
        details = details,
        emoji = emoji,
        hang_type = hang_type,
    )
    
    copy = activity_metadata.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, activity_metadata)
    
    vampytest.assert_eq(copy, activity_metadata)


def test__ActivityMetadataHanging__copy_with__no_fields():
    """
    Tests whether ``ActivityMetadataHanging.copy_with`` works as intended.
    
    Case: No fields given.
    """
    created_at = DateTime(2014, 9, 16, tzinfo = TimeZone.utc)
    details = 'details'
    emoji = BUILTIN_EMOJIS['x']
    hang_type = HangType.custom
    
    activity_metadata = ActivityMetadataHanging(
        created_at = created_at,
        details = details,
        emoji = emoji,
        hang_type = hang_type,
    )
    
    copy = activity_metadata.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, activity_metadata)
    
    vampytest.assert_eq(copy, activity_metadata)


def test__ActivityMetadataHanging__copy_with__all_fields():
    """
    Tests whether ``ActivityMetadataHanging.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_created_at = DateTime(2014, 9, 16, tzinfo = TimeZone.utc)
    old_details = 'details'
    old_emoji = BUILTIN_EMOJIS['x']
    old_hang_type = HangType.custom
    
    new_created_at = DateTime(2014, 10, 16, tzinfo = TimeZone.utc)
    new_details = 'seven'
    new_emoji = BUILTIN_EMOJIS['heart']
    new_hang_type = HangType.gaming
    
    activity_metadata = ActivityMetadataHanging(
        created_at = old_created_at,
        details = old_details,
        emoji = old_emoji,
        hang_type = old_hang_type,
    )
    
    copy = activity_metadata.copy_with(
        created_at = new_created_at,
        details = new_details,
        emoji = new_emoji,
        hang_type = new_hang_type,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, activity_metadata)
    
    vampytest.assert_eq(copy.created_at, new_created_at)
    vampytest.assert_eq(copy.details, new_details)
    vampytest.assert_is(copy.emoji, new_emoji)
    vampytest.assert_is(copy.hang_type, new_hang_type)


def test__ActivityMetadataHanging__copy_with_keyword_parameters__no_fields():
    """
    Tests whether ``ActivityMetadataHanging.copy_with_keyword_parameters`` works as intended.
    
    Case: No fields given.
    """
    created_at = DateTime(2014, 9, 16, tzinfo = TimeZone.utc)
    details = 'details'
    emoji = BUILTIN_EMOJIS['x']
    hang_type = HangType.custom
    
    activity_metadata = ActivityMetadataHanging(
        created_at = created_at,
        details = details,
        emoji = emoji,hang_type = hang_type,
    )
    
    keyword_parameters = {}
    copy = activity_metadata.copy_with_keyword_parameters(keyword_parameters)
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, activity_metadata)
    
    vampytest.assert_eq(copy, activity_metadata)


def test__ActivityMetadataHanging__copy_with_keyword_parameters__all_fields_given():
    """
    Tests whether ``ActivityMetadataHanging.copy_with_keyword_parameters`` works as intended.
    
    Case: All fields given.
    """
    old_created_at = DateTime(2014, 9, 16, tzinfo = TimeZone.utc)
    old_details = 'details'
    old_emoji = BUILTIN_EMOJIS['x']
    old_hang_type = HangType.custom
    
    new_created_at = DateTime(2014, 10, 16, tzinfo = TimeZone.utc)
    new_details = 'seven'
    new_emoji = BUILTIN_EMOJIS['heart']
    new_hang_type = HangType.gaming
    
    activity_metadata = ActivityMetadataHanging(
        created_at = old_created_at,
        details = old_details,
        emoji = old_emoji,
        hang_type = old_hang_type,
    )
    
    keyword_parameters = {
        'created_at': new_created_at,
        'details': new_details,
        'emoji': new_emoji,
        'hang_type': new_hang_type,
    }
    copy = activity_metadata.copy_with_keyword_parameters(keyword_parameters)
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, activity_metadata)
    
    vampytest.assert_eq(copy.created_at, new_created_at)
    vampytest.assert_eq(copy.emoji, new_emoji)
    vampytest.assert_eq(copy.details, new_details)
    vampytest.assert_is(copy.hang_type, new_hang_type)
