import vampytest

from ....core import BUILTIN_EMOJIS
from ....emoji import Emoji

from ...forum_tag import ForumTag
from ...permission_overwrite import PermissionOverwrite, PermissionOverwriteTargetType

from ..flags import ChannelFlag
from ..guild_media import ChannelMetadataGuildMedia
from ..preinstanced import ForumLayout, SortOrder


def _assert_fields_set(channel_metadata):
    vampytest.assert_instance(channel_metadata, ChannelMetadataGuildMedia)
    
    vampytest.assert_instance(channel_metadata.parent_id, int)
    vampytest.assert_instance(channel_metadata.name, str)
    vampytest.assert_instance(channel_metadata._cache_permission, dict, nullable = True)
    vampytest.assert_instance(channel_metadata.permission_overwrites, dict, nullable = True)
    vampytest.assert_instance(channel_metadata.position, int)
    vampytest.assert_instance(channel_metadata.available_tags, tuple, nullable = True)
    vampytest.assert_instance(channel_metadata.default_forum_layout, ForumLayout)
    vampytest.assert_instance(channel_metadata.default_sort_order, SortOrder)
    vampytest.assert_instance(channel_metadata.default_thread_auto_archive_after, int)
    vampytest.assert_instance(channel_metadata.default_thread_reaction, Emoji, nullable = True)
    vampytest.assert_instance(channel_metadata.default_thread_slowmode, int)
    vampytest.assert_instance(channel_metadata.flags, ChannelFlag)
    vampytest.assert_instance(channel_metadata.topic, str, nullable = True)


def test__ChannelMetadataGuildMedia__new__0():
    """
    Tests whether ``ChannelMetadataGuildMedia.__new__`` works as intended.
    
    Case: all fields given.
    """
    parent_id = 202307040100
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202307040101, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    available_tags = [
        ForumTag.precreate(
            202307040102,
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
    default_forum_layout = ForumLayout.list
    
    channel_metadata = ChannelMetadataGuildMedia(
        parent_id = parent_id,
        name = name,
        permission_overwrites = permission_overwrites,
        position = position,
        available_tags = available_tags,
        default_thread_auto_archive_after = default_thread_auto_archive_after,
        default_thread_reaction = default_thread_reaction,
        default_thread_slowmode = default_thread_slowmode,
        flags = flags,
        topic = topic,
        default_sort_order = default_sort_order,
        default_forum_layout = default_forum_layout,
    )
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
    vampytest.assert_eq(channel_metadata.default_thread_reaction, default_thread_reaction)
    vampytest.assert_eq(channel_metadata.default_thread_slowmode, default_thread_slowmode)
    vampytest.assert_eq(channel_metadata.flags, flags)
    vampytest.assert_eq(channel_metadata.topic, topic)
    vampytest.assert_is(channel_metadata.default_sort_order, default_sort_order)
    vampytest.assert_is(channel_metadata.default_forum_layout, default_forum_layout)


def test__ChannelMetadataGuildMedia__new__1():
    """
    Tests whether ``ChannelMetadataGuildMedia.__new__`` works as intended.
    
    Case: no fields given.
    """
    channel_metadata = ChannelMetadataGuildMedia()
    _assert_fields_set(channel_metadata)


def test__ChannelMetadataGuildMedia__from_keyword_parameters__0():
    """
    Tests whether ``ChannelMetadataGuildMedia.from_keyword_parameters`` works as intended.
    
    Case: all fields given.
    """
    parent_id = 202307040103
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202307040104, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    available_tags = [
        ForumTag.precreate(
            202307040105,
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
    default_forum_layout = ForumLayout.list
    
    keyword_parameters = {
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
        'default_forum_layout': default_forum_layout,
    }
    
    channel_metadata = ChannelMetadataGuildMedia.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(channel_metadata)
    vampytest.assert_eq(keyword_parameters, {})
    
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
    vampytest.assert_is(channel_metadata.default_sort_order, default_sort_order)
    vampytest.assert_is(channel_metadata.default_forum_layout, default_forum_layout)


def test__ChannelMetadataGuildMedia__from_keyword_parameters__1():
    """
    Tests whether ``ChannelMetadataGuildMedia.from_keyword_parameters`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    channel_metadata = ChannelMetadataGuildMedia.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(channel_metadata)
    vampytest.assert_eq(keyword_parameters, {})


def test__ChannelMetadataGuildMedia__create_empty():
    """
    Tests whether ``ChannelMetadataGuildMedia._create_empty`` works as intended.
    """
    channel_metadata = ChannelMetadataGuildMedia._create_empty()
    _assert_fields_set(channel_metadata)
