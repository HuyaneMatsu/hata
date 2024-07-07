from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....embed import Embed
from ....utils import datetime_to_timestamp

from ...attachment import Attachment
from ...message import MessageFlag

from ..message_snapshot import MessageSnapshot

from .test__MessageSnapshot__constructor import _assert_fields_set


def test__MessageSnapshot__from_data():
    """
    Tests whether ``MessageSnapshot.from_data`` works as intended.
    """
    attachments = [
        Attachment.precreate(202405250002, name = 'Koishi'),
        Attachment.precreate(202405250003, name = 'Komeiji'),
    ]
    content = 'orin'
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    edited_at = DateTime(2017, 5, 14, tzinfo = TimeZone.utc)
    embeds = [Embed('okuu'), Embed('egg')]
    flags = MessageFlag(12)
    
    data = {
        'message': {
            'attachments': [
                attachment.to_data(include_internals = True)
                for attachment in attachments
            ],
            'content': content,
            'timestamp': datetime_to_timestamp(created_at),
            'edited_timestamp': datetime_to_timestamp(edited_at),
            'embeds': [embed.to_data() for embed in embeds],
            'flags': int(flags),
        },
    }
    
    message_snapshot = MessageSnapshot.from_data(data)
    _assert_fields_set(message_snapshot)

    vampytest.assert_eq(message_snapshot.attachments, tuple(attachments))
    vampytest.assert_eq(message_snapshot.content, content)
    vampytest.assert_eq(message_snapshot.created_at, created_at)
    vampytest.assert_eq(message_snapshot.edited_at, edited_at)
    vampytest.assert_eq(message_snapshot.embeds, tuple(embeds))
    vampytest.assert_eq(message_snapshot.flags, flags)


def test__MessageSnapshot__to_data():
    """
    Tests whether ``MessageSnapshot.to_data`` works as intended.
    
    Case: include defaults.
    """
    attachments = [
        Attachment.precreate(202405250004, name = 'Koishi'),
        Attachment.precreate(202405250005, name = 'Komeiji'),
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
    
    vampytest.assert_eq(
        message_snapshot.to_data(
            defaults = True,
        ),
        {
            'message': {
                'attachments': [
                    attachment.to_data(defaults = True, include_internals = True)
                    for attachment in attachments
                ],
                'content': content,
                'timestamp': datetime_to_timestamp(created_at),
                'edited_timestamp': datetime_to_timestamp(edited_at),
                'embeds': [embed.to_data(defaults = True) for embed in embeds],
                'flags': int(flags),
            },
        }
    )
