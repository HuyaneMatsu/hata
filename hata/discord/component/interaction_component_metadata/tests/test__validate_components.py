import vampytest

from ...component import ComponentType
from ...interaction_component import InteractionComponent

from ..fields import validate_components__row


def _iter_options__passing():
    interaction_component__text_input = InteractionComponent(
        ComponentType.text_input,
        custom_id = 'koishi',
    )
    
    interaction_component__button = InteractionComponent(
        ComponentType.button,
        custom_id = 'koishi',
    )
    
    yield (
        None,
        None,
    )
    
    yield (
        [],
        None,
    )
    
    yield (
        [
            interaction_component__text_input,
        ],
        (
            interaction_component__text_input,
        ),
    )
    
    yield (
        [
            interaction_component__button,
        ],
        (
            interaction_component__button,
        ),
    )


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_components(input_value):
    """
    Tests whether `validate_components__row` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : ``None | tuple<InteractionComponent>``
    
    Raises
    ------
    TypeError
    """
    output = validate_components__row(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, InteractionComponent)
    
    return output
