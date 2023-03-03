import vampytest

from ..fields import parse_custom_message


def test__parse_custom_message():
    """
    Tests whether ``parse_custom_message`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'custom_message': None}, None),
        ({'custom_message': ''}, None),
        ({'custom_message': 'a'}, 'a'),
    ):
        output = parse_custom_message(input_data)
        vampytest.assert_eq(output, expected_output)
