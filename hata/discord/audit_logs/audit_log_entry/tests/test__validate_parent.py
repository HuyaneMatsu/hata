import vampytest

from ...audit_log import AuditLog

from ..fields import validate_parent


def _iter_options__passing():
    yield None, None
    
    audit_log = AuditLog()
    
    yield audit_log, audit_log


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_parent(input_value):
    """
    Tests whether `validate_parent` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | AuditLog`
    
    Raises
    ------
    TypeError
    """
    return validate_parent(input_value)
