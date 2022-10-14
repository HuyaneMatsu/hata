import vampytest

from ..fields import parse_syncing


def test__parse_syncing():
    """
    Tests whether ``parse_syncing`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'syncing': False}, False),
        ({'syncing': True}, True),
    ):
        output = parse_syncing(input_data)
        vampytest.assert_eq(output, expected_output)
