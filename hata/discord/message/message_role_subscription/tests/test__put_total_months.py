import vampytest

from ..fields import put_total_months


def test__put_total_months():
    """
    Tests whether ``put_total_months`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (1, False, {'total_months_subscribed': 1}),
    ):
        data = put_total_months(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
