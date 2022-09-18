from datetime import datetime as DateTime

import vampytest

from ...core import BUILTIN_EMOJIS
from ...bases import Icon, IconType
from ...guild import VoiceRegion
from ...permission import PermissionOverwrite, PermissionOverwriteTargetType

from ..channel_type import ChannelType
from ..channel import Channel
from ..flags import ChannelFlag
from ..forum_tag import ForumTag
from ..preinstanced import VideoQualityMode


def test__Channel__thread_users__0():
    """
    Tests whether ``Channel.thread_users`` works as intended.
    
    Only testing for a thread channel obviously.
    """
    channel = Channel.precreate(202208080000, channel_type = ChannelType.guild_thread_public)
    
    vampytest.assert_is(channel.thread_users, None)
    
    value = {}
    channel.thread_users = value
    vampytest.assert_is(channel.thread_users, value)
    
    channel.thread_users = None
    vampytest.assert_is(channel.thread_users, None)


def test__Channel__general_properties():
    """
    Checks whether the general proxy properties of the ``Channel`` work as intended.
    """
    for channel_type, field_name, value in (
        (ChannelType.guild_thread_public, 'applied_tag_ids', (202209180147, 202209180148)),
        (ChannelType.guild_thread_public, 'archived', True),
        (ChannelType.guild_thread_public, 'archived_at', DateTime(2022, 5, 14)),
        (ChannelType.guild_thread_public, 'auto_archive_after', 604800),
        (ChannelType.guild_forum, 'available_tags', (ForumTag('tumoneko'), )),
        (ChannelType.guild_voice, 'bitrate', 50000),
        (ChannelType.guild_forum, 'default_thread_auto_archive_after', 604800),
        (ChannelType.guild_forum, 'default_thread_reaction', BUILTIN_EMOJIS['heart']),
        (ChannelType.guild_forum, 'default_thread_slowmode', 69),
        (ChannelType.guild_forum, 'flags', ChannelFlag(1)),
        (ChannelType.guild_thread_private, 'invitable', False),
        (ChannelType.guild_thread_private, 'name', 'fated'),
        (ChannelType.guild_text, 'nsfw', True),
        (ChannelType.guild_thread_private, 'open', False),
        (ChannelType.guild_thread_private, 'owner_id', 202209180149),
        (ChannelType.guild_thread_private, 'parent_id', 202209180150),
        (ChannelType.guild_text, 'position', 7),
        (ChannelType.guild_voice, 'region', VoiceRegion.brazil),
        (ChannelType.guild_text, 'slowmode', 32),
        (ChannelType.guild_text, 'topic', 'determination'),
        (ChannelType.guild_voice, 'user_limit', 66),
        (ChannelType.guild_voice, 'video_quality_mode', VideoQualityMode.full),
    ):
        channel = Channel(channel_type = channel_type, **{field_name: value})
        
        vampytest.assert_eq(getattr(channel, field_name), value)


def test__Channel__icon():
    """
    Tests whether ``Channel.icon`` works as intended.
    """
    icon = Icon(IconType.static, 123)
    
    channel = Channel.precreate(202209180151, channel_type = ChannelType.private_group, icon = icon)
    vampytest.assert_eq(channel.icon, icon)


def test__Channel__permission_overwrites():
    """
    Tests whether ``Channel.permission_overwrites`` works as intended.
    """
    # permission_overwrites
    permission_overwrites = [
        PermissionOverwrite(202209180152, target_type = PermissionOverwriteTargetType.user)
    ]
    
    channel = Channel(channel_type = ChannelType.guild_text, permission_overwrites = permission_overwrites)
    
    vampytest.assert_eq(
        channel.permission_overwrites,
        {permission_overwrite.target_id: permission_overwrite for permission_overwrite in permission_overwrites},
    )
