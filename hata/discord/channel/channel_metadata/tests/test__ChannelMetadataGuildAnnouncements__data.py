import vampytest

from ...permission_overwrite import PermissionOverwrite, PermissionOverwriteTargetType

from ..guild_announcements import ChannelMetadataGuildAnnouncements

from .test__ChannelMetadataGuildAnnouncements__constructor import _assert_fields_set


def test__ChannelMetadataGuildAnnouncements__from_data():
    """
    Tests whether ``ChannelMetadataGuildAnnouncements.from_data` works as intended.
    """
    parent_id = 202209170235
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170236, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    default_thread_auto_archive_after = 86400
    default_thread_slowmode = 60
    nsfw = True
    slowmode = 30
    topic = 'rin'
    
    data = {
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
    }
    
    channel_metadata = ChannelMetadataGuildAnnouncements.from_data(data)
    _assert_fields_set(channel_metadata)
    
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


def test__ChannelMetadataGuildAnnouncements__to_data():
    """
    Tests whether ``ChannelMetadataGuildAnnouncements.to_data`` works as intended.
    
    Case: include defaults and internals.
    """
    parent_id = 202209170236
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170237, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    default_thread_auto_archive_after = 86400
    default_thread_slowmode = 60
    nsfw = True
    slowmode = 30
    topic = 'rin'
    
    channel_metadata = ChannelMetadataGuildAnnouncements(
        parent_id = parent_id,
        name = name,
        permission_overwrites = permission_overwrites,
        position = position,
        default_thread_auto_archive_after = default_thread_auto_archive_after,
        default_thread_slowmode = default_thread_slowmode,
        nsfw = nsfw,
        slowmode = slowmode,
        topic = topic,
    )
    
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


def test__ChannelMetadataGuildAnnouncements__update_attributes():
    """
    Tests whether ``ChannelMetadataGuildAnnouncements._update_attributes`` works as intended.
    """
    old_parent_id = 202209170238
    new_parent_id = 202209170239
    old_name = 'Armelyrics'
    new_name = 'Okuu'
    old_permission_overwrites = [
        PermissionOverwrite(202209170240, target_type = PermissionOverwriteTargetType.user)
    ]
    new_permission_overwrites = [
        PermissionOverwrite(202209170241, target_type = PermissionOverwriteTargetType.role)
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
    
    channel_metadata = ChannelMetadataGuildAnnouncements(
        parent_id = old_parent_id,
        name = old_name,
        permission_overwrites = old_permission_overwrites,
        position = old_position,
        default_thread_auto_archive_after = old_default_thread_auto_archive_after,
        default_thread_slowmode = old_default_thread_slowmode,
        nsfw = old_nsfw,
        slowmode = old_slowmode,
        topic = old_topic,
    )
    
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


def test__ChannelMetadataGuildAnnouncements__difference_update_attributes():
    """
    Tests whether ``ChannelMetadataGuildAnnouncements._difference_update_attributes`` works as intended.
    """
    old_parent_id = 202209170242
    new_parent_id = 202209170243
    old_name = 'Armelyrics'
    new_name = 'Okuu'
    old_permission_overwrites = [
        PermissionOverwrite(202209170244, target_type = PermissionOverwriteTargetType.user)
    ]
    new_permission_overwrites = [
        PermissionOverwrite(202209170245, target_type = PermissionOverwriteTargetType.role)
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
    
    channel_metadata = ChannelMetadataGuildAnnouncements(
        parent_id = old_parent_id,
        name = old_name,
        permission_overwrites = old_permission_overwrites,
        position = old_position,
        default_thread_auto_archive_after = old_default_thread_auto_archive_after,
        default_thread_slowmode = old_default_thread_slowmode,
        nsfw = old_nsfw,
        slowmode = old_slowmode,
        topic = old_topic,
    )
    
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


def test__ChannelMetadataGuildAnnouncements__from_partial_data():
    """
    Tests whether ``ChannelMetadataGuildAnnouncements._from_partial_data`` works as intended.
    """
    name = 'Armelyrics'
    
    channel_metadata = ChannelMetadataGuildAnnouncements._from_partial_data({
        'name': name,
    })
    _assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.name, name)
