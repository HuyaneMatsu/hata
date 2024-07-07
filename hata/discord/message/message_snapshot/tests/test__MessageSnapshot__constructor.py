from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....embed import Embed

from ...attachment import Attachment
from ...message import MessageFlag

from ..message_snapshot import MessageSnapshot


def _assert_fields_set(message_snapshot):
    """
    Tests whether all attributes are set of the given message snapshot.
    
    Parameters
    ----------
    message_snapshot : ``MessageSnapshot``
        The message snapshot to check.
    """
    vampytest.assert_instance(message_snapshot, MessageSnapshot)
    vampytest.assert_instance(message_snapshot.attachments, tuple, nullable = True)
    vampytest.assert_instance(message_snapshot.content, str, nullable = True)
    vampytest.assert_instance(message_snapshot.created_at, DateTime)
    vampytest.assert_instance(message_snapshot.edited_at, DateTime, nullable = True)
    vampytest.assert_instance(message_snapshot.embeds, tuple, nullable = True)
    vampytest.assert_instance(message_snapshot.flags, MessageFlag)


def test__MessageSnapshot__new__no_fields():
    """
    Tests whether ``MessageSnapshot.__new__`` works as intended.
    
    Case: No fields given.
    """
    message_snapshot = MessageSnapshot()
    _assert_fields_set(message_snapshot)


def test__MessageSnapshot__new__all_fields():
    """
    Tests whether ``MessageSnapshot.__new__`` works as intended.
    
    Case: All fields given.
    """
    attachments = [
        Attachment.precreate(202405250000, name = 'Koishi'),
        Attachment.precreate(202405250001, name = 'Komeiji'),
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
    _assert_fields_set(message_snapshot)
    
    vampytest.assert_eq(message_snapshot.attachments, tuple(attachments))
    vampytest.assert_eq(message_snapshot.content, content)
    vampytest.assert_eq(message_snapshot.created_at, created_at)
    vampytest.assert_eq(message_snapshot.edited_at, edited_at)
    vampytest.assert_eq(message_snapshot.embeds, tuple(embeds))
    vampytest.assert_eq(message_snapshot.flags, flags)
