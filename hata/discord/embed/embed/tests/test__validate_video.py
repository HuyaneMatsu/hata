import vampytest

from ...embed_video import EmbedVideo

from ..fields import validate_video


def test__validate_video__0():
    """
    Tests whether `validate_video` works as intended.
    
    Case: passing.
    """
    video = EmbedVideo(url = 'https://orindance.party/')
    
    for input_value, expected_output in (
        (None, None),
        (video, video),
    ):
        output = validate_video(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_video__1():
    """
    Tests whether `validate_video` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_video(input_value)
