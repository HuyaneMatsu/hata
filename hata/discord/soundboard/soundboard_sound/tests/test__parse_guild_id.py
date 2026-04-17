import vampytest

from ..fields import parse_guild_id


def _iter_options():
    guild_id = 202305240000
    
    yield {}, 0
    yield {'guild_id': None}, 0
    yield {'guild_id': str(guild_id)}, guild_id


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_guild_id(input_data):
    """
    Tests whether ``parse_guild_id`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to try to parse the guild identifier from.
    
    Returns
    -------
    output : `int`
    """
    return parse_guild_id(input_data)
