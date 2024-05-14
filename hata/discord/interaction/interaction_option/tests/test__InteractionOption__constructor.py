import vampytest

from ....application_command import ApplicationCommandOptionType

from ..interaction_option import InteractionOption


def _assert_fields_set(interaction_option):
    """
    Checks whether all attributes of the given interaction option are set.
    
    Parameters
    ----------
    interaction_option : ``InteractionOption``
    """
    vampytest.assert_instance(interaction_option, InteractionOption)
    vampytest.assert_instance(interaction_option.focused, bool)
    vampytest.assert_instance(interaction_option.name, str)
    vampytest.assert_instance(interaction_option.options, tuple, nullable = True)
    vampytest.assert_instance(interaction_option.type, ApplicationCommandOptionType)
    vampytest.assert_instance(interaction_option.value, object, nullable = True)


def test__InteractionOption__new__0():
    """
    Tests whether ``InteractionOption.__new__`` works as intended.
    
    Case: No fields.
    """
    interaction_option = InteractionOption()
    _assert_fields_set(interaction_option)


def test__InteractionOption__new__1():
    """
    Tests whether ``InteractionOption.__new__`` works as intended.
    
    Case: No fields.
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
    _assert_fields_set(interaction_option)
    
    vampytest.assert_eq(interaction_option.focused, focused)
    vampytest.assert_eq(interaction_option.name, name)
    vampytest.assert_eq(interaction_option.options, tuple(options))
    vampytest.assert_is(interaction_option.type, option_type)
    vampytest.assert_eq(interaction_option.value, value)


def test__InteractionOption__create_empty():
    """
    Tests whether ``InteractionOption._create_empty`` works as intended.
    """
    interaction_option = InteractionOption._create_empty()
    _assert_fields_set(interaction_option)
