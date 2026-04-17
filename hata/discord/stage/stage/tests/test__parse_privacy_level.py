import vampytest

from ....scheduled_event import PrivacyLevel

from ..fields import parse_privacy_level


def test__parse_privacy_level():
    """
    Tests whether ``parse_privacy_level`` works as intended.
    """
    for input_data, expected_output in (
        ({}, PrivacyLevel.guild_only),
        ({'privacy_level': PrivacyLevel.guild_only.value}, PrivacyLevel.guild_only),
        ({'privacy_level': PrivacyLevel.public.value}, PrivacyLevel.public),
    ):
        output = parse_privacy_level(input_data)
        vampytest.assert_eq(output, expected_output)
