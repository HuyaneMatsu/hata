import vampytest

from ..provider import EmbedProvider


def test__EmbedProvider__repr():
    """
    Tests whether ``EmbedProvider.__repr__`` works as intended.
    """
    name = 'orin'
    url = 'https://orindance.party/'
    
    embed_provider = EmbedProvider(name = name, url = url)
    vampytest.assert_instance(repr(embed_provider), str)


def test__EmbedProvider__hash():
    """
    Tests whether ``EmbedProvider.__hash__`` works as intended.
    """
    name = 'orin'
    url = 'https://orindance.party/'
    
    embed_provider = EmbedProvider(name = name, url = url)
    vampytest.assert_instance(hash(embed_provider), int)



def _iter_options__eq():
    name = 'orin'
    url = 'https://orindance.party/'
    
    keyword_parameters = {
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
def test__EmbedProvider__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``EmbedProvider.__eq__`` works as intended.
    
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
    embed_provider_0 = EmbedProvider(**keyword_parameters_0)
    embed_provider_1 = EmbedProvider(**keyword_parameters_1)
    
    output = embed_provider_0 == embed_provider_1
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__bool():
    url = 'https://orindance.party/'
    name = 'orin'
    
    yield {}, False
    yield {'name': name}, True
    yield {'url': url}, True
    yield {'name': name, 'url': url}, True


@vampytest._(vampytest.call_from(_iter_options__bool()).returning_last())
def test__EmbedProvider__bool(keyword_parameters):
    """
    Tests whether ``EmbedProvider.__bool__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the embed provider with.
    
    Returns
    -------
    output : `bool`
    """
    embed_provider = EmbedProvider(**keyword_parameters)
    output = bool(embed_provider)
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__len():
    url = 'https://orindance.party/'
    name = 'orin'
    
    yield {}, 0
    yield {'name': name}, len(name)
    yield {'url': url}, 0
    yield {'name': name, 'url': url}, len(name)


@vampytest._(vampytest.call_from(_iter_options__len()).returning_last())
def test__EmbedProvider__len(keyword_parameters):
    """
    Tests whether ``EmbedProvider.__len__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the embed provider with.
    
    Returns
    -------
    output : `int`
    """
    embed_provider = EmbedProvider(**keyword_parameters)
    output = len(embed_provider)
    vampytest.assert_instance(output, int)
    return output
