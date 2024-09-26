import vampytest

from ..component import Component, ComponentType
from ..shared_fields import put_components_into


def _iter_options():
    component_0 = Component(ComponentType.button, label = 'Hell')
    component_1 = Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Rose')])

    yield None, False, {'components': []}
    yield None, True, {'components': []}
    
    yield (component_0, ), False, {'components': [component_0.to_data()]}
    yield (component_0, ), True, {'components': [component_0.to_data(defaults = True)]}
    
    yield (
        (component_0, component_1),
        False,
        {'components': [component_0.to_data(), component_1.to_data()]},
    )
    yield (
        (component_0, component_1),
        True,
        {'components': [component_0.to_data(defaults = True), component_1.to_data(defaults = True)]},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_components_into(input_value, defaults):
    """
    Tests whether ``put_components_into`` works as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<Component>`
        The components to serialize.
    
    defaults : `bool`
        Whether field as their default should included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_components_into(input_value, {}, defaults)
