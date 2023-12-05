import vampytest

from ..fields import parse_interaction_event_types
from ..preinstanced import ApplicationInteractionEventType


def _iter_options():
    yield ({}, None)
    yield ({'interactions_event_types': None}, None)
    yield ({'interactions_event_types': []}, None)
    yield (
        {
            'interactions_event_types': [
                ApplicationInteractionEventType.none.value,
            ],
        },
        (
            ApplicationInteractionEventType.none,
        ),
    )
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_interaction_event_types(input_data):
    """
    Tests whether ``parse_interaction_event_types`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | tuple<ApplicationInteractionEventType>`
    """
    return parse_interaction_event_types(input_data)
