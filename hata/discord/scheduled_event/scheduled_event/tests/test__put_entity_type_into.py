import vampytest

from ..fields import put_entity_type_into
from ..preinstanced import ScheduledEventEntityType


def _iter_options():
    yield ScheduledEventEntityType.none, False, {'entity_type': ScheduledEventEntityType.none.value}
    yield ScheduledEventEntityType.none, True, {'entity_type': ScheduledEventEntityType.none.value}
    yield ScheduledEventEntityType.stage, False, {'entity_type': ScheduledEventEntityType.stage.value}
    yield ScheduledEventEntityType.stage, True, {'entity_type': ScheduledEventEntityType.stage.value}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_entity_type_into(input_value, defaults):
    """
    Tests whether ``put_entity_type_into`` works as intended.
    
    Parameters
    ----------
    input_value : ``ScheduledEventEntityType``
        Value to serialize.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_entity_type_into(input_value, {}, defaults)
