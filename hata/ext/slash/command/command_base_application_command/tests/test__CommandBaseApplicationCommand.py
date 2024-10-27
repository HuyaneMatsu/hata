import vampytest
from scarletio import WeakReferer

from ......discord.application import ApplicationIntegrationType
from ......discord.application_command import (
    ApplicationCommand, ApplicationCommandIntegrationContextType, ApplicationCommandPermissionOverwrite,
    ApplicationCommandPermissionOverwriteTargetType, ApplicationCommandTargetType, INTEGRATION_CONTEXT_TYPES_ALL
)
from ......discord.client import Client
from ......discord.client.compounds.tests.helpers import TestDiscordApiClient
from ......discord.events.handling_helpers import check_name
from ......discord.interaction import InteractionEvent, InteractionOption
from ......discord.permission import Permission

from ....response_modifier import ResponseModifier
from ....utils import (
    SYNC_ID_GLOBAL, SYNC_ID_NON_GLOBAL, UNLOADING_BEHAVIOUR_DELETE, UNLOADING_BEHAVIOUR_INHERIT,
    UNLOADING_BEHAVIOUR_KEEP
)

from ..command_base_application_command import CommandBaseApplicationCommand
from ..helpers import (
    _validate_delete_on_unload, _validate_guild, _validate_integration_context_types, _validate_integration_types,
    _validate_is_global, _validate_name, _validate_nsfw, _validate_required_permissions
)


def _assert_fields_set(command_base_application_command):
    """
    Asserts whether the given instance has all of its fields set.
    
    Parameters
    ----------
    command_base_application_command : ``CommandBaseApplicationCommand``
        The command to checkout.
    """
    vampytest.assert_instance(command_base_application_command, CommandBaseApplicationCommand)
    vampytest.assert_instance(command_base_application_command._exception_handlers, list, nullable = True)
    vampytest.assert_instance(command_base_application_command._parent_reference, WeakReferer, nullable = True)
    vampytest.assert_instance(command_base_application_command.name, str)
    vampytest.assert_instance(command_base_application_command._permission_overwrites, dict, nullable = True)
    vampytest.assert_instance(
        command_base_application_command._registered_application_command_ids, dict, nullable = True,
    )
    vampytest.assert_instance(command_base_application_command._schema, ApplicationCommand, nullable = True)
    vampytest.assert_instance(command_base_application_command._unloading_behaviour, int)
    vampytest.assert_instance(command_base_application_command.global_, bool)
    vampytest.assert_instance(command_base_application_command.guild_ids, set, nullable = True)
    vampytest.assert_instance(command_base_application_command.integration_context_types, tuple, nullable = True)
    vampytest.assert_instance(command_base_application_command.integration_types, tuple, nullable = True)
    vampytest.assert_instance(command_base_application_command.nsfw, bool)
    vampytest.assert_instance(command_base_application_command.required_permissions, Permission)


class InstantiableCommandBaseApplicationCommand(CommandBaseApplicationCommand):
    __slots__ = ()
    
    def __new__(
        cls,
        function,
        name = None,
        *,
        delete_on_unload = ...,
        guild = ...,
        integration_context_types = ...,
        integration_types = ...,
        is_global = ...,
        nsfw = ...,
        required_permissions = ...,
        **keyword_parameters,
    ):
        name = _validate_name(name)
        name = check_name(function, name)
        
        # delete_on_unload
        if delete_on_unload is ...:
            unloading_behaviour = UNLOADING_BEHAVIOUR_INHERIT
        elif _validate_delete_on_unload(delete_on_unload):
            unloading_behaviour = UNLOADING_BEHAVIOUR_DELETE
        else:
            unloading_behaviour = UNLOADING_BEHAVIOUR_KEEP
        
        # guild
        if guild is ...:
            guild_ids = None
        else:
            guild_ids = _validate_guild(guild)
        
        # integration_context_types
        if integration_context_types is ...:
            integration_context_types = INTEGRATION_CONTEXT_TYPES_ALL
        else:
            integration_context_types = _validate_integration_context_types(integration_context_types)
        
        # integration_types
        if integration_types is ...:
            integration_types = (ApplicationCommandIntegrationContextType.guild,)
        else:
            integration_types = _validate_integration_types(integration_types)
        
        # is_global
        if is_global is ...:
            is_global = False
        else:
            is_global = _validate_is_global(is_global)
        
        # nsfw
        if nsfw is ...:
            nsfw = False
        else:
            nsfw = _validate_nsfw(nsfw)
        
        # required_permissions
        if required_permissions is ...:
            required_permissions = Permission()
        else:
            required_permissions = _validate_required_permissions(required_permissions)
        
        # Check extra parameters
        response_modifier = ResponseModifier(keyword_parameters)
        if keyword_parameters:
            raise TypeError(
                f'Extra or unused parameters: {keyword_parameters!r}.'
            )
        
        self = object.__new__(cls)
        self._exception_handlers = None
        self._parent_reference = None
        self.name = name
        
        self._permission_overwrites = None
        self._registered_application_command_ids = None
        self._schema = None
        self._unloading_behaviour = unloading_behaviour
        self.global_ = is_global
        self.guild_ids = guild_ids
        self.integration_context_types = integration_context_types
        self.integration_types = integration_types
        self.nsfw = nsfw
        self.required_permissions = required_permissions
        return self


