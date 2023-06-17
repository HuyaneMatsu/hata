import vampytest

from ..constants import MAX_STAGE_CHANNEL_VIDEO_USERS_DEFAULT
from ..fields import parse_max_stage_channel_video_users


def test__parse_max_stage_channel_video_users():
    """
    Tests whether ``parse_max_stage_channel_video_users`` works as intended.
    """
    for input_data, expected_output in (
        ({}, MAX_STAGE_CHANNEL_VIDEO_USERS_DEFAULT),
        ({'max_stage_video_channel_users': 1}, 1),
    ):
        output = parse_max_stage_channel_video_users(input_data)
        vampytest.assert_eq(output, expected_output)
