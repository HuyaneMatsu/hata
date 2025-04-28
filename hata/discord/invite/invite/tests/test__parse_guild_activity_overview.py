import vampytest

from ....guild import GuildActivityOverview

from ..fields import parse_guild_activity_overview


def _iter_options():
    guild_id = 202504270000
    guild_activity_overview = GuildActivityOverview.precreate(guild_id)
    
    yield {}, None
    yield {'profile': None}, None
    yield {'profile': {'id': str(guild_id)}}, guild_activity_overview


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_guild_activity_overview(input_data):
    """
    Tests whether ``parse_guild_activity_overview`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``None | Guild``
    """
    output = parse_guild_activity_overview(input_data)
    vampytest.assert_instance(output, GuildActivityOverview, nullable = True)
    return output
