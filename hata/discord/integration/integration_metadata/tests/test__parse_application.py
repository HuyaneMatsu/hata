import vampytest

from ...integration_application import IntegrationApplication

from ..fields import parse_application


def test__parse_application():
    """
    Tests whether ``parse_application`` works as intended.
    """
    integration_application_id = 202210140018
    application = IntegrationApplication.precreate(integration_application_id, name = 'hell')
    
    for data, expected_output in (
        ({}, None),
        ({'application': None}, None),
        ({'application': application.to_data(defaults = True, include_internals = True)}, application),
    ):
        output = parse_application(data)
        vampytest.assert_eq(output, expected_output)
