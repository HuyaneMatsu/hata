from datetime import datetime as DateTime

import vampytest

from ....channel import Channel, ChannelType
from ....component import Component, ComponentType
from ....core import BUILTIN_EMOJIS
from ....embed import EmbedAuthor, Embed, EmbedField, EmbedFooter, EmbedProvider, EmbedType
from ....emoji import Reaction, ReactionMapping, ReactionType
from ....guild import Guild
from ....role import Role
from ....sticker import Sticker
from ....user import User

from ...attachment import Attachment
from ...message_activity import MessageActivity
from ...message_application import MessageApplication
from ...message_call import MessageCall
from ...message_interaction import MessageInteraction
from ...message_role_subscription import MessageRoleSubscription

from ..flags import MessageFlag
from ..message import Message
from ..preinstanced import MessageType

from .test__Message__contructor import _assert_fields_set


def test__Message__iter_contents__0():
    """
    Tests whether ``Message.iter_contents`` works as intended.
    
    Case: All contents.
    """
    message_content = 'okuu'
    embed_0_title = 'orin'
    embed_0_author_name = 'riverside'
    embed_0_description = 'relief'
    embed_0_field_0_name = 'shiki'
    embed_0_field_0_value = 'yukari'
    embed_0_field_1_name = 'ran'
    embed_0_field_1_value = 'chen'
    embed_0_footer_text = 'okina'
    embed_0_provider_name = 'hecatia'
    embed_1_title = 'reimu'
    
    embed_0 = Embed(title = embed_0_title, description = embed_0_description)
    embed_0.author = EmbedAuthor(embed_0_author_name)
    embed_0.fields = [
        EmbedField(embed_0_field_0_name, embed_0_field_0_value),
        EmbedField(embed_0_field_1_name, embed_0_field_1_value),
    ]
    embed_0.footer = EmbedFooter(embed_0_footer_text)
    embed_0.provider = EmbedProvider(embed_0_provider_name)
    
    embed_1 = Embed(title = embed_1_title)
    
    message = Message(content = message_content, embeds = [embed_0, embed_1])
    
    
    contents = {
        embed_0_title, embed_0_author_name, embed_0_description, embed_0_field_0_name, embed_0_field_0_value,
        embed_0_field_1_name, embed_0_field_1_value, embed_0_footer_text, embed_0_provider_name,
        message_content, embed_1_title
    }
    
    vampytest.assert_eq({*message.iter_contents()}, contents)


def test__Message__iter_contents__1():
    """
    Tests whether ``Embed.iter_contents`` works as intended.
    
    Case: No contents.
    """
    message = Message()
    vampytest.assert_eq({*message.iter_contents()}, set())


def test__Message__contents__all_contents():
    """
    Tests whether ``Message.contents`` works as intended.
    
    Case: All contents.
    """
    message_content = 'okuu'
    embed_0_title = 'orin'
    embed_0_author_name = 'riverside'
    embed_0_description = 'relief'
    embed_0_field_0_name = 'shiki'
    embed_0_field_0_value = 'yukari'
    embed_0_field_1_name = 'ran'
    embed_0_field_1_value = 'chen'
    embed_0_footer_text = 'okina'
    embed_0_provider_name = 'hecatia'
    embed_1_title = 'reimu'
    
    embed_0 = Embed(title = embed_0_title, description = embed_0_description)
    embed_0.author = EmbedAuthor(embed_0_author_name)
    embed_0.fields = [
        EmbedField(embed_0_field_0_name, embed_0_field_0_value),
        EmbedField(embed_0_field_1_name, embed_0_field_1_value),
    ]
    embed_0.footer = EmbedFooter(embed_0_footer_text)
    embed_0.provider = EmbedProvider(embed_0_provider_name)
    
    embed_1 = Embed(title = embed_1_title)
    
    message = Message(content = message_content, embeds = [embed_0, embed_1])
    
    contents = {
        embed_0_title, embed_0_author_name, embed_0_description, embed_0_field_0_name, embed_0_field_0_value,
        embed_0_field_1_name, embed_0_field_1_value, embed_0_footer_text, embed_0_provider_name,
        message_content, embed_1_title
    }
    
    output = message.contents
    vampytest.assert_instance(output, list)
    vampytest.assert_eq({*output}, contents)


def test__Message__contents__no_contents():
    """
    Tests whether ``Message.contents`` works as intended.
    
    Case: No contents.
    """
    message = Message()
    
    output = message.contents
    vampytest.assert_instance(output, list)
    vampytest.assert_eq({*output}, set())


def test__Message__add_reaction():
    """
    Tests whether ``Message._add_reaction`` works as intended.
    """
    reaction_0 = Reaction(BUILTIN_EMOJIS['x'], reaction_type = ReactionType.standard)
    user_0 = User.precreate(202305040098)
    user_1 = User.precreate(202305040099)
    
    message = Message()
    message._add_reaction(reaction_0, user_0)
    message._add_reaction(reaction_0, user_1)
    
    vampytest.assert_eq(message.reactions, {reaction_0: [user_0, user_1]})


def test__Message__remove_reaction():
    """
    Tests whether ``Message._remove_reaction`` works as intended.
    """
    reaction_0 = Reaction(BUILTIN_EMOJIS['x'], reaction_type = ReactionType.standard)
    
    user_0 = User.precreate(202305040100)
    
    message = Message()
    message._add_reaction(reaction_0, user_0)
    message._remove_reaction(reaction_0, user_0)
    
    vampytest.assert_eq(message.reactions, {})


