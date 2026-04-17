__all__ = ('ChannelType', )

from scarletio import export

from ...bases import Preinstance as P, PreinstancedBase

from ..channel_metadata import (
    ChannelMetadataBase, ChannelMetadataGuildAnnouncements, ChannelMetadataGuildCategory, ChannelMetadataGuildDirectory,
    ChannelMetadataGuildForum, ChannelMetadataGuildMedia, ChannelMetadataGuildStage, ChannelMetadataGuildStore,
    ChannelMetadataGuildText, ChannelMetadataGuildThreadAnnouncements, ChannelMetadataGuildThreadPrivate,
    ChannelMetadataGuildThreadPublic, ChannelMetadataGuildVoice, ChannelMetadataPrivate, ChannelMetadataPrivateGroup
)


from .flags import ChannelTypeFlag


@export
class ChannelType(PreinstancedBase, value_type = int):
    """
    Represents a channel's type.
    
    Attributes
    ----------
    flags : ``ChannelTypeFlag``
        The flags of the channel type defining the channel type's specifications.
    
    name : `str`
        The channel type's name.
    
    metadata_type : `type<ChannelMetadataBase>`
        The respective metadata type of the channel.
    
    value : `int`
        The identifier of the channel type.
    
    Type Attributes
    ---------------
    Every predefined channel type can be accessed as type attribute as well:
    
    +-------------------------------+-------------------------------+-------+-----------------------------------------------+
    | Type attribute name           | Name                          | Value | Metadata type                                 |
    +===============================+===============================+=======+===============================================+
    | unknown                       | unknown                       | -1    | ``ChannelMetadataBase``                       |
    +-------------------------------+-------------------------------+-------+-----------------------------------------------+
    | guild_text                    | guild text                    | 0     | ``ChannelMetadataGuildText``                  |
    +-------------------------------+-------------------------------+-------+-----------------------------------------------+
    | private                       | private                       | 1     | ``ChannelMetadataPrivate``                    |
    +-------------------------------+-------------------------------+-------+-----------------------------------------------+
    | guild_voice                   | guild voice                   | 2     | ``ChannelMetadataGuildVoice``                 |
    +-------------------------------+-------------------------------+-------+-----------------------------------------------+
    | private_group                 | private group                 | 3     | ``ChannelMetadataPrivateGroup``               |
    +-------------------------------+-------------------------------+-------+-----------------------------------------------+
    | guild_category                | guild category                | 4     | ``ChannelMetadataGuildCategory``              |
    +-------------------------------+-------------------------------+-------+-----------------------------------------------+
    | guild_announcements           | guild announcements           | 5     | ``ChannelMetadataGuildAnnouncements``         |
    +-------------------------------+-------------------------------+-------+-----------------------------------------------+
    | guild_store                   | guild store                   | 6     | ``ChannelMetadataGuildStore``                 |
    +-------------------------------+-------------------------------+-------+-----------------------------------------------+
    | thread                        | thread                        | 9     | ``ChannelMetadataBase``                       |
    +-------------------------------+-------------------------------+-------+-----------------------------------------------+
    | guild_thread_announcements    | guild thread announcements    | 10    | ``ChannelMetadataGuildThreadAnnouncements``   |
    +-------------------------------+-------------------------------+-------+-----------------------------------------------+
    | guild_thread_public           | guild thread public           | 11    | ``ChannelMetadataGuildThreadPublic``          |
    +-------------------------------+-------------------------------+-------+-----------------------------------------------+
    | guild_thread_private          | guild thread private          | 12    | ``ChannelMetadataGuildThreadPrivate``         |
    +-------------------------------+-------------------------------+-------+-----------------------------------------------+
    | guild_stage                   | guild stage                   | 13    | ``ChannelMetadataGuildStage``                 |
    +-------------------------------+-------------------------------+-------+-----------------------------------------------+
    | guild_directory               | guild directory               | 14    | ``ChannelMetadataGuildDirectory``             |
    +-------------------------------+-------------------------------+-------+-----------------------------------------------+
    | guild_forum                   | guild forum                   | 15    | ``ChannelMetadataGuildForum``                 |
    +-------------------------------+-------------------------------+-------+-----------------------------------------------+
    | guild_media                   | guild media                   | 16    | ``ChannelMetadataGuildMedia``                 |
    +-------------------------------+-------------------------------+-------+-----------------------------------------------+
    """
    __slots__ = ('flags', 'metadata_type',)
    
    def __new__(cls, value, name = None, metadata_type = None, flags = ChannelTypeFlag.all):
        """
        Creates a new channel type.
        
        Parameters
        ----------
        value : `int`
            The Discord side identifier value of the channel type.
        
        name : `None | str` = `None`, Optional
            The default name of the channel type.
        
        metadata_type : `None | type<ChannelMetadataBase>` = `None`, Optional
            The channel type's respective metadata type.
        
        flags : ``ChannelTypeFlags`` = `ChannelTypeFlag.all`, Optional
            The flags of the channel type defining the channel type's specifications.
        """
        if metadata_type is None:
            metadata_type = ChannelMetadataBase
        
        self = PreinstancedBase.__new__(cls, value, name)
        self.metadata_type = metadata_type
        self.flags = flags
        return self
    
    
    unknown = P(
        -1,
        'unknown',
        ChannelMetadataBase,
        ChannelTypeFlag.all,
    )
    
    guild_text = P(
        0,
        'guild text',
        ChannelMetadataGuildText,
        ChannelTypeFlag().update_by_keys(
            connectable = False,
            guild = True,
            guild_sortable = True,
            guild_system = True,
            invitable = True,
            private = False,
            readable = True,
            textual = True,
            thread = False,
            threadable = True,
            forum = False,
        ),
    )
    
    private = P(
        1,
        'private',
        ChannelMetadataPrivate,
        ChannelTypeFlag().update_by_keys(
            connectable = True,
            guild = False,
            guild_sortable = False,
            guild_system = False,
            invitable = False,
            private = True,
            readable = True,
            textual = True,
            thread = False,
            threadable = False,
            forum = False,
        ),
    )
    
    guild_voice = P(
        2,
        'guild voice',
        ChannelMetadataGuildVoice,
        ChannelTypeFlag().update_by_keys(
            connectable = True,
            guild = True,
            guild_sortable = True,
            guild_system = False,
            invitable = True,
            private = False,
            readable = True,
            textual = True,
            thread = False,
            threadable = False,
            forum = False,
        ),
    )
    
    private_group = P(
        3,
        'private group',
        ChannelMetadataPrivateGroup,
        ChannelTypeFlag().update_by_keys(
            connectable = True,
            guild = False,
            guild_sortable = False,
            guild_system = False,
            invitable = True,
            private = True,
            readable = True,
            textual = True,
            thread = False,
            threadable = False,
            forum = False,
        ),
    )
    
    guild_category = P(
        4,
        'guild category',
        ChannelMetadataGuildCategory,
        ChannelTypeFlag().update_by_keys(
            connectable = False,
            guild = True,
            guild_sortable = True,
            guild_system = False,
            invitable = False,
            private = False,
            readable = False,
            textual = False,
            thread = False,
            threadable = False,
            forum = False,
        ),
    )
    
    guild_announcements = P(
        5,
        'guild announcements',
        ChannelMetadataGuildAnnouncements,
        ChannelTypeFlag().update_by_keys(
            connectable = False,
            guild = True,
            guild_sortable = True,
            guild_system = True,
            invitable = True,
            private = False,
            readable = True,
            textual = True,
            thread = False,
            threadable = True,
            forum = False,
        ),
    )
    
    guild_store = P(
        6,
        'guild store',
        ChannelMetadataGuildStore,
        ChannelTypeFlag().update_by_keys(
            connectable = False,
            guild = True,
            guild_sortable = True,
            guild_system = False,
            invitable = True,
            private = False,
            readable = False,
            textual = False,
            thread = False,
            threadable = False,
            forum = False,
        )
    )
    
    thread = P(
        9,
        'thread',
        ChannelMetadataBase,
        ChannelTypeFlag().update_by_keys(
            connectable = False,
            guild = False,
            guild_sortable = False,
            guild_system = False,
            invitable = False,
            private = False,
            readable = True,
            textual = True,
            thread = True,
            threadable = False,
            forum = False,
        ),
    )
    
    guild_thread_announcements = P(
        10,
        'guild thread announcements',
        ChannelMetadataGuildThreadAnnouncements,
        ChannelTypeFlag().update_by_keys(
            connectable = False,
            guild = True,
            guild_sortable = False,
            guild_system = False,
            invitable = False,
            private = False,
            readable = True,
            textual = True,
            thread = True,
            threadable = False,
            forum = False,
        ),
    )
    
    guild_thread_public = P(
        11,
        'guild thread public',
        ChannelMetadataGuildThreadPublic,
        ChannelTypeFlag().update_by_keys(
            connectable = False,
            guild = True,
            guild_sortable = False,
            guild_system = False,
            invitable = False,
            private = False,
            readable = True,
            textual = True,
            thread = True,
            threadable = False,
            forum = False,
        ),
    )
    
    guild_thread_private = P(
        12,
        'guild thread private',
        ChannelMetadataGuildThreadPrivate,
        ChannelTypeFlag().update_by_keys(
            connectable = False,
            guild = True,
            guild_sortable = False,
            guild_system = False,
            invitable = False,
            private = False,
            readable = True,
            textual = True,
            thread = True,
            threadable = False,
            forum = False,
        ),
    )
    
    guild_stage = P(
        13,
        'guild stage',
        ChannelMetadataGuildStage,
        ChannelTypeFlag().update_by_keys(
            connectable = True,
            guild = True,
            guild_sortable = True,
            guild_system = False,
            invitable = True,
            private = False,
            readable = False,
            textual = True,
            thread = False,
            threadable = False,
            forum = False,
        )
    )
    
    guild_directory = P(
        14,
        'guild directory',
        ChannelMetadataGuildDirectory,
        ChannelTypeFlag().update_by_keys(
            connectable = False,
            guild = True,
            guild_sortable = True,
            guild_system = False,
            invitable = True,
            private = False,
            readable = True,
            textual = False,
            thread = False,
            threadable = False,
            forum = False,
        ),
    )
    
    guild_forum = P(
        15,
        'guild forum',
        ChannelMetadataGuildForum,
        ChannelTypeFlag().update_by_keys(
            connectable = False,
            guild = True,
            guild_sortable = True,
            guild_system = False,
            invitable = True,
            private = False,
            readable = True,
            textual = False,
            thread = False,
            threadable = True,
            forum = True,
        ),
    )

    guild_media = P(
        16,
        'guild media',
        ChannelMetadataGuildMedia,
        ChannelTypeFlag().update_by_keys(
            connectable = False,
            guild = True,
            guild_sortable = True,
            guild_system = False,
            invitable = True,
            private = False,
            readable = True,
            textual = False,
            thread = False,
            threadable = True,
            forum = True,
        ),
    )
