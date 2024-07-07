from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....core import BUILTIN_EMOJIS
from ....emoji import Emoji

from ..custom import ActivityMetadataCustom


def _assert_fields_set(activity_metadata):
    """
    Asserts whether the given custom activity metadata's fields are all set correctly.
    
    Parameters
    ----------
    activity_metadata : ``ActivityMetadataCustom``
        The activity metadata to check.
    """
    vampytest.assert_instance(activity_metadata, ActivityMetadataCustom)
    vampytest.assert_instance(activity_metadata.created_at, DateTime, nullable = True)
    vampytest.assert_instance(activity_metadata.emoji, Emoji, nullable = True)
    vampytest.assert_instance(activity_metadata.state, str, nullable = True)


def test__ActivityMetadataCustom__new__0():
    """
    Tests whether ``ActivityMetadataCustom.__new__`` works as intended.
    
    Case: No fields given.
    """
    activity_metadata = ActivityMetadataCustom()
    _assert_fields_set(activity_metadata)


def test__ActivityMetadataCustom__new__1():
    """
    Tests whether ``ActivityMetadataCustom.__new__`` works as intended.
    
    Case: All fields given.
    """
    created_at = DateTime(2016, 5, 4, tzinfo = TimeZone.utc)
    emoji = BUILTIN_EMOJIS['x']
    state = 'bloody'
    
    activity_metadata = ActivityMetadataCustom(
        created_at = created_at,
        emoji = emoji,
        state = state,
    )
    _assert_fields_set(activity_metadata)
    
    vampytest.assert_eq(activity_metadata.created_at, created_at)
    vampytest.assert_eq(activity_metadata.emoji, emoji)
    vampytest.assert_eq(activity_metadata.state, state)


def test__ActivityMetadataCustom__from_keyword_parameters__0():
    """
    Tests whether ``ActivityMetadataCustom.from_keyword_parameters`` works as intended.
    
    Case: No fields given.
    """
    keyword_parameters = {}
    activity_metadata = ActivityMetadataCustom.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(activity_metadata)
    vampytest.assert_eq(keyword_parameters, {})


def test__ActivityMetadataCustom__from_keyword_parameters__1():
    """
    Tests whether ``ActivityMetadataCustom.from_keyword_parameters`` works as intended.
    
    Case: All fields given.
    """
    created_at = DateTime(2016, 5, 4, tzinfo = TimeZone.utc)
    emoji = BUILTIN_EMOJIS['x']
    state = 'bloody'
    
    keyword_parameters = {
        'created_at': created_at,
        'emoji': emoji,
        'state': state,
    }
    activity_metadata = ActivityMetadataCustom.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(activity_metadata)
    vampytest.assert_eq(keyword_parameters, {})
    
    vampytest.assert_eq(activity_metadata.created_at, created_at)
    vampytest.assert_eq(activity_metadata.emoji, emoji)
    vampytest.assert_eq(activity_metadata.state, state)


def test__ActivityMetadataCustom__from_keyword_parameters__2():
    """
    Tests whether ``ActivityMetadataCustom.from_keyword_parameters`` works as intended.
    
    Case: Should pop empty name.
    """
    for keyword_parameters in ({'name': None}, {'name': ''}):
        activity_metadata = ActivityMetadataCustom.from_keyword_parameters(keyword_parameters)
        _assert_fields_set(activity_metadata)
        vampytest.assert_eq(keyword_parameters, {})
