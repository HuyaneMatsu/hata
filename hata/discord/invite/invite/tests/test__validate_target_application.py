import vampytest

from ....application import Application

from ..fields import validate_target_application


def _iter_options():
    application_id = 202308030002
    application = Application.precreate(application_id)
    yield application, application
    yield None, None


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_target_application__passing(input_value):
    """
    Tests whether `validate_target_application` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `None`, ``Application``
        The application to validate.
    
    Returns
    -------
    output : `None`, ``Application``
    """
    return validate_target_application(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
def test__validate_target_application__type_error(input_value):
    """
    Tests whether `validate_target_application` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        Value to pass.
    
    Raises
    ------
    TypeError
    """
    validate_target_application(input_value)
