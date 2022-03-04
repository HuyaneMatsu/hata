__all__ = ('TopGGClient', )

from scarletio import Future, Task, shield, sleep
from scarletio import IgnoreCaseMultiValueDictionary, LOOP_TIME, WeakReferer, from_json, to_json
from scarletio.http_client import RequestContextManager
from scarletio.web_common.headers import AUTHORIZATION, CONTENT_TYPE, METHOD_GET, METHOD_POST, RETRY_AFTER, USER_AGENT

from ...discord.client import Client
from ...discord.core import KOKORO
from ...discord.http import LIBRARY_USER_AGENT

from .bots_query import create_bots_query_search_value, get_bots_query_sort_by_value
from .constants import (
    JSON_KEY_POST_BOT_STATS_GUILD_COUNT, JSON_KEY_POST_BOT_STATS_SHARD_COUNT, JSON_KEY_POST_BOT_STATS_SHARD_ID,
    JSON_KEY_VOTED, JSON_KEY_WEEKEND_STATUS, QUERY_KEY_GET_BOTS_LIMIT, QUERY_KEY_GET_BOTS_OFFSET,
    QUERY_KEY_GET_BOTS_SEARCH_QUERY, QUERY_KEY_GET_BOTS_SORT_BY, QUERY_KEY_GET_USER_VOTE_USER_ID,
    RATE_LIMIT_BOTS_RESET_AFTER, RATE_LIMIT_BOTS_SIZE, RATE_LIMIT_GLOBAL_DEFAULT_DURATION,
    RATE_LIMIT_GLOBAL_RESET_AFTER, RATE_LIMIT_GLOBAL_SIZE
)
from .exceptions import TopGGGloballyRateLimited, TopGGHttpException
from .rate_limit_handling import RateLimitGroup, RateLimitHandler, StackedRateLimitHandler
from .types import BotInfo, BotsQueryResult, UserInfo


AUTO_POST_INTERVAL = 1800.0
WEEKEND_STATE_UPDATE_INTERVAL = 300.0

TOP_GG_ENDPOINT = 'https://top.gg/api'

async def _start_auto_post(client):
    """
    Client launch event handler starting auto post.
    
    This method is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
    """
    top_gg_client = client.top_gg
    
    # update client is if required
    top_gg_client.client_id = client.id
    
    # Do not post initially, we might not have all the guilds loaded yet.
    if top_gg_client._auto_post_running:
        top_gg_client._auto_post_handler = KOKORO.call_later(
            AUTO_POST_INTERVAL,
            _trigger_auto_post,
            WeakReferer(top_gg_client),
        )


async def _stop_auto_post(client):
    """
    Client disconnect event handler, which stops auto posting.
    
    This method is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
    """
    top_gg_client = client.top_gg
    
    top_gg_client._auto_post_running = False
    
    auto_post_handler = top_gg_client._auto_post_handler
    if (auto_post_handler is not None):
        top_gg_client._auto_post_handler = None
        auto_post_handler.cancel()


def _trigger_auto_post(top_gg_client_reference):
    """
    Triggers an auto post.
    
    Parameters
    ----------
    top_gg_client_reference : ``WeakReferer`` to ``TopGGClient``
        Weak reference to the top.gg client.
    """
    top_gg_client = top_gg_client_reference()
    if (top_gg_client is not None):
        Task(_do_auto_post(top_gg_client, top_gg_client_reference), KOKORO)


async def _do_auto_post(top_gg_client, top_gg_client_reference):
    """
    Does an auto post.
    
    This method is a coroutine.
    
    Parameters
    ----------
    top_gg_client : ``TopGGClient``
        The top.gg client.
    top_gg_client_reference : ``WeakReferer`` to ``TopGGClient``
        Weak reference to the top.gg client.
    
    Raises
    ------
    TopGGHttpException
        Any exception raised by top.gg api.
    """
    try:
        await top_gg_client.post_bot_stats()
    except ConnectionError:
        return
    finally:
        if top_gg_client._auto_post_running:
            top_gg_client._auto_post_handler = KOKORO.call_later(
                AUTO_POST_INTERVAL,
                _trigger_auto_post,
                top_gg_client_reference,
            )


