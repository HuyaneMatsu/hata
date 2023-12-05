import vampytest

from ....core import BUILTIN_EMOJIS

from ...forum_tag import ForumTag
from ...forum_tag_change import ForumTagChange
from ...permission_overwrite import PermissionOverwrite, PermissionOverwriteTargetType

from ..flags import ChannelFlag
from ..guild_media import ChannelMetadataGuildMedia
from ..preinstanced import ForumLayout, SortOrder

from .test__ChannelMetadataGuildMedia__constructor import _assert_fields_set


def test__ChannelMetadataGuildMedia__from_data():
    """
    Tests whether ``ChannelMetadataGuildMedia.from_data` works as intended.
    """
    parent_id = 202307040106
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202307040107, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    available_tags = [
        ForumTag.precreate(
            202307040108,
            emoji = BUILTIN_EMOJIS['heart'],
            name = 'Yup',
            moderated = False,
        )
    ]
    default_thread_auto_archive_after = 86400
    default_thread_reaction_emoji = BUILTIN_EMOJIS['monkey']
    default_thread_slowmode = 60
    flags = ChannelFlag(1)
    topic = 'Dearest'
    default_sort_order = SortOrder.creation_date
    default_forum_layout = ForumLayout.list
    
    
    channel_metadata = ChannelMetadataGuildMedia.from_data({
        'parent_id': str(parent_id),
        'name': name,
        'permission_overwrites': [
            permission_overwrite.to_data(include_internals = True)
            for permission_overwrite in permission_overwrites
        ],
        'position': position,
        'available_tags': [forum_tag.to_data(include_internals = True) for forum_tag in available_tags],
        'default_auto_archive_duration': default_thread_auto_archive_after // 60,
        'default_reaction_emoji': {'emoji_name': default_thread_reaction_emoji.unicode},
        'default_thread_rate_limit_per_user': default_thread_slowmode,
        'flags': int(flags),
        'topic': topic,
        'default_sort_order': default_sort_order.value,
        'default_forum_layout': default_forum_layout.value,
    })
    _assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.parent_id, parent_id)
    vampytest.assert_eq(channel_metadata.name, name)
    vampytest.assert_eq(
        channel_metadata.permission_overwrites,
        {permission_overwrite.target_id: permission_overwrite for permission_overwrite in permission_overwrites},
    )
    vampytest.assert_eq(channel_metadata.position, position)
    vampytest.assert_eq(channel_metadata.available_tags, tuple(available_tags))
    vampytest.assert_eq(channel_metadata.default_thread_auto_archive_after, default_thread_auto_archive_after)
    vampytest.assert_eq(channel_metadata.default_thread_reaction_emoji, default_thread_reaction_emoji)
    vampytest.assert_eq(channel_metadata.default_thread_slowmode, default_thread_slowmode)
    vampytest.assert_eq(channel_metadata.flags, flags)
    vampytest.assert_eq(channel_metadata.topic, topic)
    vampytest.assert_is(channel_metadata.default_sort_order, default_sort_order)
    vampytest.assert_is(channel_metadata.default_forum_layout, default_forum_layout)


