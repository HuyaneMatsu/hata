from datetime import datetime as DateTime

import vampytest

from ....channel import Channel, ChannelType
from ....component import Component, ComponentType
from ....core import BUILTIN_EMOJIS
from ....embed import EmbedAuthor, Embed, EmbedField, EmbedFooter, EmbedProvider, EmbedType
from ....emoji import Reaction, ReactionMapping, ReactionType
from ....guild import Guild
from ....interaction import Resolved
from ....poll import Poll, PollAnswer, PollQuestion, PollResult
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


def test__Message__iter_contents__all_contents():
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
    poll_question_text = 'marisa'
    poll_answer_0_text = 'junko'
    poll_answer_1_text = 'clown'
    
    embed_0 = Embed(title = embed_0_title, description = embed_0_description)
    embed_0.author = EmbedAuthor(embed_0_author_name)
    embed_0.fields = [
        EmbedField(embed_0_field_0_name, embed_0_field_0_value),
        EmbedField(embed_0_field_1_name, embed_0_field_1_value),
    ]
    embed_0.footer = EmbedFooter(embed_0_footer_text)
    embed_0.provider = EmbedProvider(embed_0_provider_name)
    
    embed_1 = Embed(title = embed_1_title)
    
    poll = Poll(
        answers = [PollAnswer(text = poll_answer_0_text), PollAnswer(text = poll_answer_1_text)],
        question = PollQuestion(text = poll_question_text),
    )
    
    message = Message(content = message_content, embeds = [embed_0, embed_1], poll = poll)
    
    
    contents = {
        embed_0_title, embed_0_author_name, embed_0_description, embed_0_field_0_name, embed_0_field_0_value,
        embed_0_field_1_name, embed_0_field_1_value, embed_0_footer_text, embed_0_provider_name,
        message_content, embed_1_title, poll_question_text, poll_answer_0_text, poll_answer_1_text
    }
    
    vampytest.assert_eq({*message.iter_contents()}, contents)


def test__Message__iter_contents__no_contents():
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
    poll_question_text = 'marisa'
    poll_answer_0_text = 'junko'
    poll_answer_1_text = 'clown'
    
    embed_0 = Embed(title = embed_0_title, description = embed_0_description)
    embed_0.author = EmbedAuthor(embed_0_author_name)
    embed_0.fields = [
        EmbedField(embed_0_field_0_name, embed_0_field_0_value),
        EmbedField(embed_0_field_1_name, embed_0_field_1_value),
    ]
    embed_0.footer = EmbedFooter(embed_0_footer_text)
    embed_0.provider = EmbedProvider(embed_0_provider_name)
    
    embed_1 = Embed(title = embed_1_title)
    
    poll = Poll(
        answers = [PollAnswer(text = poll_answer_0_text), PollAnswer(text = poll_answer_1_text)],
        question = PollQuestion(text = poll_question_text),
    )
    
    message = Message(content = message_content, embeds = [embed_0, embed_1], poll = poll)
    
    contents = {
        embed_0_title, embed_0_author_name, embed_0_description, embed_0_field_0_name, embed_0_field_0_value,
        embed_0_field_1_name, embed_0_field_1_value, embed_0_footer_text, embed_0_provider_name,
        message_content, embed_1_title, poll_question_text, poll_answer_0_text, poll_answer_1_text
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
    poll = Poll(expires_at = DateTime(2016, 5, 14))
    reactions = ReactionMapping({
        BUILTIN_EMOJIS['x']: [None, None],
    })
    referenced_message = Message.precreate(202305040107, content = 'Patchouli')
    resolved = Resolved(attachments = [Attachment.precreate(202310110034)])
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
        poll = poll,
        reactions = reactions,
        referenced_message = referenced_message,
        resolved = resolved,
        role_subscription = role_subscription,
        stickers = stickers,
        thread = thread,
        tts = tts,
    )
    
    copy = message.copy()
    vampytest.assert_is_not(message, copy)
    _assert_fields_set(message)
    
    vampytest.assert_eq(message, copy)


def test__Message__copy_with__no_fields():
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
    poll = Poll(expires_at = DateTime(2016, 5, 14))
    reactions = ReactionMapping({
        BUILTIN_EMOJIS['x']: [None, None],
    })
    referenced_message = Message.precreate(202305040133, content = 'Patchouli')
    resolved = Resolved(attachments = [Attachment.precreate(202310110035)])
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
        poll = poll,
        reactions = reactions,
        referenced_message = referenced_message,
        resolved = resolved,
        role_subscription = role_subscription,
        stickers = stickers,
        thread = thread,
        tts = tts,
    )
    
    copy = message.copy_with()
    vampytest.assert_is_not(message, copy)
    _assert_fields_set(message)
    
    vampytest.assert_eq(message, copy)


