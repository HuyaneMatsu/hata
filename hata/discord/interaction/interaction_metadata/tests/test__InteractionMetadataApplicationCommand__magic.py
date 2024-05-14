import vampytest

from ....message import Attachment

from ...interaction_option import InteractionOption
from ...resolved import Resolved

from ..application_command import InteractionMetadataApplicationCommand


def test__InteractionMetadataApplicationCommand__repr():
    """
    Tests whether ``InteractionMetadataApplicationCommand.__repr__`` works as intended.
    """
    application_command_id = 202211060023
    name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    resolved = Resolved(attachments = [Attachment.precreate(202211060024)])
    target_id = 202211060025
    
    interaction_metadata = InteractionMetadataApplicationCommand(
        application_command_id = application_command_id,
        name = name,
        options = options,
        resolved = resolved,
        target_id = target_id,
    )
    vampytest.assert_instance(repr(interaction_metadata), str)


def test__InteractionMetadataApplicationCommand__hash():
    """
    Tests whether ``InteractionMetadataApplicationCommand.__hash__`` works as intended.
    """
    application_command_id = 202211060026
    name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    resolved = Resolved(attachments = [Attachment.precreate(202211060027)])
    target_id = 202211060028
    
    interaction_metadata = InteractionMetadataApplicationCommand(
        application_command_id = application_command_id,
        name = name,
        options = options,
        resolved = resolved,
        target_id = target_id,
    )
    vampytest.assert_instance(hash(interaction_metadata), int)


def test__InteractionMetadataApplicationCommand__eq():
    """
    Tests whether ``InteractionMetadataApplicationCommand.__eq__`` works as intended.
    """
    application_command_id = 202211060029
    name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    resolved = Resolved(attachments = [Attachment.precreate(202211060030)])
    target_id = 202211060031
    
    keyword_parameters = {
        'application_command_id': application_command_id,
        'name': name,
        'options': options,
        'resolved': resolved,
        'target_id': target_id,
    }
    
    interaction_metadata = InteractionMetadataApplicationCommand(**keyword_parameters)
    
    vampytest.assert_eq(interaction_metadata, interaction_metadata)
    vampytest.assert_ne(interaction_metadata, object())
    
    for field_name, field_value in (
        ('application_command_id', 202211060032),
        ('name', 'Reisen'),
        ('options', None),
        ('resolved', None),
        ('target_id', 202211060033)
    ):
        test_interaction_metadata = InteractionMetadataApplicationCommand(
            **{**keyword_parameters, field_name: field_value}
        )
        vampytest.assert_ne(interaction_metadata, test_interaction_metadata)
