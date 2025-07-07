__all__ = ()

from scarletio import Compound

from ...channel import Channel
from ...core import GUILDS
from ...guild import Guild
from ...http import DiscordApiClient
from ...payload_building import add_payload_fields_from_keyword_parameters
from ...user import create_partial_user_from_id, ClientUserBase, User, VoiceState
from ...user.guild_profile.utils import GUILD_PROFILE_FIELD_CONVERTERS

from ..request_helpers import (
    get_channel_guild_id_and_id, get_guild_and_id, get_guild_id, get_role_guild_id_and_id, get_user_and_id, get_user_id
)


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
    
    api : DiscordApiClient
    id : int
    
    async def user_guild_profile_edit(
        self,
        guild,
        user,
        *,
        reason = None,
        **keyword_parameters,
    ):
        """
        Edits the user's guild profile at the given guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``int | Guild``
            Where the user will be edited.
        
        user : ``ClientUserBase``, `int`
            The user to edit, or their identifier.
        
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Will show up at the guild's audit logs.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters representing which field of the guild profile should be edited.
        
        Other Parameters
        ----------------
        deaf : `bool`, Optional (Keyword only)
            Whether the user should be deafen at the voice channels.
        
        mute : `bool`, Optional (Keyword only)
            Whether the user should be muted at the voice channels.
        
        nick : `None`, `str`, Optional (Keyword only)
            The new nick of the user. You can remove the current one by passing it as `None`, an empty string.
        
        voice_channel : ``None | int | Channel`` , Optional (Keyword only)
            Moves the user to the given voice channel. Only applicable if the user is already at a voice channel.
            
            Pass it as `None` to disconnect the user from it's voice channel.
        
        role_ids : `None`, `iterable` of (``Role``, `int`), Optional (Keyword only)
            The new roles of the user. Give it as `None` to remove all of the user's roles.
        
        roles : `None`, `iterable` of (``Role``, `int`), Optional (Keyword only)
            Alternative of `role_ids`.
        
        timed_out_until : `None | DateTime`, Optional (Keyword only)
            Until when the user is timed out.
        
        timeout_duration : `int`, `float`, `TimeDelta`, Optional (Keyword only)
            The timeout duration of the user in seconds or in delta.
        
            The max allowed value equals to 28 days.
        
        voice_channel : ``None | int | Channel`` , Optional (Keyword only)
            Alternative of `voice_channel_id`.
        
        voice_channel_id : ``None | int | Channel`` , Optional (Keyword only)
            Moves the user to the given voice channel. Only applicable if the user is already at a voice channel.
            
            Pass it as `None` to disconnect the user from it's voice channel.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id = get_guild_id(guild)
        user_id = get_user_id(user)
        
        data = {}
        add_payload_fields_from_keyword_parameters(GUILD_PROFILE_FIELD_CONVERTERS, keyword_parameters, data, True)
        
        if data:
            await self.api.user_guild_profile_edit(guild_id, user_id, data, reason)
    
    
    async def user_role_add(self, user, role, *, reason = None):
        """
        Adds the role on the user.
        
        This method is a coroutine.
        
        Parameters
        ----------
        user : ```ClientUserBase``, `int`
            The user who will get the role.
        role : ``Role | (int, int)``
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
        
        await self.api.user_role_add(guild_id, user_id, role_id, reason)
    
    
    async def user_role_delete(self, user, role, *, reason = None):
        """
        Deletes the role from the user.
        
        This method is a coroutine.
        
        Parameters
        ----------
        user : ```ClientUserBase``, `int`
            The user from who the role will be removed.
        role : ``Role | (int, int)``
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
        
        await self.api.user_role_delete(guild_id, user_id, role_id, reason)
    
    
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
       
        await self.api.user_move(guild_id, user_id, {'channel_id': channel_id})
    
    
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
        
        await self.api.voice_state_edit(guild_id, user_id, data)
    
    
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
        
        await self.api.voice_state_edit(guild_id, user_id, data)
    
    
    async def user_get(self, user, *, force_update = False):
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
        
        data = await self.api.user_get(user_id)
        return User.from_data(data)
    
    
    async def guild_user_get(self, guild, user):
        """
        Gets an user and it's profile at a guild. The user must be the member of the guild. If the user is already
        loaded updates it.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``int | Guild``
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
        guild_id = get_guild_id(guild)
        
        data = await self.api.guild_user_get(guild_id, user_id)
        
        return User.from_data(data['user'], data, guild_id)
    
    
    async def guild_user_search(self, guild, query, limit = 1):
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
        users : ``list<ClientUserBase>``
        
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
        guild_id = get_guild_id(guild)
        
        assert _assert__guild_user_search__query(query)
        assert _assert__guild_user_search__limit(limit)
        
        if limit <= 0 or limit > 1000:
            limit = 1000
        
        data = {'query': query}
        
        if limit != 1:
            data['limit'] = limit
        
        datas = await self.api.guild_user_search(guild_id, data)
        
        return [User.from_data(data['user'], data, guild_id) for data in datas]
    
    
    async def user_voice_kick(self, user, guild):
        """
        Kicks the user from the guild's voice channels. The user must be in a voice channel at the guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        user : ```ClientUserBase``, `int`
            The user who will be kicked from the voice channel.
        guild : ``int | Guild``
            The guild from what's voice channel the user will be kicked.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        user_id = get_user_id(user)
        guild_id = get_guild_id(guild)
        
        await self.api.user_move(guild_id, user_id, {'channel_id': None})
    
    
    async def voice_state_get(self, guild, user, *, force_update = False):
        """
        Gets the user's voice state at the given guild.
                
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``int | Guild``
            The respective guild.
        user : ```ClientUserBase``, `int`
            The user to get its voice state.
        force_update : `bool` = `False`, Optional (Keyword only)
            Whether the user should be requested even if it supposed to be up to date.
        
        Returns
        -------
        voice_state : ``VoiceState``
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
            
        """
        user, user_id = get_user_and_id(user)
        guild, guild_id = get_guild_and_id(guild)
        
        while True:
            if force_update:
                break
            
            if (guild is None) or guild.partial:
                break
            
            voice_state = guild.get_voice_state(user_id)
            if (voice_state is None):
                break
            
            return voice_state
            
        voice_state_data = await self.api.voice_state_get(guild_id, user_id)
        
        # Try to re-get the guild.
        if guild is None:
            guild = GUILDS.get(guild_id, None)
        
        if guild is None:
            return VoiceState.from_data(voice_state_data, guild_id, strong_cache = False)
        
        if user is None:
            user = create_partial_user_from_id(user_id)
        
        return guild._update_voice_state_restricted(voice_state_data, user)
    
    
    async def voice_state_get_own(self, guild, *, force_update = False):
        """
        Gets the user's voice state at the given guild.
                
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``int | Guild``
            The respective guild.
        force_update : `bool` = `False`, Optional (Keyword only)
            Whether the user should be requested even if it supposed to be up to date.
        
        Returns
        -------
        voice_state : ``VoiceState``
        
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
        
        while True:
            if force_update:
                break
            
            if (guild is None) or guild.partial:
                break
            
            voice_state = guild.get_voice_state(self.id)
            if (voice_state is None):
                break
            
            return voice_state
        
        voice_state_data = await self.api.voice_state_get_own(guild_id)
        
        # Try to re-get the guild.
        if guild is None:
            guild = GUILDS.get(guild_id, None)
        
        if guild is None:
            return VoiceState.from_data(voice_state_data, guild_id, strong_cache = False)
        
        return guild._update_voice_state_restricted(voice_state_data, self)
