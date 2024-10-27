import vampytest

from ....application import ApplicationIntegrationType
from ....interaction import InteractionType
from ....user import User

from ..message_interaction import MessageInteraction


def test__MessageInteraction__repr():
    """
    tests whether ``MessageInteraction.__repr__`` works as intended.
    """
    message_interaction_id = 202403250021
    
    interaction_type = InteractionType.application_command
    user = User.precreate(202403250022)
    sub_command_name_stack = ('Afraid', 'Darkness')
    name = 'Chata'
    response_message_id = 20240325009
    interacted_message_id = 20240325040
    target_message_id = 202410060014
    target_user = User.precreate(202410060015)
    triggering_interaction = MessageInteraction.precreate(202403260008, name = 'pain')
    authorizer_user_ids = {
        ApplicationIntegrationType.user_install: 202403270018,
        ApplicationIntegrationType.guild_install: 202403270019,
    }
    
    message_interaction = MessageInteraction.precreate(
        message_interaction_id,
        authorizer_user_ids = authorizer_user_ids,
        interacted_message_id = interacted_message_id,
        interaction_type = interaction_type,
        name = name,
        response_message_id = response_message_id,
        sub_command_name_stack = sub_command_name_stack,
        target_message_id = target_message_id,
        target_user = target_user,
        triggering_interaction = triggering_interaction,
        user = user,
    )
    
    vampytest.assert_instance(repr(message_interaction), str)


def test__MessageInteraction__hash():
    """
    tests whether ``MessageInteraction.__hash__`` works as intended.
    """
    message_interaction_id = 202403250023
    
    interaction_type = InteractionType.application_command
    user = User.precreate(202403250024)
    sub_command_name_stack = ('Afraid', 'Darkness')
    name = 'Chata'
    response_message_id = 20240325010
    interacted_message_id = 20240325041
    target_message_id = 202410060016
    target_user = User.precreate(202410060017)
    triggering_interaction = MessageInteraction.precreate(202403260009, name = 'pain')
    authorizer_user_ids = {
        ApplicationIntegrationType.user_install: 202403270020,
        ApplicationIntegrationType.guild_install: 202403270021,
    }
    
    message_interaction = MessageInteraction.precreate(
        message_interaction_id,
        authorizer_user_ids = authorizer_user_ids,
        interacted_message_id = interacted_message_id,
        interaction_type = interaction_type,
        name = name,
        response_message_id = response_message_id,
        sub_command_name_stack = sub_command_name_stack,
        target_message_id = target_message_id,
        target_user = target_user,
        triggering_interaction = triggering_interaction,
        user = user,
    )
    
    vampytest.assert_instance(hash(message_interaction), int)


def _iter_options__eq():
    interaction_type = InteractionType.application_command
    user = User.precreate(202403250027)
    sub_command_name_stack = ('Afraid', 'Darkness')
    name = 'Chata'
    response_message_id = 20240325011
    interacted_message_id = 20240325042
    target_message_id = 202410060018
    target_user = User.precreate(202410060019)
    triggering_interaction = MessageInteraction.precreate(202403260010, name = 'pain')
    authorizer_user_ids = {
        ApplicationIntegrationType.user_install: 202403270022,
        ApplicationIntegrationType.guild_install: 202403270023,
    }
    
    keyword_parameters = {
        'authorizer_user_ids': authorizer_user_ids,
        'interacted_message_id': interacted_message_id,
        'interaction_type': interaction_type,
        'name': name,
        'response_message_id': response_message_id,
        'sub_command_name_stack': sub_command_name_stack,
        'target_message_id': target_message_id,
        'target_user': target_user,
        'triggering_interaction': triggering_interaction,
        'user': user,
    }
    
    yield (
        {},
        {},
        True,
    )
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'authorizer_user_ids': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'interacted_message_id': 0,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'name': 'Slayer',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'response_message_id': 0,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'interaction_type': InteractionType.form_submit,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'sub_command_name_stack': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'target_message_id': 0,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'target_user': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'triggering_interaction': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'user': User.precreate(202403250028),
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__MessageInteraction__eq__partial(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``MessageInteraction.__eq__`` works as intended.
    
    Case: partial.
    
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
    message_interaction_0 = MessageInteraction(**keyword_parameters_0)
    message_interaction_1 = MessageInteraction(**keyword_parameters_1)
    
    output = message_interaction_0 == message_interaction_1
    vampytest.assert_instance(output, bool)
    return output


def test__MessageInteraction__eq__partial_with_non_partial():
    """
    Tests whether ``MessageInteraction.__eq__`` works as intended.
    
    Case: Partial with non-partial.
    """
    name = 'Afraid'
    message_interaction_id_0 = 202403250025
    message_interaction_id_1 = 202403250026
    
    message_interaction_0 = MessageInteraction.precreate(message_interaction_id = message_interaction_id_0, name = name)
    message_interaction_1 = MessageInteraction.precreate(message_interaction_id = message_interaction_id_1)
    message_interaction_2 = MessageInteraction(name = name)
    
    vampytest.assert_ne(message_interaction_0, message_interaction_1)
    vampytest.assert_eq(message_interaction_0, message_interaction_2)
    vampytest.assert_ne(message_interaction_1, message_interaction_2)