def test__CommandBaseApplicationCommand__new():
    """
    Tests whether ``CommandBaseApplicationCommand.__new__`` works as intended.
    """
    async def function():
        pass
    
    name = 'yuuka'
    
    with vampytest.assert_raises(NotImplementedError):
        CommandBaseApplicationCommand(function, name)


def test__CommandBaseApplicationCommand__repr():
    """
    Tests whether ``CommandBaseApplicationCommand.__repr__`` works as intended.
    """
    # Note: guild cannot be `None` and is mutually exclusive is `is_global`.
    async def function():
        pass
    
    name = 'yuuka'
    delete_on_unload = True
    # guild = None
    integration_context_types = [
        ApplicationCommandIntegrationContextType.guild,
        ApplicationCommandIntegrationContextType.bot_private_channel,
    ]
    integration_types = [
        ApplicationIntegrationType.guild_install,
        ApplicationIntegrationType.user_install,
    ]
    is_global = True
    nsfw = True
    required_permissions = Permission(8)
    
    
    async def exception_handler(client, interaction_event, command, exception):
        return
    
    command_base_application_command = InstantiableCommandBaseApplicationCommand(
        function,
        name,
        delete_on_unload = delete_on_unload,
        # guild = guild,
        integration_context_types = integration_context_types,
        integration_types = integration_types,
        is_global = is_global,
        nsfw = nsfw,
        required_permissions = required_permissions,
    )
    command_base_application_command.error(exception_handler)
    
    output = repr(command_base_application_command)
    vampytest.assert_in(type(command_base_application_command).__name__, output)
    vampytest.assert_in(f'name = {name!r}', output)
    vampytest.assert_in(f'exception_handlers = {[exception_handler]!r}', output)
    vampytest.assert_in(f'type = global', output)
    vampytest.assert_in(f'unloading_behaviour = delete', output)
    vampytest.assert_in(f'integration_context_types = {tuple(integration_context_types)!r}', output)
    vampytest.assert_in(f'integration_types = {tuple(integration_types)!r}', output)
    vampytest.assert_in(f'nsfw = {nsfw!r}', output)
    vampytest.assert_in(f'required_permissions = {required_permissions!r}', output)


