import vampytest

from ..fields import parse_verified


def test__parse_verified():
    """
    Tests whether ``parse_verified`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'verified': False}, False),
        ({'verified': True}, True),
    ):
        output = parse_verified(input_data)
        vampytest.assert_eq(output, expected_output)
