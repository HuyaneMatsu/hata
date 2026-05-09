import vampytest

from ..fields import put_avatar_url


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
            'avatar_url': None,
        },
    )
    yield (
        'https://orindance.party/',
        False,
        {
            'avatar_url': 'https://orindance.party/',
        },
    )
    
    yield (
        'https://orindance.party/',
        True,
        {
            'avatar_url': 'https://orindance.party/',
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_avatar_url(input_value, defaults):
    """
    Tests whether ``put_avatar_url`` is working as intended.
    
    Parameters
    ----------
    input_value : `None | int`
        Value to serialize.
    
    defaults : `bool`
        Whether default values should be serialized as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_avatar_url(input_value, {}, defaults)
