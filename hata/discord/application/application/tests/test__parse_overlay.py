import vampytest

from ..fields import parse_overlay


def test__parse_overlay():
    """
    Tests whether ``parse_overlay`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'overlay': False}, False),
        ({'overlay': True}, True),
    ):
        output = parse_overlay(input_data)
        vampytest.assert_eq(output, expected_output)
