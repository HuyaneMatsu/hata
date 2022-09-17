import vampytest

from ....bases import Icon, IconType
from ....user import User

from .. import ChannelMetadataPrivateGroup


def test__ChannelMetadataPrivateGroup__repr():
    """
    Tests whether ``.ChannelMetadataPrivateGroup.__repr__`` works as intended.
    """
    users = [User.precreate(202209160017)]
    owner_id = 202209160020
    icon = Icon(IconType.static, 1)
    name = 'Armelyrics'
    
    keyword_parameters = {
        'users': users,
        'owner_id': owner_id,
        'name': name,
    }
    channel_metadata = ChannelMetadataPrivateGroup(keyword_parameters)
    channel_metadata.icon = icon
    
    vampytest.assert_instance(repr(channel_metadata), str)


def test__ChannelMetadataPrivateGroup__eq():
    """
    Tests whether ``.ChannelMetadataPrivateGroup.__eq__`` works as intended.
    """
    user_1 = User.precreate(202209160018)
    user_2 = User.precreate(202209160019)
    owner_id = 202209160021
    icon = Icon(IconType.static, 1)
    name = 'Armelyrics'
    
    keyword_parameters = {
        'users': [user_1],
        'owner_id': owner_id,
        'name': name,
    }
    channel_metadata = ChannelMetadataPrivateGroup(keyword_parameters)
    channel_metadata.icon = icon
    
    vampytest.assert_eq(channel_metadata, channel_metadata)
    vampytest.assert_ne(channel_metadata, object())
    
    for field_name, field_value in (
        ('users', [user_2]),
        ('owner_id', 202209160022),
        ('icon', Icon(IconType.static, 2)),
        ('name', 'Okuu'),        
    ):
        if field_name == 'icon':
            test_channel_metadata = ChannelMetadataPrivateGroup(keyword_parameters)
            test_channel_metadata.icon = field_value
        
        else:
            test_channel_metadata = ChannelMetadataPrivateGroup({**keyword_parameters, field_name: field_value})
            test_channel_metadata.icon = icon
        
        vampytest.assert_ne(channel_metadata, test_channel_metadata)