def test__Message__copy_with__all_fields():
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
    old_poll = Poll(expires_at = DateTime(2016, 5, 14))
    old_reactions = ReactionMapping({
        BUILTIN_EMOJIS['x']: [None, None],
    })
    old_referenced_message = Message.precreate(202305040149, content = 'Patchouli')
    old_resolved = Resolved(attachments = [Attachment.precreate(202310110036)])
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
    new_poll = Poll(expires_at = DateTime(2016, 5, 15))
    new_reactions = ReactionMapping({
        BUILTIN_EMOJIS['heart']: [None],
    })
    new_referenced_message = Message.precreate(202305040164, content = 'Book')
    new_resolved = Resolved(attachments = [Attachment.precreate(202310110036)])
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
        poll = old_poll,
        reactions = old_reactions,
        referenced_message = old_referenced_message,
        resolved = old_resolved,
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
        poll = new_poll,
        reactions = new_reactions,
        referenced_message = new_referenced_message,
        resolved = new_resolved,
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
    vampytest.assert_eq(copy.poll, new_poll)
    vampytest.assert_eq(copy.reactions, new_reactions)
    vampytest.assert_eq(copy.referenced_message, new_referenced_message)
    vampytest.assert_eq(copy.resolved, new_resolved)
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


def _iter_options__guild():
    guild_id_0 = 202305050000
    guild_id_1 = 202305050001
    guild_0 = Guild.precreate(guild_id_0)
    
    yield 202305050002, 0, None
    yield 202305050003, guild_id_0, guild_0
    yield 202305050004, guild_id_1, None


@vampytest._(vampytest.call_from(_iter_options__guild()).returning_last())
def test__Message__guild(message_id, input_value):
    """
    Tests whether ``Message.guild`` works as intended.
    
    Parameters
    ----------
    message_id : `int`
        Message identifier to create the instance with.
    input_value : `int`
        Value to test with.
    
    Returns
    -------
    output : `None | Guild`
    """
    message = Message.precreate(message_id, guild_id = input_value)
    output = message.guild
    vampytest.assert_instance(output, Guild, nullable = True)
    return output


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


def test__Message__clean_content__default():
    """
    Tests whether Message.clean_content`` works as intended.
    
    Case: default.
    """
    content = 'arara'
    
    message = Message(content = content)
    
    output = message.clean_content
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, content)


def test__Message__clean_content__non_default():
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


def _iter_options__mentioned_channels():
    channel_0 = Channel.precreate(202305050012)
    channel_1 = Channel.precreate(202305050057)
    
    yield None, None
    yield channel_0.mention, (channel_0, )
    yield channel_0.mention + channel_1.mention, (channel_0, channel_1)


@vampytest._(vampytest.call_from(_iter_options__mentioned_channels()).returning_last())
def test__Message__mentioned_channels(input_value):
    """
    Tests whether ``Message.mentioned_channels`` works as intended.
    
    Parameters
    ----------
    input_value : `None | str`
        Value to test with.
    
    Returns
    -------
    output : `None | tuple<Channel>`
    """
    message = Message(content = input_value)
    return message.mentioned_channels


def _iter_options__mentioned_roles():
    role_id_0 = 202305050013
    role_id_1 = 202305050056
    role_0 = Role.precreate(role_id_0)
    role_1 = Role.precreate(role_id_1)
    
    yield None, None
    yield [role_id_0], (role_0,)
    yield [role_id_0, role_id_1], (role_0, role_1)


@vampytest._(vampytest.call_from(_iter_options__mentioned_roles()).returning_last())
def test__Message__mentioned_roles(input_value):
    """
    Tests whether ``Message.mentioned_roles`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<int>`
        Value to test with.
    
    Returns
    -------
    output : `None | tuple<Role>`
    """
    message = Message(mentioned_role_ids = input_value)
    return message.mentioned_roles


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


def _iter_options__attachment():
    attachment_0 = Attachment.precreate(202305050016, name = 'Koishi')
    attachment_1 = Attachment.precreate(202305050017, name = 'Satori')
    
    yield None, None
    yield [attachment_1], attachment_1
    yield [attachment_0, attachment_1], attachment_0


@vampytest._(vampytest.call_from(_iter_options__attachment()).returning_last())
def test__Message__attachment(input_value):
    """
    Tests whether ``Message.attachment`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<Attachment>`
        Value to test with.
    
    Returns
    -------
    output : `NNone | Attachment`
    """
    message = Message(attachments = input_value)
    output = message.attachment
    vampytest.assert_instance(output, Attachment, nullable = True)
    return output


def _iter_options__embed():
    embed_0 = Embed('Koishi')
    embed_1 = Embed('Satori')
    
    yield None, None
    yield [embed_1], embed_1
    yield [embed_0, embed_1], embed_0


@vampytest._(vampytest.call_from(_iter_options__embed()).returning_last())
def test__Message__embed(input_value):
    """
    Tests whether ``Message.embed`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<Embed>`
        Value to test with.
    
    Returns
    -------
    output : `NNone | Embed`
    """
    message = Message(embeds = input_value)
    output = message.embed
    vampytest.assert_instance(output, Embed, nullable = True)
    return output


