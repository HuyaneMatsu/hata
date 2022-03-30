__all__ = ()

import warnings

from scarletio import copy_docs, include

from ...utils.module_deprecation import deprecated_import

from . import channel_types as CHANNEL_TYPES


Channel = include('Channel')

class DeprecatedChannelMetType(type):
    """
    Meta type for the old deprecated channels warning about deprecation when instance or subtype checking.
    """
    def __instancecheck__(cls, instance):
        warnings.warn(
            f'`{cls.__name__}` is deprecated and will be removed in 2022. Please use `{Channel.__name__}` instead.',
            FutureWarning,
            stacklevel = 2,
        )
        
        return isinstance(instance, Channel) and instance.type in cls.allowed_types
    
    def __subclasscheck__(cls, klass):
        warnings.warn(
            f'`{cls.__name__}` is deprecated and will be removed in 2022. Please use `{Channel.__name__}` instead.',
            FutureWarning,
            stacklevel = 2,
        )
        
        return issubclass(klass, Channel) or (klass is cls)


@deprecated_import
class ChannelBase(metaclass=DeprecatedChannelMetType):
    """
    Deprecated and will be removed in 2022 August. Please use the ``Channel`` type instead.
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
    
    type = 0
    
    @classmethod
    def precreate(cls, channel_id, **kwargs):
        channel_type = next(iter(cls.allowed_types))
        
        warnings.warn(
            (
                f'`{cls.__name__}.precreate(...)` is deprecated and will be removed in 2022 August. Please use: '
                f'`{Channel.__name__}.precreate(channel_id, channel_type={channel_type}, ...)` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        return Channel.precreate(channel_id, channel_type=channel_type, **kwargs)


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
    type = CHANNEL_TYPES.guild_category
    
    allowed_types = frozenset((
        CHANNEL_TYPES.guild_category,
    ))


@deprecated_import
@copy_docs(ChannelBase)
class ChannelDirectory(ChannelGuildMainBase):
    type = CHANNEL_TYPES.guild_directory
    
    allowed_types = frozenset((
        CHANNEL_TYPES.guild_directory,
    ))


@deprecated_import
@copy_docs(ChannelBase)
class ChannelForum(ChannelGuildMainBase):
    type = CHANNEL_TYPES.guild_forum
    
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
    type = CHANNEL_TYPES.guild_text
    
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
    type = CHANNEL_TYPES.guild_voice
    
    allowed_types = frozenset((
        CHANNEL_TYPES.guild_voice,
    ))


@deprecated_import
@copy_docs(ChannelBase)
class ChannelStage(ChannelVoiceBase):
    type = CHANNEL_TYPES.guild_stage
    
    allowed_types = frozenset((
        CHANNEL_TYPES.guild_stage,
    ))


@deprecated_import
@copy_docs(ChannelBase)
class ChannelPrivate(ChannelTextBase, ChannelBase):
    type = CHANNEL_TYPES.private
    
    allowed_types = frozenset((
        CHANNEL_TYPES.private,
    ))


@deprecated_import
@copy_docs(ChannelBase)
class ChannelGroup(ChannelTextBase, ChannelBase):
    type = CHANNEL_TYPES.private_group
    
    allowed_types = frozenset((
        CHANNEL_TYPES.private_group,
    ))


@deprecated_import
@copy_docs(ChannelBase)
class ChannelThread(ChannelGuildBase, ChannelTextBase):
    allowed_types = frozenset((
        CHANNEL_TYPES.guild_thread_announcements,
        CHANNEL_TYPES.guild_thread_public,
        CHANNEL_TYPES.guild_thread_private,
    ))
