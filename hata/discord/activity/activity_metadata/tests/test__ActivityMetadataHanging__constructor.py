from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....core import BUILTIN_EMOJIS
from ....emoji import Emoji

from ..hanging import ActivityMetadataHanging
from ..preinstanced import HangType


def _assert_fields_set(activity_metadata):
    """
    Asserts whether the given hanging activity metadata's fields are all set correctly.
    
    Parameters
    ----------
    activity_metadata : ``ActivityMetadataHanging``
        The activity metadata to check.
    """
    vampytest.assert_instance(activity_metadata, ActivityMetadataHanging)
    vampytest.assert_instance(activity_metadata.created_at, DateTime, nullable = True)
    vampytest.assert_instance(activity_metadata.details, str, nullable = True)
    vampytest.assert_instance(activity_metadata.emoji, Emoji, nullable = True)
    vampytest.assert_instance(activity_metadata.hang_type, HangType)


def test__ActivityMetadataHanging__new__no_fields():
    """
    Tests whether ``ActivityMetadataHanging.__new__`` works as intended.
    
    Case: No fields given.
    """
    activity_metadata = ActivityMetadataHanging()
    _assert_fields_set(activity_metadata)


def test__ActivityMetadataHanging__new__all_fields():
    """
    Tests whether ``ActivityMetadataHanging.__new__`` works as intended.
    
    Case: All fields given.
    """
    created_at = DateTime(2016, 5, 4, tzinfo = TimeZone.utc)
    details = 'bloody'
    emoji = BUILTIN_EMOJIS['x']
    hang_type = HangType.custom
    
    activity_metadata = ActivityMetadataHanging(
        created_at = created_at,
        details = details,
        emoji = emoji,
        hang_type = hang_type,
    )
    _assert_fields_set(activity_metadata)
    
    vampytest.assert_eq(activity_metadata.created_at, created_at)
    vampytest.assert_eq(activity_metadata.details, details)
    vampytest.assert_is(activity_metadata.emoji, emoji)
    vampytest.assert_is(activity_metadata.hang_type, hang_type)


def test__ActivityMetadataHanging__from_keyword_parameters__no_fields_given():
    """
    Tests whether ``ActivityMetadataHanging.from_keyword_parameters`` works as intended.
    
    Case: No fields given.
    """
    keyword_parameters = {}
    activity_metadata = ActivityMetadataHanging.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(activity_metadata)
    vampytest.assert_eq(keyword_parameters, {})


def test__ActivityMetadataHanging__from_keyword_parameters__all_fields_given():
    """
    Tests whether ``ActivityMetadataHanging.from_keyword_parameters`` works as intended.
    
    Case: All fields given.
    """
    created_at = DateTime(2016, 5, 4, tzinfo = TimeZone.utc)
    details = 'bloody'
    emoji = BUILTIN_EMOJIS['x']
    hang_type = HangType.custom
    
    keyword_parameters = {
        'created_at': created_at,
        'details': details,
        'emoji': emoji,
        'hang_type': hang_type,
    }
    activity_metadata = ActivityMetadataHanging.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(activity_metadata)
    vampytest.assert_eq(keyword_parameters, {})
    
    vampytest.assert_eq(activity_metadata.created_at, created_at)
    vampytest.assert_eq(activity_metadata.details, details)
    vampytest.assert_is(activity_metadata.emoji, emoji)
    vampytest.assert_is(activity_metadata.hang_type, hang_type)


@vampytest.call_with(None)
@vampytest.call_with('')
def test__ActivityMetadataHanging__from_keyword_parameters__pop_empty_name(name):
    """
    Tests whether ``ActivityMetadataHanging.from_keyword_parameters`` works as intended.
    
    Case: Should pop empty name.
    
    Parameters
    ----------
    name : `None | str`
        Value to use.
    """
    keyword_parameters = {'name': name}
    activity_metadata = ActivityMetadataHanging.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(activity_metadata)
    vampytest.assert_eq(keyword_parameters, {})
