import vampytest

from ..fields import parse_required


def test__parse_required():
    """
    Tests whether ``parse_required`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'required': False}, False),
        ({'required': True}, True),
    ):
        output = parse_required(input_data)
        vampytest.assert_eq(output, expected_output)
