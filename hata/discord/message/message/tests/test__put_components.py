import vampytest

from ....component import Component, ComponentType

from ..fields import put_components


def _iter_options():
    component_0 = Component(ComponentType.button, label = 'Hell')
    component_1 = Component(ComponentType.row, components = [Component(ComponentType.button, label = 'Rose')])

    yield (
        None,
        False,
        False,
        {},
    )
    
    yield (
        None,
        True,
        False,
        {
            'components': [],
        },
    )
    
    yield (
        (
            component_0,
        ),
        False,
        False,
        {
            'components': [
                component_0.to_data(defaults = False, include_internals = False),
            ],
        },
    )
    
    yield (
        (
            component_0,
        ),
        True,
        False,
        {
            'components': [
                component_0.to_data(defaults = True, include_internals = False),
            ],
        },
    )
    
    yield (
        (
            component_0,
            component_1,
        ),
        False,
        False,
        {
            'components': [
                component_0.to_data(defaults = False, include_internals = False),
                component_1.to_data(defaults = False, include_internals = False),
            ],
        },
    )
    
    yield (
        (
            component_0,
            component_1,
        ),
        True,
        False,
        {
            'components': [
                component_0.to_data(defaults = True, include_internals = False),
                component_1.to_data(defaults = True, include_internals = False),
            ],
        },
    )
    
    yield (
        (
            component_0,
            component_1,
        ),
        True,
        True,
        {
            'components': [
                component_0.to_data(defaults = True, include_internals = True),
                component_1.to_data(defaults = True, include_internals = True),
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_components(input_value, defaults, include_internals):
    """
    Tests whether ``put_components`` works as intended.
    
    Parameters
    ----------
    input_value : ``None | tuple<Component>``
        The components to serialize.
    
    defaults : `bool`
        Whether field as their default should included as well.
    
    include_internals : `bool`
        Whether internal fields should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_components(input_value, {}, defaults, include_internals = include_internals)
