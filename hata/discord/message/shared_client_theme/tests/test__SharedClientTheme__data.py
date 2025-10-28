import vampytest

from ....color import Color

from ..preinstanced import SharedClientThemeBaseTheme
from ..shared_client_theme import SharedClientTheme

from .test__SharedClientTheme__constructor import _assert_fields_set


def test__SharedClientTheme__from_data():
    """
    Tests whether ``SharedClientTheme.__new__`` works as intended.
    """
    base_theme = SharedClientThemeBaseTheme.darker
    colors = [Color(12333), Color(15566)]
    gradient_angle = 5
    intensity = 2
    
    data = {
        'base_theme': base_theme.value,
        'colors': [format(color, 'X') for color in colors],
        'gradient_angle': gradient_angle,
        'base_mix': intensity,
    }
    
    shared_client_theme = SharedClientTheme.from_data(data)
    
    _assert_fields_set(shared_client_theme)
    
    vampytest.assert_is(shared_client_theme.base_theme, base_theme)
    vampytest.assert_eq(shared_client_theme.colors, tuple(colors))
    vampytest.assert_eq(shared_client_theme.gradient_angle, gradient_angle)
    vampytest.assert_eq(shared_client_theme.intensity, intensity)


def test__SharedClientTheme__to_data():
    """
    Tests whether ``SharedClientTheme.__new__`` works as intended.
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
    
    vampytest.assert_eq(
        shared_client_theme.to_data(defaults = True),{
            'base_theme': base_theme.value,
            'colors': [format(color, 'X') for color in colors],
            'gradient_angle': gradient_angle,
            'base_mix': intensity,
        },
    )
