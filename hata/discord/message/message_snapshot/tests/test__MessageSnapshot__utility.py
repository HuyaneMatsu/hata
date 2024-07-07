from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....embed import Embed

from ...attachment import Attachment
from ...message import MessageFlag

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
    content = 'orin'
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    edited_at = DateTime(2017, 5, 14, tzinfo = TimeZone.utc)
    embeds = [Embed('okuu'), Embed('egg')]
    flags = MessageFlag(12)
    
    message_snapshot = MessageSnapshot(
        attachments = attachments,
        content = content,
        created_at = created_at,
        edited_at = edited_at,
        embeds = embeds,
        flags = flags,
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
    content = 'orin'
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    edited_at = DateTime(2017, 5, 14, tzinfo = TimeZone.utc)
    embeds = [Embed('okuu'), Embed('egg')]
    flags = MessageFlag(12)
    
    message_snapshot = MessageSnapshot(
        attachments = attachments,
        content = content,
        created_at = created_at,
        edited_at = edited_at,
        embeds = embeds,
        flags = flags,
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
    old_content = 'orin'
    old_created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    old_edited_at = DateTime(2017, 5, 14, tzinfo = TimeZone.utc)
    old_embeds = [Embed('okuu'), Embed('egg')]
    old_flags = MessageFlag(12)
    
    new_attachments = [
        Attachment.precreate(202405250020, name = 'komeiji'),
        Attachment.precreate(202405250021, name = 'koishi'),
    ]
    new_content = 'miau'
    new_created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    new_edited_at = DateTime(2017, 5, 14, tzinfo = TimeZone.utc)
    new_embeds = [Embed('boils'), Embed('them')]
    new_flags = MessageFlag(78)
    
    message_snapshot = MessageSnapshot(
        attachments = old_attachments,
        content = old_content,
        created_at = old_created_at,
        edited_at = old_edited_at,
        embeds = old_embeds,
        flags = old_flags,
    )
    copy = message_snapshot.copy_with(
        attachments = new_attachments,
        content = new_content,
        created_at = new_created_at,
        edited_at = new_edited_at,
        embeds = new_embeds,
        flags = new_flags,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(message_snapshot, copy)
    
    vampytest.assert_eq(copy.attachments, tuple(new_attachments))
    vampytest.assert_eq(copy.content, new_content)
    vampytest.assert_eq(copy.created_at, new_created_at)
    vampytest.assert_eq(copy.edited_at, new_edited_at)
    vampytest.assert_eq(copy.embeds, tuple(new_embeds))
    vampytest.assert_eq(copy.flags, new_flags)


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
