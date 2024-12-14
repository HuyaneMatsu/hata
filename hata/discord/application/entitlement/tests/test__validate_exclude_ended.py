import vampytest

from ..fields import validate_exclude_ended


def _iter_options__passing():
    yield None, False
    yield True, True
    yield False, False


def _ter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_ter_options__type_error()).raising(TypeError))
def test__validate_exclude_ended(input_value):
    """
    Tests whether `validate_exclude_ended` works as intended.
    
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
    return validate_exclude_ended(input_value)
