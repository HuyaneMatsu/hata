import vampytest

from ....permission import PermissionOverwrite, PermissionOverwriteTargetType

from .. import ChannelMetadataGuildDirectory


def test__ChannelMetadataGuildDirectory__from_data():
    """
    Tests whether ``ChannelMetadataGuildDirectory.from_data` works as intended.
    """
    parent_id = 202209170054
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170055, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    
    
    channel_metadata = ChannelMetadataGuildDirectory.from_data({
        'parent_id': str(parent_id),
        'name': name,
        'permission_overwrites': [
            permission_overwrite.to_data(include_internals = True)
            for permission_overwrite in permission_overwrites
        ],
        'position': position,
    })
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildDirectory)
    
    vampytest.assert_eq(channel_metadata.parent_id, parent_id)
    vampytest.assert_eq(channel_metadata.name, name)
    vampytest.assert_eq(
        channel_metadata.permission_overwrites,
        {permission_overwrite.target_id: permission_overwrite for permission_overwrite in permission_overwrites},
    )
    vampytest.assert_eq(channel_metadata.position, position)


def test__ChannelMetadataGuildDirectory__to_data():
    """
    Tests whether ``ChannelMetadataGuildDirectory.to_data`` works as intended.
    """
    parent_id = 202209170057
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170056, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    
    channel_metadata = ChannelMetadataGuildDirectory({
        'parent_id': parent_id,
        'name': name,
        'permission_overwrites': permission_overwrites,
        'position': position,
    })
    
    data = channel_metadata.to_data()
    
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


def test__ChannelMetadataGuildDirectory__update_attributes():
    """
    Tests whether ``ChannelMetadataGuildDirectory._update_attributes`` works as intended.
    """
    old_parent_id = 202209170058
    new_parent_id = 202209170059
    old_name = 'Armelyrics'
    new_name = 'Okuu'
    old_permission_overwrites = [
        PermissionOverwrite(202209170060, target_type = PermissionOverwriteTargetType.user)
    ]
    new_permission_overwrites = [
        PermissionOverwrite(202209170061, target_type = PermissionOverwriteTargetType.role)
    ]
    old_position = 7
    new_position = 5
    
    channel_metadata = ChannelMetadataGuildDirectory({
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


def test__ChannelMetadataGuildDirectory__difference_update_attributes():
    """
    Tests whether ``ChannelMetadataGuildDirectory._difference_update_attributes`` works as intended.
    """
    old_parent_id = 202209170062
    new_parent_id = 202209170063
    old_name = 'Armelyrics'
    new_name = 'Okuu'
    old_permission_overwrites = [
        PermissionOverwrite(202209170064, target_type = PermissionOverwriteTargetType.user)
    ]
    new_permission_overwrites = [
        PermissionOverwrite(202209170065, target_type = PermissionOverwriteTargetType.role)
    ]
    old_position = 7
    new_position = 5
    
    channel_metadata = ChannelMetadataGuildDirectory({
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


def test__ChannelMetadataGuildDirectory__from_partial_data():
    """
    Tests whether ``ChannelMetadataGuildDirectory._from_partial_data`` works as intended.
    """
    name = 'Armelyrics'
    
    channel_metadata = ChannelMetadataGuildDirectory._from_partial_data({
        'name': name,
    })
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildDirectory)
    
    vampytest.assert_instance(channel_metadata.parent_id, int)
    vampytest.assert_instance(channel_metadata._permission_cache, dict, nullable = True)
    vampytest.assert_instance(channel_metadata.permission_overwrites, dict)
    vampytest.assert_instance(channel_metadata.position, int)
    
    vampytest.assert_eq(channel_metadata.name, name)
