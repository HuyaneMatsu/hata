from datetime import datetime as DateTime

import vampytest

from ....channel import Channel, ChannelType, create_partial_channel_data
from ....component import Component, ComponentType
from ....core import BUILTIN_EMOJIS
from ....embed import Embed
from ....emoji import Reaction, ReactionMapping, ReactionMappingLine, ReactionType
from ....interaction import Resolved
from ....poll import Poll
from ....sticker import Sticker, create_partial_sticker_data
from ....user import User
from ....utils import datetime_to_timestamp

from ...attachment import Attachment
from ...message_activity import MessageActivity
from ...message_application import MessageApplication
from ...message_call import MessageCall
from ...message_interaction import MessageInteraction
from ...message_role_subscription import MessageRoleSubscription
from ...message_snapshot import MessageSnapshot
from ...poll_change import PollChange
from ...poll_update import PollUpdate

from ..flags import MessageFlag
from ..message import Message
from ..preinstanced import MessageType

from .test__Message__contructor import _assert_fields_set


def test__Message__from_data__all_fields():
    """
    Tests whether ``from_data`` works as intended.
    
    Case: All fields given.
    """
    activity = MessageActivity(party_id = 'Remilia')
    application = MessageApplication.precreate(202305030039, name = 'Flandre')
    application_id = 202305030040
    attachments = [
        Attachment.precreate(202305030041, name = 'Koishi'),
        Attachment.precreate(202305030042, name = 'Komeiji'),
    ]
    author = User.precreate(202305030043, name = 'Orin')
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
    interaction = MessageInteraction.precreate(202305030044, name = 'Ran')
    mentioned_channels_cross_guild = [
        Channel.precreate(202305030045, channel_type = ChannelType.guild_text, name = 'Chen'),
        Channel.precreate(202305030046, channel_type = ChannelType.guild_text, name = 'Yuugi'),
    ]
    mentioned_everyone = True
    mentioned_role_ids = [202305030047, 202305030048]
    mentioned_users = [
        User.precreate(202305030049, name = 'Scarlet'),
        User.precreate(202305030050, name = 'Izaoyi'),
    ]
    message_type = MessageType.call
    nonce = 'Sakuya'
    pinned = True
    poll = Poll(expires_at = DateTime(2016, 5, 14))
    reactions = ReactionMapping(
        lines = {
            Reaction.from_fields(BUILTIN_EMOJIS['x'], ReactionType.standard): ReactionMappingLine(count = 2),
        },
    )
    referenced_message = Message.precreate(202305030051, content = 'Patchouli')
    resolved = Resolved(attachments = [Attachment.precreate(202310110008)])
    role_subscription = MessageRoleSubscription(tier_name = 'Knowledge')
    snapshots = [
        MessageSnapshot(content = 'Kazami'),
        MessageSnapshot(content = 'Yuuka'),
    ]
    stickers = [
        Sticker.precreate(202305030052, name = 'Kirisame'),
        Sticker.precreate(202305030053, name = 'Marisa'),
    ]
    thread = Channel.precreate(202305030054, channel_type = ChannelType.guild_thread_private, name = 'Yuyuko')
    tts = True
    
    message_id = 202305030055
    channel_id = 202305030056
    guild_id = 202305030057
    
    input_data = {
        'author': author.to_data(include_internals = True),
        'channel_id': str(channel_id),
        'guild_id': str(guild_id),
        'id': str(message_id),
        'type': message_type.value,
        
        'activity': activity.to_data(),
        'application': application.to_data(include_internals = True),
        'application_id': str(application_id),
        'call': call.to_data(),
        'edited_timestamp': datetime_to_timestamp(edited_at),
        'interaction_metadata': interaction.to_data(include_internals = True),
        'mention_channels': [create_partial_channel_data(channel) for channel in mentioned_channels_cross_guild],
        'mention_everyone': mentioned_everyone,
        'mention_roles': [str(role_id) for role_id in mentioned_role_ids],
        'mentions': [user.to_data(include_internals = True) for user in mentioned_users],
        'pinned': pinned,
        'poll': poll.to_data(include_internals = True),
        'reactions': reactions.to_data(),
        'referenced_message': referenced_message.to_data(include_internals = True, recursive = False),
        'message_reference': referenced_message.to_message_reference_data(),
        'resolved': resolved.to_data(),
        'role_subscription_data': role_subscription.to_data(),
        'message_snapshots': [snapshot.to_data() for snapshot in snapshots],
        'sticker_items': [create_partial_sticker_data(sticker) for sticker in stickers],
        'thread': thread.to_data(include_internals = True),
        
        'attachments': [attachment.to_data(include_internals = True) for attachment in attachments],
        'components': [component.to_data() for component in components],
        'content': content,
        'embeds': [embed.to_data() for embed in embeds],
        'flags': int(flags),
        'nonce': nonce,
        'tts': tts,
    }
    
    message = Message.from_data(input_data)
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
    vampytest.assert_eq(message.snapshots, tuple(snapshots))
    vampytest.assert_eq(message.stickers, tuple(stickers))
    vampytest.assert_eq(message.thread, thread)
    vampytest.assert_eq(message.tts, tts)
    vampytest.assert_is(message.type, message_type)

    vampytest.assert_eq(message.id, message_id)
    vampytest.assert_eq(message.channel_id, channel_id)
    vampytest.assert_eq(message.guild_id, guild_id)


