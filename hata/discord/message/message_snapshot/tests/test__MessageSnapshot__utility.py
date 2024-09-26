from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....channel import Channel
from ....component import Component, ComponentType
from ....embed import Embed
from ....role import Role
from ....sticker import Sticker
from ....user import User

from ...attachment import Attachment
from ...message import MessageFlag, MessageType

from ..message_snapshot import MessageSnapshot

from .test__MessageSnapshot__constructor import _assert_fields_set


def test__MessageSnapshot__copy():
    """
    Tests whether ``MessageSnapshot.copy`` works as intended.
    """
    attachments = [
        Attachment.precreate(202405250014, name = 'Koishi'),
        Attachment.precreate(202405250015, name = 'Komeiji'),
    ]
    components = [
        Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Rose')]),
        Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Slayer')]),
    ]
    content = 'orin'
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    edited_at = DateTime(2017, 5, 14, tzinfo = TimeZone.utc)
    embeds = [Embed('okuu'), Embed('egg')]
    flags = MessageFlag(12)
    mentioned_role_ids = [202407200024, 202407200025]
    mentioned_users = [
        User.precreate(202407200052, name = 'Kaenbyou'),
        User.precreate(202407200053, name = 'Rin'),
    ]
    message_type = MessageType.call
    stickers = [
        Sticker.precreate(202409200072, name = 'Make'),
        Sticker.precreate(202409200073, name = 'Me'),
    ]
    
    message_snapshot = MessageSnapshot(
        attachments = attachments,
        components = components,
        content = content,
        created_at = created_at,
        edited_at = edited_at,
        embeds = embeds,
        flags = flags,
        mentioned_role_ids = mentioned_role_ids,
        mentioned_users = mentioned_users,
        message_type = message_type,
        stickers = stickers,
    )
    copy = message_snapshot.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(message_snapshot, copy)
    
    vampytest.assert_eq(message_snapshot, copy)


def test__MessageSnapshot__copy_with__no_fields():
    """
    Tests whether ``MessageSnapshot.copy_with`` works as intended.
    
    Case: no fields given.
    """
    attachments = [
        Attachment.precreate(202405250016, name = 'Koishi'),
        Attachment.precreate(202405250017, name = 'Komeiji'),
    ]
    components = [
        Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Rose')]),
        Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Slayer')]),
    ]
    content = 'orin'
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    edited_at = DateTime(2017, 5, 14, tzinfo = TimeZone.utc)
    embeds = [Embed('okuu'), Embed('egg')]
    flags = MessageFlag(12)
    mentioned_role_ids = [202407200026, 202407200027]
    mentioned_users = [
        User.precreate(202407200054, name = 'Kaenbyou'),
        User.precreate(202407200055, name = 'Rin'),
    ]
    message_type = MessageType.call
    stickers = [
        Sticker.precreate(202409200074, name = 'Make'),
        Sticker.precreate(202409200075, name = 'Me'),
    ]
    
    message_snapshot = MessageSnapshot(
        attachments = attachments,
        components = components,
        content = content,
        created_at = created_at,
        edited_at = edited_at,
        embeds = embeds,
        flags = flags,
        mentioned_role_ids = mentioned_role_ids,
        mentioned_users = mentioned_users,
        message_type = message_type,
        stickers = stickers,
    )
    copy = message_snapshot.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(message_snapshot, copy)
    
    vampytest.assert_eq(message_snapshot, copy)


