__all__ = ()

from ..application import Entitlement, Subscription
from ..application_command import ApplicationCommand
from ..auto_moderation import AutoModerationRule
from ..bases import maybe_snowflake, maybe_snowflake_pair, maybe_snowflake_token_pair
from ..channel import Channel, ForumTag, PermissionOverwrite
from ..core import (
    APPLICATION_COMMANDS, AUTO_MODERATION_RULES, CHANNELS, EMBEDDED_ACTIVITIES, EMOJIS, FORUM_TAGS, GUILDS, MESSAGES,
    ROLES, SCHEDULED_EVENTS, SOUNDBOARD_SOUNDS, STICKERS, STICKER_PACKS, SUBSCRIPTIONS, USERS
)
from ..embedded_activity import EmbeddedActivity
from ..emoji import Emoji, Reaction, ReactionType
from ..guild import Guild
from ..message import Message
from ..oauth2 import Achievement, Oauth2Access, Oauth2User
from ..role import Role
from ..poll import PollAnswer
from ..scheduled_event import ScheduledEvent
from ..soundboard import SoundboardSound
from ..stage import Stage
from ..sticker import Sticker, StickerPack
from ..user import ClientUserBase
from ..webhook import Webhook


def validate_message_to_delete(message):
    """
    Validates a message to delete.
    
    Parameters
    ----------
    message : ``Message``, `tuple` (`int`, `int`)
        The message to validate for deletion.
    
    Returns
    -------
    channel_id : `int`
        The channel's identifier where the message is.
    message_id : `int`
        The message's identifier.
    message : `None`, ``Message``
        The referenced message if found.
    
    Raises
    ------
    TypeError
        If message was not given neither as ``Message``, `tuple` (`int`, `int`).
    """
    if isinstance(message, Message):
        channel_id = message.channel_id
        message_id = message.id
    else:
        snowflake_pair = maybe_snowflake_pair(message)
        if snowflake_pair is None:
            raise TypeError(
                f'`message` can be `{Message.__name__}`, '
                f'`tuple` of (`int`, `int`), got {type(message).__name__}; {message!r}.'
            )
        
        channel_id, message_id = snowflake_pair
        
        message = MESSAGES.get(message, None)
    
    return channel_id, message_id, message


def get_channel_id(channel, type_checker):
    """
    Gets the channel's identifier from the given channel or of it's identifier.
    
    Parameters
    ----------
    channel : ``Channel``, `int`
        The channel, or it's identifier.
    type_checker : `FunctionType`
        Type checker for `channel`.
    
    Returns
    -------
    channel_id : `int`
        The channel's identifier.
    
    Raises
    ------
    TypeError
        If `channel`'s type is incorrect.
    """
    if isinstance(channel, Channel):
        if type_checker(channel) or channel.partial:
            return channel.id
    
    else:
        channel_id = maybe_snowflake(channel)
        if (channel_id is not None):
            return channel_id
        
    raise TypeError(
        f'`channel` can be `{Channel.__name__}`, `int`,  passing the `{type_checker.__name__}` check, '
        f'got {channel.__class__.__name__}; {channel!r}.'
    )


def get_channel_guild_id_and_id(channel, type_checker):
    """
    Gets the channel's and it's guild's identifier from the given channel or of it's identifier.
    
    Parameters
    ----------
    channel : ``Channel``, `tuple` (`int`, `int`)
        The role, or `guild-id`, `role-id` pair.
    type_checker : `FunctionType`
        Type checker for `channel`.
    
    Returns
    -------
    snowflake_pair : `tuple` (`int`, `int`)
        The channel's guild's and it's own identifier if applicable.
    
    Raises
    ------
    TypeError
        If `channel`'s type is incorrect.
    """
    if isinstance(channel, Channel):
        if type_checker(channel) or channel.partial:
            return channel.guild_id, channel.id
    
    else:
        snowflake_pair = maybe_snowflake_pair(channel)
        if (snowflake_pair is not None):
            return snowflake_pair
    
    raise TypeError(
        f'`channel` can be `{Channel.__name__}`, `tuple` (`int`, `int`),  passing the `{type_checker.__name__}` check, '
        f'got {channel.__class__.__name__}; {channel!r}.'
    )


def build_get_channel_and_id_error_message(channel, type_checker):
    """
    Builds error message for `get_channel_and_id`.
    
    Parameters
    ----------
    channel : `object`
        The object that was passed as `channel`.
    type_checker : `None | FunctionType`
        Type checker for `channel`.
    
    Returns
    -------
    error_message : `str`
    """
    parts = ['`channel` can be `', Channel.__name__, '`, `int`']
    
    if (type_checker is not None):
        parts.append(', passing the `')
        parts.append(type_checker.__name__)
        parts.append('` check')
    
    parts.append(', got ')
    parts.append(type(channel).__name__)
    parts.append('; ')
    parts.append(repr(channel))
    parts.append('.')
    
    return ''.join(parts)


def get_channel_and_id(channel, type_checker = None):
    """
    Gets thread channel and it's identifier from the given thread channel or of it's identifier.
    
    Parameters
    ----------
    channel : ``Channel``, `int`
        The channel, or it's identifier.
    type_checker : `None | FunctionType` = `None`, Optional
        Type checker for `channel`.
    
    Returns
    -------
    channel : `None`, ``Channel``
        The channel if found.
    channel_id : `int`
        The channel's identifier.
    
    Raises
    ------
    TypeError
        If `channel`'s type is incorrect.
    """
    while True:
        if isinstance(channel, Channel):
            if (type_checker is None) or type_checker(channel) or channel.partial:
                channel_id = channel.id
                break
        
        else:
            channel_id = maybe_snowflake(channel)
            if (channel_id is not None):
                try:
                    channel = CHANNELS[channel_id]
                except KeyError:
                    channel = None
                    break
                
                if (type_checker is None) or type_checker(channel) or channel.partial:
                    channel_id = channel.id
                    break
        
        raise TypeError(build_get_channel_and_id_error_message(channel, type_checker))
    
    return channel, channel_id


