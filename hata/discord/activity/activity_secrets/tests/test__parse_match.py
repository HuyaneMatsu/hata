import vampytest

from ..fields import parse_match


def test__parse_match():
    """
    Tests whether ``parse_match`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'match': None}, None),
        ({'match': ''}, None),
        ({'match': 'a'}, 'a'),
    ):
        output = parse_match(input_data)
        vampytest.assert_eq(output, expected_output)
