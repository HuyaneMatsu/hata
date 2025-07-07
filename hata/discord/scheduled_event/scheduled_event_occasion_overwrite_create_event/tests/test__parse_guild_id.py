import vampytest

from ..fields import parse_guild_id


def _iter_options():
    guild_id = 202506210040
    
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
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_guild_id(input_data)
    vampytest.assert_instance(output, int)
    return output
