import vampytest

from ....bases import Icon, IconType
from ....user import User

from .. import ChannelMetadataPrivateGroup

from .test__ChannelMetadataPrivateGroup__constructor import assert_fields_set


def test__ChannelMetadataPrivateGroup__from_data():
    """
    Tests whether ``ChannelMetadataPrivateGroup.from_data` works as intended.
    """
    user_1 = User.precreate(202209160009)
    owner_id = 202209160010
    icon = Icon(IconType.static, 1)
    name = 'Armelyrics'
    
    channel_metadata = ChannelMetadataPrivateGroup.from_data({
        'recipients': [user_1.to_data()],
        'owner_id': str(owner_id),
        'icon': icon.as_base16_hash,
        'name': name,
    })
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataPrivateGroup)
    assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.users, [user_1])
    vampytest.assert_eq(channel_metadata.owner_id, owner_id)
    vampytest.assert_eq(channel_metadata.icon, icon)
    vampytest.assert_eq(channel_metadata.name, name)


def test__ChannelMetadataPrivateGroup__to_data():
    """
    Tests whether ``ChannelMetadataPrivateGroup.to_data`` works as intended.
    """
    user_1 = User.precreate(202209160011)
    owner_id = 202209160012
    icon = Icon(IconType.static, 1)
    name = 'Armelyrics'
    
    channel_metadata = ChannelMetadataPrivateGroup({
        'users': [user_1],
        'owner_id': owner_id,
        'name': name,
    })
    channel_metadata.icon = icon
    
    data = channel_metadata.to_data()
    
    vampytest.assert_eq(
        data,
        {
            'recipients': [user_1.to_data()],
            'owner_id': str(owner_id),
            'icon': icon.as_base16_hash,
            'name': name,
        },
    )


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
    
    channel_metadata = ChannelMetadataPrivateGroup({
        'owner_id': old_owner_id,
        'name': old_name,
    })
    channel_metadata.icon = old_icon
    
    channel_metadata._update_attributes({
        'owner_id': str(new_owner_id),
        'icon': new_icon.as_base16_hash,
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
    
    channel_metadata = ChannelMetadataPrivateGroup({
        'owner_id': str(old_owner_id),
        'name': old_name,
    })
    channel_metadata.icon = old_icon
    
    old_attributes = channel_metadata._difference_update_attributes({
        'owner_id': str(new_owner_id),
        'icon': new_icon.as_base16_hash,
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
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataPrivateGroup)
    assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.name, name)
