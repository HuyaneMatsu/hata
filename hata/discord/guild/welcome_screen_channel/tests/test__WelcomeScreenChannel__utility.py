import vampytest

from ....channel import Channel
from ....core import BUILTIN_EMOJIS

from ..welcome_screen_channel import WelcomeScreenChannel

from .test__WelcomeScreenChannel__constructor import _check_is_every_field_set


def test__WelcomeScreenChannel__new__copy():
    """
    Tests whether ``WelcomeScreenChannel.copy`` works as intended.
    """
    channel_id = 202212230015
    description = 'Yukari'
    emoji = BUILTIN_EMOJIS['x']
    
    welcome_screen_channel = WelcomeScreenChannel(
        channel_id = channel_id,
        description = description,
        emoji = emoji,
    )
    copy = welcome_screen_channel.copy()
    _check_is_every_field_set(copy)
    
    vampytest.assert_eq(welcome_screen_channel, copy)
    vampytest.assert_is_not(welcome_screen_channel, copy)


def test__WelcomeScreenChannel__new__copy_with__0():
    """
    Tests whether ``WelcomeScreenChannel.copy_with`` works as intended.
    
    Case: No fields given.
    """
    channel_id = 202212230016
    description = 'Yukari'
    emoji = BUILTIN_EMOJIS['x']
    
    welcome_screen_channel = WelcomeScreenChannel(
        channel_id = channel_id,
        description = description,
        emoji = emoji,
    )
    copy = welcome_screen_channel.copy_with()
    _check_is_every_field_set(copy)
    
    vampytest.assert_eq(welcome_screen_channel, copy)
    vampytest.assert_is_not(welcome_screen_channel, copy)


def test__WelcomeScreenChannel__new__copy_with__1():
    """
    Tests whether ``WelcomeScreenChannel.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_channel_id = 202212230017
    new_channel_id = 202212230018
    old_description = 'Yukari'
    new_description = 'Yurica'
    old_emoji = BUILTIN_EMOJIS['x']
    new_emoji = BUILTIN_EMOJIS['heart']
    
    welcome_screen_channel = WelcomeScreenChannel(
        channel_id = old_channel_id,
        description = old_description,
        emoji = old_emoji,
    )
    copy = welcome_screen_channel.copy_with(
        channel_id = new_channel_id,
        description = new_description,
        emoji = new_emoji,
    )
    _check_is_every_field_set(copy)
    
    vampytest.assert_is_not(welcome_screen_channel, copy)
    
    vampytest.assert_eq(copy.channel_id, new_channel_id)
    vampytest.assert_eq(copy.description, new_description)
    vampytest.assert_is(copy.emoji, new_emoji)


def test__WelcomeScreenChannel__channel():
    """
    Tests whether ``WelcomeScreenChannel.channel`` works as intended.
    """
    channel_id = 202212230018
    channel = Channel.precreate(channel_id)
    
    welcome_screen_channel = WelcomeScreenChannel(
        channel_id = channel_id,
    )
    
    vampytest.assert_is(welcome_screen_channel.channel, channel)