def _iter_options__sticker():
    sticker_0 = Sticker.precreate(202305050018, name = 'Koishi')
    sticker_1 = Sticker.precreate(202305050019, name = 'Satori')
    
    yield None, None
    yield [sticker_1], sticker_1
    yield [sticker_0, sticker_1], sticker_0


@vampytest._(vampytest.call_from(_iter_options__sticker()).returning_last())
def test__Message__sticker(input_value):
    """
    Tests whether ``Message.sticker`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<Sticker>`
        Value to test with.
    
    Returns
    -------
    output : `NNone | Sticker`
    """
    message = Message(stickers = input_value)
    output = message.sticker
    vampytest.assert_instance(output, Sticker, nullable = True)
    return output


def _iter_options__iter_attachments():
    attachment_0 = Attachment.precreate(202305050020, name = 'Koishi')
    attachment_1 = Attachment.precreate(202305050021, name = 'Satori')
    
    yield None, []
    yield [attachment_0], [attachment_0]
    yield [attachment_0, attachment_1], [attachment_0, attachment_1]


@vampytest._(vampytest.call_from(_iter_options__iter_attachments()).returning_last())
def test__Message__iter_attachments(input_value):
    """
    Tests whether ``Message.iter_attachments`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<Attachment>`
        Value to test with.
    
    Returns
    -------
    output : `list<Attachment>`
    """
    message = Message(attachments = input_value)
    return [*message.iter_attachments()]


def _iter_options__iter_components():
    component_0 = Component(ComponentType.button, label = 'Koishi')
    component_1 = Component(ComponentType.button, label = 'Satori')
    
    yield None, []
    yield [component_0], [component_0]
    yield [component_0, component_1], [component_0, component_1]


@vampytest._(vampytest.call_from(_iter_options__iter_components()).returning_last())
def test__Message__iter_components(input_value):
    """
    Tests whether ``Message.iter_components`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<Component>`
        Value to test with.
    
    Returns
    -------
    output : `list<Component>`
    """
    message = Message(components = input_value)
    return [*message.iter_components()]


def _iter_options__iter_embeds():
    embed_0 = Embed('Koishi')
    embed_1 = Embed('Satori')
    
    yield None, []
    yield [embed_0], [embed_0]
    yield [embed_0, embed_1], [embed_0, embed_1]


@vampytest._(vampytest.call_from(_iter_options__iter_embeds()).returning_last())
def test__Message__iter_embeds(input_value):
    """
    Tests whether ``Message.iter_embeds`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<Embed>`
        Value to test with.
    
    Returns
    -------
    output : `list<Embed>`
    """
    message = Message(embeds = input_value)
    return [*message.iter_embeds()]


def _iter_options__iter_mentioned_channels():
    channel_0 = Channel.precreate(202305050022)
    channel_1 = Channel.precreate(202305050023)
    
    yield None, []
    yield channel_0.mention, [channel_0]
    yield channel_0.mention + channel_1.mention, [channel_0, channel_1]


@vampytest._(vampytest.call_from(_iter_options__iter_mentioned_channels()).returning_last())
def test__Message__iter_mentioned_channels(input_value):
    """
    Tests whether ``Message.iter_mentioned_channels`` works as intended.
    
    Parameters
    ----------
    input_value : `None | str`
        Value to test with.
    
    Returns
    -------
    output : `list<Channel>`
    """
    message = Message(content = input_value)
    return [*message.iter_mentioned_channels()]


def _iter_options__iter_mentioned_channels_cross_guild():
    channel_0 = Channel.precreate(202305050024)
    channel_1 = Channel.precreate(202305050025)
    
    yield None, []
    yield [channel_0], [channel_0]
    yield [channel_0, channel_1], [channel_0, channel_1]


@vampytest._(vampytest.call_from(_iter_options__iter_mentioned_channels_cross_guild()).returning_last())
def test__Message__iter_mentioned_channels_cross_guild(input_value):
    """
    Tests whether ``Message.iter_mentioned_channels_cross_guild`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<Channel>`
        Value to test with.
    
    Returns
    -------
    output : `list<Channel>`
    """
    message = Message(mentioned_channels_cross_guild = input_value)
    return [*message.iter_mentioned_channels_cross_guild()]


def _iter_options__iter_mentioned_role_ids():
    role_id_0 = 202305050026
    role_id_1 = 202305050027
    
    yield None, []
    yield [role_id_0], [role_id_0]
    yield [role_id_0, role_id_1], [role_id_0, role_id_1]


@vampytest._(vampytest.call_from(_iter_options__iter_mentioned_role_ids()).returning_last())
def test__Message__iter_mentioned_role_ids(input_value):
    """
    Tests whether ``Message.iter_mentioned_role_ids`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<int>`
        Value to test with.
    
    Returns
    -------
    output : `list<int>`
    """
    message = Message(mentioned_role_ids = input_value)
    return [*message.iter_mentioned_role_ids()]


