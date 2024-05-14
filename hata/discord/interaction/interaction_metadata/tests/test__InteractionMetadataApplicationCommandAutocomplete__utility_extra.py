import vampytest

from ....application_command import ApplicationCommandOptionType

from ...interaction_option import InteractionOption

from ..application_command_autocomplete import InteractionMetadataApplicationCommandAutocomplete


def test__InteractionMetadataApplicationCommandAutocomplete__iter_options():
    """
    Tests whether ``InteractionMetadataApplicationCommandAutocomplete.iter_options`` works as intended.
    """
    interaction_option_1 = InteractionOption(name = 'negative')
    interaction_option_2 = InteractionOption(name = 'number')
    
    for interaction_option, expected_output in (
        (InteractionMetadataApplicationCommandAutocomplete(options = None), []),
        (InteractionMetadataApplicationCommandAutocomplete(options = [interaction_option_1]), [interaction_option_1]),
        (
            InteractionMetadataApplicationCommandAutocomplete(options = [interaction_option_2, interaction_option_1]),
            [interaction_option_2, interaction_option_1]
        ),
    ):
        vampytest.assert_eq([*interaction_option.iter_options()], expected_output)


def test__InteractionMetadataApplicationCommandAutocomplete__focused_option__0():
    """
    Tests whether ``InteractionMetadataApplicationCommandAutocomplete.focused_option`` works as intended.
    
    Case: nope.
    """
    interaction_metadata = InteractionMetadataApplicationCommandAutocomplete()
    
    vampytest.assert_is(interaction_metadata.focused_option, None)


def test__InteractionMetadataApplicationCommandAutocomplete__focused_option__1():
    """
    Tests whether ``InteractionMetadataApplicationCommandAutocomplete.focused_option`` works as intended.
    
    Case: yes!
    """
    interaction_option_1 = InteractionOption(focused = True)
    interaction_metadata = InteractionMetadataApplicationCommandAutocomplete(
        options = [interaction_option_1],
    )
    
    vampytest.assert_is(interaction_metadata.focused_option, interaction_option_1)


def test__InteractionMetadataApplicationCommandAutocomplete__get_non_focused_values():
    """
    Tests whether ``InteractionMetadataApplicationCommandAutocomplete.get_non_focused_values`` works as intended.
    """
    interaction_option_1 = InteractionOption(name = 'Yang', value = 'Xiao Long', focused = False)
    interaction_option_2 = InteractionOption(name = 'Ruby', value = 'Rose', focused = False)
    
    interaction_metadata = InteractionMetadataApplicationCommandAutocomplete(
        options = [interaction_option_1, interaction_option_2],
    )
    
    vampytest.assert_eq(
        interaction_metadata.get_non_focused_values(),
        {
            'Yang': 'Xiao Long',
            'Ruby': 'Rose',
        }
    )


def test__InteractionMetadataApplicationCommandAutocomplete__get_value_of():
    """
    Tests whether ``InteractionMetadataApplicationCommandAutocomplete.get_value_of`` works as intended.
    """
    interaction_option_1 = InteractionOption(name = 'fumo', value = 'friday')
    interaction_option_2 = InteractionOption(
        name = 'maou',
        option_type = ApplicationCommandOptionType.sub_command,
        options = [interaction_option_1],
        value = 'day',
    )

    interaction_metadata = InteractionMetadataApplicationCommandAutocomplete(
        options = [interaction_option_2],
    )
    
    vampytest.assert_eq(interaction_metadata.get_value_of('maou', 'fumo'), 'friday')
