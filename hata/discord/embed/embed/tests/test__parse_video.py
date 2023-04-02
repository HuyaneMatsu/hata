import vampytest

from ...embed_video import EmbedVideo

from ..fields import parse_video


def test__parse_video():
    """
    Tests whether ``parse_video`` works as intended.
    """
    video = EmbedVideo(url = 'https://orindance.party/')
    
    for input_data, expected_output in (
        ({}, None),
        ({'video': None}, None),
        ({'video': video.to_data()}, video),
    ):
        output = parse_video(input_data)
        vampytest.assert_eq(output, expected_output)
