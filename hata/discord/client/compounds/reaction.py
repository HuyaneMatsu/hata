__all__ = ()

from scarletio import Compound, Theory

from ...core import MESSAGES
from ...emoji import Emoji
from ...emoji.reaction_mapping.fields import validate_reaction
from ...http import DiscordApiClient
from ...user import ClientUserBase, User
from ...utils import log_time_converter

from ..request_helpers import get_channel_id_and_message_id, get_reaction_emoji_value_and_type, get_user_id


class ClientCompoundReactionEndpoints(Compound):
    
    id: int
    api : DiscordApiClient
    
    @Theory
    async def message_get(self, message, *, force_update = False): ...
    
    
    async def reaction_add(self, message, reaction):
        """
        Adds a reaction on the given message.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message : ``Message``, `tuple` (`int`, `int`)
            The message on which the reaction will be put on.
        
        emoji : ``Reaction``, ``Emoji``, `str`
            The reaction to react with. if given as ``Emoji`` / `str` will use standard reaction.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id, message_id = get_channel_id_and_message_id(message)
        emoji_value, reaction_type = get_reaction_emoji_value_and_type(reaction)
        await self.api.reaction_add(channel_id, message_id, emoji_value, {'type': reaction_type.value})
    
    
    async def reaction_delete(self, message, reaction, user):
        """
        Removes the specified reaction of the user from the given message.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message : ``Message``, `tuple` (`int`, `int`)
            The message from which the reaction will be removed.
            
        reaction : ``Reaction``, ``Emoji``, `str`
            The reaction to remove.
            
        user : ```ClientUserBase``, `int`
            The user, who's reaction will be removed.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id, message_id = get_channel_id_and_message_id(message)
        emoji_value, reaction_type = get_reaction_emoji_value_and_type(reaction)
        user_id = get_user_id(user)
        
        if user_id == self.id:
            await self.api.reaction_delete_own(channel_id, message_id, emoji_value, reaction_type.value)
        else:
            await self.api.reaction_delete(channel_id, message_id, emoji_value, reaction_type.value, user_id)
    
    
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
            - If a parameter's type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id, message_id = get_channel_id_and_message_id(message)
        
        if isinstance(emoji, Emoji):
            emoji_value = emoji.as_reaction
        elif isinstance(emoji, str):
            emoji_value = emoji
        else:
            raise TypeError(
                f'`emoji` can be `{Emoji.__name__}`, `str`, got {emoji.__class__.__name__}; {emoji!r}.'
            )
        
        await self.api.reaction_delete_emoji(channel_id, message_id, emoji_value)
    
    
    async def reaction_delete_own(self, message, reaction):
        """
        Removes the specified reaction of the client from the given message.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message : ``Message``, `tuple` (`int`, `int`)
            The message from which the reaction will be removed.
            
        emoji : ``Reaction``, ``Emoji``, `str`
            The reaction to remove.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id, message_id = get_channel_id_and_message_id(message)
        emoji_value, reaction_type = get_reaction_emoji_value_and_type(reaction)
        await self.api.reaction_delete_own(channel_id, message_id, emoji_value, reaction_type.value)
    
    
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
        
        await self.api.reaction_clear(channel_id, message_id)
    
    
    async def reaction_user_get_chunk(self, message, reaction, *, limit = None, after = None):
        """
        Requests the users, who reacted on the given message with the given emoji.
        
        If the message has no reactors at all or no reactors with that emoji, returns an empty list. If we know the
        emoji's every reactors we query the parameters from that.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message : ``Message``, `tuple` (`int`, `int`)
            The message, what's reactions will be requested.
        reaction : ``Reaction``, ``Emoji``, `str`
            The emoji, what's reactors will be requested.
        limit : `None`, `int` = `None`, Optional (Keyword only)
            The amount of users to request. Can be in range [1:100]. Defaults to 100 by Discord.
        after : `None`, `int`, ``DiscordEntity``, `datetime` = `None`, Optional (Keyword only)
            The timestamp after the message's reactors were created.
        
        Returns
        -------
        users : `list` of ``ClientUserBase``
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            The given `emoji` is not a valid reaction.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        `before` parameter is not supported by Discord.
        """
        if limit is None:
            limit = 100
        
        elif isinstance(limit, int):
            if limit < 1:
                limit = 1
            elif limit > 100:
                limit = 100
        
        else:
            raise TypeError(
                f'`limit` can be `None`, `int`, got {limit.__class__.__name__}; {limit!r}.'
            )
        
        channel_id, message_id = get_channel_id_and_message_id(message)
        reaction = validate_reaction(reaction)
        
        try:
            message = MESSAGES[message_id]
        except KeyError:
            reactions = None
        else:
            reactions = message.reactions
            
            if reactions is None:
                return []
            
            try:
                line = reactions[reaction]
            except KeyError:
                return []
            
            if not line.unknown:
                after = 0 if after is None else log_time_converter(after)
                # before = 9223372036854775807 if before is None else log_time_converter(before)
                users = line.filter_after(limit, after)
                return users
        
        query_parameters = {
            'limit': limit,
            'type': reaction.type.value,
        }
        
        if (after is not None):
            query_parameters['after'] = log_time_converter(after)
        
        # Before is not supported!
        # if (before is not None):
        #     data['before'] = log_time_converter(before)
        
        data = await self.api.reaction_user_get_chunk(
            channel_id, message_id, reaction.emoji.as_reaction, query_parameters
        )
        
        users = [User.from_data(user_data) for user_data in data]
        
        if (reactions is not None):
            reactions._fill_some_reactions(reaction, users)
        
        return users
    
    
    async def reaction_user_get_all(self, message, reaction):
        """
        Requests the all the users, which reacted on the message with the given message.
        
        If the message has no reactors at all or no reactors with that emoji returns an empty list. If the emoji's
        every reactors are known, then do requests are done.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message : ``Message``, `tuple` (`int`, `int`)
            The message, what's reactions will be requested.
        reaction : ``Reacton``, ``Emoji``, `str`
            The reaction, what's reactors will be requested.
        
        Returns
        -------
        users : `list` of ``ClientUserBase``
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            The given `emoji` is not a valid reaction.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id, message_id = get_channel_id_and_message_id(message)
        reaction = validate_reaction(reaction)
        
        try:
            message = MESSAGES[message_id]
        except KeyError:
            reactions = None
        else:
            reactions = message.reactions
            
            if (reactions is None):
                return []
            
            try:
                line = reactions[reaction]
            except KeyError:
                return []
            
            if not line.unknown:
                users = [*line]
                return users
        
        query_parameters = {
            'after': 0,
            'limit': 100,
            'type': reaction.type.value,
        }
        
        users = []
        emoji_value = reaction.emoji.as_reaction
        
        while True:
            user_datas = await self.api.reaction_user_get_chunk(
                channel_id, message_id, emoji_value, query_parameters
            )
            users.extend(User.from_data(user_data) for user_data in user_datas)
            
            if len(user_datas) < 100:
                break
            
            query_parameters['after'] = users[-1].id
        
        if (reactions is not None):
            reactions._fill_all_reactions(reaction, users)
        
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
            - If a parameter's type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        # Get message
        message = await self.message_get(message)
        
        # Get reactions
        reactions = message.reactions
        if (reactions is not None) and reactions:
            users = []
            query_parameters = {
                'limit': 100,
            }
            
            for reaction, line in reactions.iter_items():
                if not line.unknown:
                    continue
                
                emoji_value = reaction.emoji.as_reaction
                query_parameters['after'] = 0
                query_parameters['type'] = reaction.type.value
                
                while True:
                    user_datas = await self.api.reaction_user_get_chunk(
                        message.channel_id, message.id, emoji_value, query_parameters
                    )
                    users.extend(User.from_data(user_data) for user_data in user_datas)
                    
                    if len(user_datas) < 100:
                        break
                    
                    query_parameters['after'] = users[-1].id
                
                reactions._fill_all_reactions(reaction, users)
                users.clear()
        
        return message
