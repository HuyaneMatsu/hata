import vampytest

from ...preinstanced import VoiceRegion

from ..region import parse_region


def test__parse_region():
    """
    Tests whether ``parse_region`` works as intended.
    """
    for input_data, expected_output in (
        ({}, VoiceRegion.unknown),
        ({'rtc_region': None}, VoiceRegion.unknown),
        ({'rtc_region': VoiceRegion.brazil.value}, VoiceRegion.brazil),
    ):
        output = parse_region(input_data)
        vampytest.assert_is(output, expected_output)
