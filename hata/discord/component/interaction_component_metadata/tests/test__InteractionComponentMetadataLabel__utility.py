import vampytest

from ...component import ComponentType
from ...interaction_component import InteractionComponent

from ..label import InteractionComponentMetadataLabel

from .test__InteractionComponentMetadataLabel__constructor import _assert_fields_set


def test__InteractionComponentMetadataLabel__copy():
    """
    Tests whether ``InteractionComponentMetadataLabel.copy`` works as intended.
    """
    interaction_component = InteractionComponent(
        ComponentType.text_input,
        custom_id = 'koishi',
    )
    
    interaction_component_metadata = InteractionComponentMetadataLabel(
        component = interaction_component
    )
    
    copy = interaction_component_metadata.copy()
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, interaction_component_metadata)
    vampytest.assert_eq(copy, interaction_component_metadata)


def test__InteractionComponentMetadataLabel__copy_with__no_fields():
    """
    Tests whether ``InteractionComponentMetadataLabel.copy_with`` works as intended.
    
    Case: no fields given.
    """
    interaction_component = InteractionComponent(
        ComponentType.text_input,
        custom_id = 'koishi',
    )
    
    interaction_component_metadata = InteractionComponentMetadataLabel(
        component = interaction_component,
    )
    
    copy = interaction_component_metadata.copy_with()
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, interaction_component_metadata)
    vampytest.assert_eq(copy, interaction_component_metadata)


def test__InteractionComponentMetadataLabel__copy_with__all_fields():
    """
    Tests whether ``InteractionComponentMetadataLabel.copy_with`` works as intended.
    
    Case: all fields given.
    """
    old_interaction_component = InteractionComponent(
        ComponentType.text_input,
        custom_id = 'koishi',
    )
    
    new_interaction_component = InteractionComponent(
        ComponentType.text_input,
        custom_id = 'satori',
    )
    
    interaction_component_metadata = InteractionComponentMetadataLabel(
        component = old_interaction_component,
    )
    
    copy = interaction_component_metadata.copy_with(
        component = new_interaction_component,
    )
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, interaction_component_metadata)
    vampytest.assert_ne(copy, interaction_component_metadata)
    
    vampytest.assert_eq(copy.component, new_interaction_component)


def test__InteractionComponentMetadataLabel__copy_with_keyword_parameters__no_fields():
    """
    Tests whether ``InteractionComponentMetadataLabel.copy_with_keyword_parameters`` works as intended.
    
    Case: no fields given.
    """
    interaction_component = InteractionComponent(
        ComponentType.text_input,
        custom_id = 'koishi',
    )
    
    interaction_component_metadata = InteractionComponentMetadataLabel(
        component = interaction_component,
    )
    
    copy = interaction_component_metadata.copy_with_keyword_parameters({})
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, interaction_component_metadata)
    vampytest.assert_eq(copy, interaction_component_metadata)


def test__InteractionComponentMetadataLabel__copy_with_keyword_parameters__all_fields():
    """
    Tests whether ``InteractionComponentMetadataLabel.copy_with_keyword_parameters`` works as intended.
    
    Case: all fields given.
    """
    old_interaction_component = InteractionComponent(
        ComponentType.text_input,
        custom_id = 'koishi',
    )
    
    new_interaction_component = InteractionComponent(
        ComponentType.text_input,
        custom_id = 'satori',
    )
    
    interaction_component_metadata = InteractionComponentMetadataLabel(
        component = old_interaction_component,
    )
    
    copy = interaction_component_metadata.copy_with_keyword_parameters({
        'component': new_interaction_component,
    })
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, interaction_component_metadata)
    vampytest.assert_ne(copy, interaction_component_metadata)
    
    vampytest.assert_eq(copy.component, new_interaction_component)


def _iter_options__iter_custom_ids_and_values():
    yield (
        {},
        [],
    )
    
    yield (
        {
            'component': InteractionComponent(
                ComponentType.text_input,
                custom_id = 'koishi',
                value = 'smart',
            ),
        },
        [
            (
                'koishi',
                ComponentType.text_input,
                'smart',
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_custom_ids_and_values()).returning_last())
def test__InteractionComponentMetadataLabel__iter_custom_ids_and_values(keyword_parameters):
    """
    Tests whether ``InteractionComponentMetadataLabel.iter_custom_ids_and_values`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `list<(str, ComponentType, None | str | tuple<str>)>`
    """
    interaction_component_metadata = InteractionComponentMetadataLabel(**keyword_parameters)
    
    return [*interaction_component_metadata.iter_custom_ids_and_values()]
