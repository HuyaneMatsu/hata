import vampytest

from ....color import Color

from ..preinstanced import SharedClientThemeBaseTheme
from ..shared_client_theme import SharedClientTheme


def test__SharedClientTheme__repr():
    """
    Tests whether ``SharedClientTheme.__repr__`` works as intended.
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
    
    output = repr(shared_client_theme)
    vampytest.assert_instance(output, str)


def test__SharedClientTheme__hash():
    """
    Tests whether ``SharedClientTheme.__repr__`` works as intended.
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
    
    output = hash(shared_client_theme)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    base_theme = SharedClientThemeBaseTheme.darker
    colors = [Color(12333), Color(15566)]
    gradient_angle = 5
    intensity = 2
    
    keyword_parameters = {
        'base_theme': base_theme,
        'colors': colors,
        'gradient_angle': gradient_angle,
        'intensity': intensity,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'base_theme': SharedClientThemeBaseTheme.light,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'colors': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'gradient_angle': 7,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'intensity': 8,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__SharedClientTheme__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``SharedClientTheme.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    shared_client_theme_0 = SharedClientTheme(**keyword_parameters_0)
    shared_client_theme_1 = SharedClientTheme(**keyword_parameters_1)
    
    output = shared_client_theme_0 == shared_client_theme_1
    vampytest.assert_instance(output, bool)
    return output