def test__Message__from_data__caching():
    """
    Tests whether ``from_data`` works as intended.
    
    Case: Caching.
    """
    message_id = 202305030058
    
    input_data = {
        'id': str(message_id),
    }
    
    message = Message.from_data(input_data)
    test_message = Message.from_data(input_data)
    
    vampytest.assert_is(message, test_message)


def test__Message__from_data__should_not_update_if_updated():
    """
    Tests whether ``from_data`` works as intended.
    
    Case: Should not update if already up to date.
    """
    call = MessageCall(ended_at = DateTime(2045, 3, 4))
    message_id = 202305030059
    
    input_data = {
        'id': str(message_id),
    }
    
    message = Message.from_data(input_data)
    
    input_data = {
        'id': str(message_id),
        'call': call.to_data(),
    }
    
    Message.from_data(input_data)
    vampytest.assert_is(message.call, None)


def test__Message__from_data__should_update_if_precreate():
    """
    Tests whether ``from_data`` works as intended.
    
    Case: Should update if precreated
    """
    call = MessageCall(ended_at = DateTime(2045, 3, 4))
    message_id = 202305030060
    
    message = Message.precreate(message_id)
    
    input_data = {
        'id': str(message_id),
        'call': call.to_data(),
    }
    
    Message.from_data(input_data)
    
    vampytest.assert_eq(message.call, call)


