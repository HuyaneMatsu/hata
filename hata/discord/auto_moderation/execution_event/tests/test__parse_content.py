import vampytest

from ..fields import parse_content


def test__parse_content():
    """
    Tests whether ``parse_content`` works as intended.
    """
    content = 'owo'
    
    for input_data, expected_output in (
        ({}, None),
        ({'content': None}, None),
        ({'content': ''}, None),
        ({'content': str(content)}, content),
    ):
        output = parse_content(input_data)
        vampytest.assert_eq(output, expected_output)
