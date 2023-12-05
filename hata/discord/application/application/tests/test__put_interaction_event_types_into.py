import vampytest

from ..fields import put_interaction_event_types_into
from ..preinstanced import ApplicationInteractionEventType


def _iter_options():
    yield (None, False, {'interactions_event_types': []})
    yield (None, True, {'interactions_event_types': []})
    yield (
        (
            ApplicationInteractionEventType.none,
        ),
        False,
        {
            'interactions_event_types': [
                ApplicationInteractionEventType.none.value,
            ],
        },
    )
    yield (
        (
            ApplicationInteractionEventType.none,
        ),
        True,
        {
            'interactions_event_types': [
                ApplicationInteractionEventType.none.value,
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_interaction_event_types_into(input_value, defaults):
    """
    Tests whether ``put_interaction_event_types_into`` is working as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<ApplicationInteractionEventType>`
        The value to serialise.
    defaults : `bool`
        Whether values with their default value should be included in the output as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_interaction_event_types_into(input_value, {}, defaults)