def test__Message__to_data():
    """
    Tests whether ``to_data`` works as intended.
    
    Case: All fields given.
    """
    activity = MessageActivity(party_id = 'Remilia')
    application = MessageApplication.precreate(202310110010, name = 'Flandre')
    application_id = 202310110011
    attachments = [
        Attachment.precreate(202310110012, name = 'Koishi'),
        Attachment.precreate(202310110013, name = 'Komeiji'),
    ]
    author = User.precreate(202310110014, name = 'Orin')
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
    interaction = MessageInteraction.precreate(202310110015, name = 'Ran')
    mentioned_channels_cross_guild = [
        Channel.precreate(202310110016, channel_type = ChannelType.guild_text, name = 'Chen'),
        Channel.precreate(202310110017, channel_type = ChannelType.guild_text, name = 'Yuugi'),
    ]
    mentioned_everyone = True
    mentioned_role_ids = [202310110018, 202310110019]
    mentioned_users = [
        User.precreate(202310110020, name = 'Scarlet'),
        User.precreate(202310110021, name = 'Izaoyi'),
    ]
    message_type = MessageType.inline_reply
    nonce = 'Sakuya'
    pinned = True
    poll = Poll(expires_at = DateTime(2016, 5, 14))
    reactions = ReactionMapping(
        lines = {
            Reaction.from_fields(BUILTIN_EMOJIS['x'], ReactionType.standard): ReactionMappingLine(count = 2),
        },
    )
    referenced_message = Message.precreate(202310110022, content = 'Patchouli')
    resolved = Resolved(attachments = [Attachment.precreate(202310110023)])
    role_subscription = MessageRoleSubscription(tier_name = 'Knowledge')
    snapshots = [
        MessageSnapshot(content = 'Kazami'),
        MessageSnapshot(content = 'Yuuka'),
    ]
    stickers = [
        Sticker.precreate(202310110024, name = 'Kirisame'),
        Sticker.precreate(202310110025, name = 'Marisa'),
    ]
    thread = Channel.precreate(202310110026, channel_type = ChannelType.guild_thread_private, name = 'Yuyuko')
    tts = True
    
    message_id = 202310110027
    channel_id = 202310110028
    guild_id = 202310110029
    
    expected_output = {
        'guild_id': str(guild_id),
        'id': str(message_id),
        
        'activity': activity.to_data(defaults = True),
        'attachments': [attachment.to_data(defaults = True, include_internals = True) for attachment in attachments],
        'application': application.to_data(defaults = True, include_internals = True),
        'application_id': str(application_id),
        'webhook_id': str(application_id),
        'author': author.to_data(defaults = True, include_internals = True),
        'call': call.to_data(defaults = True),
        'channel_id': str(channel_id),
        'edited_timestamp': datetime_to_timestamp(edited_at),
        'interaction_metadata': interaction.to_data(defaults = True, include_internals = True),
        'mention_channels': [create_partial_channel_data(channel) for channel in mentioned_channels_cross_guild],
        'mention_everyone': mentioned_everyone,
        'mention_roles': [str(role_id) for role_id in mentioned_role_ids],
        'mentions': [user.to_data(defaults = True, include_internals = True) for user in mentioned_users],
        'pinned': pinned,
        'poll': poll.to_data(defaults = True, include_internals = True),
        'reactions': reactions.to_data(),
        'referenced_message': referenced_message.to_data(defaults = True, include_internals = True, recursive = False),
        'message_reference': referenced_message.to_message_reference_data(),
        'resolved': resolved.to_data(defaults = True),
        'role_subscription_data': role_subscription.to_data(defaults = True),
        'message_snapshots': [snapshots.to_data(defaults = True) for snapshots in snapshots],
        'sticker_items': [create_partial_sticker_data(sticker) for sticker in stickers],
        'thread': thread.to_data(defaults = True, include_internals = True),
        'type': message_type.value,
        
        'components': [component.to_data(defaults = True) for component in components],
        'content': content,
        'embeds': [embed.to_data(defaults = True, include_internals = True) for embed in embeds],
        'flags': int(flags),
        'nonce': nonce,
        'tts': tts,
    }
    
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
        snapshots = snapshots,
        stickers = stickers,
        thread = thread,
        tts = tts,
    )
    
    vampytest.assert_eq(
        message.to_data(defaults = True, include_internals = True, recursive = True),
        expected_output,
    )


def test__Message__create_message_was_up_to_date__new():
    """
    Tests whether ``Message._create_message_was_up_to_date`` works as intended.
    
    Case: New.
    """
    call = MessageCall(ended_at = DateTime(2045, 3, 4))
    message_id = 202305030061
    
    input_data = {
        'id': str(message_id),
        'call': call.to_data(),
    }
    
    message, was_up_to_date = Message._create_message_was_up_to_date(input_data)
    _assert_fields_set(message)
    vampytest.assert_instance(was_up_to_date, bool)
    
    vampytest.assert_eq(message.call, call)
    vampytest.assert_false(was_up_to_date)


def test__Message__create_message_was_up_to_date__in_cache_require_update():
    """
    Tests whether ``Message._create_message_was_up_to_date`` works as intended.
    
    Case: In cache, needs update.
    """
    call = MessageCall(ended_at = DateTime(2045, 3, 4))
    message_id = 202305030062
    
    message = Message.precreate(message_id)
    
    input_data = {
        'id': str(message_id),
        'call': call.to_data(),
    }
    
    message, was_up_to_date = Message._create_message_was_up_to_date(input_data)
    _assert_fields_set(message)
    vampytest.assert_instance(was_up_to_date, bool)
    
    vampytest.assert_eq(message.call, call)
    vampytest.assert_false(was_up_to_date)


