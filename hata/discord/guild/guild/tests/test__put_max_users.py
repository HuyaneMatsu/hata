import vampytest

from ..fields import put_max_users


def test__put_max_users():
    """
    Tests whether ``put_max_users`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (0, False, {'max_members': 0}),
        (0, True, {'max_members': 0}),
        (1, False, {'max_members': 1}),
        (1, True, {'max_members': 1}),
    ):
        data = put_max_users(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
