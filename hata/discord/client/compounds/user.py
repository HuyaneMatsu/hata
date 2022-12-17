__all__ = ()

from scarletio import Compound

from ...bases import maybe_snowflake
from ...channel import Channel
from ...core import GUILDS
from ...guild import Guild, create_partial_guild_from_id
from ...http import DiscordHTTPClient
from ...role import Role
from ...user import ClientUserBase, User
from ...utils import datetime_to_timestamp

from ..request_helpers import (
    get_guild_and_id, get_guild_id, get_channel_guild_id_and_id, get_role_guild_id_and_id, get_user_and_id, get_user_id,
    validate_timeout_duration
)


def _assert__user_guild_profile_edit__nick(nick):
    """
    Asserts the `nick` parameter of ``Client.user_guild_profile_edit`` method.
    
    Parameters
    ----------
    nick : `Ellipsis`, `None`, `int`
        The new nick of the user.
    
    Raises
    ------
    AssertionError
        - If `nick` was not given neither as `None`, `str`.
        - If `nick` length is out of the expected range [0:32].
    """
    if nick is ...:
        pass
    
    elif nick is None:
        pass
    
    elif isinstance(nick, str):
        nick_length = len(nick)
        if nick_length > 32:
            raise AssertionError(
                f'`nick` length can be in range [0:32], got {nick_length}; {nick!r}.'
            )
    
    else:
        raise AssertionError(
            f'`nick` can be `None`, `str`, got {nick.__class__.__name__}; {nick!r}.'
        )
    
    return True


def _assert__user_guild_profile_edit__deaf(deaf):
    """
    Asserts the `deaf` parameter of ``Client.user_guild_profile_edit`` method.
    
    Parameters
    ----------
    deaf : `Ellipsis`, `bool`
        Whether the user should be deafen at the voice channels.
    
    Raises
    ------
    AssertionError
        - If `deaf` was not given as `bool`.
    """
    if (deaf is not ...) and (not isinstance(deaf, bool)):
        raise TypeError(
            f'`deaf` can be `bool`, got {deaf.__class__.__name__}; {deaf!r}'
        )
    
    return True


def _assert__user_guild_profile_edit__mute(mute):
    """
    Asserts the `mute` parameter of ``Client.user_guild_profile_edit`` method.
    
    Parameters
    ----------
    mute : `Ellipsis`, `bool`
        Whether the user should be muted at the voice channels.
    
    Raises
    ------
    AssertionError
        - If `mute` was not given as `bool`.
    """
    if (mute is not ...) and (not isinstance(mute, bool)):
        raise TypeError(
            f'`mute` can be `bool`, got {mute.__class__.__name__}; {mute!r}'
        )
    
    return True


def _assert__guild_user_search__query(query):
    """
    Asserts the `query` parameter of ``Client.guild_user_search`` method.
    
    Parameters
    ----------
    query : `str`
        The query string with what the user's name or nick should start.
    
    Raises
    ------
    AssertionError
        - If `query` was not given as `str`.
        - If `query`'s length is out of the expected range [1:32].
    """
    if not isinstance(query, str):
        raise TypeError(
            f'`query` can be `str`, got {query.__class__.__name__}; {query!r}'
        )
    
    query_length = len(query)
    if query_length < 1 or query_length > 32:
        raise AssertionError(
            f'`query` length can be in range [1:32], got {query_length!r}; {query!r}.'
        )
    
    return True


def _assert__guild_user_search__limit(limit):
    """
    Asserts the `limit` parameter of ``Client.guild_user_search`` method.
    
    Parameters
    ----------
    limit : `int`
        The maximal amount of users to return. Can be in range [1:1000].
    
    Raises
    ------
    AssertionError
        - If `limit` was not given as `int`.
    """
    if not isinstance(limit, int):
        raise TypeError(
            f'`limit` can be `int`, got {limit.__class__.__name__}; {limit!r}'
        )
    
    return True


