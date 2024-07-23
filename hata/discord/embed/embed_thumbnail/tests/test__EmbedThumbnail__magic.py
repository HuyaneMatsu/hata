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



def _iter_options__eq():
    url_0 = 'https://orindance.party/'
    url_1 = 'https://www.astil.dev/'
    
    yield (
        {
            'url': url_0,
        },
        {},
        {
            'url': url_0,
        },
        {},
        True,
    )
    
    yield (
        {
            'url': url_0,
        },
        {},
        {
            'url': url_1,
        },
        {},
        False,
    )
    
    yield (
        {
            'url': url_0,
        },
        {
            'proxy_url': url_0,
            'width': 2,
            'height': 3,
        },
        {
            'url': url_0,
        },
        {},
        True,
    )
    
    yield (
        {
            'url': url_0,
        },
        {
            'proxy_url': url_0,
            'width': 2,
            'height': 3,
        },
        {
            'url': url_0,
        },
        {
            'proxy_url': url_1,
        },
        False,
    )
    
    yield (
        {
            'url': url_0,
        },
        {
            'proxy_url': url_0,
            'width': 2,
            'height': 3,
        },
        {
            'url': url_0,
        },
        {
            'proxy_url': url_1,
            'width': 2,
        },
        False,
    )
    
    yield (
        {
            'url': url_0,
        },
        {
            'proxy_url': url_0,
            'width': 2,
            'height': 3,
        },
        {
            'url': url_0,
        },
        {
            'proxy_url': url_1,
            'height': 3,
        },
        False,
    )
    
    yield (
        {
            'url': url_0,
        },
        {
            'proxy_url': url_0,
            'width': 2,
            'height': 3,
        },
        {
            'url': url_0,
        },
        {
            'proxy_url': url_1,
            'width': 2,
            'height': 3,
        },
        True,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__EmbedThumbnail__eq(
    keyword_parameters_0,
    additional_attributes_0,
    keyword_parameters_1,
    additional_attributes_1,
):
    """
    Tests whether ``EmbedThumbnail.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    additional_attributes_0 : `dict<str, object>`
        Additional attributes to set.
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    additional_attributes_1 : `dict<str, object>`
        Additional attributes to set.
    
    Returns
    -------
    output : `bool`
    """
    embed_thumbnail_0 = EmbedThumbnail(**keyword_parameters_0)
    for item in additional_attributes_0.items():
        setattr(embed_thumbnail_0, *item)
    
    
    embed_thumbnail_1 = EmbedThumbnail(**keyword_parameters_1)
    for item in additional_attributes_1.items():
        setattr(embed_thumbnail_1, *item)
    
    output = embed_thumbnail_0 == embed_thumbnail_1
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__bool():
    url = 'https://orindance.party/'
    
    yield {}, False
    yield {'url': url}, True


@vampytest._(vampytest.call_from(_iter_options__bool()).returning_last())
def test__EmbedThumbnail__bool(keyword_parameters):
    """
    Tests whether ``EmbedThumbnail.__bool__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the embed thumbnail with.
    
    Returns
    -------
    output : `bool`
    """
    field = EmbedThumbnail(**keyword_parameters)
    output = bool(field)
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__len():
    url = 'https://orindance.party/'
    
    yield {}, 0
    yield {'url': url}, 0


@vampytest._(vampytest.call_from(_iter_options__len()).returning_last())
def test__EmbedThumbnail__len(keyword_parameters):
    """
    Tests whether ``EmbedThumbnail.__len__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the embed thumbnail with.
    
    Returns
    -------
    output : `int`
    """
    field = EmbedThumbnail(**keyword_parameters)
    output = len(field)
    vampytest.assert_instance(output, int)
    return output
