import vampytest

from ...sku import SKU

from ..fields import put_sku


def _iter_options():
    sku = SKU.precreate(
        202507040001,
    )
    
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'sku': None,
        },
    )
    
    yield (
        sku,
        False,
        {
            'sku': sku.to_data(defaults = False, include_internals = True)
        },
    )
    
    yield (
        sku,
        True,
        {
            'sku': sku.to_data(defaults = True, include_internals = True),
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_sku(input_value, defaults):
    """
    Tests whether ``put_sku`` works as intended.
    
    Parameters
    ----------
    input_value : ``None | SKU``
        The value to serialise.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_sku(input_value, {}, defaults)
