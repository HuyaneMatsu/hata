import vampytest

from ..fields import put_icon_proxy_url


def _iter_options():
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'proxy_icon_url': None,
        },
    )
    
    yield (
        'https://orindance.party/',
        False,
        {
            'proxy_icon_url': 'https://orindance.party/',
        },
    )
    
    yield (
        'https://orindance.party/',
        True,
        {
            'proxy_icon_url': 'https://orindance.party/',
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_icon_proxy_url(input_value, defaults):
    """
    Tests whether ``put_icon_proxy_url`` works as intended.
    
    Parameters
    ----------
    input_value : `None | str`
        Value to serialise.
    
    defaults : `bool`
        Whether values as their defaults should be serialised as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_icon_proxy_url(input_value, {}, defaults)
