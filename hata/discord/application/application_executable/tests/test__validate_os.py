import vampytest

from ..fields import validate_os
from ..preinstanced import OperationSystem


def test__validate_os__0():
    """
    Tests whether ``validate_os`` works as intended.
    """
    for input_value, expected_output in (
        (OperationSystem.linux, OperationSystem.linux.value),
        (OperationSystem.linux.value, OperationSystem.linux.value),
    ):
        output = validate_os(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_os__1():
    """
    Tests whether `validate_os` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_os(input_value)
