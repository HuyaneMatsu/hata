import vampytest

from ..role import Role
from ..utils import create_partial_role_from_id


def test__create_partial_role_from_id():
    """
    Tests whether ``create_partial_role_from_id`` works as intended.
    """
    role_id = 202211050000
    guild_id = 202211050001
    
    role = create_partial_role_from_id(role_id, guild_id)
    vampytest.assert_instance(role, Role)
    
    vampytest.assert_eq(role.id, role_id)
    vampytest.assert_eq(role.guild_id, guild_id)
    
    test_role = create_partial_role_from_id(role_id, guild_id)
    vampytest.assert_is(role, test_role)