async def get_weekend_status_task(top_gg_client):
    """
    Returns the weekend multiplier is on.
    
    This function is used for synchronizing multiple ``TopGGClient.get_weekend_status`` calls.
    
    This function is a coroutine.
    
    Parameters
    ----------
    top_gg_client : ``TopGGClient``
        The top.gg client to use.
    
    Returns
    -------
    weekend_status : `bool`
    
    Raises
    ------
    ConnectionError
        No internet connection.
    TopGGGloballyRateLimited
        If the client got globally rate limited by top.gg and `raise_on_top_gg_global_rate_limit` was given as
        `True`.
    TopGGHttpException
        Any exception raised by top.gg api.
    """
    try:
        data = await top_gg_client._get_weekend_status()
    finally:
        top_gg_client._weekend_status_request_task = None
    
    return data[JSON_KEY_WEEKEND_STATUS]


class TopGGClient:
    """
    Represents a client connection towards top.gg.
    
    Attributes
    ----------
    _auto_post_handler : `None`, ``TimerHandle``
        Handle to repeat the auto poster.
    _auto_post_running : `bool`
        Whether auto posting is still running.
    _global_rate_limit_expires_at : `float`
        When the global rate limit expires in monotonic time.
    _headers : `IgnoreCaseMultiValueDictionary`
        Request headers.
    _raise_on_top_gg_global_rate_limit : `bool`
        Whether ``TopGGGloballyRateLimited`` should be raised when the client gets globally rate limited.
    _rate_limit_handler_global : ``RateLimitHandler``
        Rate limit handler applied to all rate limits.
    _rate_limit_handler_bots : ``RateLimitHandler``
        Rate limit handler applied to `/bots` endpoints.
    _weekend_status_cache_time : `float`
        When the last ``.get_weekend_status`` was done.
    _weekend_status_cache_value : `bool`
        The response of the last ``get_weekend_status`` call.
    _weekend_status_request_task : `None`, ``Task``
        Synchronization task for requesting weekend status.
    client_id : `int`
        The client's identifier.
    client_reference : ``WeakReferer`` to ``Client``
        Weakreference towards the wrapped bot.
    http : ``DiscordHTTPClient``
        Http client to do requests with.
    top_gg_token : `str`
        Top.gg api token.
    """
    __slots__ = (
        '__weakref__', '_auto_post_handler', '_auto_post_running', '_global_rate_limit_expires_at', '_headers',
        '_raise_on_top_gg_global_rate_limit', '_rate_limit_handler_bots', '_rate_limit_handler_global',
        '_weekend_status_cache_time', '_weekend_status_cache_value', '_weekend_status_request_task', 'client_id',
        'client_reference', 'http', 'top_gg_token'
    )
    
    def __new__(cls, client, top_gg_token, auto_post_bot_stats=True, raise_on_top_gg_global_rate_limit=False):
        """
        Creates a new top.gg client instance.
        
        Parameters
        ----------
        client : ``Client``
            The discord client.
        top_gg_token : `str`
            Top.gg api token.
        auto_post_bot_stats : `bool` = `True`, Optional
            Whether auto post should be started as the client launches up.
        raise_on_top_gg_global_rate_limit : `bool` = `False`, Optional
            Whether ``TopGGGloballyRateLimited`` should be raised when the client gets globally rate limited.
        
        Raises
        ------
        TypeError
            - If `client` is not ``Client``.
            - If `top_gg_token` is not `str`.
            - If `auto_post_bot_stats` is not `bool`.
            - If `raise_on_top_gg_global_rate_limit` is not `bool` isinstance.
        """
        if not isinstance(client, Client):
            raise TypeError(
                f'`client` can be `{Client.__name__}`, got {client.__class__.__name__}; {client!r}.'
            )
        
        if not isinstance(top_gg_token, str):
            raise TypeError(
                f'`top_gg_token` can be `str`, got {top_gg_token.__class__.__name__}; {top_gg_token!r}.'
            )
        
        if not isinstance(auto_post_bot_stats, bool):
            raise TypeError(
                f'`auto_post_bot_stats` can be `bool`, got '
                f'{auto_post_bot_stats.__class__.__name__}; {auto_post_bot_stats!r}.'
            )
        
        if not isinstance(raise_on_top_gg_global_rate_limit, bool):
            raise TypeError(
                f'`raise_on_top_gg_global_rate_limit` can be `bool`, got '
                f'{raise_on_top_gg_global_rate_limit.__class__.__name__}; {raise_on_top_gg_global_rate_limit!r}.'
            )
        
        
        client_reference = WeakReferer(client)
        
        headers = IgnoreCaseMultiValueDictionary()
        headers[USER_AGENT] = LIBRARY_USER_AGENT
        headers[AUTHORIZATION] = top_gg_token
        
        self = object.__new__(cls)
        self.client_reference = client_reference
        self._auto_post_handler = None
        self._auto_post_running = auto_post_bot_stats
        self._raise_on_top_gg_global_rate_limit = raise_on_top_gg_global_rate_limit
        self._headers = headers
        
        self.client_id = client.id
        self.http = client.http
        self.top_gg_token = top_gg_token
        
        self._global_rate_limit_expires_at = 0.0
        self._rate_limit_handler_global = RateLimitGroup(RATE_LIMIT_GLOBAL_SIZE, RATE_LIMIT_GLOBAL_RESET_AFTER)
        self._rate_limit_handler_bots = RateLimitGroup(RATE_LIMIT_BOTS_SIZE, RATE_LIMIT_BOTS_RESET_AFTER)
        
        self._weekend_status_cache_time = 0.0
        self._weekend_status_cache_value = False
        self._weekend_status_request_task = None
        
        return self
    
    
    def __repr__(self):
        """Returns the representation of the top.gg client."""
        repr_parts = ['<', self.__class__.__name__, ' to ' ]
        
        client = self.client_reference()
        if client is None:
            client_name = str(self.client_id)
        else:
            client_name = client.full_name
        
        repr_parts.append(client_name)
        
        if self.is_auto_posting:
            repr_parts.append('(auto-posting)')
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def is_auto_posting(self):
        """
        Returns whether the bot stats are auto posted to top.gg
        
        Returns
        -------
        is_auto_posting : `bool`
        """
        return self._auto_post_running
    
    
    def start_auto_posting(self):
        """
        Starts auto posting bot stats.
        """
        if not self._auto_post_running:
            self._auto_post_running = True
            
            # We can only start it, if our client is running.
            client = self.client_reference()
            if (client is not None) and client.running:
                
                # Check edge case
                auto_post_handler = self._auto_post_handler
                if (auto_post_handler is None):
                    
                    self._auto_post_handler = KOKORO.call_later(
                        AUTO_POST_INTERVAL,
                        _trigger_auto_post,
                        WeakReferer(self),
                    )
    
    def stop_auto_posting(self):
        """
        Stops auto posting bot starts.
        """
        if self._auto_post_running:
            self._auto_post_running = False
            
            auto_post_handler = self._auto_post_handler
            if (auto_post_handler is not None):
                self._auto_post_handler = None
                auto_post_handler.cancel()
    
    
    async def post_bot_stats(self):
        """
        Posts your guild & shard count.
        
        This method is a coroutine.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        TopGGGloballyRateLimited
            If the client got globally rate limited by top.gg and `raise_on_top_gg_global_rate_limit` was given as
            `True`.
        TopGGHttpException
            Any exception raised by top.gg api.
        """
        client = self.client_reference()
        if (client is not None):
            guild_count = len(client.guilds)
            
            shard_count = client.shard_count
            if shard_count < 1:
                shard_count = 1
            
            data = {
                JSON_KEY_POST_BOT_STATS_GUILD_COUNT: guild_count,
                JSON_KEY_POST_BOT_STATS_SHARD_COUNT: shard_count,
                JSON_KEY_POST_BOT_STATS_SHARD_ID: 0,
            }
            
            await self._post_bot_stats(data)
    
    
    async def get_weekend_status(self, *, force_update=False):
        """
        Returns the weekend multiplier is on.
        
        This method is a coroutine.
        
        Parameters
        ----------
        force_update : `bool` = `False`, Optional (Keyword only)
            Whether the weekend status should be forcefully updated instead of using the cached one.
        
        Returns
        -------
        weekend_status : `bool`
        
        Raises
        ------
        ConnectionError
            No internet connection.
        TopGGGloballyRateLimited
            If the client got globally rate limited by top.gg and `raise_on_top_gg_global_rate_limit` was given as
            `True`.
        TopGGHttpException
            Any exception raised by top.gg api.
        """
        if force_update or (self._weekend_status_cache_time < LOOP_TIME()):
            task = self._weekend_status_request_task
            if task is None:
                task = Task(get_weekend_status_task(self), KOKORO)
                self._weekend_status_request_task = task
            
            weekend_status = await shield(task, KOKORO)
        else:
            weekend_status = self._weekend_status_cache_value
        
        return weekend_status
    
    
    async def get_bot_voters(self):
        """
        Returns the last 1000 voters.
        
        This method is a coroutine.
        
        Returns
        -------
        voters : `list` of ``UserInfo``
        
        Raises
        ------
        ConnectionError
            No internet connection.
        TopGGGloballyRateLimited
            If the client got globally rate limited by top.gg and `raise_on_top_gg_global_rate_limit` was given as
            `True`.
        TopGGHttpException
            Any exception raised by top.gg api.
        """
        user_datas = await self._get_bot_voters()
        return [UserInfo.from_data(user_data) for user_data in user_datas]
    
    
    async def get_bot_info(self):
        """
        Returns your bot's information.
        
        This method is a coroutine.
        
        Returns
        -------
        bot_info : ``BotInfo``
        
        Raises
        ------
        ConnectionError
            No internet connection.
        TopGGGloballyRateLimited
            If the client got globally rate limited by top.gg and `raise_on_top_gg_global_rate_limit` was given as
            `True`.
        TopGGHttpException
            Any exception raised by top.gg api.
        """
        data = await self._get_bot_info()
        return BotInfo.from_data(data)
    
    
    async def get_bots(self, *, limit=50, offset=0, sort_by=None, search=None):
        """
        Gets information about multiple bots.
        
        This method is a coroutine.
        
        Parameters
        ----------
        limit : `int` = `50`, Optional (Keyword only)
            The amount of bots to query.
        offset : `int` = `0`, Optional (Keyword only)
            Query offset
        sort_by : `None`, `str` = `None`, Optional (Keyword only)
            Which field to sort by the bots.
        search : `None`, `dict` of (`str`, `Any`) items = `None`, Optional (Keyword only)
            Fields an expected values to search for.
        
        Returns
        -------
        get_bots_result : ``BotsQueryResult``
        
        Raises
        ------
        LookupError
            - If `sort_by` refers to a not existent field.
            - If `search` contains a not existent field.
        ConnectionError
            No internet connection.
        TopGGGloballyRateLimited
            If the client got globally rate limited by top.gg and `raise_on_top_gg_global_rate_limit` was given as
            `True`.
        TopGGHttpException
            Any exception raised by top.gg api.
        
        Keys
        ----
        `sort_by` fields and `search` field's keys might be the following:
        
        - banner_url
        - certified_at
        - discriminator
        - donate_bot_guild_id
        - featured_guild_ids
        - github_url
        - id
        - invite_url
        - is_certified
        - long_description
        - name
        - owner_id
        - owner_ids
        - prefix
        - short_description
        - support_server_invite_url
        - tags
        - upvotes
        - upvotes_monthly
        - vanity_url
        - website_url
        """
        if limit > 500:
            limit = 500
        
        query_sort_by_value = get_bots_query_sort_by_value(sort_by)
        query_search_value = create_bots_query_search_value(search)
        
        query_parameters = {
            QUERY_KEY_GET_BOTS_LIMIT: limit,
            QUERY_KEY_GET_BOTS_OFFSET: offset,
            QUERY_KEY_GET_BOTS_SORT_BY: query_sort_by_value,
            QUERY_KEY_GET_BOTS_SEARCH_QUERY: query_search_value,
            # QUERY_KEY_GET_BOTS_FIELDS: BOTS_QUERY_FIELDS_VALUE, # Defaults to all fields, so we just skip it
        }
        
        data = await self._get_bots(query_parameters)
        return BotsQueryResult.from_data(data)
    
    
    async def get_user_info(self, user_id):
        """
        Gets user info for the given user identifier.
        
        This method is a coroutine.
        
        Parameters
        ----------
        user_id : `int`
            The user's identifier to get.
        
        Returns
        -------
        user_info : ``UserInfo``
        
        Raises
        ------
        ConnectionError
            No internet connection.
        TopGGGloballyRateLimited
            If the client got globally rate limited by top.gg and `raise_on_top_gg_global_rate_limit` was given as
            `True`.
        TopGGHttpException
            Any exception raised by top.gg api.
        """
        data = await self._get_user_info(user_id)
        return UserInfo.from_data(data)
    
    
    async def get_user_vote(self, user_id):
        """
        Returns whether the user voted in the last 12 hours.
        
        This method is a coroutine.
        
        Parameters
        ----------
        user_id : `int`
            The user's identifier.
        
        Returns
        -------
        voted : `bool`
        
        Raises
        ------
        ConnectionError
            No internet connection.
        TopGGGloballyRateLimited
            If the client got globally rate limited by top.gg and `raise_on_top_gg_global_rate_limit` was given as
            `True`.
        TopGGHttpException
            Any exception raised by top.gg api.
        """
        data = await self._get_user_vote({QUERY_KEY_GET_USER_VOTE_USER_ID: user_id})
        return bool(data[JSON_KEY_VOTED])
    
    
    async def _post_bot_stats(self, data):
        """
        Posts bot stats to top.gg.
        
        This method is a coroutine.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Bot stats.
        
        Returns
        -------
        response_data : `Any`
        
        Raises
        ------
        ConnectionError
            No internet connection.
        TopGGGloballyRateLimited
            If the client got globally rate limited by top.gg and `raise_on_top_gg_global_rate_limit` was given as
            `True`.
        TopGGHttpException
            Any exception raised by top.gg api.
        """
        return await self._request(
            METHOD_POST,
            f'{TOP_GG_ENDPOINT}/bots/stats',
            StackedRateLimitHandler(self._rate_limit_handler_bots, self._rate_limit_handler_global),
            data = data,
        )
    
    
    async def _get_weekend_status(self):
        """
        Gets weekend status from top.gg.
        
        This method is a coroutine.
        
        Returns
        -------
        response_data : `Any`
        
        Raises
        ------
        ConnectionError
            No internet connection.
        TopGGGloballyRateLimited
            If the client got globally rate limited by top.gg and `raise_on_top_gg_global_rate_limit` was given as
            `True`.
        TopGGHttpException
            Any exception raised by top.gg api.
        """
        return await self._request(
            METHOD_GET,
            f'{TOP_GG_ENDPOINT}/weekend',
            RateLimitHandler(self._rate_limit_handler_global),
        )
    
    
    async def _get_bot_voters(self):
        """
        Gets the last 1000 voters.
        
        This method is a coroutine.
        
        Returns
        -------
        response_data : `Any`
        
        Raises
        ------
        ConnectionError
            No internet connection.
        TopGGGloballyRateLimited
            If the client got globally rate limited by top.gg and `raise_on_top_gg_global_rate_limit` was given as
            `True`.
        TopGGHttpException
            Any exception raised by top.gg api.
        """
        return await self._request(
            METHOD_GET,
            f'{TOP_GG_ENDPOINT}/bots/{self.client_id}/votes',
            StackedRateLimitHandler(self._rate_limit_handler_bots, self._rate_limit_handler_global),
        )
    
    
    async def _get_bot_info(self):
        """
        Gets bot information and returns it.
        
        This method is a coroutine.
        
        Returns
        -------
        response_data : `Any`
        
        Raises
        ------
        ConnectionError
            No internet connection.
        TopGGGloballyRateLimited
            If the client got globally rate limited by top.gg and `raise_on_top_gg_global_rate_limit` was given as
            `True`.
        TopGGHttpException
            Any exception raised by top.gg api.
        """
        return await self._request(
            METHOD_GET,
            f'{TOP_GG_ENDPOINT}/bots/{self.client_id}',
            StackedRateLimitHandler(self._rate_limit_handler_bots, self._rate_limit_handler_global),
        )
    
    
    async def _get_bots(self, query_parameters):
        """
        Gets information about multiple bots.
        
        This method is a coroutine.
        
        Parameters
        ----------
        query_parameters : `dict` of (`str`, `Any`) items
            Query parameters.
            
        Returns
        -------
        response_data : `Any`
        
        Raises
        ------
        ConnectionError
            No internet connection.
        TopGGGloballyRateLimited
            If the client got globally rate limited by top.gg and `raise_on_top_gg_global_rate_limit` was given as
            `True`.
        TopGGHttpException
            Any exception raised by top.gg api.
        """
        return await self._request(
            METHOD_GET,
            f'{TOP_GG_ENDPOINT}/bots',
            StackedRateLimitHandler(self._rate_limit_handler_bots, self._rate_limit_handler_global),
            query_parameters = query_parameters,
        )
    
    
    async def _get_user_info(self, user_id):
        """
        Gets user info for the given user identifier.
        
        This method is a coroutine.
        
        Parameters
        ----------
        user_id : `int`
            The user's identifier to get.
            
        Returns
        -------
        response_data : `Any`
        
        Raises
        ------
        ConnectionError
            No internet connection.
        TopGGGloballyRateLimited
            If the client got globally rate limited by top.gg and `raise_on_top_gg_global_rate_limit` was given as
            `True`.
        TopGGHttpException
            Any exception raised by top.gg api.
        """
        return await self._request(
            METHOD_GET,
            f'{TOP_GG_ENDPOINT}/users/{user_id}',
            RateLimitHandler(self._rate_limit_handler_global),
        )

    async def _get_user_vote(self, query_parameters):
        """
        Returns whether the user voted in the last 12 hours.
        
        This method is a coroutine.
        
        Parameters
        ----------
        query_parameters : `dict` of (`str`, `Any`) items
            Query parameters.
        
        Returns
        -------
        response_data : `Any`
        
        Raises
        ------
        ConnectionError
            No internet connection.
        TopGGGloballyRateLimited
            If the client got globally rate limited by top.gg and `raise_on_top_gg_global_rate_limit` was given as
            `True`.
        TopGGHttpException
            Any exception raised by top.gg api.
        """
        return await self._request(
            METHOD_GET,
            f'{TOP_GG_ENDPOINT}/bots/{self.client_id}/check',
            RateLimitHandler(self._rate_limit_handler_global),
            query_parameters = query_parameters,
        )
    
    async def _request(self, method, url, rate_limit_handler, data=None, query_parameters=None):
        """
        Does a request towards top.gg API.
        
        This method is a coroutine.
        
        Parameters
        ----------
        method : `str`
            Http method.
        url : `str`
            Endpoint to do request towards.
        rate_limit_handler : ``RateLimitHandlerBase`
            Rate limit handle to handle rate limit as.
        data : `None`, `Any` = `None`, Optional
            Json serializable data.
        query_parameters : `None`, `Any` = `None`, Optional
            Query parameters.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        TopGGGloballyRateLimited
            If the client got globally rate limited by top.gg and `raise_on_top_gg_global_rate_limit` was given as
            `True`.
        TopGGHttpException
            Any exception raised by top.gg api.
        """
        headers = self._headers.copy()
        
        if (data is not None):
            headers[CONTENT_TYPE] = 'application/json'
            data = to_json(data)
        
        try_again = 2
        while try_again > 0:
            global_rate_limit_expires_at = self._global_rate_limit_expires_at
            if global_rate_limit_expires_at > LOOP_TIME():
                if self._raise_on_top_gg_global_rate_limit:
                    raise TopGGGloballyRateLimited(None)
                
                future = Future(KOKORO)
                KOKORO.call_at(global_rate_limit_expires_at, Future.set_result_if_pending, future, None)
                await future
            
            async with rate_limit_handler.ctx():
                try:
                    async with RequestContextManager(
                        self.http._request(method, url, headers, data, query_parameters)
                    ) as response:
                        response_data = await response.text(encoding='utf-8')
                except OSError as err:
                    if not try_again:
                        raise ConnectionError('Invalid address or no connection with Top.gg.') from err
                    
                    await sleep(0.5 / try_again, KOKORO)
                    
                    try_again -= 1
                    continue
                
                response_headers = response.headers
                status = response.status
                
                content_type_headers = response_headers.get(CONTENT_TYPE, None)
                if (content_type_headers is not None) and content_type_headers.startswith('application/json'):
                    response_data = from_json(response_data)
                
                if 199 < status < 305:
                    return response_data
                
                # Are we rate limited?
                if status == 429:
                    try:
                        retry_after = headers[RETRY_AFTER]
                    except KeyError:
                        retry_after = RATE_LIMIT_GLOBAL_DEFAULT_DURATION
                    else:
                        try:
                            retry_after = float(retry_after)
                        except ValueError:
                            retry_after = RATE_LIMIT_GLOBAL_DEFAULT_DURATION
                    
                    self._global_rate_limit_expires_at = LOOP_TIME() + retry_after
                    
                    if self._raise_on_top_gg_global_rate_limit:
                        raise TopGGGloballyRateLimited(None)
                        
                    await sleep(retry_after, KOKORO)
                    continue
                
                
                # Python casts sets to frozensets
                if (status in {400, 401, 402, 404}):
                    raise TopGGHttpException(response, response_data)
                
                if try_again and (status >= 500):
                    await sleep(10.0 / try_again, KOKORO)
                    try_again -= 1
                    continue
                
                raise TopGGHttpException(response, response_data)
