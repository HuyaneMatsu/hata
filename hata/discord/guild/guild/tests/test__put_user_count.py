import vampytest

from ..fields import put_user_count


def test__put_user_count():
    """
    Tests whether ``put_user_count`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (0, False, {'member_count': 0}),
    ):
        data = put_user_count(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
