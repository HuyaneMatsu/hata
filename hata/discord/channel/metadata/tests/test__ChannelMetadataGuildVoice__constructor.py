import vampytest

from ....guild import VoiceRegion
from ....permission import PermissionOverwrite, PermissionOverwriteTargetType

from ...preinstanced import VideoQualityMode

from .. import ChannelMetadataGuildVoice


def assert_fields_set(channel_metadata):
    vampytest.assert_instance(channel_metadata.parent_id, int)
    vampytest.assert_instance(channel_metadata.name, str)
    vampytest.assert_instance(channel_metadata._permission_cache, dict, nullable = True)
    vampytest.assert_instance(channel_metadata.permission_overwrites, dict)
    vampytest.assert_instance(channel_metadata.position, int)
    vampytest.assert_instance(channel_metadata.bitrate, int)
    vampytest.assert_instance(channel_metadata.region, VoiceRegion, nullable = True)
    vampytest.assert_instance(channel_metadata.user_limit, int)
    vampytest.assert_instance(channel_metadata.nsfw, bool)
    vampytest.assert_instance(channel_metadata.video_quality_mode, VideoQualityMode)


def test__ChannelMetadataGuildVoice__new__0():
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
    user_limit = 4
    nsfw = True
    video_quality_mode = VideoQualityMode.auto
    
    keyword_parameters = {
        'parent_id': parent_id,
        'name': name,
        'permission_overwrites': permission_overwrites,
        'position': position,
        'bitrate': bitrate,
        'region': region,
        'user_limit': user_limit,
        'nsfw': nsfw,
        'video_quality_mode': video_quality_mode,
    }
    channel_metadata = ChannelMetadataGuildVoice(keyword_parameters)
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildVoice)
    vampytest.assert_eq(keyword_parameters, {})
    
    assert_fields_set(channel_metadata)
    
    
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


def test__ChannelMetadataGuildVoice__new__1():
    """
    Tests whether ``ChannelMetadataGuildVoice.__new__`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    channel_metadata = ChannelMetadataGuildVoice(keyword_parameters)
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildVoice)
    vampytest.assert_eq(keyword_parameters, {})
    
    assert_fields_set(channel_metadata)


def test__ChannelMetadataGuildVoice__create_empty():
    """
    Tests whether ``ChannelMetadataGuildVoice._create_empty`` works as intended.
    """
    channel_metadata = ChannelMetadataGuildVoice._create_empty()
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildVoice)
    
    assert_fields_set(channel_metadata)



def test__ChannelMetadataGuildVoice__precreate__0():
    """
    Tests whether ``ChannelMetadataGuildVoice.precreate`` works as intended.
    
    Case: all fields given.
    """
    parent_id = 202209170149
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170150, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    bitrate = 50000
    region = VoiceRegion.brazil
    user_limit = 4
    nsfw = True
    video_quality_mode = VideoQualityMode.auto
    
    keyword_parameters = {
        'parent_id': parent_id,
        'name': name,
        'permission_overwrites': permission_overwrites,
        'position': position,
        'bitrate': bitrate,
        'region': region,
        'user_limit': user_limit,
        'nsfw': nsfw,
        'video_quality_mode': video_quality_mode,
    }
    
    channel_metadata = ChannelMetadataGuildVoice.precreate(keyword_parameters)
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildVoice)
    vampytest.assert_eq(keyword_parameters, {})
    
    assert_fields_set(channel_metadata)
    
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


def test__ChannelMetadataGuildVoice__precreate__1():
    """
    Tests whether ``ChannelMetadataGuildVoice.precreate`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    channel_metadata = ChannelMetadataGuildVoice.precreate(keyword_parameters)
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildVoice)
    vampytest.assert_eq(keyword_parameters, {})
    
    assert_fields_set(channel_metadata)
