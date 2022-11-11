import vampytest

from ..fields import parse_nick


def test__parse_nick():
    """
    Tests whether ``parse_nick`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'nick': None}, None),
        ({'nick': ''}, None),
        ({'nick': 'a'}, 'a'),
    ):
        output = parse_nick(input_data)
        vampytest.assert_eq(output, expected_output)
