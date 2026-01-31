import vampytest

from ..fields import put_pinned


def _iter_options():
    yield (
        False,
        False,
        {},
    )
    
    yield (
        False,
        True,
        {
            'pinned': False,
        },
    )
    
    yield (
        True,
        False,
        {
            'pinned': True,
        },
    )
    
    yield (
        True,
        True,
        {
            'pinned': True
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_pinned(input_value, defaults):
    """
    Tests whether ``put_pinned`` works as intended.
    
    Parameters
    ----------
    input_value : `bool`
        The value to serialise.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_pinned(input_value, {}, defaults)
