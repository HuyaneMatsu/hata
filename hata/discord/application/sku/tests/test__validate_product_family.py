import vampytest

from ..fields import validate_product_family
from ..preinstanced import SKUProductFamily


def _iter_options__passing():
    yield None, SKUProductFamily.none
    yield SKUProductFamily.boost.value, SKUProductFamily.boost
    yield SKUProductFamily.boost, SKUProductFamily.boost


def _iter_options__type_error():
    yield 'a'
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_product_family(input_value):
    """
    Tests whether `validate_product_family` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    value : ``SKUProductFamily``
    
    Raises
    ------
    TypeError
    """
    output = validate_product_family(input_value)
    vampytest.assert_instance(output, SKUProductFamily)
    return output