def test__Message__create_message_was_up_to_date__in_cache_up_to_date():
    """
    Tests whether ``Message._create_message_was_up_to_date`` works as intended.
    
    Case: In cache, up to date.
    """
    call = MessageCall(ended_at = DateTime(2045, 3, 4))
    message_id = 202305030063
    
    input_data = {
        'id': str(message_id),
    }
    
    message = Message.from_data(input_data)
    
    input_data = {
        'id': str(message_id),
        'call': call.to_data(),
    }
    
    _, was_up_to_date = Message._create_message_was_up_to_date(input_data)
    _assert_fields_set(message)
    vampytest.assert_instance(was_up_to_date, bool)
    
    vampytest.assert_is(message.call, None)
    vampytest.assert_true(was_up_to_date)


def test__Message__create_from_partial_data__with_message_id_key():
    """
    Tests whether ``Message._create_from_partial_data`` works as intended.
    
    Case: with key `message_id`.
    """
    message_id = 202305030064
    channel_id = 202305030065
    guild_id = 202305030066
    
    input_data = {
        'message_id': str(message_id),
        'channel_id': str(channel_id),
        'guild_id': str(guild_id),
    }
    
    message = Message._create_from_partial_data(input_data)
    _assert_fields_set(message)
    
    vampytest.assert_eq(message.id, message_id)
    vampytest.assert_eq(message.channel_id, channel_id)
    vampytest.assert_eq(message.guild_id, guild_id)
    
    test_message = Message._create_from_partial_data(input_data)
    vampytest.assert_is(message, test_message)


def test__Message__create_from_partial_data__with_id_key():
    """
    Tests whether ``Message._create_from_partial_data`` works as intended.
    
    Case: with key `id`.
    """
    message_id = 202305030067
    channel_id = 202305030068
    guild_id = 202305030069
    
    input_data = {
        'id': str(message_id),
        'channel_id': str(channel_id),
        'guild_id': str(guild_id),
    }
    
    message = Message._create_from_partial_data(input_data)
    _assert_fields_set(message)
    
    vampytest.assert_eq(message.id, message_id)
    vampytest.assert_eq(message.channel_id, channel_id)
    vampytest.assert_eq(message.guild_id, guild_id)
    
    test_message = Message._create_from_partial_data(input_data)
    vampytest.assert_is(message, test_message)


def test__Message__create_from_partial_data__without_id_key():
    """
    Tests whether ``Message._create_from_partial_data`` works as intended.
    
    Case: without id key.
    """
    channel_id = 202305030070
    guild_id = 202305030071
    
    input_data = {
        'channel_id': str(channel_id),
        'guild_id': str(guild_id),
    }
    
    message = Message._create_from_partial_data(input_data)
    _assert_fields_set(message)
    
    vampytest.assert_eq(message.channel_id, channel_id)
    vampytest.assert_eq(message.guild_id, guild_id)
    
    test_message = Message._create_from_partial_data(input_data)
    vampytest.assert_is_not(message, test_message)


def test__Message__create_from_partial_fields():
    """
    Tests whether ``Message._create_from_partial_fields`` works as intended.
    """
    message_id = 202305030072
    channel_id = 202305030073
    guild_id = 202305030074
    
    message = Message._create_from_partial_fields(message_id, channel_id, guild_id)
    
    vampytest.assert_eq(message.id, message_id)
    vampytest.assert_eq(message.channel_id, channel_id)
    vampytest.assert_eq(message.guild_id, guild_id)
    
    test_message = Message._create_from_partial_fields(message_id, channel_id, guild_id)
    vampytest.assert_is(message, test_message)


def test__Message__set_attributes__guild_id():
    """
    Checks whether ``Message._set_attributes`` sets `.guild_id` from its channel's if not present in the data.
    """
    message_id = 202305030075
    channel_id = 202305030076
    guild_id = 202305030077
    
    message = Message.precreate(message_id)
    
    channel = Channel.precreate(channel_id, guild_id = guild_id)
    
    input_data = {
        'channel_id': str(channel_id),
        'guild_id': None,
    }
    
    message._set_attributes(input_data)
    
    vampytest.assert_eq(message.guild_id, guild_id)