def test__CommandBaseApplicationCommand__hash():
    """
    Tests whether ``CommandBaseApplicationCommand.__hash__`` works as intended.
    """
    # Note: guild cannot be `None` and is mutually exclusive is `is_global`.
    async def function():
        pass
    
    name = 'yuuka'
    delete_on_unload = True
    # guild = None
    integration_context_types = [
        ApplicationCommandIntegrationContextType.guild,
        ApplicationCommandIntegrationContextType.bot_private_channel,
    ]
    integration_types = [
        ApplicationIntegrationType.guild_install,
        ApplicationIntegrationType.user_install,
    ]
    is_global = True
    nsfw = True
    required_permissions = Permission(8)
    
    
    async def exception_handler(client, interaction_event, command, exception):
        return
    
    command_base_application_command = InstantiableCommandBaseApplicationCommand(
        function,
        name,
        delete_on_unload = delete_on_unload,
        # guild = guild,
        integration_context_types = integration_context_types,
        integration_types = integration_types,
        is_global = is_global,
        nsfw = nsfw,
        required_permissions = required_permissions,
    )
    command_base_application_command.error(exception_handler)
    
    output = hash(command_base_application_command)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    async def function_0():
        pass
    
    name = 'yuuka'
    delete_on_unload = True
    guild = [202410230000, 202410230001]
    integration_context_types = [
        ApplicationCommandIntegrationContextType.guild,
        ApplicationCommandIntegrationContextType.bot_private_channel,
    ]
    integration_types = [
        ApplicationIntegrationType.guild_install,
        ApplicationIntegrationType.user_install,
    ]
    is_global = True
    nsfw = True
    required_permissions = Permission(8)
    
    async def exception_handler(client, interaction_event, command, exception):
        return
    
    keyword_parameters = {
        'function': function_0,
        'name': name,
        'delete_on_unload': delete_on_unload,
        'guild': guild,
        'integration_context_types': integration_context_types,
        'integration_types': integration_types,
        'is_global': is_global,
        'nsfw': nsfw,
        'required_permissions': required_permissions,
    }
    
    yield (
        keyword_parameters,
        (),
        keyword_parameters,
        (),
        True,
    )
    
    yield (
        keyword_parameters,
        (),
        {
            **keyword_parameters,
            'name': 'kazami',
        },
        (),
        False,
    )
    
    yield (
        keyword_parameters,
        (),
        {
            **keyword_parameters,
            'delete_on_unload': False,
        },
        (),
        False,
    )
    
    yield (
        keyword_parameters,
        (),
        {
            **keyword_parameters,
            'guild': [202410230003, 202410230004],
        },
        (),
        False,
    )
    
    yield (
        keyword_parameters,
        (),
        {
            **keyword_parameters,
            'integration_context_types': [ApplicationCommandIntegrationContextType.guild],
        },
        (),
        False,
    )
    
    yield (
        keyword_parameters,
        (),
        {
            **keyword_parameters,
            'integration_types': [ApplicationIntegrationType.guild_install],
        },
        (),
        False,
    )
    
    yield (
        keyword_parameters,
        (),
        {
            **keyword_parameters,
            'is_global': False,
        },
        (),
        False,
    )
    
    yield (
        keyword_parameters,
        (),
        {
            **keyword_parameters,
            'nsfw': False,
        },
        (),
        False,
    )
    
    yield (
        keyword_parameters,
        (),
        {
            **keyword_parameters,
            'required_permissions': Permission(6),
        },
        (),
        False,
    )
    
    yield (
        keyword_parameters,
        (),
        keyword_parameters,
        (exception_handler,),
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__CommandBaseApplicationCommand__eq(keyword_parameters_0, exception_handlers_0, keyword_parameters_1, exception_handlers_1):
    """
    Tests whether ``CommandBaseApplicationCommand.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    exception_handlers_0 : `tuple<CoroutineFunctionType>`
        Exception handlers to register to the instance.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    exception_handlers_1 : `tuple<CoroutineFunctionType>`
        Exception handlers to register to the instance.
    
    Returns
    -------
    output : `bool`
    """
    command_base_application_command_0 = InstantiableCommandBaseApplicationCommand(**keyword_parameters_0)
    for exception_handler in exception_handlers_0:
        command_base_application_command_0.error(exception_handler)
    
    command_base_application_command_1 = InstantiableCommandBaseApplicationCommand(**keyword_parameters_1)
    for exception_handler in exception_handlers_1:
        command_base_application_command_1.error(exception_handler)
    
    output = command_base_application_command_0 == command_base_application_command_1
    vampytest.assert_instance(output, bool)
    return output


def test__CommandBaseApplicationCommand__copy():
    """
    Tests whether ``CommandBaseApplicationCommand.copy`` works as intended.
    """
    async def function():
        pass
    
    name = 'yuuka'
    delete_on_unload = True
    # guild = None
    integration_context_types = [
        ApplicationCommandIntegrationContextType.guild,
        ApplicationCommandIntegrationContextType.bot_private_channel,
    ]
    integration_types = [
        ApplicationIntegrationType.guild_install,
        ApplicationIntegrationType.user_install,
    ]
    is_global = True
    nsfw = True
    required_permissions = Permission(8)
    
    
    async def exception_handler(client, interaction_event, command, exception):
        return
    
    command_base_application_command = InstantiableCommandBaseApplicationCommand(
        function,
        name,
        delete_on_unload = delete_on_unload,
        # guild = guild,
        integration_context_types = integration_context_types,
        integration_types = integration_types,
        is_global = is_global,
        nsfw = nsfw,
        required_permissions = required_permissions,
    )
    command_base_application_command.error(exception_handler)
    copy = command_base_application_command.copy()
    _assert_fields_set(copy)
    vampytest.assert_eq(copy, command_base_application_command)


def test__CommandBaseApplicationCommand__target():
    """
    Tests whether ``CommandBaseApplicationCommand.target`` works as intended.
    """
    function = None
    name = 'yuuka'
    
    command_base_application_command = InstantiableCommandBaseApplicationCommand(function, name)
    
    output = command_base_application_command.target
    vampytest.assert_instance(output, ApplicationCommandTargetType)
    vampytest.assert_is(output, ApplicationCommandTargetType.none)


def test__CommandBaseApplicationCommand__default():
    """
    Tests whether ``CommandBaseApplicationCommand.default`` works as intended.
    """
    function = None
    name = 'yuuka'
    
    command_base_application_command = InstantiableCommandBaseApplicationCommand(function, name)
    
    output = command_base_application_command.default
    vampytest.assert_instance(output, bool)
    vampytest.assert_is(output, False)


def test__CommandBaseApplicationCommand__description():
    """
    Tests whether ``CommandBaseApplicationCommand.description`` works as intended.
    """
    function = None
    name = 'yuuka'
    
    command_base_application_command = InstantiableCommandBaseApplicationCommand(function, name)
    
    output = command_base_application_command.description
    vampytest.assert_instance(output, str, nullable = True)
    vampytest.assert_is(output, None)


async def test__CommandBase__invoke_auto_completion():
    """
    Tests whether ``CommandBase.invoke_auto_completion`` works as intended.
    
    This function is a coroutine.
    """
    function = None
    name = 'yuuka'
    
    command_base_application_command = InstantiableCommandBaseApplicationCommand(function, name)
    auto_complete_option = InteractionOption()
    
    client_id = 202410220000
    interaction_event_id = 202410220001
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    
    client = Client(
        token,
        api = api,
        client_id = client_id,
    )
    interaction_event = InteractionEvent.precreate(interaction_event_id)
    
    try:
        await command_base_application_command.invoke_auto_completion(client, interaction_event, auto_complete_option)
        
    finally:
        client._delete()
        client = None


def test__CommandBaseApplicationCommand__mention__no_sync():
    """
    Tests whether ``CommandBaseApplicationCommand.mention`` works as intended.
    
    Case: no sync.
    """
    function = None
    name = 'yuuka'
    
    command_base_application_command = InstantiableCommandBaseApplicationCommand(function, name)
    
    output = command_base_application_command.mention
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, f'/{name!s}')


