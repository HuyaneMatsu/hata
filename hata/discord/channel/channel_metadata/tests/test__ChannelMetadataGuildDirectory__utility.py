import vampytest

from ...permission_overwrite import PermissionOverwrite, PermissionOverwriteTargetType

from ..guild_directory import ChannelMetadataGuildDirectory

from .test__ChannelMetadataGuildDirectory__constructor import _assert_fields_set


def test__ChannelMetadataGuildDirectory__copy():
    """
    Tests whether ``ChannelMetadataGuildDirectory.copy` works as intended.
    """
    name = 'alice'
    parent_id = 202304120143
    permission_overwrites = [
        PermissionOverwrite(202304120144, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    
    channel_metadata = ChannelMetadataGuildDirectory(
        name = name,
        parent_id = parent_id,
        permission_overwrites = permission_overwrites,
        position = position,
    )
    
    copy = channel_metadata.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    
    vampytest.assert_eq(copy, channel_metadata)


def test__ChannelMetadataGuildDirectory__copy_with__0():
    """
    Tests whether ``ChannelMetadataGuildDirectory.copy_with` works as intended.
    
    Case: No fields.
    """
    name = 'alice'
    parent_id = 202304120145
    permission_overwrites = [
        PermissionOverwrite(202304120146, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    
    channel_metadata = ChannelMetadataGuildDirectory(
        name = name,
        parent_id = parent_id,
        permission_overwrites = permission_overwrites,
        position = position,
    )
    
    copy = channel_metadata.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    
    vampytest.assert_eq(copy, channel_metadata)


def test__ChannelMetadataGuildDirectory__copy_with__1():
    """
    Tests whether ``ChannelMetadataGuildDirectory.copy_with` works as intended.
    
    Case: All fields.
    """
    old_name = 'alice'
    old_parent_id = 202304120147
    old_permission_overwrites = [
        PermissionOverwrite(202304120148, target_type = PermissionOverwriteTargetType.user)
    ]
    old_position = 7
    
    new_name = 'emotion'
    new_parent_id = 202304120149
    new_permission_overwrites = [
        PermissionOverwrite(202304120150, target_type = PermissionOverwriteTargetType.role)
    ]
    new_position = 5
    
    channel_metadata = ChannelMetadataGuildDirectory(
        name = old_name,
        parent_id = old_parent_id,
        permission_overwrites = old_permission_overwrites,
        position = old_position,
    )
    
    copy = channel_metadata.copy_with(
        name = new_name,
        parent_id = new_parent_id,
        permission_overwrites = new_permission_overwrites,
        position = new_position,
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


def test__ChannelMetadataGuildDirectory__copy_with_keyword_parameters__0():
    """
    Tests whether ``ChannelMetadataGuildDirectory.copy_with_keyword_parameters` works as intended.
    
    Case: No fields.
    """
    name = 'alice'
    parent_id = 202304120151
    permission_overwrites = [
        PermissionOverwrite(202304120152, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    
    channel_metadata = ChannelMetadataGuildDirectory(
        name = name,
        parent_id = parent_id,
        permission_overwrites = permission_overwrites,
        position = position,
    )
    
    keyword_parameters = {}
    copy = channel_metadata.copy_with_keyword_parameters(keyword_parameters)
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    vampytest.assert_eq(keyword_parameters, {})
    
    vampytest.assert_eq(copy, channel_metadata)


def test__ChannelMetadataGuildDirectory__copy_with_keyword_parameters__1():
    """
    Tests whether ``ChannelMetadataGuildDirectory.copy_with_keyword_parameters` works as intended.
    
    Case: All fields.
    """
    old_name = 'alice'
    old_parent_id = 202304120153
    old_permission_overwrites = [
        PermissionOverwrite(202304120154, target_type = PermissionOverwriteTargetType.user)
    ]
    old_position = 7
    
    new_name = 'emotion'
    new_parent_id = 202304120155
    new_permission_overwrites = [
        PermissionOverwrite(202304120156, target_type = PermissionOverwriteTargetType.role)
    ]
    new_position = 5
    
    channel_metadata = ChannelMetadataGuildDirectory(
        name = old_name,
        parent_id = old_parent_id,
        permission_overwrites = old_permission_overwrites,
        position = old_position,
    )
    
    keyword_parameters = {
        'name': new_name,
        'parent_id': new_parent_id,
        'permission_overwrites': new_permission_overwrites,
        'position': new_position,
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
