from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...permission_overwrite import PermissionOverwrite, PermissionOverwriteTargetType

from ..preinstanced import VideoQualityMode, VoiceRegion

from ..guild_voice import ChannelMetadataGuildVoice


def _assert_fields_set(channel_metadata):
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildVoice)
    
    vampytest.assert_instance(channel_metadata.parent_id, int)
    vampytest.assert_instance(channel_metadata.name, str)
    vampytest.assert_instance(channel_metadata._cache_permission, dict, nullable = True)
    vampytest.assert_instance(channel_metadata.permission_overwrites, dict, nullable = True)
    vampytest.assert_instance(channel_metadata.position, int)
    vampytest.assert_instance(channel_metadata.bitrate, int)
    vampytest.assert_instance(channel_metadata.region, VoiceRegion, nullable = True)
    vampytest.assert_instance(channel_metadata.status, str, nullable = True)
    vampytest.assert_instance(channel_metadata.user_limit, int)
    vampytest.assert_instance(channel_metadata.nsfw, bool)
    vampytest.assert_instance(channel_metadata.video_quality_mode, VideoQualityMode)
    vampytest.assert_instance(channel_metadata.voice_engaged_since, DateTime, nullable = True)


def test__ChannelMetadataGuildVoice__new__no_fields():
    """
    Tests whether ``ChannelMetadataGuildVoice.__new__`` works as intended.
    
    Case: no fields given.
    """
    channel_metadata = ChannelMetadataGuildVoice()
    _assert_fields_set(channel_metadata)


def test__ChannelMetadataGuildVoice__new__all_fields():
    """
    Tests whether ``ChannelMetadataGuildVoice.__new__`` works as intended.
    
    Case: all fields given.
    """
    parent_id = 202209170145
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170148, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    bitrate = 50000
    region = VoiceRegion.brazil
    status = 'koishi love'
    user_limit = 4
    nsfw = True
    video_quality_mode = VideoQualityMode.auto
    voice_engaged_since = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    channel_metadata = ChannelMetadataGuildVoice(
        parent_id = parent_id,
        name = name,
        permission_overwrites = permission_overwrites,
        position = position,
        bitrate = bitrate,
        region = region,
        status = status,
        user_limit = user_limit,
        nsfw = nsfw,
        video_quality_mode = video_quality_mode,
        voice_engaged_since = voice_engaged_since,
    )
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
    vampytest.assert_eq(channel_metadata.status, status)
    vampytest.assert_eq(channel_metadata.user_limit, user_limit)
    vampytest.assert_eq(channel_metadata.nsfw, nsfw)
    vampytest.assert_is(channel_metadata.video_quality_mode, video_quality_mode)
    vampytest.assert_eq(channel_metadata.voice_engaged_since, voice_engaged_since)


def test__ChannelMetadataGuildVoice__from_keyword_parameters__no_fields():
    """
    Tests whether ``ChannelMetadataGuildVoice.from_keyword_parameters`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    channel_metadata = ChannelMetadataGuildVoice.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(channel_metadata)
    vampytest.assert_eq(keyword_parameters, {})


def test__ChannelMetadataGuildVoice__from_keyword_parameters__all_fields():
    """
    Tests whether ``ChannelMetadataGuildVoice.from_keyword_parameters`` works as intended.
    
    Case: all fields given.
    """
    parent_id = 202304110024
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202304110025, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    bitrate = 50000
    region = VoiceRegion.brazil
    user_limit = 4
    status = 'koishi love'
    nsfw = True
    video_quality_mode = VideoQualityMode.auto
    voice_engaged_since = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    keyword_parameters = {
        'parent_id': parent_id,
        'name': name,
        'permission_overwrites': permission_overwrites,
        'position': position,
        'bitrate': bitrate,
        'region': region,
        'status': status,
        'user_limit': user_limit,
        'nsfw': nsfw,
        'video_quality_mode': video_quality_mode,
        'voice_engaged_since': voice_engaged_since,
    }
    channel_metadata = ChannelMetadataGuildVoice.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(channel_metadata)
    vampytest.assert_eq(keyword_parameters, {})
    
    vampytest.assert_eq(channel_metadata.parent_id, parent_id)
    vampytest.assert_eq(channel_metadata.name, name)
    vampytest.assert_eq(
        channel_metadata.permission_overwrites,
        {permission_overwrite.target_id: permission_overwrite for permission_overwrite in permission_overwrites},
    )
    vampytest.assert_eq(channel_metadata.position, position)
    vampytest.assert_eq(channel_metadata.bitrate, bitrate)
    vampytest.assert_eq(channel_metadata.region, region)
    vampytest.assert_eq(channel_metadata.status, status)
    vampytest.assert_eq(channel_metadata.user_limit, user_limit)
    vampytest.assert_eq(channel_metadata.nsfw, nsfw)
    vampytest.assert_is(channel_metadata.video_quality_mode, video_quality_mode)
    vampytest.assert_eq(channel_metadata.voice_engaged_since, voice_engaged_since)


def test__ChannelMetadataGuildVoice__create_empty():
    """
    Tests whether ``ChannelMetadataGuildVoice._create_empty`` works as intended.
    """
    channel_metadata = ChannelMetadataGuildVoice._create_empty()
    _assert_fields_set(channel_metadata)
