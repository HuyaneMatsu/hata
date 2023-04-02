import vampytest

from ..thumbnail import EmbedThumbnail


def test__EmbedThumbnail__repr():
    """
    Tests whether ``EmbedThumbnail.__repr__`` works as intended.
    """
    url = 'https://orindance.party/'
    
    field = EmbedThumbnail(url)
    vampytest.assert_instance(repr(field), str)


def test__EmbedThumbnail__hash():
    """
    Tests whether ``EmbedThumbnail.__hash__`` works as intended.
    """
    url = 'https://orindance.party/'
    
    field = EmbedThumbnail(url)
    vampytest.assert_instance(hash(field), int)


def test__EmbedThumbnail__eq():
    """
    Tests whether ``EmbedThumbnail.__eq__`` works as intended.
    """
    url = 'https://orindance.party/'
    
    keyword_parameters = {
        'url': url,
    }
    
    field = EmbedThumbnail(**keyword_parameters)
    
    vampytest.assert_eq(field, field)
    vampytest.assert_ne(field, object())
    
    for field_name, field_value in (
        ('url', 'https://www.astil.dev/'),
    ):
        test_field = EmbedThumbnail(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(field, test_field)


def test__EmbedThumbnail__bool():
    """
    Tests whether ``EmbedThumbnail.__bool__`` works as intended.
    """
    url = 'https://orindance.party/'
    
    for field, expected_output in (
        (EmbedThumbnail(None), False),
        (EmbedThumbnail(url), True),
    ):
        vampytest.assert_eq(bool(field), expected_output)



def test__EmbedThumbnail__len():
    """
    Tests whether ``EmbedThumbnail.__len__`` works as intended.
    """
    url = 'https://orindance.party/'
    
    for field, expected_output in (
        (EmbedThumbnail(None), 0),
        (EmbedThumbnail(url), 0),
    ):
        vampytest.assert_eq(len(field), expected_output)
