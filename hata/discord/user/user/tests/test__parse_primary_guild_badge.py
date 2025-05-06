import vampytest

from ....bases import Icon, IconType
from ....guild import GuildBadge

from ..fields import parse_primary_guild_badge


def _iter_options():
    guild_badge = GuildBadge(guild_id = 202405180000, icon = Icon(IconType.static, 2))
    
    yield ({}, None)
    yield ({'primary_guild': None}, None)
    yield ({'primary_guild': guild_badge.to_data()}, guild_badge)
    


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_primary_guild_badge(input_data):
    """
    Tests whether ``parse_primary_guild_badge`` works as intended.
    
    Parameters
    ----------
    input_data : dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | GuildBadge`
    """
    output = parse_primary_guild_badge(input_data)
    vampytest.assert_instance(output, GuildBadge, nullable = True)
    return output
