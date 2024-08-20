import vampytest

from ..fields import validate_entity_type
from ..preinstanced import ScheduledEventEntityType


def _iter_options__passing():
    yield None, ScheduledEventEntityType.none
    yield ScheduledEventEntityType.stage, ScheduledEventEntityType.stage
    yield ScheduledEventEntityType.stage.value, ScheduledEventEntityType.stage


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_entity_type(input_value):
    """
    Validates whether ``validate_entity_type`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : ``ScheduledEventEntityType``
    
    Raises
    ------
    TypeError
    """
    output = validate_entity_type(input_value)
    vampytest.assert_instance(output, ScheduledEventEntityType)
    return output