def test__Message__remove_reaction_emoji():
    """
    Tests whether ``Message._remove_reaction_emoji`` works as intended.
    """
    emoji_0 = BUILTIN_EMOJIS['x']
    reaction_0 = Reaction(emoji_0, reaction_type = ReactionType.standard)
    
    user_0 = User.precreate(202305040101)
    
    message = Message()
    message._add_reaction(reaction_0, user_0)
    output = message._remove_reaction_emoji(emoji_0)
    
    vampytest.assert_eq(message.reactions, {})
    vampytest.assert_eq(
        output,
        {
            reaction_0: [user_0]
        },
    )


def test__Message__copy():
    """
    Tests whether ``Message.copy`` works as intended.
    """
    activity = MessageActivity(party_id = 'Remilia')
    application = MessageApplication.precreate(202305040105, name = 'Flandre')
    application_id = 202305040106
    attachments = [
        Attachment.precreate(202305040107, name = 'Koishi'),
        Attachment.precreate(202305040108, name = 'Komeiji'),
    ]
    author = User.precreate(202305040109, name = 'Orin')
    call = MessageCall(ended_at = DateTime(2045, 3, 4))
    components = [
        Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Okuu')]),
        Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Parsee')]),
    ]
    content = 'Satori'
    edited_at = DateTime(2016, 5, 14)
    embeds = [
        Embed('Yakumo'),
        Embed('Yukari'),
    ]
    flags = MessageFlag(15)
    interaction = MessageInteraction.precreate(202305040110, name = 'Ran')
    mentioned_channels_cross_guild = [
        Channel.precreate(202305040111, channel_type = ChannelType.guild_text, name = 'Chen'),
        Channel.precreate(202305040112, channel_type = ChannelType.guild_text, name = 'Yuugi'),
    ]
    mentioned_everyone = True
    mentioned_role_ids = [202305040113, 202305040114]
    mentioned_users = [
        User.precreate(202305040115, name = 'Scarlet'),
        User.precreate(202305040116, name = 'Izaoyi'),
    ]
    message_type = MessageType.call
    nonce = 'Sakuya'
    pinned = True
    reactions = ReactionMapping({
        BUILTIN_EMOJIS['x']: [None, None],
    })
    referenced_message = Message.precreate(202305040107, content = 'Patchouli')
    role_subscription = MessageRoleSubscription(tier_name = 'Knowledge')
    stickers = [
        Sticker.precreate(202305040118, name = 'Kirisame'),
        Sticker.precreate(202305040119, name = 'Marisa'),
    ]
    thread = Channel.precreate(202305040120, channel_type = ChannelType.guild_thread_private, name = 'Yuyuko')
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
        reactions = reactions,
        referenced_message = referenced_message,
        role_subscription = role_subscription,
        stickers = stickers,
        thread = thread,
        tts = tts,
    )
    
    copy = message.copy()
    vampytest.assert_is_not(message, copy)
    _assert_fields_set(message)
    
    vampytest.assert_eq(message, copy)


def test__Message__copy_with__0():
    """
    Tests whether ``Message.copy_with`` works as intended.
    
    Case: No fields given.
    """
    activity = MessageActivity(party_id = 'Remilia')
    application = MessageApplication.precreate(202305040121, name = 'Flandre')
    application_id = 202305040122
    attachments = [
        Attachment.precreate(202305040123, name = 'Koishi'),
        Attachment.precreate(202305040124, name = 'Komeiji'),
    ]
    author = User.precreate(202305040125, name = 'Orin')
    call = MessageCall(ended_at = DateTime(2045, 3, 4))
    components = [
        Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Okuu')]),
        Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Parsee')]),
    ]
    content = 'Satori'
    edited_at = DateTime(2016, 5, 14)
    embeds = [
        Embed('Yakumo'),
        Embed('Yukari'),
    ]
    flags = MessageFlag(15)
    interaction = MessageInteraction.precreate(202305040126, name = 'Ran')
    mentioned_channels_cross_guild = [
        Channel.precreate(202305040127, channel_type = ChannelType.guild_text, name = 'Chen'),
        Channel.precreate(202305040128, channel_type = ChannelType.guild_text, name = 'Yuugi'),
    ]
    mentioned_everyone = True
    mentioned_role_ids = [202305040129, 202305040130]
    mentioned_users = [
        User.precreate(202305040131, name = 'Scarlet'),
        User.precreate(202305040132, name = 'Izaoyi'),
    ]
    message_type = MessageType.call
    nonce = 'Sakuya'
    pinned = True
    reactions = ReactionMapping({
        BUILTIN_EMOJIS['x']: [None, None],
    })
    referenced_message = Message.precreate(202305040133, content = 'Patchouli')
    role_subscription = MessageRoleSubscription(tier_name = 'Knowledge')
    stickers = [
        Sticker.precreate(202305040134, name = 'Kirisame'),
        Sticker.precreate(202305040135, name = 'Marisa'),
    ]
    thread = Channel.precreate(202305040136, channel_type = ChannelType.guild_thread_private, name = 'Yuyuko')
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
        reactions = reactions,
        referenced_message = referenced_message,
        role_subscription = role_subscription,
        stickers = stickers,
        thread = thread,
        tts = tts,
    )
    
    copy = message.copy_with()
    vampytest.assert_is_not(message, copy)
    _assert_fields_set(message)
    
    vampytest.assert_eq(message, copy)


