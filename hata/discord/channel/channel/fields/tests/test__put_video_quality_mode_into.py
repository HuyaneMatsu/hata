import vampytest

from ...preinstanced import VideoQualityMode

from ..video_quality_mode import put_video_quality_mode_into


def test__put_video_quality_mode_into():
    """
    Tests whether ``put_video_quality_mode_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (VideoQualityMode.none, False, {}),
        (VideoQualityMode.auto, False, {}),
        (VideoQualityMode.full, False, {'video_quality_mode': VideoQualityMode.full.value}),
        (VideoQualityMode.none, True, {'video_quality_mode': VideoQualityMode.auto.value}),
        (VideoQualityMode.auto, True, {'video_quality_mode': VideoQualityMode.auto.value}),
    ):
        data = put_video_quality_mode_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
