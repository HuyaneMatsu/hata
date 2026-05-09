import vampytest

from ..fields import put_icon_url


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
            'icon_url': None,
        },
    )
    
    yield (
        'https://orindance.party/',
        False,
        {
            'icon_url': 'https://orindance.party/',
        },
    )
    
    yield (
        'https://orindance.party/',
        True,
        {
            'icon_url': 'https://orindance.party/',
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_icon_url(input_value, defaults):
    """
    Tests whether ``put_icon_url`` works as intended.
    
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
    return put_icon_url(input_value, {}, defaults)
