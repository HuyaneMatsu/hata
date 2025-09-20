import vampytest

from ....application_command import ApplicationCommandTargetType

from ...interaction_option import InteractionOption

from ..application_command import InteractionMetadataApplicationCommand


def _assert_fields_set(interaction_metadata):
    """
    Checks whether all fields of the given interaction metadata are set.
    
    Parameters
    ----------
    interaction_metadata : ``InteractionMetadataApplicationCommand``
        The interaction metadata to check.
    """
    vampytest.assert_instance(interaction_metadata, InteractionMetadataApplicationCommand)
    vampytest.assert_instance(interaction_metadata.application_command_id, int)
    vampytest.assert_instance(interaction_metadata.application_command_name, str)
    vampytest.assert_instance(interaction_metadata.options, tuple, nullable = True)
    vampytest.assert_instance(interaction_metadata.target_id, int)
    vampytest.assert_instance(interaction_metadata.target_type, ApplicationCommandTargetType)


def test__InteractionMetadataApplicationCommand__new__no_fields():
    """
    Tests whether ``InteractionMetadataApplicationCommand.__new__`` works as intended.
    
    Case: No fields given.
    """
    interaction_metadata = InteractionMetadataApplicationCommand()
    _assert_fields_set(interaction_metadata)


def test__InteractionMetadataApplicationCommand__new__all_fields():
    """
    Tests whether ``InteractionMetadataApplicationCommand.__new__`` works as intended.
    
    Case: All fields given.
    """
    application_command_id = 202211060013
    application_command_name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    target_id = 202211060015
    target_type = ApplicationCommandTargetType.user
    
    interaction_metadata = InteractionMetadataApplicationCommand(
        application_command_id = application_command_id,
        application_command_name = application_command_name,
        options = options,
        target_id = target_id,
        target_type = target_type,
    )
    _assert_fields_set(interaction_metadata)
    
    vampytest.assert_eq(interaction_metadata.application_command_id, application_command_id)
    vampytest.assert_eq(interaction_metadata.application_command_name, application_command_name)
    vampytest.assert_eq(interaction_metadata.options, tuple(options))
    vampytest.assert_eq(interaction_metadata.target_id, target_id)
    vampytest.assert_eq(interaction_metadata.target_type, target_type)


def test__InteractionMetadataApplicationCommand__from_keyword_parameters__no_fields():
    """
    Tests whether ``InteractionMetadataApplicationCommand.from_keyword_parameters`` works as intended.
    
    Case: No fields given.
    """
    interaction_metadata = InteractionMetadataApplicationCommand.from_keyword_parameters({})
    _assert_fields_set(interaction_metadata)


def test__InteractionMetadataApplicationCommand__from_keyword_parameters__all_fields():
    """
    Tests whether ``InteractionMetadataApplicationCommand.from_keyword_parameters`` works as intended.
    
    Case: All fields given.
    """
    application_command_id = 202509140000
    application_command_name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    target_id = 202509140001
    target_type = ApplicationCommandTargetType.user
    
    interaction_metadata = InteractionMetadataApplicationCommand.from_keyword_parameters({
        'application_command_id': application_command_id,
        'application_command_name': application_command_name,
        'options': options,
        'target_id': target_id,
        'target_type': target_type,
    })
    _assert_fields_set(interaction_metadata)
    
    vampytest.assert_eq(interaction_metadata.application_command_id, application_command_id)
    vampytest.assert_eq(interaction_metadata.application_command_name, application_command_name)
    vampytest.assert_eq(interaction_metadata.options, tuple(options))
    vampytest.assert_eq(interaction_metadata.target_id, target_id)
    vampytest.assert_eq(interaction_metadata.target_type, target_type)


def test__InteractionMetadataApplicationCommand__create_empty():
    """
    Tests whether ``InteractionMetadataApplicationCommand._create_empty`` works as intended.
    """
    interaction_metadata = InteractionMetadataApplicationCommand._create_empty()
    _assert_fields_set(interaction_metadata)