def test__Message__copy_with__1():
    """
    Tests whether ``Message.copy_with`` works as intended.
    
    Case: No fields given.
    """
    old_activity = MessageActivity(party_id = 'Remilia')
    old_application = MessageApplication.precreate(202305040137, name = 'Flandre')
    old_application_id = 202305040138
    old_attachments = [
        Attachment.precreate(202305040139, name = 'Koishi'),
        Attachment.precreate(202305040140, name = 'Komeiji'),
    ]
    old_author = User.precreate(202305040141, name = 'Orin')
    old_call = MessageCall(ended_at = DateTime(2045, 3, 4))
    old_components = [
        Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Okuu')]),
        Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Parsee')]),
    ]
    old_content = 'Satori'
    old_edited_at = DateTime(2016, 5, 14)
    old_embeds = [
        Embed('Yakumo'),
        Embed('Yukari'),
    ]
    old_flags = MessageFlag(15)
    old_interaction = MessageInteraction.precreate(202305040142, name = 'Ran')
    old_mentioned_channels_cross_guild = [
        Channel.precreate(202305040143, channel_type = ChannelType.guild_text, name = 'Chen'),
        Channel.precreate(202305040144, channel_type = ChannelType.guild_text, name = 'Yuugi'),
    ]
    old_mentioned_everyone = True
    old_mentioned_role_ids = [202305040145, 202305040146]
    old_mentioned_users = [
        User.precreate(202305040147, name = 'Scarlet'),
        User.precreate(202305040148, name = 'Izaoyi'),
    ]
    old_message_type = MessageType.call
    old_nonce = 'Sakuya'
    old_pinned = True
    old_reactions = ReactionMapping({
        BUILTIN_EMOJIS['x']: [None, None],
    })
    old_referenced_message = Message.precreate(202305040149, content = 'Patchouli')
    old_role_subscription = MessageRoleSubscription(tier_name = 'Knowledge')
    old_stickers = [
        Sticker.precreate(202305040150, name = 'Kirisame'),
        Sticker.precreate(202305040151, name = 'Marisa'),
    ]
    old_thread = Channel.precreate(202305040152, channel_type = ChannelType.guild_thread_private, name = 'Yuyuko')
    old_tts = True
    
    new_activity = MessageActivity(party_id = 'Best girl')
    new_application = MessageApplication.precreate(202305040153, name = 'Christmas tree')
    new_application_id = 202305040154
    new_attachments = [
        Attachment.precreate(202305040155, name = 'Closed eye'),
        Attachment.precreate(202305040156, name = 'Satoris'),
    ]
    new_author = User.precreate(202305040080, name = 'Dancing')
    new_call = MessageCall(ended_at = DateTime(2045, 5, 4))
    new_components = [
        Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Nuclear bird')]),
        Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Green hell')]),
    ]
    new_content = 'Open eye'
    new_edited_at = DateTime(2016, 6, 14)
    new_embeds = [
        Embed('Old hag and pets'),
        Embed('Old hag'),
    ]
    new_flags = MessageFlag(12)
    new_interaction = MessageInteraction.precreate(202305040157, name = 'Old pet')
    new_mentioned_channels_cross_guild = [
        Channel.precreate(202305040158, channel_type = ChannelType.guild_text, name = 'Cat'),
        Channel.precreate(202305040159, channel_type = ChannelType.guild_text, name = 'One horned'),
    ]
    new_mentioned_everyone = False
    new_mentioned_role_ids = [202305040160, 202305040161]
    new_mentioned_users = [
        User.precreate(202305040162, name = 'Vampires'),
        User.precreate(202305040163, name = 'Love shop'),
    ]
    new_message_type = MessageType.user_add
    new_nonce = 'Maid'
    new_pinned = False
    new_reactions = ReactionMapping({
        BUILTIN_EMOJIS['heart']: [None],
    })
    new_referenced_message = Message.precreate(202305040164, content = 'Book')
    new_role_subscription = MessageRoleSubscription(tier_name = 'Big brain')
    new_stickers = [
        Sticker.precreate(202305040165, name = 'Magic'),
        Sticker.precreate(202305040166, name = 'Witch'),
    ]
    new_thread = Channel.precreate(202305040167, channel_type = ChannelType.guild_thread_private, name = 'Hungry')
    new_tts = False
    
    message = Message(
        activity = old_activity,
        application = old_application,
        application_id = old_application_id,
        attachments = old_attachments,
        author = old_author,
        call = old_call,
        components = old_components,
        content = old_content,
        edited_at = old_edited_at,
        embeds = old_embeds,
        flags = old_flags,
        interaction = old_interaction,
        mentioned_channels_cross_guild = old_mentioned_channels_cross_guild,
        mentioned_everyone = old_mentioned_everyone,
        mentioned_role_ids = old_mentioned_role_ids,
        mentioned_users = old_mentioned_users,
        message_type = old_message_type,
        nonce = old_nonce,
        pinned = old_pinned,
        reactions = old_reactions,
        referenced_message = old_referenced_message,
        role_subscription = old_role_subscription,
        stickers = old_stickers,
        thread = old_thread,
        tts = old_tts,
    )
    
    copy = message.copy_with(
        activity = new_activity,
        application = new_application,
        application_id = new_application_id,
        attachments = new_attachments,
        author = new_author,
        call = new_call,
        components = new_components,
        content = new_content,
        edited_at = new_edited_at,
        embeds = new_embeds,
        flags = new_flags,
        interaction = new_interaction,
        mentioned_channels_cross_guild = new_mentioned_channels_cross_guild,
        mentioned_everyone = new_mentioned_everyone,
        mentioned_role_ids = new_mentioned_role_ids,
        mentioned_users = new_mentioned_users,
        message_type = new_message_type,
        nonce = new_nonce,
        pinned = new_pinned,
        reactions = new_reactions,
        referenced_message = new_referenced_message,
        role_subscription = new_role_subscription,
        stickers = new_stickers,
        thread = new_thread,
        tts = new_tts,
    )
    vampytest.assert_is_not(message, copy)
    _assert_fields_set(message)
    
    vampytest.assert_ne(message, copy)

    vampytest.assert_eq(copy.activity, new_activity)
    vampytest.assert_eq(copy.application, new_application)
    vampytest.assert_eq(copy.application_id, new_application_id)
    vampytest.assert_eq(copy.attachments, tuple(new_attachments))
    vampytest.assert_eq(copy.author, new_author)
    vampytest.assert_eq(copy.call, new_call)
    vampytest.assert_eq(copy.components, tuple(new_components))
    vampytest.assert_eq(copy.content, new_content)
    vampytest.assert_eq(copy.edited_at, new_edited_at)
    vampytest.assert_eq(copy.embeds, tuple(new_embeds))
    vampytest.assert_eq(copy.flags, new_flags)
    vampytest.assert_eq(copy.interaction, new_interaction)
    vampytest.assert_eq(copy.mentioned_channels_cross_guild, tuple(new_mentioned_channels_cross_guild))
    vampytest.assert_eq(copy.mentioned_everyone, new_mentioned_everyone)
    vampytest.assert_eq(copy.mentioned_role_ids, tuple(new_mentioned_role_ids))
    vampytest.assert_eq(copy.mentioned_users, tuple(new_mentioned_users))
    vampytest.assert_eq(copy.nonce, new_nonce)
    vampytest.assert_eq(copy.pinned, new_pinned)
    vampytest.assert_eq(copy.reactions, new_reactions)
    vampytest.assert_eq(copy.referenced_message, new_referenced_message)
    vampytest.assert_eq(copy.role_subscription, new_role_subscription)
    vampytest.assert_eq(copy.stickers, tuple(new_stickers))
    vampytest.assert_eq(copy.thread, new_thread)
    vampytest.assert_eq(copy.tts, new_tts)
    vampytest.assert_is(copy.type, new_message_type)


