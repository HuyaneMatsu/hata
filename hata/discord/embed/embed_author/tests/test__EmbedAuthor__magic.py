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


def _iter_options__bool():
    icon_url = 'attachment://orin.png'
    name = 'orin'
    url = 'https://orindance.party/'
    
    yield {}, False
    yield {'name': name}, True
    yield {'url': url}, True
    yield {'name': name, 'url': url}, True
    yield {'icon_url': icon_url}, True
    yield {'icon_url': icon_url, 'name': name}, True
    yield {'icon_url': icon_url, 'url': url}, True
    yield {'icon_url': icon_url, 'name': name, 'url': url}, True


@vampytest._(vampytest.call_from(_iter_options__bool()).returning_last())
def test__EmbedAuthor__bool(keyword_parameters):
    """
    Tests whether ``EmbedAuthor.__bool__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the embed author with.
    
    Returns
    -------
    output : `bool`
    """
    field = EmbedAuthor(**keyword_parameters)
    output = bool(field)
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__len():
    icon_url = 'attachment://orin.png'
    name = 'orin'
    url = 'https://orindance.party/'
    
    yield {}, 0
    yield {'name': name}, len(name)
    yield {'url': url}, 0
    yield {'name': name, 'url': url}, len(name)
    yield {'icon_url': icon_url}, 0
    yield {'icon_url': icon_url, 'name': name}, len(name)
    yield {'icon_url': icon_url, 'url': url}, 0
    yield {'icon_url': icon_url, 'name': name, 'url': url}, len(name)


@vampytest._(vampytest.call_from(_iter_options__len()).returning_last())
def test__EmbedAuthor__len(keyword_parameters):
    """
    Tests whether ``EmbedAuthor.__len__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the embed author with.
    
    Returns
    -------
    output : `int`
    """
    field = EmbedAuthor(**keyword_parameters)
    output = len(field)
    vampytest.assert_instance(output, int)
    return output
