import vampytest

from ..fields import parse_temporary


def test__parse_temporary():
    """
    Tests whether ``parse_temporary`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'ephemeral': False}, False),
        ({'ephemeral': True}, True),
    ):
        output = parse_temporary(input_data)
        vampytest.assert_eq(output, expected_output)
