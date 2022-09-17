import vampytest

from ....user import User

from .. import ChannelMetadataPrivate


def test__ChannelMetadataPrivate__repr():
    """
    Tests whether ``.ChannelMetadataPrivate.__repr__`` works as intended.
    """
    users = [User.precreate(202209150004)]
    
    channel_metadata = ChannelMetadataPrivate({
        'users': users
    })
    
    vampytest.assert_instance(repr(channel_metadata), str)


def test__ChannelMetadataPrivate__eq():
    """
    Tests whether ``.ChannelMetadataPrivate.__eq__`` works as intended.
    """
    user_1 = User.precreate(202209150005)
    user_2 = User.precreate(202209150006)
    
    keyword_parameters = {'users': [user_1]}
    
    channel_metadata = ChannelMetadataPrivate(keyword_parameters)
    
    vampytest.assert_eq(channel_metadata, channel_metadata)
    vampytest.assert_ne(channel_metadata, object())
    
    for field_name, field_value in (
        ('users', [user_2]),
    ):
        test_channel_metadata = ChannelMetadataPrivate({**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(channel_metadata, test_channel_metadata)
