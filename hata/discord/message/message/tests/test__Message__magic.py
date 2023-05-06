from datetime import datetime as DateTime

import vampytest

from ....channel import Channel, ChannelType, create_partial_channel_data
from ....component import Component, ComponentType
from ....core import BUILTIN_EMOJIS
from ....embed import Embed
from ....emoji import ReactionMapping
from ....sticker import Sticker
from ....user import User
from ....utils import datetime_to_timestamp

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


def test__Message__repr():
    """
    Tests whether ``Message.__repr__`` works as intended.
    """
    activity = MessageActivity(party_id = 'Remilia')
    application = MessageApplication.precreate(202305040020, name = 'Flandre')
    application_id = 202305040021
    attachments = [
        Attachment.precreate(202305040022, name = 'Koishi'),
        Attachment.precreate(202305040023, name = 'Komeiji'),
    ]
    author = User.precreate(202305040024, name = 'Orin')
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
    interaction = MessageInteraction.precreate(202305040025, name = 'Ran')
    mentioned_channels_cross_guild = [
        Channel.precreate(202305040026, channel_type = ChannelType.guild_text, name = 'Chen'),
        Channel.precreate(202305040027, channel_type = ChannelType.guild_text, name = 'Yuugi'),
    ]
    mentioned_everyone = True
    mentioned_role_ids = [202305040028, 202305040029]
    mentioned_users = [
        User.precreate(202305040030, name = 'Scarlet'),
        User.precreate(202305040031, name = 'Izaoyi'),
    ]
    message_type = MessageType.call
    nonce = 'Sakuya'
    pinned = True
    reactions = ReactionMapping({
        BUILTIN_EMOJIS['x']: [None, None],
    })
    referenced_message = Message.precreate(202305040032, content = 'Patchouli')
    role_subscription = MessageRoleSubscription(tier_name = 'Knowledge')
    stickers = [
        Sticker.precreate(202305040033, name = 'Kirisame'),
        Sticker.precreate(202305040034, name = 'Marisa'),
    ]
    thread = Channel.precreate(202305040035, channel_type = ChannelType.guild_thread_private, name = 'Yuyuko')
    tts = True
    
    keyword_parameters = {
        'activity': activity,
        'application': application,
        'application_id': application_id,
        'attachments': attachments,
        'author': author,
        'call': call,
        'components': components,
        'content': content,
        'edited_at': edited_at,
        'embeds': embeds,
        'flags': flags,
        'interaction': interaction,
        'mentioned_channels_cross_guild': mentioned_channels_cross_guild,
        'mentioned_everyone': mentioned_everyone,
        'mentioned_role_ids': mentioned_role_ids,
        'mentioned_users': mentioned_users,
        'message_type': message_type,
        'nonce': nonce,
        'pinned': pinned,
        'reactions': reactions,
        'referenced_message': referenced_message,
        'role_subscription': role_subscription,
        'stickers': stickers,
        'thread': thread,
        'tts': tts,
    }
    
    message_id = 202305040036
    channel_id = 202305040037
    guild_id = 202305040038
    
    message = Message.precreate(
        message_id,
        channel_id = channel_id,
        guild_id = guild_id,
        **keyword_parameters,
    )
    
    vampytest.assert_instance(repr(message), str)

    message = Message(
        **keyword_parameters,
    )
    
    vampytest.assert_instance(repr(message), str)


