import vampytest

from ....core import BUILTIN_EMOJIS

from ..welcome_screen_channel import WelcomeScreenChannel


def test__WelcomeScreenChannel__repr():
    """
    Tests whether ``WelcomeScreenChannel.__repr__`` works as intended.
    """
    channel_id = 202212230011
    description = 'Yukari'
    emoji = BUILTIN_EMOJIS['x']
    
    welcome_screen_channel = WelcomeScreenChannel(
        channel_id = channel_id,
        description = description,
        emoji = emoji,
    )
    vampytest.assert_instance(repr(welcome_screen_channel), str)


def test__WelcomeScreenChannel__hash():
    """
    Tests whether ``WelcomeScreenChannel.__hash__`` works as intended.
    """
    channel_id = 202212230012
    description = 'Yukari'
    emoji = BUILTIN_EMOJIS['x']
    
    welcome_screen_channel = WelcomeScreenChannel(
        channel_id = channel_id,
        description = description,
        emoji = emoji,
    )
    vampytest.assert_instance(hash(welcome_screen_channel), int)


def test__WelcomeScreenChannel__eq():
    """
    Tests whether ``WelcomeScreenChannel.__eq__`` works as intended.
    """
    channel_id = 202212230013
    description = 'Yukari'
    emoji = BUILTIN_EMOJIS['x']
    
    keyword_parameters = {
        'channel_id': channel_id,
        'description': description,
        'emoji': emoji,
    }
    
    welcome_screen_channel = WelcomeScreenChannel(**keyword_parameters)
    vampytest.assert_eq(welcome_screen_channel, welcome_screen_channel)
    vampytest.assert_ne(welcome_screen_channel, object())
    
    for field_name, field_value in (
        ('channel_id', 202212230014),
        ('description', 'Yurica'),
        ('emoji', BUILTIN_EMOJIS['heart']),
    ):
        test_welcome_screen_channel = WelcomeScreenChannel(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(welcome_screen_channel, test_welcome_screen_channel)
