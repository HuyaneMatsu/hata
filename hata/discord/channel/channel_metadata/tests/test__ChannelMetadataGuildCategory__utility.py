import vampytest

from ...permission_overwrite import PermissionOverwrite, PermissionOverwriteTargetType

from ..guild_category import ChannelMetadataGuildCategory

from .test__ChannelMetadataGuildCategory__constructor import _assert_fields_set


def test__ChannelMetadataGuildCategory__copy():
    """
    Tests whether ``ChannelMetadataGuildCategory.copy` works as intended.
    """
    name = 'alice'
    parent_id = 202304120115
    permission_overwrites = [
        PermissionOverwrite(202304120116, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    
    channel_metadata = ChannelMetadataGuildCategory(
        name = name,
        parent_id = parent_id,
        permission_overwrites = permission_overwrites,
        position = position,
    )
    
    copy = channel_metadata.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    
    vampytest.assert_eq(copy, channel_metadata)


def test__ChannelMetadataGuildCategory__copy_with__0():
    """
    Tests whether ``ChannelMetadataGuildCategory.copy_with` works as intended.
    
    Case: No fields.
    """
    name = 'alice'
    parent_id = 202304120117
    permission_overwrites = [
        PermissionOverwrite(202304120118, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    
    channel_metadata = ChannelMetadataGuildCategory(
        name = name,
        parent_id = parent_id,
        permission_overwrites = permission_overwrites,
        position = position,
    )
    
    copy = channel_metadata.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    
    vampytest.assert_eq(copy, channel_metadata)


def test__ChannelMetadataGuildCategory__copy_with__1():
    """
    Tests whether ``ChannelMetadataGuildCategory.copy_with` works as intended.
    
    Case: All fields.
    """
    old_name = 'alice'
    old_parent_id = 202304120119
    old_permission_overwrites = [
        PermissionOverwrite(202304120120, target_type = PermissionOverwriteTargetType.user)
    ]
    old_position = 7
    
    new_name = 'emotion'
    new_parent_id = 202304120121
    new_permission_overwrites = [
        PermissionOverwrite(202304120122, target_type = PermissionOverwriteTargetType.role)
    ]
    new_position = 5
    
    channel_metadata = ChannelMetadataGuildCategory(
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


def test__ChannelMetadataGuildCategory__copy_with_keyword_parameters__0():
    """
    Tests whether ``ChannelMetadataGuildCategory.copy_with_keyword_parameters` works as intended.
    
    Case: No fields.
    """
    name = 'alice'
    parent_id = 202304120123
    permission_overwrites = [
        PermissionOverwrite(202304120124, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    
    channel_metadata = ChannelMetadataGuildCategory(
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


def test__ChannelMetadataGuildCategory__copy_with_keyword_parameters__1():
    """
    Tests whether ``ChannelMetadataGuildCategory.copy_with_keyword_parameters` works as intended.
    
    Case: All fields.
    """
    old_name = 'alice'
    old_parent_id = 202304120125
    old_permission_overwrites = [
        PermissionOverwrite(202304120126, target_type = PermissionOverwriteTargetType.user)
    ]
    old_position = 7
    
    new_name = 'emotion'
    new_parent_id = 202304120127
    new_permission_overwrites = [
        PermissionOverwrite(202304120128, target_type = PermissionOverwriteTargetType.role)
    ]
    new_position = 5
    
    channel_metadata = ChannelMetadataGuildCategory(
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
