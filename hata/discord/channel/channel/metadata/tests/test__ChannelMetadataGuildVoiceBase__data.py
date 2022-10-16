import vampytest

from .....permission import PermissionOverwrite, PermissionOverwriteTargetType

from ...preinstanced import VoiceRegion

from ..guild_voice_base import ChannelMetadataGuildVoiceBase

from .test__ChannelMetadataGuildVoiceBase__constructor import assert_fields_set


def test__ChannelMetadataGuildVoiceBase__from_data():
    """
    Tests whether ``ChannelMetadataGuildVoiceBase.from_data` works as intended.
    """
    parent_id = 202209170128
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170129, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    bitrate = 50000
    region = VoiceRegion.brazil
    user_limit = 4
    
    channel_metadata = ChannelMetadataGuildVoiceBase.from_data({
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
    })
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildVoiceBase)
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


def test__ChannelMetadataGuildVoiceBase__to_data():
    """
    Tests whether ``ChannelMetadataGuildVoiceBase.to_data`` works as intended.
    
    Case: include defaults and internals.
    """
    parent_id = 202209170130
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170131, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    bitrate = 50000
    region = VoiceRegion.brazil
    user_limit = 4
    
    channel_metadata = ChannelMetadataGuildVoiceBase({
        'parent_id': parent_id,
        'name': name,
        'permission_overwrites': permission_overwrites,
        'position': position,
        'bitrate': bitrate,
        'region': region,
        'user_limit': user_limit,
    })
    
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
        },
    )


def test__ChannelMetadataGuildVoiceBase__update_attributes():
    """
    Tests whether ``ChannelMetadataGuildVoiceBase._update_attributes`` works as intended.
    """
    old_parent_id = 202209170132
    new_parent_id = 202209170133
    old_name = 'Armelyrics'
    new_name = 'Okuu'
    old_permission_overwrites = [
        PermissionOverwrite(202209170134, target_type = PermissionOverwriteTargetType.user)
    ]
    new_permission_overwrites = [
        PermissionOverwrite(202209170135, target_type = PermissionOverwriteTargetType.role)
    ]
    old_position = 7
    new_position = 5
    old_bitrate = 50000
    new_bitrate = 60000
    old_region = VoiceRegion.brazil
    new_region = VoiceRegion.india
    old_user_limit = 4
    new_user_limit = 5
    
    channel_metadata = ChannelMetadataGuildVoiceBase({
        'parent_id': old_parent_id,
        'name': old_name,
        'permission_overwrites': old_permission_overwrites,
        'position': old_position,
        'bitrate': old_bitrate,
        'region': old_region,
        'user_limit': old_user_limit,
    })
    
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



def test__ChannelMetadataGuildVoiceBase__difference_update_attributes():
    """
    Tests whether ``ChannelMetadataGuildVoiceBase._difference_update_attributes`` works as intended.
    """
    old_parent_id = 202209170136
    new_parent_id = 202209170137
    old_name = 'Armelyrics'
    new_name = 'Okuu'
    old_permission_overwrites = [
        PermissionOverwrite(202209170138, target_type = PermissionOverwriteTargetType.user)
    ]
    new_permission_overwrites = [
        PermissionOverwrite(202209170139, target_type = PermissionOverwriteTargetType.role)
    ]
    old_position = 7
    new_position = 5
    old_bitrate = 50000
    new_bitrate = 60000
    old_region = VoiceRegion.brazil
    new_region = VoiceRegion.india
    old_user_limit = 4
    new_user_limit = 5
    
    channel_metadata = ChannelMetadataGuildVoiceBase({
        'parent_id': str(old_parent_id),
        'name': old_name,
        'permission_overwrites': old_permission_overwrites,
        'position': old_position,
        'bitrate': old_bitrate,
        'region': old_region,
        'user_limit': old_user_limit,
    })
    
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
    
    vampytest.assert_in('parent_id', old_attributes)
    vampytest.assert_in('name', old_attributes)
    vampytest.assert_in('permission_overwrites', old_attributes)
    vampytest.assert_in('position', old_attributes)
    vampytest.assert_in('bitrate', old_attributes)
    vampytest.assert_in('region', old_attributes)
    vampytest.assert_in('user_limit', old_attributes)
    
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


def test__ChannelMetadataGuildVoiceBase__from_partial_data():
    """
    Tests whether ``ChannelMetadataGuildVoiceBase._from_partial_data`` works as intended.
    """
    name = 'Armelyrics'
    
    channel_metadata = ChannelMetadataGuildVoiceBase._from_partial_data({
        'name': name,
    })
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildVoiceBase)
    assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.name, name)
