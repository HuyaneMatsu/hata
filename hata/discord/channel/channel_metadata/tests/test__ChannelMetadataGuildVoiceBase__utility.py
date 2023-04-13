import vampytest

from ...permission_overwrite import PermissionOverwrite, PermissionOverwriteTargetType

from ..guild_voice_base import ChannelMetadataGuildVoiceBase
from ..preinstanced import VoiceRegion

from .test__ChannelMetadataGuildVoiceBase__constructor import _assert_fields_set


def test__ChannelMetadataGuildVoiceBase__copy():
    """
    Tests whether ``ChannelMetadataGuildVoiceBase.copy` works as intended.
    """
    name = 'alice'
    parent_id = 202304120192
    permission_overwrites = [
        PermissionOverwrite(202304120193, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    bitrate = 50000
    region = VoiceRegion.brazil
    user_limit = 4
    
    channel_metadata = ChannelMetadataGuildVoiceBase(
        name = name,
        parent_id = parent_id,
        permission_overwrites = permission_overwrites,
        position = position,
        bitrate = bitrate,
        region = region,
        user_limit = user_limit,
    )
    
    copy = channel_metadata.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    
    vampytest.assert_eq(copy, channel_metadata)


def test__ChannelMetadataGuildVoiceBase__copy_with__0():
    """
    Tests whether ``ChannelMetadataGuildVoiceBase.copy_with` works as intended.
    
    Case: No fields.
    """
    name = 'alice'
    parent_id = 202304120194
    permission_overwrites = [
        PermissionOverwrite(202304120195, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    bitrate = 50000
    region = VoiceRegion.brazil
    user_limit = 4
    
    channel_metadata = ChannelMetadataGuildVoiceBase(
        name = name,
        parent_id = parent_id,
        permission_overwrites = permission_overwrites,
        position = position,
        bitrate = bitrate,
        region = region,
        user_limit = user_limit,
    )
    
    copy = channel_metadata.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    
    vampytest.assert_eq(copy, channel_metadata)


def test__ChannelMetadataGuildVoiceBase__copy_with__1():
    """
    Tests whether ``ChannelMetadataGuildVoiceBase.copy_with` works as intended.
    
    Case: All fields.
    """
    old_name = 'alice'
    old_parent_id = 202304120196
    old_permission_overwrites = [
        PermissionOverwrite(202304120197, target_type = PermissionOverwriteTargetType.user)
    ]
    old_position = 7
    old_bitrate = 50000
    old_region = VoiceRegion.brazil
    old_user_limit = 4
    
    new_name = 'emotion'
    new_parent_id = 202304120198
    new_permission_overwrites = [
        PermissionOverwrite(202304120199, target_type = PermissionOverwriteTargetType.role)
    ]
    new_position = 5
    new_bitrate = 60000
    new_region = VoiceRegion.india
    new_user_limit = 5
    
    channel_metadata = ChannelMetadataGuildVoiceBase(
        name = old_name,
        parent_id = old_parent_id,
        permission_overwrites = old_permission_overwrites,
        position = old_position,
        bitrate = old_bitrate,
        region = old_region,
        user_limit = old_user_limit,
    )
    
    copy = channel_metadata.copy_with(
        name = new_name,
        parent_id = new_parent_id,
        permission_overwrites = new_permission_overwrites,
        position = new_position,
        bitrate = new_bitrate,
        region = new_region,
        user_limit = new_user_limit,
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
    vampytest.assert_eq(copy.bitrate, new_bitrate)
    vampytest.assert_eq(copy.region, new_region)
    vampytest.assert_eq(copy.user_limit, new_user_limit)


def test__ChannelMetadataGuildVoiceBase__copy_with_keyword_parameters__0():
    """
    Tests whether ``ChannelMetadataGuildVoiceBase.copy_with_keyword_parameters` works as intended.
    
    Case: No fields.
    """
    name = 'alice'
    parent_id = 202304120200
    permission_overwrites = [
        PermissionOverwrite(202304120201, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    bitrate = 50000
    region = VoiceRegion.brazil
    user_limit = 4
    
    channel_metadata = ChannelMetadataGuildVoiceBase(
        name = name,
        parent_id = parent_id,
        permission_overwrites = permission_overwrites,
        position = position,
        bitrate = bitrate,
        region = region,
        user_limit = user_limit,
    )
    
    keyword_parameters = {}
    copy = channel_metadata.copy_with_keyword_parameters(keyword_parameters)
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    vampytest.assert_eq(keyword_parameters, {})
    
    vampytest.assert_eq(copy, channel_metadata)


def test__ChannelMetadataGuildVoiceBase__copy_with_keyword_parameters__1():
    """
    Tests whether ``ChannelMetadataGuildVoiceBase.copy_with_keyword_parameters` works as intended.
    
    Case: All fields.
    """
    old_name = 'alice'
    old_parent_id = 202304120202
    old_permission_overwrites = [
        PermissionOverwrite(202304120203, target_type = PermissionOverwriteTargetType.user)
    ]
    old_position = 7
    old_bitrate = 50000
    old_region = VoiceRegion.brazil
    old_user_limit = 4
    
    new_name = 'emotion'
    new_parent_id = 202304120204
    new_permission_overwrites = [
        PermissionOverwrite(202304120205, target_type = PermissionOverwriteTargetType.role)
    ]
    new_position = 5
    new_bitrate = 60000
    new_region = VoiceRegion.india
    new_user_limit = 5
    
    channel_metadata = ChannelMetadataGuildVoiceBase(
        name = old_name,
        parent_id = old_parent_id,
        permission_overwrites = old_permission_overwrites,
        position = old_position,
        bitrate = old_bitrate,
        region = old_region,
        user_limit = old_user_limit,
    )
    
    keyword_parameters = {
        'name': new_name,
        'parent_id': new_parent_id,
        'permission_overwrites': new_permission_overwrites,
        'position': new_position,
        'bitrate': new_bitrate,
        'region': new_region,
        'user_limit': new_user_limit,
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
    vampytest.assert_eq(copy.bitrate, new_bitrate)
    vampytest.assert_eq(copy.region, new_region)
    vampytest.assert_eq(copy.user_limit, new_user_limit)
