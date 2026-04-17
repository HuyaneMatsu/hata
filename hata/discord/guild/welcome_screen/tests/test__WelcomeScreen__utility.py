import vampytest

from ...welcome_screen_channel import WelcomeScreenChannel

from ..welcome_screen import WelcomeScreen

from .test__WelcomeScreen__constructor import _check_is_every_field_set


def test__WelcomeScreen__new__copy():
    """
    Tests whether ``WelcomeScreen.copy`` works as intended.
    """
    description = 'Yukari'
    welcome_channels = [
        WelcomeScreenChannel(
            description = 'Koishi',
        ),
    ]
    
    welcome_screen = WelcomeScreen(
        description = description,
        welcome_channels = welcome_channels,
    )
    copy = welcome_screen.copy()
    _check_is_every_field_set(copy)
    
    vampytest.assert_eq(welcome_screen, copy)
    vampytest.assert_is_not(welcome_screen, copy)


def test__WelcomeScreen__new__copy_with__0():
    """
    Tests whether ``WelcomeScreen.copy_with`` works as intended.
    
    Case: No fields given.
    """
    description = 'Yukari'
    welcome_channels = [
        WelcomeScreenChannel(
            description = 'Koishi',
        ),
    ]
    
    welcome_screen = WelcomeScreen(
        description = description,
        welcome_channels = welcome_channels,
    )
    copy = welcome_screen.copy_with()
    _check_is_every_field_set(copy)
    
    vampytest.assert_eq(welcome_screen, copy)
    vampytest.assert_is_not(welcome_screen, copy)


def test__WelcomeScreen__new__copy_with__1():
    """
    Tests whether ``WelcomeScreen.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_description = 'Yukari'
    new_description = 'Yurica'
    old_welcome_channels = [
        WelcomeScreenChannel(
            description = 'Koishi',
        ),
    ]
    new_welcome_channels = [
        WelcomeScreenChannel(
            description = 'Satori',
        ),
        WelcomeScreenChannel(
            description = 'Orin',
        ),
    ]
    
    welcome_screen = WelcomeScreen(
        description = old_description,
        welcome_channels = old_welcome_channels,
    )
    copy = welcome_screen.copy_with(
        description = new_description,
        welcome_channels = new_welcome_channels,
    )
    _check_is_every_field_set(copy)
    
    vampytest.assert_is_not(welcome_screen, copy)
    
    vampytest.assert_eq(copy.description, new_description)
    vampytest.assert_eq(copy.welcome_channels, tuple(new_welcome_channels))


def test__WelcomeScreen__iter_welcome_channels():
    """
    Asserts whether ``WelcomeScreen.iter_welcome_channels`` works as intended.
    """
    welcome_screen_channel_0 = WelcomeScreenChannel(
        description = 'Koishi',
    )
    
    welcome_screen_channel_1 = WelcomeScreenChannel(
        description = 'Satori',
    )
    
    for input_value, expected_output in (
        (None, []),
        ([welcome_screen_channel_0], [welcome_screen_channel_0]),
        (
            [welcome_screen_channel_0, welcome_screen_channel_1],
            [welcome_screen_channel_0, welcome_screen_channel_1],
        ),
    ):
        welcome_screen = WelcomeScreen(welcome_channels = input_value)
        vampytest.assert_eq(expected_output, [*welcome_screen.iter_welcome_channels()])