def test__CommandBaseApplicationCommand__mention__sync_global():
    """
    Tests whether ``CommandBaseApplicationCommand.mention`` works as intended.
    
    Case: synced global.
    """
    function = None
    name = 'yuuka'
    is_global = True
    application_command_id = 202410220002
    
    command_base_application_command = InstantiableCommandBaseApplicationCommand(
        function,
        name,
        is_global = is_global,
    )
    command_base_application_command._register_guild_and_application_command_id(SYNC_ID_GLOBAL, application_command_id)
    
    output = command_base_application_command.mention
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, f'</{name!s}:{application_command_id!s}>')


def test__CommandBaseApplicationCommand__mention_at__no_sync():
    """
    Tests whether ``CommandBaseApplicationCommand.mention_at`` works as intended.
    
    Case: no sync.
    """
    function = None
    name = 'yuuka'
    guild_id = 202410220003
    
    command_base_application_command = InstantiableCommandBaseApplicationCommand(
        function,
        name,
        guild = guild_id,
    )
    
    output = command_base_application_command.mention_at(guild_id)
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, f'/{name!s}')


def test__CommandBaseApplicationCommand__mention_at__sync_guild():
    """
    Tests whether ``CommandBaseApplicationCommand.mention_at`` works as intended.
    
    Case: synced guild.
    """
    function = None
    name = 'yuuka'
    guild_id = 202410220004
    application_command_id = 202410220005
    
    command_base_application_command = InstantiableCommandBaseApplicationCommand(
        function,
        name,
        guild = guild_id,
    )
    command_base_application_command._register_guild_and_application_command_id(guild_id, application_command_id)
    
    output = command_base_application_command.mention_at(guild_id)
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, f'</{name!s}:{application_command_id!s}>')


def test__CommandBaseApplicationCommand__get_real_command_count():
    """
    Tests whether ``CommandBaseApplicationCommand.get_real_command_count`` works as intended.
    """
    function = None
    name = 'yuuka'
    
    command_base_application_command = InstantiableCommandBaseApplicationCommand(function, name)
    
    output = command_base_application_command.get_real_command_count()
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 1)


def test__CommandBaseApplicationCommand__interactions():
    """
    Tests whether ``CommandBaseApplicationCommand.interactions`` works as intended.
    """
    function = None
    name = 'yuuka'
    
    command_base_application_command = InstantiableCommandBaseApplicationCommand(function, name)
    
    with vampytest.assert_raises(RuntimeError):
        command_base_application_command.interactions()


def test__CommandBaseApplicationCommand__add_permission_overwrite__add():
    """
    Tests whether ``CommandBaseApplicationCommand.add_permission_overwrite`` works as intended.
    
    Case: add.
    """
    function = None
    name = 'yuuka'
    guild_id = 202410220006
    
    permission_overwrite_0 = ApplicationCommandPermissionOverwrite(
        (ApplicationCommandPermissionOverwriteTargetType.role, 202410220008),
        True,
    )
    permission_overwrite_1 = ApplicationCommandPermissionOverwrite(
        (ApplicationCommandPermissionOverwriteTargetType.role, 202410220009),
        True,
    )
    
    command_base_application_command = InstantiableCommandBaseApplicationCommand(
        function,
        name,
        guild = guild_id,
    )
    
    command_base_application_command.add_permission_overwrite(guild_id, permission_overwrite_0)
    vampytest.assert_eq(
        command_base_application_command._permission_overwrites,
        {
            guild_id: [permission_overwrite_0],
        }
    )
    
    command_base_application_command.add_permission_overwrite(guild_id, permission_overwrite_1)
    vampytest.assert_eq(
        command_base_application_command._permission_overwrites,
        {
            guild_id: [permission_overwrite_0, permission_overwrite_1],
        }
    )


def test__CommandBaseApplicationCommand__add_permission_overwrite__add_inverted():
    """
    Tests whether ``CommandBaseApplicationCommand.add_permission_overwrite`` works as intended.
    
    Case: add inverted.
    """
    function = None
    name = 'yuuka'
    guild_id = 202410220010
    
    permission_overwrite_0 = ApplicationCommandPermissionOverwrite(
        (ApplicationCommandPermissionOverwriteTargetType.role, 202410220011),
        True,
    )
    permission_overwrite_1 = ApplicationCommandPermissionOverwrite(
        (ApplicationCommandPermissionOverwriteTargetType.role, 202410220011),
        False,
    )
    
    command_base_application_command = InstantiableCommandBaseApplicationCommand(
        function,
        name,
        guild = guild_id,
    )
    
    command_base_application_command.add_permission_overwrite(guild_id, permission_overwrite_0)
    command_base_application_command.add_permission_overwrite(guild_id, permission_overwrite_1)
    
    vampytest.assert_eq(
        command_base_application_command._permission_overwrites,
        {
            guild_id: None,
        }
    )


