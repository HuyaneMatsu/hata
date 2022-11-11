import vampytest

from ....user import User

from ..private import ChannelMetadataPrivate

from .test__ChannelMetadataPrivate__constructor import assert_fields_set


def test__ChannelMetadataPrivate__from_data():
    """
    Tests whether ``ChannelMetadataPrivate.from_data` works as intended.
    """
    user_1 = User.precreate(202209160002)
    
    channel_metadata = ChannelMetadataPrivate.from_data({
        'recipients': [user_1.to_data()],
    })
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataPrivate)
    assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.users, [user_1])


def test__ChannelMetadataPrivate__to_data():
    """
    Tests whether ``ChannelMetadataPrivate.to_data`` works as intended.
    
    Case: include defaults and internals.
    """
    user_1 = User.precreate(202209160003)
    
    channel_metadata = ChannelMetadataPrivate({
        'users': [user_1],
    })
    
    data = channel_metadata.to_data(defaults = True, include_internals = True)
    
    vampytest.assert_eq(
        data,
        {
            'recipients': [user_1.to_data()],
        },
    )


def test__ChannelMetadataPrivate__update_attributes():
    """
    Tests whether ``ChannelMetadataPrivate._update_attributes`` works as intended.
    """
    channel_metadata = ChannelMetadataPrivate({})
    
    channel_metadata._update_attributes({})


def test__ChannelMetadataPrivate__difference_update_attributes():
    """
    Tests whether ``ChannelMetadataPrivate._difference_update_attributes`` works as intended.
    """
    channel_metadata = ChannelMetadataPrivate({})
    
    old_attributes = channel_metadata._difference_update_attributes({})


def test__ChannelMetadataPrivate__from_partial_data():
    """
    Tests whether ``ChannelMetadataPrivate._from_partial_data`` works as intended.
    """
    channel_metadata = ChannelMetadataPrivate._from_partial_data({})
    assert_fields_set(channel_metadata)

    vampytest.assert_instance(channel_metadata.users, list)
