import vampytest

from ...permission_overwrite import PermissionOverwrite, PermissionOverwriteTargetType

from ..guild_voice_base import ChannelMetadataGuildVoiceBase
from ..preinstanced import VoiceRegion


def _assert_fields_set(channel_metadata):
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildVoiceBase)
    
    vampytest.assert_instance(channel_metadata.parent_id, int)
    vampytest.assert_instance(channel_metadata.name, str)
    vampytest.assert_instance(channel_metadata._cache_permission, dict, nullable = True)
    vampytest.assert_instance(channel_metadata.permission_overwrites, dict, nullable = True)
    vampytest.assert_instance(channel_metadata.position, int)
    vampytest.assert_instance(channel_metadata.bitrate, int)
    vampytest.assert_instance(channel_metadata.region, VoiceRegion, nullable = True)
    vampytest.assert_instance(channel_metadata.user_limit, int)


def test__ChannelMetadataGuildVoiceBase__new__0():
    """
    Tests whether ``ChannelMetadataGuildVoiceBase.__new__`` works as intended.
    
    Case: all fields given.
    """
    parent_id = 202209170124
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170125, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    bitrate = 50000
    region = VoiceRegion.brazil
    user_limit = 4
    
    channel_metadata = ChannelMetadataGuildVoiceBase(
        parent_id = parent_id,
        name = name,
        permission_overwrites = permission_overwrites,
        position = position,
        bitrate = bitrate,
        region = region,
        user_limit = user_limit,
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
    vampytest.assert_eq(channel_metadata.user_limit, user_limit)


def test__ChannelMetadataGuildVoiceBase__new__1():
    """
    Tests whether ``ChannelMetadataGuildVoiceBase.__new__`` works as intended.
    
    Case: no fields given.
    """
    channel_metadata = ChannelMetadataGuildVoiceBase()
    _assert_fields_set(channel_metadata)


def test__ChannelMetadataGuildVoiceBase__from_keyword_parameters__0():
    """
    Tests whether ``ChannelMetadataGuildVoiceBase.from_keyword_parameters`` works as intended.
    
    Case: all fields given.
    """
    parent_id = 202209170124
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170125, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    bitrate = 50000
    region = VoiceRegion.brazil
    user_limit = 4
    
    keyword_parameters = {
        'parent_id': parent_id,
        'name': name,
        'permission_overwrites': permission_overwrites,
        'position': position,
        'bitrate': bitrate,
        'region': region,
        'user_limit': user_limit,
    }
    channel_metadata = ChannelMetadataGuildVoiceBase.from_keyword_parameters(keyword_parameters)
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


def test__ChannelMetadataGuildVoiceBase__from_keyword_parameters__1():
    """
    Tests whether ``ChannelMetadataGuildVoiceBase.from_keyword_parameters`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    channel_metadata = ChannelMetadataGuildVoiceBase.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(channel_metadata)
    vampytest.assert_eq(keyword_parameters, {})


def test__ChannelMetadataGuildVoiceBase__create_empty():
    """
    Tests whether ``ChannelMetadataGuildVoiceBase._create_empty`` works as intended.
    """
    channel_metadata = ChannelMetadataGuildVoiceBase._create_empty()
    _assert_fields_set(channel_metadata)
