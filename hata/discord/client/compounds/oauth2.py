__all__ = ()

from scarletio import Compound, IgnoreCaseMultiValueDictionary
from scarletio.web_common import BasicAuth
from scarletio.web_common.headers import AUTHORIZATION

from ...application import Application, ApplicationRoleConnection
from ...application.application_role_connection.utils import APPLICATION_ROLE_CONNECTION_FIELD_CONVERTERS
from ...bases import maybe_snowflake
from ...guild import create_partial_guild_from_data
from ...http import DiscordHTTPClient
from ...oauth2 import Connection, Oauth2Access, Oauth2Scope, Oauth2User
from ...oauth2.oauth2_access.fields import (
    put_scopes_into as put_oauth2_scopes_into, validate_scopes as validate_oauth2_scopes
)
from ...payload_building import build_edit_payload
from ...role import Role

from ..request_helpers import get_guild_id, get_oauth2_access_token, get_oauth2_access_token_and_user_id
from ..utils import UserGuildPermission

from .application_command import _assert__application_id


def _assert__redirect_url(redirect_url):
    """
    Asserts whether the `redirect_url`'s type is correct.
    
    Parameters
    ----------
    redirect_url : `str`
        The url, where the activation page redirected to.
    
    Raises
    ------
    AssertionError
        - If `redirect_url` is not `str`.
    """
    if not isinstance(redirect_url, str):
        raise AssertionError(
            f'`redirect_url` can be `str`, got {redirect_url.__class__.__name__}; {redirect_url!r}.'
        )
    
    return True


def _assert__code(code):
    """
    Asserts whether the `code`'s type is correct.
    
    Parameters
    ----------
    code : `str`
        The code, what is included with the redirect url after a successful activation.
    
    Raises
    ------
    AssertionError
        - If `code` is not `str`.
    """
    if not isinstance(code, str):
        raise AssertionError(
            f'`code` can be `str`, got {code.__class__.__name__}; {code!r}.'
        )
    
    return True


