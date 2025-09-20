import vampytest

from ....message import Attachment
from ....resolved import Resolved

from ..fields import validate_resolved


def _iter_options__passing():
    entity_id = 202211050043
    resolved = Resolved(attachments = [Attachment.precreate(entity_id)])
    
    yield (None, None)
    yield (resolved, resolved)


def _iter_options__type_error():
    yield 12.6

@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_resolved(input_value):
    """
    Tests whether ``validate_resolved`` works as intended.
    
    Case: Passing.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : ``None | Resolved``
    
    Raises
    ------
    TypeError
    """
    output = validate_resolved(input_value)
    vampytest.assert_instance(output, Resolved, nullable = True)
    return output