def _iter_options__iter_mentioned_roles():
    role_id_0 = 202305050028
    role_id_1 = 202305050029
    role_0 = Role.precreate(role_id_0)
    role_1 = Role.precreate(role_id_1)
    
    yield None, []
    yield [role_id_0], [role_0]
    yield [role_id_0, role_id_1], [role_0, role_1]


@vampytest._(vampytest.call_from(_iter_options__iter_mentioned_roles()).returning_last())
def test__Message__iter_mentioned_roles(input_value):
    """
    Tests whether ``Message.iter_mentioned_roles`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<int>`
        Value to test with.
    
    Returns
    -------
    output : `list<Role>`
    """
    message = Message(mentioned_role_ids = input_value)
    return [*message.iter_mentioned_roles()]


def _iter_options__iter_mentioned_users():
    user_0 = User.precreate(202305050030)
    user_1 = User.precreate(202305050031)
    
    yield None, []
    yield [user_0], [user_0]
    yield [user_0, user_1], [user_0, user_1]


@vampytest._(vampytest.call_from(_iter_options__iter_mentioned_users()).returning_last())
def test__Message__iter_mentioned_users(input_value):
    """
    Tests whether ``Message.iter_mentioned_users`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<ClientUserBase>`
        Value to test with.
    
    Returns
    -------
    output : `list<ClientUserBase>`
    """
    message = Message(mentioned_users = input_value)
    return [*message.iter_mentioned_users()]


def _iter_options__iter_stickers():
    sticker_0 = Sticker.precreate(202305050032)
    sticker_1 = Sticker.precreate(202305050033)
    
    yield None, []
    yield [sticker_0], [sticker_0]
    yield [sticker_0, sticker_1], [sticker_0, sticker_1]


@vampytest._(vampytest.call_from(_iter_options__iter_stickers()).returning_last())
def test__Message__iter_stickers(input_value):
    """
    Tests whether ``Message.iter_stickers`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<Sticker>`
        Value to test with.
    
    Returns
    -------
    output : `list<Sticker>`
    """
    message = Message(stickers = input_value)
    return [*message.iter_stickers()]


def _iter_options__has_activity():
    activity = MessageActivity(party_id = 'Remilia')
    
    yield None, False
    yield activity, True


@vampytest._(vampytest.call_from(_iter_options__has_activity()).returning_last())
def test__Message__has_activity(input_value):
    """
    Tests whether ``Message.has_activity`` works as intended.
    
    Parameters
    ----------
    input_value : `None | MessageActivity`
        Value to test with.
    
    Returns
    -------
    output : `bool`
    """
    message = Message(activity = input_value)
    output = message.has_activity()
    vampytest.assert_instance(output, bool)
    return output



def _iter_options__has_application():
    application = MessageApplication.precreate(202305050034, name = 'Flandre')
    
    yield None, False
    yield application, True


@vampytest._(vampytest.call_from(_iter_options__has_application()).returning_last())
def test__Message__has_application(input_value):
    """
    Tests whether ``Message.has_application`` works as intended.
    
    Parameters
    ----------
    input_value : `None | MessageApplication`
        Value to test with.
    
    Returns
    -------
    output : `bool`
    """
    message = Message(application = input_value)
    output = message.has_application()
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__has_application_id():
    application_id = 202305050035
    
    yield 0, False
    yield application_id, True


@vampytest._(vampytest.call_from(_iter_options__has_application_id()).returning_last())
def test__Message__has_application_id(input_value):
    """
    Tests whether ``Message.has_application_id`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Value to test with.
    
    Returns
    -------
    output : `bool`
    """
    message = Message(application_id = input_value)
    output = message.has_application_id()
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__has_attachments():
    attachments = [
        Attachment.precreate(202305050036, name = 'Koishi'),
        Attachment.precreate(202305050037, name = 'Komeiji'),
    ]
    
    yield None, False
    yield attachments, True


@vampytest._(vampytest.call_from(_iter_options__has_attachments()).returning_last())
def test__Message__has_attachments(input_value):
    """
    Tests whether ``Message.has_attachments`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<Attachment>`
        Value to test with.
    
    Returns
    -------
    output : `bool`
    """
    message = Message(attachments = input_value)
    output = message.has_attachments()
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__has_components():
    components = [
        Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Okuu')]),
        Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Parsee')]),
    ]
    
    yield None, False
    yield components, True


@vampytest._(vampytest.call_from(_iter_options__has_components()).returning_last())
def test__Message__has_components(input_value):
    """
    Tests whether ``Message.has_components`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<Component>`
        Value to test with.
    
    Returns
    -------
    output : `bool`
    """
    message = Message(components = input_value)
    output = message.has_components()
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__has_content():
    content = 'sakuya'
    
    yield None, False
    yield content, True


@vampytest._(vampytest.call_from(_iter_options__has_content()).returning_last())
def test__Message__has_content(input_value):
    """
    Tests whether ``Message.has_content`` works as intended.
    
    Parameters
    ----------
    input_value : `None | str`
        Value to test with.
    
    Returns
    -------
    output : `bool`
    """
    message = Message(content = input_value)
    output = message.has_content()
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__has_edited_at():
    edited_at = DateTime(2016, 5, 14)
    
    yield None, False
    yield edited_at, True


