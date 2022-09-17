import vampytest

from ...constants import BITRATE_DEFAULT

from ..bitrate import parse_bitrate


def test__parse_bitrate():
    """
    Tests whether ``parse_bitrate`` works as intended.
    """
    for input_data, expected_output in (
        ({}, BITRATE_DEFAULT),
        ({'bitrate': 1}, 1),
    ):
        output = parse_bitrate(input_data)
        vampytest.assert_eq(output, expected_output)
