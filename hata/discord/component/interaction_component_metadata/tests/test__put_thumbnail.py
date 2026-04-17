import vampytest

from ...component import ComponentType
from ...interaction_component import InteractionComponent

from ..fields import put_thumbnail


def _iter_options():
    interaction_component = InteractionComponent(
        ComponentType.button,
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
        {
            'thumbnail': None,
        },
    )
    
    yield (
        interaction_component,
        False,
        {
            'thumbnail': interaction_component.to_data(),
        },
    )
    
    yield (
        interaction_component,
        True,
        {
            'thumbnail': interaction_component.to_data(defaults = True),
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_thumbnail(input_value, defaults):
    """
    Tests whether ``put_thumbnail`` works as intended.
    
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
    return put_thumbnail(input_value, {}, defaults)
