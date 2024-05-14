import vampytest

from ....component import ComponentType
from ....message import Attachment, Message

from ...resolved import Resolved

from ..message_component import InteractionMetadataMessageComponent

from .test__InteractionMetadataMessageComponent__constructor import _check_is_all_field_set


def test__InteractionMetadataMessageComponent__copy():
    """
    Tests whether ``InteractionMetadataMessageComponent.copy`` works as intended.
    """
    component_type = ComponentType.button
    custom_id = 'Inaba'
    resolved = Resolved(attachments = [Attachment.precreate(202211060053)])
    values = ['black', 'rock', 'shooter']
    
    interaction_metadata = InteractionMetadataMessageComponent(
        component_type = component_type,
        custom_id = custom_id,
        resolved = resolved,
        values = values,
    )
    copy = interaction_metadata.copy()
    _check_is_all_field_set(copy)
    vampytest.assert_is_not(copy, interaction_metadata)
    vampytest.assert_eq(copy, interaction_metadata)


def test__InteractionMetadataMessageComponent__copy_with__0():
    """
    Tests whether ``InteractionMetadataMessageComponent.copy_with`` works as intended.
    
    Case: No fields given.
    """
    component_type = ComponentType.button
    custom_id = 'Inaba'
    resolved = Resolved(attachments = [Attachment.precreate(202211060054)])
    values = ['black', 'rock', 'shooter']
    
    interaction_metadata = InteractionMetadataMessageComponent(
        component_type = component_type,
        custom_id = custom_id,
        resolved = resolved,
        values = values,
    )
    copy = interaction_metadata.copy_with()
    _check_is_all_field_set(copy)
    vampytest.assert_is_not(copy, interaction_metadata)
    vampytest.assert_eq(copy, interaction_metadata)


def test__InteractionMetadataMessageComponent__copy_with__1():
    """
    Tests whether ``InteractionMetadataMessageComponent.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_component_type = ComponentType.button
    old_custom_id = 'Inaba'
    old_resolved = Resolved(attachments = [Attachment.precreate(202211060055)])
    old_values = ['black', 'rock', 'shooter']
    
    new_component_type = ComponentType.row
    new_custom_id = 'Reisen'
    new_resolved = Resolved(messages = [Message.precreate(202211060056)])
    new_values = ['Empress']
    
    interaction_metadata = InteractionMetadataMessageComponent(
        component_type = old_component_type,
        custom_id = old_custom_id,
        resolved = old_resolved,
        values = old_values,
    )
    copy = interaction_metadata.copy_with(
        component_type = new_component_type,
        custom_id = new_custom_id,
        resolved = new_resolved,
        values = new_values,
    )
    _check_is_all_field_set(copy)
    vampytest.assert_is_not(copy, interaction_metadata)
    
    vampytest.assert_eq(copy.component_type, new_component_type)
    vampytest.assert_eq(copy.custom_id, new_custom_id)
    vampytest.assert_eq(copy.resolved, new_resolved)
    vampytest.assert_eq(copy.values, tuple(new_values))
