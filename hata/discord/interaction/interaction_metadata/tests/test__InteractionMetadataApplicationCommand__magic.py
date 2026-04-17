import vampytest

from ....application_command import ApplicationCommandTargetType
from ....message import Attachment

from ...interaction_option import InteractionOption

from ..application_command import InteractionMetadataApplicationCommand


def test__InteractionMetadataApplicationCommand__repr():
    """
    Tests whether ``InteractionMetadataApplicationCommand.__repr__`` works as intended.
    """
    application_command_id = 202211060023
    application_command_name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    target_id = 202211060025
    target_type = ApplicationCommandTargetType.user
    
    interaction_metadata = InteractionMetadataApplicationCommand(
        application_command_id = application_command_id,
        application_command_name = application_command_name,
        options = options,
        target_id = target_id,
        target_type = target_type,
    )
    
    output = repr(interaction_metadata)
    vampytest.assert_instance(output, str)


def test__InteractionMetadataApplicationCommand__hash():
    """
    Tests whether ``InteractionMetadataApplicationCommand.__hash__`` works as intended.
    """
    application_command_id = 202211060026
    application_command_name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    target_id = 202211060028
    target_type = ApplicationCommandTargetType.user
    
    interaction_metadata = InteractionMetadataApplicationCommand(
        application_command_id = application_command_id,
        application_command_name = application_command_name,
        options = options,
        target_id = target_id,
        target_type = target_type,
    )
    
    output = hash(interaction_metadata)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    application_command_id = 202211060029
    application_command_name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    target_id = 202211060031
    target_type = ApplicationCommandTargetType.user
    
    keyword_parameters = {
        'application_command_id': application_command_id,
        'application_command_name': application_command_name,
        'options': options,
        'target_id': target_id,
        'target_type': target_type,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'application_command_id': 202211060032,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'application_command_name': 'Reisen',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'options': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'target_id': 202211060033,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'target_type': ApplicationCommandTargetType.channel,
        },
        False,
    )
    

@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__InteractionMetadataApplicationCommand__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``InteractionMetadataApplicationCommand.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    interaction_metadata_0 = InteractionMetadataApplicationCommand(**keyword_parameters_0)
    interaction_metadata_1 = InteractionMetadataApplicationCommand(**keyword_parameters_1)
    
    output = interaction_metadata_0 == interaction_metadata_1
    vampytest.assert_instance(output, bool)
    return output
