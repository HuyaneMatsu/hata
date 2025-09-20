import vampytest

from ...component import ComponentType
from ...interaction_component import InteractionComponent

from ..fields import parse_component


def _iter_options():
    interaction_component = InteractionComponent(
        ComponentType.text_input,
        custom_id = 'requiem',
    )
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'component': None,
        },
        None,
    )
    
    yield (
        {
            'component': interaction_component.to_data(),
        },
        interaction_component,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_component(input_data):
    """
    Tests whether ``parse_component`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``None | InteractionComponent``
    """
    output = parse_component(input_data)
    vampytest.assert_instance(output, InteractionComponent, nullable = True)
    return output
