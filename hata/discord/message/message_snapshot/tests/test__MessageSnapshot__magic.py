from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....component import Component, ComponentType
from ....embed import Embed
from ....soundboard import SoundboardSound
from ....sticker import Sticker
from ....user import User

from ...attachment import Attachment
from ...message import MessageFlag, MessageType

from ..message_snapshot import MessageSnapshot


def test__MessageSnapshot__repr():
    """
    Tests whether ``MessageSnapshot.__repr__`` works as intended.
    """
    attachments = [
        Attachment.precreate(202405250006, name = 'Koishi'),
        Attachment.precreate(202405250007, name = 'Komeiji'),
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
    mentioned_role_ids = [202407200018, 202407200019]
    mentioned_users = [
        User.precreate(202407200046, name = 'Kaenbyou'),
        User.precreate(202407200047, name = 'Rin'),
    ]
    message_type = MessageType.call
    soundboard_sounds = [
        SoundboardSound.precreate(202501300014, name = 'whither'),
        SoundboardSound.precreate(202501300015, name = 'Yuyuko'),
    ]
    stickers = [
        Sticker.precreate(202409200066, name = 'Make'),
        Sticker.precreate(202409200067, name = 'Me'),
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
        soundboard_sounds = soundboard_sounds,
        stickers = stickers,
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
    components = [
        Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Rose')]),
        Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Slayer')]),
    ]
    content = 'orin'
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    edited_at = DateTime(2017, 5, 14, tzinfo = TimeZone.utc)
    embeds = [Embed('okuu'), Embed('egg')]
    flags = MessageFlag(12)
    mentioned_role_ids = [202407200020, 202407200021]
    mentioned_users = [
        User.precreate(202407200048, name = 'Kaenbyou'),
        User.precreate(202407200049, name = 'Rin'),
    ]
    message_type = MessageType.call
    soundboard_sounds = [
        SoundboardSound.precreate(202501300016, name = 'whither'),
        SoundboardSound.precreate(202501300017, name = 'Yuyuko'),
    ]
    stickers = [
        Sticker.precreate(202409200068, name = 'Make'),
        Sticker.precreate(202409200069, name = 'Me'),
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
        soundboard_sounds = soundboard_sounds,
        stickers = stickers,
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
    message_snapshot = MessageSnapshot()
    
    output = message_snapshot == other
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__eq__same_type():
    attachments = [
        Attachment.precreate(202405250012, name = 'Koishi'),
        Attachment.precreate(202405250013, name = 'Komeiji'),
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
    mentioned_role_ids = [202407200022, 202407200023]
    mentioned_users = [
        User.precreate(202407200050, name = 'Kaenbyou'),
        User.precreate(202407200051, name = 'Rin'),
    ]
    message_type = MessageType.call
    soundboard_sounds = [
        SoundboardSound.precreate(202501300018, name = 'whither'),
        SoundboardSound.precreate(202501300019, name = 'Yuyuko'),
    ]
    stickers = [
        Sticker.precreate(202409200070, name = 'Make'),
        Sticker.precreate(202409200071, name = 'Me'),
    ]
    
    keyword_parameters = {
        'attachments': attachments,
        'components': components,
        'content': content,
        'created_at': created_at,
        'edited_at': edited_at,
        'embeds': embeds,
        'flags': flags,
        'mentioned_role_ids': mentioned_role_ids,
        'mentioned_users': mentioned_users,
        'message_type': message_type,
        'soundboard_sounds': soundboard_sounds,
        'stickers': stickers,
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
            'components': None,
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
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'mentioned_role_ids': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'mentioned_users': None,
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
            'soundboard_sounds': [
                SoundboardSound.precreate(202501300020, name = 'that'),
                SoundboardSound.precreate(202501300021, name = 'heart'),
            ],
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'stickers': None,
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
