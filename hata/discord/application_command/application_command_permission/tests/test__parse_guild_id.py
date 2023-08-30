import vampytest

from ..fields import parse_guild_id


def _iter_options():
    role_id = 202302210027
    
    yield {}, 0
    yield {'guild_id': None}, 0
    yield {'guild_id': str(role_id)}, role_id


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
    return parse_guild_id(input_data)
