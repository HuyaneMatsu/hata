import vampytest

from ....integration import Integration

from ..fields import put_integrations_into


def test__put_integrations_into():
    """
    Tests whether ``put_integrations_into`` works as intended.
    
    Case: include internals.
    """
    integration = Integration.precreate(202210070000, name = 'ExistRuth')
    
    for input_value, defaults, expected_output in (
        (None, False, {'integrations': []}),
        (None, True, {'integrations': []}),
        ([integration], False, {'integrations': [integration.to_data(include_internals = True)]}),
    ):
        data = put_integrations_into(input_value, {}, defaults, include_internals = True)
        vampytest.assert_eq(data, expected_output)
