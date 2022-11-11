import vampytest

from ....component import ComponentType

from ..fields import validate_type


def test__validate_type__0():
    """
    Tests whether `validate_type` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (ComponentType.row, ComponentType.row),
        (ComponentType.row.value, ComponentType.row)
    ):
        output = validate_type(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_type__1():
    """
    Tests whether `validate_type` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_type(input_value)
