from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....embed import Embed

from ...attachment import Attachment
from ...message import MessageFlag

from ..message_snapshot import MessageSnapshot


def test__MessageSnapshot__repr():
    """
    Tests whether ``MessageSnapshot.__repr__`` works as intended.
    """
    attachments = [
        Attachment.precreate(202405250006, name = 'Koishi'),
        Attachment.precreate(202405250007, name = 'Komeiji'),
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
    
    vampytest.assert_instance(repr(message_snapshot), str)


def test__MessageSnapshot__hash():
    """
    Tests whether ``MessageSnapshot.__hash__`` works as intended.
    """
    attachments = [
        Attachment.precreate(202405250008, name = 'Koishi'),
        Attachment.precreate(202405250009, name = 'Komeiji'),
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
    
    vampytest.assert_instance(hash(message_snapshot), int)


def _iter_options__eq__different_type():
    yield object(), False


@vampytest._(vampytest.call_from(_iter_options__eq__different_type()).returning_last())
def test__messageSnapshot__eq__different_type(other):
    """
    Tests whether ``MessageSnapshot.__eq__`` works as intended.
    
    Case: Different type.
    
    Parameters
    ----------
    other : `object`
        Object to compare to.
    
    Returns
    -------
    output : `bool`
    """
    attachments = [
        Attachment.precreate(202405250010, name = 'Koishi'),
        Attachment.precreate(202405250011, name = 'Komeiji'),
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
    
    output = message_snapshot == other
    vampytest.assert_instance(output, bool)
    return output



def _iter_options__eq__same_type():
    attachments = [
        Attachment.precreate(202405250012, name = 'Koishi'),
        Attachment.precreate(202405250013, name = 'Komeiji'),
    ]
    content = 'orin'
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    edited_at = DateTime(2017, 5, 14, tzinfo = TimeZone.utc)
    embeds = [Embed('okuu'), Embed('egg')]
    flags = MessageFlag(12)
    
    keyword_parameters = {
        'attachments': attachments,
        'content': content,
        'created_at': created_at,
        'edited_at': edited_at,
        'embeds': embeds,
        'flags': flags,
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
            'attachments': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'content': 'miau',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'created_at': DateTime(2016, 5, 15, tzinfo = TimeZone.utc),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'edited_at': DateTime(2017, 5, 15, tzinfo = TimeZone.utc),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'embeds': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'flags': MessageFlag(78),
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq__same_type()).returning_last())
def test__messageSnapshot__eq__same_type(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``MessageSnapshot.__eq__`` works as intended.
    
    Case: Different type.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    message_snapshot_0 = MessageSnapshot(**keyword_parameters_0)
    message_snapshot_1 = MessageSnapshot(**keyword_parameters_1)
    
    output = message_snapshot_0 == message_snapshot_1
    vampytest.assert_instance(output, bool)
    return output
