import vampytest

from ..fields import parse_label


def test__parse_label():
    """
    Tests whether ``parse_label`` works as intended.
    """
    for input_data, expected_output in (
        ({}, ''),
        ({'label': None}, ''),
        ({'label': ''}, ''),
        ({'label': 'a'}, 'a'),
    ):
        output = parse_label(input_data)
        vampytest.assert_eq(output, expected_output)
