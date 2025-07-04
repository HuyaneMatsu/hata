import vampytest

from ..fields import validate_asset_path


def _iter_options__passing():
    yield None, ''
    yield '', ''
    yield 'nameplates/nameplates/cityscape/', 'nameplates/nameplates/cityscape/'


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_asset_path(input_value):
    """
    Tests whether `validate_asset_path` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `str`
    
    Raises
    ------
    ValueError
    """
    return validate_asset_path(input_value)
