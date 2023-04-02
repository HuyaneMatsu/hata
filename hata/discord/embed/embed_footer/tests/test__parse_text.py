import vampytest

from ..fields import parse_text


def test__parse_text():
    """
    Tests whether ``parse_text`` works as intended.
    """
    for input_data, expected_output in (
        ({'text': None}, None),
        ({'text': ''}, None),
        ({'text': 'a'}, 'a'),
    ):
        output = parse_text(input_data)
        vampytest.assert_eq(output, expected_output)
