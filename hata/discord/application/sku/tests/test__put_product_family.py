import vampytest

from ..fields import put_product_family
from ..preinstanced import SKUProductFamily


def _iter_options():
    yield (
        SKUProductFamily.none,
        False,
        {
            'product_line': SKUProductFamily.none.value,
        },
    )
    
    yield (
        SKUProductFamily.none,
        True,
        {
            'product_line': SKUProductFamily.none.value,
        },
    )
    
    yield (
        SKUProductFamily.boost,
        False,
        {
            'product_line': SKUProductFamily.boost.value,
        },
    )
    
    yield (
        SKUProductFamily.boost,
        True,
        {
            'product_line': SKUProductFamily.boost.value,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_product_family(input_value, defaults):
    """
    Tests whether ``put_product_family`` is working as intended.
    
    Parameters
    ----------
    input_value : ``SKUProductFamily``
        Input value.
    
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_product_family(input_value, {}, defaults)
