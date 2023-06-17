import vampytest

from ..fields import put_approximate_user_count_into


def test__put_approximate_user_count_into():
    """
    Tests whether ``put_approximate_user_count_into`` works as intended.
    """
    for input_, defaults, expected_output in (
        (0, False, {'approximate_member_count': 0}),
    ):
        data = put_approximate_user_count_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