def test__ChannelMetadataGuildMedia__to_data():
    """
    Tests whether ``ChannelMetadataGuildMedia.to_data`` works as intended.
    
    Case: include defaults and internals.
    """
    parent_id = 202307040109
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202307040110, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    available_tags = [
        ForumTag.precreate(
            202307040111,
            emoji = BUILTIN_EMOJIS['heart'],
            name = 'Yup',
            moderated = False,
        )
    ]
    default_thread_auto_archive_after = 86400
    default_thread_reaction_emoji = BUILTIN_EMOJIS['monkey']
    default_thread_slowmode = 60
    flags = ChannelFlag(1)
    topic = 'Dearest'
    default_sort_order = SortOrder.creation_date
    default_forum_layout = ForumLayout.list
    
    channel_metadata = ChannelMetadataGuildMedia(
        parent_id = parent_id,
        name = name,
        permission_overwrites = permission_overwrites,
        position = position,
        available_tags = available_tags,
        default_thread_auto_archive_after = default_thread_auto_archive_after,
        default_thread_reaction_emoji = default_thread_reaction_emoji,
        default_thread_slowmode = default_thread_slowmode,
        flags = flags,
        topic = topic,
        default_sort_order = default_sort_order,
        default_forum_layout = default_forum_layout,
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
            'available_tags': [
                forum_tag.to_data(defaults = True, include_internals = True) for forum_tag in available_tags
            ],
            'default_auto_archive_duration': default_thread_auto_archive_after // 60,
            'default_reaction_emoji': {'emoji_name': default_thread_reaction_emoji.unicode},
            'default_thread_rate_limit_per_user': default_thread_slowmode,
            'flags': int(flags),
            'topic': topic,
            'default_sort_order': default_sort_order.value,
            'default_forum_layout': default_forum_layout.value,
        },
    )


def test__ChannelMetadataGuildMedia__update_attributes():
    """
    Tests whether ``ChannelMetadataGuildMedia._update_attributes`` works as intended.
    """
    old_parent_id = 202307040112
    old_name = 'Armelyrics'
    old_permission_overwrites = [
        PermissionOverwrite(202307040113, target_type = PermissionOverwriteTargetType.user)
    ]
    old_position = 7
    old_available_tags = [
        ForumTag.precreate(
            202307040114,
            emoji = BUILTIN_EMOJIS['heart'],
            name = 'Yup',
            moderated = False,
        )
    ]
    old_default_thread_auto_archive_after = 86400
    old_default_thread_reaction_emoji = BUILTIN_EMOJIS['monkey']
    old_default_thread_slowmode = 60
    old_flags = ChannelFlag(1)
    old_topic = 'Dearest'
    old_default_sort_order = SortOrder.creation_date
    old_default_forum_layout = ForumLayout.list
    
    new_parent_id = 202307040115
    new_name = 'Okuu'
    new_permission_overwrites = [
        PermissionOverwrite(202307040116, target_type = PermissionOverwriteTargetType.role)
    ]
    new_position = 5
    new_available_tags = [
        ForumTag.precreate(
            202307040117,
            emoji = BUILTIN_EMOJIS['duck'],
            name = 'Ashy',
            moderated = True,
        )
    ]
    new_default_thread_auto_archive_after = 3600
    new_default_thread_reaction_emoji = BUILTIN_EMOJIS['radio']
    new_default_thread_slowmode = 600
    new_flags = ChannelFlag(4)
    new_topic = 'My'
    new_default_sort_order = SortOrder.latest_activity
    new_default_forum_layout = ForumLayout.gallery
    
    channel_metadata = ChannelMetadataGuildMedia(
        parent_id = old_parent_id,
        name = old_name,
        permission_overwrites = old_permission_overwrites,
        position = old_position,
        available_tags = old_available_tags,
        default_thread_auto_archive_after = old_default_thread_auto_archive_after,
        default_thread_reaction_emoji = old_default_thread_reaction_emoji,
        default_thread_slowmode = old_default_thread_slowmode,
        flags = old_flags,
        topic = old_topic,
        default_sort_order = old_default_sort_order,
        default_forum_layout = old_default_forum_layout,
    )
    
    channel_metadata._update_attributes({
        'parent_id': str(new_parent_id),
        'name': new_name,
        'permission_overwrites': [
            permission_overwrite.to_data(include_internals = True)
            for permission_overwrite in new_permission_overwrites
        ],
        'position': new_position,
        'available_tags': [forum_tag.to_data(include_internals = True) for forum_tag in new_available_tags],
        'default_auto_archive_duration': new_default_thread_auto_archive_after // 60,
        'default_reaction_emoji': {'emoji_name': new_default_thread_reaction_emoji.unicode},
        'default_thread_rate_limit_per_user': new_default_thread_slowmode,
        'flags': int(new_flags),
        'topic': new_topic,
        'default_sort_order': new_default_sort_order.value,
        'default_forum_layout': new_default_forum_layout.value,
    })
    
    vampytest.assert_eq(channel_metadata.parent_id, new_parent_id)
    vampytest.assert_eq(channel_metadata.name, new_name)
    vampytest.assert_eq(
        channel_metadata.permission_overwrites,
        {permission_overwrite.target_id: permission_overwrite for permission_overwrite in new_permission_overwrites},
    )
    vampytest.assert_eq(channel_metadata.position, new_position)
    vampytest.assert_eq(channel_metadata.available_tags, tuple(new_available_tags))
    vampytest.assert_eq(channel_metadata.default_thread_auto_archive_after, new_default_thread_auto_archive_after)
    vampytest.assert_eq(channel_metadata.default_thread_reaction_emoji, new_default_thread_reaction_emoji)
    vampytest.assert_eq(channel_metadata.default_thread_slowmode, new_default_thread_slowmode)
    vampytest.assert_eq(channel_metadata.flags, new_flags)
    vampytest.assert_eq(channel_metadata.topic, new_topic)
    vampytest.assert_is(channel_metadata.default_sort_order, new_default_sort_order)
    vampytest.assert_is(channel_metadata.default_forum_layout, new_default_forum_layout)


