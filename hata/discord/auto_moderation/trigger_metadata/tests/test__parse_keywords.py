import vampytest

from ..fields import parse_keywords


def test__parse_keywords():
    """
    Tests whether ``parse_keywords`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'keyword_filter': None}, None),
        ({'keyword_filter': []}, None),
        ({'keyword_filter': ['a']}, ('a', )),
    ):
        output = parse_keywords(input_data)
        vampytest.assert_eq(output, expected_output)
