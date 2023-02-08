import vampytest

from ..fields import parse_refresh_token


def test__parse_refresh_token():
    """
    Tests whether ``parse_refresh_token`` works as intended.
    """
    for input_data, expected_output in (
        ({'refresh_token': ''}, ''),
        ({'refresh_token': 'a'}, 'a'),
    ):
        output = parse_refresh_token(input_data)
        vampytest.assert_eq(output, expected_output)
