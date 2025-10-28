from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....channel import Channel, ChannelType
from ....component import Component, ComponentType
from ....core import BUILTIN_EMOJIS
from ....embed import Embed
from ....emoji import Reaction, ReactionMapping, ReactionMappingLine, ReactionType
from ....poll import Poll
from ....resolved import Resolved
from ....soundboard import SoundboardSound
from ....sticker import Sticker
from ....user import User, UserBase

from ...attachment import Attachment
from ...message_activity import MessageActivity
from ...message_application import MessageApplication
from ...message_call import MessageCall
from ...message_interaction import MessageInteraction
from ...message_role_subscription import MessageRoleSubscription
from ...message_snapshot import MessageSnapshot
from ...shared_client_theme import SharedClientTheme

from ..flags import MessageFlag
from ..message import Message
from ..preinstanced import MessageType


def _assert_fields_set(message):
    """
    Asserts whether every fields are set of the given message.
    
    Parameters
    ----------
    message : ``Message``
        The message to check.
    """
    vampytest.assert_instance(message, Message)
    
    vampytest.assert_instance(message._cache_mentioned_channels, tuple, nullable = True)
    vampytest.assert_instance(message._state, int)
    vampytest.assert_instance(message.activity, MessageActivity, nullable = True)
    vampytest.assert_instance(message.application, MessageApplication, nullable = True)
    vampytest.assert_instance(message.application_id, int)
    vampytest.assert_instance(message.attachments, tuple, nullable = True)
    vampytest.assert_instance(message.author, UserBase)
    vampytest.assert_instance(message.call, MessageCall, nullable = True)
    vampytest.assert_instance(message.channel_id, int)
    vampytest.assert_instance(message.components, tuple, nullable = True)
    vampytest.assert_instance(message.content, str, nullable = True)
    vampytest.assert_instance(message.edited_at, DateTime, nullable = True)
    vampytest.assert_instance(message.embeds, tuple, nullable = True)
    vampytest.assert_instance(message.flags, MessageFlag)
    vampytest.assert_instance(message.guild_id, int)
    vampytest.assert_instance(message.id, int)
    vampytest.assert_instance(message.interaction, MessageInteraction, nullable = True)
    vampytest.assert_instance(message.mentioned_channels_cross_guild, tuple, nullable = True)
    vampytest.assert_instance(message.mentioned_everyone, bool)
    vampytest.assert_instance(message.mentioned_role_ids, tuple, nullable = True)
    vampytest.assert_instance(message.mentioned_users, tuple, nullable = True)
    vampytest.assert_instance(message.nonce, str, nullable = True)
    vampytest.assert_instance(message.pinned, bool)
    vampytest.assert_instance(message.poll, Poll, nullable = True)
    vampytest.assert_instance(message.reactions, ReactionMapping, nullable = True)
    vampytest.assert_instance(message.referenced_message, Message, nullable = True)
    vampytest.assert_instance(message.resolved, Resolved, nullable = True)
    vampytest.assert_instance(message.role_subscription, MessageRoleSubscription, nullable = True)
    vampytest.assert_instance(message.shared_client_theme, SharedClientTheme, nullable = True)
    vampytest.assert_instance(message.snapshots, tuple, nullable = True)
    vampytest.assert_instance(message.soundboard_sounds, tuple, nullable = True)
    vampytest.assert_instance(message.stickers, tuple, nullable = True)
    vampytest.assert_instance(message.thread, Channel, nullable = True)
    vampytest.assert_instance(message.tts, bool)
    vampytest.assert_instance(message.type, MessageType)


def test__Message__new__no_fields():
    """
    Tests whether ``Message.__new__`` works as intended.
    
    Case: No fields given.
    """
    message = Message()
    _assert_fields_set(message)


