import vampytest

from ....core import BUILTIN_EMOJIS

from ...forum_tag import ForumTag
from ...permission_overwrite import PermissionOverwrite, PermissionOverwriteTargetType

from ..flags import ChannelFlag
from ..guild_media import ChannelMetadataGuildMedia
from ..preinstanced import ForumLayout, SortOrder


def test__ChannelMetadataGuildMedia__repr():
    """
    Tests whether ``.ChannelMetadataGuildMedia.__repr__`` works as intended.
    """
    parent_id = 202307040124
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202307040125, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    available_tags = [
        ForumTag.precreate(
            202307040126,
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
    
    vampytest.assert_instance(repr(channel_metadata), str)


def test__ChannelMetadataGuildMedia__hash():
    """
    Tests whether ``.ChannelMetadataGuildMedia.__hash__`` works as intended.
    """
    parent_id = 202209180089
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202307040127, target_type = PermissionOverwriteTargetType.user)
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
    
    vampytest.assert_instance(hash(channel_metadata), int)


def test__ChannelMetadataGuildMedia__eq():
    """
    Tests whether ``.ChannelMetadataGuildMedia.__eq__`` works as intended.
    """
    parent_id = 202307040128
    name = 'Armelyrics'
    permission_overwrites = [
        PermissionOverwrite(202307040129, target_type = PermissionOverwriteTargetType.user)
    ]
    position = 7
    available_tags = [
        ForumTag.precreate(
            202307040130,
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
    
    keyword_parameters = {
        'parent_id': parent_id,
        'name': name,
        'permission_overwrites': permission_overwrites,
        'position': position,
        'available_tags': available_tags,
        'default_thread_auto_archive_after': default_thread_auto_archive_after,
        'default_thread_reaction_emoji': default_thread_reaction_emoji,
        'default_thread_slowmode': default_thread_slowmode,
        'flags': flags,
        'topic': topic,
        'default_sort_order': default_sort_order,
        'default_forum_layout': default_forum_layout,
    }
    channel_metadata = ChannelMetadataGuildMedia(**keyword_parameters)
    
    vampytest.assert_eq(channel_metadata, channel_metadata)
    vampytest.assert_ne(channel_metadata, object())
    
    for field_name, field_value in (
        ('parent_id', 202307040131),
        ('name', 'Okuu'),
        (
            'permission_overwrites',
            [
                PermissionOverwrite(202307040132, target_type = PermissionOverwriteTargetType.role)
            ],
        ),
        ('position', 6),
        ('available_tags', None),
        ('default_thread_auto_archive_after', 3600),
        ('default_thread_reaction_emoji', None),
        ('default_thread_slowmode', 0),
        ('flags', ChannelFlag(3)),
        ('topic', 'Dai'),
        ('default_sort_order', SortOrder.latest_activity),
        ('default_forum_layout', ForumLayout.gallery),
    ):
        test_channel_metadata = ChannelMetadataGuildMedia(**{**keyword_parameters, field_name: field_value})
        
        vampytest.assert_ne(channel_metadata, test_channel_metadata)
