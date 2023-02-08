import vampytest

from ..fields import parse_mfa


def test__parse_mfa():
    """
    Tests whether ``parse_mfa`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'mfa_enabled': False}, False),
        ({'mfa_enabled': True}, True),
    ):
        output = parse_mfa(input_data)
        vampytest.assert_eq(output, expected_output)
