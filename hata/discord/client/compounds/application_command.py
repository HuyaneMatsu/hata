__all__ = ()

from scarletio import Compound, IgnoreCaseMultiValueDictionary
from scarletio.web_common.headers import AUTHORIZATION

from ...application import Application
from ...application_command import (
    ApplicationCommand, ApplicationCommandPermission, ApplicationCommandPermissionOverwrite,
    ApplicationCommandPermissionOverwriteTargetType
)
from ...application_command.application_command.constants import (
    APPLICATION_COMMAND_LIMIT_GLOBAL, APPLICATION_COMMAND_LIMIT_GUILD
)
from ...application_command.application_command_permission.constants import APPLICATION_COMMAND_PERMISSION_OVERWRITE_MAX
from ...http import DiscordHTTPClient
from ...oauth2 import Oauth2Access, Oauth2Scope, Oauth2User

from ..request_helpers import (
    get_application_command_and_id, get_application_command_id, get_application_command_id_nullable, get_guild_id
)


def _assert__application_id(application_id):
    """
    Asserts the the client's has `.application` synced by asserting whether it's value is not `0`.
    
    Parameters
    ----------
    application_id : `int`
        The client's application id.
    
    Raises
    ------
    AssertionError
        - If the client's application is not yet synced.
    """
    if application_id == 0:
        raise AssertionError(
            'The client\'s application is not yet synced.'
        )
    
    return True


def _assert__application_command(application_command):
    """
    Asserts whether the given ``application_command`` is indeed ``ApplicationCommand`` instance.
    
    Parameters
    ----------
    application_command : ``ApplicationCommand``
        The application command to checkout.
    
    Raises
    ------
    AssertionError
        - If `application_command` was not given as ``ApplicationCommand``.
    """
    if not isinstance(application_command, ApplicationCommand):
        raise AssertionError(
            f'`application_command` can be `{ApplicationCommand.__name__}`, got '
            f'{application_command.__class__.__name__}; {application_command!r}.'
        )
    
    return True


def _assert__new_application_command(new_application_command):
    """
    Asserts whether the given ``new_application_command`` is indeed ``ApplicationCommand`` instance.
    
    Parameters
    ----------
    new_application_command : ``ApplicationCommand``
        The application command to checkout.
    
    Raises
    ------
    AssertionError
        - If `new_application_command` was not given as ``ApplicationCommand``.
    """
    if not isinstance(new_application_command, ApplicationCommand):
        raise AssertionError(
            f'`new_application_command` can be `{ApplicationCommand.__name__}`, got '
            f'{new_application_command.__class__.__name__}; {new_application_command!r}.'
        )
    
    return True


def _assert__application_command_permission_edit__access_scope(access):
    """
    Asserts whether ``Client.application_command_permission_edit``'s `access` parameter has the required scopes.
    
    This function is only called when `access` is either ``Oauth2Access`` or ``Oauth2User`` instance.
    
    Parameters
    ----------
    access : ``Oauth2Access``, ``Oauth2User``
        A user's access token.
    
    Raises
    ------
    AssertionError
        - If the `access` lacks `applications.commands.permissions.update` scope.
    """
    if not access.has_scope(Oauth2Scope.applications_commands_permissions_update):
        raise AssertionError(
            f'The given `access` not grants `\'applications.commands.permissions.update\'` scope, '
            f'what is required, got {access!r}.'
        )
    
    return True


