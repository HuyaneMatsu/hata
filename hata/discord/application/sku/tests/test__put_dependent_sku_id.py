import vampytest

from ..fields import put_dependent_sku_id


def _iter_options():
    dependent_sku_id = 202506290001

    yield (
        0,
        False,
        {
            'dependent_sku_id': None,
        },
    )
    
    yield (
        0,
        True,
        {
            'dependent_sku_id': None,
        },
    )
    
    yield (
        dependent_sku_id,
        False,
        {
            'dependent_sku_id': str(dependent_sku_id),
        },
    )
    
    yield (
        dependent_sku_id,
        True,
        {
            'dependent_sku_id': str(dependent_sku_id),
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_dependent_sku_id(input_value, defaults):
    """
    Tests whether ``put_dependent_sku_id`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        The value to serialise.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_dependent_sku_id(input_value, {}, defaults)
