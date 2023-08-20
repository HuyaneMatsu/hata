import vampytest

from ....application import Application

from ..fields import validate_target_application_id


def _iter_options():
    application_id = 202309200000
    application = Application.precreate(application_id)
    
    yield application_id, application_id
    yield application, application_id
    yield 0, 0


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_target_application_id__passing(input_value):
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
    """
    return validate_target_application_id(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
def test__validate_target_application_id__type_error(input_value):
    """
    Tests whether `validate_target_application_id` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Raises
    ------
    TypeError
    """
    validate_target_application_id(input_value)
