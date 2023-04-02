import vampytest

from ..provider import EmbedProvider


def test__EmbedProvider__repr():
    """
    Tests whether ``EmbedProvider.__repr__`` works as intended.
    """
    name = 'orin'
    url = 'https://orindance.party/'
    
    field = EmbedProvider(name = name, url = url)
    vampytest.assert_instance(repr(field), str)


def test__EmbedProvider__hash():
    """
    Tests whether ``EmbedProvider.__hash__`` works as intended.
    """
    name = 'orin'
    url = 'https://orindance.party/'
    
    field = EmbedProvider(name = name, url = url)
    vampytest.assert_instance(hash(field), int)


def test__EmbedProvider__eq():
    """
    Tests whether ``EmbedProvider.__eq__`` works as intended.
    """
    name = 'orin'
    url = 'https://orindance.party/'
    
    keyword_parameters = {
        'name': name,
        'url': url,
    }
    
    field = EmbedProvider(**keyword_parameters)
    
    vampytest.assert_eq(field, field)
    vampytest.assert_ne(field, object())
    
    for field_name, field_value in (
        ('name', 'rin'),
        ('url', 'https://www.astil.dev/'),
    ):
        test_field = EmbedProvider(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(field, test_field)


def test__EmbedProvider__bool():
    """
    Tests whether ``EmbedProvider.__bool__`` works as intended.
    """
    name = 'orin'
    url = 'https://orindance.party/'
    
    for field, expected_output in (
        (EmbedProvider(), False),
        (EmbedProvider(name = name), True),
        (EmbedProvider(url = url), True),
        (EmbedProvider(name = name, url = url), True),
    ):
        vampytest.assert_eq(bool(field), expected_output)



def test__EmbedProvider__len():
    """
    Tests whether ``EmbedProvider.__len__`` works as intended.
    """
    name = 'orin'
    url = 'https://orindance.party/'
    
    for field, expected_output in (
        (EmbedProvider(), 0),
        (EmbedProvider(name = name), len(name)),
        (EmbedProvider(url = url), 0),
        (EmbedProvider(name = name, url = url), len(name)),
    ):
        vampytest.assert_eq(len(field), expected_output)
