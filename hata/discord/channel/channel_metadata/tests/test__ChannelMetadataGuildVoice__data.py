import vampytest

from ...permission_overwrite import PermissionOverwrite, PermissionOverwriteTargetType

from ..preinstanced import VideoQualityMode, VoiceRegion

from ..guild_voice import ChannelMetadataGuildVoice

from .test__ChannelMetadataGuildVoice__constructor import _assert_fields_set


def test__ChannelMetadataGuildVoice__from_data():
    """
    Tests whether ``ChannelMetadataGuildVoice.from_data` works as intended.
    """
    parent_id = 202209170151
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170152, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    bitrate = 50000
    region = VoiceRegion.brazil
    user_limit = 4
    nsfw = True
    video_quality_mode = VideoQualityMode.auto
    
    channel_metadata = ChannelMetadataGuildVoice.from_data({
        'parent_id': str(parent_id),
        'name': name,
        'permission_overwrites': [
            permission_overwrite.to_data(include_internals = True)
            for permission_overwrite in permission_overwrites
        ],
        'position': position,
        'bitrate': bitrate,
        'rtc_region': region.value,
        'user_limit': user_limit,
        'nsfw': nsfw,
        'video_quality_mode': video_quality_mode.value,
    })
    _assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.parent_id, parent_id)
    vampytest.assert_eq(channel_metadata.name, name)
    vampytest.assert_eq(
        channel_metadata.permission_overwrites,
        {permission_overwrite.target_id: permission_overwrite for permission_overwrite in permission_overwrites},
    )
    vampytest.assert_eq(channel_metadata.position, position)
    vampytest.assert_eq(channel_metadata.bitrate, bitrate)
    vampytest.assert_eq(channel_metadata.region, region)
    vampytest.assert_eq(channel_metadata.user_limit, user_limit)
    vampytest.assert_eq(channel_metadata.nsfw, nsfw)
    vampytest.assert_eq(channel_metadata.video_quality_mode, video_quality_mode)


def test__ChannelMetadataGuildVoice__to_data():
    """
    Tests whether ``ChannelMetadataGuildVoice.to_data`` works as intended.
    
    Case: include defaults and internals.
    """
    parent_id = 202209170153
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170154, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    bitrate = 50000
    region = VoiceRegion.brazil
    user_limit = 4
    nsfw = True
    video_quality_mode = VideoQualityMode.auto
    
    channel_metadata = ChannelMetadataGuildVoice(
        parent_id = parent_id,
        name = name,
        permission_overwrites = permission_overwrites,
        position = position,
        bitrate = bitrate,
        region = region,
        user_limit = user_limit,
        nsfw = nsfw,
        video_quality_mode = video_quality_mode,
    )
    
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
            'bitrate': bitrate,
            'rtc_region': region.value,
            'user_limit': user_limit,
            'nsfw': nsfw,
            'video_quality_mode': video_quality_mode.value,
        },
    )


def test__ChannelMetadataGuildVoice__update_attributes():
    """
    Tests whether ``ChannelMetadataGuildVoice._update_attributes`` works as intended.
    """
    old_parent_id = 202209170155
    new_parent_id = 202209170156
    old_name = 'Armelyrics'
    new_name = 'Okuu'
    old_permission_overwrites = [
        PermissionOverwrite(202209170157, target_type = PermissionOverwriteTargetType.user)
    ]
    new_permission_overwrites = [
        PermissionOverwrite(202209170158, target_type = PermissionOverwriteTargetType.role)
    ]
    old_position = 7
    new_position = 5
    old_bitrate = 50000
    new_bitrate = 60000
    old_region = VoiceRegion.brazil
    new_region = VoiceRegion.india
    old_user_limit = 4
    new_user_limit = 5
    old_nsfw = True
    new_nsfw = False
    old_video_quality_mode = VideoQualityMode.auto
    new_video_quality_mode = VideoQualityMode.full
    
    channel_metadata = ChannelMetadataGuildVoice(
        parent_id = old_parent_id,
        name = old_name,
        permission_overwrites = old_permission_overwrites,
        position = old_position,
        bitrate = old_bitrate,
        region = old_region,
        user_limit = old_user_limit,
        nsfw = old_nsfw,
        video_quality_mode = old_video_quality_mode,
    )
    
    channel_metadata._update_attributes({
        'parent_id': str(new_parent_id),
        'name': new_name,
        'permission_overwrites': [
            permission_overwrite.to_data(include_internals = True)
            for permission_overwrite in new_permission_overwrites
        ],
        'position': new_position,
        'bitrate': new_bitrate,
        'rtc_region': new_region.value,
        'user_limit': new_user_limit,
        'nsfw': new_nsfw,
        'video_quality_mode': new_video_quality_mode.value,
    })
    
    vampytest.assert_eq(channel_metadata.parent_id, new_parent_id)
    vampytest.assert_eq(channel_metadata.name, new_name)
    vampytest.assert_eq(
        channel_metadata.permission_overwrites,
        {permission_overwrite.target_id: permission_overwrite for permission_overwrite in new_permission_overwrites},
    )
    vampytest.assert_eq(channel_metadata.position, new_position)
    vampytest.assert_eq(channel_metadata.bitrate, new_bitrate)
    vampytest.assert_eq(channel_metadata.region, new_region)
    vampytest.assert_eq(channel_metadata.user_limit, new_user_limit)
    vampytest.assert_eq(channel_metadata.nsfw, new_nsfw)
    vampytest.assert_eq(channel_metadata.video_quality_mode, new_video_quality_mode)



