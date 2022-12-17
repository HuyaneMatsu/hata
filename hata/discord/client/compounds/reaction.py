__all__ = ()

from scarletio import Compound, Theory

from ...core import MESSAGES

from ...http import DiscordHTTPClient

from ...user import ClientUserBase, User
from ...utils import log_time_converter

from ..request_helpers import get_channel_id_and_message_id, get_emoji_from_reaction, get_reaction, get_user_id


class ClientCompoundReactionEndpoints(Compound):
    
    id: int
    http : DiscordHTTPClient
    
    @Theory
    async def message_get(self, message, *, force_update = False): ...
    
    
    async def reaction_add(self, message, emoji):
        """
        Adds a reaction on the given message.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message : ``Message``, `tuple` (`int`, `int`)
            The message on which the reaction will be put on.
        emoji : ``Emoji``, `str`
            The emoji to react with.
        
        Raises
        ------
        TypeError
            - If `message` was not given neither as ``Message``, `tuple` (`int`, `int`).
            - If `emoji`'s type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id, message_id = get_channel_id_and_message_id(message)
        emoji_as_reaction = get_reaction(emoji)
        
        await self.http.reaction_add(channel_id, message_id, emoji_as_reaction)
    
    
    async def reaction_delete(self, message, emoji, user):
        """
        Removes the specified reaction of the user from the given message.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message : ``Message``, `tuple` (`int`, `int`)
            The message from which the reaction will be removed.
        emoji : ``Emoji``, `str`
            The emoji to remove.
        user : ```ClientUserBase``, `int`
            The user, who's reaction will be removed.
        
        Raises
        ------
        TypeError
            - If `message` was not given neither as ``Message``, `tuple` (`int`, `int`).
            - If `user` was not given neither as ``ClientUserBase`` nor `int`.
            - If `emoji` was not given as ``Emoji``, `str`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id, message_id = get_channel_id_and_message_id(message)
        emoji_as_reaction = get_reaction(emoji)
        user_id = get_user_id(user)
        
        if user_id == self.id:
            await self.http.reaction_delete_own(channel_id, message_id, emoji_as_reaction)
        else:
            await self.http.reaction_delete(channel_id, message_id, emoji_as_reaction, user_id)
    
    
    async def reaction_delete_emoji(self, message, emoji):
        """
        Removes all the reaction of the specified emoji from the given message.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message : ``Message``, `tuple` (`int`, `int`)
            The message from which the reactions will be removed.
        emoji : ``Emoji``, `str`
            The reaction to remove.
        
        Raises
        ------
        TypeError
            - If `message` was not given neither as ``Message``, `tuple` (`int`, `int`).
            - If `emoji`'s type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id, message_id = get_channel_id_and_message_id(message)
        as_reaction = get_reaction(emoji)
        
        await self.http.reaction_delete_emoji(channel_id, message_id, as_reaction)
    
    
    async def reaction_delete_own(self, message, emoji):
        """
        Removes the specified reaction of the client from the given message.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message : ``Message``, `tuple` (`int`, `int`)
            The message from which the reaction will be removed.
        emoji : ``Emoji``, `str`
            The emoji to remove.
        
        Raises
        ------
        TypeError
            - If `message` was not given neither as ``Message``, `tuple` (`int`, `int`).
            - If `emoji`'s type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id, message_id = get_channel_id_and_message_id(message)
        as_reaction = get_reaction(emoji)
        await self.http.reaction_delete_own(channel_id, message_id, as_reaction)
    
    
    async def reaction_clear(self, message):
        """
        Removes all the reactions from the given message.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message : ``Message``, `tuple` (`int`, `int`)
            The message from which the reactions will be cleared.
        
        Raises
        ------
        TypeError
            If `message` was not given neither as ``Message``, `tuple` (`int`, `int`) instance.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id, message_id = get_channel_id_and_message_id(message)
        
        await self.http.reaction_clear(channel_id, message_id)
    
    
    async def reaction_user_get_chunk(self, message, emoji, *, limit=None, after=None):
        """
        Requests the users, who reacted on the given message with the given emoji.
        
        If the message has no reactors at all or no reactors with that emoji, returns an empty list. If we know the
        emoji's every reactors we query the parameters from that.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message : ``Message``, `tuple` (`int`, `int`)
            The message, what's reactions will be requested.
        emoji : ``Emoji``, `str`
            The emoji, what's reactors will be requested.
        limit : `None`, `int` = `None`, Optional (Keyword only)
            The amount of users to request. Can be in range [1:100]. Defaults to 25 by Discord.
        after : `None`, `int`, ``DiscordEntity``, `datetime` = `None`, Optional (Keyword only)
            The timestamp after the message's reactors were created.
        
        Returns
        -------
        users : `list` of ``ClientUserBase``
        
        Raises
        ------
        TypeError
            - If `message` was not given neither as ``Message``, `tuple` (`int`, `int`).
            - If `after` was passed with an unexpected type.
            - If `emoji`'s type is incorrect.
        ValueError
            The given `emoji` is not a valid reaction.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `limit` was not given neither as `None`, `int`.
            - If `limit` is out of the expected range [1:100].
        
        Notes
        -----
        `before` parameter is not supported by Discord.
        """
        if limit is None:
            limit = 25
        else:
            if __debug__:
                if not isinstance(limit, int):
                    raise AssertionError(
                        f'`limit` can be `None`, `int`, got {limit.__class__.__name__}; {limit!r}.'
                    )
                
                if limit < 1 or limit > 100:
                    raise AssertionError(
                        f'`limit` can be between in range [1:100], got {limit!r}.'
                    )
        
        channel_id, message_id = get_channel_id_and_message_id(message)
        emoji = get_emoji_from_reaction(emoji)
        
        try:
            message = MESSAGES[message_id]
        except KeyError:
            reactions = None
        else:
            reactions = message.reactions
            
            if reactions is None:
                return []
            
            try:
                line = reactions[emoji]
            except KeyError:
                return []
            
            if not line.unknown:
                after = 0 if after is None else log_time_converter(after)
                # before = 9223372036854775807 if before is None else log_time_converter(before)
                users = line.filter_after(limit, after)
                return users
        
        data = {}
        if limit != 25:
            data['limit'] = limit
        
        if (after is not None):
            data['after'] = log_time_converter(after)
        
        # if (before is not None):
        #     data['before'] = log_time_converter(before)
        
        data = await self.http.reaction_user_get_chunk(channel_id, message_id, emoji.as_reaction, data)
        
        users = [User.from_data(user_data) for user_data in data]
        
        if (reactions is not None):
            reactions._update_some_users(emoji, users)
        
        return users
    
    
    async def reaction_user_get_all(self, message, emoji):
        """
        Requests the all the users, which reacted on the message with the given message.
        
        If the message has no reactors at all or no reactors with that emoji returns an empty list. If the emoji's
        every reactors are known, then do requests are done.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message : ``Message``, `tuple` (`int`, `int`)
            The message, what's reactions will be requested.
        emoji : ``Emoji``, `str`
            The emoji, what's reactors will be requested.
        
        Returns
        -------
        users : `list` of ``ClientUserBase``
        
        Raises
        ------
        TypeError
            - If `message` was not given neither as ``Message``, `tuple` (`int`, `int`).
            - If `emoji`'s type is incorrect.
        ValueError
            The given `emoji` is not a valid reaction.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id, message_id = get_channel_id_and_message_id(message)
        emoji = get_emoji_from_reaction(emoji)
        
        try:
            message = MESSAGES[message_id]
        except KeyError:
            reactions = None
        else:
            reactions = message.reactions
            
            if (reactions is None):
                return []
            
            try:
                line = reactions[emoji]
            except KeyError:
                return []
            
            if not line.unknown:
                users = list(line)
                return users
        
        data = {'limit': 100, 'after': 0}
        users = []
        reaction = emoji.as_reaction
        
        while True:
            user_datas = await self.http.reaction_user_get_chunk(channel_id, message_id, reaction, data)
            users.extend(User.from_data(user_data) for user_data in user_datas)
            
            if len(user_datas) < 100:
                break
            
            data['after'] = users[-1].id
        
        if (reactions is not None):
            reactions._update_all_users(emoji, users)
        
        return users
    
    
    async def reaction_get_all(self, message):
        """
        Requests all the reactors for every emoji on the given message.
        
        Like the other reaction getting methods, this method prefers using the internal cache as well over doing a
        request.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message : ``Message``, `tuple` (`int`, `int`)
            The message, what's reactions will be requested.
        
        Returns
        -------
        message : ``Message``
        
        Raises
        ------
        TypeError
            If `message` was not given neither as ``Message``, `tuple` (`int`, `int`).
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id, message_id = get_channel_id_and_message_id(message)
        message = MESSAGES.get(message_id, None)
        if (message is None):
            message = await self.message_get((channel_id, message_id))
        
        reactions = message.reactions
        if (reactions is not None) and reactions:
            users = []
            data = {'limit': 100}
            
            for emoji, line in reactions.items():
                if not line.unknown:
                    continue
                
                reaction = emoji.as_reaction
                data['after'] = 0
                
                while True:
                    user_datas = await self.http.reaction_user_get_chunk(channel_id, message_id, reaction, data)
                    users.extend(User.from_data(user_data) for user_data in user_datas)
                    
                    if len(user_datas) < 100:
                        break
                    
                    data['after'] = users[-1].id
                
                reactions._update_all_users(emoji, users)
                users.clear()
        
        return message