@vampytest._(vampytest.call_from(_iter_options__has_edited_at()).returning_last())
def test__Message__has_edited_at(input_value):
    """
    Tests whether ``Message.has_edited_at`` works as intended.
    
    Parameters
    ----------
    input_value : `None | DateTime`
        Value to test with.
    
    Returns
    -------
    output : `bool`
    """
    message = Message(edited_at = input_value)
    output = message.has_edited_at()
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__has_embeds():
    embeds = [
        Embed('Yakumo'),
        Embed('Yukari'),
    ]
    
    yield None, False
    yield embeds, True


@vampytest._(vampytest.call_from(_iter_options__has_embeds()).returning_last())
def test__Message__has_embeds(input_value):
    """
    Tests whether ``Message.has_embeds`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<Embed>`
        Value to test with.
    
    Returns
    -------
    output : `bool`
    """
    message = Message(embeds = input_value)
    output = message.has_embeds()
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__has_flags():
    flags = MessageFlag(15)
    
    yield 0, False
    yield flags, True


@vampytest._(vampytest.call_from(_iter_options__has_flags()).returning_last())
def test__Message__has_flags(input_value):
    """
    Tests whether ``Message.has_flags`` works as intended.
    
    Parameters
    ----------
    input_value : `None | int`
        Value to test with.
    
    Returns
    -------
    output : `bool`
    """
    message = Message(flags = input_value)
    output = message.has_flags()
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__has_interaction():
    interaction = MessageInteraction.precreate(202305050038, name = 'Ran')
    
    yield None, False
    yield interaction, True


@vampytest._(vampytest.call_from(_iter_options__has_interaction()).returning_last())
def test__Message__has_interaction(input_value):
    """
    Tests whether ``Message.has_interaction`` works as intended.
    
    Parameters
    ----------
    input_value : `None | MessageInteraction`
        Value to test with.
    
    Returns
    -------
    output : `bool`
    """
    message = Message(interaction = input_value)
    output = message.has_interaction()
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__has_mentioned_channels():
    channel_0 = Channel.precreate(202305050039, channel_type = ChannelType.guild_text, name = 'Chen')
    channel_1 = Channel.precreate(202404180000, channel_type = ChannelType.guild_text, name = 'Chen')
    
    yield None, None, False
    yield channel_0.mention, None, False
    yield channel_1.mention, [channel_1], True


@vampytest._(vampytest.call_from(_iter_options__has_mentioned_channels()).returning_last())
def test__Message__has_mentioned_channels(input_value, cache):
    """
    Tests whether ``Message.has_mentioned_channels`` works as intended.
    
    Parameters
    ----------
    input_value : `None | str`
        Value to test with.
    cache : `None | list<object>`
        Objects to keep in cache.
    
    Returns
    -------
    output : `bool`
    """
    message = Message(content = input_value)
    output = message.has_mentioned_channels()
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__has_mentioned_channels_cross_guild():
    mentioned_channels_cross_guild = [
        Channel.precreate(202305050041, channel_type = ChannelType.guild_text, name = 'Chen'),
        Channel.precreate(202305050042, channel_type = ChannelType.guild_text, name = 'Yuugi'),
    ]
    
    yield None, False
    yield mentioned_channels_cross_guild, True


@vampytest._(vampytest.call_from(_iter_options__has_mentioned_channels_cross_guild()).returning_last())
def test__Message__has_mentioned_channels_cross_guild(input_value):
    """
    Tests whether ``Message.has_mentioned_channels_cross_guild`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<Channel>`
        Value to test with.
    
    Returns
    -------
    output : `bool`
    """
    message = Message(mentioned_channels_cross_guild = input_value)
    output = message.has_mentioned_channels_cross_guild()
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__has_mentioned_everyone():
    yield False, False
    yield True, True


@vampytest._(vampytest.call_from(_iter_options__has_mentioned_everyone()).returning_last())
def test__Message__has_mentioned_everyone(input_value):
    """
    Tests whether ``Message.has_mentioned_everyone`` works as intended.
    
    Parameters
    ----------
    input_value : `bool`
        Value to test with.
    
    Returns
    -------
    output : `bool`
    """
    message = Message(mentioned_everyone = input_value)
    output = message.has_mentioned_everyone()
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__has_mentioned_role_ids():
    mentioned_role_ids = [202305050043, 202305050044]
    
    yield None, False
    yield mentioned_role_ids, True


@vampytest._(vampytest.call_from(_iter_options__has_mentioned_role_ids()).returning_last())
def test__Message__has_mentioned_role_ids(input_value):
    """
    Tests whether ``Message.has_mentioned_role_ids`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<int>`
        Value to test with.
    
    Returns
    -------
    output : `bool`
    """
    message = Message(mentioned_role_ids = input_value)
    output = message.has_mentioned_role_ids()
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__has_mentioned_roles():
    mentioned_role_ids = [202305050045, 202305050046]
    
    yield None, False
    yield mentioned_role_ids, True


