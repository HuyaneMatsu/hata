import vampytest

from ....component import ComponentType
from ....message import Attachment

from ...resolved import Resolved

from ..message_component import InteractionMetadataMessageComponent


def _check_is_all_field_set(interaction_metadata):
    """
    Checks whether all fields of the given interaction metadata are set.
    
    Parameters
    ----------
    interaction_metadata : ``InteractionMetadataMessageComponent``
        The interaction metadata to check.
    """
    vampytest.assert_instance(interaction_metadata, InteractionMetadataMessageComponent)
    vampytest.assert_instance(interaction_metadata.component_type, ComponentType)
    vampytest.assert_instance(interaction_metadata.custom_id, str, nullable = True)
    vampytest.assert_instance(interaction_metadata.resolved, Resolved, nullable = True)
    vampytest.assert_instance(interaction_metadata.values, tuple, nullable = True)


def test__InteractionMetadataMessageComponent__new__0():
    """
    Tests whether ``InteractionMetadataMessageComponent.__new__`` works as intended.
    
    Case: No fields given.
    """
    interaction_metadata = InteractionMetadataMessageComponent()
    _check_is_all_field_set(interaction_metadata)


def test__InteractionMetadataMessageComponent__new__1():
    """
    Tests whether ``InteractionMetadataMessageComponent.__new__`` works as intended.
    
    Case: All fields given.
    """
    component_type = ComponentType.button
    custom_id = 'Inaba'
    resolved = Resolved(attachments = [Attachment.precreate(202211060047)])
    values = ['black', 'rock', 'shooter']
    
    interaction_metadata = InteractionMetadataMessageComponent(
        component_type = component_type,
        custom_id = custom_id,
        resolved = resolved,
        values = values,
    )
    _check_is_all_field_set(interaction_metadata)
    
    vampytest.assert_eq(interaction_metadata.component_type, component_type)
    vampytest.assert_eq(interaction_metadata.custom_id, custom_id)
    vampytest.assert_eq(interaction_metadata.resolved, resolved)
    vampytest.assert_eq(interaction_metadata.values, tuple(values))
    

def test__InteractionMetadataMessageComponent__create_empty():
    """
    Tests whether ``InteractionMetadataMessageComponent._create_empty`` works as intended.
    """
    interaction_metadata = InteractionMetadataMessageComponent._create_empty()
    _check_is_all_field_set(interaction_metadata)
