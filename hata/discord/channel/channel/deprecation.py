__all__ = ()

import warnings

from scarletio import modulize

from ....utils.module_deprecation import deprecated_import

from .preinstanced import ChannelType


@deprecated_import
def get_channel_type_name(channel_type):
    """
    Returns the channel type's name.
    
    Parameters
    ----------
    channel_type : `int`, ``ChannelType``
        The channel type to get it's name.
    
    Returns
    -------
    channel_name : `str`
    """
    warnings.warn(
        '`get_channel_type_name` is deprecated and will be removed in 2023 January.',
        FutureWarning,
        stacklevel = 2,
    )
    
    if isinstance(channel_type, int):
        return ChannelType.get(channel_type).name
    
    if isinstance(channel_type, ChannelType):
        return channel_type.name
    
    return ''


@deprecated_import
def get_channel_type_names(channel_types):
    """
    Returns multiple channel type's names connected by comma.
    
    Parameters
    ----------
    channel_types : `iterable` of (`int`, ``ChannelType``)
        The channel types to get the their name.
    
    Returns
    -------
    channel_names : `str`
    """
    warnings.warn(
        '`get_channel_type_names` is deprecated and will be removed in 2023 January.',
        FutureWarning,
        stacklevel = 2,
    )
    
    return ', '.join(sorted(get_channel_type_name(channel_type) for channel_type in channel_types))


