import vampytest

from ....message import Attachment

from ..fields import validate_attachment_id


def _iter_options__passing():
    attachment_id = 202509200003
    
    yield None, 0
    yield 0, 0
    yield attachment_id, attachment_id
    yield Attachment.precreate(attachment_id), attachment_id
    yield str(attachment_id), attachment_id


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
def test__validate_attachment_id(input_value):
    """
    Tests whether `validate_attachment_id` works as intended.
    
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
    output = validate_attachment_id(input_value)
    vampytest.assert_instance(output, int)
    return output
