from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....channel import Channel, ChannelType
from ....component import Component, ComponentType
from ....core import BUILTIN_EMOJIS
from ....embed import EmbedAuthor, Embed, EmbedField, EmbedFooter, EmbedProvider
from ....emoji import Reaction, ReactionMapping, ReactionMappingLine, ReactionType
from ....poll import Poll, PollAnswer, PollQuestion
from ....resolved import Resolved
from ....soundboard import SoundboardSound
from ....sticker import Sticker
from ....user import User

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
    poll = Poll(expires_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc))
    reactions = ReactionMapping(
        lines = {
            Reaction.from_fields(BUILTIN_EMOJIS['x'], ReactionType.standard): ReactionMappingLine(count = 2),
        },
    )
    referenced_message = Message.precreate(202305040032, content = 'Patchouli')
    resolved = Resolved(attachments = [Attachment.precreate(202310110030)])
    role_subscription = MessageRoleSubscription(tier_name = 'Knowledge')
    shared_client_theme = SharedClientTheme(intensity = 6)
    snapshots = [
        MessageSnapshot(content = 'Kazami'),
        MessageSnapshot(content = 'Yuuka'),
    ]
    soundboard_sounds = [
        SoundboardSound.precreate(202501290014, name = 'whither'),
        SoundboardSound.precreate(202501290015, name = 'Yuyuko'),
    ]
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
        'poll': poll,
        'reactions': reactions,
        'referenced_message': referenced_message,
        'resolved': resolved,
        'role_subscription': role_subscription,
        'shared_client_theme': shared_client_theme,
        'snapshots': snapshots,
        'soundboard_sounds': soundboard_sounds,
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
    poll = Poll(expires_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc))
    reactions = ReactionMapping(
        lines = {
            Reaction.from_fields(BUILTIN_EMOJIS['x'], ReactionType.standard): ReactionMappingLine(count = 2),
        },
    )
    referenced_message = Message.precreate(202305040050, content = 'Patchouli')
    resolved = Resolved(attachments = [Attachment.precreate(202310110031)])
    role_subscription = MessageRoleSubscription(tier_name = 'Knowledge')
    shared_client_theme = SharedClientTheme(intensity = 6)
    snapshots = [
        MessageSnapshot(content = 'Kazami'),
        MessageSnapshot(content = 'Yuuka'),
    ]
    soundboard_sounds = [
        SoundboardSound.precreate(202501290016, name = 'whither'),
        SoundboardSound.precreate(202501290017, name = 'Yuyuko'),
    ]
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
        'poll': poll,
        'reactions': reactions,
        'referenced_message': referenced_message,
        'resolved': resolved,
        'role_subscription': role_subscription,
        'shared_client_theme': shared_client_theme,
        'snapshots': snapshots,
        'soundboard_sounds': soundboard_sounds,
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


def test__Message__eq__same():
    """
    Tests whether ``Message.__eq__`` works as intended.
    
    Case: same.
    """
    content = 'miau'
    
    message_id = 202305040092
    channel_id = 202305040093
    guild_id = 202305040094
    
    message = Message.precreate(
        message_id,
        channel_id = channel_id,
        guild_id = guild_id,
        content = content,
    )
    
    output = message == message
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)


def test__Message__eq__partial_comparison():
    """
    Tests whether ``Message.__eq__`` works as intended.
    
    Case: partial comparison.
    """
    content = 'miau'
    
    message_id = 202305040200
    channel_id = 202305040202
    guild_id = 2023050402003
    
    message_0 = Message.precreate(
        message_id,
        channel_id = channel_id,
        guild_id = guild_id,
        content = content,
    )
    
    message_1 = Message(
        content = content,
    )
    
    output = message_0 == message_1
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)


def _iter_options__eq__different_type():
    yield object(), False


