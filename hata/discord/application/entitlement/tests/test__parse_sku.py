import vampytest

from ...sku import SKU

from ..fields import parse_sku


def _iter_options():
    sku = SKU.precreate(
        202507040000,
    )
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'sku': None,
        },
        None,
    )
    
    yield (
        {
            'sku': sku.to_data(include_internals = True),
        },
        sku,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_sku(input_data):
    """
    Tests whether ``parse_sku`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``None | SKU``
    """
    output = parse_sku(input_data)
    vampytest.assert_instance(output, SKU, nullable = True)
    return output
