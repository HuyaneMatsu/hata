import vampytest

from ..fields import parse_type
from ..preinstanced import AuditLogEntryType


def _iter_options():
    yield {}, AuditLogEntryType.none
    yield {'action_type': AuditLogEntryType.channel_update.value}, AuditLogEntryType.channel_update


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_type(input_data):
    """
    Tests whether ``parse_type`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data.
    
    Returns
    -------
    output : ``AuditLogEntryType``
    """
    output = parse_type(input_data)
    vampytest.assert_instance(output, AuditLogEntryType)
    return output
