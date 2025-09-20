import vampytest

from ....application_command import ApplicationCommandOptionType, ApplicationCommandTargetType
from ....component import ComponentType, InteractionComponent

from ...interaction_option import InteractionOption

from ..interaction_event import InteractionEvent
from ..preinstanced import InteractionType


def test__InteractionEvent__proxies():
    """
    Tests whether ``InteractionEvent`` field proxies work as intended.
    
    Case: Default.
    """
    interaction_event = InteractionEvent()
    
    vampytest.assert_instance(interaction_event.components, tuple, nullable = True)
    vampytest.assert_instance(interaction_event.custom_id, str, nullable = True)
    vampytest.assert_instance(interaction_event.application_command_id, int)
    vampytest.assert_instance(interaction_event.application_command_name, str)
    vampytest.assert_instance(interaction_event.options, tuple, nullable = True)
    vampytest.assert_instance(interaction_event.target_id, int)
    vampytest.assert_instance(interaction_event.target_type, ApplicationCommandTargetType)


def test__InteractionEvent__proxies_application_command__read():
    """
    Tests whether ``InteractionEvent`` field proxies work as intended.
    
    Case: application command & read.
    """
    application_command_id = 202211100014
    application_command_name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    target_id = 202211100016
    target_type = ApplicationCommandTargetType.user
    
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.application_command,
        application_command_id = application_command_id,
        application_command_name = application_command_name,
        options = options,
        target_id = target_id,
        target_type = target_type,
    )
    
    vampytest.assert_eq(interaction_event.application_command_id, application_command_id)
    vampytest.assert_eq(interaction_event.application_command_name, application_command_name)
    vampytest.assert_eq(interaction_event.options, tuple(options))
    vampytest.assert_eq(interaction_event.target_id, target_id)
    vampytest.assert_is(interaction_event.target_type, target_type)


def test__InteractionEvent__proxies_application_command_autocomplete__read():
    """
    Tests whether ``InteractionEvent`` field proxies work as intended.
    
    Case: application command autocomplete & read.
    """
    application_command_id = 202211100017
    application_command_name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.application_command_autocomplete,
        application_command_id = application_command_id,
        application_command_name = application_command_name,
        options = options,
    )
    
    vampytest.assert_eq(interaction_event.application_command_id, application_command_id)
    vampytest.assert_eq(interaction_event.application_command_name, application_command_name)
    vampytest.assert_eq(interaction_event.options, tuple(options))


def test__InteractionEvent__proxies_message_component__read():
    """
    Tests whether ``InteractionEvent`` field proxies work as intended.
    
    Case: message component & read.
    """
    component = InteractionComponent(
        ComponentType.string_select,
        custom_id = 'Inaba',
        values = ['black', 'rock', 'shooter'],
    )
    
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.message_component,
        component = component,
    )
    
    vampytest.assert_eq(interaction_event.component, component)


def test__InteractionEvent__proxies_form_submit__read():
    """
    Tests whether ``InteractionEvent`` field proxies work as intended.
    
    Case: form submit & read.
    """
    custom_id = 'Inaba'
    components = [
        InteractionComponent(
            ComponentType.text_input,
            custom_id = 'Rem',
        ),
    ]
    
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.form_submit,
        custom_id = custom_id,
        components = components,
    )
    
    vampytest.assert_eq(interaction_event.custom_id, custom_id)
    vampytest.assert_eq(interaction_event.components, tuple(components))


def test__InteractionEvent__proxies_application_command__write():
    """
    Tests whether ``InteractionEvent`` field proxies work as intended.
    
    Case: application command & write.
    """
    application_command_id = 202519150000
    application_command_name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    target_id = 202519150001
    target_type = ApplicationCommandTargetType.user
    
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.application_command,
    )
    
    interaction_event.application_command_id = application_command_id
    interaction_event.application_command_name = application_command_name
    interaction_event.options = options
    interaction_event.target_id = target_id
    interaction_event.target_type = target_type
    
    vampytest.assert_eq(interaction_event.application_command_id, application_command_id)
    vampytest.assert_eq(interaction_event.application_command_name, application_command_name)
    vampytest.assert_eq(interaction_event.options, tuple(options))
    vampytest.assert_eq(interaction_event.target_id, target_id)
    vampytest.assert_is(interaction_event.target_type, target_type)
    

def test__InteractionEvent__proxies_application_command_autocomplete__write():
    """
    Tests whether ``InteractionEvent`` field proxies work as intended.
    
    Case: application command autocomplete & write.
    """
    application_command_id = 202519150002
    application_command_name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.application_command_autocomplete,
    )
    
    interaction_event.application_command_id = application_command_id
    interaction_event.application_command_name = application_command_name
    interaction_event.options = options
    
    vampytest.assert_eq(interaction_event.application_command_id, application_command_id)
    vampytest.assert_eq(interaction_event.application_command_name, application_command_name)
    vampytest.assert_eq(interaction_event.options, tuple(options))


