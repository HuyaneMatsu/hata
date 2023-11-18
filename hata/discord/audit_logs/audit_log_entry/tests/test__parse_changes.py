import vampytest

from ....application_command import (
    ApplicationCommandPermissionOverwrite, ApplicationCommandPermissionOverwriteTargetType
)
from ....core import BUILTIN_EMOJIS
from ....emoji import Emoji

from ...audit_log_change import AuditLogChange
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
            'roles': AuditLogChange(
                'roles',
                before = (role_1,),
                after = (role_0,),
            ),
            'mute': AuditLogChange('mute', before = False),
            'deaf': AuditLogChange('deaf', after = False),
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

    emoji_0 = BUILTIN_EMOJIS['x']
    emoji_1 = Emoji.precreate(202311140000)
    
    yield (
        {
            'changes': [
                {
                    'key': 'emoji_name',
                    'old_value': emoji_0.unicode,
                },
                {
                    'key': 'emoji_id',
                    'new_value': str(emoji_1.id),
                },
            ],
        },
        AuditLogEntryType.soundboard_sound_create,
        {
            'emoji': AuditLogChange(
                'emoji',
                before = emoji_0,
                after = emoji_1,
            ),
        },
    )

    permission_overwrite_0 = ApplicationCommandPermissionOverwrite(
        (ApplicationCommandPermissionOverwriteTargetType.role, 202311180000), True
    )
    permission_overwrite_1 = ApplicationCommandPermissionOverwrite(
        (ApplicationCommandPermissionOverwriteTargetType.role, 202311180000), False
    )
    permission_overwrite_2 = ApplicationCommandPermissionOverwrite(
        (ApplicationCommandPermissionOverwriteTargetType.role, 202311180001), True
    )
    permission_overwrite_3 = ApplicationCommandPermissionOverwrite(
        (ApplicationCommandPermissionOverwriteTargetType.role, 202311180002), False
    )
    
    yield (
        {
            'changes': [
                {
                    'key': str(permission_overwrite_0.target_id),
                    'old_value': permission_overwrite_0.to_data(),
                    'new_value': permission_overwrite_1.to_data(),
                },
                {
                    'key': str(permission_overwrite_2.target_id),
                    'old_value': permission_overwrite_2.to_data(),
                },
                {
                    'key': str(permission_overwrite_3.target_id),
                    'new_value': permission_overwrite_3.to_data(),
                },
            ],
        },
        AuditLogEntryType.application_command_permission_update,
        {
            'permission_overwrites': AuditLogChange(
                'permission_overwrites',
                before = (permission_overwrite_0, permission_overwrite_2),
                after = (permission_overwrite_1, permission_overwrite_3),
            ),
        },
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