def test__Message__set_attributes__caching():
    """
    Tests whether ``Message._set_attributes`` works as intended.
    
    Case: caching.
    """
    channel_id_0 = 202305030119
    channel_id_1 = 202305030120
    
    channel_0 = Channel.precreate(channel_id_0)
    channel_1 = Channel.precreate(channel_id_1)
    
    old_content = channel_0.mention
    new_content = channel_1.mention
    
    message = Message(content = old_content)
    old_mentioned_channels = message.mentioned_channels
    
    input_data = {
        'content': new_content,
    }
    
    message._set_attributes(input_data)
    new_mentioned_channels = message.mentioned_channels
    
    vampytest.assert_ne(old_mentioned_channels, new_mentioned_channels)


def test__message__late_init__loading():
    """
    Tests whether ``Message._late_init`` works as intended.
    
    Case: flags -> Loading.
    """
    call = MessageCall(ended_at = DateTime(2045, 3, 4))
    message_id = 202305030078
    
    message = Message.precreate(message_id, flags = MessageFlag().update_by_keys(loading = True))

    input_data = {
        'id': str(message_id),
        'call': call.to_data(),
    }
    
    message._late_init(input_data)
    
    vampytest.assert_eq(message.call, call)


def test__message__late_init__not_loading_but_receiving_interaction():
    """
    Tests whether ``Message._late_init`` works as intended.
    
    Case: flags -> not Loading & interaction received.
    """
    interaction = MessageInteraction.precreate(202305030081, name = 'Koishi')
    call = MessageCall(ended_at = DateTime(2045, 3, 4))
    message_id = 202305030082
    
    message = Message.precreate(message_id, flags = MessageFlag().update_by_keys(loading = False))

    input_data = {
        'id': str(message_id),
        'call': call.to_data(),
        'interaction_metadata': interaction.to_data(include_internals = True),
    }
    
    message._late_init(input_data)
    
    vampytest.assert_is(message.call, None)
    vampytest.assert_eq(message.interaction, interaction)


