import vampytest

from ....application_command import (
    ApplicationCommandPermissionOverwrite, ApplicationCommandPermissionOverwriteTargetType
)

from ...audit_log_change import AuditLogChange
from ...audit_log_role import AuditLogRole

from ..fields import put_changes
from ..preinstanced import AuditLogEntryType


def _iter_options():
    yield None, False, AuditLogEntryType.user_kick, {}
    yield None, True, AuditLogEntryType.user_kick, {'changes': []}
    
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
        'roles': AuditLogChange(
            'roles',
            before = (role_1,),
            after = (role_0,),
        ),
        'mute': AuditLogChange('mute', before = False),
        'deaf': AuditLogChange('deaf', after = False),
    }
    
    yield changes, False, AuditLogEntryType.user_kick, data
    yield changes, True, AuditLogEntryType.user_kick, data


    permission_overwrite_0 = ApplicationCommandPermissionOverwrite(
        (ApplicationCommandPermissionOverwriteTargetType.role, 202311180003), True
    )
    permission_overwrite_1 = ApplicationCommandPermissionOverwrite(
        (ApplicationCommandPermissionOverwriteTargetType.role, 202311180003), False
    )
    permission_overwrite_2 = ApplicationCommandPermissionOverwrite(
        (ApplicationCommandPermissionOverwriteTargetType.role, 202311180004), True
    )
    permission_overwrite_3 = ApplicationCommandPermissionOverwrite(
        (ApplicationCommandPermissionOverwriteTargetType.role, 202311180005), False
    )
    
    data = {
        'changes': [
            {
                'key': str(permission_overwrite_0.target_id),
                'old_value': permission_overwrite_0.to_data(defaults = True),
                'new_value': permission_overwrite_1.to_data(defaults = True),
            },
            {
                'key': str(permission_overwrite_2.target_id),
                'old_value': permission_overwrite_2.to_data(defaults = True),
            },
            {
                'key': str(permission_overwrite_3.target_id),
                'new_value': permission_overwrite_3.to_data(defaults = True),
            },
        ],
    }
    
    changes = {
        'permission_overwrites': AuditLogChange(
            'permission_overwrites',
            before = (permission_overwrite_0, permission_overwrite_2),
            after = (permission_overwrite_1, permission_overwrite_3),
        ),
    }
    
    yield changes, False, AuditLogEntryType.application_command_permission_update, data


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test_put_changes(input_value, defaults, entry_type):
    """
    Tests whether ``put_changes`` works as intended.
    
    Parameters
    ----------
    input_value : `dict<str, object>`
        Data to parse from.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    entry_type : ``AuditLogEntryType``
        The entry type to serialize as.
    
    Returns
    -------
    output : `None | dict<str, AuditLogChange>`
    """
    return put_changes(input_value, {}, defaults, entry_type = entry_type)
