import vampytest

from ....application import Application

from ..fields import validate_application


def _iter_options__passing():
    application_id = 202502010002
    application = Application.precreate(application_id)
    yield application, application
    yield None, None


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_application(input_value):
    """
    Tests whether `validate_application` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `None | Application`
        The application to validate.
    
    Returns
    -------
    output : `None | Application`
    
    Raises
    ------
    TypeError
    """
    output = validate_application(input_value)
    vampytest.assert_instance(output, Application, nullable = True)
    return output
