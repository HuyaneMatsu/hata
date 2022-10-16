import vampytest

from .....core import BUILTIN_EMOJIS
from .....permission import PermissionOverwrite, PermissionOverwriteTargetType

from ....forum_tag import ForumTag

from ...flags import ChannelFlag

from ..guild_forum import ChannelMetadataGuildForum


def test__ChannelMetadataGuildForum__repr():
    """
    Tests whether ``.ChannelMetadataGuildForum.__repr__`` works as intended.
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
    }
    channel_metadata = ChannelMetadataGuildForum(keyword_parameters)
    
    vampytest.assert_instance(repr(channel_metadata), str)


def test__ChannelMetadataGuildForum__hash():
    """
    Tests whether ``.ChannelMetadataGuildForum.__hash__`` works as intended.
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
    }
    channel_metadata = ChannelMetadataGuildForum(keyword_parameters)
    
    vampytest.assert_instance(hash(channel_metadata), int)


def test__ChannelMetadataGuildForum__eq():
    """
    Tests whether ``.ChannelMetadataGuildForum.__eq__`` works as intended.
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
    }
    channel_metadata = ChannelMetadataGuildForum(keyword_parameters)
    
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
    ):
        test_channel_metadata = ChannelMetadataGuildForum({**keyword_parameters, field_name: field_value})
        
        vampytest.assert_ne(channel_metadata, test_channel_metadata)
