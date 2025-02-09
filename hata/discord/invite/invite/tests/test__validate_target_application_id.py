import vampytest

from ....application import Application

from ..fields import validate_target_application_id


def _iter_options__passing():
    application_id = 202309200000
    application = Application.precreate(application_id)
    
    yield application_id, application_id
    yield application, application_id
    yield 0, 0


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_target_application_id(input_value):
    """
    Tests whether `validate_target_application_id` works as intended.
    
    Case: passing.
    
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
    """
    output = validate_target_application_id(input_value)
    vampytest.assert_instance(output, int)
    return output
