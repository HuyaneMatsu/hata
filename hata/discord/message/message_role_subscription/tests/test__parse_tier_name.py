import vampytest

from ..fields import parse_tier_name


def test__parse_tier_name():
    """
    Tests whether ``parse_tier_name`` works as intended.
    """
    for input_data, expected_output in (
        ({'tier_name': ''}, ''),
        ({'tier_name': 'a'}, 'a'),
    ):
        output = parse_tier_name(input_data)
        vampytest.assert_eq(output, expected_output)
