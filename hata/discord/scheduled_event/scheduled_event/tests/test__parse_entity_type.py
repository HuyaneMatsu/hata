import vampytest

from ..fields import parse_entity_type
from ..preinstanced import ScheduledEventEntityType


def test__parse_entity_type():
    """
    Tests whether ``parse_entity_type`` works as intended.
    """
    for input_data, expected_output in (
        ({}, ScheduledEventEntityType.none),
        ({'entity_type': None}, ScheduledEventEntityType.none),
        ({'entity_type': ScheduledEventEntityType.stage.value}, ScheduledEventEntityType.stage),
    ):
        output = parse_entity_type(input_data)
        vampytest.assert_is(output, expected_output)
