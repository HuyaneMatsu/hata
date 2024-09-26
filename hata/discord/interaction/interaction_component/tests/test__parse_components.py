import vampytest

from ....component import ComponentType

from ..fields import parse_components
from ..interaction_component import InteractionComponent


def _iter_options():
    component_0 = InteractionComponent(custom_id = 'requiem')
    component_1 = InteractionComponent(
        component_type = ComponentType.row,
        components = [InteractionComponent(custom_id = 'rose')],
    )
    
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
    output : `None | tuple<InteractionComponent>`
    """
    output = parse_components(input_data)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output
