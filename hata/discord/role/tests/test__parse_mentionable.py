import vampytest

from ..fields import parse_mentionable


def test__parse_mentionable():
    """
    Tests whether ``parse_mentionable`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'mentionable': False}, False),
        ({'mentionable': True}, True),
    ):
        output = parse_mentionable(input_data)
        vampytest.assert_eq(output, expected_output)