@vampytest._(vampytest.call_from(_iter_options__has_mentioned_roles()).returning_last())
def test__Message__has_mentioned_roles(input_value):
    """
    Tests whether ``Message.has_mentioned_roles`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<int>`
        Value to test with.
    
    Returns
    -------
    output : `bool`
    """
    message = Message(mentioned_role_ids = input_value)
    output = message.has_mentioned_roles()
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__has_mentioned_users():
    mentioned_users = [
        User.precreate(202305050047, name = 'Scarlet'),
        User.precreate(202305050048, name = 'Izaoyi'),
    ]
    
    yield None, False
    yield mentioned_users, True


@vampytest._(vampytest.call_from(_iter_options__has_mentioned_users()).returning_last())
def test__Message__has_mentioned_users(input_value):
    """
    Tests whether ``Message.has_mentioned_users`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<ClientUserBase>`
        Value to test with.
    
    Returns
    -------
    output : `bool`
    """
    message = Message(mentioned_users = input_value)
    output = message.has_mentioned_users()
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__has_nonce():
    nonce = 'sakuya'
    
    yield None, False
    yield nonce, True


@vampytest._(vampytest.call_from(_iter_options__has_nonce()).returning_last())
def test__Message__has_nonce(input_value):
    """
    Tests whether ``Message.has_nonce`` works as intended.
    
    Parameters
    ----------
    input_value : `None | str`
        Value to test with.
    
    Returns
    -------
    output : `bool`
    """
    message = Message(nonce = input_value)
    output = message.has_nonce()
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__has_pinned():
    yield False, False
    yield True, True


@vampytest._(vampytest.call_from(_iter_options__has_pinned()).returning_last())
def test__Message__has_pinned(input_value):
    """
    Tests whether ``Message.has_pinned`` works as intended.
    
    Parameters
    ----------
    input_value : `bool`
        Value to test with.
    
    Returns
    -------
    output : `bool`
    """
    message = Message(pinned = input_value)
    output = message.has_pinned()
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__has_poll():
    poll = Poll(expires_at = DateTime(2016, 5, 14))
    
    yield None, False
    yield poll, True


@vampytest._(vampytest.call_from(_iter_options__has_poll()).returning_last())
def test__Message__has_poll(input_value):
    """
    Tests whether ``Message.has_poll`` works as intended.
    
    Parameters
    ----------
    input_value : `None | Poll`
        Value to test with.
    
    Returns
    -------
    output : `bool`
    """
    message = Message(poll = input_value)
    output = message.has_poll()
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__has_reactions():
    reactions = ReactionMapping({
        BUILTIN_EMOJIS['x']: [None, None],
    })
    
    yield None, False
    yield ReactionMapping(), False,
    yield reactions, True


@vampytest._(vampytest.call_from(_iter_options__has_reactions()).returning_last())
def test__Message__has_reactions(input_value):
    """
    Tests whether ``Message.has_reactions`` works as intended.
    
    Parameters
    ----------
    input_value : `None | ReactionMapping`
        Value to test with.
    
    Returns
    -------
    output : `bool`
    """
    message = Message(reactions = input_value)
    output = message.has_reactions()
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__has_referenced_message():
    referenced_message = Message.precreate(202305050049, content = 'Patchouli')
    
    yield None, False
    yield referenced_message, True


@vampytest._(vampytest.call_from(_iter_options__has_referenced_message()).returning_last())
def test__Message__has_referenced_message(input_value):
    """
    Tests whether ``Message.has_referenced_message`` works as intended.
    
    Parameters
    ----------
    input_value : `None | Message`
        Value to test with.
    
    Returns
    -------
    output : `bool`
    """
    message = Message(referenced_message = input_value)
    output = message.has_referenced_message()
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__has_role_subscription():
    role_subscription = MessageRoleSubscription(tier_name = 'Knowledge')
    
    yield None, False
    yield role_subscription, True


@vampytest._(vampytest.call_from(_iter_options__has_role_subscription()).returning_last())
def test__Message__has_role_subscription(input_value):
    """
    Tests whether ``Message.has_role_subscription`` works as intended.
    
    Parameters
    ----------
    input_value : `None | MessageRoleSubscription`
        Value to test with.
    
    Returns
    -------
    output : `bool`
    """
    message = Message(role_subscription = input_value)
    output = message.has_role_subscription()
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__has_stickers():
    stickers = [
        Sticker.precreate(202305050050, name = 'Kirisame'),
        Sticker.precreate(202305050051, name = 'Marisa'),
    ]
    
    yield None, False
    yield stickers, True


