__all__ = ('DiscordApiClient',)

from scarletio import (
    CauseGroup, Future, IgnoreCaseMultiValueDictionary, LOOP_TIME, RichAttributeErrorBaseType, WeakMap, from_json,
    sleep, to_json
)
from scarletio.http_client import HTTPClient, RequestContextManager
from scarletio.web_common import FormData, quote
from scarletio.web_common.headers import CONTENT_TYPE, METHOD_DELETE, METHOD_GET, METHOD_PATCH, METHOD_POST, METHOD_PUT

from ..core import KOKORO
from ..exceptions import DiscordException

from . import rate_limit_groups as RATE_LIMIT_GROUPS
from .connector_cache import get_connector
from .headers import AUDIT_LOG_REASON, build_headers
from .rate_limit import NO_SPECIFIC_RATE_LIMITER, RateLimitHandler, StackedStaticRateLimitHandler
from .urls import API_ENDPOINT, STATUS_ENDPOINT


NON_JSON_TYPES = (FormData, bytes, type(None))

REQUEST_RETRY_LIMIT = 5


class DiscordApiClient(RichAttributeErrorBaseType):
    """
    Discord api client that adds http information to requests.
    
    Also can be mocked when testing.
    
    Attributes
    ----------
    debug_options : `None | set<str>`
        Debug options used when requesting towards Discord.
    http : ``HTTPClient``
        The used http client.
    global_rate_limit_expires_at : `float`
        The time when global rate limit will expire in monotonic time.
    handlers : `WeakMap<RateLimitHandler>`
        Rate limit handlers of the Discord requests.
    headers : ``IgnoreCaseMultiValueDictionary``
        Headers used by every every Discord request.
    """
    __slots__ = ('debug_options', 'http', 'global_rate_limit_expires_at', 'handlers', 'headers')
    
    def __new__(cls, bot, token, *, debug_options = None, http = None):
        """
        Creates a new Discord api client.
        
        Parameters
        ----------
        bot : `bool`
            Whether the respective client is a bot.
        token : `str`
            The client's token.
        
        debug_options: `None | set<str>` = `None`, Optional (Keyword only)
            Http debug options, like `'canary'` (I don't know more either).
        
        http : `None | HTTPClient`` = `None`, Optional (Keyword only)
            The http client to use instead of creating a new one.
        """
        connector = get_connector()
        headers = build_headers(bot, token, debug_options)
        
        if http is None:
            http = HTTPClient(KOKORO, connector = connector)
        
        self = object.__new__(cls)
        self.debug_options = debug_options
        self.http = http
        self.global_rate_limit_expires_at = 0.0
        self.handlers = WeakMap()
        self.headers = headers
        return self
    
    
    async def discord_request(self, handler, method, url, data = None, params = None, headers = None, reason = None):
        """
        Does a request towards Discord.
        
        This method is a coroutine.
        
        Parameters
        ----------
        handler : ``RateLimitHandler``, ``StackedStaticRateLimitHandler``
            Rate limit handler for the request.
        method : `str`
            The method of the request.
        url : `str`
            The url to request.
        data : `None`, `object` = `None`, Optional
            Payload to request with.
        params : `None`, `object` = `None`, Optional
            Query parameters.
        headers : `None`, ``IgnoreCaseMultiValueDictionary`` = `None`, Optional
            Headers to do the request with. If passed then the session's own headers wont be used.
        reason : `None`, `str` = `None`, Optional
            Shows up at the request's respective guild if applicable.
        
        Returns
        -------
        response_data : `object`
        
        Raises
        ------
        TypeError
            `data`, `params` type is bad, or they contain object(s) with bad type.
        ConnectionError
            No internet connection.
        DiscordException
            Any exception raised by the Discord API.
        """
        if headers is None:
            # normal request
            headers = self.headers.copy()
            
            if not isinstance(data, NON_JSON_TYPES):
                headers[CONTENT_TYPE] = 'application/json'
                data = to_json(data)
            
            if (reason is not None):
                headers[AUDIT_LOG_REASON] = quote(reason, safe = '\\ ')
        else:
            # bearer or webhook request
            if (CONTENT_TYPE not in headers) and (not isinstance(data, NON_JSON_TYPES)):
                headers[CONTENT_TYPE] = 'application/json'
                data = to_json(data)
        
        if not handler.is_unlimited():
            handler = self.handlers.set(handler)
        
        causes = None
        
        while True:
            global_rate_limit_expires_at = self.global_rate_limit_expires_at
            if global_rate_limit_expires_at > LOOP_TIME():
                future = Future(KOKORO)
                KOKORO.call_at(global_rate_limit_expires_at, Future.set_result_if_pending, future, None)
                await future
            
            await handler.enter()
            with handler.ctx() as lock:
                try:
                    async with RequestContextManager(
                        self.http._request(method, url, headers, data = data, params = params)
                    ) as response:
                        response_data = await response.text(encoding = 'utf-8')
                except OSError as err:
                    if causes is None:
                        causes = []
                    
                    causes.append(err)
                    
                    if len(causes) >= REQUEST_RETRY_LIMIT:
                        try:
                            raise ConnectionError(
                                'Invalid address or no connection with Discord.'
                            ) from CauseGroup(*causes)
                        finally:
                            causes = None
                    
                    # os can not handle more, need to wait for the blocking job to be done. This can happen on Windows.
                    await sleep(0.1 * len(causes), KOKORO)
                    # Invalid address causes OSError too, but we will let it run 5 times, then raise a ConnectionError
                    continue
                
                response_headers = response.headers
                status = response.status
                
                content_type_headers = response_headers.get(CONTENT_TYPE, None)
                if (content_type_headers is not None) and content_type_headers.startswith('application/json'):
                    response_data = from_json(response_data)
                
                if 199 < status < 305:
                    lock.exit(response_headers)
                    return response_data
                
                if status == 429:
                    if 'code' in response_data: # Can happen at the case of rate limit ban
                        try:
                            raise DiscordException(
                                response, response_data, data, self.debug_options
                            ) from (None if causes is None else CauseGroup(*causes))
                        finally:
                            causes = None
                    
                    retry_after = response_data.get('retry_after', 0.0)
                    if response_data.get('global', False):
                        global_rate_limit_expires_at = LOOP_TIME() + retry_after
                        self.global_rate_limit_expires_at = global_rate_limit_expires_at
                        future = Future(KOKORO)
                        KOKORO.call_at(global_rate_limit_expires_at, Future.set_result_if_pending, future, None)
                        await future
                    else:
                        await sleep(retry_after, KOKORO)
                    continue
                
                if ((causes is None) or (len(causes) < REQUEST_RETRY_LIMIT)) and (status in (500, 502, 503)):
                    if causes is None:
                        causes = []
                    causes.append(DiscordException(response, response_data, None, None))
                    
                    await sleep(2.0 * len(causes), KOKORO)
                    continue
                
                lock.exit(response_headers)
                
                try:
                    raise DiscordException(
                        response, response_data, data, self.debug_options
                    ) from (None if causes is None else CauseGroup(*causes))
                finally:
                    causes = None

    # client
    
    async def client_edit(self, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.client_edit, NO_SPECIFIC_RATE_LIMITER),
            METHOD_PATCH,
            f'{API_ENDPOINT}/users/@me',
            data,
        )
    
    # `client_guild_profile_nick_edit` is deprecated, use `client_guild_profile_edit` instead.
    async def client_guild_profile_nick_edit(self, guild_id, data, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.client_guild_profile_nick_edit, guild_id),
            METHOD_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/members/@me/nick',
            data,
            reason = reason,
        )
    
    
    async def client_guild_profile_edit(self, guild_id, data, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.client_guild_profile_edit, guild_id),
            METHOD_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/members/@me',
            data,
            reason = reason,
        )
    
    
    async def client_user_get(self):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.client_user_get, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/users/@me',
        )
    
    # hooman only
    async def client_settings_get(self):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.client_settings_get, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/users/@me/settings',
        )
    
    # hooman only
    async def client_settings_edit(self, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.client_settings_edit, NO_SPECIFIC_RATE_LIMITER),
            METHOD_PATCH,
            f'{API_ENDPOINT}/users/@me/settings',
            data,
        )
    
    # hooman only
    async def client_logout(self):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.client_logout, NO_SPECIFIC_RATE_LIMITER),
            METHOD_POST,
            f'{API_ENDPOINT}/auth/logout',
        )
    
    
    async def guild_get_chunk(self, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.guild_get_chunk, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/users/@me/guilds',
            params = data,
        )
    
    
    async def channel_private_get_all(self):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.channel_private_get_all, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/users/@me/channels'
        )
    
    # hooman only
    async def client_gateway_hooman(self):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.client_gateway_hooman, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/gateway',
        )
    
    # bot only
    async def client_gateway_bot(self):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.client_gateway_bot, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/gateway/bot',
        )
    
    # bot only
    async def oauth2_application_get_own(self):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.oauth2_application_get_own, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/oauth2/applications/@me',
        )
    
    
    async def application_get_own(self):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.application_get_own, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/applications/@me',
        )
    
    
    async def application_edit_own(self, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.application_edit_own, NO_SPECIFIC_RATE_LIMITER),
            METHOD_PATCH,
            f'{API_ENDPOINT}/applications/@me',
            data,
        )
    
    
    async def client_connection_get_all(self):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.client_connection_get_all, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/users/@me/connections',
        )
    
    # oauth2
    
    async def oauth2_token(self, data, headers): # UNLIMITED
        headers[CONTENT_TYPE] = 'application/x-www-form-urlencoded'
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.oauth2_token, NO_SPECIFIC_RATE_LIMITER),
            METHOD_POST,
            f'{API_ENDPOINT}/oauth2/token',
            data,
            headers = headers,
        )
    
    
    async def user_info_get(self, headers):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.user_info_get, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/users/@me',
            headers = headers,
        )
    
    
    async def user_connection_get_all(self, headers):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.user_connection_get_all, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/users/@me/connections',
            headers = headers,
        )
    
    
    async def guild_user_add(self, guild_id, user_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.guild_user_add, guild_id),
            METHOD_PUT,
            f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}',
            data,
        )
    
    
    async def user_guild_get_all(self, headers):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.user_guild_get_all, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/users/@me/guilds',
            headers = headers,
        )
    
    
    async def user_application_role_connection_get(self, application_id, headers):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.user_application_role_connection_get, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/users/@me/applications/{application_id}/role-connection',
            headers = headers,
        )
    
    
    async def user_application_role_connection_edit(self, application_id, data, headers):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.user_application_role_connection_edit, NO_SPECIFIC_RATE_LIMITER),
            METHOD_PUT,
            f'{API_ENDPOINT}/users/@me/applications/{application_id}/role-connection',
            data,
            headers = headers,
        )
    
    # channel
    async def channel_private_create(self, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.channel_private_create, NO_SPECIFIC_RATE_LIMITER),
            METHOD_POST,
            f'{API_ENDPOINT}/users/@me/channels',
            data,
        )
    
    
    async def channel_group_create(self, user_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.channel_group_create, NO_SPECIFIC_RATE_LIMITER),
            METHOD_POST,
            f'{API_ENDPOINT}/users/{user_id}/channels',
            data,
        )
    
    
    async def channel_group_leave(self, channel_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.channel_group_leave, channel_id),
            METHOD_DELETE,
            f'{API_ENDPOINT}/channels/{channel_id}'
        )
    
    
    async def channel_group_user_get_all(self, channel_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.channel_group_user_add, channel_id),
            METHOD_GET,
            f'{API_ENDPOINT}/channels/{channel_id}/recipients',
        )
    
    
    async def channel_group_user_add(self, channel_id, user_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.channel_group_user_add, channel_id),
            METHOD_PUT,
            f'{API_ENDPOINT}/channels/{channel_id}/recipients/{user_id}',
        )
    
    
    async def channel_group_user_delete(self, channel_id, user_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.channel_group_user_delete, channel_id),
            METHOD_DELETE,
            f'{API_ENDPOINT}/channels/{channel_id}/recipients/{user_id}',
        )
    
    
    async def channel_group_edit(self, channel_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.channel_group_edit, channel_id),
            METHOD_PATCH,
            f'{API_ENDPOINT}/channels/{channel_id}',
            data,
        )
    
    
    async def channel_move(self, guild_id, data, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.channel_move, guild_id),
            METHOD_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/channels',
            data,
            reason = reason,
        )
    
    
    async def channel_edit(self, channel_id, data, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.channel_edit, channel_id),
            METHOD_PATCH,
            f'{API_ENDPOINT}/channels/{channel_id}',
            data,
            reason = reason,
        )
    
    
    async def channel_edit_status(self, channel_id, data, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.channel_edit, channel_id),
            METHOD_PUT,
            f'{API_ENDPOINT}/channels/{channel_id}/voice-status',
            data,
            reason = reason,
        )
    
    
    async def channel_create(self, guild_id, data, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.channel_create, guild_id),
            METHOD_POST,
            f'{API_ENDPOINT}/guilds/{guild_id}/channels',
            data,
            reason = reason,
        )
    
    
    async def channel_delete(self, channel_id, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.channel_delete, channel_id),
            METHOD_DELETE,
            f'{API_ENDPOINT}/channels/{channel_id}',
            reason = reason,
        )
    
    
    async def channel_follow(self, channel_id, data, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.channel_follow, channel_id),
            METHOD_POST,
            f'{API_ENDPOINT}/channels/{channel_id}/followers',
            data,
            reason = reason,
        )
    
    
    async def permission_overwrite_create(self, channel_id, overwrite_id, data, reason ):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.permission_overwrite_create, channel_id),
            METHOD_PUT,
            f'{API_ENDPOINT}/channels/{channel_id}/permissions/{overwrite_id}',
            data,
            reason = reason,
        )
    
    
    async def permission_overwrite_delete(self, channel_id, overwrite_id, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.permission_overwrite_delete, channel_id),
            METHOD_DELETE,
            f'{API_ENDPOINT}/channels/{channel_id}/permissions/{overwrite_id}',
            reason = reason,
        )
    
    # messages
    
    # hooman only
    async def message_ack(self, channel_id, message_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.message_ack, channel_id),
            METHOD_POST,
            f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/ack',
            data,
        )
    
    
    async def message_get(self, channel_id, message_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.message_get, channel_id),
            METHOD_GET,
            f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}',
        )
    
    
    async def message_get_chunk(self, channel_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.message_get_chunk, channel_id),
            METHOD_GET,
            f'{API_ENDPOINT}/channels/{channel_id}/messages',
            params = data,
        )
    
    
    async def message_create(self, channel_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.message_create, channel_id),
            METHOD_POST,
            f'{API_ENDPOINT}/channels/{channel_id}/messages',
            data,
        )
    
    
    async def message_delete(self, channel_id, message_id, reason):
        return await self.discord_request(
            StackedStaticRateLimitHandler(RATE_LIMIT_GROUPS.static_message_delete, channel_id),
            METHOD_DELETE,
            f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}',
            reason = reason,
        )
    
    # after 2 week else & not own
    async def message_delete_b2wo(self, channel_id, message_id, reason):
        return await self.discord_request(
            StackedStaticRateLimitHandler(RATE_LIMIT_GROUPS.static_message_delete_b2wo, channel_id),
            METHOD_DELETE,
            f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}',
            reason = reason,
        )
    
    
    async def message_delete_multiple(self, channel_id, data, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.message_delete_multiple, channel_id),
            METHOD_POST,
            f'{API_ENDPOINT}/channels/{channel_id}/messages/bulk-delete',
            data,
            reason = reason,
        )
    
    
    async def message_edit(self, channel_id, message_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.message_edit, channel_id),
            METHOD_PATCH,
            f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}',
            data,
        )
    
    
    async def message_suppress_embeds(self, channel_id, message_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.message_suppress_embeds, channel_id),
            METHOD_POST,
            f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/suppress-embeds',
            data,
        )
    
    
    async def message_crosspost(self, channel_id, message_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.message_crosspost, channel_id),
            METHOD_POST,
            f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/crosspost',
        )
    
    
    async def message_pin(self, channel_id, message_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.message_pin, channel_id),
            METHOD_PUT,
            f'{API_ENDPOINT}/channels/{channel_id}/pins/{message_id}',
        )
    
    
    async def message_unpin(self, channel_id, message_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.message_unpin, channel_id),
            METHOD_DELETE,
            f'{API_ENDPOINT}/channels/{channel_id}/pins/{message_id}',
        )
    
    
    async def channel_pin_get_all(self, channel_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.channel_pin_get_all, channel_id),
            METHOD_GET,
            f'{API_ENDPOINT}/channels/{channel_id}/pins',
        )
    
    # hooman only
    async def channel_pin_ack(self, channel_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.channel_pin_ack, channel_id),
            METHOD_POST,
            f'{API_ENDPOINT}/channels/{channel_id}/pins/ack',
        )
    
    # poll
    
    async def poll_finalize(self, channel_id, message_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.poll_finalize, NO_SPECIFIC_RATE_LIMITER),
            METHOD_POST,
            f'{API_ENDPOINT}/channels/{channel_id}/polls/{message_id}/expire',
        )
    
    async def poll_result_user_get_chunk(self, channel_id, message_id, answer_id, query_parameters):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.poll_result_user_get_chunk, message_id),
            METHOD_GET,
            f'{API_ENDPOINT}/channels/{channel_id}/polls/{message_id}/answers/{answer_id}',
            params = query_parameters,
        )
    
    # channel directory
    
    async def channel_directory_search(self, channel_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.channel_directory_search, channel_id),
            METHOD_GET,
            f'{API_ENDPOINT}/channels/{channel_id}/directory-entries/search',
            data,
        )
    
    
    async def channel_directory_counts(self, channel_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.channel_directory_counts, channel_id),
            METHOD_GET,
            f'{API_ENDPOINT}/channels/{channel_id}/directory-entries/counts',
        )
    
    
    async def channel_directory_get_all(self, channel_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.channel_directory_get_all, channel_id),
            METHOD_GET,
            f'{API_ENDPOINT}/channels/{channel_id}/directory-entries/list',
        )
    
    # forum tag
    
    async def forum_tag_create(self, channel_id, data, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.forum_tag_create, channel_id),
            METHOD_POST,
            f'{API_ENDPOINT}/channels/{channel_id}/tags',
            data,
            reason = reason,
        )
    
    
    async def forum_tag_edit(self, channel_id, forum_tag_id, data, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.forum_tag_edit, channel_id),
            METHOD_PUT,
            f'{API_ENDPOINT}/channels/{channel_id}/tags/{forum_tag_id}',
            data,
            reason = reason,
        )
    
    
    async def forum_tag_delete(self, channel_id, forum_tag_id, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.forum_tag_delete, channel_id),
            METHOD_DELETE,
            f'{API_ENDPOINT}/channels/{channel_id}/tags/{forum_tag_id}',
            reason = reason,
        )
    
    # typing
    
    async def typing(self, channel_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.typing, channel_id),
            METHOD_POST,
            f'{API_ENDPOINT}/channels/{channel_id}/typing',
        )
    
    # reactions
    
    async def reaction_add(self, channel_id, message_id, reaction, query_parameters):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.reaction_add, channel_id),
            METHOD_PUT,
            f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/reactions/{reaction}/@me',
            params = query_parameters,
        )
    
    
    async def reaction_delete(self, channel_id, message_id, reaction, reaction_type, user_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.reaction_delete, channel_id),
            METHOD_DELETE,
            f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/reactions/{reaction}/{reaction_type}/{user_id}',
        )
    
    
    async def reaction_delete_emoji(self, channel_id, message_id, reaction):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.reaction_delete_emoji, channel_id),
            METHOD_DELETE,
            f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/reactions/{reaction}',
        )
    
    
    async def reaction_delete_own(self, channel_id, message_id, reaction, reaction_type):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.reaction_delete_own, channel_id),
            METHOD_DELETE,
            f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/reactions/{reaction}/{reaction_type}/@me',
        )
    
    
    async def reaction_clear(self, channel_id, message_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.reaction_clear, channel_id),
            METHOD_DELETE,
            f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/reactions',
        )
    
    
    async def reaction_user_get_chunk(self, channel_id, message_id, reaction, query_parameters):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.reaction_user_get_chunk, channel_id),
            METHOD_GET,
            f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/reactions/{reaction}',
            params = query_parameters,
        )
    
    # guild
    
    async def guild_get(self, guild_id, params):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.guild_get, guild_id),
            METHOD_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}',
            params = params,
        )
    
    
    async def guild_preview_get(self, guild_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.guild_preview_get, guild_id),
            METHOD_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/preview',
        )
    
    
    async def guild_user_delete(self, guild_id, user_id, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.guild_user_delete, NO_SPECIFIC_RATE_LIMITER),
            METHOD_DELETE,
            f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}',
            reason = reason,
        )
    
    
    async def guild_ban_add(self, guild_id, user_id, data, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.guild_ban_add, NO_SPECIFIC_RATE_LIMITER),
            METHOD_PUT,
            f'{API_ENDPOINT}/guilds/{guild_id}/bans/{user_id}',
            data,
            reason = reason,
        )
    
    
    async def guild_ban_add_multiple(self, guild_id, data, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.guild_ban_add_multiple, NO_SPECIFIC_RATE_LIMITER),
            METHOD_POST,
            f'{API_ENDPOINT}/guilds/{guild_id}/bulk-ban',
            data,
            reason = reason,
        )
    
    
    async def guild_ban_delete(self, guild_id, user_id, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.guild_ban_delete, NO_SPECIFIC_RATE_LIMITER),
            METHOD_DELETE,
            f'{API_ENDPOINT}/guilds/{guild_id}/bans/{user_id}',
            reason = reason,
        )
    
    
    async def user_guild_profile_edit(self, guild_id, user_id, data, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.user_guild_profile_edit, guild_id),
            METHOD_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}',
            data,
            reason = reason,
        )
    
    
    async def guild_discovery_get(self, guild_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.guild_discovery_get, guild_id),
            METHOD_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/discovery-metadata',
        )
    
    
    async def guild_discovery_edit(self, guild_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.guild_discovery_edit, guild_id),
            METHOD_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/discovery-metadata',
            data,
        )
    
    
    async def guild_discovery_add_sub_category(self, guild_id, category_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.guild_discovery_add_sub_category, guild_id),
            METHOD_PUT,
            f'{API_ENDPOINT}/guilds/{guild_id}/discovery-categories/{category_id}'
        )
    
    
    async def guild_discovery_delete_sub_category(self, guild_id, category_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.guild_discovery_delete_sub_category, guild_id),
            METHOD_DELETE,
            f'{API_ENDPOINT}/guilds/{guild_id}/discovery-categories/{category_id}',
        )
    
    # hooman only
    async def guild_ack(self, guild_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.guild_ack, guild_id),
            METHOD_POST,
            f'{API_ENDPOINT}/guilds/{guild_id}/ack',
            data,
        )
    
    
    async def guild_leave(self, guild_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.guild_leave, guild_id),
            METHOD_DELETE,
            f'{API_ENDPOINT}/users/@me/guilds/{guild_id}',
        )
    
    
    async def guild_delete(self, guild_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.guild_delete, guild_id),
            METHOD_DELETE,
            f'{API_ENDPOINT}/guilds/{guild_id}',
        )
    
    
    async def guild_create(self, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.guild_create, NO_SPECIFIC_RATE_LIMITER),
            METHOD_POST,
            f'{API_ENDPOINT}/guilds',
            data,
        )
    
    
    async def guild_prune(self, guild_id, data, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.guild_prune, guild_id),
            METHOD_POST,
            f'{API_ENDPOINT}/guilds/{guild_id}/prune', params = data,
            reason = reason,
        )
    
    
    async def guild_prune_estimate(self, guild_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.guild_prune_estimate, guild_id),
            METHOD_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/prune',
            params = data,
        )
    
    
    async def guild_edit(self, guild_id, data, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.guild_edit, guild_id),
            METHOD_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}',
            data,
            reason = reason,
        )
    
    
    async def guild_ban_get_chunk(self, guild_id, query_parameters):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.guild_ban_get_chunk, guild_id),
            METHOD_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/bans',
            params = query_parameters,
        )
    
    
    async def guild_ban_get(self, guild_id, user_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.guild_ban_get, guild_id),
            METHOD_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/bans/{user_id}',
        )
    
    
    async def invite_get_vanity(self, guild_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.invite_get_vanity, guild_id),
            METHOD_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/vanity-url',
        )
    
    
    async def invite_edit_vanity(self, guild_id, data, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.invite_edit_vanity, guild_id),
            METHOD_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/vanity-url',
            data,
            reason = reason,
        )
    
    
    async def audit_log_get_chunk(self, guild_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.audit_log_get_chunk, guild_id),
            METHOD_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/audit-logs',
            params = data,
        )
    
    
    async def user_role_add(self, guild_id, user_id, role_id, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.user_role_add, guild_id),
            METHOD_PUT,
            f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}/roles/{role_id}',
            reason = reason,
        )
    
    
    async def user_role_delete(self, guild_id, user_id, role_id, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.user_role_delete, guild_id),
            METHOD_DELETE,
            f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}/roles/{role_id}',
            reason = reason,
        )
    
    
    async def user_move(self, guild_id, user_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.user_move, guild_id),
            METHOD_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}',
            data,
        )
    
    
    async def guild_incidents_edit(self, guild_id, data, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.guild_incidents_edit, guild_id),
            METHOD_PUT,
            f'{API_ENDPOINT}/guilds/{guild_id}/incident-actions',
            data,
            reason = reason,
        )
    
    
    async def integration_get_all(self, guild_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.integration_get_all, guild_id),
            METHOD_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/integrations',
            params = data,
        )
    
    
    async def integration_create(self, guild_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.integration_create, guild_id),
            METHOD_POST,
            f'{API_ENDPOINT}/guilds/{guild_id}/integrations',
            data,
        )
    
    
    async def integration_edit(self, guild_id, integration_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.integration_edit, guild_id),
            METHOD_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/integrations/{integration_id}',
            data,
        )
    
    
    async def integration_delete(self, guild_id, integration_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.integration_delete, guild_id),
            METHOD_DELETE,
            f'{API_ENDPOINT}/guilds/{guild_id}/integrations/{integration_id}',
        )
    
    
    async def integration_sync(self, guild_id, integration_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.integration_sync, guild_id),
            METHOD_POST,
            f'{API_ENDPOINT}/guilds/{guild_id}/integrations/{integration_id}/sync',
        )
    
    
    async def guild_inventory_settings_edit(self, guild_id, data, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.guild_inventory_settings_edit, guild_id),
            METHOD_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/inventory/settings',
            data,
            reason = reason,
        )
    
    
    async def guild_embed_get(self, guild_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.guild_embed_get, guild_id),
            METHOD_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/embed',
        )
    
    
    async def guild_embed_edit(self, guild_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.guild_embed_edit, guild_id),
            METHOD_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/embed',
            data,
        )
    
    
    async def guild_widget_get(self, guild_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.guild_widget_get, guild_id),
            METHOD_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/widget.json',
            headers = IgnoreCaseMultiValueDictionary(),
        )
    
    
    async def guild_user_get_chunk(self, guild_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.guild_user_get_chunk, guild_id),
            METHOD_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/members',
            params = data,
        )
    
    
    async def guild_voice_region_get_all(self, guild_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.guild_voice_region_get_all, guild_id),
            METHOD_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/regions',
        )
    
    
    async def guild_channel_get_all(self, guild_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.guild_channel_get_all, guild_id),
            METHOD_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/channels'
        )
    
    
    async def guild_role_get_all(self, guild_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.guild_role_get_all, guild_id),
            METHOD_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/roles',
        )
    
    
    async def welcome_screen_get(self, guild_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.welcome_screen_get, guild_id),
            METHOD_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/welcome-screen',
        )
    
    
    async def welcome_screen_edit(self, guild_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.welcome_screen_edit, guild_id),
            METHOD_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/welcome-screen',
            data,
        )
    
    
    async def verification_screen_get(self, guild_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.verification_screen_get, guild_id),
            METHOD_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/member-verification',
        )
    
    
    async def verification_screen_edit(self, guild_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.verification_screen_edit, guild_id),
            METHOD_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/member-verification',
            data,
        )
    
    
    async def onboarding_screen_get(self, guild_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.onboarding_screen_get, guild_id),
            METHOD_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/onboarding',
        )
    
    
    async def onboarding_screen_edit(self, guild_id, data, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.onboarding_screen_edit, guild_id),
            METHOD_PUT,
            f'{API_ENDPOINT}/guilds/{guild_id}/onboarding',
            data,
            reason = reason,
        )
    
    # Voice
    
    async def voice_state_edit_own(self, guild_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.voice_state_edit_own, NO_SPECIFIC_RATE_LIMITER),
            METHOD_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/voice-states/@me',
            data,
        )
    
    
    async def voice_state_edit(self, guild_id, user_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.voice_state_edit, NO_SPECIFIC_RATE_LIMITER),
            METHOD_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/voice-states/{user_id}',
            data,
        )
    
    
    async def voice_state_get(self, guild_id, user_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.voice_state_get, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/voice-states/{user_id}',
        )
    
    
    async def voice_state_get_own(self, guild_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.voice_state_get_own, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/voice-states/@me',
        )
    
    # Invite
    
    async def invite_create(self, channel_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.invite_create, channel_id),
            METHOD_POST,
            f'{API_ENDPOINT}/channels/{channel_id}/invites',
            data,
        )
    
    
    async def invite_get(self,invite_code, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.invite_get, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/invites/{invite_code}',
            params = data,
        )
    
    
    async def invite_get_all_guild(self, guild_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.invite_get_all_guild, guild_id),
            METHOD_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/invites',
        )
    
    
    async def invite_get_all_channel(self, channel_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.invite_get_all_channel, channel_id),
            METHOD_GET,
            f'{API_ENDPOINT}/channels/{channel_id}/invites',
        )
    
    
    async def invite_delete(self,invite_code, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.invite_delete, NO_SPECIFIC_RATE_LIMITER),
            METHOD_DELETE,
            f'{API_ENDPOINT}/invites/{invite_code}',
            reason = reason,
        )
    
    
    # role
    
    async def role_get(self, guild_id, role_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.role_get, guild_id),
            METHOD_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/roles/{role_id}',
        )
    
    
    async def role_edit(self, guild_id, role_id, data, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.role_edit, guild_id),
            METHOD_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/roles/{role_id}',
            data,
            reason = reason,
        )
    
    
    async def role_delete(self, guild_id, role_id, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.role_delete, guild_id),
            METHOD_DELETE,
            f'{API_ENDPOINT}/guilds/{guild_id}/roles/{role_id}',
            reason = reason,
        )
    
    
    async def role_create(self, guild_id, data, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.role_create, guild_id),
            METHOD_POST,
            f'{API_ENDPOINT}/guilds/{guild_id}/roles',
            data,
            reason = reason,
        )
    
    
    async def role_move(self, guild_id, data, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.role_move, guild_id),
            METHOD_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/roles',
            data,
            reason = reason,
        )
    
    
    # emoji guild
    
    async def emoji_get_guild(self, guild_id, emoji_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.emoji_get_guild, guild_id),
            METHOD_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/emojis/{emoji_id}',
        )
    
    
    async def emoji_get_all_guild(self, guild_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.emoji_get_all_guild, guild_id),
            METHOD_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/emojis'
        )
    
    
    async def emoji_edit_guild(self, guild_id, emoji_id, data, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.emoji_edit_guild, guild_id),
            METHOD_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/emojis/{emoji_id}',
            data,
            reason = reason,
        )
    
    
    async def emoji_create_guild(self, guild_id, data, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.emoji_create_guild, guild_id),
            METHOD_POST,
            f'{API_ENDPOINT}/guilds/{guild_id}/emojis',
            data,
            reason = reason,
        )
    
    
    async def emoji_delete_guild(self, guild_id, emoji_id, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.emoji_delete_guild, guild_id),
            METHOD_DELETE,
            f'{API_ENDPOINT}/guilds/{guild_id}/emojis/{emoji_id}',
            reason = reason,
        )
    
    
    # emoji / application
    
    
    async def emoji_get_application(self, application_id, emoji_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.emoji_get_application, application_id),
            METHOD_GET,
            f'{API_ENDPOINT}/applications/{application_id}/emojis/{emoji_id}',
        )
    
    
    async def emoji_get_all_application(self, application_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.emoji_get_all_application, application_id),
            METHOD_GET,
            f'{API_ENDPOINT}/applications/{application_id}/emojis'
        )
    
    
    async def emoji_edit_application(self, application_id, emoji_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.emoji_edit_application, application_id),
            METHOD_PATCH,
            f'{API_ENDPOINT}/applications/{application_id}/emojis/{emoji_id}',
            data,
        )
    
    
    async def emoji_create_application(self, application_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.emoji_create_application, application_id),
            METHOD_POST,
            f'{API_ENDPOINT}/applications/{application_id}/emojis',
            data,
        )
    
    
    async def emoji_delete_application(self, application_id, emoji_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.emoji_delete_application, application_id),
            METHOD_DELETE,
            f'{API_ENDPOINT}/applications/{application_id}/emojis/{emoji_id}',
        )
    
    
    # relations
    
    async def relationship_delete(self, user_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.relationship_delete, NO_SPECIFIC_RATE_LIMITER),
            METHOD_DELETE,
            f'{API_ENDPOINT}/users/@me/relationships/{user_id}',
        )
    
    
    async def relationship_create(self, user_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.relationship_create, NO_SPECIFIC_RATE_LIMITER),
            METHOD_PUT,
            f'{API_ENDPOINT}/users/@me/relationships/{user_id}',
            data,
        )
    
    
    async def relationship_friend_request(self, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.relationship_friend_request, NO_SPECIFIC_RATE_LIMITER),
            METHOD_POST,
            f'{API_ENDPOINT}/users/@me/relationships',
            data,
        )
    
    # webhook
    
    async def webhook_create(self, channel_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.webhook_create, channel_id),
            METHOD_POST,
            f'{API_ENDPOINT}/channels/{channel_id}/webhooks',
            data,
        )
    
    
    async def webhook_get(self, webhook_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.webhook_get, webhook_id),
            METHOD_GET,
            f'{API_ENDPOINT}/webhooks/{webhook_id}',
        )
    
    
    async def webhook_get_all_channel(self, channel_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.webhook_get_all_channel, channel_id),
            METHOD_GET,
            f'{API_ENDPOINT}/channels/{channel_id}/webhooks',
        )
    
    
    async def webhook_get_all_guild(self, guild_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.webhook_get_all_guild, guild_id),
            METHOD_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/webhooks',
        )
    
    
    async def webhook_get_token(self, webhook_id, webhook_token):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.webhook_get_token, webhook_id),
            METHOD_GET,
            f'{API_ENDPOINT}/webhooks/{webhook_id}/{webhook_token}',
            headers = IgnoreCaseMultiValueDictionary(),
        )
    
    
    async def webhook_delete_token(self, webhook_id, webhook_token):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.webhook_delete_token, webhook_id),
            METHOD_DELETE,
            f'{API_ENDPOINT}/webhooks/{webhook_id}/{webhook_token}',
            headers = IgnoreCaseMultiValueDictionary(),
        )
    
    
    async def webhook_delete(self, webhook_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.webhook_delete, webhook_id),
            METHOD_DELETE,
            f'{API_ENDPOINT}/webhooks/{webhook_id}',
        )
    
    
    async def webhook_edit_token(self, webhook_id, webhook_token, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.webhook_edit_token, webhook_id),
            METHOD_PATCH,
            f'{API_ENDPOINT}/webhooks/{webhook_id}/{webhook_token}',
            data,
            headers = IgnoreCaseMultiValueDictionary(),
        )
    
    
    async def webhook_edit(self, webhook_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.webhook_edit, webhook_id),
            METHOD_PATCH,
            f'{API_ENDPOINT}/webhooks/{webhook_id}',
            data,
        )
    
    
    async def webhook_message_create(self, webhook_id, webhook_token, data, query_parameters):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.webhook_message_create, webhook_id),
            METHOD_POST,
            f'{API_ENDPOINT}/webhooks/{webhook_id}/{webhook_token}',
            data, headers = IgnoreCaseMultiValueDictionary(),
            params = query_parameters,
        )
    
    
    async def webhook_message_edit(self, webhook_id, webhook_token, message_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.webhook_message_edit, webhook_id),
            METHOD_PATCH,
            f'{API_ENDPOINT}/webhooks/{webhook_id}/{webhook_token}/messages/{message_id}',
            data,
            headers = IgnoreCaseMultiValueDictionary(),
        )
    
    
    async def webhook_message_delete(self, webhook_id, webhook_token, message_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.webhook_message_edit, webhook_id),
            METHOD_DELETE,
            f'{API_ENDPOINT}/webhooks/{webhook_id}/{webhook_token}/messages/{message_id}',
            headers = IgnoreCaseMultiValueDictionary(),
        )
    
    
    async def webhook_message_get(self, webhook_id, webhook_token, message_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.webhook_message_get, webhook_id),
            METHOD_GET,
            f'{API_ENDPOINT}/webhooks/{webhook_id}/{webhook_token}/messages/{message_id}',
            headers = IgnoreCaseMultiValueDictionary(),
        )
    
    # user
    
    async def user_get(self, user_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.user_get, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/users/{user_id}',
        )
    
    
    async def guild_user_get(self, guild_id, user_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.guild_user_get, guild_id),
            METHOD_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}',
        )
    
    
    async def guild_user_search(self, guild_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.guild_user_search, guild_id),
            METHOD_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/members/search',
            params = data,
        )
    
    # hooman only
    async def user_get_profile(self, user_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.user_get_profile, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/users/{user_id}/profile',
        )
    
    # hypesquad
    
    async def hypesquad_house_change(self, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.hypesquad_house_change, NO_SPECIFIC_RATE_LIMITER),
            METHOD_POST,
            f'{API_ENDPOINT}/hypesquad/online',
            data,
        )
    
    
    async def hypesquad_house_leave(self):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.hypesquad_house_leave, NO_SPECIFIC_RATE_LIMITER),
            METHOD_DELETE,
            f'{API_ENDPOINT}/hypesquad/online',
        )
    
    # achievements
    
    async def achievement_get_all(self, application_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.achievement_get_all, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/applications/{application_id}/achievements',
        )
    
    
    async def achievement_get(self, application_id, achievement_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.achievement_get, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/applications/{application_id}/achievements/{achievement_id}',
        )
    
    
    async def achievement_create(self, application_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.achievement_create, NO_SPECIFIC_RATE_LIMITER),
            METHOD_POST,
            f'{API_ENDPOINT}/applications/{application_id}/achievements',
            data,
        )
    
    
    async def achievement_edit(self, application_id, achievement_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.achievement_edit, NO_SPECIFIC_RATE_LIMITER),
            METHOD_PATCH,
            f'{API_ENDPOINT}/applications/{application_id}/achievements/{achievement_id}',
            data,
        )
    
    
    async def achievement_delete(self, application_id, achievement_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.achievement_delete, NO_SPECIFIC_RATE_LIMITER),
            METHOD_DELETE,
            f'{API_ENDPOINT}/applications/{application_id}/achievements/{achievement_id}',
        )
    
    
    async def user_achievement_get_all(self, application_id, headers):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.user_achievement_get_all, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/users/@me/applications/{application_id}/achievements',
            headers = headers,
        )
    
    
    async def user_achievement_update(self, user_id, application_id, achievement_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.user_achievement_update, NO_SPECIFIC_RATE_LIMITER),
            METHOD_PUT,
            f'{API_ENDPOINT}/users/{user_id}/applications/{application_id}/achievements/{achievement_id}',
            data,
        )
    
    # application role connection
    
    async def application_role_connection_metadata_get_all(self, application_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.application_role_connection_metadata_get_all, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/applications/{application_id}/role-connections/metadata',
        )
    
    
    async def application_role_connection_metadata_edit_all(self, application_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.application_role_connection_metadata_edit_all, NO_SPECIFIC_RATE_LIMITER),
            METHOD_PUT,
            f'{API_ENDPOINT}/applications/{application_id}/role-connections/metadata',
            data,
        )
    
    
    async def application_role_connection_metadata_delete_all(self, application_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.application_role_connection_metadata_delete_all, NO_SPECIFIC_RATE_LIMITER),
            METHOD_DELETE,
            f'{API_ENDPOINT}/applications/{application_id}/role-connections/metadata',
        )
    
    # random
    
    # hooman only sadly, but this would be nice to be allowed, to get name and icon at least
    async def application_get(self, application_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.application_get, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/applications/{application_id}',
        )
    
    
    async def application_get_all_detectable(self):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.application_get_all_detectable, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/applications/detectable',
        )
    
    
    async def eula_get(self, eula_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.eula_get, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/store/eulas/{eula_id}',
        )
    
    
    async def discovery_category_get_all(self, params):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.discovery_category_get_all, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/discovery/categories',
            params = params,
        )
    
    
    async def discovery_validate_term(self, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.discovery_validate_term, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/discovery/valid-term',
            params = data,
        )
    
    
    async def discovery_stage_get_all(self):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.discovery_stage_get_all, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/discovery',
        )
    
    
    async def discovery_guild_get_all(self):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.discovery_guild_get_all, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/guild-discovery',
        )
    
    
    async def stage_get_all(self, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.stage_get_all, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/stage-instances',
            data,
        )
    
    
    async def stage_create(self, data, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.stage_create, NO_SPECIFIC_RATE_LIMITER),
            METHOD_POST,
            f'{API_ENDPOINT}/stage-instances',
            data,
            reason = reason,
        )
    
    
    async def stage_get(self, channel_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.stage_get, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/stage-instances/{channel_id}',
        )
    
    
    async def stage_edit(self, channel_id, data, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.stage_edit, NO_SPECIFIC_RATE_LIMITER),
            METHOD_PATCH,
            f'{API_ENDPOINT}/stage-instances/{channel_id}',
            data,
            reason = reason,
        )
    
    
    async def stage_delete(self, channel_id, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.stage_delete, NO_SPECIFIC_RATE_LIMITER),
            METHOD_DELETE,
            f'{API_ENDPOINT}/stage-instances/{channel_id}',
            reason = reason,
        )
    
    
    # Scheduled events
    
    async def scheduled_event_create(self, guild_id, data, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.scheduled_event_create, guild_id),
            METHOD_POST,
            f'{API_ENDPOINT}/guilds/{guild_id}/scheduled-events',
            data,
            reason = reason,
        )
    
    
    async def scheduled_event_edit(self, guild_id, scheduled_event_id, data, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.scheduled_event_edit, guild_id),
            METHOD_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/scheduled-events/{scheduled_event_id}',
            data,
            reason = reason,
        )
    
    
    async def scheduled_event_delete(self, guild_id, scheduled_event_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.scheduled_event_delete, guild_id),
            METHOD_DELETE,
            f'{API_ENDPOINT}/guilds/{guild_id}/scheduled-events/{scheduled_event_id}',
        )
    
    
    async def scheduled_event_get(self, guild_id, scheduled_event_id, params):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.scheduled_event_get, guild_id),
            METHOD_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/scheduled-events/{scheduled_event_id}',
            params = params,
        )
    
    
    async def scheduled_event_get_all_guild(self, guild_id, params):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.scheduled_event_get_all_guild, guild_id),
            METHOD_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/scheduled-events',
            params = params,
        )
    
    
    async def scheduled_event_user_get_chunk(self, guild_id, scheduled_event_id, params):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.scheduled_event_user_get_chunk, guild_id),
            METHOD_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/scheduled-events/{scheduled_event_id}/users',
            params = params,
        )
    
    
    # DiscordException Forbidden (403), code = 20001: Bots cannot use this endpoint
    # data structure: {'sticker_ids': [sticker_id_1, ...]}
    async def greet(self, channel_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.greet, channel_id),
            METHOD_POST,
            f'{API_ENDPOINT}/channels/{channel_id}/greet',
            data,
        )
    
    
    # hooman only
    async def bulk_ack(self):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.bulk_ack, NO_SPECIFIC_RATE_LIMITER),
            METHOD_POST,
            f'{API_ENDPOINT}/read-states/ack-bulk',
        )
    
    
    async def voice_region_get_all(self):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.voice_region_get_all, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/voice/regions',
        )
    
    
    # channel
    
    async def channel_get(self, channel_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.channel_get, channel_id),
            METHOD_GET,
            f'{API_ENDPOINT}/channels/{channel_id}',
        )
    
    
    # thread
    
    async def guild_thread_get_all_active(self, guild_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.guild_thread_get_all_active, guild_id),
            METHOD_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/threads/active',
        )
    
    
    # DiscordException Bad Request (400), code = 50001: Missing Access
    async def thread_create(self, channel_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.thread_create, channel_id),
            METHOD_POST,
            f'{API_ENDPOINT}/channels/{channel_id}/threads',
            data,
        )
    
    
    async def thread_create_from_message(self, channel_id, message_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.thread_create_from_message, channel_id),
            METHOD_POST,
            f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/threads',
            data,
        )
    
    
    async def thread_user_get_chunk(self, channel_id, query_parameters):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.thread_user_get_chunk, channel_id),
            METHOD_GET,
            f'{API_ENDPOINT}/channels/{channel_id}/thread-members',
            params = query_parameters,
        )
    
    
    async def thread_join(self, channel_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.thread_join, channel_id),
            METHOD_POST,
            f'{API_ENDPOINT}/channels/{channel_id}/thread-members/@me'
        )
    
    
    async def thread_leave(self, channel_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.thread_leave, channel_id),
            METHOD_DELETE,
            f'{API_ENDPOINT}/channels/{channel_id}/thread-members/@me',
        )
    
    
    async def thread_user_get(self, channel_id, user_id, query_parameters):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.thread_user_get, channel_id),
            METHOD_GET,
            f'{API_ENDPOINT}/channels/{channel_id}/thread-members/{user_id}',
            params = query_parameters,
        )
    
    
    async def thread_user_add(self, channel_id, user_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.thread_user_add, channel_id),
            METHOD_POST,
            f'{API_ENDPOINT}/channels/{channel_id}/thread-members/{user_id}',
        )
    
    
    async def thread_user_delete(self, channel_id, user_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.thread_user_delete, channel_id),
            METHOD_DELETE,
            f'{API_ENDPOINT}/channels/{channel_id}/thread-members/{user_id}',
        )
    
    # DiscordException Forbidden (403), code = 20001: Bots cannot use this endpoint
    async def thread_self_settings_edit(self, channel_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.thread_self_settings_edit, channel_id),
            METHOD_GET,
            f'{API_ENDPOINT}/channels/{channel_id}/thread-members/@me/settings',
        )
    
    # Removed in V10
    async def channel_thread_get_chunk_active(self, channel_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.channel_thread_get_chunk_active, channel_id),
            METHOD_GET,
            f'{API_ENDPOINT}/channels/{channel_id}/threads/active',
            params = data,
        )
    
    
    async def channel_thread_get_chunk_archived_private(self, channel_id, query_parameters):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.channel_thread_get_chunk_archived_private, channel_id),
            METHOD_GET,
            f'{API_ENDPOINT}/channels/{channel_id}/threads/archived/private',
            params = query_parameters,
        )
    
    
    async def channel_thread_get_chunk_archived_public(self, channel_id, query_parameters):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.channel_thread_get_chunk_archived_public, channel_id),
            METHOD_GET,
            f'{API_ENDPOINT}/channels/{channel_id}/threads/archived/public',
            params = query_parameters,
        )
    
    
    async def channel_thread_get_chunk_self_archived(self, channel_id, query_parameters):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.channel_thread_get_chunk_self_archived, channel_id),
            METHOD_GET,
            f'{API_ENDPOINT}/channels/{channel_id}/users/@me/threads/archived/private',
            params = query_parameters,
        )
    
    # application command & interaction
    
    async def application_command_global_get(self, application_id, application_command_id, query_parameters):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.application_command_global_get, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/applications/{application_id}/commands/{application_command_id}',
            params = query_parameters,
        )
    
    
    async def application_command_global_get_all(self, application_id, query_parameters):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.application_command_global_get_all, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/applications/{application_id}/commands',
            params = query_parameters,
        )
    
    
    async def application_command_global_create(self, application_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.application_command_global_create, NO_SPECIFIC_RATE_LIMITER),
            METHOD_POST,
            f'{API_ENDPOINT}/applications/{application_id}/commands',
            data,
        )
    
    
    async def application_command_global_edit(self, application_id, application_command_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.application_command_global_edit, NO_SPECIFIC_RATE_LIMITER),
            METHOD_PATCH,
            f'{API_ENDPOINT}/applications/{application_id}/commands/{application_command_id}',
            data,
        )
    
    
    async def application_command_global_delete(self, application_id, application_command_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.application_command_global_delete, NO_SPECIFIC_RATE_LIMITER),
            METHOD_DELETE,
            f'{API_ENDPOINT}/applications/{application_id}/commands/{application_command_id}',
        )
    
    
    async def application_command_global_update_multiple(self, application_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.application_command_global_update_multiple, NO_SPECIFIC_RATE_LIMITER),
            METHOD_PUT,
            f'{API_ENDPOINT}/applications/{application_id}/commands',
            data,
        )
    
    
    async def application_command_guild_get(self, application_id, guild_id, application_command_id, query_parameters):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.application_command_guild_get, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/applications/{application_id}/guilds/{guild_id}/commands/{application_command_id}',
            params = query_parameters,
        )
    
    
    async def application_command_guild_get_all(self, application_id, guild_id, query_parameters):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.application_command_guild_get_all, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/applications/{application_id}/guilds/{guild_id}/commands',
            params = query_parameters,
        )
    
    
    async def application_command_guild_create(self, application_id, guild_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.application_command_guild_create, guild_id),
            METHOD_POST,
            f'{API_ENDPOINT}/applications/{application_id}/guilds/{guild_id}/commands',
            data,
        )
    
    
    async def application_command_guild_edit(self, application_id, guild_id, application_command_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.application_command_guild_edit, guild_id),
            METHOD_PATCH,
            f'{API_ENDPOINT}/applications/{application_id}/guilds/{guild_id}/commands/{application_command_id}',
            data,
        )
    
    
    async def application_command_guild_delete(self, application_id, guild_id, application_command_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.application_command_guild_delete, guild_id),
            METHOD_DELETE,
            f'{API_ENDPOINT}/applications/{application_id}/guilds/{guild_id}/commands/{application_command_id}',
        )
    
    
    async def application_command_guild_update_multiple(self, application_id, guild_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.application_command_guild_update_multiple, guild_id),
            METHOD_PUT,
            f'{API_ENDPOINT}/applications/{application_id}/guilds/{guild_id}/commands',
            data,
        )
    
    
    async def application_command_permission_get(self, application_id, guild_id, application_command_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.application_command_permission_get, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/applications/{application_id}/guilds/{guild_id}/commands/{application_command_id}'
            f'/permissions',
        )
    
    
    async def application_command_permission_edit(
        self, application_id, guild_id, application_command_id, data, headers
    ):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.application_command_permission_edit, NO_SPECIFIC_RATE_LIMITER),
            METHOD_PUT,
            f'{API_ENDPOINT}/applications/{application_id}/guilds/{guild_id}/commands/{application_command_id}'
            f'/permissions',
            data,
            headers = headers,
        )
    
    
    async def application_command_permission_get_all_guild(self, application_id, guild_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.application_command_permission_get_all_guild, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/applications/{application_id}/guilds/{guild_id}/commands/permissions',
        )
    
    
    async def interaction_response_message_create(
        self, interaction_id, interaction_token, data, query_string_parameters
    ):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.interaction_response_message_create, NO_SPECIFIC_RATE_LIMITER),
            METHOD_POST,
            f'{API_ENDPOINT}/interactions/{interaction_id}/{interaction_token}/callback',
            data,
            query_string_parameters,
        )
    
    
    async def interaction_response_message_edit(self, application_id, interaction_id, interaction_token, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.interaction_response_message_edit, interaction_id),
            METHOD_PATCH,
            f'{API_ENDPOINT}/webhooks/{application_id}/{interaction_token}/messages/@original',
            data,
        )
    
    
    async def interaction_response_message_delete(self, application_id, interaction_id, interaction_token):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.interaction_response_message_delete, interaction_id),
            METHOD_DELETE,
            f'{API_ENDPOINT}/webhooks/{application_id}/{interaction_token}/messages/@original',
        )
    
    
    async def interaction_response_message_get(self, application_id, interaction_id, interaction_token):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.interaction_response_message_get, interaction_id),
            METHOD_GET,
            f'{API_ENDPOINT}/webhooks/{application_id}/{interaction_token}/messages/@original',
        )
    
    
    async def interaction_followup_message_create(self, application_id, interaction_id, interaction_token, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.interaction_followup_message_create, interaction_id),
            METHOD_POST,
            f'{API_ENDPOINT}/webhooks/{application_id}/{interaction_token}',
            data,
        )
    
    
    async def interaction_followup_message_edit(
        self, application_id, interaction_id, interaction_token, message_id, data
    ):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.interaction_followup_message_edit, interaction_id),
            METHOD_PATCH,
            f'{API_ENDPOINT}/webhooks/{application_id}/{interaction_token}/messages/{message_id}',
            data,
        )
    
    
    async def interaction_followup_message_delete(self, application_id, interaction_id, interaction_token, message_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.interaction_followup_message_delete, interaction_id),
            METHOD_DELETE,
            f'{API_ENDPOINT}/webhooks/{application_id}/{interaction_token}/messages/{message_id}',
        )
    
    
    async def interaction_followup_message_get(self, application_id, interaction_id, interaction_token, message_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.interaction_followup_message_get, interaction_id),
            METHOD_GET,
            f'{API_ENDPOINT}/webhooks/{application_id}/{interaction_token}/messages/{message_id}'
        )
    
    # User account only
    async def message_interaction(self, channel_id, message_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.message_interaction, channel_id),
            METHOD_GET,
            f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/interaction-data',
        )
    
    # Embedded activity
    
    async def embedded_activity_get(self, application_id, embedded_activity_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.embedded_activity_get, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/applications/{application_id}/activity-instances/{embedded_activity_id}'
        )
    
    # Soundboard
    
    async def soundboard_sound_get_all_default(self):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.soundboard_sound_get_all_default, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/soundboard-default-sounds'
        )
    
    
    async def soundboard_sound_create(self, guild_id, data, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.soundboard_sound_create, NO_SPECIFIC_RATE_LIMITER),
            METHOD_POST,
            f'{API_ENDPOINT}/guilds/{guild_id}/soundboard-sounds',
            data,
            reason = reason,
        )
    
    
    async def soundboard_sound_delete(self, guild_id, soundboard_sound_id, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.soundboard_sound_delete, NO_SPECIFIC_RATE_LIMITER),
            METHOD_DELETE,
            f'{API_ENDPOINT}/guilds/{guild_id}/soundboard-sounds/{soundboard_sound_id}',
            reason = reason,
        )
    
    
    async def soundboard_sound_edit(self, guild_id, soundboard_sound_id, data, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.soundboard_sound_edit, NO_SPECIFIC_RATE_LIMITER),
            METHOD_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/soundboard-sounds/{soundboard_sound_id}',
            data,
            reason = reason,
        )
    
    # Sticker
    
    async def sticker_get_all_guild(self, guild_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.sticker_get_all_guild, guild_id),
            METHOD_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/stickers',
        )
    
    
    async def sticker_pack_get(self, sticker_pack_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.sticker_pack_get, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/sticker-packs/{sticker_pack_id}',
        )
    
    
    async def sticker_pack_get_all(self):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.sticker_pack_get_all, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/sticker-packs',
        )
    
    
    async def sticker_get_guild(self, guild_id, sticker_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.sticker_get_guild, guild_id),
            METHOD_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/stickers/{sticker_id}',
        )
    
    
    async def sticker_create(self, guild_id, data, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.sticker_create, guild_id),
            METHOD_POST,
            f'{API_ENDPOINT}/guilds/{guild_id}/stickers',
            data,
            reason = reason,
        )
    
    
    async def sticker_delete(self, guild_id, sticker_id, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.sticker_delete, guild_id),
            METHOD_DELETE,
            f'{API_ENDPOINT}/guilds/{guild_id}/stickers/{sticker_id}',
            reason = reason,
        )
    
    
    async def sticker_get(self, sticker_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.sticker_get, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/stickers/{sticker_id}',
        )
    
    
    async def sticker_edit(self, guild_id, sticker_id, data, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.sticker_edit, guild_id),
            METHOD_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/stickers/{sticker_id}',
            data,
            reason = reason,
        )
    
    # status
    
    async def status_incident_unresolved(self):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.status_incident_unresolved, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{STATUS_ENDPOINT}/incidents/unresolved.json',
            headers = IgnoreCaseMultiValueDictionary(),
        )
    
    
    async def status_maintenance_active(self):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.status_maintenance_active, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{STATUS_ENDPOINT}/scheduled-maintenances/active.json',
            headers = IgnoreCaseMultiValueDictionary(),
        )
    
    
    async def status_maintenance_upcoming(self):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.status_maintenance_upcoming, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{STATUS_ENDPOINT}/scheduled-maintenances/upcoming.json',
            headers = IgnoreCaseMultiValueDictionary(),
        )
    
    # auto moderation
    
    async def auto_moderation_rule_get(self, guild_id, auto_moderation_rule_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.auto_moderation_rule_get, guild_id),
            METHOD_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/auto-moderation/rules/{auto_moderation_rule_id}',
        )
    
    
    async def auto_moderation_rule_get_all(self, guild_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.auto_moderation_rule_get_all, guild_id),
            METHOD_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/auto-moderation/rules',
        )
    
    
    async def auto_moderation_rule_create(self, guild_id, data, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.auto_moderation_rule_get, guild_id),
            METHOD_POST,
            f'{API_ENDPOINT}/guilds/{guild_id}/auto-moderation/rules',
            data,
            reason = reason,
        )
    
    
    async def auto_moderation_rule_edit(self, guild_id, auto_moderation_rule_id, data, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.auto_moderation_rule_edit, guild_id),
            METHOD_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/auto-moderation/rules/{auto_moderation_rule_id}',
            data,
            reason = reason,
        )

    async def auto_moderation_rule_delete(self, guild_id, auto_moderation_rule_id, reason):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.auto_moderation_rule_delete, guild_id),
            METHOD_DELETE,
            f'{API_ENDPOINT}/guilds/{guild_id}/auto-moderation/rules/{auto_moderation_rule_id}',
            reason = reason,
        )
    
    # sku & entitlement & subscription
    
    async def sku_get_all(self, application_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.sku_get_all, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/applications/{application_id}/skus',
        )
    
    
    async def entitlement_get_chunk(self, application_id, query_parameters):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.entitlement_get_chunk, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/applications/{application_id}/entitlements',
            params = query_parameters,
        )
    
    
    async def entitlement_create(self, application_id, data):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.entitlement_create, NO_SPECIFIC_RATE_LIMITER),
            METHOD_POST,
            f'{API_ENDPOINT}/applications/{application_id}/entitlements',
            data,
        )
    
    
    async def entitlement_delete(self, application_id, entitlement_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.entitlement_delete, NO_SPECIFIC_RATE_LIMITER),
            METHOD_DELETE,
            f'{API_ENDPOINT}/applications/{application_id}/entitlements/{entitlement_id}',
        )
    
    
    async def entitlement_consume(self, application_id, entitlement_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.entitlement_consume, NO_SPECIFIC_RATE_LIMITER),
            METHOD_POST,
            f'{API_ENDPOINT}/applications/{application_id}/entitlements/{entitlement_id}/consume',
        )

    async def subscription_get_sku(self, sku_id, subscription_id):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.subscription_get_sku, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/skus/{sku_id}/subscriptions/{subscription_id}',
        )
    
    
    async def subscription_get_chunk_sku_user(self, sku_id, query_parameters):
        return await self.discord_request(
            RateLimitHandler(RATE_LIMIT_GROUPS.subscription_get_chunk_sku_user, NO_SPECIFIC_RATE_LIMITER),
            METHOD_GET,
            f'{API_ENDPOINT}/skus/{sku_id}/subscriptions',
            params = query_parameters,
        )
