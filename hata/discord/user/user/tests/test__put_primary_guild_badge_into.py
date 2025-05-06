import vampytest

from ....bases import Icon, IconType
from ....guild import GuildBadge

from ..fields import put_primary_guild_badge


def _iter_options():
    guild_badge = GuildBadge(guild_id = 202405180001, icon = Icon(IconType.static, 2))
    
    yield (None, False, {})
    yield (None, True, {'primary_guild': None})
    yield (guild_badge, False, {'primary_guild': guild_badge.to_data()})
    yield (guild_badge, True, {'primary_guild': guild_badge.to_data(defaults = True)})


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_primary_guild_badge(input_value, defaults):
    """
    Tests whether ``put_primary_guild_badge`` is working as intended.
    
    Parameters
    ----------
    input_value : `None | GuildBadge`
        Value to serialise.
    
    defaults : `bool`
        Whether fields with their default value should be included.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_primary_guild_badge(input_value, {}, defaults)
