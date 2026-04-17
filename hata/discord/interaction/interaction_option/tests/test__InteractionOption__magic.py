import vampytest

from ....application_command import ApplicationCommandOptionType

from ..interaction_option import InteractionOption


def test__InteractionOption__repr():
    """
    Tests whether ``InteractionOption.__repr__`` works as intended.
    """
    focused = True
    name = 'Worldly'
    options = [InteractionOption(name = 'flower')]
    option_type = ApplicationCommandOptionType.sub_command
    value = 'flower land'
    
    interaction_option = InteractionOption(
        focused = focused,
        name = name,
        options = options,
        option_type = option_type,
        value = value,
    )
    
    vampytest.assert_instance(repr(interaction_option), str)


def test__InteractionOption__hash():
    """
    Tests whether ``InteractionOption.__hash__`` works as intended.
    """
    focused = True
    name = 'Worldly'
    options = [InteractionOption(name = 'flower')]
    option_type = ApplicationCommandOptionType.sub_command
    value = 'flower land'
    
    interaction_option = InteractionOption(
        focused = focused,
        name = name,
        options = options,
        option_type = option_type,
        value = value,
    )
    
    vampytest.assert_instance(hash(interaction_option), int)


def test__InteractionOption__eq():
    """
    Tests whether ``InteractionOption.__eq__`` works as intended.
    """
    focused = True
    name = 'Worldly'
    options = [InteractionOption(name = 'flower')]
    option_type = ApplicationCommandOptionType.sub_command
    value = 'flower land'
    
    keyword_parameters = {
        'focused': focused,
        'name': name,
        'options': options,
        'option_type': option_type,
        'value': value,
    }
    
    interaction_option = InteractionOption(**keyword_parameters)
    
    vampytest.assert_eq(interaction_option, interaction_option)
    vampytest.assert_ne(interaction_option, object())

    for field_name, field_value in (
        ('focused', False),
        ('name', 'night'),
        ('options', None),
        ('option_type', ApplicationCommandOptionType.string),
        ('value', 'blooms'),
    ):
        test_interaction_option = InteractionOption(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(interaction_option, test_interaction_option)
