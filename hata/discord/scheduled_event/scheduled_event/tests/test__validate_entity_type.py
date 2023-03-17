import vampytest

from ..fields import validate_entity_type
from ..preinstanced import ScheduledEventEntityType


def test__validate_entity_type__0():
    """
    Tests whether `validate_entity_type` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, ScheduledEventEntityType.none),
        (ScheduledEventEntityType.stage, ScheduledEventEntityType.stage),
        (ScheduledEventEntityType.stage.value, ScheduledEventEntityType.stage)
    ):
        output = validate_entity_type(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_entity_type__1():
    """
    Tests whether `validate_entity_type` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_entity_type(input_value)
