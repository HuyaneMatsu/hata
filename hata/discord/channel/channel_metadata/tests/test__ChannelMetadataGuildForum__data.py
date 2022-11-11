import vampytest

from ....core import BUILTIN_EMOJIS
from ....permission import PermissionOverwrite, PermissionOverwriteTargetType

from ...forum_tag import ForumTag

from ..flags import ChannelFlag
from ..preinstanced import SortOrder

from ..guild_forum import ChannelMetadataGuildForum

from .test__ChannelMetadataGuildForum__constructor import assert_fields_set


def test__ChannelMetadataGuildForum__from_data():
    """
    Tests whether ``ChannelMetadataGuildForum.from_data` works as intended.
    """
    parent_id = 202209170077
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170078, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    available_tags = [
        ForumTag.precreate(
            202209170079,
            emoji = BUILTIN_EMOJIS['heart'],
            name = 'Yup',
            moderated = False,
        )
    ]
    default_thread_auto_archive_after = 86400
    default_thread_reaction = BUILTIN_EMOJIS['monkey']
    default_thread_slowmode = 60
    flags = ChannelFlag(1)
    topic = 'Dearest'
    default_sort_order = SortOrder.creation_date
    
    
    channel_metadata = ChannelMetadataGuildForum.from_data({
        'parent_id': str(parent_id),
        'name': name,
        'permission_overwrites': [
            permission_overwrite.to_data(include_internals = True)
            for permission_overwrite in permission_overwrites
        ],
        'position': position,
        'available_tags': [forum_tag.to_data(include_internals = True) for forum_tag in available_tags],
        'default_auto_archive_duration': default_thread_auto_archive_after // 60,
        'default_reaction_emoji': {'emoji_name': default_thread_reaction.unicode},
        'default_thread_rate_limit_per_user': default_thread_slowmode,
        'flags': int(flags),
        'topic': topic,
        'default_sort_order': default_sort_order.value,
    })
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildForum)
    assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.parent_id, parent_id)
    vampytest.assert_eq(channel_metadata.name, name)
    vampytest.assert_eq(
        channel_metadata.permission_overwrites,
        {permission_overwrite.target_id: permission_overwrite for permission_overwrite in permission_overwrites},
    )
    vampytest.assert_eq(channel_metadata.position, position)
    vampytest.assert_eq(channel_metadata.available_tags, tuple(available_tags))
    vampytest.assert_eq(channel_metadata.default_thread_auto_archive_after, default_thread_auto_archive_after)
    vampytest.assert_eq(channel_metadata.default_thread_reaction, default_thread_reaction)
    vampytest.assert_eq(channel_metadata.default_thread_slowmode, default_thread_slowmode)
    vampytest.assert_eq(channel_metadata.flags, flags)
    vampytest.assert_eq(channel_metadata.topic, topic)
    vampytest.assert_eq(channel_metadata.default_sort_order, default_sort_order)


def test__ChannelMetadataGuildForum__to_data():
    """
    Tests whether ``ChannelMetadataGuildForum.to_data`` works as intended.
    
    Case: include defaults and internals.
    """
    parent_id = 202209170080
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170081, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    available_tags = [
        ForumTag.precreate(
            202209170082,
            emoji = BUILTIN_EMOJIS['heart'],
            name = 'Yup',
            moderated = False,
        )
    ]
    default_thread_auto_archive_after = 86400
    default_thread_reaction = BUILTIN_EMOJIS['monkey']
    default_thread_slowmode = 60
    flags = ChannelFlag(1)
    topic = 'Dearest'
    default_sort_order = SortOrder.creation_date
    
    channel_metadata = ChannelMetadataGuildForum({
        'parent_id': parent_id,
        'name': name,
        'permission_overwrites': permission_overwrites,
        'position': position,
        'available_tags': available_tags,
        'default_thread_auto_archive_after': default_thread_auto_archive_after,
        'default_thread_reaction': default_thread_reaction,
        'default_thread_slowmode': default_thread_slowmode,
        'flags': flags,
        'topic': topic,
        'default_sort_order': default_sort_order,
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
            'available_tags': [
                forum_tag.to_data(defaults = True, include_internals = True) for forum_tag in available_tags
            ],
            'default_auto_archive_duration': default_thread_auto_archive_after // 60,
            'default_reaction_emoji': {'emoji_name': default_thread_reaction.unicode},
            'default_thread_rate_limit_per_user': default_thread_slowmode,
            'flags': int(flags),
            'topic': topic,
            'default_sort_order': default_sort_order.value,
        },
    )