@vampytest._(vampytest.call_from(_iter_options__has_stickers()).returning_last())
def test__Message__has_stickers(input_value):
    """
    Tests whether ``Message.has_stickers`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<Sticker>`
        Value to test with.
    
    Returns
    -------
    output : `bool`
    """
    message = Message(stickers = input_value)
    output = message.has_stickers()
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__has_thread():
    thread = Channel.precreate(202305050052, channel_type = ChannelType.guild_thread_private, name = 'Yuyuko')
    
    yield None, False
    yield thread, True


@vampytest._(vampytest.call_from(_iter_options__has_thread()).returning_last())
def test__Message__has_thread(input_value):
    """
    Tests whether ``Message.has_thread`` works as intended.
    
    Parameters
    ----------
    input_value : `None | Channel`
        Value to test with.
    
    Returns
    -------
    output : `bool`
    """
    message = Message(thread = input_value)
    output = message.has_thread()
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__has_tts():
    yield False, False
    yield True, True


@vampytest._(vampytest.call_from(_iter_options__has_tts()).returning_last())
def test__Message__has_tts(input_value):
    """
    Tests whether ``Message.has_tts`` works as intended.
    
    Parameters
    ----------
    input_value : `bool`
        Value to test with.
    
    Returns
    -------
    output : `bool`
    """
    message = Message(tts = input_value)
    output = message.has_tts()
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__has_type():
    yield MessageType.default, False
    yield MessageType.call, True


@vampytest._(vampytest.call_from(_iter_options__has_type()).returning_last())
def test__Message__has_type(input_value):
    """
    Tests whether ``Message.has_type`` works as intended.
    
    Parameters
    ----------
    input_value : `MessageType`
        Value to test with.
    
    Returns
    -------
    output : `bool`
    """
    message = Message(message_type = input_value)
    output = message.has_type()
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__add_poll_vote():
    answer_id_0 = 202404200008
    user_0 = User.precreate(202404200010)
    user_1 = User.precreate(202404200011)
    
    yield (
        None,
        answer_id_0,
        user_0,
        (
            True,
            Poll(results = [PollResult(answer_id = answer_id_0, count = 1, users = [user_0])]),
        )
    )
    
    yield (
        Poll(results = [PollResult(answer_id = answer_id_0, count = 1, users = [user_1])]),
        answer_id_0,
        user_0,
        (
            True,
            Poll(results = [PollResult(answer_id = answer_id_0, count = 2, users = [user_0, user_1])]),
        )
    )
    
    yield (
        Poll(results = [PollResult(answer_id = answer_id_0, count = 1, users = [user_0])]),
        answer_id_0,
        user_0,
        (
            False,
            Poll(results = [PollResult(answer_id = answer_id_0, count = 1, users = [user_0])]),
        )
    )


@vampytest._(vampytest.call_from(_iter_options__add_poll_vote()).returning_last())
def test__Message__add_poll_vote(poll, answer_id, user):
    """
    Tests whether ``Message._add_poll_vote`` works as intended.
    
    Parameters
    ----------
    poll : `None | Poll`
        Poll to create the message with.
    answer_id : `int`
        The answer's identifier.
    user : ``ClientUserBase``
        The user who added their vote.
    
    Returns
    -------
    output : `(int, None | Poll)`
    """
    if (poll is not None):
        poll.copy()
    
    message = Message(poll = poll)
    output = message._add_poll_vote(answer_id, user)
    vampytest.assert_instance(output, bool)
    return output, message.poll


def _iter_options__remove_poll_vote():
    answer_id_0 = 2024042000012
    user_0 = User.precreate(202404200014)
    user_1 = User.precreate(202404200015)
    
    yield (
        None,
        answer_id_0,
        user_0,
        (
            False,
            None,
        )
    )
    
    yield (
        Poll(results = [PollResult(answer_id = answer_id_0, count = 1, users = [user_1])]),
        answer_id_0,
        user_0,
        (
            False,
            Poll(results = [PollResult(answer_id = answer_id_0, count = 1, users = [user_1])]),
        )
    )
    
    yield (
        Poll(results = [PollResult(answer_id = answer_id_0, count = 2, users = [user_0, user_1])]),
        answer_id_0,
        user_0,
        (
            True,
            Poll(results = [PollResult(answer_id = answer_id_0, count = 1, users = [user_1])]),
        )
    )
    
    yield (
        Poll(results = [PollResult(answer_id = answer_id_0, count = 1, users = [user_0])]),
        answer_id_0,
        user_0,
        (
            True,
            Poll(results = [PollResult(answer_id = answer_id_0, count = 0, users = [])]),
        )
    )


@vampytest._(vampytest.call_from(_iter_options__remove_poll_vote()).returning_last())
def test__Message__remove_poll_vote(poll, answer_id, user):
    """
    Tests whether ``Message._remove_poll_vote`` works as intended.
    
    Parameters
    ----------
    poll : `None | Poll`
        Poll to create the message with.
    answer_id : `int`
        The answer's identifier.
    user : ``ClientUserBase``
        The user who removed their vote.
    
    Returns
    -------
    output : `(int, None | Poll)`
    """
    if (poll is not None):
        poll.copy()
    
    message = Message(poll = poll)
    output = message._remove_poll_vote(answer_id, user)
    vampytest.assert_instance(output, bool)
    return output, message.poll


