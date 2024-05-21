import vampytest

from ....bases import Icon, IconType

from ...user_clan import UserClan

from ..fields import parse_clan


def _iter_options():
    clan = UserClan(guild_id = 202405180000, icon = Icon(IconType.static, 2))
    
    yield ({}, None)
    yield ({'clan': None}, None)
    yield ({'clan': clan.to_data()}, clan)
    


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_clan(input_data):
    """
    Tests whether ``parse_clan`` works as intended.
    
    Parameters
    ----------
    input_data : dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | UserClan`
    """
    return parse_clan(input_data)
