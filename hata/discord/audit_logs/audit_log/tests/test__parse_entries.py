import vampytest

from ...audit_log_change import AuditLogChange
from ...audit_log_entry import AuditLogEntry, AuditLogEntryType

from ..audit_log import AuditLog
from ..fields import parse_entries


def _iter_options():
    guild_id = 202406240018
    entry_id_0 = 202406240015
    entry_id_1 = 202406240016
    entry_id_2 = 202406240017
    
    entry_0 = AuditLogEntry.precreate(
        entry_id_0,
        entry_type = AuditLogEntryType.none,
        guild_id = guild_id,
    )
    entry_1 = AuditLogEntry.precreate(
        entry_id_1,
        entry_type = AuditLogEntryType.guild_update,
        changes = [AuditLogChange('name', before = 'okuu', after = 'orin')],
        guild_id = guild_id,
    )
    entry_2 = AuditLogEntry.precreate(
        entry_id_2,
        entry_type = AuditLogEntryType.guild_update,
        changes = [AuditLogChange('name', before = 'orin', after = 'okuu')],
        guild_id = guild_id,
    )
    
    yield (
        {},
        guild_id,
        None,
    )
    
    yield (
        {
            'audit_log_entries': [],
        },
        guild_id,
        None,
    )
    
    yield (
        {
            'audit_log_entries': [
                entry_0.to_data(defaults = True),
            ],
        },
        guild_id,
        None,
    )
    
    yield (
        {
            'audit_log_entries': [
                entry_0.to_data(defaults = True),
                entry_1.to_data(defaults = True),
                entry_2.to_data(defaults = True),
            ],
        },
        guild_id,
        [
            entry_1,
            entry_2,
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_entries(input_data, guild_id):
    """
    Tests whether ``parse_entries`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    guild_id : `int`
        Respective guild's identifier.
    
    Returns
    -------
    output : `None | list<ClientAuditLogEntryBase>`
    """
    parent = AuditLog({}, guild_id = guild_id)
    output = parse_entries(input_data, parent)
    
    vampytest.assert_instance(output, list, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_is(element.parent, parent)
    
    return output
