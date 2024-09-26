import vampytest

from ....component import ComponentType

from ...interaction_component import InteractionComponent

from ..fields import validate_components


def _iter_options__passing():
    component_0 = InteractionComponent(custom_id = 'fury')
    component_1 = InteractionComponent(
        component_type = ComponentType.row,
        components = [InteractionComponent(custom_id = 'Rose')],
    )
    
    yield None, None
    yield [], None
    yield [component_0], (component_0, )
    yield [component_1, component_0], (component_1, component_0)


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_components(input_value):
    """
    Tests whether `validate_components` works as intended.
    
    Returns
    -------
    output : `None | tuple<InteractionComponent>`
    
    Raises
    ------
    TypeError
    """
    output = validate_components(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output
