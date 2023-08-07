import vampytest

from ..fields import put_id_into


def test__put_id_into():
    """
    Tests whether ``put_id_into`` works as intended.
    """
    integration_id = 202307310013
    
    for input_value, defaults, expected_output in (
        (integration_id, False, {'id': str(integration_id)}),
    ):
        data = put_id_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
