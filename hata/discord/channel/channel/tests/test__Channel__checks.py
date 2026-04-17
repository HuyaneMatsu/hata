import vampytest

from ..channel import Channel
from ..preinstanced import ChannelType


def _iter_options():
    channel_types = [
        ChannelType.guild_text,
        ChannelType.private,
        ChannelType.guild_voice,
        ChannelType.private_group,
        ChannelType.guild_category,
        ChannelType.guild_announcements,
        ChannelType.guild_store,
        ChannelType.thread,
        ChannelType.guild_thread_announcements,
        ChannelType.guild_thread_public,
        ChannelType.guild_thread_private,
        ChannelType.guild_stage,
        ChannelType.guild_directory,
        ChannelType.guild_forum,
        ChannelType.guild_media,
    ]
    
    for check, passing_types in (
        (
            Channel.is_in_group_textual,
            {
                ChannelType.guild_text,
                ChannelType.private,
                ChannelType.guild_voice,
                ChannelType.private_group,
                ChannelType.guild_announcements,
                ChannelType.thread,
                ChannelType.guild_thread_announcements,
                ChannelType.guild_thread_public,
                ChannelType.guild_thread_private,
                ChannelType.guild_stage,
            },
        ), (
            Channel.is_in_group_guild_textual,
            {
                ChannelType.guild_text,
                ChannelType.guild_voice,
                ChannelType.guild_announcements,
                ChannelType.guild_thread_announcements,
                ChannelType.guild_thread_public,
                ChannelType.guild_thread_private,
                ChannelType.guild_stage,
            },
        ), (
            Channel.is_in_group_guild_system,
            {
                ChannelType.guild_text,
                ChannelType.guild_announcements,
            },
        ), (
            Channel.is_in_group_connectable,
            {
                ChannelType.private,
                ChannelType.guild_voice,
                ChannelType.private_group,
                ChannelType.guild_stage,
            },
        ), (
            Channel.is_in_group_guild_connectable,
            {
                ChannelType.guild_voice,
                ChannelType.guild_stage,
            },
        ), (
            Channel.is_in_group_private,
            {
                ChannelType.private,
                ChannelType.private_group,
            },
        ), (
            Channel.is_in_group_guild,
            {
                ChannelType.guild_text,
                ChannelType.guild_voice,
                ChannelType.guild_category,
                ChannelType.guild_announcements,
                ChannelType.guild_store,
                ChannelType.guild_thread_announcements,
                ChannelType.guild_thread_public,
                ChannelType.guild_thread_private,
                ChannelType.guild_stage,
                ChannelType.guild_directory,
                ChannelType.guild_forum,
                ChannelType.guild_media,
            },
        ), (
            Channel.is_in_group_thread,
            {
                ChannelType.thread,
                ChannelType.guild_thread_announcements,
                ChannelType.guild_thread_public,
                ChannelType.guild_thread_private,
            },
        ), (
            Channel.is_in_group_threadable,
            {
                ChannelType.guild_text,
                ChannelType.guild_announcements,
                ChannelType.guild_forum,
                ChannelType.guild_media,
            },
        ), (
            Channel.is_in_group_invitable,
            {
                ChannelType.guild_text,
                ChannelType.guild_voice,
                ChannelType.private_group,
                ChannelType.guild_announcements,
                ChannelType.guild_store,
                ChannelType.guild_stage,
                ChannelType.guild_directory,
                ChannelType.guild_forum,
                ChannelType.guild_media,
            },
        ), (
            Channel.is_in_group_guild_sortable,
            {
                ChannelType.guild_text,
                ChannelType.guild_voice,
                ChannelType.guild_category,
                ChannelType.guild_announcements,
                ChannelType.guild_store,
                ChannelType.guild_stage,
                ChannelType.guild_directory,
                ChannelType.guild_forum,
                ChannelType.guild_media,
            },
        ), (
            Channel.is_in_group_forum,
            {
                ChannelType.guild_forum,
                ChannelType.guild_media,
            },
        ), (
            Channel.is_guild_text,
            {
                ChannelType.guild_text,
            },
        ), (
            Channel.is_private,
            {
                ChannelType.private,
            },
        ), (
            Channel.is_guild_voice,
            {
                ChannelType.guild_voice,
            },
        ), (
            Channel.is_private_group,
            {
                ChannelType.private_group,
            },
        ), (
            Channel.is_guild_category,
            {
                ChannelType.guild_category,
            },
        ), (
            Channel.is_guild_announcements,
            {
                ChannelType.guild_announcements,
            },
        ), (
            Channel.is_guild_store,
            {
                ChannelType.guild_store,
            },
        ), (
            Channel.is_thread,
            {
                ChannelType.thread,
            },
        ), (
            Channel.is_guild_thread_announcements,
            {
                ChannelType.guild_thread_announcements,
            },
        ), (
            Channel.is_guild_thread_public,
            {
                ChannelType.guild_thread_public,
            },
        ), (
            Channel.is_guild_thread_private,
            {
                ChannelType.guild_thread_private,
            },
        ), (
            Channel.is_guild_stage,
            {
                ChannelType.guild_stage,
            },
        ), (
            Channel.is_guild_directory,
            {
                ChannelType.guild_directory,
            },
        ), (
            Channel.is_guild_forum,
            {
                ChannelType.guild_forum,
            },
        ), (
            Channel.is_guild_media,
            {
                ChannelType.guild_media,
            },
        ),
    ):
        for channel_type in channel_types:
            yield channel_type, check, channel_type in passing_types


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__Channel__checks(channel_type, check):
    """
    Tests whether ``Channel`` checks work.
    
    Parameters
    ----------
    channel_type : ``ChannelType``
        The channel to create the channel with.
    check : `FunctionType`
        The check to call on the channel.
    
    Returns
    -------
    output : `bool`
    """
    return check(Channel(channel_type = channel_type))
