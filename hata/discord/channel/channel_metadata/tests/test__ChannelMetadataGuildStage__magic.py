from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...permission_overwrite import PermissionOverwrite, PermissionOverwriteTargetType

from ..preinstanced import VoiceRegion

from ..guild_stage import ChannelMetadataGuildStage


def test__ChannelMetadataGuildStage__repr():
    """
    Tests whether ``.ChannelMetadataGuildStage.__repr__`` works as intended.
    """
    parent_id = 202209170140
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170185, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    bitrate = 50000
    region = VoiceRegion.brazil
    user_limit = 4
    topic = 'crimson'
    voice_engaged_since = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    channel_metadata = ChannelMetadataGuildStage(
        parent_id = parent_id,
        name = name,
        permission_overwrites = permission_overwrites,
        position = position,
        bitrate = bitrate,
        region = region,
        user_limit = user_limit,
        topic = topic,
        voice_engaged_since = voice_engaged_since,
    )
    
    vampytest.assert_instance(repr(channel_metadata), str)



def test__ChannelMetadataGuildStage__hash():
    """
    Tests whether ``.ChannelMetadataGuildStage.__hash__`` works as intended.
    """
    parent_id = 2022091800094
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209180095, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    bitrate = 50000
    region = VoiceRegion.brazil
    user_limit = 4
    topic = 'crimson'
    voice_engaged_since = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    channel_metadata = ChannelMetadataGuildStage(
        parent_id = parent_id,
        name = name,
        permission_overwrites = permission_overwrites,
        position = position,
        bitrate = bitrate,
        region = region,
        user_limit = user_limit,
        topic = topic,
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
    topic = 'crimson'
    voice_engaged_since = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    keyword_parameters = {
        'parent_id': parent_id,
        'name': name,
        'permission_overwrites': permission_overwrites,
        'position': position,
        'bitrate': bitrate,
        'region': region,
        'user_limit': user_limit,
        'topic': topic,
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
            'topic': 'sky',
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
def test__ChannelMetadataGuildStage__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ChannelMetadataGuildStage.__eq__`` works as intended.
    
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
    channel_metadata_0 = ChannelMetadataGuildStage(**keyword_parameters_0)
    channel_metadata_1 = ChannelMetadataGuildStage(**keyword_parameters_1)
    
    output = channel_metadata_0 == channel_metadata_1
    vampytest.assert_instance(output, bool)
    return output
