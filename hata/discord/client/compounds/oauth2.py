__all__ = ()

from scarletio import Compound, IgnoreCaseMultiValueDictionary
from scarletio.web_common import BasicAuth
from scarletio.web_common.headers import AUTHORIZATION

from ...bases import maybe_snowflake
from ...guild import create_partial_guild_from_data
from ...http import DiscordHTTPClient
from ...oauth2 import Connection, Oauth2Access, Oauth2Scope, Oauth2User
from ...oauth2.helpers import build_joined_scopes, join_oauth2_scopes
from ...role import Role

from ..request_helpers import get_guild_id, get_user_id_nullable
from ..utils import UserGuildPermission


class ClientCompoundOauth2Endpoints(Compound):
    
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
        AssertionError
            - If `redirect_url` was not given as `str`.
            - If `code` was not given as `str`.
        
        See Also
        --------
        ``parse_oauth2_redirect_url`` : Parses `redirect_url` and the `code` from a full url.
        """
        if __debug__:
            if not isinstance(redirect_url, str):
                raise AssertionError(
                    f'`redirect_url` can be `str`, got {redirect_url.__class__.__name__}; {redirect_url!r}.'
                )
            
            if not isinstance(code, str):
                raise AssertionError(
                    f'`code` can be `str`, got {code.__class__.__name__}; {code!r}.'
                )
        
        joined_scopes = build_joined_scopes(scopes)
        
        data = {
            'client_id': self.id,
            'client_secret': self.secret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_url,
            'scope': joined_scopes,
        }
        
        data = await self.http.oauth2_token(data, IgnoreCaseMultiValueDictionary())
        if len(data) == 1:
            return
        
        return Oauth2Access(data, redirect_url)
    
    
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
        joined_scopes = build_joined_scopes(scopes)
        
        data = {
            'grant_type': 'client_credentials',
            'scope': joined_scopes,
        }
        
        headers = IgnoreCaseMultiValueDictionary()
        headers[AUTHORIZATION] = BasicAuth(str(self.id), self.secret).encode()
        data = await self.http.oauth2_token(data, headers)
        return Oauth2Access(data, '')
    
    
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
            If `access` was not given neither as ``Oauth2Access``, ``Oauth2User``  or `str`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        Needs `'email'` or / and `'identify'` scopes granted for more data
        """
        if isinstance(access, (Oauth2Access, Oauth2User)):
            access_token = access.access_token
        elif isinstance(access, str):
            access_token = access
        else:
            raise TypeError(
                f'`access` can be `{Oauth2Access.__name__}`, `{Oauth2User.__name__}`, `str`, got '
                f'{access.__class__.__name__}; {access!r}.'
            )
        
        headers = IgnoreCaseMultiValueDictionary()
        headers[AUTHORIZATION] = f'Bearer {access_token}'
        data = await self.http.user_info_get(headers)
        return Oauth2User(data, access)
        
    
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
            If `access` was not given neither as ``Oauth2Access``, ``Oauth2User``  or `str`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If the given `access` not grants `'connections'` scope.
        """
        if isinstance(access, (Oauth2Access, Oauth2User)):
            if __debug__:
                if not access.has_scope(Oauth2Scope.connections):
                    raise AssertionError(
                        f'The given `access` not grants `\'connections\'` scope, what is required, '
                        f'got {access!r}.'
                    )
            
            access_token = access.access_token
        elif isinstance(access, str):
            access_token = access
        else:
            raise TypeError(
                f'`access` can be `{Oauth2Access.__name__}`, `{Oauth2User.__name__}`, `str`'
                f', got {access.__class__.__name__}; {access!r}.'
            )
        
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
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If `access` was not given neither as ``Oauth2Access``, ``Oauth2User``.
        
        Notes
        -----
        By default access tokens expire after one week.
        """
        if __debug__:
            if not isinstance(access, (Oauth2Access, Oauth2User)):
                raise AssertionError(
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
                'scope': join_oauth2_scopes(access.scopes)
            }
        else:
            data = {
                'client_id': self.id,
                'client_secret': self.secret,
                'grant_type': 'client_credentials',
                'scope': join_oauth2_scopes(access.scopes),
            }
        
        data = await self.http.oauth2_token(data, IgnoreCaseMultiValueDictionary())
        
        access._renew(data)
    
    
    async def guild_user_add(self, guild, access, user=None, *, nick=None, roles=None, mute=False, deaf=False):
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
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `user` and `access` refers to a different user.
            - If the nick's length is over `32`.
            - If the nick was not given neither as `None`, `str`.
            - If `mute` was not given as `bool`.
            - If `deaf` was not given as `bool`.
            - If `roles` was not given neither as `None`, `list`.
        """
        user_id = get_user_id_nullable(user)
        
        
        if isinstance(access, Oauth2Access):
            access_token = access.access_token
            
            if __debug__:
                if not access.has_scope(Oauth2Scope.guilds_join):
                    raise AssertionError(
                        f'The given `access` not grants `\'guilds.join\'` scope, what is required, '
                        f'got {access!r}.'
                    )
        
        elif isinstance(access, Oauth2User):
            access_token = access.access_token
            if __debug__:
                if not access.has_scope(Oauth2Scope.guilds_join):
                    raise AssertionError(
                        f'The given `access` not grants `\'guilds.join\'` scope, what is required, '
                        f'got access={access!r}, scopes={access.scopes!r}.'
                    )
                
                if user_id and (user_id != access.id):
                    raise AssertionError(
                        f'The given `user` and `access` refers to different users, got user={user!r}, '
                        f'access={access!r}.'
                    )
            
            user_id = access.id
        
        elif isinstance(access, str):
            access_token = access
        
        else:
            raise TypeError(
                f'`access` can be `{Oauth2Access.__name__}`, `{Oauth2User.__name__}`, `str`, got '
                f'{access.__class__.__name__}; {access!r}.'
            )
        
        
        if not user_id:
            raise TypeError(
                f'`user` was not detectable neither from `user` nor from `access` parameters, got '
                f'user={user!r}, access={access!r}.'
            )
        
        
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
        Requests a user's guilds with it's ``Oauth2Access``. The user must provide the `'guilds'` oauth2  scope for this
        request to succeed.
        
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
            If `access` was not given neither as ``Oauth2Access``, ``Oauth2User``  or `str`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If the given `access` not grants `'guilds'` scope.
        """
        if isinstance(access, (Oauth2Access, Oauth2User)):
            if __debug__:
                if not access.has_scope(Oauth2Scope.guilds):
                    raise AssertionError(
                        f'The given `access` not grants `\'guilds\'` scope, what is required, '
                        f'got {access!r}.'
                    )
            
            access_token = access.access_token
        
        elif isinstance(access, str):
            access_token = access
        
        else:
            raise TypeError(
                f'`access` can be `{Oauth2Access.__name__}`, `{Oauth2User.__name__}` `str`'
                f', got {access.__class__.__name__}; {access!r}.'
            )
        
        headers = IgnoreCaseMultiValueDictionary()
        headers[AUTHORIZATION] = f'Bearer {access_token}'
        data = await self.http.user_guild_get_all(headers)
        return [(create_partial_guild_from_data(guild_data), UserGuildPermission(guild_data)) for guild_data in data]
