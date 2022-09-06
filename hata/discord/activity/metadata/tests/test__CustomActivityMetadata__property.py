from datetime import datetime as DateTime

import vampytest

from ....emoji import Emoji, create_partial_emoji_data
from ....utils import datetime_to_millisecond_unix_time

from .. import CustomActivityMetadata


def test__CustomActivityMetadata__name__0():
    """
    Tests whether ``CustomActivityMetadata.name`` works as intended.
    
    Case: No fields given.
    """
    activity_metadata = CustomActivityMetadata.from_data({})
    
    vampytest.assert_instance(activity_metadata.name, str)


def test__CustomActivityMetadata__name__1():
    """
    Tests whether ``CustomActivityMetadata.name`` works as intended.
    
    Case: All fields given.
    """
    state = 'state'
    emoji = Emoji.precreate(202209060009, name='Code49')
    created_at = DateTime(2014, 9, 16)
    
    activity_metadata = CustomActivityMetadata.from_data({
        'state': state,
        'emoji': create_partial_emoji_data(emoji),
        'created_at': datetime_to_millisecond_unix_time(created_at),
    })
    
    vampytest.assert_instance(activity_metadata.name, str)
