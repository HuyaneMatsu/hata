import vampytest

from ..fields import put_integration_id_into


def test__put_integration_id_into():
    """
    Tests whether ``put_integration_id_into`` works as intended.
    """
    integration_id = 202212160001
    
    for input_, defaults, expected_output in (
        (0, False, {}),
        (0, True, {'integration_id': None}),
        (integration_id, False, {'integration_id': str(integration_id)}),
    ):
        data = put_integration_id_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
