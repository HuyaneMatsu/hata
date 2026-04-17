import vampytest

from ...role_manager_metadata import RoleManagerMetadataBase, RoleManagerMetadataBot

from ..fields import validate_manager_metadata


def test__validate_manager_metadata__0():
    """
    Tests whether `validate_manager_metadata` works as intended.
    
    Case: passing.
    """
    manager_metadata = RoleManagerMetadataBot(bot_id = 202211010017)
    
    for input_value, expected_output in (
        (manager_metadata, manager_metadata),
        (None, RoleManagerMetadataBase()),
    ):
        output = validate_manager_metadata(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_manager_metadata__2():
    """
    Tests whether `validate_manager_metadata` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_manager_metadata(input_value)
