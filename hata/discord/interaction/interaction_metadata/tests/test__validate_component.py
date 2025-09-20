import vampytest

from ....component import ComponentType, InteractionComponent

from ..fields import validate_component


def _iter_options__passing():
    interaction_component__text_input = InteractionComponent(
        ComponentType.text_input,
        custom_id = 'fury',
    )
    
    yield (
        None,
        None,
    )
    
    yield (
        interaction_component__text_input,
        interaction_component__text_input,
    )


def _iter_options__type_error():
    yield 12.6

@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_component(input_value):
    """
    Tests whether ``validate_component`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : ``None | InteractionComponent``
    
    Raises
    ------
    TypeError
    """
    output = validate_component(input_value)
    vampytest.assert_instance(output, InteractionComponent, nullable = True)
    return output
