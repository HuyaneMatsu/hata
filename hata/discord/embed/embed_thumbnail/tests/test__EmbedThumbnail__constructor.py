import vampytest

from ...embed_field_base import EmbedMediaFlag

from ..thumbnail import EmbedThumbnail


def _assert_fields_set(embed_thumbnail):
    """
    Checks whether every fields of the given embed thumbnail are set.
    
    Parameters
    ----------
    embed_thumbnail : ``EmbedThumbnail``
        The field to check.
    """
    vampytest.assert_instance(embed_thumbnail, EmbedThumbnail)
    vampytest.assert_instance(embed_thumbnail.flags, EmbedMediaFlag)
    vampytest.assert_instance(embed_thumbnail.height, int)
    vampytest.assert_instance(embed_thumbnail.url, str, nullable = True)
    vampytest.assert_instance(embed_thumbnail.proxy_url, str, nullable = True)
    vampytest.assert_instance(embed_thumbnail.width, int)


def test__EmbedThumbnail__new():
    """
    Tests whether ``EmbedThumbnail.__new__`` works as intended.
    """
    url = 'https://orindance.party/'
    
    embed_thumbnail = EmbedThumbnail(url)
    _assert_fields_set(embed_thumbnail)
    
    vampytest.assert_eq(embed_thumbnail.url, url)
