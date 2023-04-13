import vampytest

from ...permission_overwrite import PermissionOverwrite, PermissionOverwriteTargetType

from ..guild_voice import ChannelMetadataGuildVoice
from ..preinstanced import VideoQualityMode, VoiceRegion

from .test__ChannelMetadataGuildVoice__constructor import _assert_fields_set


def test__ChannelMetadataGuildVoice__copy():
    """
    Tests whether ``ChannelMetadataGuildVoice.copy` works as intended.
    """
    name = 'alice'
    parent_id = 202304130014
    permission_overwrites = [
        PermissionOverwrite(202304130015, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    bitrate = 50000
    region = VoiceRegion.brazil
    user_limit = 4
    nsfw = True
    video_quality_mode = VideoQualityMode.full
    
    channel_metadata = ChannelMetadataGuildVoice(
        name = name,
        parent_id = parent_id,
        permission_overwrites = permission_overwrites,
        position = position,
        bitrate = bitrate,
        region = region,
        user_limit = user_limit,
        nsfw = nsfw,
        video_quality_mode = video_quality_mode,
    )
    
    copy = channel_metadata.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    
    vampytest.assert_eq(copy, channel_metadata)


def test__ChannelMetadataGuildVoice__copy_with__0():
    """
    Tests whether ``ChannelMetadataGuildVoice.copy_with` works as intended.
    
    Case: No fields.
    """
    name = 'alice'
    parent_id = 202304130016
    permission_overwrites = [
        PermissionOverwrite(202304130017, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    bitrate = 50000
    region = VoiceRegion.brazil
    user_limit = 4
    nsfw = True
    video_quality_mode = VideoQualityMode.full
    
    channel_metadata = ChannelMetadataGuildVoice(
        name = name,
        parent_id = parent_id,
        permission_overwrites = permission_overwrites,
        position = position,
        bitrate = bitrate,
        region = region,
        user_limit = user_limit,
        nsfw = nsfw,
        video_quality_mode = video_quality_mode,
    )
    
    copy = channel_metadata.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    
    vampytest.assert_eq(copy, channel_metadata)


def test__ChannelMetadataGuildVoice__copy_with__1():
    """
    Tests whether ``ChannelMetadataGuildVoice.copy_with` works as intended.
    
    Case: All fields.
    """
    old_name = 'alice'
    old_parent_id = 202304130018
    old_permission_overwrites = [
        PermissionOverwrite(202304130019, target_type = PermissionOverwriteTargetType.user)
    ]
    old_position = 7
    old_bitrate = 50000
    old_region = VoiceRegion.brazil
    old_user_limit = 4
    old_nsfw = True
    old_video_quality_mode = VideoQualityMode.full
    
    new_name = 'emotion'
    new_parent_id = 202304130020
    new_permission_overwrites = [
        PermissionOverwrite(202304130021, target_type = PermissionOverwriteTargetType.role)
    ]
    new_position = 5
    new_bitrate = 60000
    new_region = VoiceRegion.india
    new_user_limit = 5
    new_nsfw = False
    new_video_quality_mode = VideoQualityMode.auto
    
    channel_metadata = ChannelMetadataGuildVoice(
        name = old_name,
        parent_id = old_parent_id,
        permission_overwrites = old_permission_overwrites,
        position = old_position,
        bitrate = old_bitrate,
        region = old_region,
        user_limit = old_user_limit,
        nsfw = old_nsfw,
        video_quality_mode = old_video_quality_mode,
    )
    
    copy = channel_metadata.copy_with(
        name = new_name,
        parent_id = new_parent_id,
        permission_overwrites = new_permission_overwrites,
        position = new_position,
        bitrate = new_bitrate,
        region = new_region,
        user_limit = new_user_limit,
        nsfw = new_nsfw,
        video_quality_mode = new_video_quality_mode,
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
    vampytest.assert_eq(copy.nsfw, new_nsfw)
    vampytest.assert_eq(copy.video_quality_mode, new_video_quality_mode)


def test__ChannelMetadataGuildVoice__copy_with_keyword_parameters__0():
    """
    Tests whether ``ChannelMetadataGuildVoice.copy_with_keyword_parameters` works as intended.
    
    Case: No fields.
    """
    name = 'alice'
    parent_id = 202304130022
    permission_overwrites = [
        PermissionOverwrite(202304130023, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    bitrate = 50000
    region = VoiceRegion.brazil
    user_limit = 4
    nsfw = True
    video_quality_mode = VideoQualityMode.full
    
    channel_metadata = ChannelMetadataGuildVoice(
        name = name,
        parent_id = parent_id,
        permission_overwrites = permission_overwrites,
        position = position,
        bitrate = bitrate,
        region = region,
        user_limit = user_limit,
        nsfw = nsfw,
        video_quality_mode = video_quality_mode,
    )
    
    keyword_parameters = {}
    copy = channel_metadata.copy_with_keyword_parameters(keyword_parameters)
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, channel_metadata)
    vampytest.assert_eq(keyword_parameters, {})
    
    vampytest.assert_eq(copy, channel_metadata)


def test__ChannelMetadataGuildVoice__copy_with_keyword_parameters__1():
    """
    Tests whether ``ChannelMetadataGuildVoice.copy_with_keyword_parameters` works as intended.
    
    Case: All fields.
    """
    old_name = 'alice'
    old_parent_id = 202304130024
    old_permission_overwrites = [
        PermissionOverwrite(202304130025, target_type = PermissionOverwriteTargetType.user)
    ]
    old_position = 7
    old_bitrate = 50000
    old_region = VoiceRegion.brazil
    old_user_limit = 4
    old_nsfw = True
    old_video_quality_mode = VideoQualityMode.full
    
    new_name = 'emotion'
    new_parent_id = 202304130026
    new_permission_overwrites = [
        PermissionOverwrite(202304130027, target_type = PermissionOverwriteTargetType.role)
    ]
    new_position = 5
    new_bitrate = 60000
    new_region = VoiceRegion.india
    new_user_limit = 5
    new_nsfw = False
    new_video_quality_mode = VideoQualityMode.auto
    
    channel_metadata = ChannelMetadataGuildVoice(
        name = old_name,
        parent_id = old_parent_id,
        permission_overwrites = old_permission_overwrites,
        position = old_position,
        bitrate = old_bitrate,
        region = old_region,
        user_limit = old_user_limit,
        nsfw = old_nsfw,
        video_quality_mode = old_video_quality_mode,
    )
    
    keyword_parameters = {
        'name': new_name,
        'parent_id': new_parent_id,
        'permission_overwrites': new_permission_overwrites,
        'position': new_position,
        'bitrate': new_bitrate,
        'region': new_region,
        'user_limit': new_user_limit,
        'nsfw': new_nsfw,
        'video_quality_mode': new_video_quality_mode,
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
    vampytest.assert_eq(copy.nsfw, new_nsfw)
    vampytest.assert_eq(copy.video_quality_mode, new_video_quality_mode)
