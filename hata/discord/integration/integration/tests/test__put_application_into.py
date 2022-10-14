import vampytest

from ...integration_application import IntegrationApplication

from ..fields import put_application_into


def test__put_application_into():
    """
    Tests whether ``put_application_into`` works as intended.
    """
    integration_application_id = 202210140019
    application = IntegrationApplication.precreate(integration_application_id, name = 'hell')
    
    for input_value, expected_output in (
        (application, {'application': application.to_data(defaults = True)}),
    ):
        data = put_application_into(input_value, {}, True)
        vampytest.assert_eq(data, expected_output)
