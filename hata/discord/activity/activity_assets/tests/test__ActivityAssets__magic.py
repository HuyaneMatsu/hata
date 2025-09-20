import vampytest

from ..assets import ActivityAssets


def test__ActivityAssets__repr():
    """
    Tests whether ``ActivityAssets.__repr__`` works as intended.
    """
    image_large = 'plain'
    image_small = 'asia'
    text_large = 'senya'
    text_small = 'vocal'
    url_large = 'https://orindance.party/bbo.png'
    url_small = 'https://orindance.party/llo.png'
    
    activity_assets = ActivityAssets(
        image_large = image_large,
        image_small = image_small,
        text_large = text_large,
        text_small = text_small,
        url_large = url_large,
        url_small = url_small,
    )
    
    output = repr(activity_assets)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    image_large = 'plain'
    image_small = 'asia'
    text_large = 'senya'
    text_small = 'vocal'
    url_large = 'https://orindance.party/bbo.png'
    url_small = 'https://orindance.party/llo.png'
    
    keyword_parameters = {
        'image_large': image_large,
        'image_small': image_small,
        'text_large': text_large,
        'text_small': text_small,
        'url_large': url_large,
        'url_small': url_small,
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
            'image_large': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'image_small': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'text_large': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'text_small': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'url_large': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'url_small': None,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__Activity_assets__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ActivityAssets.__eq__`` works as intended.
    
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
    activity_assets_0 = ActivityAssets(**keyword_parameters_0)
    activity_assets_1 = ActivityAssets(**keyword_parameters_1)
    
    output = activity_assets_0 == activity_assets_1
    vampytest.assert_instance(output, bool)
    return output


def test__ActivityAssets__hash():
    """
    Tests whether ``ActivityAssets.__hash__`` works as intended.
    """
    image_large = 'plain'
    image_small = 'asia'
    text_large = 'senya'
    text_small = 'vocal'
    url_large = 'https://orindance.party/bbo.png'
    url_small = 'https://orindance.party/llo.png'
    
    activity_assets = ActivityAssets(
        image_large = image_large,
        image_small = image_small,
        text_large = text_large,
        text_small = text_small,
        url_large = url_large,
        url_small = url_small,
    )
    
    output = hash(activity_assets)
    vampytest.assert_instance(output, int)


def _iter_options__bool():
    image_large = 'plain'
    image_small = 'asia'
    text_large = 'senya'
    text_small = 'vocal'
    url_large = 'https://orindance.party/bbo.png'
    url_small = 'https://orindance.party/llo.png'
    
    yield (
        {},
        False,
    )
    
    yield (
        {
            'image_large': image_large,
        },
        True,
    )
    
    yield (
        {
            'image_small': image_small,
        },
        True,
    )
    
    yield (
        {
            'text_large': text_large,
        },
        True,
    )
    
    yield (
        {
            'text_small': text_small,
        },
        True,
    )
    
    yield (
        {
            'url_large': url_large,
        },
        True,
    )
    
    yield (
        {
            'url_small': url_small,
        },
        True,
    )


@vampytest._(vampytest.call_from(_iter_options__bool()).returning_last())
def test__Activity_assets__bool(keyword_parameters):
    """
    Tests whether ``ActivityAssets.__bool__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    activity_assets = ActivityAssets(**keyword_parameters)
    
    output = bool(activity_assets)
    vampytest.assert_instance(output, bool)
    return output
