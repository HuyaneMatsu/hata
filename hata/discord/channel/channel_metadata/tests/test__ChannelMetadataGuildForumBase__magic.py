import vampytest

from ....core import BUILTIN_EMOJIS

from ...forum_tag import ForumTag
from ...permission_overwrite import PermissionOverwrite, PermissionOverwriteTargetType

from ..flags import ChannelFlag
from ..guild_forum import ChannelMetadataGuildForumBase
from ..preinstanced import ForumLayout, SortOrder


def test__ChannelMetadataGuildForumBase__repr():
    """
    Tests whether ``.ChannelMetadataGuildForumBase.__repr__`` works as intended.
    """
    parent_id = 202209170095
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170096, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    available_tags = [
        ForumTag.precreate(
            202209170097,
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
    

    channel_metadata = ChannelMetadataGuildForumBase(
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
    
    vampytest.assert_instance(repr(channel_metadata), str)


def test__ChannelMetadataGuildForumBase__hash():
    """
    Tests whether ``.ChannelMetadataGuildForumBase.__hash__`` works as intended.
    """
    parent_id = 202209180089
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209180090, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    available_tags = [
        ForumTag.precreate(
            202209180091,
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
    

    channel_metadata = ChannelMetadataGuildForumBase(
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
    
    vampytest.assert_instance(hash(channel_metadata), int)


def test__ChannelMetadataGuildForumBase__eq():
    """
    Tests whether ``.ChannelMetadataGuildForumBase.__eq__`` works as intended.
    """
    parent_id = 202209170098
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202209170099, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    available_tags = [
        ForumTag.precreate(
            2022091700100,
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
    channel_metadata = ChannelMetadataGuildForumBase(**keyword_parameters)
    
    vampytest.assert_eq(channel_metadata, channel_metadata)
    vampytest.assert_ne(channel_metadata, object())
    
    for field_name, field_value in (
        ('parent_id', 202209170101),
        ('name', 'Okuu'),
        (
            'permission_overwrites',
            [
                PermissionOverwrite(202209170070, target_type = PermissionOverwriteTargetType.role)
            ],
        ),
        ('position', 6),
        ('available_tags', None),
        ('default_thread_auto_archive_after', 3600),
        ('default_thread_reaction', None),
        ('default_thread_slowmode', 0),
        ('flags', ChannelFlag(3)),
        ('topic', 'Dai'),
        ('default_sort_order', SortOrder.latest_activity),
        ('default_forum_layout', ForumLayout.gallery),
    ):
        test_channel_metadata = ChannelMetadataGuildForumBase(**{**keyword_parameters, field_name: field_value})
        
        vampytest.assert_ne(channel_metadata, test_channel_metadata)
