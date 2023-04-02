import vampytest

from ..video import EmbedVideo


def _assert_fields_set(field):
    """
    Checks whether every fields of the given activity field are set.
    
    Parameters
    ----------
    field : ``EmbedVideo``
        The field to check.
    """
    vampytest.assert_instance(field, EmbedVideo)
    vampytest.assert_instance(field.height, int)
    vampytest.assert_instance(field.url, str, nullable = True)
    vampytest.assert_instance(field.proxy_url, str, nullable = True)
    vampytest.assert_instance(field.width, int)


def test__EmbedVideo__new():
    """
    Tests whether ``EmbedVideo.__new__`` works as intended.
    """
    url = 'https://orindance.party/'
    
    field = EmbedVideo(url)
    _assert_fields_set(field)
    
    vampytest.assert_eq(field.url, url)
