import vampytest

from ...interaction_component import InteractionComponent

from ..form_submit import InteractionMetadataFormSubmit


def _assert_fields_set(interaction_metadata):
    """
    Checks whether all fields of the given interaction metadata are set.
    
    Parameters
    ----------
    interaction_metadata : ``InteractionMetadataFormSubmit``
        The interaction metadata to check.
    """
    vampytest.assert_instance(interaction_metadata, InteractionMetadataFormSubmit)
    vampytest.assert_instance(interaction_metadata.custom_id, str, nullable = True)
    vampytest.assert_instance(interaction_metadata.components, tuple, nullable = True)


def test__InteractionMetadataFormSubmit__new__0():
    """
    Tests whether ``InteractionMetadataFormSubmit.__new__`` works as intended.
    
    Case: No fields given.
    """
    interaction_metadata = InteractionMetadataFormSubmit()
    _assert_fields_set(interaction_metadata)


def test__InteractionMetadataFormSubmit__new__1():
    """
    Tests whether ``InteractionMetadataFormSubmit.__new__`` works as intended.
    
    Case: All fields given.
    """
    custom_id = 'Inaba'
    components = [InteractionComponent(custom_id = 'Rem')]
    
    interaction_metadata = InteractionMetadataFormSubmit(
        custom_id = custom_id,
        components = components,
    )
    _assert_fields_set(interaction_metadata)
    
    vampytest.assert_eq(interaction_metadata.custom_id, custom_id)
    vampytest.assert_eq(interaction_metadata.components, tuple(components))
    

def test__InteractionMetadataFormSubmit__create_empty():
    """
    Tests whether ``InteractionMetadataFormSubmit._create_empty`` works as intended.
    """
    interaction_metadata = InteractionMetadataFormSubmit._create_empty()
    _assert_fields_set(interaction_metadata)
