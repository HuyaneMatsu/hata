import vampytest

from ..video import EmbedVideo


def test__EmbedVideo__repr():
    """
    Tests whether ``EmbedVideo.__repr__`` works as intended.
    """
    url = 'https://orindance.party/'
    
    embed_video = EmbedVideo(url)
    vampytest.assert_instance(repr(embed_video), str)


def test__EmbedVideo__hash():
    """
    Tests whether ``EmbedVideo.__hash__`` works as intended.
    """
    url = 'https://orindance.party/'
    
    embed_video = EmbedVideo(url)
    vampytest.assert_instance(hash(embed_video), int)


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
def test__EmbedVideo__eq(
    keyword_parameters_0,
    additional_attributes_0,
    keyword_parameters_1,
    additional_attributes_1,
):
    """
    Tests whether ``EmbedVideo.__eq__`` works as intended.
    
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
    embed_video_0 = EmbedVideo(**keyword_parameters_0)
    for item in additional_attributes_0.items():
        setattr(embed_video_0, *item)
    
    
    embed_video_1 = EmbedVideo(**keyword_parameters_1)
    for item in additional_attributes_1.items():
        setattr(embed_video_1, *item)
    
    output = embed_video_0 == embed_video_1
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__bool():
    url = 'https://orindance.party/'
    
    yield {}, False
    yield {'url': url}, True


@vampytest._(vampytest.call_from(_iter_options__bool()).returning_last())
def test__EmbedVideo__bool(keyword_parameters):
    """
    Tests whether ``EmbedVideo.__bool__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the embed video with.
    
    Returns
    -------
    output : `bool`
    """
    embed_video = EmbedVideo(**keyword_parameters)
    output = bool(embed_video)
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__len():
    url = 'https://orindance.party/'
    
    yield {}, 0
    yield {'url': url}, 0


@vampytest._(vampytest.call_from(_iter_options__len()).returning_last())
def test__EmbedVideo__len(keyword_parameters):
    """
    Tests whether ``EmbedVideo.__len__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the embed video with.
    
    Returns
    -------
    output : `int`
    """
    embed_video = EmbedVideo(**keyword_parameters)
    output = len(embed_video)
    vampytest.assert_instance(output, int)
    return output