def get_stage_and_channel_id(stage):
    """
    Gets the stage an its channel's identifier.
    
    Parameters
    ----------
    stage : `Stage`, ``Channel``, `int`
        The stage, or it's identifier.
    
    Returns
    -------
    stage : `None`, ``Stage``
        The identified stage if any.
    channel_id : `int`
        The channel's identifier.
    
    Raises
    ------
    TypeError
        If `stage`'s type is incorrect.
    """
    while True:
        if isinstance(stage, Stage):
            channel_id = stage.channel.id
            break
        
        elif isinstance(stage, Channel):
            if stage.is_guild_stage() or stage.partial:
                channel_id = stage.id
                stage = None
                break
        
        else:
            channel_id = maybe_snowflake(stage)
            if (channel_id is not None):
                stage = None
                break
        
        raise TypeError(
            f'`stage` can be `{Stage.__name__}`, `{Channel.__name__}`, `int`, got '
            f'{stage.__class__.__name__}; {stage!r}.'
        )
    
    return stage, channel_id


def get_stage_channel_id(stage):
    """
    Gets stage's channel's identifier from the given stage or of it's identifier.
    
    Parameters
    ----------
    stage : `Stage`, ``Channel``, `int`
        The stage, or it's identifier.
    
    Returns
    -------
    channel_id : `int`
        The channel's identifier.
    
    Raises
    ------
    TypeError
        If `stage`'s type is incorrect.
    """
    while True:
        if isinstance(stage, Stage):
            channel_id = stage.channel.id
            break
        
        elif isinstance(stage, Channel):
            if stage.is_guild_stage() or stage.partial:
                channel_id = stage.id
                break
        
        else:
            channel_id = maybe_snowflake(stage)
            if (channel_id is not None):
                break
        
        raise TypeError(
            f'`stage` can be `{Stage.__name__}`, `{Channel.__name__}`, `int`, got '
            f'{stage.__class__.__name__}; {stage!r}.'
        )
    
    return channel_id


def get_user_id(user):
    """
    Gets user identifier from the given user or of it's identifier.
    
    Parameters
    ----------
    user : ``ClientUserBase``, `int`
        The user, or it's identifier.
    
    Returns
    -------
    user_id : `int`
        The user's identifier.
    
    Raises
    ------
    TypeError
        If `user`'s type is incorrect.
    """
    if isinstance(user, ClientUserBase):
        return user.id
    
    user_id = maybe_snowflake(user)
    if (user_id is not None):
        return user_id
    
    raise TypeError(
        f'`user` can be `{ClientUserBase.__name__}`, `int`, got {user.__class__.__name__}; {user!r}.'
    )


def get_user_and_id(user):
    """
    Gets user and it's identifier from the given user or of it's identifier.
    
    Parameters
    ----------
    user : ``ClientUserBase``, `int`
        The user, or it's identifier.
    
    Returns
    -------
    user : `None`, ``ClientUserBase``
        The user if found.
    user_id : `int`
        The user's identifier.
    
    Raises
    ------
    TypeError
        If `user`'s type is incorrect.
    """
    while True:
        if isinstance(user, ClientUserBase):
            user_id = user.id
            break
        
        user_id = maybe_snowflake(user)
        if (user_id is not None):
            try:
                user = USERS[user_id]
            except KeyError:
                user = None
                break
            
            if isinstance(user, ClientUserBase):
                break
        
        raise TypeError(
            f'`user` can be `{ClientUserBase.__name__}`, `int`, got {user.__class__.__name__}; {user!r}.'
        )
        
    return user, user_id


def get_user_id_nullable(user):
    """
    Gets user identifier from the given user or of it's identifier.
    
    > The user can be `None`. At that case `user_id` will default to `0`.
    
    Parameters
    ----------
    user : `None`, ``ClientUserBase``, `int`
        The user, or it's identifier.
    
    Returns
    -------
    user_id : `int`
        The user's identifier.
    
    Raises
    ------
    TypeError
        If `user`'s type is incorrect.
    """
    if user is None:
        return 0
    
    if isinstance(user, ClientUserBase):
        return user.id
    
    user_id = maybe_snowflake(user)
    if (user_id is not None):
        return user_id
        
    raise TypeError(
        f'`user` can be `{ClientUserBase.__name__}`, `int`, got {user.__class__.__name__}; {user!r}.'
    )


def get_guild_id(guild):
    """
    Gets the guild's identifier from the given guild or of it's identifier.
    
    Parameters
    ----------
    guild : ``Guild``, `int`
        The guild, or it's identifier.
    
    Returns
    -------
    guild_id : `int`
        The guild's identifier.
    
    Raises
    ------
    TypeError
        If `guild`'s type is incorrect.
    """
    if isinstance(guild, Guild):
        return guild.id
    
    guild_id = maybe_snowflake(guild)
    if (guild_id is not None):
        return guild_id
        
    raise TypeError(
        f'`guild` can be `{Guild.__name__}`, `int`, got {guild.__class__.__name__}; {guild!r}.'
    )


def get_guild_and_id(guild):
    """
    Gets the guild and it's identifier from the given guild or of it's identifier.
    
    Parameters
    ----------
    guild : ``Guild``, `int`
        The guild, or it's identifier.
    
    Returns
    -------
    guild : `None`, ``Guild``
        The guild if found.
    guild_id : `int`
        The guild's identifier.
    
    Raises
    ------
    TypeError
        If `guild`'s type is incorrect.
    """
    if isinstance(guild, Guild):
        guild_id = guild.id
    else:
        guild_id = maybe_snowflake(guild)
        if guild_id is None:
            raise TypeError(
                f'`guild` can be `{Guild.__name__}`, `int`, got {guild.__class__.__name__}; {guild!r}.'
            )
        
        guild = GUILDS.get(guild_id, None)
    
    return guild, guild_id


def get_achievement_id(achievement):
    """
    Gets the achievement identifier from the given achievement or of it's identifier.
    
    Parameters
    ----------
    achievement : ``Achievement``, `int`
        The achievement, or it's identifier.
    
    Returns
    -------
    achievement_id : `int`
        The achievement's identifier.
    
    Raises
    ------
    TypeError
        If `achievement`'s type is incorrect.
    """
    if isinstance(achievement, Achievement):
        achievement_id = achievement.id
    else:
        achievement_id = maybe_snowflake(achievement)
        if achievement_id is None:
            raise TypeError(
                f'`achievement` can be `{Achievement.__name__}`, `int`, got '
                f'{achievement.__class__.__name__}; {achievement!r}.'
            )
    
    return achievement_id


