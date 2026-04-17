import vampytest

from ....application_command import ApplicationCommandOptionType

from ..interaction_option import InteractionOption

from .test__InteractionOption__constructor import _assert_fields_set


def test__InteractionOption__from_data():
    """
    Tests whether ``InteractionOption.from_data`` works as intended.
    """
    focused = True
    name = 'Worldly'
    options = [InteractionOption(name = 'flower')]
    option_type = ApplicationCommandOptionType.sub_command
    value = 'flower land'
    
    data = {
        'focused': focused,
        'name': name,
        'options': [option.to_data() for option in options],
        'type': option_type.value,
        'value': value,
    }
    
    interaction_option = InteractionOption.from_data(data)
    _assert_fields_set(interaction_option)
    
    vampytest.assert_eq(interaction_option.focused, focused)
    vampytest.assert_eq(interaction_option.name, name)
    vampytest.assert_eq(interaction_option.options, tuple(options))
    vampytest.assert_is(interaction_option.type, option_type)
    vampytest.assert_eq(interaction_option.value, value)


def test__InteractionOption__to_data():
    """
    Tests whether ``InteractionOption.to_data`` works as intended.
    
    Case: defaults.
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
    
    vampytest.assert_eq(
        interaction_option.to_data(
            defaults = True,
        ),
        {
            'focused': focused,
            'name': name,
            'options': [option.to_data(defaults = True) for option in options],
            'type': option_type.value,
            'value': value,
        },
    )
