import vampytest

from ....soundboard import SoundboardSound

from ..fields import validate_sound_id


def _iter_options__passing():
    sound_id = 202408180002
    
    yield None, 0
    yield 0, 0
    yield sound_id, sound_id
    yield SoundboardSound.precreate(sound_id), sound_id
    yield str(sound_id), sound_id


def _iter_options__type_error():
    yield 12.6


def _iter_options__value_error():
    yield '-1'
    yield '1111111111111111111111'
    yield -1
    yield 1111111111111111111111


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_sound_id(input_value):
    """
    Tests whether `validate_sound_id` works as intended.
    
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
    output = validate_sound_id(input_value)
    vampytest.assert_instance(output, int)
    return output