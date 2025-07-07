import vampytest

from ...sku import SKU

from ..fields import validate_sku


def _iter_options__passing():
    sku = SKU.precreate(
        202507040002,
    )
    
    yield None, None
    yield sku, sku


def _iter_options__type_error():
    yield 12.6
    yield '12'


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_sku(input_value):
    """
    Tests whether `validate_sku` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to validate.
    
    Returns
    -------
    output : ``None | SKU``
    
    Raises
    ------
    TypeError
    """
    output = validate_sku(input_value)
    vampytest.assert_instance(output, SKU, nullable = True)
    return output
