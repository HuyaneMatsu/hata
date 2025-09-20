import vampytest

from ....component import Component, ComponentType, InteractionComponent

from ..message_component import InteractionMetadataMessageComponent


def test__InteractionMetadataMessageComponent__repr():
    """
    Tests whether ``InteractionMetadataMessageComponent.__repr__`` works as intended.
    """
    component = InteractionComponent(
        ComponentType.string_select,
        custom_id = 'Inaba',
        values = ['black', 'rock', 'shooter'],
    )
    
    interaction_metadata = InteractionMetadataMessageComponent(
        component = component,
    )
    
    output = repr(interaction_metadata)
    vampytest.assert_instance(output, str)


def test__InteractionMetadataMessageComponent__hash():
    """
    Tests whether ``InteractionMetadataMessageComponent.__hash__`` works as intended.
    """
    component = InteractionComponent(
        ComponentType.string_select,
        custom_id = 'Inaba',
        values = ['black', 'rock', 'shooter'],
    )
    
    interaction_metadata = InteractionMetadataMessageComponent(
        component = component,
    )
    
    output = hash(interaction_metadata)
    vampytest.assert_instance(output, int)


def test__InteractionMetadataMessageComponent__eq__different_type():
    """
    Tests whether ``InteractionMetadataMessageComponent.__eq__`` works as intended.
    
    Case: different type.
    """
    interaction_metadata = InteractionMetadataMessageComponent()
    vampytest.assert_ne(interaction_metadata, object())


def _iter_options__eq():
    component = InteractionComponent(
        ComponentType.string_select,
        custom_id = 'Inaba',
        values = ['black', 'rock', 'shooter'],
    )
    
    keyword_parameters = {
        'component': component,
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
            'component': InteractionComponent(
                component_type = ComponentType.button,
                custom_id = 'Reisen',
            ),
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__InteractionMetadataMessageComponent__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``InteractionMetadataMessageComponent.__eq__`` works as intended.
    
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
    interaction_metadata_0 = InteractionMetadataMessageComponent(**keyword_parameters_0)
    interaction_metadata_1 = InteractionMetadataMessageComponent(**keyword_parameters_1)
    
    output = interaction_metadata_0 == interaction_metadata_1
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__eq__component():
    component_type = ComponentType.button
    custom_id = 'Inaba'
    
    keyword_parameters = {
        'component_type': component_type,
        'custom_id': custom_id,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        {
            **keyword_parameters,
            'component_type': ComponentType.user_select,
            
        },
        keyword_parameters,
        False,
    )
    
    yield (
        {
            **keyword_parameters,
            'custom_id': 'Reisen',
        },
        keyword_parameters,
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq__component()).returning_last())
def test__InteractionMetadataMessageComponent__eq__component(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``InteractionMetadataMessageComponent.__eq__`` works as intended.
    
    Case: With component.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create component with.
    """
    interaction_metadata = InteractionMetadataMessageComponent(
        component = InteractionComponent(**keyword_parameters_0),
    )
    component = Component(**keyword_parameters_1)
    
    output = interaction_metadata == component
    vampytest.assert_instance(output, bool)
    return output
