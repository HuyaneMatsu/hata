import vampytest

from ....guild import Guild

from ..fields import parse_guild


def _iter_options():
    guild_id = 202307290011
    guild = Guild.precreate(guild_id)
    
    yield {}, None
    yield {'guild': None}, None
    yield {'guild': {'id': str(guild_id)}}, guild
    yield {'guild_id': None}, None
    yield {'guild_id': str(guild_id)}, guild


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_guild(input_data):
    """
    Tests whether ``parse_guild`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``None | Guild``
    """
    output = parse_guild(input_data)
    vampytest.assert_instance(output, Guild, nullable = True)
    return output