def test__Message__hash():
    """
    Tests whether ``Message.__hash__`` works as intended.
    """
    activity = MessageActivity(party_id = 'Remilia')
    application = MessageApplication.precreate(202305040039, name = 'Flandre')
    application_id = 202305040040
    attachments = [
        Attachment.precreate(202305040041, name = 'Koishi'),
        Attachment.precreate(202305040042, name = 'Komeiji'),
    ]
    author = User.precreate(202305040043, name = 'Orin')
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
    interaction = MessageInteraction.precreate(202305040044, name = 'Ran')
    mentioned_channels_cross_guild = [
        Channel.precreate(202305040045, channel_type = ChannelType.guild_text, name = 'Chen'),
        Channel.precreate(202305040046, channel_type = ChannelType.guild_text, name = 'Yuugi'),
    ]
    mentioned_everyone = True
    mentioned_role_ids = [202305040046, 202305040047]
    mentioned_users = [
        User.precreate(202305040048, name = 'Scarlet'),
        User.precreate(202305040049, name = 'Izaoyi'),
    ]
    message_type = MessageType.call
    nonce = 'Sakuya'
    pinned = True
    reactions = ReactionMapping({
        BUILTIN_EMOJIS['x']: [None, None],
    })
    referenced_message = Message.precreate(202305040050, content = 'Patchouli')
    role_subscription = MessageRoleSubscription(tier_name = 'Knowledge')
    stickers = [
        Sticker.precreate(202305040051, name = 'Kirisame'),
        Sticker.precreate(202305040052, name = 'Marisa'),
    ]
    thread = Channel.precreate(202305040053, channel_type = ChannelType.guild_thread_private, name = 'Yuyuko')
    tts = True
    
    keyword_parameters = {
        'activity': activity,
        'application': application,
        'application_id': application_id,
        'attachments': attachments,
        'author': author,
        'call': call,
        'components': components,
        'content': content,
        'edited_at': edited_at,
        'embeds': embeds,
        'flags': flags,
        'interaction': interaction,
        'mentioned_channels_cross_guild': mentioned_channels_cross_guild,
        'mentioned_everyone': mentioned_everyone,
        'mentioned_role_ids': mentioned_role_ids,
        'mentioned_users': mentioned_users,
        'message_type': message_type,
        'nonce': nonce,
        'pinned': pinned,
        'reactions': reactions,
        'referenced_message': referenced_message,
        'role_subscription': role_subscription,
        'stickers': stickers,
        'thread': thread,
        'tts': tts,
    }
    
    message_id = 202305040054
    channel_id = 202305040055
    guild_id = 202305040056
    
    message = Message.precreate(
        message_id,
        channel_id = channel_id,
        guild_id = guild_id,
        **keyword_parameters,
    )
    
    vampytest.assert_instance(hash(message), int)

    message = Message(
        **keyword_parameters,
    )
    
    vampytest.assert_instance(hash(message), int)


def test__Message__format():
    """
    Tests whether ``Message.__format__`` works as intended.
    """
    message_id = 202305040057
    channel_id = 202305040058
    guild_id = 202305040059
    
    message = Message.precreate(
        message_id,
        channel_id = channel_id,
        guild_id = guild_id,
    )
    
    vampytest.assert_instance(format(message, ''), str)
    vampytest.assert_instance(format(message, 'c'), str)
    vampytest.assert_instance(format(message, 'e'), str)
    
    with vampytest.assert_raises(ValueError):
        format(message, 'pepe')


