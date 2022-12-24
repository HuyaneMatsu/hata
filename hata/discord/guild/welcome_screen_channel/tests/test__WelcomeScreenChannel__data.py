import vampytest

from ....core import BUILTIN_EMOJIS

from ..welcome_screen_channel import WelcomeScreenChannel

from .test__WelcomeScreenChannel__constructor import _check_is_every_field_set


def test__WelcomeScreenChannel__from_data():
    """
    Tests whether ``WelcomeScreenChannel.from_data`` works as intended.
    """
    channel_id = 202212230009
    description = 'Yukari'
    emoji = BUILTIN_EMOJIS['x']
    
    data = {
        'channel_id': str(channel_id),
        'description': description,
        'emoji_name': emoji.unicode,
    }
    
    welcome_screen_channel = WelcomeScreenChannel.from_data(data)
    _check_is_every_field_set(welcome_screen_channel)
    
    vampytest.assert_eq(welcome_screen_channel.channel_id, channel_id)
    vampytest.assert_eq(welcome_screen_channel.description, description)
    vampytest.assert_is(welcome_screen_channel.emoji, emoji)


def test__WelcomeScreenChannel__to_data():
    """
    Tests whether ``WelcomeScreenChannel.to_data`` works as intended.
    
    Case: include defaults.
    """
    channel_id = 202212230010
    description = 'Yukari'
    emoji = BUILTIN_EMOJIS['x']
    
    expected_data = {
        'channel_id': str(channel_id),
        'description': description,
        'emoji_name': emoji.unicode,
    }
    
    welcome_screen_channel = WelcomeScreenChannel(
        channel_id = channel_id,
        description = description,
        emoji = emoji,
    )
    
    vampytest.assert_eq(
        welcome_screen_channel.to_data(defaults = True),
        expected_data,
    )
