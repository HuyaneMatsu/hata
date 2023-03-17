import vampytest

from ..fields import put_user_count_into


def test__put_user_count_into():
    """
    Tests whether ``put_user_count_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (0, False, {'user_count': 0}),
    ):
        data = put_user_count_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
