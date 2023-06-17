import vampytest

from ..fields import put_id_into


def test__put_id_into():
    """
    Tests whether ``put_id_into`` works as intended.
    """
    role_id = 202306150012
    
    for input_value, defaults, expected_output in (
        (0, False, {'id': None}),
        (0, True, {'id': None}),
        (role_id, False, {'id': str(role_id)}),
    ):
        data = put_id_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
