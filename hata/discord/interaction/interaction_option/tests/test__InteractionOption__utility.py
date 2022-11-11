import vampytest

from ....application_command import ApplicationCommandOptionType

from ..interaction_option import InteractionOption

from .test__InteractionOption__constructor import _check_is_all_attribute_set


def test__InteractionOption__copy():
    """
    Tests whether ``InteractionOption.copy`` works as intended.
    """
    focused = True
    name = 'Worldly'
    options = [InteractionOption(name = 'flower')]
    type_ = ApplicationCommandOptionType.sub_command
    value = 'flower land'
    
    interaction_option = InteractionOption(
        focused = focused,
        name = name,
        options = options,
        type_ = type_,
        value = value,
    )
    
    copy = interaction_option.copy()
    _check_is_all_attribute_set(copy)
    vampytest.assert_not_is(interaction_option, copy)
    vampytest.assert_eq(interaction_option, copy)


def test__InteractionOption__copy_with():
    """
    Tests whether ``InteractionOption.copy_with`` works as intended.
    
    Case: No fields given.
    """
    focused = True
    name = 'Worldly'
    options = [InteractionOption(name = 'flower')]
    type_ = ApplicationCommandOptionType.sub_command
    value = 'flower land'
    
    interaction_option = InteractionOption(
        focused = focused,
        name = name,
        options = options,
        type_ = type_,
        value = value,
    )
    
    copy = interaction_option.copy_with()
    _check_is_all_attribute_set(copy)
    vampytest.assert_not_is(interaction_option, copy)
    vampytest.assert_eq(interaction_option, copy)


def test__InteractionOption__copy_with__1():
    """
    Tests whether ``InteractionOption.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_focused = True
    new_focused = False
    old_name = 'Worldly'
    new_name = 'START'
    old_options = [InteractionOption(name = 'flower')]
    new_options = [InteractionOption(name = 'crazy')]
    old_type = ApplicationCommandOptionType.sub_command
    new_type = ApplicationCommandOptionType.sub_command_group
    old_value = 'flower land'
    new_value = 'beats'
    
    interaction_option = InteractionOption(
        focused = old_focused,
        name = old_name,
        options = old_options,
        type_ = old_type,
        value = old_value,
    )
    
    copy = interaction_option.copy_with(
        focused = new_focused,
        name = new_name,
        options = new_options,
        type_ = new_type,
        value = new_value,
    )
    
    _check_is_all_attribute_set(copy)
    vampytest.assert_not_is(interaction_option, copy)

    vampytest.assert_eq(copy.focused, new_focused)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.options, tuple(new_options))
    vampytest.assert_is(copy.type, new_type)
    vampytest.assert_eq(copy.value, new_value)


def test__InteractionOption__focused_option():
    """
    Tests whether ``InteractionOption.focused_option`` works as intended.
    """
    interaction_option_1 = InteractionOption(focused = False)
    interaction_option_2 = InteractionOption(focused = False, type_ = ApplicationCommandOptionType.sub_command)
    interaction_option_3 = InteractionOption(focused = True)
    interaction_option_4 = InteractionOption(
        focused = False, type_ = ApplicationCommandOptionType.sub_command, options = [interaction_option_3]
    )
    
    for interaction_option, expected_output in (
        (interaction_option_1, None),
        (interaction_option_2, None),
        (interaction_option_3, interaction_option_3),
        (interaction_option_4, interaction_option_3),
    ):
        vampytest.assert_is(interaction_option.focused_option, expected_output)


def test__InteractionOption__get_value_of():
    """
    Tests whether ``InteractionOption.get_value_of`` works as intended.
    """
    interaction_option_1 = InteractionOption(name = 'hello', value = 'hell')
    interaction_option_2 = InteractionOption(
        name = 'supernova',
        type_ = ApplicationCommandOptionType.sub_command,
        options = [interaction_option_1],
        value = 'vistnry',
    )
    
    for interaction_option, option_names, expected_output in (
        (interaction_option_1, [], 'hell'),
        (interaction_option_2, [], 'vistnry'),
        (interaction_option_2, ['hello'], 'hell'),
        (interaction_option_2, ['kumo'], None),
    ):
        vampytest.assert_eq(interaction_option.get_value_of(*option_names), expected_output)


def test__InteractionOption__iter_non_focused_values():
    """
    Tests whether ``InteractionOption._iter_non_focused_values`` works as intended.
    """
    interaction_option_1 = InteractionOption(name = 'hello', value = 'hell', focused = False)
    interaction_option_2 = InteractionOption(
        name = 'supernova',
        type_ = ApplicationCommandOptionType.sub_command,
        options = [interaction_option_1],
        value = 'vistnry',
        focused = False,
    )
    
    interaction_option_3 = InteractionOption(name = 'sekai', value = 'yoru', focused = True)
    
    
    for interaction_option, expected_output in (
        (interaction_option_1, {'hello': 'hell'}),
        (interaction_option_2, {'hello': 'hell'}),
        (interaction_option_3, {}),
    ):
        vampytest.assert_eq(dict(interaction_option._iter_non_focused_values()), expected_output)


def test__InteractionOption__iter_options():
    """
    Tests whether ``InteractionOption.iter_options`` works as intended.
    """
    interaction_option_1 = InteractionOption(name = 'red')
    interaction_option_2 = InteractionOption(name = 'me')
    
    for interaction_option, expected_output in (
        (InteractionOption(options = None), []),
        (InteractionOption(options = [interaction_option_1]), [interaction_option_1]),
        (
            InteractionOption(options = [interaction_option_2, interaction_option_1]),
            [interaction_option_2, interaction_option_1]
        ),
    ):
        vampytest.assert_eq([*interaction_option.iter_options()], expected_output)