def get_achievement_and_id(achievement):
    """
    Gets the achievement and it's identifier from the given achievement or of it's identifier.
    
    Parameters
    ----------
    achievement : ``Achievement``, `int`
        The achievement, or it's identifier.
    
    Returns
    -------
    achievement : ``Achievement``, `None`
        The achievement if found.
    achievement_id : `int`
        The achievement's identifier.
    
    Raises
    ------
    TypeError
        If `achievement`'s type is incorrect.
    """
    if isinstance(achievement, Achievement):
        achievement_id = achievement.id
    else:
        achievement_id = maybe_snowflake(achievement)
        if achievement_id is None:
            raise TypeError(
                f'`achievement` can be `{Achievement.__name__}`, `int`, got '
                f'{achievement.__class__.__name__}; {achievement!r}.'
            )
        
        achievement = None
    
    return achievement, achievement_id


def get_channel_id_and_message_id(message):
    """
    Gets the message's channel's and it's own identifier.
    
    Parameters
    ----------
    message : ``Message``, `tuple` (`int`, `int`)
        The message or it' representation.
    
    Returns
    -------
    channel_id : `int`
        The message's channel's identifier.
    message_id : `int`
        The message's identifier.
    
    Raises
    ------
    TypeError
        If `message`'s type is incorrect.
    """
    # 1.: Message
    # 4.: None -> raise
    # 5.: `tuple` (`int`, `int`)
    # 6.: raise
    if isinstance(message, Message):
        channel_id = message.channel_id
        message_id = message.id
    elif message is None:
        raise TypeError(
            '`message` was given as `None`. Make sure to call message create methods with non-empty content(s).'
        )
    else:
        snowflake_pair = maybe_snowflake_pair(message)
        if snowflake_pair is None:
            raise TypeError(
                f'`message` can be `{Message.__name__}`, '
                f'`tuple` of (`int`, `int`), got {message.__class__.__name__}; {message!r}.'
            )
        
        channel_id, message_id = snowflake_pair
    
    return channel_id, message_id


def get_message_and_channel_id_and_message_id(message):
    """
    Gets the message's channel's and it's own identifier.
    
    Parameters
    ----------
    message : ``Message``, `tuple` (`int`, `int`)
        The message or it' representation.
    
    Returns
    -------
    message : `None`, ``Message``
        The message in context if found.
    channel_id : `int`
        The message's channel's identifier.
    message_id : `int`
        The message's identifier.
    
    Raises
    ------
    TypeError
        If `message`'s type is incorrect.
    """
    # 1.: Message
    # 4.: None -> raise
    # 5.: `tuple` (`int`, `int`)
    # 6.: raise
    if isinstance(message, Message):
        channel_id = message.channel_id
        message_id = message.id
    elif message is None:
        raise TypeError(
            '`message` was given as `None`. Make sure to call message create methods with non-empty content(s).'
        )
    else:
        snowflake_pair = maybe_snowflake_pair(message)
        if snowflake_pair is None:
            raise TypeError(
                f'`message` can be `{Message.__name__}`, '
                f'`tuple` of (`int`, `int`), got {message.__class__.__name__}; {message!r}.'
            )
        
        channel_id, message_id = snowflake_pair
        message = MESSAGES.get(message_id, None)
    
    return message, channel_id, message_id


def get_role_id(role):
    """
    Gets the role identifier from the given role or of it's identifier.
    
    Parameters
    ----------
    role : ``Role``, `int`
        The role, or it's identifier.
    
    Returns
    -------
    role_id : `int`
        The role's identifier.
    
    Raises
    ------
    TypeError
        If `role`'s type is incorrect.
    """
    if isinstance(role, Role):
        role_id = role.id
    else:
        role_id = maybe_snowflake(role)
        if role_id is None:
            raise TypeError(
                f'`role` can be `{Role.__name__}`, `int`, got {role.__class__.__name__}; {role!r}.'
            )
    
    return role_id


def get_role_role_guild_id_and_id(role):
    """
    Gets the role identifier from the given role or of it's identifier.
    
    Parameters
    ----------
    role : ``Role``, `tuple` (`int`, `int`)
        The role, or a `guild-id`, `role-id` pair.
    
    Returns
    -------
    role : `None`, ``Role``
        The respective role.
    
    guild_id : `int`
        The role's guild's identifier.
    
    role_id : `int`
        The role's identifier.
    
    Raises
    ------
    TypeError
        If `role`'s type is incorrect.
    """
    if isinstance(role, Role):
        role_id = role.id
        guild_id = role.guild_id
    
    else:
        snowflake_pair = maybe_snowflake_pair(role)
        if snowflake_pair is None:
            raise TypeError(
                f'`role` can be `{Role.__name__}`, `tuple` (`int`, `int`), got {role.__class__.__name__}; {role!r}.'
            )
        
        guild_id, role_id = snowflake_pair
        role = ROLES.get(role_id, None)
    
    return role, guild_id, role_id


def get_role_guild_id_and_id(role):
    """
    Gets the role's and it's guild's identifier from the given role or of a `guild-id`, `role-id` pair.
    
    Parameters
    ----------
    role : ``Role``, `tuple` (`int`, `int`)
        The role, or a `guild-id`, `role-id` pair.
    
    Returns
    -------
    guild_id : `int`
        The role's guild's identifier.
    
    role_id : `int`
        The role's identifier.
    
    Raises
    ------
    TypeError
        If `role`'s type is incorrect.
    """
    if isinstance(role, Role):
        return role.guild_id, role.id
    
    snowflake_pair = maybe_snowflake_pair(role)
    if snowflake_pair is not None:
        return snowflake_pair
    
    raise TypeError(
        f'`role` can be `{Role.__name__}`, `tuple` (`int`, `int`), got {role.__class__.__name__}; {role!r}.'
    )