def test__ChannelMetadataGuildVoice__difference_update_attributes():
    """
    Tests whether ``ChannelMetadataGuildVoice._difference_update_attributes`` works as intended.
    """
    old_parent_id = 202209170159
    new_parent_id = 202209170160
    old_name = 'Armelyrics'
    new_name = 'Okuu'
    old_permission_overwrites = [
        PermissionOverwrite(202209170161, target_type = PermissionOverwriteTargetType.user)
    ]
    new_permission_overwrites = [
        PermissionOverwrite(202209170162, target_type = PermissionOverwriteTargetType.role)
    ]
    old_position = 7
    new_position = 5
    old_bitrate = 50000
    new_bitrate = 60000
    old_region = VoiceRegion.brazil
    new_region = VoiceRegion.india
    old_user_limit = 4
    new_user_limit = 5
    old_nsfw = True
    new_nsfw = False
    old_video_quality_mode = VideoQualityMode.auto
    new_video_quality_mode = VideoQualityMode.full
    
    channel_metadata = ChannelMetadataGuildVoice(
        parent_id = old_parent_id,
        name = old_name,
        permission_overwrites = old_permission_overwrites,
        position = old_position,
        bitrate = old_bitrate,
        region = old_region,
        user_limit = old_user_limit,
        nsfw = old_nsfw,
        video_quality_mode = old_video_quality_mode,
    )
    
    old_attributes = channel_metadata._difference_update_attributes({
        'parent_id': str(new_parent_id),
        'name': new_name,
        'permission_overwrites': [
            permission_overwrite.to_data(include_internals = True)
            for permission_overwrite in new_permission_overwrites
        ],
        'position': new_position,
        'bitrate': new_bitrate,
        'rtc_region': new_region.value,
        'user_limit': new_user_limit,
        'nsfw': new_nsfw,
        'video_quality_mode': new_video_quality_mode.value,
    })
    
    vampytest.assert_eq(channel_metadata.parent_id, new_parent_id)
    vampytest.assert_eq(channel_metadata.name, new_name)
    vampytest.assert_eq(
        channel_metadata.permission_overwrites,
        {permission_overwrite.target_id: permission_overwrite for permission_overwrite in new_permission_overwrites},
    )
    vampytest.assert_eq(channel_metadata.position, new_position)
    vampytest.assert_eq(channel_metadata.bitrate, new_bitrate)
    vampytest.assert_eq(channel_metadata.region, new_region)
    vampytest.assert_eq(channel_metadata.user_limit, new_user_limit)
    vampytest.assert_eq(channel_metadata.nsfw, new_nsfw)
    vampytest.assert_eq(channel_metadata.video_quality_mode, new_video_quality_mode)
    
    vampytest.assert_in('parent_id', old_attributes)
    vampytest.assert_in('name', old_attributes)
    vampytest.assert_in('permission_overwrites', old_attributes)
    vampytest.assert_in('position', old_attributes)
    vampytest.assert_in('bitrate', old_attributes)
    vampytest.assert_in('region', old_attributes)
    vampytest.assert_in('user_limit', old_attributes)
    vampytest.assert_in('nsfw', old_attributes)
    vampytest.assert_in('video_quality_mode', old_attributes)
    
    vampytest.assert_eq(old_attributes['parent_id'], old_parent_id)
    vampytest.assert_eq(old_attributes['name'], old_name)
    vampytest.assert_eq(
        old_attributes['permission_overwrites'],
        {permission_overwrite.target_id: permission_overwrite for permission_overwrite in old_permission_overwrites},
    )
    vampytest.assert_eq(old_attributes['position'], old_position)
    vampytest.assert_eq(old_attributes['bitrate'], old_bitrate)
    vampytest.assert_eq(old_attributes['region'], old_region)
    vampytest.assert_eq(old_attributes['user_limit'], old_user_limit)
    vampytest.assert_eq(old_attributes['nsfw'], old_nsfw)
    vampytest.assert_eq(old_attributes['video_quality_mode'], old_video_quality_mode)


def test__ChannelMetadataGuildVoice__from_partial_data():
    """
    Tests whether ``ChannelMetadataGuildVoice._from_partial_data`` works as intended.
    """
    name = 'Armelyrics'
    
    channel_metadata = ChannelMetadataGuildVoice._from_partial_data({
        'name': name,
    })
    _assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.name, name)
