import vampytest

from ..fields import parse_placeholder


def test__parse_placeholder():
    """
    Tests whether ``parse_placeholder`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'placeholder': None}, None),
        ({'placeholder': ''}, None),
        ({'placeholder': 'a'}, 'a'),
    ):
        output = parse_placeholder(input_data)
        vampytest.assert_eq(output, expected_output)
