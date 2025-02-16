import vampytest

from ..fields import put_max_stage_channel_video_users


def test__put_max_stage_channel_video_users():
    """
    Tests whether ``put_max_stage_channel_video_users`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (0, False, {'max_stage_video_channel_users': 0}),
        (0, True, {'max_stage_video_channel_users': 0}),
        (1, False, {'max_stage_video_channel_users': 1}),
        (1, True, {'max_stage_video_channel_users': 1}),
    ):
        data = put_max_stage_channel_video_users(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