def test__Message__difference_update_attributes():
    """
    Tests whether ``Message._difference_update_attributes`` works as intended.
    
    Case: update.
    """
    old_attachments = [
        Attachment.precreate(202305030083, name = 'Koishi'),
        Attachment.precreate(202305030084, name = 'Komeiji'),
    ]
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
    old_mentioned_channels_cross_guild = [
        Channel.precreate(202305030085, channel_type = ChannelType.guild_text, name = 'Chen'),
        Channel.precreate(202305030086, channel_type = ChannelType.guild_text, name = 'Yuugi'),
    ]
    old_mentioned_everyone = True
    old_mentioned_role_ids = [202305030130, 202305030131]
    old_mentioned_users = [
        User.precreate(202305030087, name = 'Scarlet'),
        User.precreate(202305030088, name = 'Izaoyi'),
    ]
    old_pinned = True
    old_poll = Poll(expires_at = DateTime(2016, 5, 14))
    old_resolved = Resolved(attachments = [Attachment.precreate(202310140050)])
    
    new_attachments = [
        Attachment.precreate(202305030089, name = 'Yuuka'),
        Attachment.precreate(202305030090, name = 'Yuugi'),
    ]
    new_call = MessageCall(ended_at = DateTime(2045, 4, 4))
    new_components = [
        Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Chiruno')]),
        Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Dai')]),
    ]
    new_content = 'Mokou'
    new_edited_at = DateTime(2016, 10, 28)
    new_embeds = [
        Embed('Kokoro'),
        Embed('Keine'),
    ]
    new_flags = MessageFlag(16)
    new_mentioned_channels_cross_guild = [
        Channel.precreate(202305030091, channel_type = ChannelType.guild_text, name = 'Tewi'),
        Channel.precreate(202305030092, channel_type = ChannelType.guild_text, name = 'Reisen'),
    ]
    new_mentioned_everyone = False
    new_mentioned_role_ids = [202305030093, 202305030094]
    new_mentioned_users = [
        User.precreate(202305030095, name = 'Hecatia'),
        User.precreate(202305030096, name = 'Lapislazuli'),
    ]
    new_pinned = False
    new_poll = Poll(expires_at = DateTime(2016, 5, 15))
    new_resolved = Resolved(attachments = [Attachment.precreate(202310140051)])
    
    
    message_id = 202305030097
    
    message = Message.precreate(
        message_id,
        attachments = old_attachments,
        call = old_call,
        components = old_components,
        content = old_content,
        edited_at = old_edited_at,
        embeds = old_embeds,
        flags = old_flags,
        mentioned_channels_cross_guild = old_mentioned_channels_cross_guild,
        mentioned_everyone = old_mentioned_everyone,
        mentioned_role_ids = old_mentioned_role_ids,
        mentioned_users = old_mentioned_users,
        pinned = old_pinned,
        poll = old_poll,
        resolved = old_resolved,
    )
    
    input_data = {
        'attachments': [attachment.to_data(include_internals = True) for attachment in new_attachments],
        'call': new_call.to_data(),
        'components': [component.to_data() for component in new_components],
        'content': new_content,
        'edited_timestamp': datetime_to_timestamp(new_edited_at),
        'embeds': [embed.to_data() for embed in new_embeds],
        'flags': int(new_flags),
        'pinned': new_pinned,
        'poll': new_poll.to_data(include_internals = True),
        'mention_channels': [create_partial_channel_data(channel) for channel in new_mentioned_channels_cross_guild],
        'mention_everyone': new_mentioned_everyone,
        'mention_roles': [str(role_id) for role_id in new_mentioned_role_ids],
        'mentions': [user.to_data(include_internals = True) for user in new_mentioned_users],
        'resolved': new_resolved.to_data(),
    }
    
    old_attributes = message._difference_update_attributes(input_data)

    vampytest.assert_eq(message.attachments, tuple(new_attachments))
    vampytest.assert_eq(message.call, new_call)
    vampytest.assert_eq(message.components, tuple(new_components))
    vampytest.assert_eq(message.content, new_content)
    vampytest.assert_eq(message.edited_at, new_edited_at)
    vampytest.assert_eq(message.embeds, tuple(new_embeds))
    vampytest.assert_eq(message.flags, new_flags)
    vampytest.assert_eq(message.mentioned_channels_cross_guild, tuple(new_mentioned_channels_cross_guild))
    vampytest.assert_eq(message.mentioned_everyone, new_mentioned_everyone)
    vampytest.assert_eq(message.mentioned_role_ids, tuple(new_mentioned_role_ids))
    vampytest.assert_eq(message.mentioned_users, tuple(new_mentioned_users))
    vampytest.assert_eq(message.pinned, new_pinned)
    vampytest.assert_eq(message.poll, new_poll)
    vampytest.assert_eq(message.resolved, new_resolved)
    
    expected_output = {
        'attachments': tuple(old_attachments),
        'call': old_call,
        'components': tuple(old_components),
        'content': old_content,
        'edited_at': old_edited_at,
        'embeds': tuple(old_embeds),
        'flags': old_flags,
        'mentioned_channels_cross_guild': tuple(old_mentioned_channels_cross_guild),
        'mentioned_everyone': old_mentioned_everyone,
        'mentioned_role_ids': tuple(old_mentioned_role_ids),
        'mentioned_users': tuple(old_mentioned_users),
        'pinned': old_pinned,
        'poll': PollChange.from_fields(None, PollUpdate.from_fields(new_poll, {'expires_at': DateTime(2016, 5, 14)}), None),
        'resolved': old_resolved,
    }
    
    vampytest.assert_eq(old_attributes, expected_output)


def test__Message__difference_update_attributes__caching():
    """
    Tests whether ``Message._difference_update_attributes`` works as intended.
    
    Case: caching.
    """
    channel_id_0 = 202305030115
    channel_id_1 = 202305030116
    
    channel_0 = Channel.precreate(channel_id_0)
    channel_1 = Channel.precreate(channel_id_1)
    
    old_content = channel_0.mention
    new_content = channel_1.mention
    
    message = Message(content = old_content)
    old_mentioned_channels = message.mentioned_channels
    
    input_data = {
        'content': new_content,
    }
    
    message._difference_update_attributes(input_data)
    new_mentioned_channels = message.mentioned_channels
    
    vampytest.assert_ne(old_mentioned_channels, new_mentioned_channels)


