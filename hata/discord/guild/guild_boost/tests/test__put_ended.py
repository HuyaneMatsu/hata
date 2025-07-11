import vampytest

from ..fields import put_ended


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
            'ended': False,
        },
    )
    
    yield (
        True,
        False,
        {
            'ended': True,
        },
    )
    
    yield (
        True,
        True,
        {
            'ended': True
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_ended(input_value, defaults):
    """
    Tests whether ``put_ended`` works as intended.
    
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
    return put_ended(input_value, {}, defaults)