def test__MessageSnapshot__copy_with__all_fields():
    """
    Tests whether ``MessageSnapshot.copy_with`` works as intended.
    
    Case: all fields given.
    """
    old_attachments = [
        Attachment.precreate(202405250018, name = 'Koishi'),
        Attachment.precreate(202405250019, name = 'Komeiji'),
    ]
    old_components = [
        Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Rose')]),
        Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Slayer')]),
    ]
    old_content = 'orin'
    old_created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    old_edited_at = DateTime(2017, 5, 14, tzinfo = TimeZone.utc)
    old_embeds = [Embed('okuu'), Embed('egg')]
    old_flags = MessageFlag(12)
    old_mentioned_role_ids = [202407200028, 202407200029]
    old_mentioned_users = [
        User.precreate(202407200056, name = 'Kaenbyou'),
        User.precreate(202407200057, name = 'Rin'),
    ]
    old_message_type = MessageType.call
    old_stickers = [
        Sticker.precreate(202409200076, name = 'Make'),
        Sticker.precreate(202409200077, name = 'Me'),
    ]
    
    new_attachments = [
        Attachment.precreate(202405250020, name = 'komeiji'),
        Attachment.precreate(202405250021, name = 'koishi'),
    ]
    new_components = [
        Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Carmilia')]),
        Component(ComponentType.row, components = [Component(ComponentType.button, label = 'the')]),
    ]
    new_content = 'miau'
    new_created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    new_edited_at = DateTime(2017, 5, 14, tzinfo = TimeZone.utc)
    new_embeds = [Embed('boils'), Embed('them')]
    new_flags = MessageFlag(78)
    new_mentioned_role_ids = [202407200030, 202407200031]
    new_mentioned_users = [
        User.precreate(202407200058, name = 'Kaenbyou'),
        User.precreate(202407200059, name = 'Rin'),
    ]
    new_message_type = MessageType.user_add
    new_stickers = [
        Sticker.precreate(202409200078, name = 'Come'),
        Sticker.precreate(202409200079, name = 'Alive'),
    ]
    
    message_snapshot = MessageSnapshot(
        attachments = old_attachments,
        components = old_components,
        content = old_content,
        created_at = old_created_at,
        edited_at = old_edited_at,
        embeds = old_embeds,
        flags = old_flags,
        mentioned_role_ids = old_mentioned_role_ids,
        mentioned_users = old_mentioned_users,
        message_type = old_message_type,
        stickers = old_stickers,
    )
    copy = message_snapshot.copy_with(
        attachments = new_attachments,
        components = new_components,
        content = new_content,
        created_at = new_created_at,
        edited_at = new_edited_at,
        embeds = new_embeds,
        flags = new_flags,
        mentioned_role_ids = new_mentioned_role_ids,
        mentioned_users = new_mentioned_users,
        message_type = new_message_type,
        stickers = new_stickers,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(message_snapshot, copy)
    
    vampytest.assert_eq(copy.attachments, tuple(new_attachments))
    vampytest.assert_eq(copy.components, tuple(new_components))
    vampytest.assert_eq(copy.content, new_content)
    vampytest.assert_eq(copy.created_at, new_created_at)
    vampytest.assert_eq(copy.edited_at, new_edited_at)
    vampytest.assert_eq(copy.embeds, tuple(new_embeds))
    vampytest.assert_eq(copy.flags, new_flags)
    vampytest.assert_eq(copy.mentioned_role_ids, tuple(new_mentioned_role_ids))
    vampytest.assert_eq(copy.mentioned_users, tuple(new_mentioned_users))
    vampytest.assert_eq(copy.stickers, tuple(new_stickers))
    vampytest.assert_is(copy.type, new_message_type)


def _iter_options__embed():
    embed_0 = Embed('orin')
    embed_1 = Embed('miau')
    
    yield None, None
    yield [embed_0], embed_0
    yield [embed_0, embed_1], embed_0


@vampytest._(vampytest.call_from(_iter_options__embed()).returning_last())
def test__MessageSnapshot__embed(embeds):
    """
    Tests whether ``MessageSnapshot.embed`` works as intended.
    
    Parameters
    ----------
    embeds : `None | list<Embed>`
        Embeds to test with.
    
    Returns
    -------
    embed : `None | Embed`
    """
    message_snapshot = MessageSnapshot(
        embeds = embeds,
    )
    
    output = message_snapshot.embed
    vampytest.assert_instance(output, Embed, nullable = True)
    return output


def _iter_options__attachment():
    attachment_0 = Attachment.precreate(202405250035, name = 'orin')
    attachment_1 = Attachment.precreate(202405250036, name = 'miau')
    
    yield None, None
    yield [attachment_0], attachment_0
    yield [attachment_0, attachment_1], attachment_0


@vampytest._(vampytest.call_from(_iter_options__attachment()).returning_last())
def test__MessageSnapshot__attachment(attachments):
    """
    Tests whether ``MessageSnapshot.attachment`` works as intended.
    
    Parameters
    ----------
    attachments : `None | list<Attachment>`
        Attachments to test with.
    
    Returns
    -------
    attachment : `None | Attachment`
    """
    message_snapshot = MessageSnapshot(
        attachments = attachments,
    )
    
    output = message_snapshot.attachment
    vampytest.assert_instance(output, Attachment, nullable = True)
    return output


def _iter_options__sticker():
    sticker_0 = Sticker.precreate(202409200080, name = 'orin')
    sticker_1 = Sticker.precreate(202409200081, name = 'miau')
    
    yield None, None
    yield [sticker_0], sticker_0
    yield [sticker_0, sticker_1], sticker_0


@vampytest._(vampytest.call_from(_iter_options__sticker()).returning_last())
def test__MessageSnapshot__sticker(stickers):
    """
    Tests whether ``MessageSnapshot.sticker`` works as intended.
    
    Parameters
    ----------
    stickers : `None | list<Sticker>`
        Stickers to test with.
    
    Returns
    -------
    sticker : `None | Sticker`
    """
    message_snapshot = MessageSnapshot(
        stickers = stickers,
    )
    
    output = message_snapshot.sticker
    vampytest.assert_instance(output, Sticker, nullable = True)
    return output


def _iter_options__iter_embeds():
    embed_0 = Embed('orin')
    embed_1 = Embed('miau')
    
    yield None, []
    yield [embed_0], [embed_0]
    yield [embed_0, embed_1], [embed_0, embed_1]


@vampytest._(vampytest.call_from(_iter_options__iter_embeds()).returning_last())
def test__MessageSnapshot__iter_embeds(embeds):
    """
    Tests whether ``MessageSnapshot.iter_embeds`` works as intended.
    
    Parameters
    ----------
    embeds : `None | list<Embed>`
        Embeds to test with.
    
    Returns
    -------
    embed : `None | Embed`
    """
    message_snapshot = MessageSnapshot(
        embeds = embeds,
    )
    
    return [*message_snapshot.iter_embeds()]


def _iter_options__iter_attachments():
    attachment_0 = Attachment.precreate(202405250037, name = 'orin')
    attachment_1 = Attachment.precreate(202405250038, name = 'miau')
    
    yield None, []
    yield [attachment_0], [attachment_0]
    yield [attachment_0, attachment_1], [attachment_0, attachment_1]


@vampytest._(vampytest.call_from(_iter_options__iter_attachments()).returning_last())
def test__MessageSnapshot__iter_attachments(attachments):
    """
    Tests whether ``MessageSnapshot.iter_attachments`` works as intended.
    
    Parameters
    ----------
    attachments : `None | list<Attachment>`
        Attachments to test with.
    
    Returns
    -------
    attachment : `None | Attachment`
    """
    message_snapshot = MessageSnapshot(
        attachments = attachments,
    )
    
    return [*message_snapshot.iter_attachments()]


def _iter_options__iter_components():
    component_0 = Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Rose')])
    component_1 = Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Slayer')])
    
    yield None, []
    yield [component_0], [component_0]
    yield [component_0, component_1], [component_0, component_1]


@vampytest._(vampytest.call_from(_iter_options__iter_components()).returning_last())
def test__MessageSnapshot__iter_components(components):
    """
    Tests whether ``MessageSnapshot.iter_components`` works as intended.
    
    Parameters
    ----------
    components : `None | list<Component>`
        Components to test with.
    
    Returns
    -------
    component : `None | Component`
    """
    message_snapshot = MessageSnapshot(
        components = components,
    )
    
    return [*message_snapshot.iter_components()]


def _iter_options__iter_mentioned_role_ids():
    role_id_0 = 202407200032
    role_id_1 = 202407200033
    
    yield None, []
    yield [role_id_0], [role_id_0]
    yield [role_id_0, role_id_1], [role_id_0, role_id_1]


@vampytest._(vampytest.call_from(_iter_options__iter_mentioned_role_ids()).returning_last())
def test__MessageSnapshot__iter_mentioned_role_ids(input_value):
    """
    Tests whether ``MessageSnapshot.iter_mentioned_role_ids`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<int>`
        Value to test with.
    
    Returns
    -------
    output : `list<int>`
    """
    message_snapshot = MessageSnapshot(mentioned_role_ids = input_value)
    return [*message_snapshot.iter_mentioned_role_ids()]


def _iter_options__iter_mentioned_roles():
    role_id_0 = 202407200034
    role_id_1 = 202407200035
    role_0 = Role.precreate(role_id_0)
    role_1 = Role.precreate(role_id_1)
    
    yield None, []
    yield [role_id_0], [role_0]
    yield [role_id_0, role_id_1], [role_0, role_1]


@vampytest._(vampytest.call_from(_iter_options__iter_mentioned_roles()).returning_last())
def test__MessageSnapshot__iter_mentioned_roles(input_value):
    """
    Tests whether ``MessageSnapshot.iter_mentioned_roles`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<int>`
        Value to test with.
    
    Returns
    -------
    output : `list<Role>`
    """
    message_snapshot = MessageSnapshot(mentioned_role_ids = input_value)
    return [*message_snapshot.iter_mentioned_roles()]


def _iter_options__mentioned_roles():
    role_id_0 = 202407200036
    role_id_1 = 202407200037
    role_0 = Role.precreate(role_id_0)
    role_1 = Role.precreate(role_id_1)
    
    yield None, None
    yield [role_id_0], (role_0,)
    yield [role_id_0, role_id_1], (role_0, role_1)


@vampytest._(vampytest.call_from(_iter_options__mentioned_roles()).returning_last())
def test__MessageSnapshot__mentioned_roles(input_value):
    """
    Tests whether ``MessageSnapshot.mentioned_roles`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<int>`
        Value to test with.
    
    Returns
    -------
    output : `None | tuple<Role>`
    """
    message_snapshot = MessageSnapshot(mentioned_role_ids = input_value)
    return message_snapshot.mentioned_roles


def _iter_options__iter_mentioned_users():
    user_0 = User.precreate(202407200060)
    user_1 = User.precreate(202407200061)
    
    yield None, []
    yield [user_0], [user_0]
    yield [user_0, user_1], [user_0, user_1]


@vampytest._(vampytest.call_from(_iter_options__iter_mentioned_users()).returning_last())
def test__MessageSnapshot__iter_mentioned_users(input_value):
    """
    Tests whether ``MessageSnapshot.iter_mentioned_users`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<ClientUserBase>`
        Value to test with.
    
    Returns
    -------
    output : `list<ClientUserBase>`
    """
    message_snapshot = MessageSnapshot(mentioned_users = input_value)
    return [*message_snapshot.iter_mentioned_users()]


def _iter_options__mentioned_channels():
    channel_0 = Channel.precreate(202407210000)
    channel_1 = Channel.precreate(202407210001)
    
    yield None, None
    yield channel_0.mention, (channel_0, )
    yield channel_0.mention + channel_1.mention, (channel_0, channel_1)


@vampytest._(vampytest.call_from(_iter_options__mentioned_channels()).returning_last())
def test__MessageSnapshot__mentioned_channels(input_value):
    """
    Tests whether ``MessageSnapshot.mentioned_channels`` works as intended.
    
    Parameters
    ----------
    input_value : `None | str`
        Value to test with.
    
    Returns
    -------
    output : `None | tuple<Channel>`
    """
    message_snapshot = MessageSnapshot(content = input_value)
    return message_snapshot.mentioned_channels


def _iter_options__iter_mentioned_channels():
    channel_0 = Channel.precreate(202407210002)
    channel_1 = Channel.precreate(202407210003)
    
    yield None, []
    yield channel_0.mention, [channel_0]
    yield channel_0.mention + channel_1.mention, [channel_0, channel_1]


@vampytest._(vampytest.call_from(_iter_options__iter_mentioned_channels()).returning_last())
def test__MessageSnapshot__iter_mentioned_channels(input_value):
    """
    Tests whether ``MessageSnapshot.iter_mentioned_channels`` works as intended.
    
    Parameters
    ----------
    input_value : `None | str`
        Value to test with.
    
    Returns
    -------
    output : `list<Channel>`
    """
    message_snapshot = MessageSnapshot(content = input_value)
    return [*message_snapshot.iter_mentioned_channels()]


def _iter_options__iter_stickers():
    sticker_0 = Sticker.precreate(202409200082, name = 'orin')
    sticker_1 = Sticker.precreate(202409200083, name = 'miau')
    
    yield None, []
    yield [sticker_0], [sticker_0]
    yield [sticker_0, sticker_1], [sticker_0, sticker_1]


@vampytest._(vampytest.call_from(_iter_options__iter_stickers()).returning_last())
def test__MessageSnapshot__iter_stickers(stickers):
    """
    Tests whether ``MessageSnapshot.iter_stickers`` works as intended.
    
    Parameters
    ----------
    stickers : `None | list<Sticker>`
        Stickers to test with.
    
    Returns
    -------
    sticker : `None | Sticker`
    """
    message_snapshot = MessageSnapshot(
        stickers = stickers,
    )
    
    return [*message_snapshot.iter_stickers()]
