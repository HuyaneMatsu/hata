import vampytest

from ....guild import VoiceRegion
from ....permission import PermissionOverwrite, PermissionOverwriteTargetType

from .. import ChannelMetadataGuildStage


def assert_fields_set(channel_metadata):
    vampytest.assert_instance(channel_metadata.parent_id, int)
    vampytest.assert_instance(channel_metadata.name, str)
    vampytest.assert_instance(channel_metadata._permission_cache, dict, nullable = True)
    vampytest.assert_instance(channel_metadata.permission_overwrites, dict, nullable = True)
    vampytest.assert_instance(channel_metadata.position, int)
    vampytest.assert_instance(channel_metadata.bitrate, int)
    vampytest.assert_instance(channel_metadata.region, VoiceRegion, nullable = True)
    vampytest.assert_instance(channel_metadata.user_limit, int)
    vampytest.assert_instance(channel_metadata.topic, str, nullable = True)


def test__ChannelMetadataGuildStage__new__0():
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
    
    keyword_parameters = {
        'parent_id': parent_id,
        'name': name,
        'permission_overwrites': permission_overwrites,
        'position': position,
        'bitrate': bitrate,
        'region': region,
        'user_limit': user_limit,
        'topic': topic,
    }
    channel_metadata = ChannelMetadataGuildStage(keyword_parameters)
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildStage)
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
    vampytest.assert_eq(channel_metadata.topic, topic)


def test__ChannelMetadataGuildStage__new__1():
    """
    Tests whether ``ChannelMetadataGuildStage.__new__`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    channel_metadata = ChannelMetadataGuildStage(keyword_parameters)
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildStage)
    vampytest.assert_eq(keyword_parameters, {})
    
    assert_fields_set(channel_metadata)


def test__ChannelMetadataGuildStage__create_empty():
    """
    Tests whether ``ChannelMetadataGuildStage._create_empty`` works as intended.
    """
    channel_metadata = ChannelMetadataGuildStage._create_empty()
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildStage)
    
    assert_fields_set(channel_metadata)



def test__ChannelMetadataGuildStage__precreate__0():
    """
    Tests whether ``ChannelMetadataGuildStage.precreate`` works as intended.
    
    Case: all fields given.
    """
    parent_id = 202209170169
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170170, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    bitrate = 50000
    region = VoiceRegion.brazil
    user_limit = 4
    topic = 'crimson'
    
    keyword_parameters = {
        'parent_id': parent_id,
        'name': name,
        'permission_overwrites': permission_overwrites,
        'position': position,
        'bitrate': bitrate,
        'region': region,
        'user_limit': user_limit,
        'topic': topic,
    }
    
    channel_metadata = ChannelMetadataGuildStage.precreate(keyword_parameters)
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildStage)
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
    vampytest.assert_eq(channel_metadata.topic, topic)


def test__ChannelMetadataGuildStage__precreate__1():
    """
    Tests whether ``ChannelMetadataGuildStage.precreate`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    channel_metadata = ChannelMetadataGuildStage.precreate(keyword_parameters)
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildStage)
    vampytest.assert_eq(keyword_parameters, {})
    
    assert_fields_set(channel_metadata)
