import vampytest

from ....application_command import ApplicationCommandOptionType
from ....channel import Channel
from ....component import ComponentType
from ....message import Attachment
from ....message import Message
from ....role import Role
from ....user import User

from ...interaction_component import InteractionComponent
from ...interaction_metadata import (
    InteractionMetadataApplicationCommand, InteractionMetadataApplicationCommandAutocomplete,
    InteractionMetadataFormSubmit, InteractionMetadataMessageComponent
)
from ...interaction_option import InteractionOption
from ...resolved import Resolved

from ..interaction_event import InteractionEvent
from ..preinstanced import InteractionType


def test__InteractionEvent__proxies():
    """
    Tests whether ``InteractionEvent`` field proxies work as intended.
    
    Case: Default.
    """
    interaction_event = InteractionEvent()
    
    vampytest.assert_instance(interaction_event.component_type, ComponentType)
    vampytest.assert_instance(interaction_event.components, tuple, nullable = True)
    vampytest.assert_instance(interaction_event.custom_id, str, nullable = True)
    vampytest.assert_instance(interaction_event.application_command_id, int)
    vampytest.assert_instance(interaction_event.application_command_name, str)
    vampytest.assert_instance(interaction_event.options, tuple, nullable = True)
    vampytest.assert_instance(interaction_event.resolved, Resolved, nullable = True)
    vampytest.assert_instance(interaction_event.target_id, int)
    vampytest.assert_instance(interaction_event.values, tuple, nullable = True)


def test__InteractionEvent__proxies_application_command():
    """
    Tests whether ``InteractionEvent`` field proxies work as intended.
    
    Case: application command.
    """
    id_ = 202211100014
    name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    resolved = Resolved(attachments = [Attachment.precreate(202211100015)])
    target_id = 202211100016
    
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.application_command,
        interaction = InteractionMetadataApplicationCommand(
            id = id_,
            name = name,
            options = options,
            resolved = resolved,
            target_id = target_id,
        ),
    )
    
    vampytest.assert_eq(interaction_event.application_command_id, id_)
    vampytest.assert_eq(interaction_event.application_command_name, name)
    vampytest.assert_eq(interaction_event.options, tuple(options))
    vampytest.assert_eq(interaction_event.resolved, resolved)
    vampytest.assert_eq(interaction_event.target_id, target_id)


def test__InteractionEvent__proxies_application_command_autocomplete():
    """
    Tests whether ``InteractionEvent`` field proxies work as intended.
    
    Case: application command autocomplete.
    """
    id_ = 202211100017
    name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.application_command_autocomplete,
        interaction = InteractionMetadataApplicationCommandAutocomplete(
            id = id_,
            name = name,
            options = options,
        ),
    )
    
    vampytest.assert_eq(interaction_event.application_command_id, id_)
    vampytest.assert_eq(interaction_event.application_command_name, name)
    vampytest.assert_eq(interaction_event.options, tuple(options))


def test__InteractionEvent__proxies_message_component():
    """
    Tests whether ``InteractionEvent`` field proxies work as intended.
    
    Case: message component.
    """
    component_type = ComponentType.button
    custom_id = 'Inaba'
    resolved = Resolved(attachments = [Attachment.precreate(202211100018)])
    values = ['black', 'rock', 'shooter']
    
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.message_component,
        interaction = InteractionMetadataMessageComponent(
            component_type = component_type,
            custom_id = custom_id,
            resolved = resolved,
            values = values,
        ),
    )
    
    vampytest.assert_eq(interaction_event.component_type, component_type)
    vampytest.assert_eq(interaction_event.custom_id, custom_id)
    vampytest.assert_eq(interaction_event.resolved, resolved)
    vampytest.assert_eq(interaction_event.values, tuple(values))


