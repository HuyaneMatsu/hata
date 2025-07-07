import vampytest

from ..fields import put_primary


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
            'is_primary': False,
        },
    )
    
    yield (
        True,
        False,
        {
            'is_primary': True,
        },
    )
    
    yield (
        True,
        True,
        {
            'is_primary': True
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_primary(input_value, defaults):
    """
    Tests whether ``put_primary`` works as intended.
    
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
    return put_primary(input_value, {}, defaults)
