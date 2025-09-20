import vampytest

from ....application_command import ApplicationCommandOptionType

from ...interaction_option import InteractionOption

from ..application_command_autocomplete import InteractionMetadataApplicationCommandAutocomplete



def _iter_options__iter_options():
    interaction_option_0 = InteractionOption(name = 'negative')
    interaction_option_1 = InteractionOption(name = 'number')
    
    yield (
        {
            'options': None,
        },
        [],
    )
    
    yield (
        {
            'options': [
                interaction_option_0,
            ],
        },
        [
            interaction_option_0,
        ],
    )
    
    yield (
        {
            'options': [
                interaction_option_0,
                interaction_option_1,
            ],
        },
        [
            interaction_option_0,
            interaction_option_1,
        ],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_options()).returning_last())
def test__InteractionMetadataApplicationCommandAutocomplete__iter_options(keyword_parameters):
    """
    Tests whether ``InteractionMetadataApplicationCommandAutocomplete.iter_options`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : ``list<InteractionOption>``
    """
    interaction_metadata = InteractionMetadataApplicationCommandAutocomplete(**keyword_parameters)
    
    output = [*interaction_metadata.iter_options()]
    
    for element in output:
        vampytest.assert_instance(element, InteractionOption)
    
    return output


def _iter_options__focused_option():
    interaction_option_0 = InteractionOption(focused = True, name = 'negative')
    interaction_option_1 = InteractionOption(name = 'number')
    
    yield (
        {
            'options': None,
        },
        None,
    )
    
    yield (
        {
            'options': [
                interaction_option_0,
            ],
        },
        interaction_option_0,
    )
    
    yield (
        {
            'options': [
                interaction_option_1,
            ],
        },
        None,
    )
    

@vampytest._(vampytest.call_from(_iter_options__focused_option()).returning_last())
def test__InteractionMetadataApplicationCommandAutocomplete__focused_option(keyword_parameters):
    """
    Tests whether ``InteractionMetadataApplicationCommandAutocomplete.focused_option`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : ``None | InteractionOption``
    """
    interaction_metadata = InteractionMetadataApplicationCommandAutocomplete(**keyword_parameters)
    
    output = interaction_metadata.focused_option
    vampytest.assert_instance(output, InteractionOption, nullable = True)
    return output


def _iter_options__get_non_focused_values():
    interaction_option_0 = InteractionOption(focused = False, name = 'Yang', value = 'Xiao Long')
    interaction_option_1 = InteractionOption(focused = False, name = 'Ruby', value = 'Rose')
    interaction_option_2 = InteractionOption(focused = True, name = 'Yakumo', value = 'Yukari')
    
    yield (
        {
            'options': None,
        },
        {},
    )
    
    yield (
        {
            'options': [
                interaction_option_0,
                interaction_option_1,
                interaction_option_2,
            ],
        },
        {
            'Yang': 'Xiao Long',
            'Ruby': 'Rose',
        },
    )


@vampytest._(vampytest.call_from(_iter_options__get_non_focused_values()).returning_last())
def test__InteractionMetadataApplicationCommandAutocomplete__get_non_focused_values(keyword_parameters):
    """
    Tests whether ``InteractionMetadataApplicationCommandAutocomplete.get_non_focused_values`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `dict<str, None | str>`
    """
    interaction_metadata = InteractionMetadataApplicationCommandAutocomplete(**keyword_parameters)
    
    output = interaction_metadata.get_non_focused_values()
    
    vampytest.assert_instance(output, dict)
    for key, value in output.items():
        vampytest.assert_instance(key, str)
        vampytest.assert_instance(value, str, nullable = True)
    
    return output


def _iter_options__get_value_of():
    interaction_option_0 = InteractionOption(
        name = 'fumo',
        value = 'friday',
    )
    
    interaction_option_1 = InteractionOption(
        name = 'maou',
        option_type = ApplicationCommandOptionType.sub_command,
        options = [
            interaction_option_0
        ],
        value = 'day',
    )
    
    yield (
        {
            'options': None,
        },
        (
            'koishi',
        ),
        None,
    )
    
    yield (
        {
            'options': [
                interaction_option_1,
            ],
        },
        (
            'maou',
            'fumo',
        ),
        'friday',
    )


@vampytest._(vampytest.call_from(_iter_options__get_value_of()).returning_last())
def test__InteractionMetadataApplicationCommandAutocomplete__get_value_of(keyword_parameters, option_names):
    """
    Tests whether ``InteractionMetadataApplicationCommandAutocomplete.get_value_of`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    option_names : `tuple<str>`
        Option names to get value for.
    
    Returns
    -------
    output : `None | str`
    """
    interaction_metadata = InteractionMetadataApplicationCommandAutocomplete(**keyword_parameters)
    output = interaction_metadata.get_value_of(*option_names)
    vampytest.assert_instance(output, str, nullable = True)
    return output
