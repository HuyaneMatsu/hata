import vampytest

from ....core import BUILTIN_EMOJIS
from ....emoji import Emoji

from ..welcome_screen_channel import WelcomeScreenChannel


def _check_is_every_field_set(welcome_screen_channel):
    """
    Asserts whether all fields are set of the given welcome screen channel.
    
    Parameters
    ----------
    welcome_screen_channel : ``WelcomeScreenChannel``
        The welcome screen channel instance to check.
    """
    vampytest.assert_instance(welcome_screen_channel, WelcomeScreenChannel)
    vampytest.assert_instance(welcome_screen_channel.channel_id, int)
    vampytest.assert_instance(welcome_screen_channel.description, str, nullable = True)
    vampytest.assert_instance(welcome_screen_channel.emoji, Emoji, nullable = True)



def test__WelcomeScreenChannel__new__0():
    """
    Tests whether ``WelcomeScreenChannel.__new__`` works as intended.
    
    Case: No fields given.
    """
    welcome_screen_channel = WelcomeScreenChannel()
    _check_is_every_field_set(welcome_screen_channel)


def test__WelcomeScreenChannel__new__1():
    """
    Tests whether ``WelcomeScreenChannel.__new__`` works as intended.
    
    Case: All fields given.
    """
    channel_id = 202212230008
    description = 'Yukari'
    emoji = BUILTIN_EMOJIS['x']
    
    welcome_screen_channel = WelcomeScreenChannel(
        channel_id = channel_id,
        description = description,
        emoji = emoji,
    )
    _check_is_every_field_set(welcome_screen_channel)
    
    vampytest.assert_eq(welcome_screen_channel.channel_id, channel_id)
    vampytest.assert_eq(welcome_screen_channel.description, description)
    vampytest.assert_is(welcome_screen_channel.emoji, emoji)
