import vampytest

from .....component import create_button, create_row 

from ..components import CONVERSION_COMPONENTS


def _iter_options__set_type_processor():
    button_0 = create_button('hey', custom_id = '12')

    yield button_0, [create_row(button_0)]
    yield create_row(button_0), [create_row(button_0)]


@vampytest._(vampytest.call_from(_iter_options__set_type_processor()).returning_last())
def test__CONVERSION_COMPONENTS__set_type_processor(input_value):
    """
    Tests whether ``CONVERSION_COMPONENTS.set_type_processor`` works as intended.
    
    Parameters
    ----------
    input_value : ``Component``
        Value to test.
    
    Returns
    -------
    output : `list<Component>`
    """
    return CONVERSION_COMPONENTS.set_type_processor(input_value)


def _iter_options__set_validator():
    button_0 = create_button('hey', custom_id = '12')
    button_1 = create_button('mister', custom_id = '13')
    
    yield object(), []
    yield [1], []
    yield [button_0, 1], []
    
    yield None, [None]
    yield [], [None]
    yield [[]], [[create_row()]]
    
    yield button_0, [[create_row(button_0)]]
    yield create_row(button_0), [[create_row(button_0)]]
    
    
    yield [button_0], [[create_row(button_0)]]
    yield [create_row(button_0)], [[create_row(button_0)]]
    yield [button_0, button_1], [[create_row(button_0), create_row(button_1)]]
    yield [[button_0]], [[create_row(button_0)]]
    yield [[button_0, button_1]], [[create_row(button_0, button_1)]]
    yield [create_row(button_0), create_row(button_1)], [[create_row(button_0), create_row(button_1)]]


@vampytest._(vampytest.call_from(_iter_options__set_validator()).returning_last())
def test__CONVERSION_COMPONENTS__set_validator(input_value):
    """
    Tests whether ``CONVERSION_COMPONENTS.set_validator`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test.
    
    Returns
    -------
    output : `list<None | list<Component>>`
    """
    return [*CONVERSION_COMPONENTS.set_validator(input_value)]


def _iter_options__serializer_optional():
    button_0 = create_button('hey', custom_id = '12')
    button_1 = create_button('mister', custom_id = '13')
    
    yield None, []
    
    yield [create_row(button_0)], [[create_row(button_0).to_data()]]
    yield (
        [create_row(button_0), create_row(button_1)],
        [[create_row(button_0).to_data(), create_row(button_1).to_data()]],
    )


@vampytest._(vampytest.call_from(_iter_options__serializer_optional()).returning_last())
def test__CONVERSION_COMPONENTS__serializer_optional(input_value):
    """
    Tests whether ``CONVERSION_COMPONENTS.serializer_optional`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<Component>`
        Value to test.
    
    Returns
    -------
    output : `list<list<dict<str, object>>>`
    """
    return [*CONVERSION_COMPONENTS.serializer_optional(input_value)]


def _iter_options__serializer_required():
    button_0 = create_button('hey', custom_id = '12')
    button_1 = create_button('mister', custom_id = '13')
    
    yield None, []
    
    yield [create_row(button_0)], [create_row(button_0).to_data()]
    yield (
        [create_row(button_0), create_row(button_1)],
        [create_row(button_0).to_data(), create_row(button_1).to_data()],
    )


@vampytest._(vampytest.call_from(_iter_options__serializer_required()).returning_last())
def test__CONVERSION_COMPONENTS__serializer_required(input_value):
    """
    Tests whether ``CONVERSION_COMPONENTS.serializer_required`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<Component>`
        Value to test.
    
    Returns
    -------
    output : `list<dict<str, object>>`
    """
    return CONVERSION_COMPONENTS.serializer_required(input_value)
