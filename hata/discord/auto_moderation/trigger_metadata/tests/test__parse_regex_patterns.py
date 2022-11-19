import vampytest

from ..fields import parse_regex_patterns


def test__parse_regex_patterns():
    """
    Tests whether ``parse_regex_patterns`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'regex_patterns': None}, None),
        ({'regex_patterns': []}, None),
        ({'regex_patterns': ['a']}, ('a', )),
    ):
        output = parse_regex_patterns(input_data)
        vampytest.assert_eq(output, expected_output)
