import vampytest

from ..base import ScheduledEventEntityMetadataBase
from ..location import ScheduledEventEntityMetadataLocation
from ..stage import ScheduledEventEntityMetadataStage

from ..utils import try_get_scheduled_event_metadata_type_from_data


def _iter_options():
    yield {}, ScheduledEventEntityMetadataBase
    yield {'location': None}, ScheduledEventEntityMetadataLocation
    yield {'speaker_ids': None}, ScheduledEventEntityMetadataStage
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__try_get_scheduled_event_metadata_type_from_data(data):
    """
    Tests whether ``try_get_scheduled_event_metadata_type_from_data`` works as intended.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to work with.
    
    Returns
    -------
    output : ``type<ScheduledEventEntityMetadataBase>``
    """
    output = try_get_scheduled_event_metadata_type_from_data(data)
    vampytest.assert_subtype(output, ScheduledEventEntityMetadataBase)
    return output
