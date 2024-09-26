import vampytest

from ....component import Component, ComponentType

from ..fields import validate_components


def _iter_options__passing():
    component_0 = Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Hell')])
    component_1 = Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Rose')])
    
    yield None, None
    yield [], None
    yield [component_0], (component_0, )
    yield [component_1, component_0], (component_1, component_0)


def _iter_options__type_error():
    yield 12.6


def _iter_options__value_error():
    component_0 = Component(ComponentType.button, label = 'hello')
    
    yield [component_0]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_components(input_value):
    """
    Tests whether `validate_components` works as intended.
    
    Returns
    -------
    output : `None | tuple<Component>`
    
    Raises
    ------
    TypeError
    ValueError
    """
    output = validate_components(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output
