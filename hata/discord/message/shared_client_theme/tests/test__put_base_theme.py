import vampytest

from ..fields import put_base_theme
from ..preinstanced import SharedClientThemeBaseTheme


def _iter_options():
    yield (
        SharedClientThemeBaseTheme.none,
        False,
        {
            'base_theme': SharedClientThemeBaseTheme.none.value,
        },
    )
    
    yield (
        SharedClientThemeBaseTheme.none,
        True,
        {
            'base_theme': SharedClientThemeBaseTheme.none.value
        },
    )
    
    yield (
        SharedClientThemeBaseTheme.darker,
        False,
        {
            'base_theme': SharedClientThemeBaseTheme.darker.value,
        },
    )
    
    yield (
        SharedClientThemeBaseTheme.darker,
        True,
        {
            'base_theme': SharedClientThemeBaseTheme.darker.value
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_base_theme(input_value, defaults):
    """
    Tests whether ``put_base_theme`` is working as intended.
    
    Parameters
    ----------
    input_value : ``SharedClientThemeBaseTheme``
        Input value.
    
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_base_theme(input_value, {}, defaults)
