import vampytest

from ..video import EmbedVideo


def _assert_fields_set(embed_video):
    """
    Checks whether every fields of the given embed video are set.
    
    Parameters
    ----------
    embed_video : ``EmbedVideo``
        The field to check.
    """
    vampytest.assert_instance(embed_video, EmbedVideo)
    vampytest.assert_instance(embed_video.height, int)
    vampytest.assert_instance(embed_video.url, str, nullable = True)
    vampytest.assert_instance(embed_video.proxy_url, str, nullable = True)
    vampytest.assert_instance(embed_video.width, int)


def test__EmbedVideo__new():
    """
    Tests whether ``EmbedVideo.__new__`` works as intended.
    """
    url = 'https://orindance.party/'
    
    embed_video = EmbedVideo(url)
    _assert_fields_set(embed_video)
    
    vampytest.assert_eq(embed_video.url, url)
