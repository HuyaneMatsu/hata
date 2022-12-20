import vampytest

from ...role import Role, RoleManagerType

from ..emoji import Emoji


def test__Emoji__iter_roles():
    """
    Tests whether ``Emoji.iter_roles`` works as intended.
    """
    role_id_0 = 202212190000
    role_id_1 = 202212190001
    role_0 = Role.precreate(role_id_0)
    role_1 = Role.precreate(role_id_1)
    
    for emoji, expected_output in (
        (Emoji.precreate(202212190002, roles = None), []),
        (Emoji.precreate(202212190003, roles = [role_id_0]), [role_0]),
        (Emoji.precreate(202212190004, roles = [role_id_0, role_id_1]), [role_0, role_1]),
    ):
        vampytest.assert_eq([*emoji.iter_roles()], expected_output)


def test__Emoji__is_premium():
    """
    Tests whether ``Emoji.is_premium`` works as intended.
    """
    role_id_0 = 202212190005
    role_id_1 = 202212190006
    
    role_0 = Role.precreate(role_id_0)
    role_1 = Role.precreate(role_id_1, manager_type = RoleManagerType.subscription)
    
    for emoji, expected_output in (
        (Emoji.precreate(202212190007, roles = None), False),
        (Emoji.precreate(202212190008, roles = [role_id_0]), False),
        (Emoji.precreate(202212190009, roles = [role_id_1]), True),
    ):
        vampytest.assert_eq(emoji.is_premium(), expected_output)
