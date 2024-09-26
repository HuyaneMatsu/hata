import vampytest

from ....component import Component, ComponentType

from ..fields import parse_components


def _iter_options():
    component_0 = Component(ComponentType.button, label = 'hello')
    component_1 = Component(ComponentType.row, components = Component(ComponentType.button, label = 'Rose'))
    
    yield {}, None
    yield {'components': None}, None
    yield {'components': []}, None
    yield {'components': [component_0.to_data()]}, (component_0, )
    yield {'components': [component_1.to_data(), component_0.to_data()]}, (component_1, component_0)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_components(input_data):
    """
    Tests whether ``parse_components`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | tuple<Component>`
    """
    output = parse_components(input_data)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output