def test__ChannelMetadataGuildForum__update_attributes():
    """
    Tests whether ``ChannelMetadataGuildForum._update_attributes`` works as intended.
    """
    old_parent_id = 202209170083
    new_parent_id = 202209170084
    old_name = 'Armelyrics'
    new_name = 'Okuu'
    old_permission_overwrites = [
        PermissionOverwrite(202209170085, target_type = PermissionOverwriteTargetType.user)
    ]
    new_permission_overwrites = [
        PermissionOverwrite(202209170086, target_type = PermissionOverwriteTargetType.role)
    ]
    old_position = 7
    new_position = 5
    old_available_tags = [
        ForumTag.precreate(
            202209170087,
            emoji = BUILTIN_EMOJIS['heart'],
            name = 'Yup',
            moderated = False,
        )
    ]
    new_available_tags = [
        ForumTag.precreate(
            202209170088,
            emoji = BUILTIN_EMOJIS['duck'],
            name = 'Ashy',
            moderated = True,
        )
    ]
    old_default_thread_auto_archive_after = 86400
    new_default_thread_auto_archive_after = 3600
    old_default_thread_reaction = BUILTIN_EMOJIS['monkey']
    new_default_thread_reaction = BUILTIN_EMOJIS['radio']
    old_default_thread_slowmode = 60
    new_default_thread_slowmode = 600
    old_flags = ChannelFlag(1)
    new_flags = ChannelFlag(4)
    old_topic = 'Dearest'
    new_topic = 'My'
    old_default_sort_order = SortOrder.creation_date
    new_default_sort_order = SortOrder.latest_activity
    
    channel_metadata = ChannelMetadataGuildForum({
        'parent_id': old_parent_id,
        'name': old_name,
        'permission_overwrites': old_permission_overwrites,
        'position': old_position,
        'available_tags': old_available_tags,
        'default_thread_auto_archive_after': old_default_thread_auto_archive_after,
        'default_thread_reaction': old_default_thread_reaction,
        'default_thread_slowmode': old_default_thread_slowmode,
        'flags': old_flags,
        'topic': old_topic,
        'default_sort_order': old_default_sort_order,
    })
    
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
        'default_reaction_emoji': {'emoji_name': new_default_thread_reaction.unicode},
        'default_thread_rate_limit_per_user': new_default_thread_slowmode,
        'flags': int(new_flags),
        'topic': new_topic,
        'default_sort_order': new_default_sort_order.value,
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
    vampytest.assert_eq(channel_metadata.default_thread_reaction, new_default_thread_reaction)
    vampytest.assert_eq(channel_metadata.default_thread_slowmode, new_default_thread_slowmode)
    vampytest.assert_eq(channel_metadata.flags, new_flags)
    vampytest.assert_eq(channel_metadata.topic, new_topic)
    vampytest.assert_eq(channel_metadata.default_sort_order, new_default_sort_order)