def get_webhook_id(webhook):
    """
    Gets the webhook's identifier from the given webhook or of it's identifier.
    
    Parameters
    ----------
    webhook : ``Webhook``, `int`
        The webhook, or it's identifier.
    
    Returns
    -------
    webhook_id : `int`
        The webhook's identifier.
    
    Raises
    ------
    TypeError
        If `webhook`'s type is incorrect.
    """
    if isinstance(webhook, Webhook):
        webhook_id = webhook.id
    else:
        webhook_id = maybe_snowflake(webhook)
        if webhook_id is None:
            raise TypeError(
                f'`webhook` can be `{Webhook.__name__}`, `int`, got {webhook.__class__.__name__}; {webhook!r}.'
            )
    
    return webhook_id


def get_webhook_and_id(webhook):
    """
    Gets the webhook and it's identifier from the given webhook or of it's identifier.
    
    Parameters
    ----------
    webhook : ``Webhook``, `int`
        The webhook, or it's identifier.
    
    Returns
    -------
    webhook : ``Webhook``, `None`
        The webhook if any.
    webhook_id : `int`
        The webhook's identifier.
    
    Raises
    ------
    TypeError
        If `webhook`'s type is incorrect.
    """
    while True:
        if isinstance(webhook, Webhook):
            webhook_id = webhook.id
            break
        
        webhook_id = maybe_snowflake(webhook)
        if (webhook_id is not None):
            try:
                webhook = USERS[webhook_id]
            except KeyError:
                webhook = None
                break
            
            if isinstance(webhook, Webhook):
                break
            
            raise TypeError(
                f'`webhook` can be `{Webhook.__name__}`, `int`, got {webhook.__class__.__name__}; {webhook!r}.'
            )
    
    return webhook, webhook_id


def get_webhook_id_and_token(webhook):
    """
    Gets the webhook's identifier and token from the given webhook or it's token, identifier pair.
    
    Parameters
    ----------
    webhook : ``Webhook``, `tuple` (`int`, `str`)
        The webhook or it's id and token.
    
    Returns
    -------
    webhook_id : `int`
        The webhook's identifier.
    webhook_token : `str`
        The webhook's token.
    
    Raises
    ------
    TypeError
        If `webhook`'s type is incorrect.
    """
    if isinstance(webhook, Webhook):
        snowflake_token_pair = webhook.id, webhook.token
    else:
        snowflake_token_pair = maybe_snowflake_token_pair(webhook)
        if (snowflake_token_pair is None):
            raise TypeError(
                f'`webhook` can be `{Webhook.__name__}`, `tuple` (`int`, `str`), got '
                f'{webhook.__class__.__name__}; {webhook!r}.'
            )
    
    return snowflake_token_pair


def get_webhook_and_id_and_token(webhook):
    """
    Gets the webhook, it's identifier and token from the given webhook or it's token, identifier pair.
    
    Parameters
    ----------
    webhook : ``Webhook``, `tuple` (`int`, `str`)
        The webhook or it's id and token.
    
    Returns
    -------
    webhook : ``Webhook``, `None`
        The webhook if any.
    webhook_id : `int`
        The webhook's identifier.
    webhook_token : `str`
        The webhook's token.
    
    Raises
    ------
    TypeError
        If `webhook`'s type is incorrect.
    """
    while True:
        if isinstance(webhook, Webhook):
            webhook_id = webhook.id
            webhook_token = webhook.token
            break
        
        snowflake_token_pair = maybe_snowflake_token_pair(webhook)
        if (snowflake_token_pair is not None):
            webhook_id, webhook_token = snowflake_token_pair
            
            try:
                webhook = USERS[webhook_id]
            except KeyError:
                webhook = None
                break
            
            if isinstance(webhook, Webhook):
                break
        
        raise TypeError(
            f'`webhook` can be `{Webhook.__name__}`, `tuple` (`int`, `str`), got '
            f'{webhook.__class__.__name__}; {webhook!r}.'
        )
    
    return webhook, webhook_id, webhook_token


def get_reaction_emoji_value_and_type(reaction):
    """
    Gets the reaction representation form of the given reaction.
    
    Parameters
    ----------
    reaction : ``Reaction``, ``Emoji``, `str`
        The emoji to get it's reaction form of.
    
    Returns
    -------
    emoji_value : `str`
        The emoji's reaction form.
    reaction_type : ``ReactionType``
        The reaction's type.
    
    Raises
    ------
    TypeError
        If `reaction`'s type is incorrect.
    """
    if isinstance(reaction, Emoji):
        return reaction.as_reaction, ReactionType.standard
    
    if isinstance(reaction, Reaction):
        return reaction.emoji.as_reaction, reaction.type
    
    if isinstance(reaction, str):
        return reaction, ReactionType.standard
    
    raise TypeError(
        f'`reaction` can be `{Reaction.__name__}`, `{Emoji.__name__}`, `str`, '
        f'got {type(reaction).__name__}; {reaction!r}.'
    )


def get_emoji_guild_id_and_id(emoji):
    """
    Gets the emoji's guild's and its identifier from the given value.
    
    Parameters
    ----------
    emoji : ``Emoji``, `(int, int)`
        The emoji or `guild-id`, `emoji-id` pair.
    
    Returns
    -------
    snowflake_pair : `(int, int)`
        The emoji's guild's and it's own identifier.
    
    Raises
    ------
    TypeError
        If `emoji`'s type is incorrect.
    """
    if isinstance(emoji, Emoji):
        snowflake_pair = emoji.guild_id, emoji.id
    
    else:
        snowflake_pair = maybe_snowflake_pair(emoji)
        if snowflake_pair is None:
            raise TypeError(
                f'`emoji` can be `{Emoji.__name__}`, `(int, int)`, got {type(emoji).__name__}; {emoji!r}.'
            )
    
    return snowflake_pair


def get_emoji_id(emoji):
    """
    Gets the emoji's identifier.
    
    Parameters
    ----------
    emoji : ``Emoji``, `int`
        The emoji or its identifier.
    
    Returns
    -------
    emoji_id : `int`
    """
    if isinstance(emoji, Emoji):
        emoji_id = emoji.id
    else:
        emoji_id = maybe_snowflake(emoji)
        if (emoji_id is None):
            raise TypeError(
                f'`emoji` can be `{Emoji.__name__}`, `int`, got {type(emoji).__name__}; {emoji!r}.'
            )
    
    return emoji_id


