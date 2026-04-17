import vampytest

from ..fields import parse_email


def test__parse_email():
    """
    Tests whether ``parse_email`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'email': None}, None),
        ({'email': ''}, None),
        ({'email': 'meow'}, 'meow'),
    ):
        output = parse_email(input_data)
        vampytest.assert_eq(output, expected_output)
