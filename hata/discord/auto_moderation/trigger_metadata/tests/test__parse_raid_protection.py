import vampytest

from ..fields import parse_raid_protection


def test__parse_raid_protection():
    """
    Tests whether ``parse_raid_protection`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'mention_raid_protection_enabled': False}, False),
        ({'mention_raid_protection_enabled': True}, True),
    ):
        output = parse_raid_protection(input_data)
        vampytest.assert_eq(output, expected_output)
