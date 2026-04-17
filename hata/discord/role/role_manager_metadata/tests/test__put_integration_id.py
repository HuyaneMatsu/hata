import vampytest

from ..fields import put_integration_id


def test__put_integration_id():
    """
    Tests whether ``put_integration_id`` works as intended.
    """
    integration_id = 202212160001
    
    for input_value, defaults, expected_output in (
        (0, False, {}),
        (0, True, {'integration_id': None}),
        (integration_id, False, {'integration_id': str(integration_id)}),
    ):
        data = put_integration_id(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
