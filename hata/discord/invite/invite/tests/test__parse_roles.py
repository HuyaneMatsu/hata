import vampytest

from ....role import Role, create_partial_role_data

from ..fields import parse_roles


def _iter_options():
    role_id_0 = 202604040030
    role_id_1 = 202604040031
    guild_id = 202604040032
    role_name = 'Faker'
    
    role_0 = Role.precreate(
        role_id_0,
        name = role_name,
    )
    
    role_1 = Role.precreate(
        role_id_1,
        name = role_name,
    )
    
    
    yield (
        {},
        guild_id,
        None,
    )
    
    yield (
        {
            'roles': [],
        },
        guild_id,
        None,
    )
    
    yield (
        {
            'roles': [
                create_partial_role_data(role_0),
                create_partial_role_data(role_1),
            ],
        },
        guild_id,
        (
            role_0,
            role_1,
        ),
    )
    
    yield (
        {
            'roles': [
                create_partial_role_data(role_1),
                create_partial_role_data(role_0),
            ],
        },
        guild_id,
        (
            role_0,
            role_1,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_roles(input_data, guild_id):
    """
    Tests whether ``parse_roles`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : `None | dict<int, Role>`
    """
    return parse_roles(input_data, guild_id)
