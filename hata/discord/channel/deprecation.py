__all__ = ()

from scarletio import copy_docs

from ...utils.module_deprecation import deprecated_import

from .channel import Channel

from . import channel_types as CHANNEL_TYPES

@deprecated_import
class ChannelBase:
    """
    Deprecated and scheduled for remove. Please use the ``Channel`` type instead.
    """
    allowed_types = frozenset((
        CHANNEL_TYPES.guild_text,
        CHANNEL_TYPES.private,
        CHANNEL_TYPES.guild_voice,
        CHANNEL_TYPES.private_group,
        CHANNEL_TYPES.guild_category,
        CHANNEL_TYPES.guild_announcements,
        CHANNEL_TYPES.guild_store,
        CHANNEL_TYPES.thread,
        CHANNEL_TYPES.guild_thread_announcements,
        CHANNEL_TYPES.guild_thread_public,
        CHANNEL_TYPES.guild_thread_private,
        CHANNEL_TYPES.guild_stage,
        CHANNEL_TYPES.guild_directory,
        CHANNEL_TYPES.guild_forum,
    ))
    
    def __instancecheck__(cls, instance):
        return isinstance(instance, Channel) and instance.type in cls.allowed_types
    
    def __subclasscheck__(cls, klass):
        return issubclass(klass, Channel) or (klass is cls)


@deprecated_import
@copy_docs(ChannelBase)
class ChannelTextBase(ChannelBase):
    allowed_types = frozenset((
        CHANNEL_TYPES.guild_text,
        CHANNEL_TYPES.private,
        CHANNEL_TYPES.private_group,
        CHANNEL_TYPES.guild_announcements,
        CHANNEL_TYPES.thread,
        CHANNEL_TYPES.guild_thread_announcements,
        CHANNEL_TYPES.guild_thread_public,
        CHANNEL_TYPES.guild_thread_private,
    ))


@deprecated_import
@copy_docs(ChannelBase)
class ChannelGuildBase(ChannelBase):
    allowed_types = frozenset((
        CHANNEL_TYPES.guild_text,
        CHANNEL_TYPES.guild_voice,
        CHANNEL_TYPES.guild_category,
        CHANNEL_TYPES.guild_announcements,
        CHANNEL_TYPES.guild_store,
        CHANNEL_TYPES.guild_thread_announcements,
        CHANNEL_TYPES.guild_thread_public,
        CHANNEL_TYPES.guild_thread_private,
        CHANNEL_TYPES.guild_stage,
        CHANNEL_TYPES.guild_directory,
        CHANNEL_TYPES.guild_forum,
    ))


@deprecated_import
@copy_docs(ChannelBase)
class ChannelGuildMainBase(ChannelGuildBase):
    allowed_types = frozenset((
        CHANNEL_TYPES.guild_text,
        CHANNEL_TYPES.guild_voice,
        CHANNEL_TYPES.guild_category,
        CHANNEL_TYPES.guild_announcements,
        CHANNEL_TYPES.guild_store,
        CHANNEL_TYPES.guild_stage,
        CHANNEL_TYPES.guild_directory,
        CHANNEL_TYPES.guild_forum,
    ))


@deprecated_import
@copy_docs(ChannelBase)
class ChannelCategory(ChannelGuildMainBase):
    allowed_types = frozenset((
        CHANNEL_TYPES.guild_category,
    ))


@deprecated_import
@copy_docs(ChannelBase)
class ChannelDirectory(ChannelGuildMainBase):
    allowed_types = frozenset((
        CHANNEL_TYPES.guild_directory,
    ))


@deprecated_import
@copy_docs(ChannelBase)
class ChannelForum(ChannelGuildMainBase):
    allowed_types = frozenset((
        CHANNEL_TYPES.guild_forum,
    ))


@deprecated_import
@copy_docs(ChannelBase)
class ChannelStore(ChannelGuildMainBase):
    allowed_types = frozenset((
        CHANNEL_TYPES.guild_store,
    ))


@deprecated_import
@copy_docs(ChannelBase)
class ChannelText(ChannelGuildMainBase, ChannelTextBase):
    allowed_types = frozenset((
        CHANNEL_TYPES.guild_text,
        CHANNEL_TYPES.guild_announcements,
    ))


@deprecated_import
@copy_docs(ChannelBase)
class ChannelGuildUndefined(ChannelGuildMainBase):
    allowed_types = frozenset((
        7,
        8,
    ))


@deprecated_import
@copy_docs(ChannelBase)
class ChannelVoiceBase(ChannelGuildMainBase):
    allowed_types = frozenset((
        CHANNEL_TYPES.guild_voice,
        CHANNEL_TYPES.guild_stage,
    ))


@deprecated_import
@copy_docs(ChannelBase)
class ChannelVoice(ChannelVoiceBase):
    allowed_types = frozenset((
        CHANNEL_TYPES.guild_voice,
    ))


@deprecated_import
@copy_docs(ChannelBase)
class ChannelStage(ChannelVoiceBase):
    allowed_types = frozenset((
        CHANNEL_TYPES.guild_stage,
    ))


@deprecated_import
@copy_docs(ChannelBase)
class ChannelPrivate(ChannelBase, ChannelTextBase):
    
    allowed_types = frozenset((
        CHANNEL_TYPES.private,
    ))


@deprecated_import
@copy_docs(ChannelBase)
class ChannelGroup(ChannelBase, ChannelTextBase):
    
    allowed_types = frozenset((
        CHANNEL_TYPES.private_group,
    ))


@deprecated_import
@copy_docs(ChannelBase)
class ChannelThread(ChannelGuildBase, ChannelTextBase)
    allowed_types = frozenset((
        CHANNEL_TYPES.guild_thread_announcements,
        CHANNEL_TYPES.guild_thread_public,
        CHANNEL_TYPES.guild_thread_private,
    ))