def test__InteractionEvent__proxies_form_submit():
    """
    Tests whether ``InteractionEvent`` field proxies work as intended.
    
    Case: form submit.
    """
    custom_id = 'Inaba'
    components = [InteractionComponent(custom_id = 'Rem')]
    
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.form_submit,
        interaction = InteractionMetadataFormSubmit(
            custom_id = custom_id,
            components = components,
        ),
    )
    
    vampytest.assert_eq(interaction_event.custom_id, custom_id)
    vampytest.assert_eq(interaction_event.components, tuple(components))


def test__InteractionEvent__target():
    """
    Tests whether ``InteractionEvent.target`` field proxies work as intended.
    """
    attachment = Attachment.precreate(202211100019)
    
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.application_command,
        interaction = InteractionMetadataApplicationCommand(
            resolved = Resolved(
                attachments = [attachment],
            ),
            target_id = attachment.id,
        )
    )
    
    vampytest.assert_is(interaction_event.target, attachment)


def test__InteractionEvent__iter_options():
    """
    Tests whether ``InteractionEvent.iter_options`` field proxies work as intended.
    """
    interaction_option_1 = InteractionOption(name = 'negative')
    interaction_option_2 = InteractionOption(name = 'number')
    
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.application_command_autocomplete,
        interaction = InteractionMetadataApplicationCommandAutocomplete(
            options = [interaction_option_1, interaction_option_2],
        )
    )
    
    vampytest.assert_eq([*interaction_event.iter_options()], [interaction_option_1, interaction_option_2])


def test__InteractionEvent__focused_option__1():
    """
    Tests whether ``InteractionEvent.focused_option`` works as intended.
    """
    interaction_option_1 = InteractionOption(focused = True)
    
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.application_command_autocomplete,
        interaction = InteractionMetadataApplicationCommandAutocomplete(
            options = [interaction_option_1],
        )
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
        interaction = InteractionMetadataApplicationCommandAutocomplete(
            options = [interaction_option_1, interaction_option_2],
        ),
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
        type_ = ApplicationCommandOptionType.sub_command,
        options = [interaction_option_1],
        value = 'day',
    )
    
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.application_command_autocomplete,
        interaction = InteractionMetadataApplicationCommandAutocomplete(
            options = [interaction_option_2],
        ),
    )
    
    vampytest.assert_eq(interaction_event.get_value_of('maou', 'fumo'), 'friday')


def test__InteractionEvent__value():
    """
    Tests whether ``InteractionEvent.value`` works as intended.
    """
    value = 'Yumemi'
    
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.application_command_autocomplete,
        interaction = InteractionMetadataApplicationCommandAutocomplete(
            options = [InteractionOption(value = value, focused = True)],
        ),
    )
    
    vampytest.assert_eq(interaction_event.value, value)



def test__InteractionEvent__iter_values():
    """
    Tests whether ``InteractionEvent.iter_values`` works as intended.
    """
    values = ['push', 'up']
    
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.message_component,
        interaction = InteractionMetadataMessageComponent(values = values),
    )
    
    vampytest.assert_eq([*interaction_event.iter_values()], values)


def test__InteractionEvent__iter_entries():
    """
    Tests whether ``InteractionEvent.iter_entities`` works as intended.
    """
    role = Role.precreate(202211110000)
    user = User.precreate(202211110001)
    
    resolved = Resolved(
        roles = [role],
        users = [user]
    )
    
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.message_component,
        interaction = InteractionMetadataMessageComponent(
            values = [str(role.id), str(user.id)],
            component_type = ComponentType.mentionable_select,
            resolved = resolved,
        ),
    )
    
    vampytest.assert_eq([*interaction_event.iter_entities()], [role, user])


def test__InteractionEvent__entities():
    """
    Tests whether ``InteractionEvent.entities`` works as intended.
    """
    channel = Channel.precreate(202211110003)
    role = Role.precreate(202211110004)
    user = User.precreate(202211110005)
    
    resolved = Resolved(
        channels = [channel],
        roles = [role],
        users = [user]
    )
    
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.message_component,
        interaction = InteractionMetadataMessageComponent(
            resolved = resolved,
            values = [str(user.id)],
            component_type = ComponentType.user_select,
        ),
    )
    
    vampytest.assert_eq(interaction_event.entities, [user])