def test__Message__update_attributes():
    """
    Tests whether ``Message._update_attributes`` works as intended.
    
    Case: update.
    """
    old_attachments = [
        Attachment.precreate(202305030098, name = 'Koishi'),
        Attachment.precreate(202305030099, name = 'Komeiji'),
    ]
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
    old_mentioned_channels_cross_guild = [
        Channel.precreate(202305030100, channel_type = ChannelType.guild_text, name = 'Chen'),
        Channel.precreate(202305030101, channel_type = ChannelType.guild_text, name = 'Yuugi'),
    ]
    old_mentioned_everyone = True
    old_mentioned_role_ids = [202305030102, 202305030103]
    old_mentioned_users = [
        User.precreate(202305030104, name = 'Scarlet'),
        User.precreate(202305030105, name = 'Izaoyi'),
    ]
    old_pinned = True
    old_poll = Poll(expires_at = DateTime(2016, 5, 14))
    old_resolved = Resolved(attachments = [Attachment.precreate(202310140052)])
    
    new_attachments = [
        Attachment.precreate(202305030106, name = 'Yuuka'),
        Attachment.precreate(202305030107, name = 'Yuugi'),
    ]
    new_call = MessageCall(ended_at = DateTime(2045, 4, 4))
    new_components = [
        Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Chiruno')]),
        Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Dai')]),
    ]
    new_content = 'Mokou'
    new_edited_at = DateTime(2016, 10, 28)
    new_embeds = [
        Embed('Kokoro'),
        Embed('Keine'),
    ]
    new_flags = MessageFlag(16)
    new_mentioned_channels_cross_guild = [
        Channel.precreate(202305030108, channel_type = ChannelType.guild_text, name = 'Tewi'),
        Channel.precreate(202305030109, channel_type = ChannelType.guild_text, name = 'Reisen'),
    ]
    new_mentioned_everyone = False
    new_mentioned_role_ids = [202305030110, 202305030111]
    new_mentioned_users = [
        User.precreate(202305030112, name = 'Hecatia'),
        User.precreate(202305030113, name = 'Lapislazuli'),
    ]
    new_pinned = False
    new_poll = Poll(expires_at = DateTime(2016, 5, 15))
    new_resolved = Resolved(attachments = [Attachment.precreate(202310140053)])
    
    
    message_id = 202305030114
    
    message = Message.precreate(
        message_id,
        attachments = old_attachments,
        call = old_call,
        components = old_components,
        content = old_content,
        edited_at = old_edited_at,
        embeds = old_embeds,
        flags = old_flags,
        mentioned_channels_cross_guild = old_mentioned_channels_cross_guild,
        mentioned_everyone = old_mentioned_everyone,
        mentioned_role_ids = old_mentioned_role_ids,
        mentioned_users = old_mentioned_users,
        pinned = old_pinned,
        poll = old_poll,
        resolved = old_resolved,
    )
    
    input_data = {
        'attachments': [attachment.to_data(include_internals = True) for attachment in new_attachments],
        'call': new_call.to_data(),
        'components': [component.to_data() for component in new_components],
        'content': new_content,
        'edited_timestamp': datetime_to_timestamp(new_edited_at),
        'embeds': [embed.to_data() for embed in new_embeds],
        'flags': int(new_flags),
        'pinned': new_pinned,
        'poll': new_poll.to_data(include_internals = True),
        'mention_channels': [create_partial_channel_data(channel) for channel in new_mentioned_channels_cross_guild],
        'mention_everyone': new_mentioned_everyone,
        'mention_roles': [str(role_id) for role_id in new_mentioned_role_ids],
        'mentions': [user.to_data(include_internals = True) for user in new_mentioned_users],
        'resolved': new_resolved.to_data(),
    }
    
    message._update_attributes(input_data)

    vampytest.assert_eq(message.attachments, tuple(new_attachments))
    vampytest.assert_eq(message.call, new_call)
    vampytest.assert_eq(message.components, tuple(new_components))
    vampytest.assert_eq(message.content, new_content)
    vampytest.assert_eq(message.edited_at, new_edited_at)
    vampytest.assert_eq(message.embeds, tuple(new_embeds))
    vampytest.assert_eq(message.flags, new_flags)
    vampytest.assert_eq(message.mentioned_channels_cross_guild, tuple(new_mentioned_channels_cross_guild))
    vampytest.assert_eq(message.mentioned_everyone, new_mentioned_everyone)
    vampytest.assert_eq(message.mentioned_role_ids, tuple(new_mentioned_role_ids))
    vampytest.assert_eq(message.mentioned_users, tuple(new_mentioned_users))
    vampytest.assert_eq(message.pinned, new_pinned)
    vampytest.assert_eq(message.poll, new_poll)
    vampytest.assert_eq(message.resolved, new_resolved)
    

