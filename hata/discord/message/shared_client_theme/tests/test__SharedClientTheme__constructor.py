import vampytest

from ....color import Color

from ..preinstanced import SharedClientThemeBaseTheme
from ..shared_client_theme import SharedClientTheme


def _assert_fields_set(shared_client_theme):
    """
    Asserts whether every fields of the given instance are set correctly.
    
    Parameters
    ----------
    shared_client_theme : ``SharedClientTheme``
        The instance to check.
    """
    vampytest.assert_instance(shared_client_theme, SharedClientTheme)
    vampytest.assert_instance(shared_client_theme.base_theme, SharedClientThemeBaseTheme)
    vampytest.assert_instance(shared_client_theme.colors, tuple, nullable = True)
    vampytest.assert_instance(shared_client_theme.gradient_angle, int)
    vampytest.assert_instance(shared_client_theme.intensity, int)


def test__SharedClientTheme__new__no_fields():
    """
    Tests whether ``SharedClientTheme.__new__`` works as intended.
    
    Case: no fields given.
    """
    shared_client_theme = SharedClientTheme()
    _assert_fields_set(shared_client_theme)


def test__SharedClientTheme__new__all_fields():
    """
    Tests whether ``SharedClientTheme.__new__`` works as intended.
    
    Case: all fields given.
    """
    base_theme = SharedClientThemeBaseTheme.darker
    colors = [Color(12333), Color(15566)]
    gradient_angle = 5
    intensity = 2
    
    shared_client_theme = SharedClientTheme(
        base_theme = base_theme,
        colors = colors,
        gradient_angle = gradient_angle,
        intensity = intensity,
    )
    _assert_fields_set(shared_client_theme)
    
    vampytest.assert_is(shared_client_theme.base_theme, base_theme)
    vampytest.assert_eq(shared_client_theme.colors, tuple(colors))
    vampytest.assert_eq(shared_client_theme.gradient_angle, gradient_angle)
    vampytest.assert_eq(shared_client_theme.intensity, intensity)
