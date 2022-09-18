import vampytest

from ....user import User

from .. import ChannelMetadataPrivateBase


def test__ChannelMetadataPrivateBase__repr():
    """
    Tests whether ``.ChannelMetadataPrivateBase.__repr__`` works as intended.
    """
    users = [User.precreate(202209150007)]
    
    channel_metadata = ChannelMetadataPrivateBase({
        'users': users
    })
    
    vampytest.assert_instance(repr(channel_metadata), str)



def test__ChannelMetadataPrivateBase__hash():
    """
    Tests whether ``.ChannelMetadataPrivateBase.__hash__`` works as intended.
    """
    users = [User.precreate(202209180119)]
    
    channel_metadata = ChannelMetadataPrivateBase({
        'users': users
    })
    
    vampytest.assert_instance(hash(channel_metadata), int)



def test__ChannelMetadataPrivateBase__eq():
    """
    Tests whether ``.ChannelMetadataPrivateBase.__eq__`` works as intended.
    """
    user_1 = User.precreate(202209150008)
    user_2 = User.precreate(202209150009)
    
    keyword_parameters = {'users': [user_1]}
    
    channel_metadata = ChannelMetadataPrivateBase(keyword_parameters)
    
    vampytest.assert_eq(channel_metadata, channel_metadata)
    vampytest.assert_ne(channel_metadata, object())
    
    for field_name, field_value in (
        ('users', [user_2]),
    ):
        test_channel_metadata = ChannelMetadataPrivateBase({**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(channel_metadata, test_channel_metadata)
