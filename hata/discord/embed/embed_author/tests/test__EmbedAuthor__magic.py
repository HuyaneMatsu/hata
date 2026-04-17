import vampytest

from ..author import EmbedAuthor


def test__EmbedAuthor__repr():
    """
    Tests whether ``EmbedAuthor.__repr__`` works as intended.
    """
    icon_url = 'attachment://orin.png'
    name = 'orin'
    url = 'https://orindance.party/'
    
    embed_author = EmbedAuthor(name = name, icon_url = icon_url, url = url)
    vampytest.assert_instance(repr(embed_author), str)


def test__EmbedAuthor__hash():
    """
    Tests whether ``EmbedAuthor.__hash__`` works as intended.
    """
    icon_url = 'attachment://orin.png'
    name = 'orin'
    url = 'https://orindance.party/'
    
    embed_author = EmbedAuthor(name = name, icon_url = icon_url, url = url)
    vampytest.assert_instance(hash(embed_author), int)


def _iter_options__eq():
    icon_url = 'attachment://orin.png'
    name = 'orin'
    url = 'https://orindance.party/'
    
    keyword_parameters = {
        'icon_url': icon_url,
        'name': name,
        'url': url,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'icon_url': 'attachment://rin.png',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'name': 'rin',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'url': 'https://www.astil.dev/',
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__EmbedAuthor__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``EmbedAuthor.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    embed_author_0 = EmbedAuthor(**keyword_parameters_0)
    embed_author_1 = EmbedAuthor(**keyword_parameters_1)
    
    output = embed_author_0 == embed_author_1
    vampytest.assert_instance(output, bool)
    return output


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
    embed_author = EmbedAuthor(**keyword_parameters)
    output = bool(embed_author)
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
    embed_author = EmbedAuthor(**keyword_parameters)
    output = len(embed_author)
    vampytest.assert_instance(output, int)
    return output
