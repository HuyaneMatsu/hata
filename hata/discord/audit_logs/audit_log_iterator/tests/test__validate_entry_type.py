import vampytest

from ...audit_log_entry import AuditLogEntryType

from ..fields import validate_entry_type


def _iter_options__passing():
    yield None, AuditLogEntryType.none
    yield AuditLogEntryType.guild_update, AuditLogEntryType.guild_update
    yield AuditLogEntryType.guild_update.value, AuditLogEntryType.guild_update


def _iter_options__type_error():
    yield 12.6
    yield ''


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_entry_type(input_value):
    """
    Tests whether ``validate_entry_type`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value.
    
    Returns
    -------
    output : ``AuditLogEntryType``
    
    Raises
    ------
    TypeError
    """
    output = validate_entry_type(input_value)
    vampytest.assert_instance(output, AuditLogEntryType)
    return output
