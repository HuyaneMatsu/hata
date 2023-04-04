import vampytest

from ..fields import put_max_stage_channel_video_users_into


def test__put_max_stage_channel_video_users_into():
    """
    Tests whether ``put_max_stage_channel_video_users_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (0, False, {}),
        (0, True, {'max_stage_video_channel_users': 0}),
        (1, False, {'max_stage_video_channel_users': 1}),
        (1, True, {'max_stage_video_channel_users': 1}),
    ):
        data = put_max_stage_channel_video_users_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