def test__Message__new__all_fields():
    """
    Tests whether ``Message.__new__`` works as intended.
    
    Case: All fields given.
    """
    activity = MessageActivity(party_id = 'Remilia')
    application = MessageApplication.precreate(202305030000, name = 'Flandre')
    application_id = 202305030001
    attachments = [
        Attachment.precreate(202305030002, name = 'Koishi'),
        Attachment.precreate(202305030003, name = 'Komeiji'),
    ]
    author = User.precreate(202305030004, name = 'Orin')
    call = MessageCall(ended_at = DateTime(2045, 3, 4, tzinfo = TimeZone.utc))
    components = [
        Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Okuu')]),
        Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Parsee')]),
    ]
    content = 'Satori'
    edited_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    embeds = [
        Embed('Yakumo'),
        Embed('Yukari'),
    ]
    flags = MessageFlag(15)
    interaction = MessageInteraction.precreate(202305030005, name = 'Ran')
    mentioned_channels_cross_guild = [
        Channel.precreate(202305030006, channel_type = ChannelType.guild_text, name = 'Chen'),
        Channel.precreate(202305030007, channel_type = ChannelType.guild_text, name = 'Yuugi'),
    ]
    mentioned_everyone = True
    mentioned_role_ids = [202305030008, 202305030009]
    mentioned_users = [
        User.precreate(202305030010, name = 'Scarlet'),
        User.precreate(202305030011, name = 'Izaoyi'),
    ]
    message_type = MessageType.call
    nonce = 'Sakuya'
    pinned = True
    poll = Poll(expires_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc))
    reactions = ReactionMapping(
        lines = {
            Reaction.from_fields(BUILTIN_EMOJIS['x'], ReactionType.standard): ReactionMappingLine(count = 2),
        },
    )
    referenced_message = Message.precreate(202305030012, content = 'Patchouli')
    resolved = Resolved(attachments = [Attachment.precreate(202310110006)])
    role_subscription = MessageRoleSubscription(tier_name = 'Knowledge')
    shared_client_theme = SharedClientTheme(intensity = 6)
    snapshots = [
        MessageSnapshot(content = 'Kazami'),
        MessageSnapshot(content = 'Yuuka'),
    ]
    soundboard_sounds = [
        SoundboardSound.precreate(202501290006, name = 'whither'),
        SoundboardSound.precreate(202501290007, name = 'Yuyuko'),
    ]
    stickers = [
        Sticker.precreate(202305030013, name = 'Kirisame'),
        Sticker.precreate(202305030014, name = 'Marisa'),
    ]
    thread = Channel.precreate(202305030015, channel_type = ChannelType.guild_thread_private, name = 'Yuyuko')
    tts = True
    
    
    message = Message(
        activity = activity,
        application = application,
        application_id = application_id,
        attachments = attachments,
        author = author,
        call = call,
        components = components,
        content = content,
        edited_at = edited_at,
        embeds = embeds,
        flags = flags,
        interaction = interaction,
        mentioned_channels_cross_guild = mentioned_channels_cross_guild,
        mentioned_everyone = mentioned_everyone,
        mentioned_role_ids = mentioned_role_ids,
        mentioned_users = mentioned_users,
        message_type = message_type,
        nonce = nonce,
        pinned = pinned,
        poll = poll,
        reactions = reactions,
        referenced_message = referenced_message,
        resolved = resolved,
        role_subscription = role_subscription,
        shared_client_theme = shared_client_theme,
        snapshots = snapshots,
        soundboard_sounds = soundboard_sounds,
        stickers = stickers,
        thread = thread,
        tts = tts,
    )
    
    _assert_fields_set(message)
    
    vampytest.assert_eq(message.activity, activity)
    vampytest.assert_eq(message.application, application)
    vampytest.assert_eq(message.application_id, application_id)
    vampytest.assert_eq(message.attachments, tuple(attachments))
    vampytest.assert_eq(message.author, author)
    vampytest.assert_eq(message.call, call)
    vampytest.assert_eq(message.components, tuple(components))
    vampytest.assert_eq(message.content, content)
    vampytest.assert_eq(message.edited_at, edited_at)
    vampytest.assert_eq(message.embeds, tuple(embeds))
    vampytest.assert_eq(message.flags, flags)
    vampytest.assert_eq(message.interaction, interaction)
    vampytest.assert_eq(message.mentioned_channels_cross_guild, tuple(mentioned_channels_cross_guild))
    vampytest.assert_eq(message.mentioned_everyone, mentioned_everyone)
    vampytest.assert_eq(message.mentioned_role_ids, tuple(mentioned_role_ids))
    vampytest.assert_eq(message.mentioned_users, tuple(mentioned_users))
    vampytest.assert_eq(message.nonce, nonce)
    vampytest.assert_eq(message.pinned, pinned)
    vampytest.assert_eq(message.poll, poll)
    vampytest.assert_eq(message.reactions, reactions)
    vampytest.assert_eq(message.referenced_message, referenced_message)
    vampytest.assert_eq(message.resolved, resolved)
    vampytest.assert_eq(message.role_subscription, role_subscription)
    vampytest.assert_eq(message.shared_client_theme, shared_client_theme)
    vampytest.assert_eq(message.snapshots, tuple(snapshots))
    vampytest.assert_eq(message.soundboard_sounds, tuple(soundboard_sounds))
    vampytest.assert_eq(message.stickers, tuple(stickers))
    vampytest.assert_eq(message.thread, thread)
    vampytest.assert_eq(message.tts, tts)
    vampytest.assert_is(message.type, message_type)


