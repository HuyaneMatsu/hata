import vampytest

from ...shared_client_theme import SharedClientTheme

from ..fields import validate_shared_client_theme


def _iter_options__passing():
    shared_client_theme = SharedClientTheme(
        intensity = 6,
    )
    
    yield (
        None,
        None,
    )
    
    yield (
        shared_client_theme,
        shared_client_theme,
    )


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_shared_client_theme(input_value):
    """
    Tests whether ``validate_shared_client_theme`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : ``None | SharedClientTheme``
    
    Raises
    ------
    TypeError
    """
    output = validate_shared_client_theme(input_value)
    vampytest.assert_instance(output, SharedClientTheme, nullable = True)
    return output
