import vampytest

from ....application import SKU

from ..fields import validate_sku_ids


def _iter_options():
    sku_id_0 = 202310060000
    sku_id_1 = 202310060001
    
    sku_0 = SKU.precreate(sku_id_0)
    sku_1 = SKU.precreate(sku_id_1)
    
    yield None, None
    yield [], None
    yield [sku_id_0, sku_id_1], (sku_id_0, sku_id_1)
    yield [sku_id_1, sku_id_0], (sku_id_0, sku_id_1)
    yield [sku_0, sku_1], (sku_id_0, sku_id_1)
    yield [sku_1, sku_0], (sku_id_0, sku_id_1)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_sku_ids__passing(input_value):
    """
    Tests whether `validate_sku_ids` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | list<int>`
    """
    return validate_sku_ids(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
@vampytest.call_with([12.6])
def test__validate_sku_ids__type_error(input_value):
    """
    Tests whether `validate_sku_ids` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Raises
    ------
    TypeError
    """
    validate_sku_ids(input_value)