def test__Message__is_deletable__0():
    """
    Tests whether ``Message.is_deletable`` works as intended.
    
    Case: non deletable message type.
    """
    for message_type in MessageType.INSTANCES.values():
        if not message_type.deletable:
            break
    else:
        raise RuntimeError('No not-deletable message type found.')
    
    message = Message(message_type = message_type)
    
    output = message.is_deletable()
    vampytest.assert_instance(output, bool)
    vampytest.assert_false(output)


def test__Message__is_deletable__1():
    """
    Tests whether ``Message.is_deletable`` works as intended.
    
    Case: deleted.
    """
    message = Message()
    message.deleted = True
    
    output = message.is_deletable()
    vampytest.assert_instance(output, bool)
    vampytest.assert_false(output)


def test__Message__is_deletable__2():
    """
    Tests whether ``Message.is_deletable`` works as intended.
    
    Case: invoking user only.
    """
    message = Message(flags = MessageFlag().update_by_keys(invoking_user_only = True))
    
    output = message.is_deletable()
    vampytest.assert_instance(output, bool)
    vampytest.assert_false(output)


def test__Message__is_deletable__3():
    """
    Tests whether ``Message.is_deletable`` works as intended.
    
    Case: Passing.
    """
    message = Message()
    
    output = message.is_deletable()
    vampytest.assert_instance(output, bool)
    vampytest.assert_true(output)


def test__Message__did_react__0():
    """
    Tests whether ``Message.did_react`` works as intended.
    
    Case: No reactions.
    """
    user_0 = User.precreate(202305040169)
    emoji_0 = BUILTIN_EMOJIS['x']
    
    message = Message()
    
    output = message.did_react(emoji_0, user_0)
    
    vampytest.assert_instance(output, bool)
    vampytest.assert_false(output)


def test__Message__did_react__emoji_mismatch():
    """
    Tests whether ``Message.did_react`` works as intended.
    
    Case: Emoji mismatch.
    """
    user_0 = User.precreate(202305040170)
    
    reaction_0 = Reaction(BUILTIN_EMOJIS['x'], reaction_type = ReactionType.standard)
    reaction_1 = Reaction(BUILTIN_EMOJIS['heart'], reaction_type = ReactionType.standard)
    
    message = Message()
    message._add_reaction(reaction_1, user_0)
    
    output = message.did_react(reaction_0, user_0)
    
    vampytest.assert_instance(output, bool)
    vampytest.assert_false(output)


def _iter_options__did_react():
    user_0 = User.precreate(202305040171)
    user_1 = User.precreate(202305040172)
    
    emoji_0 = BUILTIN_EMOJIS['x']
    emoji_1 = BUILTIN_EMOJIS['heart']
    emoji_2 = BUILTIN_EMOJIS['green_heart']
    
    reaction_0 = Reaction(emoji_0, reaction_type = ReactionType.standard)
    reaction_1 = Reaction(emoji_0, reaction_type = ReactionType.burst)
    reaction_2 = Reaction(emoji_1, reaction_type = ReactionType.standard)
    reaction_3 = Reaction(emoji_1, reaction_type = ReactionType.burst)
    reaction_4 = Reaction(emoji_2, reaction_type = ReactionType.standard)
    reaction_5 = Reaction(emoji_2, reaction_type = ReactionType.burst)
    
    
    message = Message()
    message._add_reaction(reaction_0, user_0)
    message._add_reaction(reaction_2, user_1)
    message._add_reaction(reaction_2, user_0)
    message._add_reaction(reaction_3, user_0)
    
    yield message, emoji_0, user_0, True
    yield message, emoji_1, user_0, True
    yield message, emoji_2, user_0, False
    yield message, reaction_0, user_0, True
    yield message, reaction_1, user_0, False
    yield message, reaction_2, user_0, True
    yield message, reaction_3, user_0, True
    yield message, reaction_4, user_0, False
    yield message, reaction_5, user_0, False

    yield message, emoji_0, user_1, False
    yield message, emoji_1, user_1, True
    yield message, emoji_2, user_1, False
    yield message, reaction_0, user_1, False
    yield message, reaction_1, user_1, False
    yield message, reaction_2, user_1, True
    yield message, reaction_3, user_1, False
    yield message, reaction_4, user_1, False
    yield message, reaction_5, user_1, False