def test__CommandBaseApplicationCommand__add_permission_overwrite__add_two_guild():
    """
    Tests whether ``CommandBaseApplicationCommand.add_permission_overwrite`` works as intended.
    
    Case: add two guild.
    """
    function = None
    name = 'yuuka'
    guild_id_0 = 202410220013
    guild_id_1 = 202410220014
    
    permission_overwrite_0 = ApplicationCommandPermissionOverwrite(
        (ApplicationCommandPermissionOverwriteTargetType.role, 202410220015),
        True,
    )
    permission_overwrite_1 = ApplicationCommandPermissionOverwrite(
        (ApplicationCommandPermissionOverwriteTargetType.role, 202410220016),
        True,
    )
    
    command_base_application_command = InstantiableCommandBaseApplicationCommand(
        function,
        name,
        guild = [guild_id_0, guild_id_1],
    )
    
    command_base_application_command.add_permission_overwrite(guild_id_0, permission_overwrite_0)
    command_base_application_command.add_permission_overwrite(guild_id_1, permission_overwrite_1)
    
    vampytest.assert_eq(
        command_base_application_command._permission_overwrites,
        {
            guild_id_0: [permission_overwrite_0],
            guild_id_1: [permission_overwrite_1],
        }
    )


def test__CommandBaseApplicationCommand__add_permission_overwrite__none_before_added():
    """
    Tests whether ``CommandBaseApplicationCommand.add_permission_overwrite`` works as intended.
    
    Case: adding none & before added.
    """
    function = None
    name = 'yuuka'
    guild_id = 202410220017
    
    permission_overwrite = ApplicationCommandPermissionOverwrite(
        (ApplicationCommandPermissionOverwriteTargetType.role, 202410220018),
        True,
    )
    
    command_base_application_command = InstantiableCommandBaseApplicationCommand(
        function,
        name,
        guild = guild_id,
    )
    
    command_base_application_command.add_permission_overwrite(guild_id, permission_overwrite)
    command_base_application_command.add_permission_overwrite(guild_id, None)
    
    vampytest.assert_eq(
        command_base_application_command._permission_overwrites,
        {
            guild_id: [permission_overwrite],
        },
    )


def test__CommandBaseApplicationCommand__add_permission_overwrite__none_before_not_added():
    """
    Tests whether ``CommandBaseApplicationCommand.add_permission_overwrite`` works as intended.
    
    Case: adding none & before not added.
    """
    function = None
    name = 'yuuka'
    guild_id = 202410220019
    
    command_base_application_command = InstantiableCommandBaseApplicationCommand(
        function,
        name,
        guild = guild_id,
    )
    
    command_base_application_command.add_permission_overwrite(guild_id, None)
    
    vampytest.assert_eq(
        command_base_application_command._permission_overwrites,
        {
            guild_id: None,
        },
    )


def test__CommandBaseApplicationCommand__add_permission_overwrite__none_has_leftover():
    """
    Tests whether ``CommandBaseApplicationCommand.add_permission_overwrite`` works as intended.
    
    Case: adding none & has leftover.
    """
    function = None
    name = 'yuuka'
    guild_id_0 = 202410220020
    guild_id_1 = 202410220022
    
    permission_overwrite = ApplicationCommandPermissionOverwrite(
        (ApplicationCommandPermissionOverwriteTargetType.role, 202410220021),
        True,
    )
    
    command_base_application_command = InstantiableCommandBaseApplicationCommand(
        function,
        name,
        guild = [guild_id_0, guild_id_1],
    )
    
    command_base_application_command.add_permission_overwrite(guild_id_0, permission_overwrite)
    command_base_application_command.add_permission_overwrite(guild_id_1, None)
    
    vampytest.assert_eq(
        command_base_application_command._permission_overwrites,
        {
            guild_id_0: [permission_overwrite],
            guild_id_1: None,
        },
    )


def test__CommandBaseApplicationCommand__get_permission_overwrites_for__none():
    """
    Tests whether ``CommandBaseApplicationCommand.get_permission_overwrites_for`` works as intended.
    
    Case: none.
    """
    function = None
    name = 'yuuka'
    guild_id = 202410220023
    
    command_base_application_command = InstantiableCommandBaseApplicationCommand(
        function,
        name,
        guild = guild_id,
    )
    
    output = command_base_application_command.get_permission_overwrites_for(guild_id)
    vampytest.assert_instance(output, list, nullable = True)
    vampytest.assert_eq(output, None)


