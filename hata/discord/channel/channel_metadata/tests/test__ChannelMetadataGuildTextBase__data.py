import vampytest

from ....permission import PermissionOverwrite, PermissionOverwriteTargetType

from ..guild_text_base import ChannelMetadataGuildTextBase

from .test__ChannelMetadataGuildTextBase__constructor import assert_fields_set


def test__ChannelMetadataGuildTextBase__from_data():
    """
    Tests whether ``ChannelMetadataGuildTextBase.from_data` works as intended.
    """
    parent_id = 202209170194
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170195, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    default_thread_auto_archive_after = 86400
    default_thread_slowmode = 60
    nsfw = True
    slowmode = 30
    topic = 'rin'
    
    channel_metadata = ChannelMetadataGuildTextBase.from_data({
        'parent_id': str(parent_id),
        'name': name,
        'permission_overwrites': [
            permission_overwrite.to_data(include_internals = True)
            for permission_overwrite in permission_overwrites
        ],
        'position': position,
        'default_auto_archive_duration': default_thread_auto_archive_after // 60,
        'default_thread_rate_limit_per_user': default_thread_slowmode,
        'nsfw': nsfw,
        'rate_limit_per_user': slowmode,
        'topic': topic
    })
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildTextBase)
    assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.parent_id, parent_id)
    vampytest.assert_eq(channel_metadata.name, name)
    vampytest.assert_eq(
        channel_metadata.permission_overwrites,
        {permission_overwrite.target_id: permission_overwrite for permission_overwrite in permission_overwrites},
    )
    vampytest.assert_eq(channel_metadata.position, position)
    vampytest.assert_eq(channel_metadata.default_thread_auto_archive_after, default_thread_auto_archive_after)
    vampytest.assert_eq(channel_metadata.default_thread_slowmode, default_thread_slowmode)
    vampytest.assert_eq(channel_metadata.nsfw, nsfw)
    vampytest.assert_eq(channel_metadata.slowmode, slowmode)
    vampytest.assert_eq(channel_metadata.topic, topic)


def test__ChannelMetadataGuildTextBase__to_data():
    """
    Tests whether ``ChannelMetadataGuildTextBase.to_data`` works as intended.
    
    Case: include defaults and internals.
    """
    parent_id = 202209170196
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170197, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    default_thread_auto_archive_after = 86400
    default_thread_slowmode = 60
    nsfw = True
    slowmode = 30
    topic = 'rin'
    
    channel_metadata = ChannelMetadataGuildTextBase({
        'parent_id': parent_id,
        'name': name,
        'permission_overwrites': permission_overwrites,
        'position': position,
        'default_thread_auto_archive_after': default_thread_auto_archive_after,
        'default_thread_slowmode': default_thread_slowmode,
        'nsfw': nsfw,
        'slowmode': slowmode,
        'topic': topic,
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
            'default_auto_archive_duration': default_thread_auto_archive_after // 60,
            'default_thread_rate_limit_per_user': default_thread_slowmode,
            'nsfw': nsfw,
            'rate_limit_per_user': slowmode,
            'topic': topic,
        },
    )


def test__ChannelMetadataGuildTextBase__update_attributes():
    """
    Tests whether ``ChannelMetadataGuildTextBase._update_attributes`` works as intended.
    """
    old_parent_id = 202209170198
    new_parent_id = 202209170199
    old_name = 'Armelyrics'
    new_name = 'Okuu'
    old_permission_overwrites = [
        PermissionOverwrite(202209170200, target_type = PermissionOverwriteTargetType.user)
    ]
    new_permission_overwrites = [
        PermissionOverwrite(202209170201, target_type = PermissionOverwriteTargetType.role)
    ]
    old_position = 7
    new_position = 5
    old_default_thread_auto_archive_after = 86400
    new_default_thread_auto_archive_after = 3600
    old_default_thread_slowmode = 60
    new_default_thread_slowmode = 69
    old_nsfw = True
    new_nsfw = False
    old_slowmode = 30
    new_slowmode = 33
    old_topic = 'rin'
    new_topic = 'orin'
    
    channel_metadata = ChannelMetadataGuildTextBase({
        'parent_id': old_parent_id,
        'name': old_name,
        'permission_overwrites': old_permission_overwrites,
        'position': old_position,
        'default_thread_auto_archive_after': old_default_thread_auto_archive_after,
        'default_thread_slowmode': old_default_thread_slowmode,
        'nsfw': old_nsfw,
        'slowmode': old_slowmode,
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
        'default_auto_archive_duration': new_default_thread_auto_archive_after // 60,
        'default_thread_rate_limit_per_user': new_default_thread_slowmode,
        'nsfw': new_nsfw,
        'rate_limit_per_user': new_slowmode,
        'topic': new_topic,
    })
    
    vampytest.assert_eq(channel_metadata.parent_id, new_parent_id)
    vampytest.assert_eq(channel_metadata.name, new_name)
    vampytest.assert_eq(
        channel_metadata.permission_overwrites,
        {permission_overwrite.target_id: permission_overwrite for permission_overwrite in new_permission_overwrites},
    )
    vampytest.assert_eq(channel_metadata.position, new_position)
    vampytest.assert_eq(channel_metadata.default_thread_auto_archive_after, new_default_thread_auto_archive_after)
    vampytest.assert_eq(channel_metadata.default_thread_slowmode, new_default_thread_slowmode)
    vampytest.assert_eq(channel_metadata.nsfw, new_nsfw)
    vampytest.assert_eq(channel_metadata.slowmode, new_slowmode)
    vampytest.assert_eq(channel_metadata.topic, new_topic)


