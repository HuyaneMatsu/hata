import vampytest

from ..fields import validate_details
from ..preinstanced import AuditLogEntryType


def _iter_options__passing():
    yield None, None
    yield {}, None
    
    yield (
        {'users_removed': 1},
        {'users_removed': 1},
    )


def _iter_options__type_error():
    yield 12.6
    yield {12.6: 'owo'}


def _iter_options__value_error():
    yield {'users_removed': -1}
    yield {'owo': 12.6}


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_details(input_value):
    """
    Tests whether ``validate_details`` works as intended.
    
    Parameters
    ----------
    input_value : `None | dict<str, object>`
        Value to validate.
    
    Returns
    -------
    output : `None | dict<str, object>`
    
    Raises
    ------
    TypeError
    ValueError
    """
    return validate_details(input_value, entry_type = AuditLogEntryType.guild_update)