def test__Message__create_empty():
    """
    Tests whether ``Message._create_empty`` works as intended.
    """
    message_id = 202305030016
    channel_id = 202305030017
    guild_id = 202305030018
    
    message = Message._create_empty(message_id, channel_id, guild_id)
    _assert_fields_set(message)
    
    vampytest.assert_eq(message.id, message_id)
    vampytest.assert_eq(message.channel_id, channel_id)
    vampytest.assert_eq(message.guild_id, guild_id)


def test__Message__precreate__no_fields():
    """
    Tests whether ``Message.precreate`` works as intended.
    
    Case: No fields & caching.
    """
    message_id = 202305030019
    
    message = Message.precreate(message_id)
    _assert_fields_set(message)
    vampytest.assert_eq(message.id, message_id)
    
    test_message = Message.precreate(message_id)
    vampytest.assert_is(message, test_message)
    

def test__Message__precreate__all_fields():
    """
    Tests whether ``Message.precreate`` works as intended.
    
    Case: All fields given.
    """
    activity = MessageActivity(party_id = 'Remilia')
    application = MessageApplication.precreate(202305030020, name = 'Flandre')
    application_id = 202305030021
    attachments = [
        Attachment.precreate(202305030022, name = 'Koishi'),
        Attachment.precreate(202305030023, name = 'Komeiji'),
    ]
    author = User.precreate(202305030024, name = 'Orin')
    call = MessageCall(ended_at = DateTime(2045, 3, 4, tzinfo = TimeZone.utc))
    components = [
        Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Okuu')]),
        Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Parsee')]),
    ]
    content = 'Satori'
    edited_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    embeds = [
        Embed('Yakumo'),
        Embed('Yukari'),
    ]
    flags = MessageFlag(15)
    interaction = MessageInteraction.precreate(202305030025, name = 'Ran')
    mentioned_channels_cross_guild = [
        Channel.precreate(202305030026, channel_type = ChannelType.guild_text, name = 'Chen'),
        Channel.precreate(202305030027, channel_type = ChannelType.guild_text, name = 'Yuugi'),
    ]
    mentioned_everyone = True
    mentioned_role_ids = [202305030028, 202305030029]
    mentioned_users = [
        User.precreate(202305030030, name = 'Scarlet'),
        User.precreate(202305030031, name = 'Izaoyi'),
    ]
    message_type = MessageType.call
    nonce = 'Sakuya'
    pinned = True
    poll = Poll(expires_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc))
    reactions = ReactionMapping(
        lines = {
            Reaction.from_fields(BUILTIN_EMOJIS['x'], ReactionType.standard): ReactionMappingLine(count = 2),
        },
    )
    referenced_message = Message.precreate(202305030032, content = 'Patchouli')
    resolved = Resolved(attachments = [Attachment.precreate(202310110007)])
    role_subscription = MessageRoleSubscription(tier_name = 'Knowledge')
    shared_client_theme = SharedClientTheme(intensity = 6)
    snapshots = [
        MessageSnapshot(content = 'Kazami'),
        MessageSnapshot(content = 'Yuuka'),
    ]
    soundboard_sounds = [
        SoundboardSound.precreate(202501290008, name = 'whither'),
        SoundboardSound.precreate(202501290009, name = 'Yuyuko'),
    ]
    stickers = [
        Sticker.precreate(202305030033, name = 'Kirisame'),
        Sticker.precreate(202305030034, name = 'Marisa'),
    ]
    thread = Channel.precreate(202305030035, channel_type = ChannelType.guild_thread_private, name = 'Yuyuko')
    tts = True
    
    message_id = 202305030036
    channel_id = 202305030037
    guild_id = 202305030038
    
    message = Message.precreate(
        message_id,
        channel_id = channel_id,
        guild_id = guild_id,
        
        activity = activity,
        application = application,
        application_id = application_id,
        attachments = attachments,
        author = author,
        call = call,
        components = components,
        content = content,
        edited_at = edited_at,
        embeds = embeds,
        flags = flags,
        interaction = interaction,
        mentioned_channels_cross_guild = mentioned_channels_cross_guild,
        mentioned_everyone = mentioned_everyone,
        mentioned_role_ids = mentioned_role_ids,
        mentioned_users = mentioned_users,
        message_type = message_type,
        nonce = nonce,
        pinned = pinned,
        poll = poll,
        reactions = reactions,
        referenced_message = referenced_message,
        resolved = resolved,
        role_subscription = role_subscription,
        shared_client_theme = shared_client_theme,
        snapshots = snapshots,
        soundboard_sounds = soundboard_sounds,
        stickers = stickers,
        thread = thread,
        tts = tts,
    )
    
    _assert_fields_set(message)
    
    vampytest.assert_eq(message.activity, activity)
    vampytest.assert_eq(message.application, application)
    vampytest.assert_eq(message.application_id, application_id)
    vampytest.assert_eq(message.attachments, tuple(attachments))
    vampytest.assert_eq(message.author, author)
    vampytest.assert_eq(message.call, call)
    vampytest.assert_eq(message.components, tuple(components))
    vampytest.assert_eq(message.content, content)
    vampytest.assert_eq(message.edited_at, edited_at)
    vampytest.assert_eq(message.embeds, tuple(embeds))
    vampytest.assert_eq(message.flags, flags)
    vampytest.assert_eq(message.interaction, interaction)
    vampytest.assert_eq(message.mentioned_channels_cross_guild, tuple(mentioned_channels_cross_guild))
    vampytest.assert_eq(message.mentioned_everyone, mentioned_everyone)
    vampytest.assert_eq(message.mentioned_role_ids, tuple(mentioned_role_ids))
    vampytest.assert_eq(message.mentioned_users, tuple(mentioned_users))
    vampytest.assert_eq(message.nonce, nonce)
    vampytest.assert_eq(message.pinned, pinned)
    vampytest.assert_eq(message.poll, poll)
    vampytest.assert_eq(message.reactions, reactions)
    vampytest.assert_eq(message.referenced_message, referenced_message)
    vampytest.assert_eq(message.resolved, resolved)
    vampytest.assert_eq(message.role_subscription, role_subscription)
    vampytest.assert_eq(message.shared_client_theme, shared_client_theme)
    vampytest.assert_eq(message.snapshots, tuple(snapshots))
    vampytest.assert_eq(message.soundboard_sounds, tuple(soundboard_sounds))
    vampytest.assert_eq(message.stickers, tuple(stickers))
    vampytest.assert_eq(message.thread, thread)
    vampytest.assert_eq(message.tts, tts)
    vampytest.assert_is(message.type, message_type)
    
    vampytest.assert_eq(message.id, message_id)
    vampytest.assert_eq(message.channel_id, channel_id)
    vampytest.assert_eq(message.guild_id, guild_id)
