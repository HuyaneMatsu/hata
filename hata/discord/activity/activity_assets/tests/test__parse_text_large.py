import vampytest

from ..fields import parse_text_large


def test__parse_text_large():
    """
    Tests whether ``parse_text_large`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'large_text': None}, None),
        ({'large_text': ''}, None),
        ({'large_text': 'a'}, 'a'),
    ):
        output = parse_text_large(input_data)
        vampytest.assert_eq(output, expected_output)
