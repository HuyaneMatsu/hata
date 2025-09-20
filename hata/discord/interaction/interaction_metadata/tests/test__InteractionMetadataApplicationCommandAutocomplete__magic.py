import vampytest

from ...interaction_option import InteractionOption

from ..application_command_autocomplete import InteractionMetadataApplicationCommandAutocomplete


def test__InteractionMetadataApplicationCommandAutocomplete__repr():
    """
    Tests whether ``InteractionMetadataApplicationCommandAutocomplete.__repr__`` works as intended.
    """
    application_command_id = 202211060005
    application_command_name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    
    interaction_metadata = InteractionMetadataApplicationCommandAutocomplete(
        application_command_id = application_command_id,
        application_command_name = application_command_name,
        options = options,
    )
    vampytest.assert_instance(repr(interaction_metadata), str)


def test__InteractionMetadataApplicationCommandAutocomplete__hash():
    """
    Tests whether ``InteractionMetadataApplicationCommandAutocomplete.__hash__`` works as intended.
    """
    application_command_id = 202211060006
    application_command_name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    
    interaction_metadata = InteractionMetadataApplicationCommandAutocomplete(
        application_command_id = application_command_id,
        application_command_name = application_command_name,
        options = options,
    )
    vampytest.assert_instance(hash(interaction_metadata), int)


def test__InteractionMetadataApplicationCommandAutocomplete__eq__different_type():
    """
    Tests whether ``InteractionMetadataApplicationCommandAutocomplete.__eq__`` works as intended.
    
    Case: different type.
    """
    interaction_metadata = InteractionMetadataApplicationCommandAutocomplete()
    vampytest.assert_ne(interaction_metadata, object())


def _iter_options__eq():
    application_command_id = 202211060007
    application_command_name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    
    keyword_parameters = {
        'application_command_id': application_command_id,
        'application_command_name': application_command_name,
        'options': options,
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
            'application_command_id': 202211060008,
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


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__InteractionMetadataApplicationCommandAutocomplete__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``InteractionMetadataApplicationCommandAutocomplete.__eq__`` works as intended.
    
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
    interaction_metadata_0 = InteractionMetadataApplicationCommandAutocomplete(**keyword_parameters_0)
    interaction_metadata_1 = InteractionMetadataApplicationCommandAutocomplete(**keyword_parameters_1)
    
    output = interaction_metadata_0 == interaction_metadata_1
    vampytest.assert_instance(output, bool)
    return output
