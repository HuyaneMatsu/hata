import vampytest

from ..fields import parse_entity_type
from ..preinstanced import ScheduledEventEntityType


def _iter_options():
    yield {}, ScheduledEventEntityType.none
    yield {'entity_type': None}, ScheduledEventEntityType.none
    yield {'entity_type': ScheduledEventEntityType.stage.value}, ScheduledEventEntityType.stage


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_entity_type(input_data):
    """
    Tests whether ``parse_entity_type`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``ScheduledEventEntityType``
    """
    output = parse_entity_type(input_data)
    vampytest.assert_instance(output, ScheduledEventEntityType)
    return output
