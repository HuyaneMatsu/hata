import vampytest

from ..thumbnail import EmbedThumbnail


def _assert_fields_set(field):
    """
    Checks whether every fields of the given embed thumbnail are set.
    
    Parameters
    ----------
    field : ``EmbedThumbnail``
        The field to check.
    """
    vampytest.assert_instance(field, EmbedThumbnail)
    vampytest.assert_instance(field.height, int)
    vampytest.assert_instance(field.url, str, nullable = True)
    vampytest.assert_instance(field.proxy_url, str, nullable = True)
    vampytest.assert_instance(field.width, int)


def test__EmbedThumbnail__new():
    """
    Tests whether ``EmbedThumbnail.__new__`` works as intended.
    """
    url = 'https://orindance.party/'
    
    field = EmbedThumbnail(url)
    _assert_fields_set(field)
    
    vampytest.assert_eq(field.url, url)
