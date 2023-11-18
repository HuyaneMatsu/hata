import vampytest

from ...audit_log_change import AuditLogChange
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
            AuditLogChange(
                'roles',
                before = [role_1,],
                after = [role_0,],
            ),
            AuditLogChange('mute', before = False),
            AuditLogChange('deaf', after = False),
        ],
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


def _iter_options__type_error():
    yield 12.6
    yield [12.6]
    yield [AuditLogChange('mute', before = 12.6)]


def _iter_options__value_error():
    yield [AuditLogChange('koishi')]


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