def test__Message__eq():
    """
    Tests whether ``Message.__eq__`` works as intended.
    """
    old_activity = MessageActivity(party_id = 'Remilia')
    old_application = MessageApplication.precreate(202305040060, name = 'Flandre')
    old_application_id = 202305040061
    old_attachments = [
        Attachment.precreate(202305040062, name = 'Koishi'),
        Attachment.precreate(202305040063, name = 'Komeiji'),
    ]
    old_author = User.precreate(202305040064, name = 'Orin')
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
    old_interaction = MessageInteraction.precreate(202305040065, name = 'Ran')
    old_mentioned_channels_cross_guild = [
        Channel.precreate(202305040066, channel_type = ChannelType.guild_text, name = 'Chen'),
        Channel.precreate(202305040067, channel_type = ChannelType.guild_text, name = 'Yuugi'),
    ]
    old_mentioned_everyone = True
    old_mentioned_role_ids = [202305040068, 202305040069]
    old_mentioned_users = [
        User.precreate(202305040070, name = 'Scarlet'),
        User.precreate(202305040071, name = 'Izaoyi'),
    ]
    old_message_type = MessageType.call
    old_nonce = 'Sakuya'
    old_pinned = True
    old_reactions = ReactionMapping({
        BUILTIN_EMOJIS['x']: [None, None],
    })
    old_referenced_message = Message.precreate(202305040072, content = 'Patchouli')
    old_role_subscription = MessageRoleSubscription(tier_name = 'Knowledge')
    old_stickers = [
        Sticker.precreate(202305040073, name = 'Kirisame'),
        Sticker.precreate(202305040074, name = 'Marisa'),
    ]
    old_thread = Channel.precreate(202305040075, channel_type = ChannelType.guild_thread_private, name = 'Yuyuko')
    old_tts = True
    
    new_activity = MessageActivity(party_id = 'Best girl')
    new_application = MessageApplication.precreate(202305040076, name = 'Christmas tree')
    new_application_id = 202305040077
    new_attachments = [
        Attachment.precreate(202305040078, name = 'Closed eye'),
        Attachment.precreate(202305040079, name = 'Satoris'),
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
    new_interaction = MessageInteraction.precreate(202305040081, name = 'Old pet')
    new_mentioned_channels_cross_guild = [
        Channel.precreate(202305040082, channel_type = ChannelType.guild_text, name = 'Cat'),
        Channel.precreate(202305040083, channel_type = ChannelType.guild_text, name = 'One horned'),
    ]
    new_mentioned_everyone = False
    new_mentioned_role_ids = [202305040084, 202305040085]
    new_mentioned_users = [
        User.precreate(202305040086, name = 'Vampires'),
        User.precreate(202305040087, name = 'Love shop'),
    ]
    new_message_type = MessageType.user_add
    new_nonce = 'Maid'
    new_pinned = False
    new_reactions = ReactionMapping({
        BUILTIN_EMOJIS['heart']: [None],
    })
    new_referenced_message = Message.precreate(202305040088, content = 'Book')
    new_role_subscription = MessageRoleSubscription(tier_name = 'Big brain')
    new_stickers = [
        Sticker.precreate(202305040089, name = 'Magic'),
        Sticker.precreate(202305040090, name = 'Witch'),
    ]
    new_thread = Channel.precreate(202305040091, channel_type = ChannelType.guild_thread_private, name = 'Hungry')
    new_tts = False
    
    keyword_parameters = {
        'activity': old_activity,
        'application': old_application,
        'application_id': old_application_id,
        'attachments': old_attachments,
        'author': old_author,
        'call': old_call,
        'components': old_components,
        'content': old_content,
        'edited_at': old_edited_at,
        'embeds': old_embeds,
        'flags': old_flags,
        'interaction': old_interaction,
        'mentioned_channels_cross_guild': old_mentioned_channels_cross_guild,
        'mentioned_everyone': old_mentioned_everyone,
        'mentioned_role_ids': old_mentioned_role_ids,
        'mentioned_users': old_mentioned_users,
        'message_type': old_message_type,
        'nonce': old_nonce,
        'pinned': old_pinned,
        'reactions': old_reactions,
        'referenced_message': old_referenced_message,
        'role_subscription': old_role_subscription,
        'stickers': old_stickers,
        'thread': old_thread,
        'tts': old_tts,
    }
    
    new_fields = (
        ('activity', new_activity),
        ('application', new_application),
        ('application_id', new_application_id),
        ('attachments', new_attachments),
        ('author', new_author),
        ('call', new_call),
        ('components', new_components),
        ('content', new_content),
        ('edited_at', new_edited_at),
        ('embeds', new_embeds),
        ('flags', new_flags),
        ('interaction', new_interaction),
        ('mentioned_channels_cross_guild', new_mentioned_channels_cross_guild),
        ('mentioned_everyone', new_mentioned_everyone),
        ('mentioned_role_ids', new_mentioned_role_ids),
        ('mentioned_users', new_mentioned_users),
        ('message_type', new_message_type),
        ('nonce', new_nonce),
        ('pinned', new_pinned),
        ('reactions', new_reactions),
        ('referenced_message', new_referenced_message),
        ('role_subscription', new_role_subscription),
        ('stickers', new_stickers),
        ('thread', new_thread),
        ('tts', new_tts),
    )
    
    message_id = 202305040092
    channel_id = 202305040093
    guild_id = 202305040094
    
    message = Message.precreate(
        message_id,
        channel_id = channel_id,
        guild_id = guild_id,
        **keyword_parameters,
    )
    
    vampytest.assert_eq(message, message)
    vampytest.assert_ne(message, object())
    
    test_message = Message(**keyword_parameters)
    
    vampytest.assert_eq(message, test_message)
    
    for field_name, field_value in new_fields:
        test_message = Message(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(message, test_message)
