import vampytest

from ...component import Component, ComponentType

from ..interaction_component import InteractionComponent


def test__InteractionComponent__repr():
    """
    Tests whether ``InteractionComponent.__repr__`` works as intended.
    """
    custom_id = 'Worldly'
    component_type = ComponentType.text_input
    value = 'flower land'
    
    interaction_component = InteractionComponent(
        component_type,
        custom_id = custom_id,
        value = value,
    )
    
    vampytest.assert_instance(repr(interaction_component), str)


def test__InteractionComponent__hash():
    """
    Tests whether ``InteractionComponent.__hash__`` works as intended.
    """
    custom_id = 'Worldly'
    component_type = ComponentType.text_input
    value = 'flower land'
    
    interaction_component = InteractionComponent(
        component_type,
        custom_id = custom_id,
        value = value,
    )
    
    vampytest.assert_instance(hash(interaction_component), int)


def _iter_options__eq():
    custom_id = 'Worldly'
    component_type = ComponentType.text_input
    value = 'flower land'
    
    keyword_parameters = {
        'custom_id': custom_id,
        'component_type': component_type,
        'value': value,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'value': 'pudding',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'custom_id': 'flower garden',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            'component_type': ComponentType.string_select,
            'values': ['pudding'],
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__InteractionComponent__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``InteractionComponent.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    interaction_component_0 = InteractionComponent(**keyword_parameters_0)
    interaction_component_1 = InteractionComponent(**keyword_parameters_1)
    
    output = interaction_component_0 == interaction_component_1
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__mod():
    yield (
        {
            'custom_id': 'Worldly',
            'component_type': ComponentType.text_input,
        },
        Component(
            ComponentType.text_input,
            custom_id = 'Worldly'
        ),
        True,
    )
    
    yield (
        {
            'custom_id': 'Worldly',
            'component_type': ComponentType.text_input,
        },
        Component(
            ComponentType.button,
            custom_id = 'Worldly'
        ),
        False,
    )
    
    yield (
        {
            'custom_id': 'Worldly',
            'component_type': ComponentType.text_input,
        },
        Component(
            ComponentType.text_input,
            custom_id = 'Flower'
        ),
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__mod()).returning_last())
def test__InteractionComponent__mod(keyword_parameters, component):
    """
    Tests whether ``InteractionComponent.__mod__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    component : ``Component``
        Component to test with.
    
    Returns
    -------
    output : `bool`
    """
    interaction_component = InteractionComponent(**keyword_parameters)
    
    output = interaction_component % component
    vampytest.assert_instance(output, bool)
    return output
