import vampytest

from ...preinstanced import VideoQualityMode

from ..video_quality_mode import parse_video_quality_mode


def test__parse_video_quality_mode():
    """
    Tests whether ``parse_video_quality_mode`` works as intended.
    """
    for input_data, expected_output in (
        ({}, VideoQualityMode.auto),
        ({'video_quality_mode': VideoQualityMode.auto.value}, VideoQualityMode.auto),
        ({'video_quality_mode': VideoQualityMode.full.value}, VideoQualityMode.full),
    ):
        output = parse_video_quality_mode(input_data)
        vampytest.assert_eq(output, expected_output)
