import vampytest

from ....integration import Integration

from ..fields import parse_integrations


def test__parse_integrations():
    """
    Tests whether ``parse_integrations`` works as intended.
    """
    integration = Integration.precreate(202210070001, name = 'ExistRuth')
    
    for input_data, expected_output in (
        ({}, None),
        ({'integrations': None}, None),
        ({'integrations': []}, None),
        ({'integrations': [integration.to_data(include_internals = True)]}, (integration, ))
    ):
        output = parse_integrations(input_data)
        
        vampytest.assert_eq(output, expected_output)