def test__InteractionEvent__iter_components():
    """
    Tests whether ``InteractionEvent.iter_components`` works as intended.
    """
    interaction_component_1 = InteractionComponent(custom_id = 'negative')
    interaction_component_2 = InteractionComponent(custom_id = 'number')
    
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.form_submit,
            interaction = InteractionMetadataFormSubmit(
            components = [
                interaction_component_2,
                interaction_component_1,
            ],
        )
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
            interaction = InteractionMetadataFormSubmit(
            components = [
                InteractionComponent(
                    custom_id = 'enclosed',
                    value = 'dancehall',
                    components = [
                        InteractionComponent(
                            custom_id = 'negative',
                            value = 'ho',
                        ),
                        InteractionComponent(
                            custom_id = 'number',
                            value = 'lo',
                        ),
                    ],
                ),
            ],
        ),
    )
    
    vampytest.assert_eq(
        dict(interaction_event.iter_custom_ids_and_values()),
        {'negative': 'ho', 'number': 'lo', 'enclosed': 'dancehall'},
    )


def test__InteractionEvent__get_custom_id_value_relation():
    """
    Tests whether ``InteractionEvent.get_custom_id_value_relation`` works as intended.
    """
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.form_submit,
            interaction = InteractionMetadataFormSubmit(
            components = [
                InteractionComponent(
                    custom_id = 'enclosed',
                    value = 'dancehall',
                    components = [
                        InteractionComponent(
                            custom_id = 'negative',
                            value = 'ho',
                        ),
                        InteractionComponent(
                            custom_id = 'number',
                            value = None,
                        ),
                    ],
                ),
            ],
        ),
    )
    
    vampytest.assert_eq(
        interaction_event.get_custom_id_value_relation(),
        {'negative': 'ho', 'enclosed': 'dancehall'},
    )


def test__InteractionEvent__get_value_for():
    """
    Tests whether ``InteractionEvent.get_value_for`` works as intended.
    """
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.form_submit,
            interaction = InteractionMetadataFormSubmit(
            components = [
                InteractionComponent(
                    custom_id = 'inside',
                    value = 'your mind',
                    components = [
                        InteractionComponent(
                            custom_id = 'Ran',
                            value = None,
                        ),
                        InteractionComponent(
                            custom_id = 'Chen',
                            value = 'Yakumo',
                        ),
                    ],  
                ),  
            ],
        )
    )
    
    vampytest.assert_is(interaction_event.get_value_for('Ran'), None)
    vampytest.assert_is(interaction_event.get_value_for('Chen'), 'Yakumo')
    vampytest.assert_is(interaction_event.get_value_for('Yukari'), None)


def test__InteractionEvent__get_match_and_value():
    """
    Tests whether ``InteractionEvent.get_match_and_value`` works as intended.
    """
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.form_submit,
            interaction = InteractionMetadataFormSubmit(
            components = [
                InteractionComponent(
                    custom_id = 'inside',
                    value = 'your mind',
                    components = [
                        InteractionComponent(
                            custom_id = 'Ran',
                            value = None,
                        ),
                        InteractionComponent(
                            custom_id = 'Chen',
                            value = 'Yakumo',
                        ),
                    ],
                ),
            ],
        ),
    )
    
    vampytest.assert_eq(
        interaction_event.get_match_and_value(lambda custom_id: 'custom_id' if custom_id == 'Chen' else None),
        ('custom_id', 'Yakumo')
    )


