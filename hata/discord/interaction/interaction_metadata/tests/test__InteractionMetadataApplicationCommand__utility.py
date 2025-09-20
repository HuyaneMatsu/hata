import vampytest

from ....application_command import ApplicationCommandTargetType
from ....message import Attachment, Message

from ...interaction_option import InteractionOption

from ..application_command import InteractionMetadataApplicationCommand

from .test__InteractionMetadataApplicationCommand__constructor import _assert_fields_set


def test__InteractionMetadataApplicationCommand__copy():
    """
    Tests whether ``InteractionMetadataApplicationCommand.copy`` works as intended.
    """
    application_command_id = 202211060034
    application_command_name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    target_id = 202211060036
    target_type = ApplicationCommandTargetType.user
    
    interaction_metadata = InteractionMetadataApplicationCommand(
        application_command_id = application_command_id,
        application_command_name = application_command_name,
        options = options,
        target_id = target_id,
        target_type = target_type,
    )
    copy = interaction_metadata.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, interaction_metadata)
    vampytest.assert_eq(copy, interaction_metadata)


def test__InteractionMetadataApplicationCommand__copy_with__no_fields():
    """
    Tests whether ``InteractionMetadataApplicationCommand.copy_with`` works as intended.
    
    Case: No fields given.
    """
    application_command_id = 202211060037
    application_command_name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    target_id = 202211060039
    target_type = ApplicationCommandTargetType.user
    
    interaction_metadata = InteractionMetadataApplicationCommand(
        application_command_id = application_command_id,
        application_command_name = application_command_name,
        options = options,
        target_id = target_id,
        target_type = target_type,
    )
    copy = interaction_metadata.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, interaction_metadata)
    vampytest.assert_eq(copy, interaction_metadata)


def test__InteractionMetadataApplicationCommand__copy_with__all_fields():
    """
    Tests whether ``InteractionMetadataApplicationCommand.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_application_command_id = 202211060040
    old_application_command_name = 'Inaba'
    old_options = [InteractionOption(name = 'Rem')]
    old_target_id = 202211060044
    old_target_type = ApplicationCommandTargetType.user
    
    new_application_command_id = 202211060041
    new_application_command_name = 'Reisen'
    new_options = [InteractionOption(name = 'Diablo')]
    new_target_id = 202211060045
    new_target_type = ApplicationCommandTargetType.user
    
    interaction_metadata = InteractionMetadataApplicationCommand(
        application_command_id = old_application_command_id,
        application_command_name = old_application_command_name,
        options = old_options,
        target_id = old_target_id,
        target_type = old_target_type,
    )
    copy = interaction_metadata.copy_with(
        application_command_id = new_application_command_id,
        application_command_name = new_application_command_name,
        options = new_options,
        target_id = new_target_id,
        target_type = new_target_type,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, interaction_metadata)
    
    vampytest.assert_eq(copy.application_command_id, new_application_command_id)
    vampytest.assert_eq(copy.application_command_name, new_application_command_name)
    vampytest.assert_eq(copy.options, tuple(new_options))
    vampytest.assert_eq(copy.target_id, new_target_id)
    vampytest.assert_is(copy.target_type, new_target_type)


def test__InteractionMetadataApplicationCommand__copy_with_keyword_parameters__no_fields():
    """
    Tests whether ``InteractionMetadataApplicationCommand.copy_with_keyword_parameters`` works as intended.
    
    Case: No fields given.
    """
    interaction_metadata = InteractionMetadataApplicationCommand()
    copy = interaction_metadata.copy_with_keyword_parameters({})
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, interaction_metadata)
    vampytest.assert_eq(copy, interaction_metadata)


def test__InteractionMetadataApplicationCommand__copy_with_keyword_parameters__all_fields():
    """
    Tests whether ``InteractionMetadataApplicationCommand.copy_with_keyword_parameters`` works as intended.
    
    Case: No fields given.
    """
    old_application_command_id = 202509140010
    old_application_command_name = 'Inaba'
    old_options = [InteractionOption(name = 'Rem')]
    old_target_id = 202509140011
    old_target_type = ApplicationCommandTargetType.user
    
    new_application_command_id = 202509140012
    new_application_command_name = 'Reisen'
    new_options = [InteractionOption(name = 'Diablo')]
    new_target_id = 202509140013
    new_target_type = ApplicationCommandTargetType.user
    
    interaction_metadata = InteractionMetadataApplicationCommand(
        application_command_id = old_application_command_id,
        application_command_name = old_application_command_name,
        options = old_options,
        target_id = old_target_id,
        target_type = old_target_type,
    )
    
    copy = interaction_metadata.copy_with_keyword_parameters({
        'application_command_id': new_application_command_id,
        'application_command_name': new_application_command_name,
        'options': new_options,
        'target_id': new_target_id,
        'target_type': new_target_type,
    })
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, interaction_metadata)
    vampytest.assert_ne(copy, interaction_metadata)
    
    vampytest.assert_eq(copy.application_command_id, new_application_command_id)
    vampytest.assert_eq(copy.application_command_name, new_application_command_name)
    vampytest.assert_eq(copy.options, tuple(new_options))
    vampytest.assert_eq(copy.target_id, new_target_id)
    vampytest.assert_is(copy.target_type, new_target_type)
