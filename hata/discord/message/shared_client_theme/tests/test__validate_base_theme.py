import vampytest

from ..fields import validate_base_theme
from ..preinstanced import SharedClientThemeBaseTheme


def _iter_options__passing():
    yield (
        None,
        SharedClientThemeBaseTheme.none,
    )
    
    yield (
        SharedClientThemeBaseTheme.darker,
        SharedClientThemeBaseTheme.darker,
    )
    
    yield (
        SharedClientThemeBaseTheme.darker.value,
        SharedClientThemeBaseTheme.darker,
    )


def _iter_option__type_error():
    yield 12.6
    yield 'wakasagihime'


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_option__type_error()).raising(TypeError))
def test__validate_base_theme(input_value):
    """
    Tests whether ``validate_base_theme`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        Input value.
    
    Returns
    -------
    output : ``SharedClientThemeBaseTheme``
    
    Raises
    ------
    TypeError
    """
    output = validate_base_theme(input_value)
    vampytest.assert_instance(output, SharedClientThemeBaseTheme)
    return output
