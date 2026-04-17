import vampytest

from ....component import ComponentType, InteractionComponent

from ..message_component import InteractionMetadataMessageComponent

from .test__InteractionMetadataMessageComponent__constructor import _assert_fields_set


def test__InteractionMetadataMessageComponent__copy():
    """
    Tests whether ``InteractionMetadataMessageComponent.copy`` works as intended.
    """
    component = InteractionComponent(
        ComponentType.string_select,
        custom_id = 'Inaba',
        values = ['black', 'rock', 'shooter'],
    )
    
    interaction_metadata = InteractionMetadataMessageComponent(
        component = component,
    )
    copy = interaction_metadata.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, interaction_metadata)
    vampytest.assert_eq(copy, interaction_metadata)


def test__InteractionMetadataMessageComponent__copy_with__no_fields():
    """
    Tests whether ``InteractionMetadataMessageComponent.copy_with`` works as intended.
    
    Case: No fields given.
    """
    component = InteractionComponent(
        ComponentType.string_select,
        custom_id = 'Inaba',
        values = ['black', 'rock', 'shooter'],
    )
    
    interaction_metadata = InteractionMetadataMessageComponent(
        component = component,
    )
    copy = interaction_metadata.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, interaction_metadata)
    vampytest.assert_eq(copy, interaction_metadata)


def test__InteractionMetadataMessageComponent__copy_with__all_fields():
    """
    Tests whether ``InteractionMetadataMessageComponent.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_component = InteractionComponent(
        ComponentType.string_select,
        custom_id = 'Inaba',
        values = ['black', 'rock', 'shooter'],
    )
    
    new_component = InteractionComponent(
        ComponentType.string_select,
        custom_id = 'Reisen',
        values = ['Empress'],
    )
    
    interaction_metadata = InteractionMetadataMessageComponent(
        component = old_component,
    )
    copy = interaction_metadata.copy_with(
        component = new_component,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, interaction_metadata)
    
    vampytest.assert_eq(copy.component, new_component)


def test__InteractionMetadataMessageComponent__copy_with_keyword_parameters__no_fields():
    """
    Tests whether ``InteractionMetadataMessageComponent.copy_with_keyword_parameters`` works as intended.
    
    Case: No fields given.
    """
    interaction_metadata = InteractionMetadataMessageComponent()
    copy = interaction_metadata.copy_with_keyword_parameters({})
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, interaction_metadata)
    vampytest.assert_eq(copy, interaction_metadata)


def test__InteractionMetadataMessageComponent__copy_with_keyword_parameters__all_fields():
    """
    Tests whether ``InteractionMetadataMessageComponent.copy_with_keyword_parameters`` works as intended.
    
    Case: No fields given.
    """
    old_component = InteractionComponent(
        ComponentType.string_select,
        custom_id = 'Inaba',
        values = ['black', 'rock', 'shooter'],
    )
    
    new_component = InteractionComponent(
        ComponentType.string_select,
        custom_id = 'Reisen',
        values = ['Empress'],
    )
    
    interaction_metadata = InteractionMetadataMessageComponent(
        component = old_component,
    )
    
    copy = interaction_metadata.copy_with_keyword_parameters({
        'component': new_component,
    })
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, interaction_metadata)
    vampytest.assert_ne(copy, interaction_metadata)
    
    vampytest.assert_eq(copy.component, new_component)
