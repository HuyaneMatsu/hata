import vampytest

from ..fields import parse_text_small


def test__parse_text_small():
    """
    Tests whether ``parse_text_small`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'small_text': None}, None),
        ({'small_text': ''}, None),
        ({'small_text': 'a'}, 'a'),
    ):
        output = parse_text_small(input_data)
        vampytest.assert_eq(output, expected_output)