def get_emoji_and_id(emoji):
    """
    Gets the emoji and its identifier.
    
    Parameters
    ----------
    emoji : ``Emoji``, `int`
        The emoji or its identifier.
    
    Returns
    -------
    emoji_and_emoji_id : `(None | Emoji, int)`
    """
    if isinstance(emoji, Emoji):
        emoji_id = emoji.id
    else:
        emoji_id = maybe_snowflake(emoji)
        if (emoji_id is None):
            raise TypeError(
                f'`emoji` can be `{Emoji.__name__}`, `int`, got {type(emoji).__name__}; {emoji!r}.'
            )
        emoji = EMOJIS.get(emoji_id, None)
    
    return emoji, emoji_id


def get_emoji_and_guild_id_and_id(emoji):
    """
    Gets the emoji and it's guild's identifier from the given emoji.
    
    Parameters
    ----------
    emoji : ``Emoji``, `(int, int)`
        The emoji or `guild-id`, `emoji-id` pair.
    
    Returns
    -------
    emoji_and_guild_id_and_emoji_id : `(None | Emoji, int, int)`
        The emoji and its guild's and it's own identifier.
    
    Raises
    ------
    TypeError
        If `emoji`'s type is incorrect.
    """
    if isinstance(emoji, Emoji):
        guild_id = emoji.guild_id
        emoji_id = emoji.id
    
    else:
        snowflake_pair = maybe_snowflake_pair(emoji)
        if snowflake_pair is None:
            raise TypeError(
                f'`emoji` can be `{Emoji.__name__}`, `(int, int)`, got {type(emoji).__name__}; {emoji!r}.'
            )
        
        guild_id, emoji_id = snowflake_pair
        emoji = EMOJIS.get(emoji_id, None)
    
    return emoji, guild_id, emoji_id


def get_sticker_and_id(sticker):
    """
    Gets sticker and it's identifier from the given sticker or of it's identifier.
    
    Parameters
    ----------
    sticker : ``Sticker``, `int`
        The sticker, or it's identifier.
    
    Returns
    -------
    sticker : ``Sticker``, `None`
        The sticker if found.
    sticker_id : `int`
        The sticker's identifier.
    
    Raises
    ------
    TypeError
        If `sticker`'s type is incorrect.
    """
    while True:
        if isinstance(sticker, Sticker):
            sticker_id = sticker.id
            break
        
        sticker_id = maybe_snowflake(sticker)
        if (sticker_id is not None):
            sticker = STICKERS.get(sticker_id, None)
            break
        
        raise TypeError(
            f'`sticker` can be `{Sticker.__name__}`, `int`, got {sticker.__class__.__name__}; {sticker!r}.'
        )
        
    return sticker, sticker_id


def get_sticker_pack_and_id(sticker_pack):
    """
    Gets sticker pack and it's identifier from the given sticker pack or of it's identifier.
    
    Parameters
    ----------
    sticker_pack : ``StickerPack``, `int`
        The sticker, or it's identifier.
    
    Returns
    -------
    sticker_pack : ``StickerPack``, `None`
        The sticker pack if found.
    sticker_pack_id : `int`
        The sticker pack's identifier.
    
    Raises
    ------
    TypeError
        If `sticker_pack`'s type is incorrect.
    """
    while True:
        if isinstance(sticker_pack, StickerPack):
            sticker_pack_id = sticker_pack.id
            break
        
        sticker_pack_id = maybe_snowflake(sticker_pack)
        if (sticker_pack_id is not None):
            sticker_pack = STICKER_PACKS.get(sticker_pack_id, None)
            break
        
        raise TypeError(
            f'`sticker_pack` can be `{StickerPack.__name__}`, `int`, got {sticker_pack.__class__.__name__}; '
            f'{sticker_pack!r}.'
        )
        
    return sticker_pack, sticker_pack_id


def get_scheduled_event_guild_id_and_id(scheduled_event):
    """
    Gets the scheduled event's and it's identifier from the given scheduled event or from a tuple of 2 identifiers.
    
    Parameters
    ----------
    scheduled_event : ``ScheduledEvent``, `tuple` of (`int`, `int`)
        The scheduled event, or a tuple of two identifiers.
    
    Returns
    -------
    guild_id : `int`
        The scheduled event's guild's identifier.
    scheduled_event_id : `int`
        The scheduled event's identifier.
    
    Raises
    ------
    TypeError
        If `scheduled_event`'s type is incorrect.
    """
    if isinstance(scheduled_event, ScheduledEvent):
        return scheduled_event.guild_id, scheduled_event.id
    
    
    snowflake_pair = maybe_snowflake_pair(scheduled_event)
    if snowflake_pair is None:
        raise TypeError(
            f'`scheduled_event` can be `{ScheduledEvent.__name__}`, `tuple` of (`int`, `int`), got '
            f'{scheduled_event.__class__.__name__}; {scheduled_event!r}.'
        )
    
    return snowflake_pair


def get_scheduled_event_and_guild_id_and_id(scheduled_event):
    """
    Gets the scheduled event, it's guild's identifier and it's identifier.
    
    Parameters
    ----------
    scheduled_event : ``ScheduledEvent``, `tuple` (`int`, `int`)
        The scheduled event, or it's identifier.
    
    Returns
    -------
    scheduled_event : `None`, ``ScheduledEvent``
        The scheduled event.
    guild_id : `int`
        The scheduled event's guild's identifier.
    scheduled_event_id : `int`
        The scheduled event's identifier.
    
    Raises
    ------
    TypeError
        If `scheduled_event`'s type is incorrect.
    """
    if isinstance(scheduled_event, ScheduledEvent):
        scheduled_event =  scheduled_event
        scheduled_event_id = scheduled_event.id
        guild_id = scheduled_event.guild_id
    else:
        snowflake_pair = maybe_snowflake_pair(scheduled_event)
        if snowflake_pair is None:
            raise TypeError(
                f'`scheduled_event` can be `{ScheduledEvent.__name__}`, `tuple` of (`int`, `int`), got '
                f'{scheduled_event.__class__.__name__}; {scheduled_event!r}.'
            )
        
        guild_id, scheduled_event_id = snowflake_pair
        
        scheduled_event = SCHEDULED_EVENTS.get(scheduled_event_id, None)
    
    return scheduled_event, guild_id, scheduled_event_id


