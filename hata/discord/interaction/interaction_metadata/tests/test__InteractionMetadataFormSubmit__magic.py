import vampytest

from ...interaction_component import InteractionComponent

from ..form_submit import InteractionMetadataFormSubmit


def test__InteractionMetadataFormSubmit__repr():
    """
    Tests whether ``InteractionMetadataFormSubmit.__repr__`` works as intended.
    """
    custom_id = 'Inaba'
    components = [InteractionComponent(custom_id = 'Rem')]
    
    interaction_metadata = InteractionMetadataFormSubmit(
        custom_id = custom_id,
        components = components,
    )
    vampytest.assert_instance(repr(interaction_metadata), str)


def test__InteractionMetadataFormSubmit__hash():
    """
    Tests whether ``InteractionMetadataFormSubmit.__hash__`` works as intended.
    """
    custom_id = 'Inaba'
    components = [InteractionComponent(custom_id = 'Rem')]
    
    interaction_metadata = InteractionMetadataFormSubmit(
        custom_id = custom_id,
        components = components,
    )
    vampytest.assert_instance(hash(interaction_metadata), int)


def test__InteractionMetadataFormSubmit__eq():
    """
    Tests whether ``InteractionMetadataFormSubmit.__eq__`` works as intended.
    """
    custom_id = 'Inaba'
    components = [InteractionComponent(custom_id = 'Rem')]
    
    keyword_parameters = {
        'custom_id': custom_id,
        'components': components,
    }
    
    interaction_metadata = InteractionMetadataFormSubmit(**keyword_parameters)
    
    vampytest.assert_eq(interaction_metadata, interaction_metadata)
    vampytest.assert_ne(interaction_metadata, object())
    
    for field_custom_id, field_value in (
        ('custom_id', 'Reisen'),
        ('components', None),
    ):
        test_interaction_metadata = InteractionMetadataFormSubmit(
            **{**keyword_parameters, field_custom_id: field_value}
        )
        vampytest.assert_ne(interaction_metadata, test_interaction_metadata)
