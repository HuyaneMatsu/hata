import vampytest

from .....bases import Icon, IconType
from .....user import User

from ..private_group import ChannelMetadataPrivateGroup


def assert_fields_set(channel_metadata):
    vampytest.assert_instance(channel_metadata.users, list)
    vampytest.assert_instance(channel_metadata.owner_id, int)
    vampytest.assert_instance(channel_metadata.icon, Icon)
    vampytest.assert_instance(channel_metadata.name, str)


def test__ChannelMetadataPrivateGroup__new__0():
    """
    Tests whether ``ChannelMetadataPrivateGroup.__new__`` works as intended.
    
    Case: all fields given.
    """
    users = [User.precreate(202209160005)]
    owner_id = 202209160006
    icon = Icon(IconType.static, 1)
    name = 'Armelyrics'
    
    keyword_parameters = {
        'users': users,
        'owner_id': owner_id,
        'name': name,
        'icon': icon,
    }
    channel_metadata = ChannelMetadataPrivateGroup(keyword_parameters)
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataPrivateGroup)
    vampytest.assert_eq(keyword_parameters, {})
    
    assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.users, users)
    vampytest.assert_eq(channel_metadata.owner_id, owner_id)
    vampytest.assert_eq(channel_metadata.icon, icon)
    vampytest.assert_eq(channel_metadata.name, name)


def test__ChannelMetadataPrivateGroup__new__1():
    """
    Tests whether ``ChannelMetadataPrivateGroup.__new__`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    channel_metadata = ChannelMetadataPrivateGroup(keyword_parameters)
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataPrivateGroup)
    vampytest.assert_eq(keyword_parameters, {})
    
    assert_fields_set(channel_metadata)

def test__ChannelMetadataPrivateGroup__create_empty():
    """
    Tests whether ``ChannelMetadataPrivateGroup._create_empty`` works as intended.
    """
    channel_metadata = ChannelMetadataPrivateGroup._create_empty()
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataPrivateGroup)
    
    assert_fields_set(channel_metadata)



def test__ChannelMetadataPrivateGroup__precreate__0():
    """
    Tests whether ``ChannelMetadataPrivateGroup.precreate`` works as intended.
    
    Case: all fields given.
    """
    users = [User.precreate(202209160007)]
    owner_id = 202209160008
    icon = Icon(IconType.static, 1)
    name = 'Armelyrics'
    
    keyword_parameters = {
        'users': users,
        'owner_id': owner_id,
        'icon': icon,
        'name': name
    }
    
    channel_metadata = ChannelMetadataPrivateGroup.precreate(keyword_parameters)
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataPrivateGroup)
    vampytest.assert_eq(keyword_parameters, {})
    
    assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.users, users)
    vampytest.assert_eq(channel_metadata.owner_id, owner_id)
    vampytest.assert_eq(channel_metadata.icon, icon)
    vampytest.assert_eq(channel_metadata.name, name)


def test__ChannelMetadataPrivateGroup__precreate__1():
    """
    Tests whether ``ChannelMetadataPrivateGroup.precreate`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    channel_metadata = ChannelMetadataPrivateGroup.precreate(keyword_parameters)
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataPrivateGroup)
    vampytest.assert_eq(keyword_parameters, {})
    
    assert_fields_set(channel_metadata)
