import vampytest

from ..fields import validate_waveform


def _iter_options__passing():
    yield (
        None,
        None,
    )
    
    yield (
        b'',
        None,
    )
    
    yield (
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    )


def _iter_options__type_error():
    yield 12.6



@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_waveform(input_value):
    """
    Tests whether `validate_waveform` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `None | bytes`
    
    Raises
    ------
    TypeError
    ValueError
    """
    output = validate_waveform(input_value)
    vampytest.assert_instance(output, bytes, nullable = True)
    return output
