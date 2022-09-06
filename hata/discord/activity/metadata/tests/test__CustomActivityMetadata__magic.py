from datetime import datetime as DateTime

import vampytest

from ....emoji import Emoji, create_partial_emoji_data
from ....utils import datetime_to_millisecond_unix_time

from .. import CustomActivityMetadata


def test__CustomActivityMetadata__repr():
    """
    Tests whether ``CustomActivityMetadata.__repr__`` works as intended.
    """
    state = 'state'
    emoji = Emoji.precreate(202209060000, name='Code49')
    created_at = DateTime(2014, 9, 16)
    
    activity_metadata = CustomActivityMetadata.from_data({
        'state': state,
        'emoji': create_partial_emoji_data(emoji),
        'created_at': datetime_to_millisecond_unix_time(created_at),
    })
    
    vampytest.assert_instance(repr(activity_metadata), str)


def test__CustomActivityMetadata__hash():
    """
    Tests whether ``CustomActivityMetadata.__hash__`` works as intended.
    """
    state = 'state'
    emoji = Emoji.precreate(202209060001, name='Code49')
    created_at = DateTime(2014, 9, 16)
    
    activity_metadata = CustomActivityMetadata.from_data({
        'state': state,
        'emoji': create_partial_emoji_data(emoji),
        'created_at': datetime_to_millisecond_unix_time(created_at),
    })
    
    vampytest.assert_instance(hash(activity_metadata), int)


def test__CustomActivityMetadata__eq():
    """
    Tests whether ``CustomActivityMetadata.__eq__`` works as intended.
    """
    state = 'state'
    emoji = Emoji.precreate(202209060002, name='Code49')
    created_at = DateTime(2014, 9, 16)
    
    data = {
        'state': state,
        'emoji': create_partial_emoji_data(emoji),
        'created_at': datetime_to_millisecond_unix_time(created_at),
    }
    
    activity_metadata = CustomActivityMetadata.from_data(data)
    
    vampytest.assert_eq(activity_metadata, activity_metadata)
    vampytest.assert_ne(activity_metadata, object())
    
    for field_name in (
        'state',
        'emoji',
        'created_at',
    ):
        temporary_activity_metadata = CustomActivityMetadata.from_data({**data, field_name: None})
        vampytest.assert_ne(temporary_activity_metadata, activity_metadata)