class ClientCompoundOauth2Endpoints(Compound):
    
    application : Application
    http : DiscordHTTPClient
    id : int
    secret : str
    
    
    async def activate_authorization_code(self, redirect_url, code, scopes):
        """
        Activates a user's oauth2 code.
        
        This method is a coroutine.
        
        Parameters
        ----------
        redirect_url : `str`
            The url, where the activation page redirected to.
        code : `str`
            The code, what is included with the redirect url after a successful activation.
        scopes : `str`, `list` of `str`
            Scope or a  list of oauth2 scopes to request.
        
        Returns
        -------
        access : ``Oauth2Access``, `None`
            If the code, the redirect url or the scopes are invalid, the methods returns `None`.
        
        Raises
        ------
        TypeError
            If `Scopes` wasn't neither as `str` not `list` of `str`s.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        See Also
        --------
        ``parse_oauth2_redirect_url`` : Parses `redirect_url` and the `code` from a full url.
        """
        assert _assert__redirect_url(redirect_url)
        assert _assert__code(code)
        
        scopes = validate_oauth2_scopes(scopes)
                
        data = {
            'client_id': self.id,
            'client_secret': self.secret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_url,
        }
        
        put_oauth2_scopes_into(scopes, data, True)
        
        
        data = await self.http.oauth2_token(data, IgnoreCaseMultiValueDictionary())
        if len(data) == 1:
            return
        
        return Oauth2Access.from_data(data, redirect_url)
    
    
    async def owners_access(self, scopes):
        """
        Similar to ``.activate_authorization_code``, but it requests the application's owner's access. It does not
        requires the redirect_url and the code parameter either.
        
        This method is a coroutine.
        
        Parameters
        ----------
        scopes : `list` of `str`
            A list of oauth2 scopes to request.
        
        Returns
        -------
        access : ``Oauth2Access``
            The oauth2 access of the client's application's owner.
        
        Raises
        ------
        TypeError
            If `Scopes` is neither `str` nor `list` of `str`s.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `redirect_url` was not given as `str`.
            - If `code` was not given as `str`.
            - If `scopes` is empty.
            - If `scopes` contains empty string.
        
        Notes
        -----
        Does not work if the client's application is owned by a team.
        """
        scopes = validate_oauth2_scopes(scopes)
        
        data = {
            'grant_type': 'client_credentials',
        }
        
        put_oauth2_scopes_into(scopes, data, True)
        
        headers = IgnoreCaseMultiValueDictionary()
        headers[AUTHORIZATION] = BasicAuth(str(self.id), self.secret).encode()
        data = await self.http.oauth2_token(data, headers)
        return Oauth2Access.from_data(data, '')
    
    
    async def user_info_get(self, access):
        """
        Request the a user's information with oauth2 access token. By default a bot account should be able to request
        every public information about a user (but you do not need oauth2 for that). If the access token has email
        or/and identify scopes, then more information should show up like this.
        
        This method is a coroutine.
        
        Parameters
        ----------
        access : ``Oauth2Access``, ``Oauth2User``, `str`
            Oauth2 access to the respective user or it's access token.
        
        Returns
        -------
        oauth2_user : ``Oauth2User``
            The requested user object.
        
        Raises
        ------
        TypeError
            - If `access` is not ``Oauth2Access``, ``Oauth2User``, `str`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        Needs `'email'` or / and `'identify'` scopes granted for more data
        """
        access_token = get_oauth2_access_token(access)
        
        headers = IgnoreCaseMultiValueDictionary()
        headers[AUTHORIZATION] = f'Bearer {access_token}'
        data = await self.http.user_info_get(headers)
        return Oauth2User.from_data(data, access)
        
    
    async def user_connection_get_all(self, access):
        """
        Requests a user's connections. This method will work only if the access token has the `'connections'` scope. At
        the returned list includes the user's hidden connections as well.
        
        This method is a coroutine.
        
        Parameters
        ----------
        access : ``Oauth2Access``, ``Oauth2User``, `str`
            Oauth2 access to the respective user or it's access token.
        
        Returns
        -------
        connections : `list` of ``Connection``
            The user's connections.
        
        Raises
        ------
        TypeError
            - If `access` is not ``Oauth2Access``, ``Oauth2User``, `str`.
        ValueError
            - If the given `access` is not providing the required scope.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        access_token = get_oauth2_access_token(access, Oauth2Scope.connections)
        
        headers = IgnoreCaseMultiValueDictionary()
        headers[AUTHORIZATION] = f'Bearer {access_token}'
        data = await self.http.user_connection_get_all(headers)
        return [Connection.from_data(connection_data) for connection_data in data]
    
    
    async def renew_access_token(self, access):
        """
        Renews the access token of an ``Oauth2Access``.
        
        This method is a coroutine.
        
        Parameters
        ----------
        access : ``Oauth2Access``, ``Oauth2User``
            Oauth2 access to the respective user.
        
        Raises
        ------
        TypeError
            - If `access` is not ``Oauth2Access``, ``Oauth2User``.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        By default access tokens expire after one week.
        """
        if not isinstance(access, (Oauth2Access, Oauth2User)):
            raise TypeError(
                f'`access` can be `{Oauth2Access.__name__}`, `{Oauth2User.__name__}`'
                f', got {access.__class__.__name__}; {access!r}.'
            )
        
        redirect_url = access.redirect_url
        if redirect_url:
            data = {
                'client_id': self.id,
                'client_secret': self.secret,
                'grant_type': 'refresh_token',
                'refresh_token': access.refresh_token,
                'redirect_uri': redirect_url,
            }
        else:
            data = {
                'client_id': self.id,
                'client_secret': self.secret,
                'grant_type': 'client_credentials',
            }
        
        put_oauth2_scopes_into(access.scopes, data, True)
        
        data = await self.http.oauth2_token(data, IgnoreCaseMultiValueDictionary())
        
        access._renew(data)
    
    
    async def guild_user_add(self, guild, access, user = None, *, nick=None, roles=None, mute=False, deaf=False):
        """
        Adds the passed to the guild. The user must have granted you the `'guilds.join'` oauth2 scope.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, where the user is going to be added.
        
        access: ``Oauth2Access``, ``Oauth2User``, `str`
            The access of the user, who will be added.
        
        user : `None`, ```ClientUserBase`` = `None`, `int`, Optional
            Defines which user will be added to the guild. The `access` must refer to this specified user.
            
            This field is optional if access is passed as an ``Oauth2User`` object.
        
        nick : `None`, `str` = `None`, Optional (Keyword only)
            The nickname, which with the user will be added.
        
        roles : `None`, `list` of (``Role``, `int`) = `None`, Optional (Keyword only)
            The roles to add the user with.
        
        mute : `bool` = `False`, Optional (Keyword only)
            Whether the user should be added as muted.
        
        deaf : `bool` = `False`, Optional (Keyword only)
            Whether the user should be added as deafen.
        
        Raises
        ------
        TypeError:
            - If `user` was not given neither as `None`, ``ClientUserBase``, `int`.
            - If `user` was passed as `None` and `access` was passed as ``Oauth2Access``, `str`.
            - If `access` was not given as ``Oauth2Access``, ``Oauth2User``, nether as `str`.
            - If the given `access` not grants `'guilds.join'` scope.
            - If `guild` was not given neither as ``Guild``, not `int`.
            - If `roles` contain not ``Role``, nor `int`.
        ValueError
            - If the given `access` is not providing the required scope.
            - If `user` and `access` refers to a different user.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        access_token, user_id = get_oauth2_access_token_and_user_id(access, user, Oauth2Scope.guilds_join)
        guild_id = get_guild_id(guild)
        
        
        data = {'access_token': access_token}
        
        
        # Security debug checks.
        if __debug__:
            if (nick is not None):
                if not isinstance(nick, str):
                    raise AssertionError(
                        f'`nick` can be `None`, `str`, got {nick.__class__.__name__}; {nick!r}.'
                    )
                
                nick_length = len(nick)
                if nick_length > 32:
                    raise AssertionError(
                        f'`nick` length can be in range [0:32], got {nick_length}; {nick!r}.'
                    )
        
        if (nick is not None) and nick:
            data['nick'] = nick
        
        
        if (roles is not None):
            if __debug__:
                if not isinstance(roles, list):
                    raise AssertionError(
                        f'`roles` can be `list` of (`{Role.__name__}`, `int`), got '
                        f'{roles.__class__.__name__}; {roles!r}.'
                    )
            
            if roles:
                role_ids = set()
                
                for index, role in enumerate(roles):
                    if isinstance(role, Role):
                        role_id = role.id
                    else:
                        role_id = maybe_snowflake(role)
                        if role_id is None:
                            raise TypeError(
                                f'`roles[{index}]` is neither `{Role.__name__}`, `int`, got '
                                f'{role.__class__.__name__}; {role!r}; roles={roles!r}.'
                            )
                    
                    role_ids.add(role_id)
                
                data['roles'] = role_ids
        
        
        if __debug__:
            if not isinstance(mute, bool):
                raise AssertionError(
                    f'`mute` can be `bool`, got {mute.__class__.__name__}; {mute!r}.'
                )
        
        if mute:
            data['mute'] = mute
        
        
        if __debug__:
            if not isinstance(deaf, bool):
                raise AssertionError(
                    f'`deaf` can be `bool`, got {deaf.__class__.__name__}; {deaf!r}.'
                )
        
        if deaf:
            data['deaf'] = deaf
        
        
        await self.http.guild_user_add(guild_id, user_id, data)
    
    
    async def user_guild_get_all(self, access):
        """
        Requests a user's guilds with it's ``Oauth2Access``.
        The user must provide the `Oauth2Scope.guilds` scope for this request to succeed.
        
        This method is a coroutine.
        
        Parameters
        ----------
        access: ``Oauth2Access``, ``Oauth2User``, `str`
            The access of the user, who's guilds will be requested.
        
        Returns
        -------
        guilds_and_permissions : `list` of `tuple` (``Guild``, ``UserGuildPermission``)
            The guilds and the user's permissions in each of them. Not loaded guilds will show up as partial ones.
        
        Raises
        ------
        TypeError
            - If `access` is not ``Oauth2Access``, ``Oauth2User``, `str`.
        ValueError
            - If the given `access` is not providing the required scope.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        access_token = get_oauth2_access_token(access, Oauth2Scope.guilds)
        
        headers = IgnoreCaseMultiValueDictionary()
        headers[AUTHORIZATION] = f'Bearer {access_token}'
        data = await self.http.user_guild_get_all(headers)
        return [(create_partial_guild_from_data(guild_data), UserGuildPermission(guild_data)) for guild_data in data]
    
    
    async def user_application_role_connection_get(self, access):
        """
        Requests a user's application role connections with it's ``Oauth2Access``.
        The user must provide the `Oauth2Scope.role_connections_write` scope for this request to succeed.
                
        This method is a coroutine.
        
        Parameters
        ----------
        access: ``Oauth2Access``, ``Oauth2User``, `str`
            The access of the user, who will's application role connections will be requested..
        
        Returns
        -------
        application_role_connection : ``ApplicationRoleConnection``
        
        Raises
        ------
        TypeError
            - If `access` is not ``Oauth2Access``, ``Oauth2User``, `str`.
        ValueError
            - If the given `access` is not providing the required scope.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        application_id = self.application.id
        assert _assert__application_id(application_id)
        access_token = get_oauth2_access_token(access, Oauth2Scope.role_connections_write)
        
        headers = IgnoreCaseMultiValueDictionary()
        headers[AUTHORIZATION] = f'Bearer {access_token}'
        data = await self.http.user_application_role_connection_get(application_id, headers)
        return ApplicationRoleConnection.from_data(data)
    
    
    async def user_application_role_connection_edit(
        self, access, application_role_connection_template = None, **keyword_parameters
    ):
        """
        Edits a user's application role connections with it's ``Oauth2Access``.
        The user must provide the `Oauth2Scope.role_connections_write` scope for this request to succeed.
                
        This method is a coroutine.
        
        Parameters
        ----------
        access: ``Oauth2Access``, ``Oauth2User``, `str`
            The access of the user, who will's application role connections will be requested..
        
        application_role_connection_template : `None`, ``ApplicationRoleConnection`` = `None`, Optional
            Application role connection to use as a template.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters either to define the template, or to overwrite specific fields' values.
        
        Other Parameters
        ----------------
        platform_name : `None`, `str`, Optional (Keyword only)
            The vanity name of the platform the application represents.
        platform_user_name : `None`, `str`, Optional (Keyword only)
            The name of the user on the application's platform.
        metadata_values : `None`, `dict` of (`str`, `str`) items, Optional (Keyword only)
            Metadata key to attached value relation.
        
        Returns
        -------
        application_role_connection : ``ApplicationRoleConnection``
        
        Raises
        ------
        TypeError
            - If `access` is not ``Oauth2Access``, ``Oauth2User``, `str`.
        ValueError
            - If the given `access` is not providing the required scope.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        application_id = self.application.id
        assert _assert__application_id(application_id)
        access_token = get_oauth2_access_token(access, Oauth2Scope.role_connections_write)
        
        data = build_edit_payload(
            None,
            application_role_connection_template,
            APPLICATION_ROLE_CONNECTION_FIELD_CONVERTERS,
            keyword_parameters,
        )
        
        headers = IgnoreCaseMultiValueDictionary()
        headers[AUTHORIZATION] = f'Bearer {access_token}'
        data = await self.http.user_application_role_connection_edit(application_id, data, headers)
        return ApplicationRoleConnection.from_data(data)
