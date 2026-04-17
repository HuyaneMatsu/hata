import vampytest

from .....component import create_button, create_row 

from ..components import _is_component_listing


def _iter_options():
    button_0 = create_button('hey', custom_id = '12')
    button_1 = create_button('mister', custom_id = '13')
    
    yield [1], []
    yield [button_0, 1], []
    
    yield [[]], [[create_row()]]
    
    yield [button_0], [[create_row(button_0)]]
    yield [create_row(button_0)], [[create_row(button_0)]]
    yield [button_0, button_1], [[create_row(button_0), create_row(button_1)]]
    yield [[button_0]], [[create_row(button_0)]]
    yield [[button_0, button_1]], [[create_row(button_0, button_1)]]
    yield [create_row(button_0), create_row(button_1)], [[create_row(button_0), create_row(button_1)]]


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__is_component_listing(input_value):
    """
    Tests whether ``_is_component_listing`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test.
    
    Returns
    -------
    output : `list<None | list<Component>>`
    """
    return [*_is_component_listing(input_value)]