@vampytest._(vampytest.call_from(_iter_options__did_react()).returning_last())
def test__Message__did_react(message, reaction_or_emoji, user):
    """
    Tests whether ``Message.did_react`` works as intended.
    
    Parameters
    ----------
    message : ``Message``
        Message to check.
    reaction_or_emoji : ``Reaction``, ``Emoji``
        The reaction or emoji to request.
    user : ``ClientUserBase``
        The user who perhaps reacted.
    
    Returns
    -------
    output : `bool`
    """
    output = message.did_react(reaction_or_emoji, user)
    vampytest.assert_instance(output, bool)
    return output


def test__Message__guild():
    """
    Tests whether ``Message.guild`` works as intended.
    """
    guild_id_0 = 202305050000
    guild_id_1 = 202305050001
    guild_0 = Guild.precreate(guild_id_0)
    
    for message_id, input_value, expected_output in (
        (202305050002, 0, None),
        (202305050003, guild_id_0, guild_0),
        (202305050004, guild_id_1, None),
    ):
        output = Message.precreate(message_id, guild_id = input_value).guild
        vampytest.assert_is(output, expected_output)


def test__Message__channel():
    """
    Tests whether ``Message.channel`` works as intended.
    """
    channel_id = 202305050005
    message_id = 202305050006
    guild_id = 202305050007
    
    message = Message.precreate(message_id, channel_id = channel_id, guild_id = guild_id)
    
    output = message.channel
    vampytest.assert_instance(output, Channel)
    vampytest.assert_eq(output.id, channel_id)
    vampytest.assert_eq(output.guild_id, guild_id)


def test__Message__clean_content__0():
    """
    Tests whether Message.clean_content`` works as intended.
    
    Case: default.
    """
    content = 'arara'
    
    message = Message(content = content)
    
    output = message.clean_content
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, content)


def test__Message__clean_content__1():
    """
    Tests whether Message.clean_content`` works as intended.
    
    Case: Non-default.
    """
    content = 'arara'
    
    message = Message(content = content, message_type = MessageType.call)
    
    output = message.clean_content
    vampytest.assert_instance(output, str)
    vampytest.assert_ne(output, content)


def test__Message__mentions():
    """
    Tests whether ``Message.mentions`` works as intended.
    """
    channel_id = 202305050008
    user_id = 202305050009
    role_id = 202305050010
    
    channel = Channel.precreate(channel_id)
    role = Role.precreate(role_id)
    user = User.precreate(user_id)
    
    content = f'{channel:m} {user:m} {role:m} @everyone'
    message = Message(
        content = content,
        mentioned_role_ids = [role_id],
        mentioned_users = [user],
        mentioned_everyone = True
    )
    
    output = message.mentions
    vampytest.assert_instance(output, list)
    vampytest.assert_eq({*output}, {channel, role, user, 'everyone'})
    
    
def test__Message__clean_embeds():
    """
    Tests whether ``Message.clean_embeds`` works as intended.
    """
    channel_id = 202305050011
    channel_name = 'yukari'
    
    channel = Channel.precreate(channel_id, name = channel_name, channel_type = ChannelType.guild_text)
    
    embeds = [
        Embed(description = channel.mention),
        Embed(embed_type = EmbedType.image),
    ]
    
    message = Message(embeds = embeds)
    
    output = message.clean_embeds
    vampytest.assert_instance(output, list)
    vampytest.assert_eq(
        output,
        [
            Embed(description = '#' + channel.name)
        ],
    )


def test__Message__mentioned_channels():
    """
    Tests whether ``Message.mentioned_channels`` works as intended.
    """
    channel_id = 202305050012
    channel = Channel.precreate(channel_id)
    
    for input_value, expected_output in (
        (None, None),
        (channel.mention, (channel,)),
    ):
        message = Message(content = input_value)
        output = message.mentioned_channels
        vampytest.assert_instance(output, tuple, nullable = True)
        vampytest.assert_eq(output, expected_output)


def test__Message__mentioned_roles():
    """
    Tests whether ``Message.mentioned_roles`` works as intended.
    """
    role_id = 202305050013
    role = Role.precreate(role_id)
    
    for input_value, expected_output in (
        (None, None),
        ([role_id], (role,)),
    ):
        message = Message(mentioned_role_ids = input_value)
        output = message.mentioned_roles
        vampytest.assert_instance(output, tuple, nullable = True)
        vampytest.assert_eq(output, expected_output)


def test__Message__deleted():
    """
    Tests whether ``Message.deleted`` works as intended.
    """
    message = Message()
    
    output = message.deleted
    vampytest.assert_instance(output, bool)
    vampytest.assert_false(output)
    
    message.deleted = True
    output = message.deleted
    vampytest.assert_instance(output, bool)
    vampytest.assert_true(output)

    message.deleted = False
    output = message.deleted
    vampytest.assert_instance(output, bool)
    vampytest.assert_false(output)


