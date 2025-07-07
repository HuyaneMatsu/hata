__all__ = ()

from scarletio import Compound, Theory

from ...http import DiscordApiClient
from ...user import ClientUserBase, User
from ...utils import log_time_converter

from ..request_helpers import (
    get_channel_id_and_message_id, get_message_and_channel_id_and_message_id, get_poll_answer_and_id
)


POLL_RESULT_USER_GET_CHUNK_LIMIT_MIN = 1
POLL_RESULT_USER_GET_CHUNK_LIMIT_MAX = 100


class ClientCompoundPollEndpoints(Compound):
    
    api : DiscordApiClient
    
    @Theory
    async def message_get(self, message, *, force_update = False): ...
    
    
    async def poll_result_user_get_chunk(self, message, poll_answer, *, limit = ..., after = ...):
        """
        Requests the users, who voted on the given message with the given answer.
        
        If the message has no poll or has no answers for that answer returns empty list. If we know every voters for
        the given answers it will pull them from the cache.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message : ``Message``, `tuple` (`int`, `int`)
            The message whats voters should be requested.
        poll_answer : ``PollAnswer``, `int`
            The poll answer to request the users for.
        limit : `None | int`, Optional (Keyword only)
            The amount of users to request. Can be in range [1:100].
        after : ``None | int | DiscordEntity | DateTime``, Optional (Keyword only)
            The timestamp after the voters were created.
        
        Returns
        -------
        users : ``list<ClientUserBase>``
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        `before` parameter is not supported by Discord.
        """
        if limit is ...:
            limit = POLL_RESULT_USER_GET_CHUNK_LIMIT_MAX
        
        elif isinstance(limit, int):
            if limit < POLL_RESULT_USER_GET_CHUNK_LIMIT_MIN:
                limit = POLL_RESULT_USER_GET_CHUNK_LIMIT_MIN
            elif limit > POLL_RESULT_USER_GET_CHUNK_LIMIT_MAX:
                limit = POLL_RESULT_USER_GET_CHUNK_LIMIT_MAX
        
        else:
            raise TypeError(
                f'`limit` can be `None | int`, got {type(limit).__name__}; {limit!r}.'
            )
        
        message, channel_id, message_id = get_message_and_channel_id_and_message_id(message)
        poll_answer, poll_answer_id = get_poll_answer_and_id(poll_answer)
        if not poll_answer_id:
            if message is None:
                message = await self.message_get((channel_id, message_id),)
            
            poll = message.poll
            if poll is None:
                return []
            
            poll_answer_id = poll.get_answer_id(poll_answer)
            if not poll_answer_id:
                return []
        
        if (message is not None):
            poll = message.poll
            if poll is None:
                return []
            
            result = poll[poll_answer_id]
            if result is None:
                return []
            
            if not result.unknown:
                after = 0 if after is ... else log_time_converter(after)
                # before = 9223372036854775807 if before is ... else log_time_converter(before)
                return result.filter_after(limit, after)
        
        
        query_parameters = {
            'limit': limit,
        }
        
        if (after is not ...):
            query_parameters['after'] = log_time_converter(after)
        
        # Before is not supported!
        # if (before is not ...):
        #     data['before'] = log_time_converter(before)
        
        data = await self.api.poll_result_user_get_chunk(
            channel_id, message_id, poll_answer_id, query_parameters
        )
        
        user_datas = data.get('users', None)
        if user_datas is None:
            users = []
        else:
            users = [User.from_data(user_data) for user_data in user_datas]
        
        if (message is not None):
            poll = message.poll
            if (poll is not None):
                poll._fill_some_votes(poll_answer_id, users)
        
        return users
    
    
    async def poll_result_user_get_all(self, message, poll_answer):
        """
        Requests the all the voters for the given answer.
        
        If all the voters are known for the given answer, they are queried from the cache instead.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message : ``Message``, `tuple` (`int`, `int`)
            The message whats voters should be requested.
        poll_answer : ``PollAnswer``, `int`
            The poll answer to request the users for.
        
        Returns
        -------
        users : ``list<ClientUserBase>``
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        message, channel_id, message_id = get_message_and_channel_id_and_message_id(message)
        poll_answer, poll_answer_id = get_poll_answer_and_id(poll_answer)
        
        if not poll_answer_id:
            if message is None:
                message = await self.message_get((channel_id, message_id),)
            
            poll = message.poll
            if poll is None:
                return []
            
            poll_answer_id = poll.get_answer_id(poll_answer)
            if not poll_answer_id:
                return []
        
        if (message is not None):
            poll = message.poll
            if poll is None:
                return []
            
            result = poll[poll_answer_id]
            if result is None:
                return []
            
            if not result.unknown:
                return sorted(result)
        
        query_parameters = {
            'after': 0,
            'limit': POLL_RESULT_USER_GET_CHUNK_LIMIT_MAX,
        }
        
        users = []
        
        while True:
            data = await self.api.poll_result_user_get_chunk(
                channel_id, message_id, poll_answer_id, query_parameters
            )
            user_datas = data.get('users', None)
            if (user_datas is not None):
                for user_data in user_datas:
                    users.append(User.from_data(user_data))
            
            if (user_datas is None) or (len(user_datas) < POLL_RESULT_USER_GET_CHUNK_LIMIT_MAX):
                break
            
            query_parameters['after'] = users[-1].id
        
        if (message is not None):
            poll = message.poll
            if (poll is not None):
                poll._fill_all_votes(poll_answer_id, users)
        
        return users
    
    
    async def poll_result_get_all(self, message):
        """
        Requests all the voters for every answer on the given message.
        
        Like the other poll voter getting methods, this method prefers using the internal cache as well over doing a
        request.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message : ``Message``, `tuple` (`int`, `int`)
            The message, what's voters should be requested.
        
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
        
        # Get poll
        poll = message.poll
        if (poll is not None):
            users = []
            query_parameters = {
                'limit': POLL_RESULT_USER_GET_CHUNK_LIMIT_MAX,
            }
            
            for answer, result in poll.iter_items():
                if not result.unknown:
                    continue
                
                query_parameters['after'] = 0
                
                while True:
                    data = await self.api.poll_result_user_get_chunk(
                        message.channel_id, message.id, answer.id, query_parameters
                    )
                    
                    user_datas = data.get('users', None)
                    if user_datas is not None:                    
                        for user_data in user_datas:
                            users.append(User.from_data(user_data))
                    
                    if (user_datas is None) or (len(user_datas) < POLL_RESULT_USER_GET_CHUNK_LIMIT_MAX):
                        break
                    
                    query_parameters['after'] = users[-1].id
                
                result._fill_all_votes(users)
                users.clear()
        
        return message
    
    
    async def poll_finalize(self, message):
        """
        Finalizes the poll on the given message.

        This method is a coroutine.
        
        Parameters
        ----------
        message : ``Message``, `tuple` (`int`, `int`)
            The message, to finalize the poll on it.
        
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
        await self.api.poll_finalize(channel_id, message_id)
