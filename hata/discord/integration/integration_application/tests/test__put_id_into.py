import vampytest

from ..fields import put_id_into


def test__put_id_into():
    """
    Tests whether ``put_id_into`` works as intended.
    """
    integration_application_id = 202212170046
    
    for input_value, defaults, expected_output in (
        (integration_application_id, False, {'id': str(integration_application_id)}),
    ):
        data = put_id_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
