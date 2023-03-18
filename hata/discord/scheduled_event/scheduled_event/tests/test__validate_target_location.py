import vampytest

from ...scheduled_event_entity_metadata import ScheduledEventEntityMetadataLocation

from ..fields import validate_target_location
from ..preinstanced import ScheduledEventEntityType


def test__validate_target_location__0():
    """
    Tests whether `validate_target_location` works as intended.
    
    Case: passing.
    """
    location = 'hell'
    
    for input_value, expected_output in (
        (
            None,
            (ScheduledEventEntityType.location, ScheduledEventEntityMetadataLocation(), 0),
        ), (
            location,
            (ScheduledEventEntityType.location, ScheduledEventEntityMetadataLocation(location = location), 0),
        ), (
            '',
            (ScheduledEventEntityType.location, ScheduledEventEntityMetadataLocation(), 0),
        )
    ):
        output = validate_target_location(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_target_location__2():
    """
    Tests whether `validate_target_location` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_target_location(input_value)
