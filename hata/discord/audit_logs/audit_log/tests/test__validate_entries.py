import vampytest

from ...audit_log_entry import AuditLogEntry, AuditLogEntryType

from ..fields import validate_entries


def _iter_options__passing():
    entry_id_0 = 202406270015
    entry_id_1 = 202406270016
    guild_id = 202406270017
    
    entry_0 = AuditLogEntry.precreate(entry_id_0, entry_type = AuditLogEntryType.guild_update, guild_id = guild_id)
    entry_1 = AuditLogEntry.precreate(entry_id_1, entry_type = AuditLogEntryType.guild_update, guild_id = guild_id)

    yield None, None
    yield [], None
    yield [entry_0], [entry_0]
    yield (
        [entry_0, entry_0],
        [entry_0],
    )
    yield (
        [entry_1, entry_0],
        [entry_0, entry_1],
    )
    yield (
        [entry_0, entry_1],
        [entry_0, entry_1],
    )


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_entries(input_value):
    """
    Validates whether ``validate_entries`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `None | list<AuditLogEntry>`
    
    Raises
    ------
    TypeError
    """
    output = validate_entries(input_value)
    vampytest.assert_instance(output, list, nullable = True)
    return output
