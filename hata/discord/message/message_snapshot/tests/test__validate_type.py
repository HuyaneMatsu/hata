import vampytest

from ...message.preinstanced import MessageType

from ..fields import validate_type


def _iter_options__passing():
    yield None, MessageType.default
    yield MessageType.call.value, MessageType.call
    yield MessageType.call, MessageType.call


def _iter_options__type_error():
    yield 'a'
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_type(input_value):
    """
    Tests whether `validate_type` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    value : ``MessageType``
    
    Raises
    ------
    TypeError
    """
    output = validate_type(input_value)
    vampytest.assert_instance(output, MessageType)
    return output
