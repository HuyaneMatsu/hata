from datetime import datetime as DateTime

import vampytest

from ....emoji import Emoji, create_partial_emoji_data
from ....utils import datetime_to_millisecond_unix_time

from .. import ActivityMetadataCustom


def test__ActivityMetadataCustom__from_data__0():
    """
    Tests whether ``ActivityMetadataCustom.from_data`` works as intended.
    
    Case: No fields given.
    """
    activity_metadata = ActivityMetadataCustom.from_data({})
    
    vampytest.assert_instance(activity_metadata, ActivityMetadataCustom)
    vampytest.assert_is(activity_metadata.state, None)
    vampytest.assert_is(activity_metadata.emoji, None)
    vampytest.assert_is(activity_metadata.created_at, None)


def test__ActivityMetadataCustom__from_data__1():
    """
    Tests whether ``ActivityMetadataCustom.from_data`` works as intended.
    
    Case: All fields given.
    """
    state = 'state'
    emoji = Emoji.precreate(202209060003, name='Code49')
    created_at = DateTime(2014, 9, 16)
    
    activity_metadata = ActivityMetadataCustom.from_data({
        'state': state,
        'emoji': create_partial_emoji_data(emoji),
        'created_at': datetime_to_millisecond_unix_time(created_at),
    })
    
    vampytest.assert_instance(activity_metadata, ActivityMetadataCustom)
    vampytest.assert_eq(activity_metadata.state, state)
    vampytest.assert_is(activity_metadata.emoji, emoji)
    vampytest.assert_eq(activity_metadata.created_at, created_at)


def test__ActivityMetadataCustom__to_data():
    """
    Tests whether ``ActivityMetadataCustom.to_data`` works as intended.
    """
    state = 'state'
    emoji = Emoji.precreate(202209060004, name='Code49')
    created_at = DateTime(2014, 9, 16)
    
    activity_metadata = ActivityMetadataCustom.from_data({
        'state': state,
        'emoji': create_partial_emoji_data(emoji),
        'created_at': datetime_to_millisecond_unix_time(created_at),
    })
    
    vampytest.assert_eq(activity_metadata.to_data(), {})


def test__ActivityMetadataCustom__to_data_user():
    """
    Tests whether ``ActivityMetadataCustom.to_data_user`` works as intended.
    """
    state = 'state'
    emoji = Emoji.precreate(202209060005, name='Code49')
    created_at = DateTime(2014, 9, 16)
    
    activity_metadata = ActivityMetadataCustom.from_data({
        'state': state,
        'emoji': create_partial_emoji_data(emoji),
        'created_at': datetime_to_millisecond_unix_time(created_at),
    })
    
    vampytest.assert_eq(activity_metadata.to_data(), {})


def test__ActivityMetadataCustom__to_data_full():
    """
    Tests whether ``ActivityMetadataCustom.to_data_full`` works as intended.
    """
    state = 'state'
    emoji = Emoji.precreate(202209060006, name='Code49')
    created_at = DateTime(2014, 9, 16)
    
    activity_metadata = ActivityMetadataCustom.from_data({
        'state': state,
        'emoji': create_partial_emoji_data(emoji),
        'created_at': datetime_to_millisecond_unix_time(created_at),
    })
    
    data = activity_metadata.to_data_full()
    
    vampytest.assert_in('state', data)
    vampytest.assert_in('emoji', data)
    vampytest.assert_in('created_at', data)
    
    vampytest.assert_eq(data['state'], state)
    vampytest.assert_eq(data['emoji'], create_partial_emoji_data(emoji))
    vampytest.assert_eq(data['created_at'], datetime_to_millisecond_unix_time(created_at))


def test__ActivityMetadataCustom__update_attributes():
    """
    Tests whether ``ActivityMetadataCustom._update_attributes`` works as intended.
    """
    old_state = 'state'
    new_state = 'remilia'
    old_emoji = Emoji.precreate(202209060007, name='Code49')
    new_emoji = Emoji.precreate(202209060008, name='Howling')
    old_created_at = DateTime(2014, 9, 16)
    new_created_at = DateTime(2014, 9, 17)
    
    activity_metadata = ActivityMetadataCustom.from_data({
        'state': old_state,
        'emoji': create_partial_emoji_data(old_emoji),
        'created_at': datetime_to_millisecond_unix_time(old_created_at),
    })
    
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
    old_emoji = Emoji.precreate(202209060007, name='Code49')
    new_emoji = Emoji.precreate(202209060008, name='Howling')
    old_created_at = DateTime(2014, 9, 16)
    new_created_at = DateTime(2014, 9, 17)
    
    activity_metadata = ActivityMetadataCustom.from_data({
        'state': old_state,
        'emoji': create_partial_emoji_data(old_emoji),
        'created_at': datetime_to_millisecond_unix_time(old_created_at),
    })
    
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
