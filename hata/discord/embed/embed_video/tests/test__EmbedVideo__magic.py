import vampytest

from ..video import EmbedVideo


def test__EmbedVideo__repr():
    """
    Tests whether ``EmbedVideo.__repr__`` works as intended.
    """
    url = 'https://orindance.party/'
    
    field = EmbedVideo(url)
    vampytest.assert_instance(repr(field), str)


def test__EmbedVideo__hash():
    """
    Tests whether ``EmbedVideo.__hash__`` works as intended.
    """
    url = 'https://orindance.party/'
    
    field = EmbedVideo(url)
    vampytest.assert_instance(hash(field), int)


def test__EmbedVideo__eq():
    """
    Tests whether ``EmbedVideo.__eq__`` works as intended.
    """
    url = 'https://orindance.party/'
    
    keyword_parameters = {
        'url': url,
    }
    
    field = EmbedVideo(**keyword_parameters)
    
    vampytest.assert_eq(field, field)
    vampytest.assert_ne(field, object())
    
    for field_name, field_value in (
        ('url', 'https://www.astil.dev/'),
    ):
        test_field = EmbedVideo(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(field, test_field)


def test__EmbedVideo__bool():
    """
    Tests whether ``EmbedVideo.__bool__`` works as intended.
    """
    url = 'https://orindance.party/'
    
    for field, expected_output in (
        (EmbedVideo(None), False),
        (EmbedVideo(url), True),
    ):
        vampytest.assert_eq(bool(field), expected_output)



def test__EmbedVideo__len():
    """
    Tests whether ``EmbedVideo.__len__`` works as intended.
    """
    url = 'https://orindance.party/'
    
    for field, expected_output in (
        (EmbedVideo(None), 0),
        (EmbedVideo(url), 0),
    ):
        vampytest.assert_eq(len(field), expected_output)
