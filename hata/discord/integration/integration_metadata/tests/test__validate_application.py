import vampytest

from ...integration_application import IntegrationApplication

from ..fields import validate_application


def test__validate_application__0():
    """
    Tests whether ``validate_application`` works as intended.
    
    Case: Passing.
    """
    integration_application_id = 202210140020
    application = IntegrationApplication.precreate(integration_application_id, name = 'hell')
    
    for input_value, expected_output in (
        (None, None),
        (application, application),
    ):
        output = validate_application(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_application__1():
    """
    Tests whether ``validate_application`` works as intended.
    
    Case: `TypeError`
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_application(input_value)
