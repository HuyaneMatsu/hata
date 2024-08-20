import vampytest

from ....application import SKU

from ..fields import validate_sku_ids


def _iter_options__passing():
    sku_id_0 = 202303150009
    sku_id_1 = 202303150010
    
    sku_0 = SKU.precreate(sku_id_0)
    sku_1 = SKU.precreate(sku_id_1)
    
    yield None, None
    yield [], None
    yield [sku_id_0, sku_id_1], (sku_id_0, sku_id_1)
    yield [sku_id_1, sku_id_0], (sku_id_0, sku_id_1)
    yield [sku_0, sku_1], (sku_id_0, sku_id_1)
    yield [sku_1, sku_0], (sku_id_0, sku_id_1)


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_sku_ids(input_value):
    """
    Tests whether `validate_sku_ids` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | list<int>`
    
    Raises
    ------
    TypeError
    """
    return validate_sku_ids(input_value)
