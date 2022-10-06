import vampytest

from ....permission import PermissionOverwrite, PermissionOverwriteTargetType

from .. import ChannelMetadataGuildMainBase

from .test__ChannelMetadataGuildMainBase__constructor import assert_fields_set


def test__ChannelMetadataGuildMainBase__from_data():
    """
    Tests whether ``ChannelMetadataGuildMainBase.from_data` works as intended.
    """
    parent_id = 202209170013
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170019, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    
    
    channel_metadata = ChannelMetadataGuildMainBase.from_data({
        'parent_id': str(parent_id),
        'name': name,
        'permission_overwrites': [
            permission_overwrite.to_data(include_internals = True)
            for permission_overwrite in permission_overwrites
        ],
        'position': position,
    })
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildMainBase)
    assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.parent_id, parent_id)
    vampytest.assert_eq(channel_metadata.name, name)
    vampytest.assert_eq(
        channel_metadata.permission_overwrites,
        {permission_overwrite.target_id: permission_overwrite for permission_overwrite in permission_overwrites},
    )
    vampytest.assert_eq(channel_metadata.position, position)


def test__ChannelMetadataGuildMainBase__to_data():
    """
    Tests whether ``ChannelMetadataGuildMainBase.to_data`` works as intended.
    
    Case: include defaults and internals.
    """
    parent_id = 202209170014
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170020, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    
    channel_metadata = ChannelMetadataGuildMainBase({
        'parent_id': parent_id,
        'name': name,
        'permission_overwrites': permission_overwrites,
        'position': position,
    })
    
    data = channel_metadata.to_data(defaults = True, include_internals = True)
    
    vampytest.assert_eq(
        data,
        {
            'parent_id': str(parent_id),
            'name': name,
            'permission_overwrites': [
                permission_overwrite.to_data(include_internals = True)
                for permission_overwrite in permission_overwrites
            ],
            'position': position,
        },
    )


def test__ChannelMetadataGuildMainBase__update_attributes():
    """
    Tests whether ``ChannelMetadataGuildMainBase._update_attributes`` works as intended.
    """
    old_parent_id = 202209170015
    new_parent_id = 202209170016
    old_name = 'Armelyrics'
    new_name = 'Okuu'
    old_permission_overwrites = [
        PermissionOverwrite(202209170021, target_type = PermissionOverwriteTargetType.user)
    ]
    new_permission_overwrites = [
        PermissionOverwrite(202209170022, target_type = PermissionOverwriteTargetType.role)
    ]
    old_position = 7
    new_position = 5
    
    channel_metadata = ChannelMetadataGuildMainBase({
        'parent_id': old_parent_id,
        'name': old_name,
        'permission_overwrites': old_permission_overwrites,
        'position': old_position,
    })
    
    channel_metadata._update_attributes({
        'parent_id': str(new_parent_id),
        'name': new_name,
        'permission_overwrites': [
            permission_overwrite.to_data(include_internals = True)
            for permission_overwrite in new_permission_overwrites
        ],
        'position': new_position,
    })
    
    vampytest.assert_eq(channel_metadata.parent_id, new_parent_id)
    vampytest.assert_eq(channel_metadata.name, new_name)
    vampytest.assert_eq(
        channel_metadata.permission_overwrites,
        {permission_overwrite.target_id: permission_overwrite for permission_overwrite in new_permission_overwrites},
    )
    vampytest.assert_eq(channel_metadata.position, new_position)


def test__ChannelMetadataGuildMainBase__difference_update_attributes():
    """
    Tests whether ``ChannelMetadataGuildMainBase._difference_update_attributes`` works as intended.
    """
    old_parent_id = 202209170017
    new_parent_id = 202209170018
    old_name = 'Armelyrics'
    new_name = 'Okuu'
    old_permission_overwrites = [
        PermissionOverwrite(202209170021, target_type = PermissionOverwriteTargetType.user)
    ]
    new_permission_overwrites = [
        PermissionOverwrite(202209170022, target_type = PermissionOverwriteTargetType.role)
    ]
    old_position = 7
    new_position = 5
    
    channel_metadata = ChannelMetadataGuildMainBase({
        'parent_id': str(old_parent_id),
        'name': old_name,
        'permission_overwrites': old_permission_overwrites,
        'position': old_position,
    })
    
    old_attributes = channel_metadata._difference_update_attributes({
        'parent_id': str(new_parent_id),
        'name': new_name,
        'permission_overwrites': [
            permission_overwrite.to_data(include_internals = True)
            for permission_overwrite in new_permission_overwrites
        ],
        'position': new_position,
    })

    vampytest.assert_eq(channel_metadata.parent_id, new_parent_id)
    vampytest.assert_eq(channel_metadata.name, new_name)
    vampytest.assert_eq(
        channel_metadata.permission_overwrites,
        {permission_overwrite.target_id: permission_overwrite for permission_overwrite in new_permission_overwrites},
    )
    vampytest.assert_eq(channel_metadata.position, new_position)
    
    vampytest.assert_in('parent_id', old_attributes)
    vampytest.assert_in('name', old_attributes)
    vampytest.assert_in('permission_overwrites', old_attributes)
    vampytest.assert_in('position', old_attributes)
    
    vampytest.assert_eq(old_attributes['parent_id'], old_parent_id)
    vampytest.assert_eq(old_attributes['name'], old_name)
    vampytest.assert_eq(
        old_attributes['permission_overwrites'],
        {permission_overwrite.target_id: permission_overwrite for permission_overwrite in old_permission_overwrites},
    )
    vampytest.assert_eq(old_attributes['position'], old_position)


def test__ChannelMetadataGuildMainBase__from_partial_data():
    """
    Tests whether ``ChannelMetadataGuildMainBase._from_partial_data`` works as intended.
    """
    name = 'Armelyrics'
    
    channel_metadata = ChannelMetadataGuildMainBase._from_partial_data({
        'name': name,
    })
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildMainBase)
    assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.name, name)
