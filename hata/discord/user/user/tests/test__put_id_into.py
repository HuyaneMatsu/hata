import vampytest

from ..fields import put_id_into


def test__put_id_into():
    """
    Tests whether ``put_id_into`` works as intended.
    """
    user_id = 202301270001
    
    for input_value, defaults, expected_output in (
        (user_id, False, {'id': str(user_id)}),
    ):
        data = put_id_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
