import vampytest

from ..fields import put_processed


def _iter_options():
    yield (
        0,
        False,
        {
            'processed_users': 0,
        },
    )
    
    yield (
        0,
        True,
        {
            'processed_users': 0,
        },
    )
    
    yield (
        1,
        False,
        {
            'processed_users': 1,
        },
    )
    
    yield (
        1,
        True,
        {
            'processed_users': 1,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_processed(input_value, defaults):
    """
    Tests whether ``put_processed`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        The value to serialise.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_processed(input_value, {}, defaults)
