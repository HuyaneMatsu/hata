import vampytest

from ..fields import put_promotion_id


def _iter_options():
    promotion_id = 202507010000
    
    yield (
        0,
        False,
        {},
    )
    
    yield (
        0,
        True,
        {
            'promotion_id': None,
        },
    )
    
    yield (
        promotion_id,
        False,
        {
            'promotion_id': str(promotion_id),
        },
    )
    
    yield (
        promotion_id,
        True,
        {
            'promotion_id': str(promotion_id),
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_promotion_id(input_value, defaults):
    """
    Tests whether ``put_promotion_id`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Input value to serialize.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_promotion_id(input_value, {}, defaults)
