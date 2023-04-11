import vampytest

from ....bases import Icon, IconType
from ....user import User

from ..private_group import ChannelMetadataPrivateGroup


def _assert_fields_set(channel_metadata):
    vampytest.assert_instance(channel_metadata, ChannelMetadataPrivateGroup)
    
    vampytest.assert_instance(channel_metadata.application_id, int)
    vampytest.assert_instance(channel_metadata.users, list)
    vampytest.assert_instance(channel_metadata.owner_id, int)
    vampytest.assert_instance(channel_metadata.icon, Icon)
    vampytest.assert_instance(channel_metadata.name, str)


def test__ChannelMetadataPrivateGroup__new__0():
    """
    Tests whether ``ChannelMetadataPrivateGroup.__new__`` works as intended.
    
    Case: all fields given.
    """
    application_id = 202301210000
    users = [User.precreate(202209160005)]
    owner_id = 202209160006
    icon = Icon(IconType.static, 1)
    name = 'Armelyrics'
    
    channel_metadata = ChannelMetadataPrivateGroup(
        application_id = application_id,
        users = users,
        owner_id = owner_id,
        name = name,
        icon = icon,
    )
    _assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.application_id, application_id)
    vampytest.assert_eq(channel_metadata.users, users)
    vampytest.assert_eq(channel_metadata.owner_id, owner_id)
    vampytest.assert_eq(channel_metadata.icon, icon)
    vampytest.assert_eq(channel_metadata.name, name)


def test__ChannelMetadataPrivateGroup__new__1():
    """
    Tests whether ``ChannelMetadataPrivateGroup.__new__`` works as intended.
    
    Case: no fields given.
    """
    channel_metadata = ChannelMetadataPrivateGroup()
    _assert_fields_set(channel_metadata)


def test__ChannelMetadataPrivateGroup__from_keyword_parameters__0():
    """
    Tests whether ``ChannelMetadataPrivateGroup.from_keyword_parameters`` works as intended.
    
    Case: all fields given.
    """
    application_id = 202304110028
    users = [User.precreate(202304110029)]
    owner_id = 202304110030
    icon = Icon(IconType.static, 1)
    name = 'Armelyrics'
    
    keyword_parameters = {
        'application_id': application_id,
        'users': users,
        'owner_id': owner_id,
        'name': name,
        'icon': icon,
    }
    channel_metadata = ChannelMetadataPrivateGroup.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(channel_metadata)
    vampytest.assert_eq(keyword_parameters, {})
    
    vampytest.assert_eq(channel_metadata.application_id, application_id)
    vampytest.assert_eq(channel_metadata.users, users)
    vampytest.assert_eq(channel_metadata.owner_id, owner_id)
    vampytest.assert_eq(channel_metadata.icon, icon)
    vampytest.assert_eq(channel_metadata.name, name)


def test__ChannelMetadataPrivateGroup__from_keyword_parameters__1():
    """
    Tests whether ``ChannelMetadataPrivateGroup.from_keyword_parameters`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    channel_metadata = ChannelMetadataPrivateGroup.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(channel_metadata)
    vampytest.assert_eq(keyword_parameters, {})


def test__ChannelMetadataPrivateGroup__create_empty():
    """
    Tests whether ``ChannelMetadataPrivateGroup._create_empty`` works as intended.
    """
    channel_metadata = ChannelMetadataPrivateGroup._create_empty()
    _assert_fields_set(channel_metadata)
