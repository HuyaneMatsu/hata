import vampytest

from ....message import Attachment, Message

from ...interaction_option import InteractionOption
from ...resolved import Resolved

from ..application_command import InteractionMetadataApplicationCommand

from .test__InteractionMetadataApplicationCommand__constructor import _check_is_all_field_set


def test__InteractionMetadataApplicationCommand__copy():
    """
    Tests whether ``InteractionMetadataApplicationCommand.copy`` works as intended.
    """
    id_ = 202211060034
    name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    resolved = Resolved(attachments = [Attachment.precreate(202211060035)])
    target_id = 202211060036
    
    interaction_metadata = InteractionMetadataApplicationCommand(
        id = id_,
        name = name,
        options = options,
        resolved = resolved,
        target_id = target_id,
    )
    copy = interaction_metadata.copy()
    _check_is_all_field_set(copy)
    vampytest.assert_is_not(copy, interaction_metadata)
    vampytest.assert_eq(copy, interaction_metadata)


def test__InteractionMetadataApplicationCommand__copy_with__0():
    """
    Tests whether ``InteractionMetadataApplicationCommand.copy_with`` works as intended.
    
    Case: No fields given.
    """
    id_ = 202211060037
    name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    resolved = Resolved(attachments = [Attachment.precreate(202211060038)])
    target_id = 202211060039
    
    interaction_metadata = InteractionMetadataApplicationCommand(
        id = id_,
        name = name,
        options = options,
        resolved = resolved,
        target_id = target_id,
    )
    copy = interaction_metadata.copy_with()
    _check_is_all_field_set(copy)
    vampytest.assert_is_not(copy, interaction_metadata)
    vampytest.assert_eq(copy, interaction_metadata)


def test__InteractionMetadataApplicationCommand__copy_with__1():
    """
    Tests whether ``InteractionMetadataApplicationCommand.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_id = 202211060040
    new_id = 202211060041
    old_name = 'Inaba'
    new_name = 'Reisen'
    old_options = [InteractionOption(name = 'Rem')]
    new_options = [InteractionOption(name = 'Diablo')]
    old_resolved = Resolved(attachments = [Attachment.precreate(202211060042)])
    new_resolved = Resolved(messages = [Message.precreate(202211060043)])
    old_target_id = 202211060044
    new_target_id = 202211060045
    
    interaction_metadata = InteractionMetadataApplicationCommand(
        id = old_id,
        name = old_name,
        options = old_options,
        resolved = old_resolved,
        target_id = old_target_id,
    )
    copy = interaction_metadata.copy_with(
        id = new_id,
        name = new_name,
        options = new_options,
        resolved = new_resolved,
        target_id = new_target_id,
    )
    _check_is_all_field_set(copy)
    vampytest.assert_is_not(copy, interaction_metadata)
    
    vampytest.assert_eq(copy.id, new_id)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.options, tuple(new_options))
    vampytest.assert_eq(copy.resolved, new_resolved)
    vampytest.assert_eq(copy.target_id, new_target_id)
