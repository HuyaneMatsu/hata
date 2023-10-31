import vampytest

from ...audit_log_change import AuditLogChange
from ...audit_log_change.flags import FLAG_IS_ADDITION, FLAG_IS_MODIFICATION, FLAG_IS_REMOVAL
from ...audit_log_role import AuditLogRole

from ..fields import parse_changes
from ..preinstanced import AuditLogEntryType


def _iter_options():
    yield {}, AuditLogEntryType.user_kick, None
    yield {'changes': None}, AuditLogEntryType.user_kick, None
    yield {'changes': []}, AuditLogEntryType.user_kick, None
    
    role_0 = AuditLogRole(role_id = 202310290000)
    role_1 = AuditLogRole(role_id = 202310290001)
    
    yield (
        {
            'changes': [
                {
                    'key': '$add',
                    'new_value': [role_0.to_data()],
                },
                {
                    'key': '$remove',
                    'new_value': [role_1.to_data()],
                },
                {
                    'key': 'mute',
                    'old_value': False,
                },
                {
                    'key': 'deaf',
                    'new_value': False,
                },
            ],
        },
        AuditLogEntryType.user_kick,
        {
            'roles': AuditLogChange('roles', FLAG_IS_REMOVAL | FLAG_IS_ADDITION, before = (role_1,), after = (role_0,)),
            'mute': AuditLogChange('mute', FLAG_IS_MODIFICATION, before = False),
            'deaf': AuditLogChange('deaf', FLAG_IS_MODIFICATION, after = False),
        },
    )
    
    yield (
        {
            'changes': [
                {
                    'key': 'asset',
                    'old_value': '',
                    'new_value': '',
                },
            ],
        },
        AuditLogEntryType.sticker_create,
        None,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test_parse_changes(input_data, entry_type):
    """
    Tests whether ``parse_changes`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    entry_type : ``AuditLogEntryType``
        The entry type to parse as.
    
    Returns
    -------
    output : `None | dict<str, AuditLogChange>`
    """
    return parse_changes(input_data, entry_type)
