import vampytest

from ...audit_log import AuditLog

from ..fields import parse_guild_id


def _iter_options():
    guild_id = 202310180012
    audit_log = AuditLog(guild_id = 202310180012)
    
    yield {}, None, 0
    yield {}, audit_log, guild_id
    yield {'guild_id': None}, None, 0
    yield {'guild_id': str(guild_id)}, None, guild_id


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_guild_id(input_data, parent):
    """
    Tests whether ``parse_guild_id`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to try to parse the guild identifier from.
    parent : `None | AuditLog`
        The entry's parent.
    
    Returns
    -------
    output : `int`
    """
    return parse_guild_id(input_data, parent)
