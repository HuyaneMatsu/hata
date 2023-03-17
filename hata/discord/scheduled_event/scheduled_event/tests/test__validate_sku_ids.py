import vampytest

from ..fields import validate_sku_ids


def test__validate_sku_ids__0():
    """
    Tests whether `validate_sku_ids` works as intended.
    
    Case: passing.
    """
    sku_id_1 = 202303150009
    sku_id_2 = 202303150010
    
    for input_value, expected_output in (
        (None, None),
        ([], None),
        ([sku_id_2, sku_id_1], (sku_id_1, sku_id_2)),
    ):
        output = validate_sku_ids(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_sku_ids__1():
    """
    Tests whether `validate_sku_ids` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
        [12.6],
    ):
        with vampytest.assert_raises(TypeError):
            validate_sku_ids(input_value)
