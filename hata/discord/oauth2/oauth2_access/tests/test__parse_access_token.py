import vampytest

from ..fields import parse_access_token


def test__parse_access_token():
    """
    Tests whether ``parse_access_token`` works as intended.
    """
    for input_data, expected_output in (
        ({'access_token': ''}, ''),
        ({'access_token': 'a'}, 'a'),
    ):
        output = parse_access_token(input_data)
        vampytest.assert_eq(output, expected_output)
