from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...permission_overwrite import PermissionOverwrite, PermissionOverwriteTargetType

from ..preinstanced import VideoQualityMode, VoiceRegion

from ..guild_voice import ChannelMetadataGuildVoice


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
    status = 'koishi love'
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
    
    vampytest.assert_instance(hash(channel_metadata), int)



def _iter_options__eq():
    parent_id = 202209170142
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170143, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    bitrate = 50000
    region = VoiceRegion.brazil
    user_limit = 4
    video_quality_mode = VideoQualityMode.auto
    voice_engaged_since = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    keyword_parameters = {
        'parent_id': parent_id,
        'name': name,
        'permission_overwrites': permission_overwrites,
        'position': position,
        'bitrate': bitrate,
        'region': region,
        'user_limit': user_limit,
        'video_quality_mode': video_quality_mode,
        'voice_engaged_since': voice_engaged_since,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'parent_id': 202209170144,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'name': 'Okuu',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'permission_overwrites': [
                PermissionOverwrite(202209170146, target_type = PermissionOverwriteTargetType.role)
            ],
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'position': 61,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'bitrate': 60000,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'region':  VoiceRegion.india,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'user_limit': 5,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'video_quality_mode': VideoQualityMode.full,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'voice_engaged_since': DateTime(2016, 5, 18, tzinfo = TimeZone.utc),
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__ChannelMetadataGuildVoice__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ChannelMetadataGuildVoice.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    channel_metadata_0 = ChannelMetadataGuildVoice(**keyword_parameters_0)
    channel_metadata_1 = ChannelMetadataGuildVoice(**keyword_parameters_1)
    
    output = channel_metadata_0 == channel_metadata_1
    vampytest.assert_instance(output, bool)
    return output
