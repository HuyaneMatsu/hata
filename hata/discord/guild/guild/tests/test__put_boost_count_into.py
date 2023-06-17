import vampytest

from ..fields import put_boost_count_into


def test__put_boost_count_into():
    """
    Tests whether ``put_boost_count_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (0, False, {}),
        (0, True, {'premium_subscription_count': 0}),
        (1, False, {'premium_subscription_count': 1}),
    ):
        data = put_boost_count_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
