import vampytest

from .....component import Component, ComponentType, create_button, create_row 

from ..components import CONVERSION_COMPONENTS


def _iter_options__set_type_processor__passing():
    component_0 = create_button('hey', custom_id = '12')

    yield component_0, [create_row(component_0)]
    yield create_row(component_0), [create_row(component_0)]


def _iter_options__set_type_processor__value_error():
    component_0 = Component(ComponentType.none)
    
    # Cannot be nested
    yield component_0


@vampytest._(vampytest.call_from(_iter_options__set_type_processor__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__set_type_processor__value_error()).raising(ValueError))
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
    
    Raises
    ------
    ValueError
    """
    return CONVERSION_COMPONENTS.set_type_processor(input_value)


def _iter_options__set_validator__passing():
    component_0 = create_button('hey', custom_id = '12')
    component_1 = create_button('mister', custom_id = '13')
    
    yield object(), []
    yield [1], []
    yield [component_0, 1], []
    
    yield None, [None]
    yield [], [None]
    yield [[]], [[create_row()]]
    
    yield component_0, [[create_row(component_0)]]
    yield create_row(component_0), [[create_row(component_0)]]
    
    
    yield [component_0], [[create_row(component_0)]]
    yield [create_row(component_0)], [[create_row(component_0)]]
    yield [component_0, component_1], [[create_row(component_0), create_row(component_1)]]
    yield [[component_0]], [[create_row(component_0)]]
    yield [[component_0, component_1]], [[create_row(component_0, component_1)]]
    yield [create_row(component_0), create_row(component_1)], [[create_row(component_0), create_row(component_1)]]


def _iter_options__set_validator__value_error():
    component_0 = Component(ComponentType.none)
    component_1 = create_button('hey', custom_id = '12')
    
    # Cannot be nested
    yield component_0
    
    # Double nested should be rejected
    yield [[create_row(component_1)]]


@vampytest._(vampytest.call_from(_iter_options__set_validator__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__set_validator__value_error()).raising(ValueError))
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
    
    Raises
    ------
    ValueError
    """
    return [*CONVERSION_COMPONENTS.set_validator(input_value)]


def _iter_options__serializer_optional():
    component_0 = create_button('hey', custom_id = '12')
    component_1 = create_button('mister', custom_id = '13')
    
    yield None, []
    
    yield [create_row(component_0)], [[create_row(component_0).to_data()]]
    yield (
        [create_row(component_0), create_row(component_1)],
        [[create_row(component_0).to_data(), create_row(component_1).to_data()]],
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
    component_0 = create_button('hey', custom_id = '12')
    component_1 = create_button('mister', custom_id = '13')
    
    yield None, []
    
    yield [create_row(component_0)], [create_row(component_0).to_data()]
    yield (
        [create_row(component_0), create_row(component_1)],
        [create_row(component_0).to_data(), create_row(component_1).to_data()],
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