def test__InteractionEvent__proxies_message_component__write():
    """
    Tests whether ``InteractionEvent`` field proxies work as intended.
    
    Case: message component & write.
    """
    component = InteractionComponent(
        ComponentType.string_select,
        custom_id = 'Inaba',
        values = ['black', 'rock', 'shooter'],
    )
    
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.message_component,
    )
    
    interaction_event.component = component
    
    vampytest.assert_eq(interaction_event.component, component)


def test__InteractionEvent__proxies_form_submit__write():
    """
    Tests whether ``InteractionEvent`` field proxies work as intended.
    
    Case: form submit & write.
    """
    custom_id = 'Inaba'
    components = [
        InteractionComponent(
            ComponentType.text_input,
            custom_id = 'Rem',
        ),
    ]
    
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.form_submit,
    )
    
    interaction_event.custom_id = custom_id
    interaction_event.components = components
    
    vampytest.assert_eq(interaction_event.custom_id, custom_id)
    vampytest.assert_eq(interaction_event.components, tuple(components))


def test__InteractionEvent__iter_options():
    """
    Tests whether ``InteractionEvent.iter_options`` field proxies work as intended.
    """
    interaction_option_1 = InteractionOption(name = 'negative')
    interaction_option_2 = InteractionOption(name = 'number')
    
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.application_command_autocomplete,
        options = [interaction_option_1, interaction_option_2],
    )
    
    vampytest.assert_eq([*interaction_event.iter_options()], [interaction_option_1, interaction_option_2])


def test__InteractionEvent__focused_option__1():
    """
    Tests whether ``InteractionEvent.focused_option`` works as intended.
    """
    interaction_option_1 = InteractionOption(focused = True)
    
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.application_command_autocomplete,
        options = [interaction_option_1],
    )
    
    vampytest.assert_is(interaction_event.focused_option, interaction_option_1)


def test__InteractionEvent__get_non_focused_values():
    """
    Tests whether ``InteractionEvent.get_non_focused_values`` works as intended.
    """
    interaction_option_1 = InteractionOption(name = 'Yang', value = 'Xiao Long', focused = False)
    interaction_option_2 = InteractionOption(name = 'Ruby', value = 'Rose', focused = False)
    
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.application_command_autocomplete,
        options = [interaction_option_1, interaction_option_2],
    )
    
    vampytest.assert_eq(
        interaction_event.get_non_focused_values(),
        {
            'Yang': 'Xiao Long',
            'Ruby': 'Rose',
        }
    )


def test__InteractionEvent__get_value_of():
    """
    Tests whether ``InteractionEvent.get_value_of`` works as intended.
    """
    interaction_option_1 = InteractionOption(name = 'fumo', value = 'friday')
    interaction_option_2 = InteractionOption(
        name = 'maou',
        option_type = ApplicationCommandOptionType.sub_command,
        options = [interaction_option_1],
        value = 'day',
    )
    
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.application_command_autocomplete,
        options = [interaction_option_2],
    )
    
    vampytest.assert_eq(interaction_event.get_value_of('maou', 'fumo'), 'friday')


def test__InteractionEvent__iter_components():
    """
    Tests whether ``InteractionEvent.iter_components`` works as intended.
    """
    interaction_component_1 = InteractionComponent(
        ComponentType.text_input,
        custom_id = 'negative',
    )
    interaction_component_2 = InteractionComponent(
        ComponentType.text_input,
        custom_id = 'number',
    )
    
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.form_submit,
        components = [
            interaction_component_2,
            interaction_component_1,
        ],
    )
    vampytest.assert_eq(
        [*interaction_event.iter_components()],
        [interaction_component_2, interaction_component_1],
    )


def test__InteractionEvent__iter_custom_ids_and_values():
    """
    Tests whether ``InteractionEvent.iter_custom_ids_and_values`` works as intended.
    """
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.form_submit,
        components = [
            InteractionComponent(
                ComponentType.row,
                components = [
                    InteractionComponent(
                        ComponentType.text_input,
                        custom_id = 'negative',
                        value = 'ho',
                    ),
                    InteractionComponent(
                        ComponentType.text_input,
                        custom_id = 'number',
                        value = 'lo',
                    ),
                ],
            ),
        ],
    )
    
    vampytest.assert_eq(
        [*interaction_event.iter_custom_ids_and_values()],
        [
            ('negative', ComponentType.text_input, 'ho'),
            ('number', ComponentType.text_input, 'lo'),
        ],
    )