def get_application_command_id(application_command):
    """
    Gets the application command's identifier.
    
    Parameters
    ----------
    application_command : ``ApplicationCommand``, `int`
        The application command or it's identifier.
    
    Returns
    -------
    application_command_id : `int`
        The application command's identifier.
    
    Raises
    ------
    TypeError
        If `application_command`'s type is incorrect.
    """
    if isinstance(application_command, ApplicationCommand):
        application_command_id = application_command.id
    
    else:
        application_command_id = maybe_snowflake(application_command)
        if application_command_id is None:
            raise TypeError(
                f'`application_command` can be `{ApplicationCommand.__name__}`, `int`, got '
                f'{application_command.__class__.__name__}; {application_command!r}.'
            )
    
    return application_command_id


def get_application_command_and_id(application_command):
    """
    Gets the application command's identifier.
    
    Parameters
    ----------
    application_command : ``ApplicationCommand``, `int`
        The application command or it's identifier.
    
    Returns
    -------
    application_command : `None`, ``ApplicationCommand``
        The application command if exists.
    application_command_id : `int`
        The application command's identifier.
    
    Raises
    ------
    TypeError
        If `application_command`'s type is incorrect.
    """
    if isinstance(application_command, ApplicationCommand):
        application_command_id = application_command.id
    
    else:
        application_command_id = maybe_snowflake(application_command)
        if application_command_id is None:
            raise TypeError(
                f'`application_command` can be `{ApplicationCommand.__name__}`, `int`, got '
                f'{application_command.__class__.__name__}; {application_command!r}.'
            )
        
        application_command = APPLICATION_COMMANDS.get(application_command_id, None)
    
    return application_command, application_command_id


def get_application_command_id_nullable(application_command):
    """
    Gets the application command's identifier.
    
    > The application command can be `None`. At that case `application_command_id` will default to `0`.
    
    Parameters
    ----------
    application_command : `None`, ``ApplicationCommand``, `int`
        The application command or it's identifier.
    
    Returns
    -------
    application_command_id : `int`
        The application command's identifier.
    
    Raises
    ------
    TypeError
        If `application_command`'s type is incorrect.
    """
    if application_command is None:
        application_command_id = 0
    
    elif isinstance(application_command, ApplicationCommand):
        application_command_id = application_command.id
    
    else:
        application_command_id = maybe_snowflake(application_command)
        if application_command_id is None:
            raise TypeError(
                f'`application_command` can be `{ApplicationCommand.__name__}`, `int`, got '
                f'{application_command.__class__.__name__}; {application_command!r}.'
            )
    
    return application_command_id


def get_auto_moderation_rule_guild_id_and_id(auto_moderation_rule):
    """
    Gets the auto moderation rule's guild's identifier and it's own identifier.
    
    Parameters
    ----------
    auto_moderation_rule : ``AutoModerationRule``, `tuple` (`int`, `int`)
        The auto moderation rule, or it's identifier as a `guild-id`, `rule-id` pair..
    
    Returns
    -------
    guild_id : `int`
        The auto moderation rule's guild's identifier.
    auto_moderation_rule_id : `int`
        The auto moderation rule's identifier.
    
    Raises
    ------
    TypeError
        If `auto_moderation_rule`'s type is incorrect.
    """
    if isinstance(auto_moderation_rule, AutoModerationRule):
        guild_id = auto_moderation_rule.guild_id
        rule_id = auto_moderation_rule.id
    
    else:
        snowflake_pair = maybe_snowflake_pair(auto_moderation_rule)
        if snowflake_pair is None:
            raise TypeError(
                f'`auto_moderation_rule` can be `{AutoModerationRule.__name__}`, `tuple` of (`int`, `int`), got '
                f'{auto_moderation_rule.__class__.__name__}; {auto_moderation_rule!r}.'
            )
        
        guild_id, rule_id = snowflake_pair
    
    return guild_id, rule_id


def get_auto_moderation_rule_and_guild_id_and_id(auto_moderation_rule):
    """
    Gets the auto moderation, its guild's identifier and it's own identifier.
    
    Parameters
    ----------
    auto_moderation_rule : ``AutoModerationRule``, `tuple` (`int`, `int`)
        The auto moderation rule, or it's identifier as a `guild-id`, `rule-id` pair..
    
    Returns
    -------
    auto_moderation_rule : `None`, ``AutoModerationRule``
        The auto moderation rule.
    guild_id : `int`
        The auto moderation rule's guild's identifier.
    auto_moderation_rule_id : `int`
        The auto moderation rule's identifier.
    
    Raises
    ------
    TypeError
        If `auto_moderation_rule`'s type is incorrect.
    """
    if isinstance(auto_moderation_rule, AutoModerationRule):
        guild_id = auto_moderation_rule.guild_id
        rule_id = auto_moderation_rule.id
    
    else:
        snowflake_pair = maybe_snowflake_pair(auto_moderation_rule)
        if snowflake_pair is None:
            raise TypeError(
                f'`auto_moderation_rule` can be `{AutoModerationRule.__name__}`, `tuple` of (`int`, `int`), got '
                f'{auto_moderation_rule.__class__.__name__}; {auto_moderation_rule!r}.'
            )
        
        guild_id, rule_id = snowflake_pair
        auto_moderation_rule = AUTO_MODERATION_RULES.get(rule_id, None)
    
    return auto_moderation_rule, guild_id, rule_id


