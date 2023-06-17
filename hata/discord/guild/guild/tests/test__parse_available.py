import vampytest

from ..fields import parse_available


def test__parse_available():
    """
    Tests whether ``parse_available`` works as intended.
    """
    for input_data, expected_output in (
        ({}, True),
        ({'unavailable': False}, True),
        ({'unavailable': True}, False),
    ):
        output = parse_available(input_data)
        vampytest.assert_eq(output, expected_output)