def _iter_options__did_vote():
    answer_id_0 = 2024042000016
    answer_id_1 = 202404200017
    user_0 = User.precreate(202404200018)
    user_1 = User.precreate(202404200019)
    
    yield (
        None,
        PollAnswer.precreate(answer_id_0),
        user_0,
        False,
    )
    
    yield (
        Poll(results = [PollResult(answer_id = answer_id_0, count = 1, users = [user_1])]),
        PollAnswer.precreate(answer_id_0),
        user_0,
        False,
    )
    
    yield (
        Poll(results = [PollResult(answer_id = answer_id_0, count = 2, users = [user_0, user_1])]),
        PollAnswer.precreate(answer_id_0),
        user_0,
        True,
    )
    
    yield (
        Poll(results = [PollResult(answer_id = answer_id_0, count = 1, users = [user_0])]),
        PollAnswer.precreate(answer_id_0),
        user_0,
        True
    )
    
    yield (
        Poll(
            answers = [
                PollAnswer.precreate(answer_id_0, text = 'mister'),
                PollAnswer.precreate(answer_id_1, text = 'sister'),
            ],
            results = [
                PollResult(answer_id = answer_id_0, count = 1, users = [user_0]),
                PollResult(answer_id = answer_id_1, count = 1, users = [user_0]),
            ],
        ),
        PollAnswer(text = 'mister'),
        user_0,
        True
    )


@vampytest._(vampytest.call_from(_iter_options__did_vote()).returning_last())
def test__Message__did_vote(poll, answer, user):
    """
    Tests whether ``Message.did_vote`` works as intended.
    
    Parameters
    ----------
    poll : `None | Poll`
        Poll to create the message with.
    answer : ``PollAnswer``
        The answer to check for.
    user : ``ClientUserBase``
        The user to check.
    
    Returns
    -------
    output : `bool`
    """
    if (poll is not None):
        poll.copy()
    
    message = Message(poll = poll)
    output = message.did_vote(answer, user)
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__has_any_content_field():
    # non-rich types automatically count as they have content.
    yield {'message_type': MessageType.call}, True
    
    yield {}, False
    
    yield {'activity': MessageActivity(party_id = 'Remilia')}, False
    yield {'application': MessageApplication.precreate(202404200022, name = 'Flandre')}, False
    yield {'application_id': 202404200023}, False
    yield (
        {
            'attachments': [
                Attachment.precreate(202404200024, name = 'Koishi'),
            ],
        },
        True,
    )
    yield {'author': User.precreate(202404200025, name = 'Orin')}, False
    yield {'call': MessageCall(ended_at = DateTime(2045, 3, 4))}, False
    yield (
        {
            'components': [
                Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Okuu')])
            ]
        },
        True,
    )
    yield {'content': 'Satori'}, True
    yield {'edited_at': DateTime(2016, 5, 14)}, False
    yield {'embeds': [Embed('Yakumo')]}, True
    yield {'flags': MessageFlag(15)}, False
    yield {'interaction': MessageInteraction.precreate(202404200026, name = 'Ran')}, False
    yield (
        {
            'mentioned_channels_cross_guild': [
                Channel.precreate(202404200027, channel_type = ChannelType.guild_text, name = 'Chen'),
            ],
        },
        False,
    )
    yield {'mentioned_everyone': True}, False
    yield {'mentioned_role_ids': [202404200028]}, False
    yield (
        {
            'mentioned_users': [
                User.precreate(202404200029, name = 'Scarlet'),
            ],
        },
        False,
    )
    yield {'message_type': MessageType.default}, False
    yield {'nonce': 'Sakuya'}, False
    yield {'pinned': True}, False
    yield {'poll': Poll(expires_at = DateTime(2016, 5, 14))}, True
    yield {'reactions': ReactionMapping({BUILTIN_EMOJIS['x']: [None, None]})}, False
    yield {'referenced_message': Message.precreate(202404200030, content = 'Patchouli')}, False
    yield {'resolved': Resolved(attachments = [Attachment.precreate(202404200031)])}, False
    yield {'role_subscription': MessageRoleSubscription(tier_name = 'Knowledge')}, False
    yield (
        {
            'stickers': [
                Sticker.precreate(202404200032, name = 'Kirisame'),
            ]
        },
        False,
    )
    yield (
        {'thread': Channel.precreate(202404200033, channel_type = ChannelType.guild_thread_private, name = 'Yuyuko')},
        False,
    )
    yield {'tts': True}, False


@vampytest._(vampytest.call_from(_iter_options__has_any_content_field()).returning_last())
def test__Message__has_any_content_field(keyword_parameters):
    """
    Tests whether ``Message.has_any_content_field`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the message with.
    
    Returns
    -------
    output : `bool`
    """
    message = Message(**keyword_parameters)
    output = message.has_any_content_field()
    vampytest.assert_instance(output, bool)
    return output
