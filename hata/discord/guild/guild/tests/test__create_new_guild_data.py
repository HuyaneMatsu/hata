import vampytest

from ....channel import Channel, ChannelType
from ....role import Role

from ..flags import SystemChannelFlag
from ..preinstanced import ContentFilterLevel, VerificationLevel
from ..utils import MessageNotificationLevel, create_new_guild_data


def test__create_new_guild_data__0():
    """
    Tests whether ``create_new_guild_data`` works as intended.
    
    Case: No fields given.
    """
    expected_output = {
        'name': '',
        'afk_channel_id': None,
        'afk_timeout': 0,
        'channels': [],
        'explicit_content_filter': 0,
        'icon': None,
        'roles': [],
        'default_message_notifications': 0,
        'system_channel_id': None,
        'system_channel_flags': 63,
        'verification_level': 0,
    }
    
    data = create_new_guild_data()
    
    vampytest.assert_eq(data, expected_output)


def test__create_new_guild_data__1():
    """
    Tests whether ``create_new_guild_data`` works as intended.
    
    Case: All fields given.
    """
    name = 'Koishi'
    afk_channel_id = 202306090004
    afk_timeout = 3600
    channels = [Channel.precreate(202306090005, channel_type = ChannelType.guild_text, name = 'orin')]
    content_filter = ContentFilterLevel.no_role
    icon = b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0Aayaya'
    roles = [Role.precreate(202306090006, name = 'okuu')]
    message_notification = MessageNotificationLevel.none
    system_channel_id = 202306090007
    system_channel_flags = SystemChannelFlag(12)
    verification_level = VerificationLevel.extreme
    
    expected_output = {
        'name': name,
        'afk_channel_id': str(afk_channel_id),
        'afk_timeout': afk_timeout,
        'channels': [channel.to_data(defaults = True, include_internals = True) for channel in channels],
        'explicit_content_filter': content_filter.value,
        'icon': 'data:image/png;base64,iVBORw0KGgpheWF5YQ==',
        'roles': [role.to_data(defaults = True, include_internals = True) for role in roles],
        'default_message_notifications': message_notification.value,
        'system_channel_id': str(system_channel_id),
        'system_channel_flags': int(system_channel_flags),
        'verification_level': verification_level.value,
    }
    
    data = create_new_guild_data(
        name = name,
        afk_channel_id = afk_channel_id,
        afk_timeout = afk_timeout,
        channels = channels,
        content_filter = content_filter,
        icon = icon,
        roles = roles,
        message_notification = message_notification,
        system_channel_flags = system_channel_flags,
        system_channel_id = system_channel_id,
        verification_level = verification_level,
    )
    
    vampytest.assert_eq(data, expected_output)