class ClientCompoundUserEndpoints(Compound):
    
    http : DiscordHTTPClient
    id : int
    
    async def user_guild_profile_edit(
        self, guild, user, *, nick = ..., deaf = ..., mute = ..., voice_channel = ..., roles = ...,
        timeout_duration = ..., reason = None
    ):
        """
        Edits the user's guild profile at the given guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            Where the user will be edited.
        
        user : ``ClientUserBase``, `int`
            The user to edit, or their identifier.
        
        nick : `None`, `str`, Optional (Keyword only)
            The new nick of the user. You can remove the current one by passing it as `None`, an empty string.
        
        deaf : `bool`, Optional (Keyword only)
            Whether the user should be deafen at the voice channels.
        
        mute : `bool`, Optional (Keyword only)
            Whether the user should be muted at the voice channels.
        
        voice_channel : `None`, ``Channel``, `int` , Optional (Keyword only)
            Moves the user to the given voice channel. Only applicable if the user is already at a voice channel.
            
            Pass it as `None` to disconnect the user from it's voice channel.
        
        roles : `None`, `iterable` of (``Role``, `int`), Optional (Keyword only)
            The new roles of the user. Give it as `None` to remove all of the user's roles.
        
        timeout_duration: `None`, `int`, `float`, `timedelta`, `datetime`, Optional (Keyword only)
            The timeout duration of the user in seconds.
            
            Pass it as `None` or as a non-positive duration to remove it.
            
            The max allowed value equals to 28 days.
            
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Will show up at the guild's audit logs.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild, guild_id = get_guild_and_id(guild)
        user, user_id = get_user_and_id(user)
        
        assert _assert__user_guild_profile_edit__nick(nick)
        assert _assert__user_guild_profile_edit__deaf(deaf)
        assert _assert__user_guild_profile_edit__mute(mute)
        
        data = {}
        if (nick is not ...):
            if (nick is not None) and (not nick):
                nick = None
            
            if (guild is not None) and (user is not None) and guild.partial:
                try:
                    guild_profile = user.guild_profiles[guild.id]
                except KeyError:
                    should_edit_nick = True
                else:
                    if guild_profile.nick == nick:
                        should_edit_nick = False
                    else:
                        should_edit_nick = True
            else:
                should_edit_nick = True
            
            if should_edit_nick:
                if self.id == user_id:
                    await self.http.client_guild_profile_edit(guild_id, {'nick': nick}, reason)
                else:
                    data['nick'] = nick
                    
        if (deaf is not ...):
            data['deaf'] = deaf
        
        if (mute is not ...):
            data['mute'] = mute
        
        if (voice_channel is not ...):
            while True:
                if voice_channel is None:
                    voice_channel_id = None
                    break
                
                elif isinstance(voice_channel, Channel):
                    if voice_channel.is_in_group_guild_connectable() or voice_channel.partial:
                        voice_channel_id = voice_channel.id
                        break
                
                else:
                    voice_channel_id = maybe_snowflake(voice_channel)
                    if voice_channel_id is not None:
                        break
                
                raise TypeError(
                    f'`voice_channel` can be `None`, any guild connectable channel, `int`, got '
                    f'{voice_channel.__class__.__name__}; {voice_channel!r}.'
                )
            
            data['channel_id'] = voice_channel_id
        
        
        if (roles is not ...):
            role_ids = set()
            if (roles is not None):
                if getattr(roles, '__iter__', None) is None:
                    raise TypeError(
                        f'`roles` can be `None`, `iterable`, got {roles.__class__.__name__}; {roles!r}.'
                    )
                
                for role in roles:
                    
                    if isinstance(role, Role):
                        role_id = role.id
                    else:
                        role_id = maybe_snowflake(role)
                        if role_id is None:
                            raise TypeError(
                                f'`roles` can contain `{Role.__name__}`, `int` elements, got '
                                f'{role.__class__.__name__}; {role!r}; roles={roles!r}.'
                            )
                    
                    role_ids.add(role_id)
            
            data['roles'] = role_ids
        
        
        if (timeout_duration is not ...):
            timeout_ends_at = validate_timeout_duration(timeout_duration)
            
            if (timeout_ends_at is None):
                timed_out_until_raw = None
            else:
                timed_out_until_raw = datetime_to_timestamp(timeout_ends_at)
            data['communication_disabled_until'] = timed_out_until_raw
        
        await self.http.user_guild_profile_edit(guild_id, user_id, data, reason)
    
    
    async def user_role_add(self, user, role, *, reason = None):
        """
        Adds the role on the user.
        
        This method is a coroutine.
        
        Parameters
        ----------
        user : ```ClientUserBase``, `int`
            The user who will get the role.
        role : ``Role``, `tuple` (`int`, `int`)
            The role to add on the user.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        TypeError
            - If `user` was not given neither as ``ClientUserBase``, neither as `int`.
            - If `role` was not given neither as ``Role`` nor as `tuple` of (`int`, `int`).
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id, role_id = get_role_guild_id_and_id(role)
        user_id = get_user_id(user)
        
        await self.http.user_role_add(guild_id, user_id, role_id, reason)
    
    
    async def user_role_delete(self, user, role, *, reason = None):
        """
        Deletes the role from the user.
        
        This method is a coroutine.
        
        Parameters
        ----------
        user : ```ClientUserBase``, `int`
            The user from who the role will be removed.
        role : ``Role``, `tuple` (`int`, `int`)
            The role to remove from the user.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        TypeError
            - If `user` was not given neither as ``ClientUserBase``, neither as `int`.
            - If `role` was not given neither as ``Role`` nor as `tuple` of (`int`, `int`).
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id, role_id = get_role_guild_id_and_id(role)
        user_id = get_user_id(user)
        
        await self.http.user_role_delete(guild_id, user_id, role_id, reason)
    
    
    async def user_voice_move(self, user, channel):
        """
        Moves the user to the given voice channel. The user must be in a voice channel at the respective guild already.
        
        This method is a coroutine.
        
        Parameters
        ----------
        user : ```ClientUserBase``, `int`
            The user to move.
        channel : ``Channel``, `tuple` (`int`, `int`)
            The channel where the user will be moved.
        
        Raises
        ------
        TypeError
            - If `user` was not given neither as ``ClientUserBase``, neither as `int`.
            - If `channel` was not given neither as ``Channel`` nor as `tuple` of (`int`, `int`).
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id, channel_id = get_channel_guild_id_and_id(channel, Channel.is_in_group_guild_connectable)
        if not guild_id:
            return
        
        user_id = get_user_id(user)
       
        await self.http.user_move(guild_id, user_id, {'channel_id': channel_id})
    
    
    async def user_voice_move_to_speakers(self, user, channel):
        """
        Moves the user to the speakers inside of a stage channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        user : ```ClientUserBase``, `int`
            The user to move.
        channel : ``Channel``, `tuple` (`int`, `int`)
            The channel where the user will be moved.
        
        Raises
        ------
        TypeError
            - If `user` was not given neither as ``ClientUserBase``, neither as `int`.
            - If `channel` was not given neither as ``Channel`` nor as `tuple` of (`int`, `int`).
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id, channel_id = get_channel_guild_id_and_id(channel, Channel.is_guild_stage)
        if not guild_id:
            return
        
        user_id = get_user_id(user)
       
        data = {
            'suppress' : False,
            'channel_id': channel_id,
        }
        
        await self.http.voice_state_user_edit(guild_id, user_id, data)
    
    
    async def user_voice_move_to_audience(self, user, channel):
        """
        Moves the user to the audience inside of a stage channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        user : ```ClientUserBase``, `int`
            The user to move.
        channel : ``Channel``, `tuple` (`int`, `int`)
            The channel where the user will be moved.
        
        Raises
        ------
        TypeError
            - If `user` was not given neither as ``ClientUserBase``, neither as `int`.
            - If `channel` was not given neither as ``Channel`` nor as `tuple` of (`int`, `int`).
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id, channel_id = get_channel_guild_id_and_id(channel, Channel.is_guild_stage)
        if not guild_id:
            return
        
        user_id = get_user_id(user)
       
        data = {
            'suppress': True,
            'channel_id': channel_id,
        }
        
        await self.http.voice_state_user_edit(guild_id, user_id, data)
    
    
    async def user_voice_kick(self, user, guild):
        """
        Kicks the user from the guild's voice channels. The user must be in a voice channel at the guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        user : ```ClientUserBase``, `int`
            The user who will be kicked from the voice channel.
        guild : ``Guild``, `int`
            The guild from what's voice channel the user will be kicked.
        
        Raises
        ------
        TypeError
            - If `user` was not given neither as ``ClientUserBase``, neither as `int`.
            - If `guild` was not given neither as ``Guild`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        user_id = get_user_id(user)
        guild_id = get_guild_id(guild)
        
        await self.http.user_move(guild_id, user_id, {'channel_id': None})
    
    
    async def user_get(self, user, *, force_update=False):
        """
        Gets an user by it's id. If the user is already loaded updates it.
        
        This method is a coroutine.
        
        Parameters
        ----------
        user : ``ClientUserBase``, `int`
            The user, who will be requested.
        force_update : `bool` = `False`, Optional (Keyword only)
            Whether the user should be requested even if it supposed to be up to date.
        
        Returns
        -------
        user : ``ClientUserBase``
        
        Raises
        ------
        TypeError
            If `user` was not given neither as ``ClientUserBase``, neither as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Raises
        ------
        TypeError
            If `user` was not given as ``ClientUserBase``, nor as `int`.
        """
        user, user_id = get_user_and_id(user)
        
        # a goto to check whether we should force update the user.
        while True:
            if force_update:
                break
            
            if user is None:
                break
            
            for guild_id in user.guild_profiles.keys():
                try:
                    guild = GUILDS[guild_id]
                except KeyError:
                    continue
                
                if not guild.partial:
                    return user
            
            break
        
        data = await self.http.user_get(user_id)
        return User._create_and_update(data)
    
    
    async def guild_user_get(self, guild, user):
        """
        Gets an user and it's profile at a guild. The user must be the member of the guild. If the user is already
        loaded updates it.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, where the user is.
        user : ```ClientUserBase``, `int`
            The user's id, who will be requested.
        
        Returns
        -------
        user : ``ClientUserBase``
        
        Raises
        ------
        TypeError
            - If `user` was not given neither as ``ClientUserBase``, neither as `int`.
            - If `guild` was not given neither as ``Guild`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        user_id = get_user_id(user)
        guild, guild_id = get_guild_and_id(guild)
        
        data = await self.http.guild_user_get(guild_id, user_id)
        
        if guild is None:
            guild = create_partial_guild_from_id(guild_id)
        
        return User._create_and_update(data, guild)
    
    
    async def guild_user_search(self, guild, query, limit=1):
        """
        Gets an user and it's profile at a guild by it's name. If the users are already loaded updates it.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``
            The guild, where the user is.
        
        query : `name`
            The query string with what the user's name or nick should start.
        
        limit : `int` = `1`, Optional
            The maximal amount of users to return. Can be in range [1:1000].
            
            When passed as non-positive value, will default to the maximal allowed amount.
        
        Returns
        -------
        users : `list` of ``ClientUserBase``
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as ``Guild`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `limit` was not given as `str`.
            - If `limit` is out fo expected range [1:1000].
        """
        guild, guild_id = get_guild_and_id(guild)
        
        assert _assert__guild_user_search__query(query)
        assert _assert__guild_user_search__limit(limit)
        
        if limit <= 0 or limit > 1000:
            limit = 1000
        
        data = {'query': query}
        
        if limit != 1:
            data['limit'] = limit
        
        data = await self.http.guild_user_search(guild_id, data)
        
        if guild is None:
            guild = create_partial_guild_from_id(guild_id)
        
        return [User._create_and_update(user_data, guild) for user_data in data]