def test__CommandBaseApplicationCommand__get_permission_overwrites_for__different_guild():
    """
    Tests whether ``CommandBaseApplicationCommand.get_permission_overwrites_for`` works as intended.
    
    Case: different guild.
    """
    function = None
    name = 'yuuka'
    guild_id_0 = 202410220024
    guild_id_1 = 202410220025
    
    permission_overwrite = ApplicationCommandPermissionOverwrite(
        (ApplicationCommandPermissionOverwriteTargetType.role, 202410220026),
        True,
    )
    
    command_base_application_command = InstantiableCommandBaseApplicationCommand(
        function,
        name,
        guild = [guild_id_0, guild_id_1],
    )
    
    command_base_application_command.add_permission_overwrite(guild_id_0, permission_overwrite)
    output = command_base_application_command.get_permission_overwrites_for(guild_id_1)
    vampytest.assert_instance(output, list, nullable = True)
    vampytest.assert_eq(output, None)


def test__CommandBaseApplicationCommand__get_permission_overwrites_for__hit():
    """
    Tests whether ``CommandBaseApplicationCommand.get_permission_overwrites_for`` works as intended.
    
    Case: hit.
    """
    function = None
    name = 'yuuka'
    guild_id = 202410220027
    
    permission_overwrite = ApplicationCommandPermissionOverwrite(
        (ApplicationCommandPermissionOverwriteTargetType.role, 202410220028),
        True,
    )
    
    command_base_application_command = InstantiableCommandBaseApplicationCommand(
        function,
        name,
        guild = guild_id,
    )
    
    command_base_application_command.add_permission_overwrite(guild_id, permission_overwrite)
    output = command_base_application_command.get_permission_overwrites_for(guild_id)
    vampytest.assert_instance(output, list, nullable = True)
    vampytest.assert_eq(output, [permission_overwrite])


def test__CommandBaseApplicationCommand__get_permission_sync_ids__none():
    """
    Tests whether ``CommandBaseApplicationCommand._get_permission_sync_ids`` works as intended.
    
    Case: none.
    """
    function = None
    name = 'yuuka'
    
    command_base_application_command = InstantiableCommandBaseApplicationCommand(
        function,
        name,
    )
    
    output = command_base_application_command._get_permission_sync_ids()
    vampytest.assert_instance(output, set)
    vampytest.assert_eq(output, set())


def test__CommandBaseApplicationCommand__get_permission_sync_ids__guild_ids():
    """
    Tests whether ``CommandBaseApplicationCommand._get_permission_sync_ids`` works as intended.
    
    Case: guild ids.
    """
    function = None
    name = 'yuuka'
    guild_id_0 = 202410220029
    guild_id_1 = 202410220030
    
    command_base_application_command = InstantiableCommandBaseApplicationCommand(
        function,
        name,
        guild = [guild_id_0, guild_id_1],
    )
    
    output = command_base_application_command._get_permission_sync_ids()
    vampytest.assert_instance(output, set)
    vampytest.assert_eq(output, {guild_id_0, guild_id_1})


def test__CommandBaseApplicationCommand__get_permission_sync_ids__permission_overwrites():
    """
    Tests whether ``CommandBaseApplicationCommand._get_permission_sync_ids`` works as intended.
    
    Case: permission overwrites.
    """
    function = None
    name = 'yuuka'
    guild_id_0 = 202410220031
    guild_id_1 = 202410220032
    
    permission_overwrite_0 = ApplicationCommandPermissionOverwrite(
        (ApplicationCommandPermissionOverwriteTargetType.role, 202410220033),
        True,
    )
    
    permission_overwrite_1 = ApplicationCommandPermissionOverwrite(
        (ApplicationCommandPermissionOverwriteTargetType.role, 202410220034),
        True,
    )
    
    command_base_application_command = InstantiableCommandBaseApplicationCommand(
        function,
        name,
    )
    
    command_base_application_command.add_permission_overwrite(guild_id_0, permission_overwrite_0)
    command_base_application_command.add_permission_overwrite(guild_id_1, permission_overwrite_1)
    output = command_base_application_command._get_permission_sync_ids()
    vampytest.assert_instance(output, set)
    vampytest.assert_eq(output, {guild_id_0, guild_id_1})


def test__CommandBaseApplicationCommand__register_guild_and_application_command_id():
    """
    Tests whether ``CommandBaseApplicationCommand._register_guild_and_application_command_id`` works as intended.
    """
    function = None
    name = 'yuuka'
    guild_id = 202410220035
    application_command_id = 202410220036
    
    command_base_application_command = InstantiableCommandBaseApplicationCommand(
        function,
        name,
        guild = guild_id,
    )
    command_base_application_command._register_guild_and_application_command_id(guild_id, application_command_id)
    
    vampytest.assert_eq(
        command_base_application_command._registered_application_command_ids,
        {
            guild_id: application_command_id
        },
    )


def test__CommandBaseApplicationCommand__unregister_guild_and_application_command_id__nothing():
    """
    Tests whether ``CommandBaseApplicationCommand._unregister_guild_and_application_command_id`` works as intended.
    
    Case: nothing.
    """
    function = None
    name = 'yuuka'
    guild_id = 202410220037
    application_command_id = 202410220038
    
    command_base_application_command = InstantiableCommandBaseApplicationCommand(
        function,
        name,
    )
    command_base_application_command._unregister_guild_and_application_command_id(guild_id, application_command_id)
    
    vampytest.assert_eq(
        command_base_application_command._registered_application_command_ids,
        None,
    )