def test__Message__partial__template():
    """
    Tests whether ``Message.partial`` works as intended.
    
    Case: template.
    """
    message = Message()
    
    output = message.partial
    vampytest.assert_instance(output, bool)
    vampytest.assert_true(output)


def test__Message__partial__precreated():
    """
    Tests whether ``Message.partial`` works as intended.
    
    Case: template.
    """
    message_id = 202305050014
    message = Message.precreate(message_id)
    
    output = message.partial
    vampytest.assert_instance(output, bool)
    vampytest.assert_true(output)


def test__Message__partial__from_data():
    """
    Tests whether ``Message.partial`` works as intended.
    
    Case: template.
    """
    message_id = 202305050015
    message = Message.from_data({'id': str(message_id)})
    
    output = message.partial
    vampytest.assert_instance(output, bool)
    vampytest.assert_false(output)


def test__Message__attachment():
    """
    Tests whether ``Message.attachment`` works as intended.
    """
    attachment_0 = Attachment.precreate(202305050016, name = 'Koishi')
    attachment_1 = Attachment.precreate(202305050017, name = 'Satori')
    
    for input_value, expected_output in (
        (None, None),
        ([attachment_1], attachment_1),
        ([attachment_0, attachment_1], attachment_0),
    ):
        message = Message(attachments = input_value)
        output = message.attachment
        vampytest.assert_eq(output, expected_output)


def test__Message__embed():
    """
    Tests whether ``message.embed`` works as intended.
    """
    embed_0 = Embed('Koishi')
    embed_1 = Embed('Satori')
    
    for input_value, expected_output in (
        (None, None),
        ([embed_1], embed_1),
        ([embed_0, embed_1], embed_0),
    ):
        message = Message(embeds = input_value)
        output = message.embed
        vampytest.assert_eq(output, expected_output)


def test__Message__sticker():
    """
    Tests whether ``Message.sticker`` works as intended.
    """
    sticker_0 = Sticker.precreate(202305050018, name = 'Koishi')
    sticker_1 = Sticker.precreate(202305050019, name = 'Satori')
    
    for input_value, expected_output in (
        (None, None),
        ([sticker_1], sticker_1),
        ([sticker_0, sticker_1], sticker_0),
    ):
        message = Message(stickers = input_value)
        output = message.sticker
        vampytest.assert_eq(output, expected_output)


def test__Message__iter_attachments():
    """
    Tests whether ``Message.iter_attachments`` works as intended.
    """
    attachment_0 = Attachment.precreate(202305050020, name = 'Koishi')
    attachment_1 = Attachment.precreate(202305050021, name = 'Satori')
    
    for input_value, expected_output in (
        (None, []),
        ([attachment_1], [attachment_1]),
        ([attachment_0, attachment_1], [attachment_0, attachment_1]),
    ):
        message = Message(attachments = input_value)
        output = [*message.iter_attachments()]
        vampytest.assert_eq(output, expected_output)


def test__Message__iter_components():
    """
    Tests whether ``Message.iter_components`` works as intended.
    """
    component_0 = Component(ComponentType.button, label = 'Koishi')
    component_1 = Component(ComponentType.button, label = 'Satori')
    
    for input_value, expected_output in (
        (None, []),
        ([component_1], [component_1]),
        ([component_0, component_1], [component_0, component_1]),
    ):
        message = Message(components = input_value)
        output = [*message.iter_components()]
        vampytest.assert_eq(output, expected_output)


def test__Message__iter_embeds():
    """
    Tests whether ``Message.iter_embeds`` works as intended.
    """
    embed_0 = Embed('Koishi')
    embed_1 = Embed('Satori')
    
    for input_value, expected_output in (
        (None, []),
        ([embed_1], [embed_1]),
        ([embed_0, embed_1], [embed_0, embed_1]),
    ):
        message = Message(embeds = input_value)
        output = [*message.iter_embeds()]
        vampytest.assert_eq(output, expected_output)


def test__Message__iter_mentioned_channels():
    """
    Tests whether ``Message.iter_mentioned_channels`` works as intended.
    """
    channel_id_0 = 202305050022
    channel_id_1 = 202305050023
    channel_0 = Channel.precreate(channel_id_0)
    channel_1 = Channel.precreate(channel_id_1)
    
    for input_value, expected_output in (
        (None, []),
        (channel_1.mention, [channel_1,]),
        (channel_0.mention + channel_1.mention, [channel_0, channel_1]),
    ):
        message = Message(content = input_value)
        output = [*message.iter_mentioned_channels()]
        vampytest.assert_eq(output, expected_output)


def test__Message__iter_mentioned_channels_cross_guild():
    """
    Tests whether ``Message.iter_mentioned_channels_cross_guild`` works as intended.
    """
    channel_id_0 = 202305050024
    channel_id_1 = 202305050025
    channel_0 = Channel.precreate(channel_id_0)
    channel_1 = Channel.precreate(channel_id_1)
    
    for input_value, expected_output in (
        (None, []),
        ([channel_1], [channel_1,]),
        ([channel_0, channel_1], [channel_0, channel_1]),
    ):
        message = Message(mentioned_channels_cross_guild = input_value)
        output = [*message.iter_mentioned_channels_cross_guild()]
        vampytest.assert_eq(output, expected_output)


def test__Message__iter_mentioned_role_ids():
    """
    Tests whether ``Message.iter_mentioned_role_ids`` works as intended.
    """
    role_id_0 = 202305050026
    role_id_1 = 202305050027
    
    for input_value, expected_output in (
        (None, []),
        ([role_id_1], [role_id_1,]),
        ([role_id_0, role_id_1], [role_id_0, role_id_1]),
    ):
        message = Message(mentioned_role_ids = input_value)
        output = [*message.iter_mentioned_role_ids()]
        vampytest.assert_eq(output, expected_output)


