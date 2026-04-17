import vampytest

from ..fields import put_type
from ..preinstanced import AuditLogEntryType


def _iter_options():
    yield AuditLogEntryType.channel_update, False, {'action_type': AuditLogEntryType.channel_update.value}
    yield AuditLogEntryType.channel_update, True, {'action_type': AuditLogEntryType.channel_update.value}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_type(input_value, defaults):
    """
    Tests whether ``put_type`` is working as intended.
    
    Parameters
    ----------
    input_value : ``AuditLogEntryType``
        Input value.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_type(input_value, {}, defaults)
