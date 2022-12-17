import vampytest

from ...role_manager_metadata import RoleManagerMetadataBase, RoleManagerMetadataBot

from ..fields import validate_manager
from ..preinstanced import RoleManagerType


def test__validate_manager__0():
    """
    Tests whether ``validate_manager`` works as intended.
    
    Case: Passing.
    """
    manager_metadata = RoleManagerMetadataBot(bot_id = 202211020003)
    
    for input_value, expected_output in (
        (None, (RoleManagerType.none, RoleManagerMetadataBase())),
        ((RoleManagerType.unset, RoleManagerMetadataBase()), (RoleManagerType.unset, RoleManagerMetadataBase())),
        ((RoleManagerType.unset, None), (RoleManagerType.unset, RoleManagerMetadataBase())),
        ((RoleManagerType.bot, manager_metadata), (RoleManagerType.bot, manager_metadata)),
        ((RoleManagerType.bot, None), (RoleManagerType.bot, RoleManagerMetadataBot())),
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
        (RoleManagerType.unset, RoleManagerMetadataBot()),
    ):
        with vampytest.assert_raises(TypeError):
            validate_manager(input_value)
