import vampytest

from ...component import Component, ComponentType
from ...string_select_option import StringSelectOption

from ..fields import put_component__label


def _iter_options():
    component = Component(
        ComponentType.string_select,
        custom_id = 'pudding',
        options = [
            StringSelectOption('bed'),
        ],
    )
    
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
            'component': None,
        },
    )
    
    yield (
        component,
        False,
        False,
        {
            'component': component.to_data(defaults = False, include_internals = False),
        },
    )
    
    yield (
        component,
        True,
        False,
        {
            'component': component.to_data(defaults = True, include_internals = False),
        },
    )
    
    yield (
        component,
        False,
        True,
        {
            'component': component.to_data(defaults = False, include_internals = True),
        },
    )
    
    yield (
        component,
        True,
        True,
        {
            'component': component.to_data(defaults = True, include_internals = True),
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_component__label(input_value, defaults, include_internals):
    """
    tests whether ``put_component__label`` works as intended.
    
    Parameters
    ----------
    input_value : ``None | Component``
        value to serialize.
    
    defaults : `bool`
        Whether fields as their defaults should be included as well.
    
    include_internals : `bool`
        Whether internal fields should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_component__label(input_value, {}, defaults, include_internals = include_internals)
