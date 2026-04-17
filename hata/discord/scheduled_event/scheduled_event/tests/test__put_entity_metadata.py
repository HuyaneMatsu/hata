import vampytest

from ...scheduled_event_entity_metadata import ScheduledEventEntityMetadataBase, ScheduledEventEntityMetadataLocation

from ..fields import put_entity_metadata


def _iter_options():
    entity_metadata = ScheduledEventEntityMetadataLocation(location = 'Koishi Wonderland')
    
    yield ScheduledEventEntityMetadataBase(), False, {}
    yield ScheduledEventEntityMetadataBase(), True, {'entity_metadata': {}}
    yield entity_metadata, False, {'entity_metadata': entity_metadata.to_data(defaults = False)}
    yield entity_metadata, True, {'entity_metadata': entity_metadata.to_data(defaults = True)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_entity_metadata(input_value, defaults):
    """
    Tests whether ``put_entity_metadata`` is working as intended.
    
    Parameters
    ----------
    input_value : ``ScheduledEventEntityMetadataBase``
        Value to serialize.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_entity_metadata(input_value, {}, defaults)
