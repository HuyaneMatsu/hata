import vampytest

from ...permission_overwrite import PermissionOverwrite, PermissionOverwriteTargetType

from ..guild_store import ChannelMetadataGuildStore

from .test__ChannelMetadataGuildStore__constructor import _assert_fields_set


def test__ChannelMetadataGuildStore__copy():
    """
    Tests whether ``ChannelMetadataGuildStore.copy` works as intended.
    """
    name = 'alice'
    parent_id = 202304120178
    permission_overwrites = [
        PermissionOverwrite(202304120179, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    nsfw = False
    
    channel_metadata = ChannelMetadataGuildStore(
        name = name,
        parent_id = parent_id,
        permission_overwrites = permission_overwrites,
        position = position,
        nsfw = nsfw,
    )
    
    copy = channel_metadata.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    
    vampytest.assert_eq(copy, channel_metadata)


def test__ChannelMetadataGuildStore__copy_with__0():
    """
    Tests whether ``ChannelMetadataGuildStore.copy_with` works as intended.
    
    Case: No fields.
    """
    name = 'alice'
    parent_id = 202304120180
    permission_overwrites = [
        PermissionOverwrite(202304120181, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    nsfw = False
    
    channel_metadata = ChannelMetadataGuildStore(
        name = name,
        parent_id = parent_id,
        permission_overwrites = permission_overwrites,
        position = position,
        nsfw = nsfw,
    )
    
    copy = channel_metadata.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    
    vampytest.assert_eq(copy, channel_metadata)


def test__ChannelMetadataGuildStore__copy_with__1():
    """
    Tests whether ``ChannelMetadataGuildStore.copy_with` works as intended.
    
    Case: All fields.
    """
    old_name = 'alice'
    old_parent_id = 202304120182
    old_permission_overwrites = [
        PermissionOverwrite(202304120183, target_type = PermissionOverwriteTargetType.user)
    ]
    old_position = 7
    old_nsfw = False
    
    new_name = 'emotion'
    new_parent_id = 202304120184
    new_permission_overwrites = [
        PermissionOverwrite(202304120185, target_type = PermissionOverwriteTargetType.role)
    ]
    new_position = 5
    new_nsfw = True
    
    channel_metadata = ChannelMetadataGuildStore(
        name = old_name,
        parent_id = old_parent_id,
        permission_overwrites = old_permission_overwrites,
        position = old_position,
        nsfw = old_nsfw,
    )
    
    copy = channel_metadata.copy_with(
        name = new_name,
        parent_id = new_parent_id,
        permission_overwrites = new_permission_overwrites,
        position = new_position,
        nsfw = new_nsfw,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.parent_id, new_parent_id)
    vampytest.assert_eq(
        copy.permission_overwrites,
        {permission_overwrite.target_id: permission_overwrite for permission_overwrite in new_permission_overwrites},
    )
    vampytest.assert_eq(copy.position, new_position)
    vampytest.assert_eq(copy.nsfw, new_nsfw)


def test__ChannelMetadataGuildStore__copy_with_keyword_parameters__0():
    """
    Tests whether ``ChannelMetadataGuildStore.copy_with_keyword_parameters` works as intended.
    
    Case: No fields.
    """
    name = 'alice'
    parent_id = 202304120186
    permission_overwrites = [
        PermissionOverwrite(202304120187, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    nsfw = False
    
    channel_metadata = ChannelMetadataGuildStore(
        name = name,
        parent_id = parent_id,
        permission_overwrites = permission_overwrites,
        position = position,
        nsfw = nsfw,
    )
    
    keyword_parameters = {}
    copy = channel_metadata.copy_with_keyword_parameters(keyword_parameters)
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    vampytest.assert_eq(keyword_parameters, {})
    
    vampytest.assert_eq(copy, channel_metadata)


def test__ChannelMetadataGuildStore__copy_with_keyword_parameters__1():
    """
    Tests whether ``ChannelMetadataGuildStore.copy_with_keyword_parameters` works as intended.
    
    Case: All fields.
    """
    old_name = 'alice'
    old_parent_id = 202304120188
    old_permission_overwrites = [
        PermissionOverwrite(202304120189, target_type = PermissionOverwriteTargetType.user)
    ]
    old_position = 7
    old_nsfw = False
    
    new_name = 'emotion'
    new_parent_id = 202304120190
    new_permission_overwrites = [
        PermissionOverwrite(202304120191, target_type = PermissionOverwriteTargetType.role)
    ]
    new_position = 5
    new_nsfw = True
    
    channel_metadata = ChannelMetadataGuildStore(
        name = old_name,
        parent_id = old_parent_id,
        permission_overwrites = old_permission_overwrites,
        position = old_position,
        nsfw = old_nsfw,
    )
    
    keyword_parameters = {
        'name': new_name,
        'parent_id': new_parent_id,
        'permission_overwrites': new_permission_overwrites,
        'position': new_position,
        'nsfw': new_nsfw,
    }
    
    copy = channel_metadata.copy_with_keyword_parameters(keyword_parameters)
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    vampytest.assert_eq(keyword_parameters, {})
    
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.parent_id, new_parent_id)
    vampytest.assert_eq(
        copy.permission_overwrites,
        {permission_overwrite.target_id: permission_overwrite for permission_overwrite in new_permission_overwrites},
    )
    vampytest.assert_eq(copy.position, new_position)
    vampytest.assert_eq(copy.nsfw, new_nsfw)
