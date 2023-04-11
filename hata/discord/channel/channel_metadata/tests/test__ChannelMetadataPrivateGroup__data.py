import vampytest

from ....bases import Icon, IconType
from ....user import User

from ..private_group import ChannelMetadataPrivateGroup

from .test__ChannelMetadataPrivateGroup__constructor import _assert_fields_set


def test__ChannelMetadataPrivateGroup__from_data():
    """
    Tests whether ``ChannelMetadataPrivateGroup.from_data` works as intended.
    """
    application_id = 202301210002
    user_1 = User.precreate(202209160009)
    owner_id = 202209160010
    icon = Icon(IconType.static, 1)
    name = 'Armelyrics'
    
    channel_metadata = ChannelMetadataPrivateGroup.from_data({
        'application_id': str(application_id),
        'recipients': [user_1.to_data(defaults = True, include_internals = True)],
        'owner_id': str(owner_id),
        'icon': icon.as_base_16_hash,
        'name': name,
    })
    _assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.application_id, application_id)
    vampytest.assert_eq(channel_metadata.users, [user_1])
    vampytest.assert_eq(channel_metadata.owner_id, owner_id)
    vampytest.assert_eq(channel_metadata.icon, icon)
    vampytest.assert_eq(channel_metadata.name, name)


def test__ChannelMetadataPrivateGroup__to_data__0():
    """
    Tests whether ``ChannelMetadataPrivateGroup.to_data`` works as intended.
    
    Case: include defaults and internals.
    """
    application_id = 202301210003
    user_1 = User.precreate(202209160011)
    owner_id = 202209160012
    icon = Icon(IconType.static, 1)
    name = 'Armelyrics'
    
    channel_metadata = ChannelMetadataPrivateGroup(
        application_id = application_id,
        users = [user_1],
        owner_id = owner_id,
        name = name,
        icon = icon,
    )
    
    data = channel_metadata.to_data(defaults = True, include_internals = True)
    
    expected_output = {
        'application_id': str(application_id),
        'recipients': [user_1.to_data(defaults = True, include_internals = True)],
        'owner_id': str(owner_id),
        'icon': icon.as_base_16_hash,
        'name': name,
    }

    vampytest.assert_eq(
        data,
        expected_output,
    )


def test__ChannelMetadataPrivateGroup__to_data__1():
    """
    Tests whether ``ChannelMetadataPrivateGroup.to_data`` works as intended.
    
    Case: default.
    """
    icon = (
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00'
        b'\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\x00\x00\x0bIDAT\x08\x99c\xf8\x0f\x04\x00\t\xfb\x03\xfd\xe3U'
        b'\xf2\x9c\x00\x00\x00\x00IEND\xaeB`\x82'
    )
    
    name = 'Armelyrics'
    
    channel_metadata = ChannelMetadataPrivateGroup(
        name = name,
        icon = icon,
    )
    
    data = channel_metadata.to_data(defaults = True, include_internals = True)
    
    vampytest.assert_in('icon', data)
    vampytest.assert_in('name', data)
    
    vampytest.assert_instance(data['icon'], str)
    vampytest.assert_eq(data['name'], name)


def test__ChannelMetadataPrivateGroup__update_attributes():
    """
    Tests whether ``ChannelMetadataPrivateGroup._update_attributes`` works as intended.
    """
    old_owner_id = 202209160013
    new_owner_id = 202209160014
    old_icon = Icon(IconType.static, 1)
    new_icon = Icon(IconType.static, 2)
    old_name = 'Armelyrics'
    new_name = 'Okuu'
    
    channel_metadata = ChannelMetadataPrivateGroup(
        owner_id = old_owner_id,
        name = old_name,
        icon = old_icon,
    )
    
    channel_metadata._update_attributes({
        'owner_id': str(new_owner_id),
        'icon': new_icon.as_base_16_hash,
        'name': new_name,
    })
    
    vampytest.assert_eq(channel_metadata.owner_id, new_owner_id)
    vampytest.assert_eq(channel_metadata.icon, new_icon)
    vampytest.assert_eq(channel_metadata.name, new_name)


def test__ChannelMetadataPrivateGroup__difference_update_attributes():
    """
    Tests whether ``ChannelMetadataPrivateGroup._difference_update_attributes`` works as intended.
    """
    old_owner_id = 202209160015
    new_owner_id = 202209160016
    old_icon = Icon(IconType.static, 1)
    new_icon = Icon(IconType.static, 2)
    old_name = 'Armelyrics'
    new_name = 'Okuu'
    
    channel_metadata = ChannelMetadataPrivateGroup(
        owner_id = old_owner_id,
        name = old_name,
        icon = old_icon,
    )
    
    old_attributes = channel_metadata._difference_update_attributes({
        'owner_id': str(new_owner_id),
        'icon': new_icon.as_base_16_hash,
        'name': new_name,
    })

    vampytest.assert_eq(channel_metadata.owner_id, new_owner_id)
    vampytest.assert_eq(channel_metadata.icon, new_icon)
    vampytest.assert_eq(channel_metadata.name, new_name)
    
    vampytest.assert_in('owner_id', old_attributes)
    vampytest.assert_in('icon', old_attributes)
    vampytest.assert_in('name', old_attributes)
    
    vampytest.assert_eq(old_attributes['owner_id'], old_owner_id)
    vampytest.assert_eq(old_attributes['icon'], old_icon)
    vampytest.assert_eq(old_attributes['name'], old_name)


def test__ChannelMetadataPrivateGroup__from_partial_data():
    """
    Tests whether ``ChannelMetadataPrivateGroup._from_partial_data`` works as intended.
    """
    name = 'Armelyrics'
    
    channel_metadata = ChannelMetadataPrivateGroup._from_partial_data({
        'name': name,
    })
    _assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.name, name)
