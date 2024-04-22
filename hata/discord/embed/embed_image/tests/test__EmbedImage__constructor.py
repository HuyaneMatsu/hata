import vampytest

from ..image import EmbedImage


def _assert_fields_set(field):
    """
    Checks whether every fields of the given embed image are set.
    
    Parameters
    ----------
    field : ``EmbedImage``
        The field to check.
    """
    vampytest.assert_instance(field, EmbedImage)
    vampytest.assert_instance(field.height, int)
    vampytest.assert_instance(field.url, str, nullable = True)
    vampytest.assert_instance(field.proxy_url, str, nullable = True)
    vampytest.assert_instance(field.width, int)


def test__EmbedImage__new():
    """
    Tests whether ``EmbedImage.__new__`` works as intended.
    """
    url = 'https://orindance.party/'
    
    field = EmbedImage(url)
    _assert_fields_set(field)
    
    vampytest.assert_eq(field.url, url)
