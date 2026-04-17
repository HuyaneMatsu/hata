from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...guild_incidents import GuildIncidents

from ..fields import validate_incidents


def _iter_options():
    timestamp = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield None, None
    
    incidents = GuildIncidents(invites_disabled_until = timestamp)
    
    yield incidents, incidents


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_incidents__passing(input_value):
    """
    Tests whether ``validate_incidents`` works as intended.
    
    Case: Passing.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | GuildIncidents`
    """
    return validate_incidents(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with('aya')
def test__validate_incidents__type_error(input_value):
    """
    Tests whether ``validate_incidents`` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Raises
    ------
    TypeError
    """
    return validate_incidents(input_value)
