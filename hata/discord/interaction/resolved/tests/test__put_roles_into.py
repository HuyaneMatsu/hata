import vampytest

from ....role import Role

from ..fields import put_roles_into


def test__put_roles_into():
    """
    Tests whether ``put_roles_into`` works as intended.
    """
    role_id = 202211050017
    role_name = 'Faker'
    
    role = Role.precreate(
        role_id,
        name = role_name,
    )
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'roles': {}}),
        (
            {
                role_id: role,
            },
                True,
            {
                'roles': {
                    str(role_id): role.to_data(defaults = True, include_internals = True),
                }
            },
        )
    ):
        output = put_roles_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