def test__Message__iter_mentioned_roles():
    """
    Tests whether ``Message.iter_mentioned_roles`` works as intended.
    """
    role_id_0 = 202305050028
    role_id_1 = 202305050029
    role_0 = Role.precreate(role_id_0)
    role_1 = Role.precreate(role_id_1)
    
    for input_value, expected_output in (
        (None, []),
        ([role_id_1], [role_1,]),
        ([role_id_0, role_id_1], [role_0, role_1]),
    ):
        message = Message(mentioned_role_ids = input_value)
        output = [*message.iter_mentioned_roles()]
        vampytest.assert_eq(output, expected_output)


def test__Message__iter_mentioned_users():
    """
    Tests whether ``Message.iter_mentioned_users`` works as intended.
    """
    user_id_0 = 202305050030
    user_id_1 = 202305050031
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)
    
    for input_value, expected_output in (
        (None, []),
        ([user_1], [user_1,]),
        ([user_0, user_1], [user_0, user_1]),
    ):
        message = Message(mentioned_users = input_value)
        output = [*message.iter_mentioned_users()]
        vampytest.assert_eq(output, expected_output)


def test__Message__iter_stickers():
    """
    Tests whether ``Message.iter_stickers`` works as intended.
    """
    sticker_id_0 = 202305050032
    sticker_id_1 = 202305050033
    sticker_0 = Sticker.precreate(sticker_id_0)
    sticker_1 = Sticker.precreate(sticker_id_1)
    
    for input_value, expected_output in (
        (None, []),
        ([sticker_1], [sticker_1,]),
        ([sticker_0, sticker_1], [sticker_0, sticker_1]),
    ):
        message = Message(stickers = input_value)
        output = [*message.iter_stickers()]
        vampytest.assert_eq(output, expected_output)


def test__Message__has_activity():
    """
    Tests whether ``Message.has_activity`` works as intended.
    """
    activity = MessageActivity(party_id = 'Remilia')
    
    for input_value, expected_output in (
        (None, False),
        (activity, True),
    ):
        message = Message(activity = input_value)
        output = message.has_activity()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, expected_output)


def test__Message__has_application():
    """
    Tests whether ``Message.has_application`` works as intended.
    """
    application = MessageApplication.precreate(202305050034, name = 'Flandre')
    
    for input_value, expected_output in (
        (None, False),
        (application, True),
    ):
        message = Message(application = input_value)
        output = message.has_application()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, expected_output)


def test__Message__has_application_id():
    """
    Tests whether ``Message.has_application_id`` works as intended.
    """
    application_id = 202305050035
    
    for input_value, expected_output in (
        (None, False),
        (application_id, True),
    ):
        message = Message(application_id = input_value)
        output = message.has_application_id()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, expected_output)


def test__Message__has_attachments():
    """
    Tests whether ``Message.has_attachments`` works as intended.
    """
    attachments = [
        Attachment.precreate(202305050036, name = 'Koishi'),
        Attachment.precreate(202305050037, name = 'Komeiji'),
    ]
    
    for input_value, expected_output in (
        (None, False),
        (attachments, True),
    ):
        message = Message(attachments = input_value)
        output = message.has_attachments()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, expected_output)


def test__Message__has_components():
    """
    Tests whether ``Message.has_components`` works as intended.
    """
    components = [
        Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Okuu')]),
        Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Parsee')]),
    ]
    
    for input_value, expected_output in (
        (None, False),
        (components, True),
    ):
        message = Message(components = input_value)
        output = message.has_components()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, expected_output)


def test__Message__has_content():
    """
    Tests whether ``Message.has_content`` works as intended.
    """
    content = 'Satori'
    
    for input_value, expected_output in (
        (None, False),
        (content, True),
    ):
        message = Message(content = input_value)
        output = message.has_content()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, expected_output)


def test__Message__has_edited_at():
    """
    Tests whether ``Message.has_edited_at`` works as intended.
    """
    edited_at = DateTime(2016, 5, 14)
    
    for input_value, expected_output in (
        (None, False),
        (edited_at, True),
    ):
        message = Message(edited_at = input_value)
        output = message.has_edited_at()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, expected_output)


def test__Message__has_embeds():
    """
    Tests whether ``Message.has_embeds`` works as intended.
    """
    embeds = [
        Embed('Yakumo'),
        Embed('Yukari'),
    ]
    
    for input_value, expected_output in (
        (None, False),
        (embeds, True),
    ):
        message = Message(embeds = input_value)
        output = message.has_embeds()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, expected_output)


def test__Message__has_flags():
    """
    Tests whether ``Message.has_flags`` works as intended.
    """
    flags = MessageFlag(15)
    
    for input_value, expected_output in (
        (None, False),
        (flags, True),
    ):
        message = Message(flags = input_value)
        output = message.has_flags()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, expected_output)


def test__Message__has_interaction():
    """
    Tests whether ``Message.has_interaction`` works as intended.
    """
    interaction = MessageInteraction.precreate(202305050038, name = 'Ran')
    
    for input_value, expected_output in (
        (None, False),
        (interaction, True),
    ):
        message = Message(interaction = input_value)
        output = message.has_interaction()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, expected_output)


def test__Message__has_mentioned_channels():
    """
    Tests whether ``Message.has_mentioned_channels`` works as intended.
    """
    channel_0 = Channel.precreate(202305050039, channel_type = ChannelType.guild_text, name = 'Chen')
    
    for input_value, expected_output in (
        (None, False),
        (channel_0.mention, True),
    ):
        message = Message(content = input_value)
        output = message.has_mentioned_channels()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, expected_output)


