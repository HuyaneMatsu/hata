import vampytest

from ..fields import validate_interaction_event_types
from ..preinstanced import ApplicationInteractionEventType


def _iter_options__passing():
    yield None, None
    yield [], None
    yield ApplicationInteractionEventType.none, (ApplicationInteractionEventType.none, )
    yield ApplicationInteractionEventType.none.value, (ApplicationInteractionEventType.none, )
    yield [ApplicationInteractionEventType.none], (ApplicationInteractionEventType.none, )
    yield [ApplicationInteractionEventType.none.value], (ApplicationInteractionEventType.none, )
    yield (
        [ApplicationInteractionEventType.none, ApplicationInteractionEventType.none],
        (ApplicationInteractionEventType.none,),
    )


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_interaction_event_types(input_value):
    """
    Tests whether `validate_interaction_event_types` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `None | tuple<ApplicationInteractionEventType>
    
    Raises
    ------
    TypeError
    """
    return validate_interaction_event_types(input_value)
