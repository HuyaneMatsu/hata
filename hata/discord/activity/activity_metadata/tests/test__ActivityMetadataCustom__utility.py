from datetime import datetime as DateTime

import vampytest

from ....core import BUILTIN_EMOJIS
from ....emoji import Emoji

from ..custom import ActivityMetadataCustom

from .test__ActivityMetadataCustom__constructor import _assert_fields_set


def test__ActivityMetadataCustom__name__0():
    """
    Tests whether ``ActivityMetadataCustom.name`` works as intended.
    
    Case: No fields given.
    """
    keyword_parameters = {}
    activity_metadata = ActivityMetadataCustom(keyword_parameters)
    
    vampytest.assert_instance(activity_metadata.name, str)


def test__ActivityMetadataCustom__name__1():
    """
    Tests whether ``ActivityMetadataCustom.name`` works as intended.
    
    Case: All fields given.
    """
    state = 'state'
    emoji = Emoji.precreate(202209060009, name = 'Code49')
    created_at = DateTime(2014, 9, 16)
    
    keyword_parameters = {
        'created_at': created_at,
        'emoji': emoji,
        'state': state,
    }
    activity_metadata = ActivityMetadataCustom(keyword_parameters)
    
    vampytest.assert_instance(activity_metadata.name, str)


def test__ActivityMetadataCustom__copy():
    """
    Tests whether ``ActivityMetadataCustom.copy`` works as intended.
    """
    state = 'state'
    emoji = BUILTIN_EMOJIS['x']
    created_at = DateTime(2014, 9, 16)
    
    keyword_parameters = {
        'created_at': created_at,
        'emoji': emoji,
        'state': state,
    }
    activity_metadata = ActivityMetadataCustom(keyword_parameters)
    
    copy = activity_metadata.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, activity_metadata)
    
    vampytest.assert_eq(copy, activity_metadata)


def test__ActivityMetadataCustom__copy_with__0():
    """
    Tests whether ``ActivityMetadataCustom.copy_with`` works as intended.
    
    Case: No fields given.
    """
    state = 'state'
    emoji = BUILTIN_EMOJIS['x']
    created_at = DateTime(2014, 9, 16)
    
    keyword_parameters = {
        'created_at': created_at,
        'emoji': emoji,
        'state': state,
    }
    activity_metadata = ActivityMetadataCustom(keyword_parameters)
    
    keyword_parameters = {}
    copy = activity_metadata.copy_with(keyword_parameters)
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, activity_metadata)
    
    vampytest.assert_eq(copy, activity_metadata)


def test__ActivityMetadataCustom__copy_with__1():
    """
    Tests whether ``ActivityMetadataCustom.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_state = 'state'
    old_emoji = BUILTIN_EMOJIS['x']
    old_created_at = DateTime(2014, 9, 16)
    new_state = 'seven'
    new_emoji = BUILTIN_EMOJIS['heart']
    new_created_at = DateTime(2014, 10, 16)
    
    keyword_parameters = {
        'created_at': old_created_at,
        'emoji': old_emoji,
        'state': old_state,
    }
    activity_metadata = ActivityMetadataCustom(keyword_parameters)
    
    keyword_parameters = {
        'created_at': new_created_at,
        'emoji': new_emoji,
        'state': new_state,
    }
    copy = activity_metadata.copy_with(keyword_parameters)
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, activity_metadata)
    
    vampytest.assert_eq(copy.created_at, new_created_at)
    vampytest.assert_eq(copy.emoji, new_emoji)
    vampytest.assert_eq(copy.state, new_state)
