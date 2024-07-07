from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...guild_incidents import GuildIncidents

from ..fields import put_incidents_into


def _iter_options():
    timestamp = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield None, False, {'incidents_data': None}
    yield None, True, {'incidents_data': None}
    
    incidents = GuildIncidents(invites_disabled_until = timestamp)
    
    yield incidents, False, {'incidents_data': incidents.to_data(defaults = False, include_internals = True)}
    yield incidents, True, {'incidents_data': incidents.to_data(defaults = True, include_internals = True)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_incidents_into(input_value, defaults):
    """
    Tests whether ``put_incidents_into`` works as intended.
    
    Parameters
    ----------
    input_value : `None | GuildIncidents`
        Value to serialise.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_incidents_into(input_value, {}, defaults)
