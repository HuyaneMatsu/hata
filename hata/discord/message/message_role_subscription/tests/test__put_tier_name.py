import vampytest

from ..fields import put_tier_name


def test__put_tier_name():
    """
    Tests whether ``put_tier_name`` works as intended.
    """
    for input_value, defaults, expected_output in (
        ('', False, {'tier_name': ''}),
        ('a', False, {'tier_name': 'a'}),
    ):
        data = put_tier_name(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
