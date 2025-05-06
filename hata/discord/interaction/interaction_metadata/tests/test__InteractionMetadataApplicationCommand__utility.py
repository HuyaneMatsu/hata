import vampytest

from ....application_command import ApplicationCommandTargetType
from ....message import Attachment, Message

from ...interaction_option import InteractionOption
from ...resolved import Resolved

from ..application_command import InteractionMetadataApplicationCommand

from .test__InteractionMetadataApplicationCommand__constructor import _assert_fields_set


def test__InteractionMetadataApplicationCommand__copy():
    """
    Tests whether ``InteractionMetadataApplicationCommand.copy`` works as intended.
    """
    application_command_id = 202211060034
    name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    resolved = Resolved(attachments = [Attachment.precreate(202211060035)])
    target_id = 202211060036
    target_type = ApplicationCommandTargetType.user
    
    interaction_metadata = InteractionMetadataApplicationCommand(
        application_command_id = application_command_id,
        name = name,
        options = options,
        resolved = resolved,
        target_id = target_id,
        target_type = target_type,
    )
    copy = interaction_metadata.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, interaction_metadata)
    vampytest.assert_eq(copy, interaction_metadata)


def test__InteractionMetadataApplicationCommand__copy_with__0():
    """
    Tests whether ``InteractionMetadataApplicationCommand.copy_with`` works as intended.
    
    Case: No fields given.
    """
    application_command_id = 202211060037
    name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    resolved = Resolved(attachments = [Attachment.precreate(202211060038)])
    target_id = 202211060039
    target_type = ApplicationCommandTargetType.user
    
    interaction_metadata = InteractionMetadataApplicationCommand(
        application_command_id = application_command_id,
        name = name,
        options = options,
        resolved = resolved,
        target_id = target_id,
        target_type = target_type,
    )
    copy = interaction_metadata.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, interaction_metadata)
    vampytest.assert_eq(copy, interaction_metadata)


def test__InteractionMetadataApplicationCommand__copy_with__1():
    """
    Tests whether ``InteractionMetadataApplicationCommand.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_application_command_id = 202211060040
    old_name = 'Inaba'
    old_options = [InteractionOption(name = 'Rem')]
    old_resolved = Resolved(attachments = [Attachment.precreate(202211060042)])
    old_target_id = 202211060044
    old_target_type = ApplicationCommandTargetType.user
    
    new_application_command_id = 202211060041
    new_name = 'Reisen'
    new_options = [InteractionOption(name = 'Diablo')]
    new_resolved = Resolved(messages = [Message.precreate(202211060043)])
    new_target_id = 202211060045
    new_target_type = ApplicationCommandTargetType.user
    
    interaction_metadata = InteractionMetadataApplicationCommand(
        application_command_id = old_application_command_id,
        name = old_name,
        options = old_options,
        resolved = old_resolved,
        target_id = old_target_id,
        target_type = old_target_type,
    )
    copy = interaction_metadata.copy_with(
        application_command_id = new_application_command_id,
        name = new_name,
        options = new_options,
        resolved = new_resolved,
        target_id = new_target_id,
        target_type = new_target_type,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, interaction_metadata)
    
    vampytest.assert_eq(copy.id, new_application_command_id)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.options, tuple(new_options))
    vampytest.assert_eq(copy.resolved, new_resolved)
    vampytest.assert_eq(copy.target_id, new_target_id)
    vampytest.assert_is(copy.target_type, new_target_type)
