import vampytest

from ...embed_video import EmbedVideo

from ..fields import put_video


def test__put_video():
    """
    Tests whether ``put_video`` is working as intended.
    """
    video = EmbedVideo(url = 'https://orindance.party/')
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (video, False, {'video': video.to_data()}),
        (video, True, {'video': video.to_data(defaults = True)}),
    ):
        data = put_video(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
