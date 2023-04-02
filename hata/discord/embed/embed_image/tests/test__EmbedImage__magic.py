import vampytest

from ..image import EmbedImage


def test__EmbedImage__repr():
    """
    Tests whether ``EmbedImage.__repr__`` works as intended.
    """
    url = 'https://orindance.party/'
    
    field = EmbedImage(url)
    vampytest.assert_instance(repr(field), str)


def test__EmbedImage__hash():
    """
    Tests whether ``EmbedImage.__hash__`` works as intended.
    """
    url = 'https://orindance.party/'
    
    field = EmbedImage(url)
    vampytest.assert_instance(hash(field), int)


def test__EmbedImage__eq():
    """
    Tests whether ``EmbedImage.__eq__`` works as intended.
    """
    url = 'https://orindance.party/'
    
    keyword_parameters = {
        'url': url,
    }
    
    field = EmbedImage(**keyword_parameters)
    
    vampytest.assert_eq(field, field)
    vampytest.assert_ne(field, object())
    
    for field_name, field_value in (
        ('url', 'https://www.astil.dev/'),
    ):
        test_field = EmbedImage(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(field, test_field)


def test__EmbedImage__bool():
    """
    Tests whether ``EmbedImage.__bool__`` works as intended.
    """
    url = 'https://orindance.party/'
    
    for field, expected_output in (
        (EmbedImage(None), False),
        (EmbedImage(url), True),
    ):
        vampytest.assert_eq(bool(field), expected_output)



def test__EmbedImage__len():
    """
    Tests whether ``EmbedImage.__len__`` works as intended.
    """
    url = 'https://orindance.party/'
    
    for field, expected_output in (
        (EmbedImage(None), 0),
        (EmbedImage(url), 0),
    ):
        vampytest.assert_eq(len(field), expected_output)
