import vampytest

from ....component import ComponentType, InteractionComponent

from ..form_submit import InteractionMetadataFormSubmit


def _iter_options__iter_components():
    interaction_component_1 = InteractionComponent(
        ComponentType.text_input,
        custom_id = 'negative',
    )
    interaction_component_2 = InteractionComponent(
        ComponentType.text_input,
        custom_id = 'number',
    )
    
    yield (
        {},
        [],
    )
    
    yield (
        {
            'components': [
                interaction_component_1,
            ],
        },
        [
            interaction_component_1,
        ],
    )
    
    yield (
        {
            'components': [
                interaction_component_1,
                interaction_component_2,
            ],
        },
        [
            interaction_component_1,
            interaction_component_2,
        ],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_components()).returning_last())
def test__InteractionMetadataFormSubmit__iter_components(keyword_parameters):
    """
    Tests whether ``InteractionMetadataFormSubmit.iter_components`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : ``list<InteractionComponent>``
    """
    interaction_metadata = InteractionMetadataFormSubmit(**keyword_parameters)
    
    output = [*interaction_metadata.iter_components()]
    
    for element in output:
        vampytest.assert_instance(element, InteractionComponent)
    
    return output


def _iter_options__iter_custom_ids_and_values():
    interaction_component_0 = InteractionComponent(
        ComponentType.text_input,
        custom_id = 'negative',
        value = 'kaenbyou',
    )
    interaction_component_1 = InteractionComponent(
        ComponentType.string_select,
        custom_id = 'number',
        values = ['kaenbyou', 'rin'],
    )
    interaction_component_2 = InteractionComponent(
        ComponentType.none,
    )
    interaction_component_3 = InteractionComponent(
        ComponentType.row,
        components = [
            interaction_component_0,
            interaction_component_1,
        ],
    )
    
    yield (
        {
            'components': [
                interaction_component_0,
            ],
        },
        [
            ('negative', ComponentType.text_input, 'kaenbyou'),
        ],
    )
    
    yield (
        {
            'components': [
                interaction_component_1,
            ],
        },
        [
            ('number', ComponentType.string_select, ('kaenbyou', 'rin')),
        ],
    )
    
    yield (
        {
            'components': [
                interaction_component_2,
            ],
        },
        [],
    )
    
    yield (
        {
            'components': [
                interaction_component_3,
            ],
        },
        [
            ('negative', ComponentType.text_input, 'kaenbyou'),
            ('number', ComponentType.string_select, ('kaenbyou', 'rin')),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_custom_ids_and_values()).returning_last())
def test__InteractionMetadataFormSubmit__iter_custom_ids_and_values(keyword_parameters):
    """
    Tests whether ``InteractionMetadataFormSubmit.iter_custom_ids_and_values`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `list<(str, ComponentType, None | str | tuple<str>)>`
    """
    interaction_metadata = InteractionMetadataFormSubmit(**keyword_parameters)
    return [*interaction_metadata.iter_custom_ids_and_values()]
