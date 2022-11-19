import vampytest

from ..fields import parse_matched_content


def test__parse_matched_content():
    """
    Tests whether ``parse_matched_content`` works as intended.
    """
    matched_content = 'owo'
    
    for input_data, expected_output in (
        ({}, None),
        ({'matched_content': None}, None),
        ({'matched_content': ''}, None),
        ({'matched_content': str(matched_content)}, matched_content),
    ):
        output = parse_matched_content(input_data)
        vampytest.assert_eq(output, expected_output)
