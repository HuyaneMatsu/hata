import vampytest

from ...welcome_screen_channel import WelcomeScreenChannel

from ..welcome_screen import WelcomeScreen


def test__WelcomeScreen__repr():
    """
    Tests whether ``WelcomeScreen.__repr__`` works as intended.
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
    vampytest.assert_instance(repr(welcome_screen), str)


def test__WelcomeScreen__hash():
    """
    Tests whether ``WelcomeScreen.__hash__`` works as intended.
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
    vampytest.assert_instance(hash(welcome_screen), int)


def test__WelcomeScreen__eq():
    """
    Tests whether ``WelcomeScreen.__eq__`` works as intended.
    """
    description = 'Yukari'
    welcome_channels = [
        WelcomeScreenChannel(
            description = 'Koishi',
        ),
    ]
    
    keyword_parameters = {
        'description': description,
        'welcome_channels': welcome_channels,
    }
    
    welcome_screen = WelcomeScreen(**keyword_parameters)
    vampytest.assert_eq(welcome_screen, welcome_screen)
    vampytest.assert_ne(welcome_screen, object())
    
    for field_name, field_value in (
        ('description', 'Yurica'),
        ('welcome_channels', None),
    ):
        test_welcome_screen = WelcomeScreen(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(welcome_screen, test_welcome_screen)
