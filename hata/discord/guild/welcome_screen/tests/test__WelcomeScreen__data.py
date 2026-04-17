import vampytest

from ...welcome_screen_channel import WelcomeScreenChannel

from ..welcome_screen import WelcomeScreen

from .test__WelcomeScreen__constructor import _check_is_every_field_set


def test__WelcomeScreen__from_data():
    """
    Tests whether ``WelcomeScreen.from_data`` works as intended.
    """
    description = 'Yukari'
    welcome_channels = [
        WelcomeScreenChannel(
            description = 'Koishi'
        ),
    ]
    
    data = {
        'description': description,
        'welcome_channels': [step.to_data(defaults = True) for step in welcome_channels],
    }
    
    welcome_screen = WelcomeScreen.from_data(data)
    _check_is_every_field_set(welcome_screen)
    
    vampytest.assert_eq(welcome_screen.description, description)
    vampytest.assert_eq(welcome_screen.welcome_channels, tuple(welcome_channels))


def test__WelcomeScreen__to_data():
    """
    Tests whether ``WelcomeScreen.to_data`` works as intended.
    
    Case: include defaults.
    """
    description = 'Yukari'
    welcome_channels = [
        WelcomeScreenChannel(
            description = 'Koishi'
        ),
    ]
    
    expected_data = {
        'description': description,
        'welcome_channels': [step.to_data(defaults = True) for step in welcome_channels],
    }
    
    welcome_screen = WelcomeScreen(
        description = description,
        welcome_channels = welcome_channels,
    )
    
    vampytest.assert_eq(
        welcome_screen.to_data(defaults = True),
        expected_data,
    )