@deprecated_import
@modulize
class CHANNEL_TYPES:
    """
    Deprecated and will be removed in 2023 January.
    
    Contains channel type identifiers.
    
    +---------------------------------------+-------+
    | Name                                  | Value |
    +=======================================+=======+
    | guild_text                            | 0     |
    +---------------------------------------+-------+
    | private                               | 1     |
    +---------------------------------------+-------+
    | guild_voice                           | 2     |
    +---------------------------------------+-------+
    | private_group                         | 3     |
    +---------------------------------------+-------+
    | guild_category                        | 4     |
    +---------------------------------------+-------+
    | guild_announcements                   | 5     |
    +---------------------------------------+-------+
    | guild_store                           | 6     |
    +---------------------------------------+-------+
    | thread                                | 9     |
    +---------------------------------------+-------+
    | guild_thread_announcements            | 10    |
    +---------------------------------------+-------+
    | guild_thread_public                   | 11    |
    +---------------------------------------+-------+
    | guild_thread_private                  | 12    |
    +---------------------------------------+-------+
    | guild_stage                           | 13    |
    +---------------------------------------+-------+
    | guild_directory                       | 14    |
    +---------------------------------------+-------+
    | guild_forum                           | 15    |
    +---------------------------------------+-------+
    
    In addition also extra groups are defined:
    
    +---------------------------------------+-------------------------------+
    | Name                                  | Elements                      |
    +=======================================+===============================+
    | GROUP_MESSAGEABLE                     | guild_text,                   |
    |                                       | private,                      |
    |                                       | guild_voice,                  |
    |                                       | private_group,                |
    |                                       | guild_announcements,          |
    |                                       | guild_thread_announcements,   |
    |                                       | guild_thread_public,          |
    |                                       | guild_thread_private          |
    +---------------------------------------+-------------------------------+
    | GROUP_GUILD_MESSAGEABLE               | guild_text,                   |
    |                                       | guild_voice,                  |
    |                                       | guild_announcements,          |
    |                                       | guild_thread_announcements,   |
    |                                       | guild_thread_public,          |
    |                                       | guild_thread_private          |
    +---------------------------------------+-------------------------------+
    | GROUP_GUILD_MAIN_TEXT                 | guild_text,                   |
    |                                       | guild_announcements           |
    +---------------------------------------+-------------------------------+
    | GROUP_CONNECTABLE                     | private,                      |
    |                                       | guild_voice,                  |
    |                                       | private_group,                |
    |                                       | guild_stage                   |
    +---------------------------------------+-------------------------------+
    | GROUP_GUILD_CONNECTABLE               | guild_voice,                  |
    |                                       | guild_stage                   |
    +---------------------------------------+-------------------------------+
    | GROUP_PRIVATE                         | private,                      |
    |                                       | private_group                 |
    +---------------------------------------+-------------------------------+
    | GROUP_GUILD                           | guild_text,                   |
    |                                       | guild_voice,                  |
    |                                       | guild_category,               |
    |                                       | guild_announcements,          |
    |                                       | guild_store,                  |
    |                                       | guild_thread_announcements,   |
    |                                       | guild_thread_public,          |
    |                                       | guild_thread_private,         |
    |                                       | guild_stage,                  |
    |                                       | guild_directory,              |
    |                                       | guild_forum                   |
    +---------------------------------------+-------------------------------+
    | GROUP_THREAD                          | guild_thread_announcements,   |
    |                                       | guild_thread_public,          |
    |                                       | guild_thread_private          |
    +---------------------------------------+-------------------------------+
    | GROUP_CAN_CONTAIN_THREADS             | guild_text,                   |
    |                                       | guild_announcements,          |
    |                                       | guild_forum                   |
    +---------------------------------------+-------------------------------+
    | GROUP_IN_PRODUCTION                   | guild_text,                   |
    |                                       | private,                      |
    |                                       | guild_voice,                  |
    |                                       | private_group,                |
    |                                       | guild_category,               |
    |                                       | guild_announcements,          |
    |                                       | guild_thread_announcements,   |
    |                                       | guild_thread_public,          |
    |                                       | guild_thread_private,         |
    |                                       | guild_stage,                  |
    |                                       | guild_directory,              |
    |                                       | guild_forum                   |
    +---------------------------------------+-------------------------------+
    | GROUP_CAN_CREATE_INVITE_TO            | guild_text,                   |
    |                                       | guild_voice,                  |
    |                                       | private_group,                |
    |                                       | guild_announcements,          |
    |                                       | guild_store,                  |
    |                                       | guild_stage,                  |
    |                                       | guild_directory               |
    +---------------------------------------+-------------------------------+
    | GROUP_GUILD_MOVABLE                   | guild_text,                   |
    |                                       | guild_voice,                  |
    |                                       | guild_category,               |
    |                                       | guild_announcements,          |
    |                                       | guild_store,                  |
    |                                       | guild_stage,                  |
    |                                       | guild_directory,              |
    |                                       | guild_forum                   |
    +---------------------------------------+-------------------------------+
    """
    guild_text = 0
    private = 1
    guild_voice = 2
    private_group = 3
    guild_category = 4
    guild_announcements = 5
    guild_store = 6
    # 7? Not in use
    # 8? Not in use
    thread = 9 # Not in use
    guild_thread_announcements = 10
    guild_thread_public = 11
    guild_thread_private = 12
    guild_stage = 13
    guild_directory = 14
    guild_forum = 15
    
    
    GROUP_MESSAGEABLE = frozenset((
        guild_text,
        private,
        guild_voice,
        private_group,
        guild_announcements,
        guild_thread_announcements,
        guild_thread_public,
        guild_thread_private,
    ))
    
    
    GROUP_GUILD_MESSAGEABLE = frozenset((
        guild_text,
        guild_voice,
        guild_announcements,
        guild_thread_announcements,
        guild_thread_public,
        guild_thread_private,
    ))
    
    
    GROUP_GUILD_MAIN_TEXT = frozenset((
        guild_text,
        guild_announcements,
    ))
    
    
    GROUP_CONNECTABLE = frozenset((
        private,
        guild_voice,
        private_group,
        guild_stage,
    ))
    
    
    GROUP_GUILD_CONNECTABLE = frozenset((
        guild_voice,
        guild_stage,
    ))
    
    
    GROUP_PRIVATE = frozenset((
        private,
        private_group,
    ))
    
    
    GROUP_GUILD = frozenset((
        guild_text,
        guild_voice,
        guild_category,
        guild_announcements,
        guild_store,
        guild_thread_announcements,
        guild_thread_public,
        guild_thread_private,
        guild_stage,
        guild_directory,
        guild_forum,
    ))
    
    
    GROUP_THREAD = frozenset((
        guild_thread_announcements,
        guild_thread_public,
        guild_thread_private,
    ))
    
    
    GROUP_CAN_CONTAIN_THREADS = frozenset((
        guild_text,
        guild_announcements,
        guild_forum,
    ))
    
    
    GROUP_IN_PRODUCTION = frozenset((
        guild_text,
        private,
        guild_voice,
        private_group,
        guild_category,
        guild_announcements,
        guild_thread_announcements,
        guild_thread_public,
        guild_thread_private,
        guild_stage,
        guild_directory,
        guild_forum,
    ))
    
    
    GROUP_CAN_CREATE_INVITE_TO = frozenset((
        guild_text,
        guild_voice,
        private_group,
        guild_announcements,
        guild_store,
        guild_stage,
        guild_directory,
        
    ))
    
    GROUP_GUILD_MOVABLE = frozenset((
        guild_text,
        guild_voice,
        guild_category,
        guild_announcements,
        guild_store,
        guild_stage,
        guild_directory,
        guild_forum,
    ))
    
    
    CHANNEL_TYPE_NAMES = {
        guild_text: 'guild text',
        private: 'guild private',
        guild_voice: 'guild voice',
        private_group: 'private group',
        guild_category: 'guild category',
        guild_announcements: 'guild announcements',
        guild_store: 'guild store',
        thread: 'thread',
        guild_thread_announcements: 'guild thread announcements',
        guild_thread_public: 'guild thread public',
        guild_thread_private: 'guild thread private',
        guild_stage: 'guild stage',
        guild_directory: 'guild directory',
        guild_forum: 'guild forum',
    }
    
    
    DEFAULT_CHANNEL_TYPE_NAME = 'unknown'
    
    
    get_channel_type_name = get_channel_type_name
    get_channel_type_names = get_channel_type_names
