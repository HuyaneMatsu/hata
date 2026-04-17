import vampytest

from ..fields import parse_user_count


def test__parse_user_count():
    """
    Tests whether ``parse_user_count`` works as intended.
    """
    for input_data, expected_output in (
        ({}, 0),
        ({'member_count': 1}, 1),
    ):
        output = parse_user_count(input_data)
        vampytest.assert_eq(output, expected_output)
