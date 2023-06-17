import vampytest

from ..fields import put_max_users_into


def test__put_max_users_into():
    """
    Tests whether ``put_max_users_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (0, False, {'max_members': 0}),
        (0, True, {'max_members': 0}),
        (1, False, {'max_members': 1}),
        (1, True, {'max_members': 1}),
    ):
        data = put_max_users_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
