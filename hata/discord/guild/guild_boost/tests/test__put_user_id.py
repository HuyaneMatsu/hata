import vampytest

from ..fields import put_user_id


def _iter_options():
    user_id = 202507060003
    
    yield (
        0,
        False,
        {
            'user_id': None,
        },
    )
    
    yield (
        0,
        True,
        {
            'user_id': None,
        },
    )
    
    yield (
        user_id,
        False,
        {
            'user_id': str(user_id),
        },
    )
    
    yield (
        user_id,
        True,
        {
            'user_id': str(user_id),
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_user_id(input_value, defaults):
    """
    Tests whether ``put_user_id`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Value to serialise.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_user_id(input_value, {}, defaults)
