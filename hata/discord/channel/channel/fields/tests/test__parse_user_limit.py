import vampytest

from ...constants import USER_LIMIT_DEFAULT

from ..user_limit import parse_user_limit


def test__parse_user_limit():
    """
    Tests whether ``parse_user_limit`` works as intended.
    """
    for input_data, expected_output in (
        ({}, USER_LIMIT_DEFAULT),
        ({'user_limit': 1}, 1),
    ):
        output = parse_user_limit(input_data)
        vampytest.assert_eq(output, expected_output)
