import vampytest

from ....role import Role

from ..fields import parse_roles


def _iter_options():
    role_id = 202211050015
    guild_id = 202211050016
    role_name = 'Faker'
    
    role = Role.precreate(
        role_id,
        name = role_name,
    )
    
    
    yield (
        {},
        guild_id,
        None,
    )
    
    yield (
        {
            'roles': {},
        },
        guild_id,
        None,
    )
    
    yield (
        {
            'roles': {
                str(role_id): role.to_data(defaults = True, include_internals = True),
            },
        },
        guild_id,
        {
            role_id: role,
        },
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
