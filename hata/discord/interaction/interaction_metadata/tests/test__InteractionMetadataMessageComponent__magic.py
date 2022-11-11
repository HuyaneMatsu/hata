import vampytest

from ....component import Component, ComponentType
from ....message import Attachment

from ...resolved import Resolved

from ..message_component import InteractionMetadataMessageComponent


def test__InteractionMetadataMessageComponent__repr():
    """
    Tests whether ``InteractionMetadataMessageComponent.__repr__`` works as intended.
    """
    component_type = ComponentType.button
    custom_id = 'Inaba'
    resolved = Resolved(attachments = [Attachment.precreate(202211060050)])
    values = ['black', 'rock', 'shooter']
    
    interaction_metadata = InteractionMetadataMessageComponent(
        component_type = component_type,
        custom_id = custom_id,
        resolved = resolved,
        values = values,
    )
    vampytest.assert_instance(repr(interaction_metadata), str)


def test__InteractionMetadataMessageComponent__hash():
    """
    Tests whether ``InteractionMetadataMessageComponent.__hash__`` works as intended.
    """
    component_type = ComponentType.button
    custom_id = 'Inaba'
    resolved = Resolved(attachments = [Attachment.precreate(202211060051)])
    values = ['black', 'rock', 'shooter']
    
    interaction_metadata = InteractionMetadataMessageComponent(
        component_type = component_type,
        custom_id = custom_id,
        resolved = resolved,
        values = values,
    )
    vampytest.assert_instance(hash(interaction_metadata), int)


def test__InteractionMetadataMessageComponent__eq__0():
    """
    Tests whether ``InteractionMetadataMessageComponent.__eq__`` works as intended.
    
    Case: generic.
    """
    component_type = ComponentType.button
    custom_id = 'Inaba'
    resolved = Resolved(attachments = [Attachment.precreate(202211060052)])
    values = ['black', 'rock', 'shooter']
    
    keyword_parameters = {
        'component_type': component_type,
        'custom_id': custom_id,
        'resolved': resolved,
        'values': values,
    }
    
    interaction_metadata = InteractionMetadataMessageComponent(**keyword_parameters)
    
    vampytest.assert_eq(interaction_metadata, interaction_metadata)
    vampytest.assert_ne(interaction_metadata, object())
    
    for field_custom_id, field_value in (
        ('component_type', ComponentType.row),
        ('custom_id', 'Reisen'),
        ('resolved', None),
        ('values', None),
    ):
        test_interaction_metadata = InteractionMetadataMessageComponent(
            **{**keyword_parameters, field_custom_id: field_value}
        )
        vampytest.assert_ne(interaction_metadata, test_interaction_metadata)


def test__InteractionMetadataMessageComponent__eq__1():
    """
    Tests whether ``InteractionMetadataMessageComponent.__eq__`` works as intended.
    
    Case: With component.
    """
    component_type = ComponentType.button
    custom_id = 'Inaba'
    
    interaction_metadata = InteractionMetadataMessageComponent(
        component_type = component_type,
        custom_id = custom_id,
    )
    
    keyword_parameters = {
        'component_type': component_type,
        'custom_id': custom_id,
    }
    component = Component(**keyword_parameters)
    
    vampytest.assert_eq(interaction_metadata, component)
    for field_custom_id, field_value in (
        ('component_type', ComponentType.user_select),
        ('custom_id', 'Reisen'),
    ):
        component = Component(**{**keyword_parameters, field_custom_id: field_value})
        vampytest.assert_ne(interaction_metadata, component)
