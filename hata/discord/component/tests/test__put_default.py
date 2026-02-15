import vampytest

from ..shared_fields import put_default


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
            'default': False,
        },
    )
    
    yield (
        True,
        False,
        {
            'default': True,
        },
    )
    
    yield (
        True,
        True,
        {
            'default': True
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_default(input_value, defaults):
    """
    Tests whether ``put_default`` works as intended.
    
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
    return put_default(input_value, {}, defaults)
