import vampytest

from ..fields import validate_video_quality_mode
from ..preinstanced import VideoQualityMode


def test__validate_video_quality_mode__0():
    """
    Tests whether `validate_video_quality_mode` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (VideoQualityMode.full, VideoQualityMode.full),
        (VideoQualityMode.full.value, VideoQualityMode.full)
    ):
        output = validate_video_quality_mode(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_video_quality_mode__1():
    """
    Tests whether `validate_video_quality_mode` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_video_quality_mode(input_value)
