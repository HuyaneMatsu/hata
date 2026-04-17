import vampytest

from ....color import Color

from ..preinstanced import SharedClientThemeBaseTheme
from ..shared_client_theme import SharedClientTheme

from .test__SharedClientTheme__constructor import _assert_fields_set


def test__SharedClientTheme__copy():
    """
    Tests whether ``SharedClientTheme.copy`` works as intended.
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
    
    copy = shared_client_theme.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, shared_client_theme)
    vampytest.assert_eq(copy, shared_client_theme)


def test__SharedClientTheme__copy_with__no_fields():
    """
    Tests whether ``SharedClientTheme.copy_with`` works as intended.
    
    Case: No fields given.
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
    
    copy = shared_client_theme.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, shared_client_theme)
    vampytest.assert_eq(copy, shared_client_theme)


def test__SharedClientTheme__copy_with__all_fields():
    """
    Tests whether ``SharedClientTheme.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_base_theme = SharedClientThemeBaseTheme.darker
    old_colors = [Color(12333), Color(15566)]
    old_gradient_angle = 5
    old_intensity = 2
    
    new_base_theme = SharedClientThemeBaseTheme.light
    new_colors = [Color(12333), Color(111)]
    new_gradient_angle = 6
    new_intensity = 3
    
    shared_client_theme = SharedClientTheme(
        base_theme = old_base_theme,
        colors = old_colors,
        gradient_angle = old_gradient_angle,
        intensity = old_intensity,
    )
    
    copy = shared_client_theme.copy_with(
        base_theme = new_base_theme,
        colors = new_colors,
        gradient_angle = new_gradient_angle,
        intensity = new_intensity,
        
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, shared_client_theme)
    
    vampytest.assert_is(copy.base_theme, new_base_theme)
    vampytest.assert_eq(copy.colors, tuple(new_colors))
    vampytest.assert_eq(copy.gradient_angle, new_gradient_angle)
    vampytest.assert_eq(copy.intensity, new_intensity)
