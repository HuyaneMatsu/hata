import vampytest

from ...integration_application import IntegrationApplication

from ..fields import validate_application


def _iter_options__passing():
    application_id = 202210140020
    application = IntegrationApplication.precreate(application_id, name = 'hell')
    
    yield None, None
    yield application, application


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_application(input_value):
    """
    Tests whether ``validate_application`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | IntegrationApplication`
    
    Raises
    ------
    TypeError
    """
    output = validate_application(input_value)
    vampytest.assert_instance(output, IntegrationApplication, nullable = True)
    return output
