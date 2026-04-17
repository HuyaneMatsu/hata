import vampytest

from ..fields import validate_sound_volume


def _iter_options__passing():
    yield None, 1.0
    yield 1.0, 1.0
    yield 0.0, 0.0
    yield 0.5, 0.5


def _iter_options__type_error():
    yield 'senya'


def _iter_options__value_error():
    yield -1.0
    yield +2.0


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_sound_volume(input_value):
    """
    Tests whether `validate_sound_volume` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `float`
    
    Raises
    ------
    TypeError
    """
    output = validate_sound_volume(input_value)
    vampytest.assert_instance(output, float)
    return output