def test__Message__has_mentioned_channels_cross_guild():
    """
    Tests whether ``Message.has_mentioned_channels_cross_guild`` works as intended.
    """
    mentioned_channels_cross_guild = [
        Channel.precreate(202305050041, channel_type = ChannelType.guild_text, name = 'Chen'),
        Channel.precreate(202305050042, channel_type = ChannelType.guild_text, name = 'Yuugi'),
    ]
    
    for input_value, expected_output in (
        (None, False),
        (mentioned_channels_cross_guild, True),
    ):
        message = Message(mentioned_channels_cross_guild = input_value)
        output = message.has_mentioned_channels_cross_guild()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, expected_output)


def test__Message__has_mentioned_everyone():
    """
    Tests whether ``Message.has_mentioned_everyone`` works as intended.
    """
    for input_value, expected_output in (
        (False, False),
        (True, True),
    ):
        message = Message(mentioned_everyone = input_value)
        output = message.has_mentioned_everyone()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, expected_output)


def test__Message__has_mentioned_role_ids():
    """
    Tests whether ``Message.has_mentioned_role_ids`` works as intended.
    """
    mentioned_role_ids = [202305050043, 202305050044]
    
    for input_value, expected_output in (
        (None, False),
        (mentioned_role_ids, True),
    ):
        message = Message(mentioned_role_ids = input_value)
        output = message.has_mentioned_role_ids()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, expected_output)


def test__Message__has_mentioned_roles():
    """
    Tests whether ``Message.has_mentioned_roles`` works as intended.
    """
    mentioned_role_ids = [202305050045, 202305050046]
    
    for input_value, expected_output in (
        (None, False),
        (mentioned_role_ids, True),
    ):
        message = Message(mentioned_role_ids = input_value)
        output = message.has_mentioned_roles()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, expected_output)


def test__Message__has_mentioned_users():
    """
    Tests whether ``Message.has_mentioned_users`` works as intended.
    """
    mentioned_users = [
        User.precreate(202305050047, name = 'Scarlet'),
        User.precreate(202305050048, name = 'Izaoyi'),
    ]
    
    for input_value, expected_output in (
        (None, False),
        (mentioned_users, True),
    ):
        message = Message(mentioned_users = input_value)
        output = message.has_mentioned_users()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, expected_output)


def test__Message__has_nonce():
    """
    Tests whether ``Message.has_nonce`` works as intended.
    """
    nonce = 'Sakuya'
    
    for input_value, expected_output in (
        (None, False),
        (nonce, True),
    ):
        message = Message(nonce = input_value)
        output = message.has_nonce()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, expected_output)


def test__Message__has_pinned():
    """
    Tests whether ``Message.has_pinned`` works as intended.
    """
    for input_value, expected_output in (
        (False, False),
        (True, True),
    ):
        message = Message(pinned = input_value)
        output = message.has_pinned()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, expected_output)


def test__Message__has_reactions():
    """
    Tests whether ``Message.has_reactions`` works as intended.
    """
    reactions = ReactionMapping({
        BUILTIN_EMOJIS['x']: [None, None],
    })
    
    for input_value, expected_output in (
        (None, False),
        (ReactionMapping(), False),
        (reactions, True),
    ):
        message = Message(reactions = input_value)
        output = message.has_reactions()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, expected_output)


def test__Message__has_referenced_message():
    """
    Tests whether ``Message.has_referenced_message`` works as intended.
    """
    referenced_message = Message.precreate(202305050049, content = 'Patchouli')
    
    for input_value, expected_output in (
        (None, False),
        (referenced_message, True),
    ):
        message = Message(referenced_message = input_value)
        output = message.has_referenced_message()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, expected_output)


def test__Message__has_role_subscription():
    """
    Tests whether ``Message.has_role_subscription`` works as intended.
    """
    role_subscription = MessageRoleSubscription(tier_name = 'Knowledge')
    
    for input_value, expected_output in (
        (None, False),
        (role_subscription, True),
    ):
        message = Message(role_subscription = input_value)
        output = message.has_role_subscription()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, expected_output)


def test__Message__has_stickers():
    """
    Tests whether ``Message.has_stickers`` works as intended.
    """
    stickers = [
        Sticker.precreate(202305050050, name = 'Kirisame'),
        Sticker.precreate(202305050051, name = 'Marisa'),
    ]
    
    for input_value, expected_output in (
        (None, False),
        (stickers, True),
    ):
        message = Message(stickers = input_value)
        output = message.has_stickers()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, expected_output)


def test__Message__has_thread():
    """
    Tests whether ``Message.has_thread`` works as intended.
    """
    thread = Channel.precreate(202305050052, channel_type = ChannelType.guild_thread_private, name = 'Yuyuko')
    
    for input_value, expected_output in (
        (None, False),
        (thread, True),
    ):
        message = Message(thread = input_value)
        output = message.has_thread()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, expected_output)


def test__Message__has_tts():
    """
    Tests whether ``Message.has_tts`` works as intended.
    """
    for input_value, expected_output in (
        (False, False),
        (True, True),
    ):
        message = Message(tts = input_value)
        output = message.has_tts()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, expected_output)


def test__Message__has_type():
    """
    Tests whether ``Message.has_type`` works as intended.
    """
    message_type = MessageType.call
    
    for input_value, expected_output in (
        (None, False),
        (message_type, True),
    ):
        message = Message(message_type = input_value)
        output = message.has_type()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, expected_output)
