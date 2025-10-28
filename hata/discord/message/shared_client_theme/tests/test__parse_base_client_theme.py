import vampytest

from ..fields import parse_base_theme
from ..preinstanced import SharedClientThemeBaseTheme


def _iter_options():
    yield (
        {},
        SharedClientThemeBaseTheme.none,
    )
    
    yield (
        {
            'base_theme': SharedClientThemeBaseTheme.darker.value,
        },
        SharedClientThemeBaseTheme.darker,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_base_theme(input_data):
    """
    Tests whether ``parse_base_theme`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data.
    
    Returns
    -------
    output : ``SharedClientThemeBaseTheme``
    """
    output = parse_base_theme(input_data)
    vampytest.assert_instance(output, SharedClientThemeBaseTheme)
    return output
