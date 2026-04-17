import vampytest

from ..fields import parse_matched_keyword


def test__parse_matched_keyword():
    """
    Tests whether ``parse_matched_keyword`` works as intended.
    """
    matched_keyword = 'owo'
    
    for input_data, expected_output in (
        ({}, None),
        ({'matched_keyword': None}, None),
        ({'matched_keyword': ''}, None),
        ({'matched_keyword': str(matched_keyword)}, matched_keyword),
    ):
        output = parse_matched_keyword(input_data)
        vampytest.assert_eq(output, expected_output)
