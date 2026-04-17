import vampytest

from ..fields import parse_renewal


def test__parse_renewal():
    """
    Tests whether ``parse_renewal`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'is_renewal': False}, False),
        ({'is_renewal': True}, True),
    ):
        output = parse_renewal(input_data)
        vampytest.assert_eq(output, expected_output)
