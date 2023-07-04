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
class ChannelType(PreinstancedBase):
    """
    Represents a channel's type.
    
    Attributes
    ----------
    name : `str`
        The channel type's name.
    value : `int`
        The identifier of the channel type.
    flags : ``ChannelTypeFlag``
        The flags of the channel type defining the channel type's specifications.
    metadata_type : `type<ChannelMetadataBase>`
        The respective metadata type of the channel.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``ChannelType``) items
        Stores the predefined ``ChannelType``-s. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The channel type' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the channel type modes.
    
    Every predefined channel type can be accessed as class attribute as well:
    
    +-------------------------------+-------------------------------+-------+-----------------------------------------------+
    | Class attribute name          | Name                          | Value | Metadata type                                 |
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
    
    INSTANCES = {}
    VALUE_TYPE = int
    
    @classmethod
    def _from_value(cls, value):
        """
        Creates a new channel type with the given value.
        
        Parameters
        ----------
        value : `int`
            The channel type's identifier value.
        
        Returns
        -------
        self : ``ChannelType``
            The created instance.
        """
        self = object.__new__(cls)
        self.name = cls.DEFAULT_NAME
        self.value = value
        self.flags = ChannelTypeFlag.all
        self.metadata_type = ChannelMetadataBase
        
        return self
    
    
    def __init__(self, value, name, metadata_type, flags):
        """
        Creates an ``ChannelType`` and stores it at the class's `.INSTANCES` class attribute as well.
        
        Parameters
        ----------
        value : `int`
            The Discord side identifier value of the channel type.
        name : `str`
            The default name of the channel type.
        metadata_type : `None`, `type<ChannelMetadataBase>`
            The channel type's respective metadata type.
        flags : ``ChannelTypeFlags``
            The flags of the channel type defining the channel type's specifications.
        """
        self.value = value
        self.name = name
        self.metadata_type = metadata_type
        self.flags = flags
        
        self.INSTANCES[value] = self
    
    
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
