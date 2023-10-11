import vampytest

from ....interaction import Resolved

from ...attachment import Attachment

from ..fields import validate_resolved


def _iter_options():
    entity_id = 202310110004
    resolved = Resolved(attachments = [Attachment.precreate(entity_id)])
    
    yield (None, None)
    yield (resolved, resolved)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_resolved__passing(input_value):
    """
    Tests whether ``validate_resolved`` works as intended.
    
    Case: Passing.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `None | Resolved`
    """
    return validate_resolved(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
def test__validate_resolved__type_error(input_value):
    """
    Tests whether ``validate_resolved`` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Raises
    ------
    TypeError
    """
    validate_resolved(input_value)
