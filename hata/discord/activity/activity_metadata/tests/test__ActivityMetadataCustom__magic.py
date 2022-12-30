from datetime import datetime as DateTime

import vampytest

from ....emoji import Emoji

from ..custom import ActivityMetadataCustom


def test__ActivityMetadataCustom__repr():
    """
    Tests whether ``ActivityMetadataCustom.__repr__`` works as intended.
    """
    state = 'state'
    emoji = Emoji.precreate(202209060000, name = 'Code49')
    created_at = DateTime(2014, 9, 16)
    
    keyword_parameters = {
        'created_at': created_at,
        'emoji': emoji,
        'state': state,
    }
    activity_metadata = ActivityMetadataCustom(keyword_parameters)
    
    vampytest.assert_instance(repr(activity_metadata), str)


def test__ActivityMetadataCustom__hash():
    """
    Tests whether ``ActivityMetadataCustom.__hash__`` works as intended.
    """
    state = 'state'
    emoji = Emoji.precreate(202209060001, name = 'Code49')
    created_at = DateTime(2014, 9, 16)
    
    keyword_parameters = {
        'created_at': created_at,
        'emoji': emoji,
        'state': state,
    }
    activity_metadata = ActivityMetadataCustom(keyword_parameters)
    
    vampytest.assert_instance(hash(activity_metadata), int)


def test__ActivityMetadataCustom__eq():
    """
    Tests whether ``ActivityMetadataCustom.__eq__`` works as intended.
    """
    state = 'state'
    emoji = Emoji.precreate(202209060002, name = 'Code49')
    created_at = DateTime(2014, 9, 16)
    
    keyword_parameters = {
        'created_at': created_at,
        'emoji': emoji,
        'state': state,
    }
    activity_metadata = ActivityMetadataCustom(keyword_parameters)
    
    vampytest.assert_eq(activity_metadata, activity_metadata)
    vampytest.assert_ne(activity_metadata, object())
    
    for field_name in (
        'state',
        'emoji',
        'created_at',
    ):
        temporary_activity_metadata = ActivityMetadataCustom({**keyword_parameters, field_name: None})
        vampytest.assert_ne(temporary_activity_metadata, activity_metadata)
