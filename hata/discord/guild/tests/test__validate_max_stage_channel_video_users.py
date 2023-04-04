import vampytest

from ..fields import validate_max_stage_channel_video_users


def test__validate_max_stage_channel_video_users__0():
    """
    Tests whether `validate_max_stage_channel_video_users` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (0, 0),
        (1, 1),
    ):
        output = validate_max_stage_channel_video_users(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_max_stage_channel_video_users__1():
    """
    Tests whether `validate_max_stage_channel_video_users` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        -1,
    ):
        with vampytest.assert_raises(ValueError):
            validate_max_stage_channel_video_users(input_value)


def test__validate_max_stage_channel_video_users__2():
    """
    Tests whether `validate_max_stage_channel_video_users` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_max_stage_channel_video_users(input_value)
