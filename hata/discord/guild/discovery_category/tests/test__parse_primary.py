import vampytest

from ..fields import parse_primary


def test__parse_primary():
    """
    Tests whether ``parse_primary`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'is_primary': False}, False),
        ({'is_primary': True}, True),
    ):
        output = parse_primary(input_data)
        vampytest.assert_eq(output, expected_output)
