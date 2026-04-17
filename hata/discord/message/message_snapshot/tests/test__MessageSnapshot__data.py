from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....component import Component, ComponentType
from ....embed import Embed
from ....soundboard import SoundboardSound
from ....sticker import Sticker, create_partial_sticker_data
from ....user import GuildProfile, User
from ....utils import datetime_to_timestamp

from ...attachment import Attachment
from ...message import MessageFlag, MessageType

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
    components = [
        Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Rose')]),
        Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Slayer')]),
    ]
    content = 'orin'
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    edited_at = DateTime(2017, 5, 14, tzinfo = TimeZone.utc)
    embeds = [Embed('okuu'), Embed('egg')]
    flags = MessageFlag(12)
    mentioned_role_ids = [202407200014, 202407200015]
    mentioned_users = [
        User.precreate(202407200042, name = 'Kaenbyou'),
        User.precreate(202407200043, name = 'Rin'),
    ]
    message_type = MessageType.call
    soundboard_sounds = [
        SoundboardSound.precreate(202501300010, name = 'whither'),
        SoundboardSound.precreate(202501300011, name = 'Yuyuko'),
    ]
    stickers = [
        Sticker.precreate(202409200062, name = 'Make'),
        Sticker.precreate(202409200063, name = 'Me'),
    ]
    
    data = {
        'message': {
            'attachments': [
                attachment.to_data(include_internals = True)
                for attachment in attachments
            ],
            'components': [component.to_data() for component in components],
            'content': content,
            'timestamp': datetime_to_timestamp(created_at),
            'edited_timestamp': datetime_to_timestamp(edited_at),
            'embeds': [embed.to_data() for embed in embeds],
            'flags': int(flags),
            'mention_roles': [str(role_id) for role_id in mentioned_role_ids],
            'mentions': [user.to_data(include_internals = True) for user in mentioned_users],
            'soundboard_sounds': [
                soundboard_sound.to_data(include_internals = True) for soundboard_sound in soundboard_sounds
            ],
            'sticker_items': [create_partial_sticker_data(sticker) for sticker in stickers],
            'type': message_type.value,
        },
    }
    
    message_snapshot = MessageSnapshot.from_data(data)
    _assert_fields_set(message_snapshot)

    vampytest.assert_eq(message_snapshot.attachments, tuple(attachments))
    vampytest.assert_eq(message_snapshot.components, tuple(components))
    vampytest.assert_eq(message_snapshot.content, content)
    vampytest.assert_eq(message_snapshot.created_at, created_at)
    vampytest.assert_eq(message_snapshot.edited_at, edited_at)
    vampytest.assert_eq(message_snapshot.embeds, tuple(embeds))
    vampytest.assert_eq(message_snapshot.flags, flags)
    vampytest.assert_eq(message_snapshot.mentioned_role_ids, tuple(mentioned_role_ids))
    vampytest.assert_eq(message_snapshot.mentioned_users, tuple(mentioned_users))
    vampytest.assert_eq(message_snapshot.soundboard_sounds, tuple(soundboard_sounds))
    vampytest.assert_eq(message_snapshot.stickers, tuple(stickers))
    vampytest.assert_is(message_snapshot.type, message_type)


def test__MessageSnapshot__to_data():
    """
    Tests whether ``MessageSnapshot.to_data`` works as intended.
    
    Case: include defaults.
    """
    guild_id = 202407200053
    user_0 = User.precreate(202407200044, name = 'Kaenbyou')
    guild_profile_0 = GuildProfile(nick = 'orin')
    user_1 = User.precreate(202407200045, name = 'Rin')
    user_0.guild_profiles[guild_id] = guild_profile_0
    
    attachments = [
        Attachment.precreate(202405250004, name = 'Koishi'),
        Attachment.precreate(202405250005, name = 'Komeiji'),
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
    mentioned_role_ids = [202407200016, 202407200017]
    mentioned_users = [user_0, user_1]
    message_type = MessageType.call
    soundboard_sounds = [
        SoundboardSound.precreate(202501300012, name = 'whither'),
        SoundboardSound.precreate(202501300013, name = 'Yuyuko'),
    ]
    stickers = [
        Sticker.precreate(202409200064, name = 'Make'),
        Sticker.precreate(202409200065, name = 'Me'),
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
    
    vampytest.assert_eq(
        message_snapshot.to_data(defaults = True, guild_id = guild_id),
        {
            'message': {
                'attachments': [
                    attachment.to_data(defaults = True, include_internals = True)
                    for attachment in attachments
                ],
                'components': [component.to_data(defaults = True) for component in components],
                'content': content,
                'timestamp': datetime_to_timestamp(created_at),
                'edited_timestamp': datetime_to_timestamp(edited_at),
                'embeds': [embed.to_data(defaults = True) for embed in embeds],
                'flags': int(flags),
                'mention_roles': [str(role_id) for role_id in mentioned_role_ids],
                'mentions': [
                    {
                        **user_0.to_data(defaults = True, include_internals = True),
                        'member': guild_profile_0.to_data(defaults = True, include_internals = True),
                    },
                    user_1.to_data(defaults = True, include_internals = True),
                ],
                'soundboard_sounds': [
                    soundboard_sound.to_data(defaults = True, include_internals = True)
                    for soundboard_sound in soundboard_sounds
                ],
                'sticker_items': [create_partial_sticker_data(sticker) for sticker in stickers],
                'type': message_type.value,
            },
        }
    )
