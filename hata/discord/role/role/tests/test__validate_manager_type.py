import vampytest

from ..fields import validate_manager_type
from ..preinstanced import RoleManagerType


def test__validate_manager_type__0():
    """
    Tests whether `validate_manager_type` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (RoleManagerType.bot, RoleManagerType.bot),
        (RoleManagerType.bot.value, RoleManagerType.bot)
    ):
        output = validate_manager_type(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_manager_type__1():
    """
    Tests whether `validate_manager_type` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_manager_type(input_value)
