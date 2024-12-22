import vampytest

from ....application_command import ApplicationCommandTargetType
from ....message import Attachment

from ...interaction_option import InteractionOption
from ...resolved import Resolved

from ..application_command import InteractionMetadataApplicationCommand


def _check_is_all_field_set(interaction_metadata):
    """
    Checks whether all fields of the given interaction metadata are set.
    
    Parameters
    ----------
    interaction_metadata : ``InteractionMetadataApplicationCommand``
        The interaction metadata to check.
    """
    vampytest.assert_instance(interaction_metadata, InteractionMetadataApplicationCommand)
    vampytest.assert_instance(interaction_metadata.id, int)
    vampytest.assert_instance(interaction_metadata.name, str)
    vampytest.assert_instance(interaction_metadata.options, tuple, nullable = True)
    vampytest.assert_instance(interaction_metadata.resolved, Resolved, nullable = True)
    vampytest.assert_instance(interaction_metadata.target_id, int)
    vampytest.assert_instance(interaction_metadata.target_type, ApplicationCommandTargetType)


def test__InteractionMetadataApplicationCommand__new__no_fields():
    """
    Tests whether ``InteractionMetadataApplicationCommand.__new__`` works as intended.
    
    Case: No fields given.
    """
    interaction_metadata = InteractionMetadataApplicationCommand()
    _check_is_all_field_set(interaction_metadata)


def test__InteractionMetadataApplicationCommand__new__all_fields():
    """
    Tests whether ``InteractionMetadataApplicationCommand.__new__`` works as intended.
    
    Case: All fields given.
    """
    application_command_id = 202211060013
    name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    resolved = Resolved(attachments = [Attachment.precreate(202211060014)])
    target_id = 202211060015
    target_type = ApplicationCommandTargetType.user
    
    interaction_metadata = InteractionMetadataApplicationCommand(
        application_command_id = application_command_id,
        name = name,
        options = options,
        resolved = resolved,
        target_id = target_id,
        target_type = target_type,
    )
    _check_is_all_field_set(interaction_metadata)
    
    vampytest.assert_eq(interaction_metadata.id, application_command_id)
    vampytest.assert_eq(interaction_metadata.name, name)
    vampytest.assert_eq(interaction_metadata.options, tuple(options))
    vampytest.assert_eq(interaction_metadata.resolved, resolved)
    vampytest.assert_eq(interaction_metadata.target_id, target_id)
    vampytest.assert_eq(interaction_metadata.target_type, target_type)
    

def test__InteractionMetadataApplicationCommand__create_empty():
    """
    Tests whether ``InteractionMetadataApplicationCommand._create_empty`` works as intended.
    """
    interaction_metadata = InteractionMetadataApplicationCommand._create_empty()
    _check_is_all_field_set(interaction_metadata)
