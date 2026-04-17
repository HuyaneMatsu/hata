import vampytest

from ...welcome_screen_channel import WelcomeScreenChannel

from ..welcome_screen import WelcomeScreen


def _check_is_every_field_set(welcome_screen):
    """
    Asserts whether all fields are set of the given welcome screen.
    
    Parameters
    ----------
    welcome_screen : ``WelcomeScreen``
        The guild welcome screen instance to check.
    """
    vampytest.assert_instance(welcome_screen, WelcomeScreen)
    vampytest.assert_instance(welcome_screen.description, str, nullable = True)
    vampytest.assert_instance(welcome_screen.welcome_channels, tuple, nullable = True)



def test__WelcomeScreen__new__0():
    """
    Tests whether ``WelcomeScreen.__new__`` works as intended.
    
    Case: No fields given.
    """
    welcome_screen = WelcomeScreen()
    _check_is_every_field_set(welcome_screen)


def test__WelcomeScreen__new__1():
    """
    Tests whether ``WelcomeScreen.__new__`` works as intended.
    
    Case: All fields given.
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
    _check_is_every_field_set(welcome_screen)
    
    vampytest.assert_eq(welcome_screen.description, description)
    vampytest.assert_eq(welcome_screen.welcome_channels, tuple(welcome_channels))
