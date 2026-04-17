import vampytest

from ..fields import parse_token


def test__parse_token():
    """
    Tests whether ``parse_token`` works as intended.
    """
    for input_data, expected_output in (
        ({}, ''),
        ({'token': None}, ''),
        ({'token': ''}, ''),
        ({'token': 'a'}, 'a'),
    ):
        output = parse_token(input_data)
        vampytest.assert_eq(output, expected_output)
