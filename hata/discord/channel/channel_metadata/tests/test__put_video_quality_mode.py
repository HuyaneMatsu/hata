import vampytest

from ..fields import put_video_quality_mode
from ..preinstanced import VideoQualityMode


def test__put_video_quality_mode():
    """
    Tests whether ``put_video_quality_mode`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (VideoQualityMode.none, False, {}),
        (VideoQualityMode.auto, False, {}),
        (VideoQualityMode.full, False, {'video_quality_mode': VideoQualityMode.full.value}),
        (VideoQualityMode.none, True, {'video_quality_mode': VideoQualityMode.auto.value}),
        (VideoQualityMode.auto, True, {'video_quality_mode': VideoQualityMode.auto.value}),
    ):
        data = put_video_quality_mode(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
