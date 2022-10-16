import vampytest

from .....user import User

from ..private_base import ChannelMetadataPrivateBase

from .test__ChannelMetadataPrivateBase__constructor import assert_fields_set


def test__ChannelMetadataPrivateBase__from_data():
    """
    Tests whether ``ChannelMetadataPrivateBase.from_data` works as intended.
    """
    user_1 = User.precreate(202209150010)
    
    channel_metadata = ChannelMetadataPrivateBase.from_data({
        'recipients': [user_1.to_data()],
    })
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataPrivateBase)
    assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.users, [user_1])


def test__ChannelMetadataPrivateBase__to_data():
    """
    Tests whether ``ChannelMetadataPrivateBase.to_data`` works as intended.
    
    Case: include defaults and internals.
    """
    user_1 = User.precreate(202209150011)
    
    channel_metadata = ChannelMetadataPrivateBase({
        'users': [user_1],
    })
    
    data = channel_metadata.to_data(defaults = True, include_internals = True)
    
    vampytest.assert_eq(
        data,
        {
            'recipients': [user_1.to_data()],
        },
    )


def test__ChannelMetadataPrivateBase__update_attributes():
    """
    Tests whether ``ChannelMetadataPrivateBase._update_attributes`` works as intended.
    """
    channel_metadata = ChannelMetadataPrivateBase({})
    
    channel_metadata._update_attributes({})


def test__ChannelMetadataPrivateBase__difference_update_attributes():
    """
    Tests whether ``ChannelMetadataPrivateBase._difference_update_attributes`` works as intended.
    """
    channel_metadata = ChannelMetadataPrivateBase({})
    
    old_attributes = channel_metadata._difference_update_attributes({})


def test__ChannelMetadataPrivateBase__from_partial_data():
    """
    Tests whether ``ChannelMetadataPrivateBase._from_partial_data`` works as intended.
    """
    channel_metadata = ChannelMetadataPrivateBase._from_partial_data({})
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataPrivateBase)
    assert_fields_set(channel_metadata)
    
    vampytest.assert_instance(channel_metadata.users, list)
