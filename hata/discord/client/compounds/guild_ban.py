__all__ = ()

from scarletio import Compound

from ...http import DiscordApiClient
from ...guild import BanAddMultipleResult, BanEntry
from ...guild.ban_add_multiple_result.fields import (
    put_delete_message_duration_into, put_user_ids_into, validate_delete_message_duration, validate_user_ids
)
from ...user import User
from ...utils import log_time_converter

from ..request_helpers import get_guild_id, get_user_id


def _assert__guild_ban_get_chunk__limit(limit):
    """
    Asserts the `limit` parameter of ``Client.guild_ban_get_chunk`` method.
    
    Parameters
    ----------
    limit : `int`
        The amount of ban entries to request. Can be in range [0:1000].
    
    Raises
    ------
    AssertionError
        - If `limit` was not given as `int`.
    """
    if (limit is not None) and (not isinstance(limit, int)):
        raise AssertionError(
            f'`limit` can be `None`, `int`, got {limit.__class__.__name__}; {limit!r}.'
        )
    
    return True


class ClientCompoundGuildBanEndpoints(Compound):
    
    api : DiscordApiClient
    
    
    async def guild_ban_add(self, guild, user, *, delete_message_duration = ..., reason = None):
        """
        Bans the given user from the guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild from where the user will be banned.
        
        user : ``ClientUserBase``, `int`
            The user to ban from the guild.
        
        delete_message_duration : `int`, Optional (Keyword only)
            How much seconds back the user's messages should be deleted. Can be in range [0:604800].
        
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the guild's audit logs.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id = get_guild_id(guild)
        user_id = get_user_id(user)
        
        data = {}
        
        # delete_message_duration
        if (delete_message_duration is not ...):
            put_delete_message_duration_into(validate_delete_message_duration(delete_message_duration), data, False)
        
        await self.api.guild_ban_add(guild_id, user_id, data, reason)
    
    
    async def guild_ban_add_multiple(self, guild, user_ids, *, delete_message_duration = 0, reason = None):
        """
        Bans the given users from the guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild from where the user will be banned.
        
        user_ids : `None`, `iterable` of `int`, `iterable` of ``ClientUserBase``
            The user to ban from the guild.
        
        delete_message_duration : `int` = `0`, Optional (Keyword only)
            How much seconds back the user's messages should be deleted. Can be in range [0:604800].
        
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the guild's audit logs.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id = get_guild_id(guild)
        
        data = {}
        
        # delete_message_duration
        if (delete_message_duration is not ...):
            put_delete_message_duration_into(validate_delete_message_duration(delete_message_duration), data, False)
        
        # user_ids
        put_user_ids_into(validate_user_ids(user_ids), data, False)
        
        data = await self.api.guild_ban_add_multiple(guild_id, data, reason)
        return BanAddMultipleResult.from_data(data)
    
    
    async def guild_ban_delete(self, guild, user, *, reason = None):
        """
        Unbans the user from the given guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild from where the user will be unbanned.
        user : ``ClientUserBase``, `int`
            The user to unban at the guild.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the guild's audit logs.
        
        Raises
        ------
        TypeError
            - If `guild` was not given neither as ``Guild`` nor `int`.
            - If `user` was not given neither as ``ClientUserBase``, nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id = get_guild_id(guild)
        user_id = get_user_id(user)
        
        await self.api.guild_ban_delete(guild_id, user_id, reason)
    
    
    async def guild_ban_get_chunk(self, guild, *, after = None, before = None, limit = 0):
        """
        Returns a chunk of the guild's ban entries.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, what's bans will be requested
        after : `None`, `int`, ``DiscordEntity``, `datetime` = `None`, Optional (Keyword only)
            The timestamp after the banned users were created.
        before : `None`, `int`, ``DiscordEntity``, `datetime` = `None`, Optional (Keyword only)
            The timestamp before the banned users were created.
        limit : `int` = `0`, Optional (Keyword only)
            The amount of ban entries to request. Can be in range [0:1000]
            
            When given as non-positive (<= 0) defaults to the maximal amount.
        
        Returns
        -------
        ban_entries : `list` of ``BanEntry`` elements
            User, reason pairs for each ban entry.
        
        Raises
        ------
        TypeError
            - If `guild` was not given neither as ``Guild``, `int`.
            - If `after`, `before` was passed with an unexpected type.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        See Also
        --------
        ``.guild_ban_get_all`` : Getting all ban entries of a guild.
        """
        guild_id = get_guild_id(guild)
        
        assert _assert__guild_ban_get_chunk__limit(limit)
        
        if limit <= 0 or limit > 1000:
            limit = 1000
        
        query_parameters = {}
        
        if limit != 1000:
            query_parameters['limit'] = limit
        
        if (after is not None):
            query_parameters['after'] = log_time_converter(after)
        
        if (before is not None):
            query_parameters['before'] = log_time_converter(before)
        
        ban_entry_datas = await self.api.guild_ban_get_chunk(guild_id, query_parameters)
        return [BanEntry.from_data(ban_entry_data) for  ban_entry_data in ban_entry_datas]
    
    
    async def guild_ban_get_all(self, guild):
        """
        Returns the guild's ban entries.
        
        This method might need multiple requests to complete it's task
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, what's bans will be requested
        
        Returns
        -------
        ban_entries : `list` of ``BanEntry`` elements
            User - reason pairs for each ban entry.
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as ``Guild``, `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        See Also
        --------
        ``.guild_ban_get_chunk`` : Getting a chunk of ban entries up to 1000 users.
        """
        guild_id = get_guild_id(guild)
        

        query_parameters = {'after': 0}
        
        ban_entries = []
        
        while True:
            ban_entry_datas = await self.api.guild_ban_get_chunk(guild_id, query_parameters)
            ban_entries.extend(BanEntry.from_data(ban_entry_data) for  ban_entry_data in ban_entry_datas)
            
            if len(ban_entry_datas) < 1000:
                break
            
            query_parameters['after'] = ban_entries[-1].user.id
        
        return ban_entries
    
    
    async def guild_ban_get(self, guild, user):
        """
        Returns the guild's ban entry for the given user id.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild where the user banned.
        user : ``ClientUserBase``, `int`
            The user's or their id, who's entry is requested.
        
        Returns
        -------
        ban_entry : ``BanEntry``
            The ban entry.
        
        Raises
        ------
        TypeError
            - If `guild` was not passed neither as ``Guild``, `int`.
            - If `user` was not given neither as ``ClientUserBase``, `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id = get_guild_id(guild)
        user_id = get_user_id(user)
        
        data = await self.api.guild_ban_get(guild_id, user_id)
        return BanEntry(User.from_data(data['user']), data.get('reason', None))
