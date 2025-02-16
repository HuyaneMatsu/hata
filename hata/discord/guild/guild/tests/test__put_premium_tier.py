import vampytest

from ..fields import put_premium_tier


def test__put_premium_tier():
    """
    Tests whether ``put_premium_tier`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (0, False, {'premium_tier': 0}),
    ):
        data = put_premium_tier(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
