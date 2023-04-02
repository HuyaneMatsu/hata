import vampytest

from ..author import EmbedAuthor


def test__EmbedAuthor__repr():
    """
    Tests whether ``EmbedAuthor.__repr__`` works as intended.
    """
    icon_url = 'attachment://orin.png'
    name = 'orin'
    url = 'https://orindance.party/'
    
    field = EmbedAuthor(name = name, icon_url = icon_url, url = url)
    vampytest.assert_instance(repr(field), str)


def test__EmbedAuthor__hash():
    """
    Tests whether ``EmbedAuthor.__hash__`` works as intended.
    """
    icon_url = 'attachment://orin.png'
    name = 'orin'
    url = 'https://orindance.party/'
    
    field = EmbedAuthor(name = name, icon_url = icon_url, url = url)
    vampytest.assert_instance(hash(field), int)


def test__EmbedAuthor__eq():
    """
    Tests whether ``EmbedAuthor.__eq__`` works as intended.
    """
    icon_url = 'attachment://orin.png'
    name = 'orin'
    url = 'https://orindance.party/'
    
    keyword_parameters = {
        'icon_url': icon_url,
        'name': name,
        'url': url,
    }
    
    field = EmbedAuthor(**keyword_parameters)
    
    vampytest.assert_eq(field, field)
    vampytest.assert_ne(field, object())
    
    for field_name, field_value in (
        ('icon_url', 'attachment://rin.png'),
        ('name', 'rin'),
        ('url', 'https://www.astil.dev/'),
    ):
        test_field = EmbedAuthor(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(field, test_field)


def test__EmbedAuthor__bool():
    """
    Tests whether ``EmbedAuthor.__bool__`` works as intended.
    """
    icon_url = 'attachment://orin.png'
    name = 'orin'
    url = 'https://orindance.party/'
    
    for field, expected_output in (
        (EmbedAuthor(), False),
        (EmbedAuthor(name = name), True),
        (EmbedAuthor(url = url), True),
        (EmbedAuthor(name = name, url = url), True),
        (EmbedAuthor(icon_url = icon_url), True),
        (EmbedAuthor(icon_url = icon_url, name = name), True),
        (EmbedAuthor(icon_url = icon_url, url = url), True),
        (EmbedAuthor(icon_url = icon_url, name = name, url = url), True),
    ):
        vampytest.assert_eq(bool(field), expected_output)



def test__EmbedAuthor__len():
    """
    Tests whether ``EmbedAuthor.__len__`` works as intended.
    """
    icon_url = 'attachment://orin.png'
    name = 'orin'
    url = 'https://orindance.party/'
    
    for field, expected_output in (
        (EmbedAuthor(), 0),
        (EmbedAuthor(name = name), len(name)),
        (EmbedAuthor(url = url), 0),
        (EmbedAuthor(name = name, url = url), len(name)),
        (EmbedAuthor(icon_url = icon_url), 0),
        (EmbedAuthor(icon_url = icon_url, name = name), len(name)),
        (EmbedAuthor(icon_url = icon_url, url = url), 0),
        (EmbedAuthor(icon_url = icon_url, name = name, url = url), len(name)),
    ):
        vampytest.assert_eq(len(field), expected_output)
