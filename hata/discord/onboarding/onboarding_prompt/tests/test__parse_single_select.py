import vampytest

from ..fields import parse_single_select


def test__parse_single_select():
    """
    Tests whether ``parse_single_select`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'single_select': False}, False),
        ({'single_select': True}, True),
    ):
        output = parse_single_select(input_data)
        vampytest.assert_eq(output, expected_output)
