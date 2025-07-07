import vampytest

from ..fields import parse_product_family
from ..preinstanced import SKUProductFamily


def _iter_options():
    yield (
        {},
        SKUProductFamily.none,
    )
    
    yield (
        {
            'product_line': None,
        },
        SKUProductFamily.none,
    )
    
    yield (
        {
            'product_line': SKUProductFamily.boost.value,
        },
        SKUProductFamily.boost,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_product_family(input_data):
    """
    Tests whether ``parse_product_family`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data.
    
    Returns
    -------
    output : ``SKUProductFamily``
    """
    output = parse_product_family(input_data)
    vampytest.assert_instance(output, SKUProductFamily)
    return output
