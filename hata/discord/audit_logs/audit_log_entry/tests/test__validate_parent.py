import vampytest

from ...audit_log import AuditLog

from ..fields import validate_parent


def _iter_options():
    yield None, None
    
    audit_log = AuditLog(None)
    
    yield audit_log, audit_log


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_parent__passing(input_value):
    """
    Tests whether `validate_parent` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | AuditLog`
    """
    return validate_parent(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
def test__validate_parent__type_error(input_value):
    """
    Tests whether `validate_parent` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Raises
    ------
    TypeError
    """
    validate_parent(input_value)