@vampytest._(vampytest.call_from(_iter_options__eq__different_type()).returning_last())
def test__Message__eq__different_type(other):
    """
    Tests whether ``Message.__eq__`` works as intended.
    
    Case: different type.
    
    Parameters
    ----------
    other : `object`
        Other object to compare to.
    
    Returns
    -------
    output : `bool`
    """
    message = Message()
    output = message == other
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__eq__same_type():
    activity = MessageActivity(party_id = 'Remilia')
    application = MessageApplication.precreate(202305040060, name = 'Flandre')
    application_id = 202305040061
    attachments = [
        Attachment.precreate(202305040062, name = 'Koishi'),
        Attachment.precreate(202305040063, name = 'Komeiji'),
    ]
    author = User.precreate(202305040064, name = 'Orin')
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
    interaction = MessageInteraction.precreate(202305040065, name = 'Ran')
    mentioned_channels_cross_guild = [
        Channel.precreate(202305040066, channel_type = ChannelType.guild_text, name = 'Chen'),
        Channel.precreate(202305040067, channel_type = ChannelType.guild_text, name = 'Yuugi'),
    ]
    mentioned_everyone = True
    mentioned_role_ids = [202305040068, 202305040069]
    mentioned_users = [
        User.precreate(202305040070, name = 'Scarlet'),
        User.precreate(202305040071, name = 'Izaoyi'),
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
    referenced_message = Message.precreate(202305040072, content = 'Patchouli')
    resolved = Resolved(attachments = [Attachment.precreate(202310110032)])
    role_subscription = MessageRoleSubscription(tier_name = 'Knowledge')
    shared_client_theme = SharedClientTheme(intensity = 6)
    snapshots = [
        MessageSnapshot(content = 'Kazami'),
        MessageSnapshot(content = 'Yuuka'),
    ]
    soundboard_sounds = [
        SoundboardSound.precreate(202501290018, name = 'whither'),
        SoundboardSound.precreate(202501290019, name = 'Yuyuko'),
    ]
    stickers = [
        Sticker.precreate(202305040073, name = 'Kirisame'),
        Sticker.precreate(202305040074, name = 'Marisa'),
    ]
    thread = Channel.precreate(202305040075, channel_type = ChannelType.guild_thread_private, name = 'Yuyuko')
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
        'poll': poll,
        'reactions': reactions,
        'referenced_message': referenced_message,
        'resolved': resolved,
        'role_subscription': role_subscription,
        'shared_client_theme': shared_client_theme,
        'snapshots': snapshots,
        'soundboard_sounds': soundboard_sounds,
        'stickers': stickers,
        'thread': thread,
        'tts': tts,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'activity': MessageActivity(party_id = 'Best girl'),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'application': MessageApplication.precreate(202305040076, name = 'Christmas tree'),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'application_id': 202305040077,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'attachments': [
                Attachment.precreate(202305040078, name = 'Closed eye'),
                Attachment.precreate(202305040079, name = 'Satoris'),
            ],
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'author': User.precreate(202305040080, name = 'Dancing'),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'call': MessageCall(ended_at = DateTime(2045, 5, 4, tzinfo = TimeZone.utc)),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'components': [
                Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Nuclear bird')]),
                Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Green hell')]),
            ],
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'content': 'Open eye',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'edited_at': DateTime(2016, 6, 14, tzinfo = TimeZone.utc),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'embeds': [
                Embed('Old hag and pets'),
                Embed('Old hag'),
            ],
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'flags': MessageFlag(12),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'interaction': MessageInteraction.precreate(202305040081, name = 'Old pet'),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'mentioned_channels_cross_guild': [
                Channel.precreate(202305040082, channel_type = ChannelType.guild_text, name = 'Cat'),
                Channel.precreate(202305040083, channel_type = ChannelType.guild_text, name = 'One horned'),
            ],
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'mentioned_everyone': False,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'mentioned_role_ids': [202305040084, 202305040085],
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'mentioned_users': [
                User.precreate(202305040086, name = 'Vampires'),
                User.precreate(202305040087, name = 'Love shop'),
            ],
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'message_type': MessageType.user_add,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'nonce': 'Maid',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'pinned': False,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'poll': Poll(expires_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'reactions': ReactionMapping(
                lines = {
                    Reaction.from_fields(BUILTIN_EMOJIS['heart'], ReactionType.standard): ReactionMappingLine(count = 1),
                },
            ),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'referenced_message': Message.precreate(202305040088, content = 'Book'),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'resolved': Resolved(attachments = [Attachment.precreate(202310110033)]),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'role_subscription': MessageRoleSubscription(tier_name = 'Big brain'),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'shared_client_theme': SharedClientTheme(intensity = 4),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'snapshots': [
                MessageSnapshot(content = 'Mushroom'),
                MessageSnapshot(content = 'Soup'),
            ]
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'soundboard_sounds': [
                SoundboardSound.precreate(202501290020, name = 'that'),
                SoundboardSound.precreate(202501290021, name = 'heart'),
            ],
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'stickers': [
                Sticker.precreate(202305040089, name = 'Magic'),
                Sticker.precreate(202305040090, name = 'Witch'),
            ],
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'thread': Channel.precreate(202305040091, channel_type = ChannelType.guild_thread_private, name = 'Hungry'),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'tts': False,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq__same_type()).returning_last())
def test__Message__eq__same_type(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``Message.__eq__`` works as intended.
    
    Case: same type.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance from.
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance from.
    
    Returns
    -------
    output : `bool`
    """
    message_0 = Message(**keyword_parameters_0)
    message_1 = Message(**keyword_parameters_1)
    output = message_0 == message_1
    vampytest.assert_instance(output, bool)
    return output


def test__Message__len__all_contents():
    """
    Tests whether ``Message.__len__`` works as intended.
    
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
    component_0_content = 'mayumi'
    component_1_content = 'keiki'
    
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
    
    component_0 = Component(
        ComponentType.text_display,
        content = component_0_content,
    )
    
    component_1 = Component(
        ComponentType.text_display,
        content = component_1_content,
    )
    
    message = Message(
        components = [component_0, component_1],
        content = message_content,
        embeds = [embed_0, embed_1],
        poll = poll,
    )
    
    length = sum(
        len(value) for value in (
            embed_0_title, embed_0_author_name, embed_0_description, embed_0_field_0_name, embed_0_field_0_value,
            embed_0_field_1_name, embed_0_field_1_value, embed_0_footer_text, embed_0_provider_name,
            message_content, embed_1_title, poll_question_text, poll_answer_0_text, poll_answer_1_text,
            component_0_content, component_1_content
        )
    )
    
    output = len(message)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, length)


def test__Message__len__no_contents():
    """
    Tests whether ``Message.__len__`` works as intended.
    
    Case: No contents.
    """
    message = Message()
    
    output = len(message)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 0)
