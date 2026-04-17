import vampytest

from ..helpers import guess_scheduled_event_entity_type_from_keyword_parameters
from ..preinstanced import ScheduledEventEntityType


def _iter_options():
    yield {}, ScheduledEventEntityType.none
    yield {'location': None}, ScheduledEventEntityType.location
    yield {'speaker_ids': None}, ScheduledEventEntityType.stage


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__guess_scheduled_event_entity_type_from_keyword_parameters(input_data):
    """
    Tests whether ``guess_scheduled_event_entity_type_from_keyword_parameters`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to guess from.
    
    Returns
    -------
    output : ``ScheduledEventEntityType``
    """
    output = guess_scheduled_event_entity_type_from_keyword_parameters(input_data)
    vampytest.assert_instance(output, ScheduledEventEntityType)
    return output
