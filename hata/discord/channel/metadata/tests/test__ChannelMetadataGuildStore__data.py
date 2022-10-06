import vampytest

from ....permission import PermissionOverwrite, PermissionOverwriteTargetType

from .. import ChannelMetadataGuildStore

from .test__ChannelMetadataGuildStore__constructor import assert_fields_set


def test__ChannelMetadataGuildStore__from_data():
    """
    Tests whether ``ChannelMetadataGuildStore.from_data` works as intended.
    """
    parent_id = 202209170106
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170107, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    nsfw = True
    
    
    channel_metadata = ChannelMetadataGuildStore.from_data({
        'parent_id': str(parent_id),
        'name': name,
        'permission_overwrites': [
            permission_overwrite.to_data(include_internals = True)
            for permission_overwrite in permission_overwrites
        ],
        'position': position,
        'nsfw': nsfw,
    })
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildStore)
    assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.parent_id, parent_id)
    vampytest.assert_eq(channel_metadata.name, name)
    vampytest.assert_eq(
        channel_metadata.permission_overwrites,
        {permission_overwrite.target_id: permission_overwrite for permission_overwrite in permission_overwrites},
    )
    vampytest.assert_eq(channel_metadata.position, position)
    vampytest.assert_eq(channel_metadata.nsfw, nsfw)


def test__ChannelMetadataGuildStore__to_data():
    """
    Tests whether ``ChannelMetadataGuildStore.to_data`` works as intended.
    
    Case: include defaults and internals.
    """
    parent_id = 202209170108
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170109, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    nsfw = True
    
    channel_metadata = ChannelMetadataGuildStore({
        'parent_id': parent_id,
        'name': name,
        'permission_overwrites': permission_overwrites,
        'position': position,
        'nsfw': nsfw,
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
            'nsfw': nsfw,
        },
    )


def test__ChannelMetadataGuildStore__update_attributes():
    """
    Tests whether ``ChannelMetadataGuildStore._update_attributes`` works as intended.
    """
    old_parent_id = 202209170110
    new_parent_id = 202209170111
    old_name = 'Armelyrics'
    new_name = 'Okuu'
    old_permission_overwrites = [
        PermissionOverwrite(202209170112, target_type = PermissionOverwriteTargetType.user)
    ]
    new_permission_overwrites = [
        PermissionOverwrite(202209170113, target_type = PermissionOverwriteTargetType.role)
    ]
    old_position = 7
    new_position = 5
    old_nsfw = True
    new_nsfw = False
    
    channel_metadata = ChannelMetadataGuildStore({
        'parent_id': old_parent_id,
        'name': old_name,
        'permission_overwrites': old_permission_overwrites,
        'position': old_position,
        'nsfw': old_nsfw,
    })
    
    channel_metadata._update_attributes({
        'parent_id': str(new_parent_id),
        'name': new_name,
        'permission_overwrites': [
            permission_overwrite.to_data(include_internals = True)
            for permission_overwrite in new_permission_overwrites
        ],
        'position': new_position,
        'nsfw': new_nsfw,
    })
    
    vampytest.assert_eq(channel_metadata.parent_id, new_parent_id)
    vampytest.assert_eq(channel_metadata.name, new_name)
    vampytest.assert_eq(
        channel_metadata.permission_overwrites,
        {permission_overwrite.target_id: permission_overwrite for permission_overwrite in new_permission_overwrites},
    )
    vampytest.assert_eq(channel_metadata.position, new_position)
    vampytest.assert_eq(channel_metadata.nsfw, new_nsfw)


def test__ChannelMetadataGuildStore__difference_update_attributes():
    """
    Tests whether ``ChannelMetadataGuildStore._difference_update_attributes`` works as intended.
    """
    old_parent_id = 202209170114
    new_parent_id = 202209170115
    old_name = 'Armelyrics'
    new_name = 'Okuu'
    old_permission_overwrites = [
        PermissionOverwrite(202209170116, target_type = PermissionOverwriteTargetType.user)
    ]
    new_permission_overwrites = [
        PermissionOverwrite(202209170117, target_type = PermissionOverwriteTargetType.role)
    ]
    old_position = 7
    new_position = 5
    old_nsfw = True
    new_nsfw = False
    
    channel_metadata = ChannelMetadataGuildStore({
        'parent_id': str(old_parent_id),
        'name': old_name,
        'permission_overwrites': old_permission_overwrites,
        'position': old_position,
        'nsfw': old_nsfw,
    })
    
    old_attributes = channel_metadata._difference_update_attributes({
        'parent_id': str(new_parent_id),
        'name': new_name,
        'permission_overwrites': [
            permission_overwrite.to_data(include_internals = True)
            for permission_overwrite in new_permission_overwrites
        ],
        'position': new_position,
        'nsfw': new_nsfw,
    })

    vampytest.assert_eq(channel_metadata.parent_id, new_parent_id)
    vampytest.assert_eq(channel_metadata.name, new_name)
    vampytest.assert_eq(
        channel_metadata.permission_overwrites,
        {permission_overwrite.target_id: permission_overwrite for permission_overwrite in new_permission_overwrites},
    )
    vampytest.assert_eq(channel_metadata.position, new_position)
    vampytest.assert_eq(channel_metadata.nsfw, new_nsfw)
    
    vampytest.assert_in('parent_id', old_attributes)
    vampytest.assert_in('name', old_attributes)
    vampytest.assert_in('permission_overwrites', old_attributes)
    vampytest.assert_in('position', old_attributes)
    vampytest.assert_in('nsfw', old_attributes)
    
    vampytest.assert_eq(old_attributes['parent_id'], old_parent_id)
    vampytest.assert_eq(old_attributes['name'], old_name)
    vampytest.assert_eq(
        old_attributes['permission_overwrites'],
        {permission_overwrite.target_id: permission_overwrite for permission_overwrite in old_permission_overwrites},
    )
    vampytest.assert_eq(old_attributes['position'], old_position)
    vampytest.assert_eq(old_attributes['nsfw'], old_nsfw)


def test__ChannelMetadataGuildStore__from_partial_data():
    """
    Tests whether ``ChannelMetadataGuildStore._from_partial_data`` works as intended.
    """
    name = 'Armelyrics'
    
    channel_metadata = ChannelMetadataGuildStore._from_partial_data({
        'name': name,
    })
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildStore)
    assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.name, name)
