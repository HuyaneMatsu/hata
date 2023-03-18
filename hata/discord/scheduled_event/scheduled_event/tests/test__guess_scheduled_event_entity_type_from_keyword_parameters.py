import vampytest

from ..helpers import guess_scheduled_event_entity_type_from_keyword_parameters
from ..preinstanced import ScheduledEventEntityType


def test__guess_scheduled_event_entity_type_from_keyword_parameters():
    """
    Tests whether ``guess_scheduled_event_entity_type_from_keyword_parameters`` works as intended.
    """
    for data, expected_value in (
        ({}, ScheduledEventEntityType.none),
        ({'location': None}, ScheduledEventEntityType.location),
        ({'speaker_ids': None}, ScheduledEventEntityType.stage),
    ):
        output = guess_scheduled_event_entity_type_from_keyword_parameters(data)
        vampytest.assert_is(output, expected_value)
