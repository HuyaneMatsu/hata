import vampytest

from ....application import ApplicationIntegrationType
from ....interaction import InteractionType
from ....user import ClientUserBase, ZEROUSER, create_partial_user_from_id

from ..message_interaction import MessageInteraction

from .test__MessageInteraction__constructor import _assert_fields_set


def _iter_options__partial():
    yield MessageInteraction.precreate(202403250029), False
    yield MessageInteraction(), True


@vampytest._(vampytest.call_from(_iter_options__partial()).returning_last())
def test__MessageInteraction__partial(message_interaction):
    """
    Tests whether ``MessageInteraction.partial`` works as intended.
    
    Parameters
    ----------
    message_interaction : ``MessageInteraction``
        Message interaction to test with.
    
    Returns
    -------
    output : `bool`
    """
    output = message_interaction.partial
    vampytest.assert_instance(output, bool)
    return output


def test__MessageInteraction__copy():
    """
    Tests whether ``MessageInteraction.copy`` works as intended.
    """
    interaction_type = InteractionType.application_command
    user_id = 202403250030
    sub_command_name_stack = ('Afraid', 'Darkness')
    name = 'Chata'
    response_message_id = 20240325012
    interacted_message_id = 20240325043
    triggering_interaction = MessageInteraction.precreate(202403260011, name = 'pain')
    authorizer_user_ids = {
        ApplicationIntegrationType.user_install: 202403270024,
        ApplicationIntegrationType.guild_install: 202403270025,
    }
    
    message_interaction = MessageInteraction(
        authorizer_user_ids = authorizer_user_ids,
        interacted_message_id = interacted_message_id,
        interaction_type = interaction_type,
        name = name,
        response_message_id = response_message_id,
        sub_command_name_stack = sub_command_name_stack,
        triggering_interaction = triggering_interaction,
        user_id = user_id,
    )
    
    copy = message_interaction.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, message_interaction)
    vampytest.assert_eq(copy, message_interaction)


def test__MessageInteraction__copy_with__no_fields():
    """
    Tests whether ``MessageInteraction.copy_with`` works as intended.
    
    Case: No fields given.
    """
    interaction_type = InteractionType.application_command
    user_id = 202403250031
    sub_command_name_stack = ('Afraid', 'Darkness')
    name = 'Chata'
    response_message_id = 20240325013
    interacted_message_id = 20240325044
    triggering_interaction = MessageInteraction.precreate(202403260012, name = 'pain')
    authorizer_user_ids = {
        ApplicationIntegrationType.user_install: 202403270026,
        ApplicationIntegrationType.guild_install: 202403270027,
    }
    
    message_interaction = MessageInteraction(
        authorizer_user_ids = authorizer_user_ids,
        interacted_message_id = interacted_message_id,
        interaction_type = interaction_type,
        name = name,
        response_message_id = response_message_id,
        sub_command_name_stack = sub_command_name_stack,
        triggering_interaction = triggering_interaction,
        user_id = user_id,
    )
    
    copy = message_interaction.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, message_interaction)
    vampytest.assert_eq(copy, message_interaction)