def test__Message__update_attributes__caching():
    """
    Tests whether ``Message._update_attributes`` works as intended.
    
    Case: caching.
    """
    channel_id_0 = 202305030117
    channel_id_1 = 202305030118
    
    channel_0 = Channel.precreate(channel_id_0)
    channel_1 = Channel.precreate(channel_id_1)
    
    old_content = channel_0.mention
    new_content = channel_1.mention
    
    message = Message(content = old_content)
    old_mentioned_channels = message.mentioned_channels
    
    input_data = {
        'content': new_content,
    }
    
    message._update_attributes(input_data)
    new_mentioned_channels = message.mentioned_channels
    
    vampytest.assert_ne(old_mentioned_channels, new_mentioned_channels)


def test__Message__update_content_fields():
    """
    Tests whether ``Message._update_content_fields`` works as intended.
    
    Case: update.
    """
    old_attachments = [
        Attachment.precreate(202305030121, name = 'Koishi'),
        Attachment.precreate(202305030122, name = 'Komeiji'),
    ]
    old_components = [
        Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Okuu')]),
        Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Parsee')]),
    ]
    old_content = 'Satori'
    old_embeds = [
        Embed('Yakumo'),
        Embed('Yukari'),
    ]
    old_poll = Poll(expires_at = DateTime(2016, 5, 14))
    
    new_attachments = [
        Attachment.precreate(202305030123, name = 'Yuuka'),
        Attachment.precreate(202305030124, name = 'Yuugi'),
    ]
    new_components = [
        Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Chiruno')]),
        Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Dai')]),
    ]
    new_content = 'Mokou'
    new_embeds = [
        Embed('Kokoro'),
        Embed('Keine'),
    ]
    new_poll = Poll(expires_at = DateTime(2016, 5, 15))
    
    
    message_id = 202305030125
    
    message = Message.precreate(
        message_id,
        attachments = old_attachments,
        components = old_components,
        content = old_content,
        embeds = old_embeds,
        poll = old_poll,
    )
    
    input_data = {
        'attachments': [attachment.to_data(include_internals = True) for attachment in new_attachments],
        'components': [component.to_data() for component in new_components],
        'content': new_content,
        'embeds': [embed.to_data() for embed in new_embeds],
        'poll': new_poll.to_data(include_internals = True),
    }
    
    message._update_content_fields(input_data)

    vampytest.assert_eq(message.attachments, tuple(new_attachments))
    vampytest.assert_eq(message.components, tuple(new_components))
    vampytest.assert_eq(message.content, new_content)
    vampytest.assert_eq(message.embeds, tuple(new_embeds))
    vampytest.assert_eq(message.poll, new_poll)
    

def test__Message__update_content_fields__caching():
    """
    Tests whether ``Message._update_content_fields`` works as intended.
    
    Case: caching.
    """
    channel_id_0 = 202305030126
    channel_id_1 = 202305030127
    
    channel_0 = Channel.precreate(channel_id_0)
    channel_1 = Channel.precreate(channel_id_1)
    
    old_content = channel_0.mention
    new_content = channel_1.mention
    
    message = Message(content = old_content)
    old_mentioned_channels = message.mentioned_channels
    
    input_data = {
        'content': new_content,
    }
    
    message._update_content_fields(input_data)
    new_mentioned_channels = message.mentioned_channels
    
    vampytest.assert_ne(old_mentioned_channels, new_mentioned_channels)


def test__Message__to_message_reference_data():
    """
    Tests whether ``Message.to_message_reference_data`` works as intended.
    """
    message_id = 202305040102
    channel_id = 202305040103
    guild_id = 2023050400104
    
    message = Message.precreate(
        message_id,
        channel_id = channel_id,
        guild_id = guild_id,
    )
    
    expected_output = {
        'message_id': str(message_id),
        'channel_id': str(channel_id),
        'guild_id': str(guild_id),
    }
    
    output = message.to_message_reference_data()
    
    vampytest.assert_eq(output, expected_output)
