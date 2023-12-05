import vampytest

from ..fields import validate_approximate_guild_count


def _iter_options__passing():
    yield 0, 0
    yield 1, 1


def _iter_options__type_error():
    yield 12.6
    yield '12'


def _iter_options__value_error():
    yield -1


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_approximate_guild_count(input_value):
    """
    Tests whether `validate_approximate_guild_count` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to validate.
    
    Returns
    -------
    output : `int`
    
    Raises
    ------
    TypeError
    ValueError
    """
    return validate_approximate_guild_count(input_value)