def test__ChannelMetadataGuildTextBase__difference_update_attributes():
    """
    Tests whether ``ChannelMetadataGuildTextBase._difference_update_attributes`` works as intended.
    """
    old_parent_id = 202209170202
    new_parent_id = 202209170203
    old_name = 'Armelyrics'
    new_name = 'Okuu'
    old_permission_overwrites = [
        PermissionOverwrite(202209170204, target_type = PermissionOverwriteTargetType.user)
    ]
    new_permission_overwrites = [
        PermissionOverwrite(202209170205, target_type = PermissionOverwriteTargetType.role)
    ]
    old_position = 7
    new_position = 5
    old_default_thread_auto_archive_after = 86400
    new_default_thread_auto_archive_after = 3600
    old_default_thread_slowmode = 60
    new_default_thread_slowmode = 69
    old_nsfw = True
    new_nsfw = False
    old_slowmode = 30
    new_slowmode = 33
    old_topic = 'rin'
    new_topic = 'orin'
    
    channel_metadata = ChannelMetadataGuildTextBase({
        'parent_id': str(old_parent_id),
        'name': old_name,
        'permission_overwrites': old_permission_overwrites,
        'position': old_position,
        'default_thread_auto_archive_after': old_default_thread_auto_archive_after,
        'default_thread_slowmode': old_default_thread_slowmode,
        'nsfw': old_nsfw,
        'slowmode': old_slowmode,
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
        'default_auto_archive_duration': new_default_thread_auto_archive_after // 60,
        'default_thread_rate_limit_per_user': new_default_thread_slowmode,
        'nsfw': new_nsfw,
        'rate_limit_per_user': new_slowmode,
        'topic': new_topic,
    })

    vampytest.assert_eq(channel_metadata.parent_id, new_parent_id)
    vampytest.assert_eq(channel_metadata.name, new_name)
    vampytest.assert_eq(
        channel_metadata.permission_overwrites,
        {permission_overwrite.target_id: permission_overwrite for permission_overwrite in new_permission_overwrites},
    )
    vampytest.assert_eq(channel_metadata.position, new_position)
    vampytest.assert_eq(channel_metadata.default_thread_auto_archive_after, new_default_thread_auto_archive_after)
    vampytest.assert_eq(channel_metadata.default_thread_slowmode, new_default_thread_slowmode)
    vampytest.assert_eq(channel_metadata.nsfw, new_nsfw)
    vampytest.assert_eq(channel_metadata.slowmode, new_slowmode)
    vampytest.assert_eq(channel_metadata.topic, new_topic)
    
    vampytest.assert_in('parent_id', old_attributes)
    vampytest.assert_in('name', old_attributes)
    vampytest.assert_in('permission_overwrites', old_attributes)
    vampytest.assert_in('position', old_attributes)
    vampytest.assert_in('default_thread_auto_archive_after', old_attributes)
    vampytest.assert_in('default_thread_slowmode', old_attributes)
    vampytest.assert_in('nsfw', old_attributes)
    vampytest.assert_in('slowmode', old_attributes)
    vampytest.assert_in('topic', old_attributes)
    
    vampytest.assert_eq(old_attributes['parent_id'], old_parent_id)
    vampytest.assert_eq(old_attributes['name'], old_name)
    vampytest.assert_eq(
        old_attributes['permission_overwrites'],
        {permission_overwrite.target_id: permission_overwrite for permission_overwrite in old_permission_overwrites},
    )
    vampytest.assert_eq(old_attributes['position'], old_position)
    vampytest.assert_eq(old_attributes['default_thread_auto_archive_after'], old_default_thread_auto_archive_after)
    vampytest.assert_eq(old_attributes['default_thread_slowmode'], old_default_thread_slowmode)
    vampytest.assert_eq(old_attributes['nsfw'], old_nsfw)
    vampytest.assert_eq(old_attributes['slowmode'], old_slowmode)
    vampytest.assert_eq(old_attributes['topic'], old_topic)


def test__ChannelMetadataGuildTextBase__from_partial_data():
    """
    Tests whether ``ChannelMetadataGuildTextBase._from_partial_data`` works as intended.
    """
    name = 'Armelyrics'
    
    channel_metadata = ChannelMetadataGuildTextBase._from_partial_data({
        'name': name,
    })
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildTextBase)
    assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.name, name)
