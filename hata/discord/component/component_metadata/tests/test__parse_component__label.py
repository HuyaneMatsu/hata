import vampytest

from ...component import Component, ComponentType
from ...string_select_option import StringSelectOption

from ..fields import parse_component__label


def _iter_options():
    component = Component(
        ComponentType.string_select,
        custom_id = 'pudding',
        options = [
            StringSelectOption('bed'),
        ],
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
            'component': component.to_data(include_internals = True),
        },
        component,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_component__label(input_data):
    """
    tests whether ``parse_component__label`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``None | Component``
    """
    output = parse_component__label(input_data)
    vampytest.assert_instance(output, Component, nullable = True)
    return output
