import vampytest

from ....channel import Channel

from ..fields import validate_channel_id


def _iter_options__passing():
    channel_id = 202211130000
    
    yield None, 0
    yield 0, 0
    yield channel_id, channel_id
    yield Channel.precreate(channel_id), channel_id
    yield str(channel_id), channel_id


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
def test__validate_channel_id(input_value):
    """
    Tests whether `validate_channel_id` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `int`
    
    Raises
    ------
    TypeError
    ValueError
    """
    output = validate_channel_id(input_value)
    vampytest.assert_instance(output, int)
    return output
