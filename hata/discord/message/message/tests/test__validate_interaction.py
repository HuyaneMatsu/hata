import vampytest

from ...message_interaction import MessageInteraction

from ..fields import validate_interaction


def _iter_options__passing():
    interaction_id = 202304300005
    interaction = MessageInteraction.precreate(interaction_id, name = 'Orin')
    
    yield None, None
    yield interaction, interaction


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_interaction(input_value):
    """
    Tests whether `validate_interaction` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        value to validate.
    
    Returns
    -------
    output : `None | MessageInteraction`
    
    Raises
    ------
    TypeError
    """
    return validate_interaction(input_value)
