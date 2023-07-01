import vampytest

from ..fields import validate_sku_id


def test__validate_sku_id__0():
    """
    Tests whether `validate_sku_id` works as intended.
    
    Case: passing.
    """
    sku_id = 202301040013
    
    for input_value, expected_output in (
        (sku_id, sku_id),
        (str(sku_id), sku_id),
    ):
        output = validate_sku_id(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_sku_id__1():
    """
    Tests whether `validate_sku_id` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        '-1',
        -1,
    ):
        with vampytest.assert_raises(AssertionError, ValueError):
            validate_sku_id(input_value)


def test__validate_sku_id__2():
    """
    Tests whether `validate_sku_id` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_sku_id(input_value)