def test__ChannelMetadataGuildMedia__difference_update_attributes():
    """
    Tests whether ``ChannelMetadataGuildMedia._difference_update_attributes`` works as intended.
    """
    old_parent_id = 202307040118
    new_parent_id = 202307040119
    old_name = 'Armelyrics'
    new_name = 'Okuu'
    old_permission_overwrites = [
        PermissionOverwrite(202307040120, target_type = PermissionOverwriteTargetType.user)
    ]
    new_permission_overwrites = [
        PermissionOverwrite(202307040121, target_type = PermissionOverwriteTargetType.role)
    ]
    old_position = 7
    new_position = 5
    old_available_tags = [
        ForumTag.precreate(
            202307040122,
            emoji = BUILTIN_EMOJIS['heart'],
            name = 'Yup',
            moderated = False,
        )
    ]
    new_available_tags = [
        ForumTag.precreate(
            202307040123,
            emoji = BUILTIN_EMOJIS['duck'],
            name = 'Ashy',
            moderated = True,
        )
    ]
    old_default_thread_auto_archive_after = 86400
    new_default_thread_auto_archive_after = 3600
    old_default_thread_reaction_emoji = BUILTIN_EMOJIS['monkey']
    new_default_thread_reaction_emoji = BUILTIN_EMOJIS['radio']
    old_default_thread_slowmode = 60
    new_default_thread_slowmode = 600
    old_flags = ChannelFlag(1)
    new_flags = ChannelFlag(4)
    old_topic = 'Dearest'
    new_topic = 'My'
    old_default_sort_order = SortOrder.creation_date
    new_default_sort_order = SortOrder.latest_activity
    old_default_forum_layout = ForumLayout.list
    new_default_forum_layout = ForumLayout.gallery
    
    channel_metadata = ChannelMetadataGuildMedia(
        parent_id = old_parent_id,
        name = old_name,
        permission_overwrites = old_permission_overwrites,
        position = old_position,
        available_tags = old_available_tags,
        default_thread_auto_archive_after = old_default_thread_auto_archive_after,
        default_thread_reaction_emoji = old_default_thread_reaction_emoji,
        default_thread_slowmode = old_default_thread_slowmode,
        flags = old_flags,
        topic = old_topic,
        default_sort_order = old_default_sort_order,
        default_forum_layout = old_default_forum_layout,
    )
    
    old_attributes = channel_metadata._difference_update_attributes({
        'parent_id': str(new_parent_id),
        'name': new_name,
        'permission_overwrites': [
            permission_overwrite.to_data(include_internals = True)
            for permission_overwrite in new_permission_overwrites
        ],
        'position': new_position,
        'available_tags': [forum_tag.to_data(include_internals = True) for forum_tag in new_available_tags],
        'default_auto_archive_duration': new_default_thread_auto_archive_after // 60,
        'default_reaction_emoji': {'emoji_name': new_default_thread_reaction_emoji.unicode},
        'default_thread_rate_limit_per_user': new_default_thread_slowmode,
        'flags': int(new_flags),
        'topic': new_topic,
        'default_sort_order': new_default_sort_order.value,
        'default_forum_layout': new_default_forum_layout.value,
    })

    vampytest.assert_eq(channel_metadata.parent_id, new_parent_id)
    vampytest.assert_eq(channel_metadata.name, new_name)
    vampytest.assert_eq(
        channel_metadata.permission_overwrites,
        {permission_overwrite.target_id: permission_overwrite for permission_overwrite in new_permission_overwrites},
    )
    vampytest.assert_eq(channel_metadata.position, new_position)
    vampytest.assert_eq(channel_metadata.available_tags, tuple(new_available_tags))
    vampytest.assert_eq(channel_metadata.default_thread_auto_archive_after, new_default_thread_auto_archive_after)
    vampytest.assert_eq(channel_metadata.default_thread_reaction_emoji, new_default_thread_reaction_emoji)
    vampytest.assert_eq(channel_metadata.default_thread_slowmode, new_default_thread_slowmode)
    vampytest.assert_eq(channel_metadata.flags, new_flags)
    vampytest.assert_eq(channel_metadata.topic, new_topic)
    vampytest.assert_is(channel_metadata.default_sort_order, new_default_sort_order)
    vampytest.assert_is(channel_metadata.default_forum_layout, new_default_forum_layout)
    
    vampytest.assert_in('parent_id', old_attributes)
    vampytest.assert_in('name', old_attributes)
    vampytest.assert_in('permission_overwrites', old_attributes)
    vampytest.assert_in('position', old_attributes)
    vampytest.assert_in('available_tags', old_attributes)
    vampytest.assert_in('default_thread_auto_archive_after', old_attributes)
    vampytest.assert_in('default_thread_reaction_emoji', old_attributes)
    vampytest.assert_in('default_thread_slowmode', old_attributes)
    vampytest.assert_in('flags', old_attributes)
    vampytest.assert_in('topic', old_attributes)
    vampytest.assert_in('default_sort_order', old_attributes)
    vampytest.assert_in('default_forum_layout', old_attributes)
    
    vampytest.assert_eq(old_attributes['parent_id'], old_parent_id)
    vampytest.assert_eq(old_attributes['name'], old_name)
    vampytest.assert_eq(
        old_attributes['permission_overwrites'],
        {permission_overwrite.target_id: permission_overwrite for permission_overwrite in old_permission_overwrites},
    )
    vampytest.assert_eq(old_attributes['position'], old_position)
    vampytest.assert_eq(
        old_attributes['available_tags'],
        ForumTagChange.from_fields(old_available_tags, None, new_available_tags),
    )
    vampytest.assert_eq(old_attributes['default_thread_auto_archive_after'], old_default_thread_auto_archive_after)
    vampytest.assert_eq(old_attributes['default_thread_reaction_emoji'], old_default_thread_reaction_emoji)
    vampytest.assert_eq(old_attributes['default_thread_slowmode'], old_default_thread_slowmode)
    vampytest.assert_eq(old_attributes['flags'], old_flags)
    vampytest.assert_eq(old_attributes['topic'], old_topic)
    vampytest.assert_eq(old_attributes['default_sort_order'], old_default_sort_order)
    vampytest.assert_eq(old_attributes['default_forum_layout'], old_default_forum_layout)


def test__ChannelMetadataGuildMedia__from_partial_data():
    """
    Tests whether ``ChannelMetadataGuildMedia._from_partial_data`` works as intended.
    """
    name = 'Armelyrics'
    
    channel_metadata = ChannelMetadataGuildMedia._from_partial_data({
        'name': name,
    })
    _assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.name, name)
