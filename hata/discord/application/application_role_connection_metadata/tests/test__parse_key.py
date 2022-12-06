import vampytest

from ..fields import parse_key


def test__parse_key():
    """
    Tests whether ``parse_key`` works as intended.
    """
    for input_data, expected_output in (
        ({}, ''),
        ({'key': None}, ''),
        ({'key': ''}, ''),
        ({'key': 'a'}, 'a'),
    ):
        output = parse_key(input_data)
        vampytest.assert_eq(output, expected_output)
