import vampytest

from ..fields import validate_type
from ..preinstanced import AuditLogEntryType


def _iter_options():
    yield None, AuditLogEntryType.none
    yield AuditLogEntryType.channel_update, AuditLogEntryType.channel_update
    yield AuditLogEntryType.channel_update.value, AuditLogEntryType.channel_update


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_type__passing(input_value):
    """
    Tests whether ``validate_type`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : ``AuditLogEntryType``
    """
    output = validate_type(input_value)
    vampytest.assert_instance(output, AuditLogEntryType)
    return output


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
@vampytest.call_with('ayaya')
def test__validate_type__type_error(input_value):
    """
    Tests whether ``validate_type`` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Raises
    ------
    TypeError
    """
    validate_type(input_value)
