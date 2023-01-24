import vampytest

from ..fields import parse_self_deaf


def test__parse_self_deaf():
    """
    Tests whether ``parse_self_deaf`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'self_deaf': False}, False),
        ({'self_deaf': True}, True),
    ):
        output = parse_self_deaf(input_data)
        vampytest.assert_eq(output, expected_output)
