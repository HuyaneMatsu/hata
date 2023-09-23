from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ...guild_incidents import GuildIncidents

from ..fields import parse_incidents


def _iter_options():
    until = DateTime(2016, 5, 14)
    
    yield {}, None
    yield {'incidents_data': None}, None
    yield {'incidents_data': {}}, GuildIncidents()
    yield (
        {'incidents_data': {'invites_disabled_until': datetime_to_timestamp(until)}},
        GuildIncidents(invites_disabled_until = until),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_incidents(input_data):
    """
    Tests whether ``parse_incidents`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | GuildIncidents`
    """
    return parse_incidents(input_data)
