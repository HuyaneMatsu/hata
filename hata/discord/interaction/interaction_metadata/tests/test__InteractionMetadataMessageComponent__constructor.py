import vampytest

from ....component import ComponentType, InteractionComponent

from ..message_component import InteractionMetadataMessageComponent


def _assert_fields_set(interaction_metadata):
    """
    Checks whether all fields of the given interaction metadata are set.
    
    Parameters
    ----------
    interaction_metadata : ``InteractionMetadataMessageComponent``
        The interaction metadata to check.
    """
    vampytest.assert_instance(interaction_metadata, InteractionMetadataMessageComponent)
    vampytest.assert_instance(interaction_metadata.component, InteractionComponent, nullable = True)


def test__InteractionMetadataMessageComponent__new__no_fields():
    """
    Tests whether ``InteractionMetadataMessageComponent.__new__`` works as intended.
    
    Case: No fields given.
    """
    interaction_metadata = InteractionMetadataMessageComponent()
    _assert_fields_set(interaction_metadata)


def test__InteractionMetadataMessageComponent__new__all_fields():
    """
    Tests whether ``InteractionMetadataMessageComponent.__new__`` works as intended.
    
    Case: All fields given.
    """
    component = InteractionComponent(
        ComponentType.string_select,
        custom_id = 'Inaba',
        values = ['black', 'rock', 'shooter'],
    )
    
    interaction_metadata = InteractionMetadataMessageComponent(
        component = component,
    )
    _assert_fields_set(interaction_metadata)
    
    vampytest.assert_eq(interaction_metadata.component, component)


def test__InteractionMetadataMessageComponent__from_keyword_parameters__no_fields():
    """
    Tests whether ``InteractionMetadataMessageComponent.from_keyword_parameters`` works as intended.
    
    Case: No fields given.
    """
    interaction_metadata = InteractionMetadataMessageComponent.from_keyword_parameters({})
    _assert_fields_set(interaction_metadata)


def test__InteractionMetadataMessageComponent__from_keyword_parameters__all_fields():
    """
    Tests whether ``InteractionMetadataMessageComponent.from_keyword_parameters`` works as intended.
    
    Case: All fields given.
    """
    component = InteractionComponent(
        ComponentType.string_select,
        custom_id = 'Inaba',
        values = ['black', 'rock', 'shooter'],
    )
    
    interaction_metadata = InteractionMetadataMessageComponent.from_keyword_parameters({
        'component': component,
    })
    _assert_fields_set(interaction_metadata)
    
    vampytest.assert_eq(interaction_metadata.component, component)


def test__InteractionMetadataMessageComponent__create_empty():
    """
    Tests whether ``InteractionMetadataMessageComponent._create_empty`` works as intended.
    """
    interaction_metadata = InteractionMetadataMessageComponent._create_empty()
    _assert_fields_set(interaction_metadata)
