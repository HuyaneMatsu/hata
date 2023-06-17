import vampytest

from ....role import Role

from ..fields import validate_roles


def test__validate_roles__0():
    """
    Tests whether ``validate_roles`` works as intended.
    
    Case: passing.
    """
    role_id = 202306100008
    role_name = 'Koishi'
    
    role = Role.precreate(
        role_id,
        name = role_name,
    )
    
    for input_value, expected_output in (
        (None, {}),
        ([], {}),
        ({}, {}),
        ([role], {role_id: role}),
        ({role_id: role}, {role_id: role}),
    ):
        output = validate_roles(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_roles__1():
    """
    Tests whether ``validate_roles`` works as intended.
    
    Case: raising.
    """
    for input_value in (
        12.6,
        [12.6],
        {12.6: 12.6},
    ):
        with vampytest.assert_raises(TypeError):
            validate_roles(input_value)
