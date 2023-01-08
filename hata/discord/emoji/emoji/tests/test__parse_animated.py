import vampytest

from ..fields import parse_animated


def test__parse_animated():
    """
    Tests whether ``parse_animated`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'animated': False}, False),
        ({'animated': True}, True),
    ):
        output = parse_animated(input_data)
        vampytest.assert_eq(output, expected_output)