def test__CommandBaseApplicationCommand__unregister_guild_and_application_command_id__different_guild():
    """
    Tests whether ``CommandBaseApplicationCommand._unregister_guild_and_application_command_id`` works as intended.
    
    Case: different guild.
    """
    function = None
    name = 'yuuka'
    guild_id_0 = 202410220039
    guild_id_1 = 202410220040
    application_command_id = 202410220041
    
    command_base_application_command = InstantiableCommandBaseApplicationCommand(
        function,
        name,
    )
    command_base_application_command._register_guild_and_application_command_id(guild_id_0, application_command_id)
    command_base_application_command._unregister_guild_and_application_command_id(guild_id_1, application_command_id)
    
    vampytest.assert_eq(
        command_base_application_command._registered_application_command_ids,
        {
            guild_id_0: application_command_id,
        },
    )


def test__CommandBaseApplicationCommand__unregister_guild_and_application_command_id__different_command():
    """
    Tests whether ``CommandBaseApplicationCommand._unregister_guild_and_application_command_id`` works as intended.
    
    Case: different command.
    """
    function = None
    name = 'yuuka'
    guild_id = 202410220042
    application_command_id_0 = 202410220043
    application_command_id_1 = 202410220044
    
    command_base_application_command = InstantiableCommandBaseApplicationCommand(
        function,
        name,
    )
    command_base_application_command._register_guild_and_application_command_id(guild_id, application_command_id_0)
    command_base_application_command._unregister_guild_and_application_command_id(guild_id, application_command_id_1)
    
    vampytest.assert_eq(
        command_base_application_command._registered_application_command_ids,
        {
            guild_id: application_command_id_0,
        },
    )


def test__CommandBaseApplicationCommand__unregister_guild_and_application_command_id__hit():
    """
    Tests whether ``CommandBaseApplicationCommand._unregister_guild_and_application_command_id`` works as intended.
    
    Case: hit.
    """
    function = None
    name = 'yuuka'
    guild_id = 202410220045
    application_command_id = 202410220046
    
    command_base_application_command = InstantiableCommandBaseApplicationCommand(
        function,
        name,
    )
    command_base_application_command._register_guild_and_application_command_id(guild_id, application_command_id)
    command_base_application_command._unregister_guild_and_application_command_id(guild_id, application_command_id)
    
    vampytest.assert_eq(
        command_base_application_command._registered_application_command_ids,
        None,
    )


def test__CommandBaseApplicationCommand__pop_application_command_id_for__miss():
    """
    Tests whether ``CommandBaseApplicationCommand._pop_application_command_id_for`` works as intended.
    
    Case: miss.
    """
    function = None
    name = 'yuuka'
    guild_id = 202410220047
    
    command_base_application_command = InstantiableCommandBaseApplicationCommand(
        function,
        name,
    )
    output = command_base_application_command._pop_application_command_id_for(guild_id)
    
    vampytest.assert_eq(
        command_base_application_command._registered_application_command_ids,
        None,
    )
    
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 0)


def test__CommandBaseApplicationCommand__pop_application_command_id_for__hit():
    """
    Tests whether ``CommandBaseApplicationCommand._pop_application_command_id_for`` works as intended.
    
    Case: hit.
    """
    function = None
    name = 'yuuka'
    guild_id = 202410220048
    application_command_id = 202410220049
    
    command_base_application_command = InstantiableCommandBaseApplicationCommand(
        function,
        name,
    )
    
    command_base_application_command._register_guild_and_application_command_id(guild_id, application_command_id)
    output = command_base_application_command._pop_application_command_id_for(guild_id)
    
    vampytest.assert_eq(
        command_base_application_command._registered_application_command_ids,
        None,
    )
    
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, application_command_id)


def test__CommandBaseApplicationCommand__iter_application_command_ids__empty():
    """
    Tests whether ``CommandBaseApplicationCommand._iter_application_command_ids`` works as intended.
    
    Case: empty.
    """
    function = None
    name = 'yuuka'
    
    command_base_application_command = InstantiableCommandBaseApplicationCommand(
        function,
        name,
    )
    
    output = {*command_base_application_command._iter_application_command_ids()}
    
    vampytest.assert_eq(
        command_base_application_command._registered_application_command_ids,
        None,
    )
    
    vampytest.assert_eq(output, set())


def test__CommandBaseApplicationCommand__iter_application_command_ids__populated():
    """
    Tests whether ``CommandBaseApplicationCommand._iter_application_command_ids`` works as intended.
    
    Case: populated.
    """
    function = None
    name = 'yuuka'
    guild_id_0 = 202410220050
    guild_id_1 = 202410220051
    application_command_id_0 = 202410220052
    application_command_id_1 = 202410220053
    
    command_base_application_command = InstantiableCommandBaseApplicationCommand(
        function,
        name,
        guild = [guild_id_0, guild_id_1],
    )
    
    command_base_application_command._register_guild_and_application_command_id(guild_id_0, application_command_id_0)
    command_base_application_command._register_guild_and_application_command_id(guild_id_1, application_command_id_1)
    output = {*command_base_application_command._iter_application_command_ids()}
    
    vampytest.assert_ne(
        command_base_application_command._registered_application_command_ids,
        None,
    )
    
    vampytest.assert_eq(output, {application_command_id_0, application_command_id_1})


