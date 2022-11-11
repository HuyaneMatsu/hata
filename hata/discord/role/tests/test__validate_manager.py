import vampytest

from ..fields import validate_manager
from ..preinstanced import RoleManagerType


def test__validate_manager__0():
    """
    Tests whether ``validate_manager`` works as intended.
    
    Case: Passing.
    """
    entity_id = 202211020003
    
    for input_value, expected_output in (
        (None, (RoleManagerType.none, 0)),
        ((RoleManagerType.unset, 0), (RoleManagerType.unset, 0)),
        ((RoleManagerType.bot, entity_id), (RoleManagerType.bot, entity_id)),
        ((RoleManagerType.bot, str(entity_id)), (RoleManagerType.bot, entity_id)),
    ):
        output = validate_manager(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_manager__1():
    """
    Tests whether ``validate_manager`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
        (),
        (RoleManagerType.unset, 12.6),
        (12.6, 0),
    ):
        with vampytest.assert_raises(TypeError):
            validate_manager(input_value)
