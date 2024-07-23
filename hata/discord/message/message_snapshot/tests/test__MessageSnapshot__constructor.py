from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....embed import Embed
from ....user import User

from ...attachment import Attachment
from ...message import MessageFlag, MessageType

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
    vampytest.assert_instance(message_snapshot._cache_mentioned_channels, tuple, nullable = True)
    vampytest.assert_instance(message_snapshot._state, int)
    vampytest.assert_instance(message_snapshot.attachments, tuple, nullable = True)
    vampytest.assert_instance(message_snapshot.content, str, nullable = True)
    vampytest.assert_instance(message_snapshot.created_at, DateTime)
    vampytest.assert_instance(message_snapshot.edited_at, DateTime, nullable = True)
    vampytest.assert_instance(message_snapshot.embeds, tuple, nullable = True)
    vampytest.assert_instance(message_snapshot.flags, MessageFlag)
    vampytest.assert_instance(message_snapshot.mentioned_role_ids, tuple, nullable = True)
    vampytest.assert_instance(message_snapshot.mentioned_users, tuple, nullable = True)
    vampytest.assert_instance(message_snapshot.type, MessageType)


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
    mentioned_role_ids = [202407200012, 202407200013]
    mentioned_users = [
        User.precreate(202407200040, name = 'Kaenbyou'),
        User.precreate(202407200041, name = 'Rin'),
    ]
    message_type = MessageType.call

    message_snapshot = MessageSnapshot(
        attachments = attachments,
        content = content,
        created_at = created_at,
        edited_at = edited_at,
        embeds = embeds,
        flags = flags,
        mentioned_role_ids = mentioned_role_ids,
        mentioned_users = mentioned_users,
        message_type = message_type,
    )
    _assert_fields_set(message_snapshot)
    
    vampytest.assert_eq(message_snapshot.attachments, tuple(attachments))
    vampytest.assert_eq(message_snapshot.content, content)
    vampytest.assert_eq(message_snapshot.created_at, created_at)
    vampytest.assert_eq(message_snapshot.edited_at, edited_at)
    vampytest.assert_eq(message_snapshot.embeds, tuple(embeds))
    vampytest.assert_eq(message_snapshot.flags, flags)
    vampytest.assert_eq(message_snapshot.mentioned_role_ids, tuple(mentioned_role_ids))
    vampytest.assert_eq(message_snapshot.mentioned_users, tuple(mentioned_users))
    vampytest.assert_is(message_snapshot.type, message_type)
