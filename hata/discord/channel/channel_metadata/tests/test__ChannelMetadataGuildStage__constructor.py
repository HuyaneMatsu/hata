from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...permission_overwrite import PermissionOverwrite, PermissionOverwriteTargetType

from ..guild_stage import ChannelMetadataGuildStage
from ..preinstanced import VoiceRegion


def _assert_fields_set(channel_metadata):
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildStage)
    
    vampytest.assert_instance(channel_metadata.parent_id, int)
    vampytest.assert_instance(channel_metadata.name, str)
    vampytest.assert_instance(channel_metadata._cache_permission, dict, nullable = True)
    vampytest.assert_instance(channel_metadata.permission_overwrites, dict, nullable = True)
    vampytest.assert_instance(channel_metadata.position, int)
    vampytest.assert_instance(channel_metadata.bitrate, int)
    vampytest.assert_instance(channel_metadata.region, VoiceRegion, nullable = True)
    vampytest.assert_instance(channel_metadata.user_limit, int)
    vampytest.assert_instance(channel_metadata.topic, str, nullable = True)
    vampytest.assert_instance(channel_metadata.voice_engaged_since, DateTime, nullable = True)


def test__ChannelMetadataGuildStage__new__no_fields():
    """
    Tests whether ``ChannelMetadataGuildStage.__new__`` works as intended.
    
    Case: no fields given.
    """
    channel_metadata = ChannelMetadataGuildStage()
    _assert_fields_set(channel_metadata)


def test__ChannelMetadataGuildStage__new__all_fields():
    """
    Tests whether ``ChannelMetadataGuildStage.__new__`` works as intended.
    
    Case: all fields given.
    """
    parent_id = 202209170172
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170171, target_type = PermissionOverwriteTargetType.user)
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
    vampytest.assert_eq(channel_metadata.topic, topic)
    vampytest.assert_eq(channel_metadata.voice_engaged_since, voice_engaged_since)


def test__ChannelMetadataGuildStage__from_keyword_parameters__no_fields():
    """
    Tests whether ``ChannelMetadataGuildStage.from_keyword_parameters`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    channel_metadata = ChannelMetadataGuildStage.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(channel_metadata)
    vampytest.assert_eq(keyword_parameters, {})


def test__ChannelMetadataGuildStage__from_keyword_parameters__all_fields():
    """
    Tests whether ``ChannelMetadataGuildStage.from_keyword_parameters`` works as intended.
    
    Case: all fields given.
    """
    parent_id = 202304110012
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202304110013, target_type = PermissionOverwriteTargetType.user)
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
    channel_metadata = ChannelMetadataGuildStage.from_keyword_parameters(keyword_parameters)
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
    vampytest.assert_eq(channel_metadata.user_limit, user_limit)
    vampytest.assert_eq(channel_metadata.topic, topic)
    vampytest.assert_eq(channel_metadata.voice_engaged_since, voice_engaged_since)


def test__ChannelMetadataGuildStage__create_empty():
    """
    Tests whether ``ChannelMetadataGuildStage._create_empty`` works as intended.
    """
    channel_metadata = ChannelMetadataGuildStage._create_empty()
    _assert_fields_set(channel_metadata)
