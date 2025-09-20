import vampytest

from ....component import ComponentType, InteractionComponent

from ..fields import put_component


def _iter_options():
    interaction_component = InteractionComponent(
        ComponentType.text_input,
        custom_id = 'Hell',
    )

    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {},
    )
    
    yield (
        interaction_component,
        False,
        {
            'data': interaction_component.to_data(),
        },
    )
    
    yield (
        interaction_component,
        True,
        {
            'data': interaction_component.to_data(defaults = True),
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_component(input_value, defaults):
    """
    Tests whether ``put_component`` works as intended.
    
    Parameters
    ----------
    input_value : ``None | tuple<InteractionComponent>``
        The component to serialize.
    
    defaults : `bool`
        Whether field as their default should included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_component(input_value, {}, defaults)