def test__CommandBaseApplicationCommand__exhaust_application_command_ids__empty():
    """
    Tests whether ``CommandBaseApplicationCommand._exhaust_application_command_ids`` works as intended.
    
    Case: empty.
    """
    function = None
    name = 'yuuka'
    
    command_base_application_command = InstantiableCommandBaseApplicationCommand(
        function,
        name,
    )
    
    output = {*command_base_application_command._exhaust_application_command_ids()}
    
    vampytest.assert_eq(
        command_base_application_command._registered_application_command_ids,
        None,
    )
    
    vampytest.assert_eq(output, set())


def test__CommandBaseApplicationCommand__exhaust_application_command_ids__populated():
    """
    Tests whether ``CommandBaseApplicationCommand._exhaust_application_command_ids`` works as intended.
    
    Case: populated.
    """
    function = None
    name = 'yuuka'
    guild_id_0 = 202410220054
    guild_id_1 = 202410220055
    application_command_id_0 = 202410220056
    application_command_id_1 = 202410220057
    
    command_base_application_command = InstantiableCommandBaseApplicationCommand(
        function,
        name,
        guild = [guild_id_0, guild_id_1],
    )
    
    command_base_application_command._register_guild_and_application_command_id(guild_id_0, application_command_id_0)
    command_base_application_command._register_guild_and_application_command_id(guild_id_1, application_command_id_1)
    output = {*command_base_application_command._exhaust_application_command_ids()}
    
    vampytest.assert_eq(
        command_base_application_command._registered_application_command_ids,
        None,
    )
    
    vampytest.assert_eq(output, {application_command_id_0, application_command_id_1})


def test__CommandBaseApplicationCommand__iter_sync_ids__global():
    """
    Tests whether ``CommandBaseApplicationCommand._iter_sync_ids`` works as intended.
    
    Case. global.
    """
    function = None
    name = 'yuuka'
    
    command_base_application_command = InstantiableCommandBaseApplicationCommand(
        function,
        name,
        is_global = True,
    )
    
    output = {*command_base_application_command._iter_sync_ids()}
    vampytest.assert_eq(output, {SYNC_ID_GLOBAL})


def test__CommandBaseApplicationCommand__iter_sync_ids__non_global():
    """
    Tests whether ``CommandBaseApplicationCommand._iter_sync_ids`` works as intended.
    
    Case. non-global.
    """
    function = None
    name = 'yuuka'
    
    command_base_application_command = InstantiableCommandBaseApplicationCommand(
        function,
        name,
    )
    
    output = {*command_base_application_command._iter_sync_ids()}
    vampytest.assert_eq(output, {SYNC_ID_NON_GLOBAL})



def test__CommandBaseApplicationCommand__iter_sync_ids__guild_bound():
    """
    Tests whether ``CommandBaseApplicationCommand._iter_sync_ids`` works as intended.
    
    Case. guild bound.
    """
    function = None
    name = 'yuuka'
    guild_id_0 = 202410220058
    guild_id_1 = 202410220058
    
    command_base_application_command = InstantiableCommandBaseApplicationCommand(
        function,
        name,
        guild = [guild_id_0, guild_id_1],
    )
    
    output = {*command_base_application_command._iter_sync_ids()}
    vampytest.assert_eq(output, {guild_id_0, guild_id_1})


def test__CommandBaseApplicationCommand__get_schema():
    """
    Tests whether ``CommandBaseApplicationCommand.get_schema`` works as intended.
    """
    # Note: guild cannot be `None` and is mutually exclusive is `is_global`.
    
    async def function():
        pass
    
    name = 'yuuka'
    delete_on_unload = True
    # guild = None
    integration_context_types = [
        ApplicationCommandIntegrationContextType.guild,
        ApplicationCommandIntegrationContextType.bot_private_channel,
    ]
    integration_types = [
        ApplicationIntegrationType.guild_install,
        ApplicationIntegrationType.user_install,
    ]
    is_global = True
    nsfw = True
    required_permissions = Permission(8)
    
    
    command_base_application_command = InstantiableCommandBaseApplicationCommand(
        function,
        name,
        delete_on_unload = delete_on_unload,
        # guild = guild,
        integration_context_types = integration_context_types,
        integration_types = integration_types,
        is_global = is_global,
        nsfw = nsfw,
        required_permissions = required_permissions,
    )
    
    output = command_base_application_command.get_schema()
    vampytest.assert_instance(output, ApplicationCommand)
    vampytest.assert_eq(command_base_application_command._schema, output)
    vampytest.assert_eq(
        output,
        ApplicationCommand(
            name,
            None,
            integration_context_types = integration_context_types,
            integration_types = integration_types,
            options = None,
            nsfw = nsfw,
            required_permissions = required_permissions,
            target_type = ApplicationCommandTargetType.none,
        )
    )