def test__InteractionEvent__iter_matches_and_values():
    """
    Tests whether ``InteractionEvent.iter_matches_and_values`` works as intended.
    """
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.form_submit,
            interaction = InteractionMetadataFormSubmit(
            components = [
                InteractionComponent(
                    custom_id = 'inside',
                    value = 'your mind',
                    components = [
                        InteractionComponent(
                            custom_id = 'Ran',
                            value = None,
                        ),
                        InteractionComponent(
                            custom_id = 'Chen',
                            value = 'Yakumo',
                        ),
                    ],  
                ),  
            ],
        ),
    )
    
    vampytest.assert_eq(
        [*interaction_event.iter_matches_and_values(lambda custom_id: 'custom_id' if 'e' in custom_id else None)],
        [('custom_id', 'your mind'), ('custom_id', 'Yakumo')],
    )


def test__InteractionEvent__resolve_attachment():
    """
    Tests whether ``InteractionEvent.resolve_attachment`` works as intended.
    """
    attachment = Attachment.precreate(202211110006)
    
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.application_command_autocomplete,
        interaction = InteractionMetadataApplicationCommand(
            resolved = Resolved(
                attachments = [attachment],
            ),
        ),
    )
    
    vampytest.assert_is(interaction_event.resolve_attachment(attachment.id), attachment)


def test__InteractionEvent__resolve_channel():
    """
    Tests whether ``InteractionEvent.resolve_channel`` works as intended.
    """
    channel = Channel.precreate(202211110007)
    
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.application_command_autocomplete,
        interaction = InteractionMetadataApplicationCommand(
            resolved = Resolved(
                channels = [channel],
            ),
        ),
    )
    vampytest.assert_is(interaction_event.resolve_channel(channel.id), channel)


def test__InteractionEvent__resolve_role():
    """
    Tests whether ``InteractionEvent.resolve_role`` works as intended.
    """
    role = Role.precreate(202211110008)
    
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.application_command_autocomplete,
        interaction = InteractionMetadataApplicationCommand(
            resolved = Resolved(
                roles = [role],
            ),
        ),
    )
    vampytest.assert_is(interaction_event.resolve_role(role.id), role)


def test__InteractionEvent__resolve_message():
    """
    Tests whether ``InteractionEvent.resolve_message`` works as intended.
    """
    message = Message.precreate(202211110009)
    
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.application_command_autocomplete,
        interaction = InteractionMetadataApplicationCommand(
            resolved = Resolved(
                messages = [message],
            ),
        ),
    )
    
    vampytest.assert_is(interaction_event.resolve_message(message.id), message)


def test__InteractionEvent__resolve_user():
    """
    Tests whether ``InteractionEvent.resolve_user`` works as intended.
    """
    user = User.precreate(202211110010)
    
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.application_command_autocomplete,
        interaction = InteractionMetadataApplicationCommand(
            resolved = Resolved(
                users = [user],
            ),
        ),
    )
    
    vampytest.assert_is(interaction_event.resolve_user(user.id), user)


def test__InteractionEvent__resolve_mentionable():
    """
    Tests whether ``InteractionEvent.resolve_mentionable`` works as intended.
    """
    role = Role.precreate(202211110011)
    user = User.precreate(202211110012)
    
    
    interaction_event = InteractionEvent(
        interaction_type = InteractionType.application_command_autocomplete,
        interaction = InteractionMetadataApplicationCommand(
            resolved = Resolved(
                roles = [role],
                users = [user],
            ),
        ),
    )
    vampytest.assert_is(interaction_event.resolve_mentionable(user.id), user)


def test__InteractionEvent__resolve_entity():
    """
    Tests whether ``InteractionEvent.resolve_entity`` works as intended.
    """
    attachment = Attachment.precreate(202211110013)
    channel = Channel.precreate(202211110014)
    message = Message.precreate(202211110015)
    role = Role.precreate(202211110016)
    user = User.precreate(202211110017)
    

    interaction_event = InteractionEvent(
        interaction_type = InteractionType.application_command_autocomplete,
        interaction = InteractionMetadataApplicationCommand(
            resolved = Resolved(
                attachments = [attachment],
                channels = [channel],
                messages = [message],
                roles = [role],
                users = [user]
            ),
        ),
    )
    
    vampytest.assert_is(interaction_event.resolve_entity(role.id), role)
