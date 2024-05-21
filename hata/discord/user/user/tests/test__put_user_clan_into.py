import vampytest

from ....bases import Icon, IconType

from ...user_clan import UserClan

from ..fields import put_clan_into


def _iter_options():
    clan = UserClan(guild_id = 202405180001, icon = Icon(IconType.static, 2))
    
    yield (None, False, {})
    yield (None, True, {'clan': None})
    yield (clan, False, {'clan': clan.to_data()})
    yield (clan, True, {'clan': clan.to_data(defaults = True)})


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_clan_into(input_value, defaults):
    """
    Tests whether ``put_clan_into`` is working as intended.
    
    Parameters
    ----------
    input_value : `None | UserClan`
        Value to serialise.
    defaults : `bool`
        Whether fields with their default value should be included.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_clan_into(input_value, {}, defaults)
