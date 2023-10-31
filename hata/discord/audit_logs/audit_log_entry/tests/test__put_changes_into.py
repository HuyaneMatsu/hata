import vampytest

from ...audit_log_change import AuditLogChange
from ...audit_log_change.flags import FLAG_IS_ADDITION, FLAG_IS_MODIFICATION, FLAG_IS_REMOVAL
from ...audit_log_role import AuditLogRole

from ..fields import put_changes_into
from ..preinstanced import AuditLogEntryType


def _iter_options():
    yield None, False, {}
    yield None, True, {'changes': []}
    
    role_0 = AuditLogRole(role_id = 202310290002)
    role_1 = AuditLogRole(role_id = 202310290003)
    
    data = {
        'changes': [
            {
                'key': '$remove',
                'new_value': [role_1.to_data(defaults = True)],
            },
            {
                'key': '$add',
                'new_value': [role_0.to_data(defaults = True)],
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
    }
    changes = {
        'roles': AuditLogChange('roles', FLAG_IS_REMOVAL | FLAG_IS_ADDITION, before = (role_1,), after = (role_0,)),
        'mute': AuditLogChange('mute', FLAG_IS_MODIFICATION, before = False),
        'deaf': AuditLogChange('deaf', FLAG_IS_MODIFICATION, after = False),
    }
    
    yield changes, False, data
    yield changes, True, data


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test_put_changes_into(input_value, defaults):
    """
    Tests whether ``put_changes_into`` works as intended.
    
    Parameters
    ----------
    input_value : `dict<str, object>`
        Data to parse from.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    output : `None | dict<str, AuditLogChange>`
    """
    return put_changes_into(input_value, {}, defaults, entry_type = AuditLogEntryType.user_kick)
