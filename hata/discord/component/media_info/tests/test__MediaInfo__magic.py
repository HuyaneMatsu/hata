import vampytest

from ..media_info import MediaInfo


def test__MediaInfo__repr():
    """
    Tests whether ``MediaInfo.__repr__`` works as intended.
    """
    content_type = 'image/png'
    height = 56
    proxy_url = 'https://orindance.party/proxy'
    url = 'https://orindance.party/'
    width = 23
    
    media_info = MediaInfo.precreate(
        content_type = content_type,
        height = height,
        proxy_url = proxy_url,
        url = url,
        width = width,
    )
    
    output = repr(media_info)
    vampytest.assert_instance(output, str)


def test__MediaInfo__hash():
    """
    Tests whether ``MediaInfo.__hash__`` works as intended.
    """
    content_type = 'image/png'
    height = 56
    proxy_url = 'https://orindance.party/proxy'
    url = 'https://orindance.party/'
    width = 23
    
    media_info = MediaInfo.precreate(
        content_type = content_type,
        height = height,
        proxy_url = proxy_url,
        url = url,
        width = width,
    )
    
    output = hash(media_info)
    vampytest.assert_instance(output, int)


def _iter_options__eq__same_type():
    content_type = 'image/png'
    height = 56
    proxy_url = 'https://orindance.party/proxy'
    url = 'https://orindance.party/'
    width = 23
    
    keyword_parameters = {
        'content_type': content_type,
        'proxy_url': proxy_url,
        'height': height,
        'url': url,
        'width': width,
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
            'content_type': 'application/json',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'height': 17,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'proxy_url': 'https://orindance.party/carting',
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
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'width': 16,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq__same_type()).returning_last())
def test__MediaInfo__eq__same_type(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``MediaInfo.__eq__`` works as intended.
    
    Case: Same type.
    
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
    media_info_0 = MediaInfo.precreate(**keyword_parameters_0)
    media_info_1 = MediaInfo.precreate(**keyword_parameters_1)
    
    output = media_info_0 == media_info_1
    vampytest.assert_instance(output, bool)
    return output
