import vampytest

from ....guild import VoiceRegion
from ....permission import PermissionOverwrite, PermissionOverwriteTargetType

from ...preinstanced import VideoQualityMode

from .. import ChannelMetadataGuildVoice


def test__ChannelMetadataGuildVoice__repr():
    """
    Tests whether ``.ChannelMetadataGuildVoice.__repr__`` works as intended.
    """
    parent_id = 202209170163
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170164, target_type = PermissionOverwriteTargetType.user)
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
    
    vampytest.assert_instance(repr(channel_metadata), str)


def test__ChannelMetadataGuildVoice__hash():
    """
    Tests whether ``.ChannelMetadataGuildVoice.__hash__`` works as intended.
    """
    parent_id = 202209180111
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209180112, target_type = PermissionOverwriteTargetType.user)
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
    
    vampytest.assert_instance(hash(channel_metadata), int)


def test__ChannelMetadataGuildVoice__eq():
    """
    Tests whether ``.ChannelMetadataGuildVoice.__eq__`` works as intended.
    """
    parent_id = 202209170165
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170166, target_type = PermissionOverwriteTargetType.user)
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
    
    vampytest.assert_eq(channel_metadata, channel_metadata)
    vampytest.assert_ne(channel_metadata, object())
    
    for field_name, field_value in (
        ('parent_id', 202209170167),
        ('name', 'Okuu'),
        (
            'permission_overwrites',
            [
                PermissionOverwrite(202209170168, target_type = PermissionOverwriteTargetType.role)
            ],
        ),
        ('position', 6),
        ('bitrate', 60000),
        ('region', VoiceRegion.india),
        ('user_limit', 5),
        ('nsfw', False),
        ('video_quality_mode', VideoQualityMode.full)
    ):
        test_channel_metadata = ChannelMetadataGuildVoice({**keyword_parameters, field_name: field_value})
        
        vampytest.assert_ne(channel_metadata, test_channel_metadata)
