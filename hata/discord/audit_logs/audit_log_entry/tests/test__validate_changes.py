import vampytest

from ...audit_log_change import AuditLogChange
from ...audit_log_change.flags import FLAG_IS_ADDITION, FLAG_IS_MODIFICATION, FLAG_IS_REMOVAL
from ...audit_log_role import AuditLogRole

from ..fields import validate_changes
from ..preinstanced import AuditLogEntryType


def _iter_options__passing():
    yield None, None
    yield [], None
    
    role_0 = AuditLogRole(role_id = 202310290006)
    role_1 = AuditLogRole(role_id = 202310290007)
    
    yield (
        [
            AuditLogChange('roles', FLAG_IS_REMOVAL | FLAG_IS_ADDITION, before = [role_1,], after = [role_0,]),
            AuditLogChange('mute', FLAG_IS_MODIFICATION, before = False),
            AuditLogChange('deaf', FLAG_IS_MODIFICATION, after = False),
        ],
        {
            'roles': AuditLogChange('roles', FLAG_IS_REMOVAL | FLAG_IS_ADDITION, before = (role_1,), after = (role_0,)),
            'mute': AuditLogChange('mute', FLAG_IS_MODIFICATION, before = False),
            'deaf': AuditLogChange('deaf', FLAG_IS_MODIFICATION, after = False),
        },
    )
    
    yield [AuditLogChange('koishi', 0)], {'koishi': AuditLogChange('koishi', 0)}


def _iter_options__type_error():
    yield 12.6
    yield [12.6]
    yield [AuditLogChange('mute', FLAG_IS_MODIFICATION, before = 12.6)]


def _iter_options__value_error():
    yield [AuditLogChange('koishi', FLAG_IS_MODIFICATION)]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_changes(input_value):
    """
    Tests whether ``validate_changes`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | dict<str, AuditLogChange>`
    
    Raises
    ------
    TypeError
    ValueError
    """
    return validate_changes(input_value, entry_type = AuditLogEntryType.user_kick)
