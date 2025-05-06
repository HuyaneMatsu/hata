import vampytest

from ....channel import ChannelType

from ..fields import validate_channel_types


def _iter_options__passing():
    yield None, None
    yield [], None
    yield [ChannelType.private], (ChannelType.private,)
    yield [ChannelType.private.value], (ChannelType.private,)


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_channel_types(input_value):
    """
    Validates whether ``validate_channel_types`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : ``None | tuple<ChannelType>``
    
    Raises
    ------
    TypeError
    """
    output = validate_channel_types(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output
