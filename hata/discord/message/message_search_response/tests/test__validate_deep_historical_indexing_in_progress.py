import vampytest

from ..fields import validate_deep_historical_indexing_in_progress


def _iter_options__passing():
    yield True, True
    yield False, False
    yield None, False


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_deep_historical_indexing_in_progress(input_value):
    """
    Tests whether `validate_deep_historical_indexing_in_progress` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `bool`
    
    Raises
    ------
    TypeError
    """
    output = validate_deep_historical_indexing_in_progress(input_value)
    vampytest.assert_instance(output, bool)
    return output
