import vampytest

from .....discord.interaction import InteractionEvent

from ..interaction_event import CONVERSION_INTERACTION_EVENT


def _iter_options__set_validator():
    interaction_event = InteractionEvent.precreate(202405190000)
    
    yield object(), []
    yield None, [None]
    yield interaction_event, [interaction_event]


@vampytest._(vampytest.call_from(_iter_options__set_validator()).returning_last())
def test__CONVERSION_INTERACTION_EVENT__set_validator(input_value):
    """
    Tests whether ``CONVERSION_INTERACTION_EVENT.set_validator`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test.
    
    Returns
    -------
    output : `list<None | InteractionEvent>`
    """
    return [*CONVERSION_INTERACTION_EVENT.set_validator(input_value)]
