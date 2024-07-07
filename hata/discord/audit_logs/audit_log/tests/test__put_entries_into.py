import vampytest

from ...audit_log_change import AuditLogChange
from ...audit_log_entry import AuditLogEntry, AuditLogEntryType

from ..fields import put_entries_into


def _iter_options():
    entry_id_0 = 202406250005
    entry_id_1 = 202406250006
    guild_id = 202406250007
    
    entry_0 = AuditLogEntry.precreate(
        entry_id_0,
        entry_type = AuditLogEntryType.guild_update,
        changes = [AuditLogChange('name', before = 'okuu', after = 'orin')],
        guild_id = guild_id,
    )
    entry_1 = AuditLogEntry.precreate(
        entry_id_1,
        entry_type = AuditLogEntryType.guild_update,
        changes = [AuditLogChange('name', before = 'orin', after = 'okuu')],
        guild_id = guild_id,
    )
    
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'audit_log_entries': [],
        },
    )
    
    yield (
        [
            entry_0,
            entry_1,
        ],
        False,
        {
            'audit_log_entries': [
                entry_0.to_data(defaults = False),
                entry_1.to_data(defaults = False),
            ],
        },
    )
    
    yield (
        [
            entry_0,
            entry_1,
        ],
        True,
        {
            'audit_log_entries': [
                entry_0.to_data(defaults = True),
                entry_1.to_data(defaults = True),
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_entries_into(input_value, defaults):
    """
    Tests whether ``put_entries_into`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<AuditLogEntry>`
        The value to serialise.
    defaults : `bool`
        Whether values with their default value should be included in the output as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_entries_into(input_value, {}, defaults)
