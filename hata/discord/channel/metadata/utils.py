__all__ = ()


from .base import ChannelMetadataBase
from .guild_announcements import ChannelMetadataGuildAnnouncements
from .guild_category import ChannelMetadataGuildCategory
from .guild_directory import ChannelMetadataGuildDirectory
from .guild_forum import ChannelMetadataGuildForum
from .guild_stage import ChannelMetadataGuildStage
from .guild_store import ChannelMetadataGuildStore
from .guild_text import ChannelMetadataGuildText
from .guild_thread_announcements import ChannelMetadataGuildThreadAnnouncements
from .guild_thread_private import ChannelMetadataGuildThreadPrivate
from .guild_thread_public import ChannelMetadataGuildThreadPublic
from .guild_voice import ChannelMetadataGuildVoice
from .private import ChannelMetadataPrivate
from .private_group import ChannelMetadataPrivateGroup


CHANNEL_METADATA_TYPES = {
    ChannelMetadataGuildAnnouncements.type: ChannelMetadataGuildAnnouncements,
    ChannelMetadataGuildCategory.type: ChannelMetadataGuildCategory,
    ChannelMetadataGuildDirectory.type: ChannelMetadataGuildDirectory,
    ChannelMetadataGuildForum.type: ChannelMetadataGuildForum,
    ChannelMetadataGuildStage.type: ChannelMetadataGuildStage,
    ChannelMetadataGuildStore.type: ChannelMetadataGuildStore,
    ChannelMetadataGuildText.type: ChannelMetadataGuildText,
    ChannelMetadataGuildThreadAnnouncements.type: ChannelMetadataGuildThreadAnnouncements,
    ChannelMetadataGuildThreadPrivate.type: ChannelMetadataGuildThreadPrivate,
    ChannelMetadataGuildThreadPublic.type: ChannelMetadataGuildThreadPublic,
    ChannelMetadataGuildVoice.type: ChannelMetadataGuildVoice,
    ChannelMetadataPrivate.type: ChannelMetadataPrivate,
    ChannelMetadataPrivateGroup.type: ChannelMetadataPrivateGroup,
}


def get_channel_metadata_type(channel_type_value):
    """
    Gets metadata type for the given channel type value.
    
    Parameters
    ----------
    channel_type_value : `int`
        The channel's type.
    
    Returns
    -------
    channel_metadata_type : ``ChannelMetadataBase``
    """
    return CHANNEL_METADATA_TYPES.get(channel_type_value, ChannelMetadataBase)