def get_forum_tag_id(forum_tag):
    """
    Gets the forum tag's identifier.
    
    Parameters
    ----------
    forum_tag : ``ForumTag``, `int`
        The forum tag or its identifier.
    
    Returns
    -------
    forum_tag_id : `int`
        The forum tag's identifier.
    
    Raises
    ------
    TypeError
        - If `forum_tag` type is incorrect.
    """
    if isinstance(forum_tag, ForumTag):
        forum_tag_id = forum_tag.id
    
    else:
        forum_tag_id = maybe_snowflake(forum_tag)
        if (forum_tag_id is None):
            raise TypeError(
                f'`forum_tag` can be `{ForumTag.__name__}, `int`, got {forum_tag.__class__.__name__}; {forum_tag!r}.'
            )
    
    return forum_tag_id


def get_forum_tag_and_id(forum_tag):
    """
    Gets the forum tag and it's identifier.
    
    Parameters
    ----------
    forum_tag : ``ForumTag``, `int`
        The forum tag or its identifier.
    
    Returns
    -------
    forum_tag : `None`, ``ForumTag``
        The forum tag if exists.
    forum_tag_id : `int`
        The forum tag's identifier.
    
    Raises
    ------
    TypeError
        - If `forum_tag` type is incorrect.
    """
    if isinstance(forum_tag, ForumTag):
        forum_tag_id = forum_tag.id
    
    else:
        forum_tag_id = maybe_snowflake(forum_tag)
        if (forum_tag_id is None):
            raise TypeError(
                f'`forum_tag` can be `{ForumTag.__name__}, `int`, got {forum_tag.__class__.__name__}; {forum_tag!r}.'
            )
        
        forum_tag = FORUM_TAGS.get(forum_tag_id, None)
    
    return forum_tag, forum_tag_id


def get_permission_overwrite_target_id(permission_overwrite):
    """
    Returns the given `permission_overwrite`'s target id.
    
    Parameters
    ----------
    permission_overwrite : ``PermissionOverwrite``
        The permission overwrite or it's target id.
    
    Returns
    -------
    target_id : `int`
    
    Raises
    ------
    TypeError
        - If `permission_overwrite` type is incorrect.
    """
    if isinstance(permission_overwrite, PermissionOverwrite):
        target_id = permission_overwrite.target_id
    
    else:
        target_id = maybe_snowflake(permission_overwrite)
        if (target_id is None):
            raise TypeError(
                f'`permission_overwrite` can be `{PermissionOverwrite.__name__}`, `int` got '
                f'{permission_overwrite.__class__.__name__}; {permission_overwrite!r}.'
            )
    
    return target_id


def _check_required_scope(access, required_scope):
    if (required_scope is not None) and (not access.has_scope(required_scope)):
        raise ValueError(
            f'The given `access` not grants {required_scope.name!r} scope, what is required, '
            f'got {access!r}.'
        )


def get_oauth2_access_token(access, required_scope = None):
    """
    Returns the given oauth2 access's access token. Accepts both access and just token as well.
    
    Parameters
    ----------
    access : ``Oauth2Access``, ``Oauth2User``, `str`
        Oauth2 access to the respective user or it's access token.
    required_scope : `None`, ``Oauth2Scope`` = `None`, Optional
        Required scope of the access if any.
    
    Returns
    -------
    access_token : `str`
    
    Raises
    ------
    TypeError
        - If `access` is not ``Oauth2Access``, ``Oauth2User``, `str`.
    ValueError
        - If the given `access` is not providing the required scope.
    """
    if isinstance(access, (Oauth2Access, Oauth2User)):
        _check_required_scope(access, required_scope)
        access_token = access.access_token
    
    elif isinstance(access, str):
        access_token = access
    
    else:
        raise TypeError(
            f'`access` can be `{Oauth2Access.__name__}`, `{Oauth2User.__name__}`, `str`'
            f', got {access.__class__.__name__}; {access!r}.'
        )
    
    return access_token


def get_oauth2_access_token_and_user_id(access, user, required_scope = None):
    """
    Returns the given oauth2 access's access token and the user's identifier.
    
    Parameters
    ----------
    access : ``Oauth2Access``, ``Oauth2User``, `str`
        Oauth2 access to the respective user or it's access token.
    required_scope : `None`, ``Oauth2Scope`` = `None`, Optional
        Required scope of the access if any.
    
    Raises
    ------
    TypeError
        - If `access` is not ``Oauth2Access``, ``Oauth2User``, `str`.
        - If `user` is not `None`, ``ClientUserBase``.
        - If `user.id` could not be determined.
    ValueError
        - If the given `access` is not providing the required scope.
        - If `user` and `access` refers to a different user.
    """
    user_id = get_user_id_nullable(user)
    
    if isinstance(access, Oauth2Access):
        _check_required_scope(access, required_scope)
        access_token = access.access_token
    
    elif isinstance(access, Oauth2User):
        _check_required_scope(access, required_scope)
        access_token = access.access_token
        
        if user_id and (user_id != access.id):
            raise ValueError(
                f'The given `user` and `access` refers to different users, got user = {user!r}, '
                f'access = {access!r}.'
            )
        
        user_id = access.id
    
    elif isinstance(access, str):
        access_token = access
    
    else:
        raise TypeError(
            f'`access` can be `{Oauth2Access.__name__}`, `{Oauth2User.__name__}`, `str`, got '
            f'{access.__class__.__name__}; {access!r}.'
        )
    
    
    if not user_id:
        raise TypeError(
            f'`user` was not detectable neither from `user` nor from `access` parameters, got '
            f'user = {user!r}, access = {access!r}.'
        )
    
    return access_token, user_id


def get_soundboard_sound_and_guild_id_and_id(soundboard_sound):
    """
    Gets the soundboard sound identifier from the given soundboard sound or of it's identifier.
    
    Parameters
    ----------
    soundboard_sound : ``SoundboardSound``, `tuple` (`int`, `int`)
        The soundboard sound, or a `guild-id`, `soundboard-sound-id` pair.
    
    Returns
    -------
    soundboard_sound : `None`, ``SoundboardSound``
        The respective soundboard sound.
    
    guild_id : `int`
        The soundboard sound's guild's identifier.
    
    soundboard_sound_id : `int`
        The soundboard sound's identifier.
    
    Raises
    ------
    TypeError
        If `soundboard_sound`'s type is incorrect.
    """
    if isinstance(soundboard_sound, SoundboardSound):
        soundboard_sound_id = soundboard_sound.id
        guild_id = soundboard_sound.guild_id
    
    else:
        snowflake_pair = maybe_snowflake_pair(soundboard_sound)
        if snowflake_pair is None:
            raise TypeError(
                f'`soundboard_sound` can be `{SoundboardSound.__name__}`, `tuple` (`int`, `int`), '
                f'got {soundboard_sound.__class__.__name__}; {soundboard_sound!r}.'
            )
        
        guild_id, soundboard_sound_id = snowflake_pair
        soundboard_sound = SOUNDBOARD_SOUNDS.get(soundboard_sound_id, None)
    
    return soundboard_sound, guild_id, soundboard_sound_id


