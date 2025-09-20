import vampytest

from ...component import ComponentType
from ...interaction_component import InteractionComponent

from ..row import InteractionComponentMetadataRow

from .test__InteractionComponentMetadataRow__constructor import _assert_fields_set


def test__InteractionComponentMetadataRow__copy():
    """
    Tests whether ``InteractionComponentMetadataRow.copy`` works as intended.
    """
    interaction_components = [
        InteractionComponent(
            ComponentType.text_input,
            custom_id = 'koishi',
        ),
        InteractionComponent(
            ComponentType.text_input,
            custom_id = 'smart',
        ),
    ]
    
    interaction_component_metadata = InteractionComponentMetadataRow(
        components = interaction_components,
    )
    
    copy = interaction_component_metadata.copy()
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, interaction_component_metadata)
    vampytest.assert_eq(copy, interaction_component_metadata)


def test__InteractionComponentMetadataRow__copy_with__no_fields():
    """
    Tests whether ``InteractionComponentMetadataRow.copy_with`` works as intended.
    
    Case: no fields given.
    """
    interaction_components = [
        InteractionComponent(
            ComponentType.text_input,
            custom_id = 'koishi',
        ),
        InteractionComponent(
            ComponentType.text_input,
            custom_id = 'smart',
        ),
    ]
    
    interaction_component_metadata = InteractionComponentMetadataRow(
        components = interaction_components,
    )
    
    copy = interaction_component_metadata.copy_with()
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, interaction_component_metadata)
    vampytest.assert_eq(copy, interaction_component_metadata)


def test__InteractionComponentMetadataRow__copy_with__all_fields():
    """
    Tests whether ``InteractionComponentMetadataRow.copy_with`` works as intended.
    
    Case: all fields given.
    """
    old_interaction_components = [
        InteractionComponent(
            ComponentType.text_input,
            custom_id = 'koishi',
        ),
        InteractionComponent(
            ComponentType.text_input,
            custom_id = 'smart',
        ),
    ]
    
    new_interaction_components = [
        InteractionComponent(
            ComponentType.text_input,
            custom_id = 'koishi',
        ),
        InteractionComponent(
            ComponentType.text_input,
            custom_id = 'smug',
        ),
    ]
    
    interaction_component_metadata = InteractionComponentMetadataRow(
        components = old_interaction_components,
    )
    
    copy = interaction_component_metadata.copy_with(
        components = new_interaction_components,
    )
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, interaction_component_metadata)
    vampytest.assert_ne(copy, interaction_component_metadata)
    
    vampytest.assert_eq(copy.components, tuple(new_interaction_components))


def test__InteractionComponentMetadataRow__copy_with_keyword_parameters__no_fields():
    """
    Tests whether ``InteractionComponentMetadataRow.copy_with_keyword_parameters`` works as intended.
    
    Case: no fields given.
    """
    interaction_components = [
        InteractionComponent(
            ComponentType.text_input,
            custom_id = 'koishi',
        ),
        InteractionComponent(
            ComponentType.text_input,
            custom_id = 'smart',
        ),
    ]
    
    interaction_component_metadata = InteractionComponentMetadataRow(
        components = interaction_components,
    )
    
    copy = interaction_component_metadata.copy_with_keyword_parameters({})
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, interaction_component_metadata)
    vampytest.assert_eq(copy, interaction_component_metadata)


def test__InteractionComponentMetadataRow__copy_with_keyword_parameters__all_fields():
    """
    Tests whether ``InteractionComponentMetadataRow.copy_with_keyword_parameters`` works as intended.
    
    Case: all fields given.
    """
    old_interaction_components = [
        InteractionComponent(
            ComponentType.text_input,
            custom_id = 'koishi',
        ),
        InteractionComponent(
            ComponentType.text_input,
            custom_id = 'smart',
        ),
    ]
    
    new_interaction_components = [
        InteractionComponent(
            ComponentType.text_input,
            custom_id = 'koishi',
        ),
        InteractionComponent(
            ComponentType.text_input,
            custom_id = 'smug',
        ),
    ]
    
    interaction_component_metadata = InteractionComponentMetadataRow(
        components = old_interaction_components,
    )
    
    copy = interaction_component_metadata.copy_with_keyword_parameters({
        'components': new_interaction_components,
    })
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, interaction_component_metadata)
    vampytest.assert_ne(copy, interaction_component_metadata)
    
    vampytest.assert_eq(copy.components, tuple(new_interaction_components))


def _iter_options__iter_custom_ids_and_values():
    yield (
        {},
        [],
    )
    
    yield (
        {
            'components': [
                InteractionComponent(
                    ComponentType.text_input,
                    custom_id = 'koishi',
                    value = 'smart',
                ),
                InteractionComponent(
                    ComponentType.text_input,
                    custom_id = 'satori',
                    value = 'smug'
                ),
            ],
        },
        [
            (
                'koishi',
                ComponentType.text_input,
                'smart',
            ),
            (
                'satori',
                ComponentType.text_input,
                'smug',
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_custom_ids_and_values()).returning_last())
def test__InteractionComponentMetadataRow__iter_custom_ids_and_values(keyword_parameters):
    """
    Tests whether ``InteractionComponentMetadataRow.iter_custom_ids_and_values`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `list<(str, ComponentType, None | str | tuple<str>)>`
    """
    interaction_component_metadata = InteractionComponentMetadataRow(**keyword_parameters)
    
    return [*interaction_component_metadata.iter_custom_ids_and_values()]
