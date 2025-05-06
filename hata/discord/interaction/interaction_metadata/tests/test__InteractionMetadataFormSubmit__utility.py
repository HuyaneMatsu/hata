import vampytest

from ...interaction_component import InteractionComponent

from ..form_submit import InteractionMetadataFormSubmit

from .test__InteractionMetadataFormSubmit__constructor import _assert_fields_set


def test__InteractionMetadataFormSubmit__copy():
    """
    Tests whether ``InteractionMetadataFormSubmit.copy`` works as intended.
    """
    custom_id = 'Inaba'
    components = [InteractionComponent(custom_id = 'Rem')]
    
    interaction_metadata = InteractionMetadataFormSubmit(
        custom_id = custom_id,
        components = components,
    )
    copy = interaction_metadata.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, interaction_metadata)
    vampytest.assert_eq(copy, interaction_metadata)


def test__InteractionMetadataFormSubmit__copy_with__0():
    """
    Tests whether ``InteractionMetadataFormSubmit.copy_with`` works as intended.
    
    Case: No fields given.
    """
    custom_id = 'Inaba'
    components = [InteractionComponent(custom_id = 'Rem')]
    
    interaction_metadata = InteractionMetadataFormSubmit(
        custom_id = custom_id,
        components = components,
    )
    copy = interaction_metadata.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, interaction_metadata)
    vampytest.assert_eq(copy, interaction_metadata)


def test__InteractionMetadataFormSubmit__copy_with__1():
    """
    Tests whether ``InteractionMetadataFormSubmit.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_custom_id = 'Inaba'
    old_components = [InteractionComponent(custom_id = 'Rem')]
    
    new_custom_id = 'Reisen'
    new_components = [InteractionComponent(custom_id = 'Diablo')]
    
    interaction_metadata = InteractionMetadataFormSubmit(
        custom_id = old_custom_id,
        components = old_components,
    )
    copy = interaction_metadata.copy_with(
        custom_id = new_custom_id,
        components = new_components,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, interaction_metadata)
    
    vampytest.assert_eq(copy.custom_id, new_custom_id)
    vampytest.assert_eq(copy.components, tuple(new_components))