def get_soundboard_sound_guild_id_and_id(soundboard_sound):
    """
    Gets the soundboard_sound's and it's guild's identifier from the given soundboard_sound or of a `guild-id`,
    `soundboard_sound-id` pair.
    
    Parameters
    ----------
    soundboard_sound : ``SoundboardSound``, `tuple` (`int`, `int`)
        The soundboard sound, or a `guild-id`, `soundboard-sound-id` pair.
    
    Returns
    -------
    guild_id : `int`
        The soundboard sound's guild's identifier.
    
    soundboard_sound_id : `int`
        The soundboard sound's identifier.
    
    Raises
    ------
    TypeError
        If `soundboard_sound`'s type is incorrect.
    """
    if isinstance(soundboard_sound, SoundboardSound):
        return soundboard_sound.guild_id, soundboard_sound.id
    
    snowflake_pair = maybe_snowflake_pair(soundboard_sound)
    if snowflake_pair is not None:
        return snowflake_pair
    
    raise TypeError(
        f'`soundboard_sound` can be `{SoundboardSound.__name__}`, `tuple` (`int`, `int`), '
        f'got {soundboard_sound.__class__.__name__}; {soundboard_sound!r}.'
    )


def get_entitlement_id(entitlement):
    """
    Gets the entitlement's identifier.
    
    Parameters
    ----------
    entitlement : ``Entitlement``, `int`
        The entitlement or its identifier.
    
    Returns
    -------
    entitlement_id : `int`
        The entitlement's identifier.
    
    Raises
    ------
    TypeError
        - If `entitlement` type is incorrect.
    """
    if isinstance(entitlement, Entitlement):
        entitlement_id = entitlement.id
    
    else:
        entitlement_id = maybe_snowflake(entitlement)
        if (entitlement_id is None):
            raise TypeError(
                f'`entitlement` can be `{Entitlement.__name__}, `int`, '
                f'got {entitlement.__class__.__name__}; {entitlement!r}.'
            )
    
    return entitlement_id


def get_poll_answer_and_id(poll_answer):
    """
    Gets the poll answer and its identifier.
    
    Parameters
    ----------
    poll_answer : ``PollAnswer``, `int`
        The poll answer to get its identifier.
    
    Returns
    -------
    poll_answer : `None`, ``PollAnswer``
    poll_answer_id : `int`
    
    Raises
    ------
    TypeError
        - If `poll_answer` type is incorrect.
    """
    if isinstance(poll_answer, PollAnswer):
        return poll_answer, poll_answer.id
    
    poll_answer_id = maybe_snowflake(poll_answer)
    if poll_answer_id is None:
        raise TypeError(
            f'`poll_answer` can be `{PollAnswer.__name__}, `int`, '
            f'got {poll_answer.__class__.__name__}; {poll_answer!r}.'
        )
    
    return None, poll_answer_id


def get_message_id(message):
    """
    Gets the message's identifier from the given message or of it's identifier.
    
    Parameters
    ----------
    message : ``Message``, `int`
        The message, or it's identifier.
    
    Returns
    -------
    message_id : `int`
        The message's identifier.
    
    Raises
    ------
    TypeError
        If `message`'s type is incorrect.
    """
    if isinstance(message, Message):
        message_id = message.id
    else:
        message_id = maybe_snowflake(message)
        if message_id is None:
            raise TypeError(
                f'`message` can be `{Message.__name__}`, `int`, got {type(message).__name__}; {message!r}.'
            )
    
    return message_id


def get_embedded_activity_and_id(embedded_activity):
    """
    Gets the embedded activity and its identifier.
    
    Parameters
    ----------
    embedded_activity : `EmbeddedActivity | int`
        The embedded activity to get its identifier.
    
    Returns
    -------
    embedded_activity : `None | EmbeddedActivity`
    embedded_activity_id : `int`
    
    Raises
    ------
    TypeError
        - If `embedded_activity` type is incorrect.
    """
    if isinstance(embedded_activity, EmbeddedActivity):
        return embedded_activity, embedded_activity.id
    
    embedded_activity_id = maybe_snowflake(embedded_activity)
    if embedded_activity_id is None:
        raise TypeError(
            f'`embedded_activity` can be `{EmbeddedActivity.__name__}, `int`, '
            f'got {type(embedded_activity).__name__}; {embedded_activity!r}.'
        )
    
    embedded_activity = EMBEDDED_ACTIVITIES.get(embedded_activity_id, None)
    return embedded_activity, embedded_activity_id



def get_subscription_and_sku_id_and_id(subscription):
    """
    Gets the subscription and it's sku's identifier from the given subscription.
    
    Parameters
    ----------
    subscription : ``Subscription``, `(int, int)`
        The subscription or `sku-id`, `subscription-id` pair.
    
    Returns
    -------
    subscription_and_sku_id_and_subscription_id : `(None | Subscription, int, int)`
        The subscription and its sku's and it's own identifier.
    
    Raises
    ------
    TypeError
        If `subscription`'s type is incorrect.
    """
    if isinstance(subscription, Subscription):
        sku_id = subscription.sku_id
        subscription_id = subscription.id
    
    else:
        snowflake_pair = maybe_snowflake_pair(subscription)
        if snowflake_pair is None:
            raise TypeError(
                f'`subscription` can be `{Subscription.__name__}`, `(int, int)`, got {type(subscription).__name__}; {subscription!r}.'
            )
        
        sku_id, subscription_id = snowflake_pair
        subscription = SUBSCRIPTIONS.get(subscription_id, None)
    
    return subscription, sku_id, subscription_id
