import vampytest

from ....role import Role

from ...interaction_event import InteractionEvent

from ..fields import parse_roles


def test__parse_roles():
    """
    Tests whether ``parse_roles`` works as intended.
    """
    role_id = 202211050015
    guild_id = 202211050016
    role_name = 'Faker'
    
    interaction_event = InteractionEvent(guild_id = guild_id)
    
    role = Role.precreate(
        role_id,
        name = role_name,
    )
    
    for input_value, expected_output in (
        ({}, None),
        ({'roles': {}}, None),
        (
            {
                'roles': {
                    str(role_id): role.to_data(defaults = True, include_internals = True),
                }
            },
            {
                role_id: role,
            }
        )
    ):
        output = parse_roles(input_value, interaction_event)
        vampytest.assert_eq(output, expected_output)