class ClientCompoundApplicationCommandEndpoints(Compound):
    
    application: Application
    http : DiscordHTTPClient
    
    async def application_command_global_get(self, application_command):
        """
        Requests the given global application command.
        
        Parameters
        ----------
        application_command : ``ApplicationCommand``, `int`
            The application command, or it's id to request.
        
        Returns
        -------
        application_commands : ``ApplicationCommand``
            The received application command.
        
        Raises
        ------
        TypeError
            If `application_command` was not given neither as ``ApplicationCommand`` not as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        application_id = self.application.id
        assert _assert__application_id(application_id)
        
        application_command, application_command_id = get_application_command_and_id(application_command)
        
        application_command_data = await self.http.application_command_global_get(
            application_id,
            application_command_id,
            {'with_localizations': True},
        )
        
        if application_command is None:
            application_command = ApplicationCommand.from_data(application_command_data)
        else:
            application_command._update_attributes(application_command_data)
        
        return application_command
    
    
    async def application_command_global_get_all(self):
        """
        Requests the client's global application commands.
        
        This method is a coroutine.
        
        Returns
        -------
        application_commands : `list` of ``ApplicationCommand``
            The received application commands.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        application_id = self.application.id
        assert _assert__application_id(application_id)
        
        data = await self.http.application_command_global_get_all(
            application_id,
            {'with_localizations': True},
        )
        
        return [ApplicationCommand.from_data(application_command_data) for application_command_data in data]
    
    
    async def application_command_global_create(self, application_command):
        """
        Creates a new global application command.
        
        > If there is an application command with the given name, will overwrite that instead.
        >
        > Each day only maximum only 200 global application command can be created.
        
        This method is a coroutine.
        
        Parameters
        ----------
        application_command : ``ApplicationCommand``
            The application command to create.
        
        Returns
        -------
        application_command : ``ApplicationCommand``
            The created application command.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        The command will be available in all guilds after 1 hour.
        """
        application_id = self.application.id
        assert _assert__application_id(application_id)
        assert _assert__application_command(application_command)
        
        data = application_command.to_data()
        data = await self.http.application_command_global_create(application_id, data)
        return ApplicationCommand.from_data(data)
    
    
    async def application_command_global_edit(self, old_application_command, new_application_command):
        """
        Edits a global application command.
        
        This method is a coroutine.
        
        Parameters
        ----------
        old_application_command : ``ApplicationCommand``, `int`
            The application command to edit. Can be given as the application command's id as well.
        new_application_command : ``ApplicationCommand``
            The application command to edit to.
        
        Returns
        -------
        application_command : ``ApplicationCommand``
            The edited application command.
        
        Raises
        ------
        TypeError
            If `old_application_command` was not given neither as ``ApplicationCommand`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        The updates will be available in all guilds after 1 hour.
        """
        old_application_command, application_command_id = get_application_command_and_id(old_application_command)
        
        application_id = self.application.id
        assert _assert__application_id(application_id)
        
        assert _assert__new_application_command(new_application_command)
        
        data = new_application_command.to_data()
        
        # Handle https://github.com/discord/discord-api-docs/issues/2525
        if (old_application_command is not None) and (old_application_command.name == data['name']):
            del data['name']
        
        await self.http.application_command_global_edit(application_id, application_command_id, data)
        return ApplicationCommand._from_edit_data(data, application_command_id, application_id)
    
    
    async def application_command_global_delete(self, application_command):
        """
        Deletes the given application command.
        
        Parameters
        ----------
        application_command : ``ApplicationCommand``, `int`
            The application command delete edit. Can be given as the application command's id as well.
        
        Raises
        ------
        TypeError
            If `application_command` was not given neither as ``ApplicationCommand`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        application_id = self.application.id
        assert _assert__application_id(application_id)
        
        application_command_id = get_application_command_id(application_command)
        
        await self.http.application_command_global_delete(application_id, application_command_id)
    
    
    async def application_command_global_update_multiple(self, application_commands):
        """
        Takes an iterable of application commands, and updates the actual global ones.
        
        If a command exists with the given name, edits it, if not, will creates a new one.
        
        > The created application commands count to the daily limit.
        
        This method is a coroutine.
        
        Parameters
        ----------
        application_commands : `iterable` of ``ApplicationCommand``
            The application commands to update the existing ones with.
        
        Returns
        -------
        application_commands : `list` of ``ApplicationCommand``
            The edited and created application commands.
        
        Raises
        ------
        TypeError
            - If `application_commands` is not iterable.
            - If an element of `application_commands` is not ``ApplicationCommand`` instance.
        ValueError
            - If more than `100` ``ApplicationCommand`` is given.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        The commands will be available in all guilds after 1 hour.
        """
        application_id = self.application.id
        assert _assert__application_id(application_id)
        
        
        if getattr(application_commands, '__iter__', None) is None:
            raise TypeError(
                f'`application_commands` can be an `iterable`, got '
                f'{application_commands.__class__.__name__}; {application_commands!r}.'
            )
        
        application_command_datas = []
        
        for application_command in application_commands:
            if not isinstance(application_command, ApplicationCommand):
                raise TypeError(
                    f'`application_commands` contains a not `{ApplicationCommand.__name__}` element, got: '
                    f'{application_command.__class__.__name__}; {application_command!r}; '
                    f'application_commands={application_commands!r}.'
                )
            
            application_command_datas.append(application_command.to_data())
        
        
        application_command_count = len(application_command_datas)
        # If we have no application commands to edit return~
        if application_command_count == 0:
            return []
        
        if application_command_count >= APPLICATION_COMMAND_LIMIT_GLOBAL:
            raise ValueError(
                f'Maximum {APPLICATION_COMMAND_LIMIT_GLOBAL} application command can be given, got '
                f'{application_command_count!r}; {application_commands!r}.'
            )
        
        application_command_datas = await self.http.application_command_global_update_multiple(
            application_id, application_command_datas
        )
        
        return [
            ApplicationCommand.from_data(application_command_data)
            for application_command_data in application_command_datas
        ]
    
    
    async def application_command_guild_get(self, guild, application_command):
        """
        Requests the given guild application command.
        
        Parameters
        ----------
        application_command : ``ApplicationCommand``, `int`
            The application command, or it's id to request.
        
        Returns
        -------
        application_commands : ``ApplicationCommand``
            The received application command.
        
        Raises
        ------
        TypeError
            - If `guild` was not given neither as``Guild`` nor `int`.
            - If `application_command` was not given neither as ``ApplicationCommand`` not as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        application_id = self.application.id
        assert _assert__application_id(application_id)
        
        guild_id = get_guild_id(guild)
        
        application_command, application_command_id = get_application_command_and_id(application_command)
        
        application_command_data = await self.http.application_command_guild_get(
            application_id,
            guild_id,
            application_command_id,
            {'with_localizations': True},
        )
        
        if application_command is None:
            application_command = ApplicationCommand.from_data(application_command_data)
        else:
            application_command._update_attributes(application_command_data)
        
        return application_command
    
    
    async def application_command_guild_get_all(self, guild):
        """
        Requests the client's global application commands.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, which application commands will be requested.
        
        Returns
        -------
        application_commands : `list` of ``ApplicationCommand``
            The received application commands.
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as``Guild`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        application_id = self.application.id
        assert _assert__application_id(application_id)
        
        guild_id = get_guild_id(guild)
        
        data = await self.http.application_command_guild_get_all(
            application_id,
            guild_id,
            {'with_localizations': True},
        )
        
        return [ApplicationCommand.from_data(application_command_data) for application_command_data in data]
    
    
    async def application_command_guild_create(self, guild, application_command):
        """
        Creates a new guild application command.
        
        > If there is an application command with the given name, will overwrite that instead.
        >
        > Each day only maximum only 200 guild application command can be created at each guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, where application commands will be created.
        application_command : ``ApplicationCommand``
            The application command to create.
        
        Returns
        -------
        application_command : ``ApplicationCommand``
            The created application command.
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as``Guild`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        application_id = self.application.id
        assert _assert__application_id(application_id)
        assert _assert__application_command(application_command)
        
        guild_id = get_guild_id(guild)
        
        data = application_command.to_data()
        data = await self.http.application_command_guild_create(application_id, guild_id, data)
        return ApplicationCommand.from_data(data)
    
    
    async def application_command_guild_edit(self, guild, old_application_command, new_application_command):
        """
        Edits a guild application command.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, to what the application command is bound to.
        old_application_command : ``ApplicationCommand``, `int`
            The application command to edit. Can be given as the application command's id as well.
        new_application_command : ``ApplicationCommand``
            The application command to edit to.
        
        Raises
        ------
        TypeError
            - If `guild` was not given neither as``Guild`` nor `int`.
            - If `old_application_command` was not given neither as ``ApplicationCommand`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        old_application_command, application_command_id = get_application_command_and_id(old_application_command)
        
        application_id = self.application.id
        assert _assert__application_id(application_id)
        
        assert _assert__new_application_command(new_application_command)
        
        guild_id = get_guild_id(guild)
        data = new_application_command.to_data()
        
        # Handle https://github.com/discord/discord-api-docs/issues/2525
        if (old_application_command is not None) and (old_application_command.name == data['name']):
            del data['name']
        
        await self.http.application_command_guild_edit(application_id, guild_id, application_command_id, data)
    
    
    async def application_command_guild_delete(self, guild, application_command):
        """
        Deletes the given application command.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, to what the application command is bound to.
        application_command : ``ApplicationCommand``, `int`
            The application command delete edit. Can be given as the application command's id as well.
        
        Raises
        ------
        TypeError
            - If `guild` was not given neither as``Guild`` nor `int`.
            - If `application_command` was not given neither as ``ApplicationCommand`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        application_id = self.application.id
        assert _assert__application_id(application_id)
        
        guild_id = get_guild_id(guild)
        
        application_command_id = get_application_command_id(application_command)
        
        await self.http.application_command_guild_delete(application_id, guild_id, application_command_id)
    
    
    async def application_command_guild_update_multiple(self, guild, application_commands):
        """
        Takes an iterable of application commands, and updates the guild's actual ones.
        
        If a command exists with the given name, edits it, if not, will creates a new one.
        
        > The created application commands count to the daily limit.
        
        This method is a coroutine.
        
        Parameters
        ----------
        application_commands : `iterable` of ``ApplicationCommand``
            The application commands to update the existing ones with.
        
        Returns
        -------
        application_commands : `list` of ``ApplicationCommand``
            The edited and created application commands.
        
        Raises
        ------
        TypeError
            - If `guild` was not given neither as``Guild`` nor `int`.
            - If `application_commands` is not iterable.
            - If an element of `application_commands` is not ``ApplicationCommand`` instance.
        ValueError
            - If more than `100` ``ApplicationCommand`` is given.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        application_id = self.application.id
        assert _assert__application_id(application_id)
        
        guild_id = get_guild_id(guild)
        
        
        iterator = getattr(type(application_commands), '__iter__', None)
        if iterator is None:
            raise TypeError(
                f'`application_commands` can be an `iterable`, got '
                f'{application_commands.__class__.__name__}; {application_commands!r}.'
            )
        
        
        application_command_datas = []
        
        for application_command in iterator(application_commands):
            if not isinstance(application_command, ApplicationCommand):
                raise TypeError(
                    f'`application_commands` contains a not `{ApplicationCommand.__name__}` element, got: '
                    f'{application_command.__class__.__name__}; {application_command!r}; '
                    f'application_commands={application_commands!r}.'
                )
            
            application_command_datas.append(application_command.to_data())
        
        
        application_command_count = len(application_command_datas)
        # If we have no application commands to edit return~
        if application_command_count == 0:
            return []
        
        if application_command_count >= APPLICATION_COMMAND_LIMIT_GUILD:
            raise ValueError(
                f'Maximum {APPLICATION_COMMAND_LIMIT_GUILD} application command can be given, got '
                f'{application_command_count!r}; {application_commands!r}.'
            )
        
        application_command_datas = await self.http.application_command_guild_update_multiple(
            application_id, guild_id, application_command_datas
        )
        
        return [
            ApplicationCommand.from_data(application_command_data)
            for application_command_data in application_command_datas
        ]
    
    
    async def application_command_permission_get(self, guild, application_command):
        """
        Returns the permissions set for the given `application_command` in the given `guild`.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The respective guild.
        application_command : ``ApplicationCommand``, `int`
            The respective application command.
        
        Returns
        -------
        permission : ``ApplicationCommandPermission``
            The requested permissions.
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as``Guild`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        Íf the application command has no permission overwrites in the guild, Discord will drop the following error:
        
        ```py
        DiscordException Not Found (404), code=10066: Unknown application command permissions
        ```
        """
        application_id = self.application.id
        assert _assert__application_id(application_id)
        
        guild_id = get_guild_id(guild)
        
        application_command_id = get_application_command_id(application_command)
        
        permission_data = await self.http.application_command_permission_get(
            application_id, guild_id, application_command_id
        )
        
        return ApplicationCommandPermission.from_data(permission_data)
    
    
    async def application_command_permission_edit(self, access, guild, application_command, permission_overwrites):
        """
        Edits the permissions of the given `application_command` in the given `guild`.
        
        > The new permissions will overwrite the existing permission of an application command.
        >
        > A command will lose it's permissions on rename.
        
        The endpoint requires oauth access with `applications.commands.permissions.update` scope.
        
        The user with the scope must have in the guild:
        
        - Permission to manage guild and roles.
        - Ability to invoke the respective command.
        - Permission to manage the resources that will be affected. The can be roles, users and channels depending on
            the permission types.
        
        This method is a coroutine.
        
        Parameters
        ----------
        access : ``Oauth2Access``, ``Oauth2User``, `str`
            A user's access token to use.
        
        guild : ``Guild``, `int`
            The respective guild.
        
        application_command : `None`, ``ApplicationCommand``, `int`
            The respective application command.
            
            Can be `None` (or `0`) if you want to edit the default overwrites for all guild level application commands.
            
        permission_overwrites : `None`, (`tuple`, `list` , `set`) of ``ApplicationCommandPermissionOverwrite``
            The new permission overwrites of the given application command inside of the guild.
            
            Give it as `None` to remove all existing one.
        
        Returns
        -------
        permissions : ``ApplicationCommandPermission``
            The application command's new permissions.
        
        Raises
        ------
        TypeError
            - If `guild` was not given neither as``Guild`` nor `int`.
            - If `permission_overwrites` was not given as `None`, `tuple`, `list`, `set`.
            - If `permission_overwrites` contains a non ``ApplicationCommandPermissionOverwrite`` element.
        ValueError
            - If `permission_overwrites` contains more than 100 elements.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        # application_id
        application_id = self.application.id
        assert _assert__application_id(application_id)
        
        # access_token
        if isinstance(access, (Oauth2Access, Oauth2User)):
            assert _assert__application_command_permission_edit__access_scope(access)
            access_token = access.access_token
        
        elif isinstance(access, str):
            access_token = access
        
        else:
            raise TypeError(
                f'`access` can be `{Oauth2Access.__name__}`, `{Oauth2User.__name__}` `str`'
                f', got {access.__class__.__name__}; {access!r}.'
            )
        
        
        guild_id = get_guild_id(guild)
        
        application_command_id = get_application_command_id_nullable(application_command)
        if application_command_id == 0:
            application_command_id = application_id
        
        permission_overwrite_datas = []
        if (permission_overwrites is not None):
            if getattr(permission_overwrites, '__iter__', None) is None:
                raise TypeError(
                    f'`permission_overwrites` can be `None`, `list`, `tuple` or '
                    f'`set`, got {permission_overwrites.__class__.__name__}; {permission_overwrites!r}.'
                )
            
            for permission_overwrite in permission_overwrites:
                if not isinstance(permission_overwrite, ApplicationCommandPermissionOverwrite):
                    raise TypeError(
                        f'`permission_overwrites` can contain `{ApplicationCommandPermissionOverwrite.__name__}` '
                        f'elements, got {permission_overwrite.__class__.__name__}; {permission_overwrite!r}; '
                        f'permission_overwrites={permission_overwrites!r}.'
                    )
                
                # We update channel permission overwrites with id of 0
                if permission_overwrite.target_type is ApplicationCommandPermissionOverwriteTargetType.channel:
                    permission_overwrite = permission_overwrite.copy_with(target = ('channel', guild_id - 1))
                
                elif permission_overwrite.target_type is ApplicationCommandPermissionOverwriteTargetType.role:
                    permission_overwrite = permission_overwrite.copy_with(target = ('role', guild_id))
                
                permission_overwrite_datas.append(permission_overwrite.to_data())
        
        
        permission_overwrite_datas_length = len(permission_overwrite_datas)
        if permission_overwrite_datas_length > APPLICATION_COMMAND_PERMISSION_OVERWRITE_MAX:
            raise ValueError(
                f'`permission_overwrites` can contain up to `{APPLICATION_COMMAND_PERMISSION_OVERWRITE_MAX}` '
                f'permission_overwrites, got {permission_overwrite_datas_length!r}; '
                f'{permission_overwrites!r}.'
            )
        
        data = {'permissions': permission_overwrite_datas}
        
        headers = IgnoreCaseMultiValueDictionary()
        headers[AUTHORIZATION] = f'Bearer {access_token}'
        
        permission_data = await self.http.application_command_permission_edit(
            application_id, guild_id, application_command_id, data, headers
        )
        
        return ApplicationCommandPermission.from_data(permission_data)
    
    
    async def application_command_permission_get_all_guild(self, guild):
        """
        Returns the permissions set for application commands in the given `guild`.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild to request application command permissions from.
        
        Returns
        -------
        permission : `list` of ``ApplicationCommandPermission``
            The requested permissions for all the application commands in the guild.
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as``Guild`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        application_id = self.application.id
        assert _assert__application_id(application_id)
        
        guild_id = get_guild_id(guild)
        
        permission_datas = await self.http.application_command_permission_get_all_guild(application_id, guild_id)
        
        return [ApplicationCommandPermission.from_data(permission_data) for permission_data in permission_datas]
