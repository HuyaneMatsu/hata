import vampytest

from ....guild import VoiceRegion
from ....permission import PermissionOverwrite, PermissionOverwriteTargetType

from .. import ChannelMetadataGuildStage

from .test__ChannelMetadataGuildStage__constructor import assert_fields_set


def test__ChannelMetadataGuildStage__from_data():
    """
    Tests whether ``ChannelMetadataGuildStage.from_data` works as intended.
    """
    parent_id = 202209170173
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170174, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    bitrate = 50000
    region = VoiceRegion.brazil
    user_limit = 4
    topic = 'crimson'
    
    channel_metadata = ChannelMetadataGuildStage.from_data({
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
        'topic': topic,
    })
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildStage)
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


def test__ChannelMetadataGuildStage__to_data():
    """
    Tests whether ``ChannelMetadataGuildStage.to_data`` works as intended.
    """
    parent_id = 202209170176
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170175, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    bitrate = 50000
    region = VoiceRegion.brazil
    user_limit = 4
    topic = 'crimson'
    
    channel_metadata = ChannelMetadataGuildStage({
        'parent_id': parent_id,
        'name': name,
        'permission_overwrites': permission_overwrites,
        'position': position,
        'bitrate': bitrate,
        'region': region,
        'user_limit': user_limit,
        'topic': topic,
    })
    
    data = channel_metadata.to_data()
    
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
            'topic': topic,
        },
    )


def test__ChannelMetadataGuildStage__update_attributes():
    """
    Tests whether ``ChannelMetadataGuildStage._update_attributes`` works as intended.
    """
    old_parent_id = 202209170178
    new_parent_id = 202209170177
    old_name = 'Armelyrics'
    new_name = 'Okuu'
    old_permission_overwrites = [
        PermissionOverwrite(202209170179, target_type = PermissionOverwriteTargetType.user)
    ]
    new_permission_overwrites = [
        PermissionOverwrite(202209170180, target_type = PermissionOverwriteTargetType.role)
    ]
    old_position = 7
    new_position = 5
    old_bitrate = 50000
    new_bitrate = 60000
    old_region = VoiceRegion.brazil
    new_region = VoiceRegion.india
    old_user_limit = 4
    new_user_limit = 5
    old_topic = 'crimson'
    new_topic = 'sky'
    
    channel_metadata = ChannelMetadataGuildStage({
        'parent_id': old_parent_id,
        'name': old_name,
        'permission_overwrites': old_permission_overwrites,
        'position': old_position,
        'bitrate': old_bitrate,
        'region': old_region,
        'user_limit': old_user_limit,
        'topic': old_topic,
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
        'topic': new_topic,
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
    vampytest.assert_eq(channel_metadata.topic, new_topic)



def test__ChannelMetadataGuildStage__difference_update_attributes():
    """
    Tests whether ``ChannelMetadataGuildStage._difference_update_attributes`` works as intended.
    """
    old_parent_id = 202209170181
    new_parent_id = 202209170182
    old_name = 'Armelyrics'
    new_name = 'Okuu'
    old_permission_overwrites = [
        PermissionOverwrite(202209170183, target_type = PermissionOverwriteTargetType.user)
    ]
    new_permission_overwrites = [
        PermissionOverwrite(202209170184, target_type = PermissionOverwriteTargetType.role)
    ]
    old_position = 7
    new_position = 5
    old_bitrate = 50000
    new_bitrate = 60000
    old_region = VoiceRegion.brazil
    new_region = VoiceRegion.india
    old_user_limit = 4
    new_user_limit = 5
    old_topic = 'crimson'
    new_topic = 'sky'
    
    channel_metadata = ChannelMetadataGuildStage({
        'parent_id': str(old_parent_id),
        'name': old_name,
        'permission_overwrites': old_permission_overwrites,
        'position': old_position,
        'bitrate': old_bitrate,
        'region': old_region,
        'user_limit': old_user_limit,
        'topic': old_topic,
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
        'topic': new_topic,
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
    vampytest.assert_eq(channel_metadata.topic, new_topic)
    
    vampytest.assert_in('parent_id', old_attributes)
    vampytest.assert_in('name', old_attributes)
    vampytest.assert_in('permission_overwrites', old_attributes)
    vampytest.assert_in('position', old_attributes)
    vampytest.assert_in('bitrate', old_attributes)
    vampytest.assert_in('region', old_attributes)
    vampytest.assert_in('user_limit', old_attributes)
    vampytest.assert_in('topic', old_attributes)
    
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
    vampytest.assert_eq(old_attributes['topic'], old_topic)


def test__ChannelMetadataGuildStage__from_partial_data():
    """
    Tests whether ``ChannelMetadataGuildStage._from_partial_data`` works as intended.
    """
    name = 'Armelyrics'
    
    channel_metadata = ChannelMetadataGuildStage._from_partial_data({
        'name': name,
    })
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildStage)
    assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.name, name)
