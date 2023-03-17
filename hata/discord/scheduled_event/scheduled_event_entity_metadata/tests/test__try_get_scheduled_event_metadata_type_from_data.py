import vampytest

from ..base import ScheduledEventEntityMetadataBase
from ..location import ScheduledEventEntityMetadataLocation
from ..stage import ScheduledEventEntityMetadataStage

from ..utils import try_get_scheduled_event_metadata_type_from_data


def test__try_get_scheduled_event_metadata_type_from_data():
    """
    Tests whether ``try_get_scheduled_event_metadata_type_from_data`` works as intended.
    """
    for data, expected_value in (
        ({}, ScheduledEventEntityMetadataBase,),
        ({'location': None}, ScheduledEventEntityMetadataLocation),
        ({'speaker_ids': None}, ScheduledEventEntityMetadataStage),
    ):
        output = try_get_scheduled_event_metadata_type_from_data(data)
        
        vampytest.assert_is(output, expected_value)