def test__MessageInteraction__copy_with__all_fields():
    """
    Tests whether ``MessageInteraction.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_interaction_type = InteractionType.application_command
    old_user_id = 202403250032
    old_sub_command_name_stack = ('Afraid', 'Darkness')
    old_name = 'Chata'
    old_response_message_id = 20240325014
    old_interacted_message_id = 20240325045
    old_triggering_interaction = MessageInteraction.precreate(202403260013, name = 'pain')
    old_authorizer_user_ids = {
        ApplicationIntegrationType.user_install: 202403270028,
        ApplicationIntegrationType.guild_install: 202403270029,
    }
    
    new_interaction_type = InteractionType.application_command
    new_user_id = 202403250033
    new_sub_command_name_stack = ('Dragon', 'Maid')
    new_name = 'Suika'
    new_response_message_id = 20240325015
    new_interacted_message_id = 20240325046
    new_triggering_interaction = MessageInteraction.precreate(202403260014, name = 'true')
    new_authorizer_user_ids = {
        ApplicationIntegrationType.user_install: 202403270030,
        ApplicationIntegrationType.guild_install: 202403270031,
    }
    
    message_interaction = MessageInteraction(
        authorizer_user_ids = old_authorizer_user_ids,
        interacted_message_id = old_interacted_message_id,
        interaction_type = old_interaction_type,
        name = old_name,
        response_message_id = old_response_message_id,
        sub_command_name_stack = old_sub_command_name_stack,
        triggering_interaction = old_triggering_interaction,
        user_id = old_user_id,
    )
    
    copy = message_interaction.copy_with(
        authorizer_user_ids = new_authorizer_user_ids,
        interacted_message_id = new_interacted_message_id,
        interaction_type = new_interaction_type,
        name = new_name,
        response_message_id = new_response_message_id,
        sub_command_name_stack = new_sub_command_name_stack,
        triggering_interaction = new_triggering_interaction,
        user_id = new_user_id,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, message_interaction)
    
    vampytest.assert_eq(copy.authorizer_user_ids, new_authorizer_user_ids)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.response_message_id, new_response_message_id)
    vampytest.assert_eq(copy.sub_command_name_stack, new_sub_command_name_stack)
    vampytest.assert_eq(copy.triggering_interaction, new_triggering_interaction)
    vampytest.assert_is(copy.type, new_interaction_type)
    vampytest.assert_eq(copy.user_id, new_user_id)


def _iter_options__joined_name():
    yield 'Kobayashi', None, 'Kobayashi'
    yield 'Kobayashi', ('to',), 'Kobayashi to'
    yield 'Kobayashi', ('to', 'Tohru',), 'Kobayashi to Tohru'


@vampytest._(vampytest.call_from(_iter_options__joined_name()).returning_last())
def test__MessageInteraction__joined_name(name, sub_command_name_stack):
    """
    Tests whether ``MessageInteraction.joined_name`` works as intended.
    
    Parameters
    ----------
    name : `str`
        Interaction name.
    sub_command_name_stack : `None | tuple<str>`
        Additional name stack of the sub command.
    
    Returns
    -------
    output : `str`
    """
    message_interaction = MessageInteraction(
        name = name,
        sub_command_name_stack = sub_command_name_stack,
    )
    
    output = message_interaction.joined_name
    vampytest.assert_instance(output, str)
    return output


def _iter_options__user():
    user_id = 202403250054
    
    yield 0, ZEROUSER
    yield user_id, create_partial_user_from_id(user_id)


@vampytest._(vampytest.call_from(_iter_options__user()).returning_last())
def test__MessageInteraction__user(user_id):
    """
    Tests whether ``MessageInteraction.user`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    Returns
    -------
    output : ``ClientUserBase``
    """
    message_interaction = MessageInteraction(
        user_id = user_id,
    )
    
    output = message_interaction.user
    vampytest.assert_instance(output, ClientUserBase)
    return output


def _iter_options__get_authorizer_user_id():
    user_id = 202403270032
    
    yield (
        None,
        ApplicationIntegrationType.user_install,
        0,
    )
    
    yield (
        {
            ApplicationIntegrationType.user_install: user_id,
        },
        ApplicationIntegrationType.user_install,
        user_id,
    )
    
    yield (
        {
            ApplicationIntegrationType.guild_install: user_id,
        },
        ApplicationIntegrationType.user_install,
        0,
    )
    
    yield (
        {
            ApplicationIntegrationType.guild_install: user_id,
        },
        ApplicationIntegrationType.guild_install,
        user_id,
    )
    
    yield (
        {
            ApplicationIntegrationType.guild_install: user_id,
        },
        ApplicationIntegrationType.user_install,
        0,
    )
    
    
    yield (
        {
            ApplicationIntegrationType.user_install: user_id,
        },
        ApplicationIntegrationType.user_install.value,
        user_id,
    )


@vampytest._(vampytest.call_from(_iter_options__get_authorizer_user_id()).returning_last())
def test__MessageInteraction__get_authorizer_user_id(authorizer_user_ids, integration_type):
    """
    Tests whether ``MessageInteraction.get_authorizer_user_id`` works as intended.
    
    Parameters
    ----------
    authorizer_user_ids : `int`
        The invoking authorizer_user_id's identifier.
    
    integration_type : `ApplicationIntegrationType | int`
        Integration type to query for.
    
    Returns
    -------
    output : `int`
    """
    message_interaction = MessageInteraction(
        authorizer_user_ids = authorizer_user_ids,
    )
    
    output = message_interaction.get_authorizer_user_id(integration_type)
    vampytest.assert_instance(output, int)
    return output


def _iter_options__get_authorizer_user():
    user_id = 202403270033
    user = create_partial_user_from_id(user_id)
    
    yield (
        None,
        ApplicationIntegrationType.user_install,
        None,
    )
    
    yield (
        {
            ApplicationIntegrationType.user_install: user_id,
        },
        ApplicationIntegrationType.user_install,
        user,
    )
    
    yield (
        {
            ApplicationIntegrationType.guild_install: user_id,
        },
        ApplicationIntegrationType.user_install,
        None,
    )
    
    yield (
        {
            ApplicationIntegrationType.guild_install: user_id,
        },
        ApplicationIntegrationType.guild_install,
        user,
    )
    
    yield (
        {
            ApplicationIntegrationType.guild_install: user_id,
        },
        ApplicationIntegrationType.user_install,
        None,
    )
    
    
    yield (
        {
            ApplicationIntegrationType.user_install: user_id,
        },
        ApplicationIntegrationType.user_install.value,
        user,
    )


@vampytest._(vampytest.call_from(_iter_options__get_authorizer_user()).returning_last())
def test__MessageInteraction__get_authorizer_user(authorizer_user_ids, integration_type):
    """
    Tests whether ``MessageInteraction.get_authorizer_user`` works as intended.
    
    Parameters
    ----------
    authorizer_user_ids : `int`
        The invoking authorizer_user_id's identifier.
    
    integration_type : `ApplicationIntegrationType | int`
        Integration type to query for.
    
    Returns
    -------
    output : `None | ClientUserBase`
    """
    message_interaction = MessageInteraction(
        authorizer_user_ids = authorizer_user_ids,
    )
    
    output = message_interaction.get_authorizer_user(integration_type)
    vampytest.assert_instance(output, ClientUserBase, nullable = True)
    return output
