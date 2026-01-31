import vampytest

from ....channel import Channel

from ..fields import validate_channel_ids


def _iter_options__passing():
    channel_id_0 = 202303030003
    channel_id_1 = 202303030004
    
    channel_0 = Channel.precreate(channel_id_0)
    channel_1 = Channel.precreate(channel_id_1)
    
    yield None, None
    yield [], None
    yield [channel_id_0, channel_id_1], (channel_id_0, channel_id_1)
    yield [channel_id_1, channel_id_0], (channel_id_0, channel_id_1)
    yield [channel_0, channel_1], (channel_id_0, channel_id_1)
    yield [channel_1, channel_0], (channel_id_0, channel_id_1)


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_channel_ids(input_value):
    """
    Tests whether `validate_channel_ids` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | tuple<int>`
    
    Raises
    ------
    TypeError
    """
    output = validate_channel_ids(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, int)
    
    return output
