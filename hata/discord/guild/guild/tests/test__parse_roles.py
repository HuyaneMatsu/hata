import vampytest

from ....role import Role

from ..guild import Guild

from ..fields import parse_roles


def _iter_options():
    role_id = 202306100006
    role_name = 'Koishi'
    
    
    role = Role.precreate(
        role_id,
        name = role_name,
    )
    
    yield {}, {}
    yield {'roles': []}, {}
    yield (
        {'roles': [role.to_data(defaults = True, include_internals = True)]},
        {role_id: role},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_roles(input_value):
    """
    Tests whether ``parse_roles`` works as intended.
    
    Parameters
    ----------
    input_value : `dict<str, object>`
        Value to pass.
    
    Returns
    -------
    output : `dict<int, Role>`
    """
    guild_id = 202306100012
    guild = Guild.precreate(guild_id)
    
    return parse_roles(input_value, guild.roles, guild_id)