def test__ChannelMetadataGuildForum__difference_update_attributes():
    """
    Tests whether ``ChannelMetadataGuildForum._difference_update_attributes`` works as intended.
    """
    old_parent_id = 202209170089
    new_parent_id = 202209170090
    old_name = 'Armelyrics'
    new_name = 'Okuu'
    old_permission_overwrites = [
        PermissionOverwrite(202209170091, target_type = PermissionOverwriteTargetType.user)
    ]
    new_permission_overwrites = [
        PermissionOverwrite(202209170092, target_type = PermissionOverwriteTargetType.role)
    ]
    old_position = 7
    new_position = 5
    old_available_tags = [
        ForumTag.precreate(
            202209170093,
            emoji = BUILTIN_EMOJIS['heart'],
            name = 'Yup',
            moderated = False,
        )
    ]
    new_available_tags = [
        ForumTag.precreate(
            202209170094,
            emoji = BUILTIN_EMOJIS['duck'],
            name = 'Ashy',
            moderated = True,
        )
    ]
    old_default_thread_auto_archive_after = 86400
    new_default_thread_auto_archive_after = 3600
    old_default_thread_reaction = BUILTIN_EMOJIS['monkey']
    new_default_thread_reaction = BUILTIN_EMOJIS['radio']
    old_default_thread_slowmode = 60
    new_default_thread_slowmode = 600
    old_flags = ChannelFlag(1)
    new_flags = ChannelFlag(4)
    old_topic = 'Dearest'
    new_topic = 'My'
    old_default_sort_order = SortOrder.creation_date
    new_default_sort_order = SortOrder.latest_activity
    
    channel_metadata = ChannelMetadataGuildForum({
        'parent_id': old_parent_id,
        'name': old_name,
        'permission_overwrites': old_permission_overwrites,
        'position': old_position,
        'available_tags': old_available_tags,
        'default_thread_auto_archive_after': old_default_thread_auto_archive_after,
        'default_thread_reaction': old_default_thread_reaction,
        'default_thread_slowmode': old_default_thread_slowmode,
        'flags': old_flags,
        'topic': old_topic,
        'default_sort_order': old_default_sort_order,
    })
    
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
        'default_reaction_emoji': {'emoji_name': new_default_thread_reaction.unicode},
        'default_thread_rate_limit_per_user': new_default_thread_slowmode,
        'flags': int(new_flags),
        'topic': new_topic,
        'default_sort_order': new_default_sort_order.value,
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
    vampytest.assert_eq(channel_metadata.default_thread_reaction, new_default_thread_reaction)
    vampytest.assert_eq(channel_metadata.default_thread_slowmode, new_default_thread_slowmode)
    vampytest.assert_eq(channel_metadata.flags, new_flags)
    vampytest.assert_eq(channel_metadata.topic, new_topic)
    vampytest.assert_eq(channel_metadata.default_sort_order, new_default_sort_order)
    
    vampytest.assert_in('parent_id', old_attributes)
    vampytest.assert_in('name', old_attributes)
    vampytest.assert_in('permission_overwrites', old_attributes)
    vampytest.assert_in('position', old_attributes)
    vampytest.assert_in('available_tags', old_attributes)
    vampytest.assert_in('default_thread_auto_archive_after', old_attributes)
    vampytest.assert_in('default_thread_reaction', old_attributes)
    vampytest.assert_in('default_thread_slowmode', old_attributes)
    vampytest.assert_in('flags', old_attributes)
    vampytest.assert_in('topic', old_attributes)
    vampytest.assert_in('default_sort_order', old_attributes)
    
    vampytest.assert_eq(old_attributes['parent_id'], old_parent_id)
    vampytest.assert_eq(old_attributes['name'], old_name)
    vampytest.assert_eq(
        old_attributes['permission_overwrites'],
        {permission_overwrite.target_id: permission_overwrite for permission_overwrite in old_permission_overwrites},
    )
    vampytest.assert_eq(old_attributes['position'], old_position)
    vampytest.assert_eq(old_attributes['available_tags'], tuple(old_available_tags))
    vampytest.assert_eq(old_attributes['default_thread_auto_archive_after'], old_default_thread_auto_archive_after)
    vampytest.assert_eq(old_attributes['default_thread_reaction'], old_default_thread_reaction)
    vampytest.assert_eq(old_attributes['default_thread_slowmode'], old_default_thread_slowmode)
    vampytest.assert_eq(old_attributes['flags'], old_flags)
    vampytest.assert_eq(old_attributes['topic'], old_topic)
    vampytest.assert_eq(old_attributes['default_sort_order'], old_default_sort_order)


def test__ChannelMetadataGuildForum__from_partial_data():
    """
    Tests whether ``ChannelMetadataGuildForum._from_partial_data`` works as intended.
    """
    name = 'Armelyrics'
    
    channel_metadata = ChannelMetadataGuildForum._from_partial_data({
        'name': name,
    })
    
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildForum)
    assert_fields_set(channel_metadata)
    
    vampytest.assert_eq(channel_metadata.name, name)
