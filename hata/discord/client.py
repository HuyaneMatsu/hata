# -*- coding: utf-8 -*-
__all__ = ('Client', 'Typer', )

import re, sys
from time import monotonic, time as time_now
from collections import deque
from os.path import split as splitpath
from threading import current_thread
from math import inf

from ..backend.dereaddons_local import multidict_titled, _spaceholder, methodize, basemethod
from ..backend.futures import Future, Task, sleep, CancelledError, WaitTillAll, WaitTillFirst, WaitTillExc
from ..backend.eventloop import EventThread
from ..backend.formdata import Formdata
from ..backend.hdrs import AUTHORIZATION
from ..backend.helpers import BasicAuth

from .others import Status, log_time_converter, DISCORD_EPOCH, VoiceRegion, ContentFilterLevel, PremiumType, \
    MessageNotificationLevel, image_to_base64, random_id, to_json, VerificationLevel, \
    RelationshipType, get_image_extension
from .user import User, USERS, GuildProfile, UserBase, UserFlag, PartialUser
from .emoji import Emoji
from .channel import ChannelCategory, ChannelGuildBase, ChannelPrivate, ChannelText, ChannelGroup, \
    message_relativeindex, cr_pg_channel_object, MessageIterator, CHANNEL_TYPES
from .guild import Guild, PartialGuild, GuildEmbed, GuildWidget, GuildFeature, GuildPreview, GuildDiscovery, \
    DiscoveryCategory, COMMUNITY_FEATURES
from .http import DiscordHTTPClient, URLS, CDN_ENDPOINT
from .http.URLS import VALID_ICON_FORMATS, VALID_ICON_FORMATS_EXTENDED
from .role import Role, PermOW
from .webhook import Webhook, PartialWebhook
from .gateway import DiscordGateway, DiscordGatewaySharder
from .parsers import EventDescriptor, _with_error, IntentFlag, PARSER_DEFAULTS
from .audit_logs import AuditLog, AuditLogIterator
from .invite import Invite
from .message import Message
from .oauth2 import Connection, parse_locale, DEFAULT_LOCALE, AO2Access, UserOA2, Achievement
from .exceptions import DiscordException, DiscordGatewayException, ERROR_CODES, InvalidToken
from .client_core import CLIENTS, CACHE_USER, CACHE_PRESENCE, KOKORO, GUILDS, DISCOVERY_CATEGORIES
from .voice_client import VoiceClient
from .activity import ActivityUnknown, ActivityBase, ActivityCustom
from .integration import Integration
from .application import Application, Team
from .ratelimit import RatelimitProxy, RATELIMIT_GROUPS
from .preconverters import preconvert_snowflake, preconvert_str, preconvert_bool, preconvert_discriminator, \
    preconvert_flag, preconvert_preinstanced_type
from .permission import Permission
from .bases import ICON_TYPE_NONE

from . import client_core, message, webhook, channel

_VALID_NAME_CHARS=re.compile('([0-9A-Za-z_]+)')

USER_CHUNK_TIMEOUT = 2.5

class SingleUserChunker(object):
    """
    A user chunk waiter, which yields after the first received chunk. Used at ``Client.request_members``.
    
    Attributes
    ----------
    timer : `Handle` or `None`
        The timeouter of the chunker, what will cancel if the timeout occures.
    waiter : `Future`
        The waiter future what will yield, when we receive the response, or when the timeout occures.
    """
    __slots__ = ('timer', 'waiter',)
    
    def __init__(self, ):
        self.waiter = Future(KOKORO)
        self.timer = KOKORO.call_at(monotonic()+USER_CHUNK_TIMEOUT, type(self)._cancel, self)
    
    def __call__(self, event):
        """
        Called when a chunk is received with it's respective nonce.
        
        Parameters
        ----------
        event : ``GuildUserChunkEvent``
            The received guild user chunk's event.
        
        Returns
        -------
        is_last : `bool`
            ``SingleUserChunker`` returns always `True`, because it waits only for one event.
        """
        self.waiter.set_result_if_pending(event.users)
        timer=self.timer
        if (timer is not None):
            self.timer = None
            timer.cancel()
        
        return True
    
    def _cancel(self):
        """
        The chunker's timer calls this method.
        
        Cancels ``.waiter`` and ``.timer``. After this method was called, the waiting coroutine will remove it's
        reference from the event handler.
        """
        self.waiter.cancel()
        
        timer=self.timer
        if (timer is not None):
            self.timer = None
            timer.cancel()
    
    def cancel(self):
        """
        Cancels the chunker.
        
        This method should be called when when the chunker is canceller from outside. Before this method is called,
        it's references should be removed as well from the event handler.
        """
        self.waiter.set_result_if_pending([])
        
        timer=self.timer
        if (timer is not None):
            self.timer = None
            timer.cancel()
    
    def __await__(self):
        """
        Awaits the chunker's waiter and returns that's result.
        
        Returns
        -------
        users : `list` of (``Client`` or ``User``) objects
            The received users. Can be an empty list.
        
        Raises
        ------
        CancelledError
            If timeout occured.
        """
        return self.waiter.__await__()

class MassUserChunker(object):
    """
    A user chunk waiter, which yields after the chunks of sertain amount of guilds are received. Used at
    ``Client._request_members`` and at ``Client._request_members``.
    
    Attributes
    ----------
    last : `float`
        The timestamp of the last received chunk.
    left : `int`
        The amount of guilds, which's chunks are not yet requested
    timer : `Handle` or `None`
        The timeouter of the chunker, what will cancel if the timeout occures.
    waiter : `Future`
        The waiter future what will yield, when we receive the response, or when the timeout occures.
    """
    __slots__ = ('last', 'left', 'timer', 'waiter',)
    
    def __init__(self, left):
        """
        Parameters
        ----------
        left : `int`
            How much guild's chunks are left to be received.
        """
        self.left = left
        self.waiter = Future(KOKORO)
        self.last = now = monotonic()
        self.timer = KOKORO.call_at(now+USER_CHUNK_TIMEOUT, type(self)._cancel, self)
    
    def __call__(self, event):
        """
        Called when a chunk is received with it's respective nonce.
        
        Updates the chunker's last received chunk's time to push out the current timeout.
        
        Parameters
        ----------
        event : ``GuildUserChunkEvent``
            The received guild user chunk's event.
        
        Returns
        -------
        is_last : `bool`
            Whether the last chunk was received.
        """
        self.last = monotonic()
        if event.index+1 != event.count:
            return False
        
        self.left = left = self.left-1
        if left > 0:
            return False
        
        self.waiter.set_result_if_pending(None)
        timer=self.timer
        if (timer is not None):
            self.timer = None
            timer.cancel()
        
        return True
    
    def _cancel(self):
        """
        The chunker's timer calls this method. If the chunker received any chunks since it's ``.timer`` was started,
        pushes out the timeout.
        
        Cancels ``.waiter`` and ``.timer``. After this method was called, the waiting coroutine will remove it's
        reference from the event handler.
        """
        now = monotonic()
        next_ = self.last + USER_CHUNK_TIMEOUT
        if next_ > now:
            self.timer = KOKORO.call_at(next_, type(self)._cancel, self)
        else:
            self.timer = None
            self.waiter.cancel()
    
    def cancel(self):
        """
        Cancels the chunker.
        
        This method should be called when when the chunker is canceller from outside. Before this method is called,
        it's references should be removed as well from the event handler.
        """
        self.left = 0
        self.waiter.set_result_if_pending(None)
        
        timer=self.timer
        if (timer is not None):
            self.timer=None
            timer.cancel()
    
    def __await__(self):
        """
        Awaits the chunker's waiter.
        
        Raises
        ------
        CancelledError
            If timeout occured.
        """
        return self.waiter.__await__()

class DiscoveryCategoryRequestCacher(object):
    """
    Cacher for storing ``Client``'s requests.
    
    Attributes
    ----------
    _active_request : `bool`
        Whether there is an active request.
    _last_update : `float`
        The last time when the cache was updated
    _waiter : `Future` or `None`
        Waiter to avoid concurrent calls.
    cached : `Any`
        Last result.
    func : `callable`
        Async callable, what's yields are cached.
    timeout : `float`
        The time interval between what the requests should be done.
    """
    __slots__ = ('_active_request', '_last_update', '_waiter', 'cached', 'func', 'timeout',)
    def __init__(self, func, timeout, cached=_spaceholder):
        """
        Creates a ``DiscoveryCategoryRequestCacher`` instance.
        
        Parameters
        ----------
        timeout : `float`
            The time after new request should be executed.
        func : `callable`
            Async callable, what's yields would be cached.
        cached : `Any`, Optional
            Whether there should be an available cache by default.
        """
        self.func = func
        self.timeout = timeout
        self.cached = cached
        self._waiter = None
        self._active_request = False
        self._last_update = -inf
    
    def __get__(self, client, type_):
        if client is None:
            return self
        
        return basemethod(self.__class__.execute, self, client)
    
    def __set__(self, obj, value):
        raise AttributeError('can\'t set attribute')
    
    def __delete__(self, obj):
        raise AttributeError('can\'t delete attribute')
    
    async def execute(self, client):
        """
        Executes the request and returns''s it's result or raises.
        
        Returns
        -------
        result : `Any`
        
        Raises
        ------
        ConnectionError
            If there is no internet connection, or there is no available cached result.
        DiscordException
        """
        if (monotonic() - self.timeout) < self._last_update:
            if self._active_request:
                waiter = self._waiter
                if waiter is None:
                    waiter = self._waiter = Future(KOKORO)
                
                result = await waiter
            else:
                result = self.cached
            
            return result
        
        self._active_request = True
        try:
            result = await self.func(client)
        except ConnectionError as err:
            result = self.cached
            if (result is _spaceholder):
                waiter = self._waiter
                if (waiter is not None):
                    self._waiter = None
                    waiter.set_exception(err)
                
                raise
        
        except BaseException as err:
            waiter = self._waiter
            if (waiter is not None):
                self._waiter = None
                waiter.set_exception(err)
            
            raise
        
        else:
            self._last_update = monotonic()
        
        finally:
            self._active_request = False
        
        waiter = self._waiter
        if (waiter is not None):
            self._waiter = None
            waiter.set_result(result)
        
        return result
    
    def __repr__(self):
        """Returns the cacher's representation."""
        result = [
            self.__class__.__name__,
            '(func=',
            repr(self.func),
            ', timeout=',
            repr(self.timeout),
                ]
        
        cached = self.cached
        if (cached is not _spaceholder):
            result.append(' cached=')
            result.append(repr(cached))
        
        result.append(')')
        
        return ''.join(result)
    
    __call__ = execute

class TimedCacheUnit(object):
    """
    Timed cache unit used at keyed request cachers.
    
    Attrbiutes
    ----------
    result : `str`
        The cached response object.
    creation_time : `float`
        The monotonic time when the last resposne was received.
    last_usage_time : `float`
        The monotnonic time when this unit was last tiem used.
    """
    __slots__ = ('creation_time', 'last_usage_time', 'result')
    def __repr__(self):
        """Returns the timed cache unit's representation."""
        return (f'<{self.__class__.__name__} creation_time={self.creation_time!r}, last_usage_time='
                f'{self.last_usage_time!r}, result={self.result!r}>')

class DiscoveryTermRequestCacher(object):
    """
    Cacher for storing ``Client'' requests. Also uses other clients, if the source client's ratelimits are already
    exhausted.
    
    Attributes
    ----------
    _last_cleanup : `float`
        The last time when a cleanup was done.
    _minimal_cleanup_interval : `float`
        The minimal time what needs to pass between cleanups.
    _ratelimit_proxy_args : `tuple` (``RatelimitGroup``, (``DiscordEntity`` or `None`))
        Ratelimit proxy arguments used when looking up the ratelimits of clients.
    _waiters : `dict` of (`str`, `
        Waiters for requests already being done.
    cached : `dict`
        Already cached responses.
    func : `callable`
        Async callable, what's yields are cached.
    timeout : `float`
        The timeout after the new request should be done insated of using the already cached response.
    """
    __slots__ =('_last_cleanup', '_minimal_cleanup_interval', '_ratelimit_proxy_args', '_waiters', 'cached', 'func', 'timeout')
    def __init__(self, func, timeout, ratelimit_group, ratelimit_limiter=None,):
        """
        Creates a new ``DiscoveryTermRequestCacher`` object with the given parameters.
        
        Parameters
        ----------
        func : `callable`
            Async callable, what's yields are cached.
        timeout : `float`
            The timeout after the new request should be done insated of using the already cached response.
        ratelimit_group : ``RatelimitGroup``
            Ratelimit group of the respective request.
        ratelimit_limiter : ``DiscordEntity``, Optional
            Retelimit limiter fo the respective request.
        """
        self.func = func
        self.timeout = timeout
        self.cached = {}
        self._ratelimit_proxy_args = (ratelimit_group, ratelimit_limiter)
        self._waiters = {}
        minimal_cleanup_interval = timeout / 10.0
        if minimal_cleanup_interval < 1800.0:
            minimal_cleanup_interval = 1800.0
        
        self._minimal_cleanup_interval = minimal_cleanup_interval
        self._last_cleanup = -inf
    
    def __get__(self, client, type_):
        if client is None:
            return self
        
        return basemethod(self.__class__.execute, self, client)
    
    def __set__(self, obj, value):
        raise AttributeError('can\'t set attribute')
    
    def __delete__(self, obj):
        raise AttributeError('can\'t delete attribute')
    
    async def execute(self, client, arg):
        """
        Executes the request and returns''s it's result or raises.
        
        Returns
        -------
        result : `Any`
        
        Raises
        ------
        ConnectionError
            If there is no internet connection, or there is no available cached result.
        TypeError
            The given `arg` was not passed as `str` instance.
        DiscordException
        """
        # First check arg
        arg_type = arg.__class__
        if arg_type is str:
            pass
        elif issubclass(arg_type, str):
            arg = str(arg)
        else:
            raise TypeError(f'The argument can be given as `str` instance, got {arg_type.__class__}.')
        
        # First check cache
        try:
            unit = self.cached[arg]
        except KeyError:
            unit = None
        else:
            now = monotonic()
            if self.timeout + unit.creation_time > now:
                unit.last_usage_time = now
                return unit.result
        
        # Second check actual request
        try:
            waiter = self._waiters[arg]
        except KeyError:
            pass
        else:
            if waiter is None:
                self._waiters[arg] = waiter = Future(KOKORO)
            
            return await waiter
        
        # No actual request is being done, so mark that we are doing a request.
        self._waiters[arg] = None
        
        # Search client with free ratelimits.
        free_count = RatelimitProxy(client, *self._ratelimit_proxy_args).free_count
        if not free_count:
            requester = client
            for client_ in CLIENTS:
                if client_ is client:
                    continue
                
                free_count = RatelimitProxy(client_, *self._ratelimit_proxy_args).free_count
                if free_count:
                    requester = client_
                    break
                
                continue
            
            # If there is no client with free count do not care about the reset times, because probably only 1 client
            # forces requests anyways, so that's ratelimits will reset first as well.
            client = requester
        
        # Do the request
        try:
            result = await self.func(client, arg)
        except ConnectionError as err:
            if (unit is None):
                waiter = self._waiters.pop(arg)
                if (waiter is not None):
                    waiter.set_exception(err)
                
                raise
            
            unit.last_usage_time = monotonic()
            result = unit.result
        
        except BaseException as err:
            waiter = self._waiters.pop(arg, None)
            if (waiter is not None):
                waiter.set_exception(err)
            
            raise
        
        else:
            if unit is None:
                self.cached[arg] = unit = TimedCacheUnit()
            
            now = monotonic()
            unit.last_usage_time = now
            unit.creation_time = now
            unit.result = result
        
        finally:
            # Do cleanup if needed
            now = monotonic()
            if self._last_cleanup + self._minimal_cleanup_interval < now:
                self._last_cleanup = now
                
                cleanup_till = now - self.timeout
                collected = []
                
                cached = self.cached
                for cached_arg, cached_unit in cached.items():
                    if cached_unit.last_usage_time < cleanup_till:
                        collected.append(cached_arg)
                
                for cached_arg in collected:
                    del cached[cached_arg]
        
        waiter = self._waiters.pop(arg)
        if (waiter is not None):
            waiter.set_result(result)
        
        return result
    
    def __repr__(self):
        """Returns the cacher's representation."""
        result = [
            self.__class__.__name__,
            '(func=',
            repr(self.func),
            ', timeout=',
            repr(self.timeout),
                ]
        
        ratelimit_group, ratelimit_limiter = self._ratelimit_proxy_args
        
        result.append(', ratelimit_group=')
        result.append(repr(ratelimit_group))
        
        if (ratelimit_limiter is not None):
            result.append(', ratelimit_limiter=')
            result.append(repr(ratelimit_limiter))
        
        result.append(')')
        
        return ''.join(result)
    
    __call__ = execute

class Client(UserBase):
    """
    Discord client class used to interact with the Discord API.
    
    Attributes
    ----------
    id : `int`
        The client's unique identificator number.
    name : str
        The client's username.
    discriminator : `int`
        The client's discriminator. Given to avoid overlapping names.
    avatar_hash : `int`
        The client's avatar's hash in `uint128`.
    avatar_type : `bool`
        The client's avatar's type.
    guild_profiles : `dict` of (``Guild``, ``GuildPorfile``) items
        A dictionary, which contains the client's guild profiles. If a client is member of a guild, then it should
        have a respective guild profile accordingly.
    is_bot : `bool`
        Whether the client is a bot or a user account.
    partial : `bool`
        Partial clients have only their id set. If any other data is set, it might not be in sync with Discord.
    activities : `list` of ``AcitvityBase`` instances
        A list of the client's activities.
    status : `Status`
        The client's display status.
    statuses : `dict` of (`str`, `str`) items
        The client's statuses for each platform.
    email : `str`
        The client's email. Defaults to empty string.
    flags : ``UserFlag``
        The client's user flags.
    locale : `str`
        The preferred locale by the client.
    mfa : `bool`
        Whether the client has two factor authorization enabled on the account.
    premium_type : ``PremiumType``
        The Nitro subscription type of the client.
    system : `bool`
        Whether the client is an Official Discord System user (part of the urgent message system).
    verified : `bool`
        Whether the email of the client is verified.
    application : ``Application``
        The bot account's application. The application data of the client is requested menwhile it logs in.
    events : ``EventDescriptor``
        Contains the event handlers of the client. New event handlers can be added through it as well.
    gateway : ``DiscordGateway`` or ``DiscordGatewaySharder``
        The gateway of the client towards Discord. If the client uses sharding, then ``DiscordGatewaySharder`` is used
        as gateway.
    http : ``DiscordHTTPClient``
        The http session of the client. Can be used as a normal http session, or for lower level interactions with the
        Discord API.
    intents : ``IntentFlag``
        The intent flags of the client.
    private_channels : `dict` of (`int`, ``ChannelPrivate``) items
        Stores the private channels of the client. The channels' other recipement' ids are the keys, meanwhile the
        channels are the values.
    group_channels : `dict` of (`int`, ``ChannelGroup``) items
        The group channels of the client. They can be accessed by their id as the key.
    ready_state : ``ReadyState`` or `None`
        The client on login in fills up it's `.ready_state` with ``Guild`` objects, which will have their members
        requested.
    relationships : `dict` of (`int`, ``Relationship``) items
        Stores the relationships of the client. The relationships' users' ids are the keys and the relationships
        themselves are the values.
    running : `bool`
        Whether the client is running or not. When the client is stopped, this attribute is set as `False` what causes
        it's heartbeats to stop and it's gateways to close and not reconnect.
    secret : `str`
        The client's secret used when interacting with oauth2 endpoints.
    shard_count : `int`
        The client's shardcount. Set as `0` if the is not using sharding.
    token : `str`
        The client's token.
    voice_clients : `dict` of (`int`, ``VoiceClient``) items
        Each bot can join a channel at every ``Guild`` and meanwhile they do, they have an active voice client for that
        guild. This attribute stores these voice clients. They keys are the guilds' ids, meanwhile the values are
        the voice clients.
    _activity : ``ActivityBase`` instance
        The client's preffered activity.
    _additional_owner_ids : `None` or `set` of `int`
        Additional users' (as id) to be passed by the ``.is_owner`` check.
    _gateway_url : `str`
        Cached up gateway url, what is invalidated after `1` minute. Used to avoid unnecessary requests when launching
        up more shards.
    _gateway_requesting : `bool`
        Whether the client alredy requests it's gateway.
    _gateway_time : `float`
        The last timestamp when `._gateway_url` was updated.
    _gateway_max_concurrency : `int`
        The max amount of shards, which can be launched at the same time.
    _gateway_waiter : `None` or `Future`
        When client gateway is being requested multiple times at the same time, this future is set and awaited at the
        secondary requests.
    _status : ``Status``
        The client's preferred status.
    _user_chunker_nonce : `int`
        The last nonce in int used for requesting guild user chunks. The default value is 0, what means the next
        request will start at 1. Nonce 0 is allocated for the case, when all the guild's user is requested.
    
    Class Attributes
    ----------------
    loop : ``EventThread``
        The eventloop of the client. Every client uses the same one.
    
    See Also
    --------
    UserBase : The superclass of ``Client`` and of other user classes.
    User : The default type of Discord users.
    Webhook : Discord webhook entity.
    WebhookRepr : Discord webhook's user representation.
    UserOA2 : A user class with extended oauth2 attributes.
    
    Notes
    -----
    Client supports weakreferencig and dynamic attribute names as well for extension support.
    """
    __slots__ = (
        'guild_profiles', 'is_bot', 'partial', #default user
        'activities', 'status', 'statuses', #presence
        'email', 'flags', 'locale', 'mfa', 'premium_type', 'system', 'verified', # OAUTH 2
        '__dict__', '_additional_owner_ids', '_activity', '_gateway_requesting', '_gateway_time', '_gateway_url',
        '_gateway_max_concurrency', '_gateway_waiter', '_status', '_user_chunker_nonce', 'application', 'events',
        'gateway', 'http', 'intents', 'private_channels', 'ready_state', 'group_channels', 'relationships', 'running',
        'secret', 'shard_count', 'token', 'voice_clients', )
    
    loop = KOKORO
    
    def __new__(cls, token, secret=None, client_id=0, activity=ActivityUnknown, status=None, is_bot=True,
            shard_count=0, intents=-1, additional_owners=None, **kwargs):
        """
        Parameters
        ----------
        token : `str`
            A valid Discord token, what the client can use to interact with the Discord API.
        secret: `str`, optional
            Client secret used when interacting with oauth2 endpoints.
        client_id : `int` ir `str`, optional
            The client's `.id`. If passed as `str` will be converted to `int`.
            When more `Client` is started up, it is recommended to define their id initially. The wrapper can detect the
            clients' id-s only when they are logging in, so the wrapper  needs to check if a ``User`` alterego of the client
            exists anywhere, and if does will replace it.
        activity : ``ActivityBase``, optional
            The client's preferred activity.
        status : `str` or ``Status``, optional
            The client's preferred status.
        is_bot : `bool`, optional
            Whether the client is a bot user or a user account. Defaults to False.
        shard_count : `int`, optional
            The client's shard count. If passed as lower as the recommended one, will reshard itself.
        intents : ``IntentFlag``, optional
             By default the client will launch up using all the intent flags. Negative values will be interpretered as
             using all the intents, meanwhile if passed as positive, non existing intent flags are removed.
        **kwargs : keyword arguments
            Additional predefined attributes for the client.
        
        Other Parameters
        ----------------
        name : `str`, Optional
            The client's ``.name``.
        discriminator : `int` or `str` instance, Optional
            The client's ``.discriminator``. Is accepted as `str` instance as well and will be converted to `int`.
        avatar : `None`, ``Icon`` or `str`, Optional
            The client's avatar. Mutually exclusive with `avatar_type` and `avatar_hash`.
        avatar_type : ``Icontype``, Optional
            The client's avatar's type. Mutually exclusive with `avatar_type`.
        avatar_hash : `int`, Optional
            The client's avatar hash. Mutually exclusive with `avatar`.
        flags : ``UserFlag`` or `int` instance, Optional
            The client's ``.flags``. If not passed as ``UserFlag``, then will be converted to it.
        
        Returns
        -------
        client : ``Client``
        
        Raises
        ------
        TypeError
            If any argument's type is bad or if unexpected argument is passed.
        ValueError
            If an argument's type is good, but it's value is unacceptable.
        """
        # token
        if (type(token) is str):
            pass
        elif isinstance(token,str):
            token = str(token)
        else:
            raise TypeError(f'`token` can be passed as `str` instance, got {token!r}.')
        
        # secret
        if (secret is None) or type(secret is str):
            pass
        elif isinstance(secret,str):
            secret = str(secret)
        else:
            raise TypeError(f'`secret` can be passed as `str` instance, got `{secret.__class__.__name__}`.')
        
        # client_id
        client_id = preconvert_snowflake(client_id, 'client_id')
        
        # activity
        if (not isinstance(activity, ActivityBase)) or (type(activity) is ActivityCustom):
            raise TypeError(f'`activity` should have been passed as `{ActivityBase.__name__} instance (except {ActivityCustom.__name__}), got: {activity.__class__.__name__}.')
        
        # status
        if (status is not None):
            status = preconvert_preinstanced_type(status, 'status', Status)
            if status is Status.offline:
                status = Status.invisible
        
        # is_bot
        is_bot = preconvert_bool(is_bot, 'is_bot')
        
        # shard count
        if (type(shard_count) is int):
            pass
        elif isinstance(shard_count, int):
            shard_count = int(shard_count)
        else:
            raise TypeError(f'`shard_count` should have been passed as `int` instance, got {shard_count.__class__.__name__}.')
        
        if shard_count<0:
            raise ValueError(f'`shard_count` can be passed only as non negative `int`, got {shard_count!r}.')
        
        # Default to `0`
        if shard_count == 1:
            shard_count = 0
        
        # intents
        intents = preconvert_flag(intents, 'intents', IntentFlag)
        
        # additonal owners
        if additional_owners is None:
            additional_owner_ids = None
        else:
            iter_ = getattr(additional_owners, '__iter__', None)
            if iter_ is None:
                raise TypeError('`additional_owners` should have been passed as `iterable`, got '
                    f'{additional_owners.__class__.__name__}.')
            
            additional_owner_ids = set()
            
            index = 1
            for additional_owner in iter_(additional_owners):
                index+=1
                if not isinstance(additional_owner,(int,UserBase)):
                    raise TypeError(f'User {index} at `additional_owners`  was not passed neither as `int` or as '
                        f'`{UserBase.__name__}` instance, got {additional_owner.__class__.__name__}')
                
                if type(additional_owner) is int:
                    pass
                elif isinstance(additional_owner, int):
                    additional_owner = int(additional_owner)
                else:
                    additional_owner = additional_owner.id
                
                additional_owner_ids.add(additional_owner)
            
            if (not additional_owner_ids):
                additional_owner_ids = None
        
        # kwargs
        if kwargs:
            processable = []
            # kwargs.name
            try:
                name = kwargs.pop('name')
            except KeyError:
                pass
            else:
                name = preconvert_str(name, 'name', 2, 32)
                processable.append(('name', name))
            
            # kwargs.discriminator
            try:
                discriminator = kwargs.pop('discriminator')
            except KeyError:
                pass
            else:
                discriminator = preconvert_discriminator(discriminator)
                processable.append(('discriminator', discriminator))
            
            # kwargs.avatar & kwargs.avatar_type & kwargs.avatar_hash
            cls.avatar.preconvert(kwargs, processable)
            
            # kwargs.flags
            try:
                flags = kwargs.pop('flags')
            except KeyError:
                pass
            else:
                flags = preconvert_flag(flags, 'flags', UserFlag)
                processable.append(('flags', flags))
            
            if kwargs:
                raise TypeError(f'Unused or unsettable attributes: {kwargs}.')
        
        else:
            processable = None
        
        if (status is None):
            _status = Status.online
        else:
            _status = status
        
        self = object.__new__(cls)
        
        self.name               = ''
        self.discriminator      = 0
        self.avatar_type        = ICON_TYPE_NONE
        self.avatar_hash        = 0
        self.flags              = UserFlag()
        self.mfa                = False
        self.system             = False
        self.verified           = False
        self.email              = ''
        self.premium_type       = PremiumType.none
        self.locale             = DEFAULT_LOCALE
        self.token              = token
        self.secret             = secret
        self.is_bot             = is_bot
        self.shard_count        = shard_count
        self.intents            = intents
        self.running            = False
        self.relationships      = {}
        self.guild_profiles     = {}
        self._status            = _status
        self.status             = Status.offline
        self.statuses           = {}
        self._activity          = activity
        self.activities         = []
        self._additional_owner_ids = additional_owner_ids
        self._gateway_url       = ''
        self._gateway_time      = -inf
        self._gateway_max_concurrency = 1
        self._gateway_requesting = False
        self._gateway_waiter    = None
        self._user_chunker_nonce= 0
        self.group_channels     = {}
        self.private_channels   = {}
        self.voice_clients      = {}
        self.id                 = client_id
        self.partial            = True
        self.ready_state        = None
        self.application        = Application()
        self.gateway            = (DiscordGatewaySharder if shard_count else DiscordGateway)(self)
        self.http               = DiscordHTTPClient(self)
        self.events             = EventDescriptor(self)
        
        if (processable is not None):
            for item in processable:
                setattr(self, *item)
        
        CLIENTS.append(self)
        
        if client_id:
            USERS[client_id]    = self
        
        return self
    
    def _init_on_ready(self, data):
        """
        Fills up the client's instance attributes on login. If there is an already existing User object with the same
        id, the client will replace it at channel participans, at ``USERS`` weakreference dictionary, at
        ``guild.users`` and at permission overwrites. This replacing is avoidable, if at the creation of the client
        the ``.client_id`` argument is set.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data requested from Discord by the ``.client_login_static`` method.
        """
        client_id           = int(data['id'])
        if self.id!=client_id:
            CLIENTS.update(self,client_id)
        
        # GOTO
        while True:
            if CACHE_USER:
                try:
                    alterego        = USERS[client_id]
                except KeyError:
                    # Go Out
                    break
                else:
                    if alterego is not self:
                        #we already exists, we need to go tru everthing and replace ourself.
                        guild_profiles=alterego.guild_profiles
                        self.guild_profiles=guild_profiles
                        for guild in guild_profiles:
                            guild.users[client_id] = self
                            for channel in guild.channels:
                                for overwrite in channel.overwrites:
                                    if overwrite.target is alterego:
                                        overwrite.target=self
            
            # This part should run at both case, except when there is no alterego detected when caching users.
            for client in CLIENTS:
                if (client is self) or (not client.running):
                    continue
                
                for channel in client.group_channels.values():
                    users = channel.users
                    for index in range(len(users)):
                        if users[index].id == client_id:
                            users[index] = self
                            break
                
                for channel in client.private_channels.values():
                    users = channel.users
                    for index in range(len(users)):
                        if users[index].id == client_id:
                            users[index] = self
                            break
            
            break
        
        self.name           = data['username']
        self.discriminator  = int(data['discriminator'])
        self._set_avatar(data)
        self.mfa            = data.get('mfa_enabled',False)
        self.system         = data.get('system',False)
        self.verified       = data.get('verified',False)
        self.email          = data.get('email','')
        self.flags          = UserFlag(data.get('flags',0))
        self.premium_type   = PremiumType.INSTANCES[data.get('premium_type',0)]
        self.locale         = parse_locale(data)
        
        self.partial        = False
        
        USERS[client_id]=self
    
    _update_presence    = User._update_presence
    _update_presence_no_return = User._update_presence_no_return
    
    @property
    def _platform(self):
        """
        Returns the client's local platform.
        
        Returns
        -------
        platform : `str`
            The platform's name or empty string if the client's status is offline or invisible.
            
        Notes
        -----
        Custom client's status is always `'web'`, so other than `''` or `'web'` will not be returned.
        """
        if self.status in (Status.offline,Status.invisible):
            return ''
        return 'web'
    
    async def client_edit(self, password=None, new_password=None, email=None, house=_spaceholder, name=None,
            avatar=_spaceholder):
        """
        Edits the client. Only the provided parameters will be changed. Every argument what refers to a user
        account is not tested.
        
        Parameters
        ----------
        password : `str`, Optional
            The actual password of the client. A must for user accounts.
        new_password : `str`, Optional
            User account only argument.
        email : `str`, Optional
            User account only argument.
        house : ``HypesquadHouse`` or `None`, Optional
            User account only argument.
        name : `str`, Optional
            The client's new name.
        avatar : `bytes-like` or `None`, Optional
            An `'jpg'`, `'png'`, `'webp'` image's raw data. If the client is premium account, then it can be
            `'gif'` as well. By passing `None` you can remove the client's current avatar.
        
        Raises
        ------
        ValueError
            - If `password` is not passed when the client is a user account.
            - If the length of the `name` is not between 2 and 32.
            - If `avatar` is passed as `bytes-like` and it's format is `'gif'`, meanwhile the user is not premium.
            - If `avatar` is passed and it's format is not any of the expected ones.
        TypeError
            - If `name` was not passed as str instance.
            - If `avatar` was not passed as `bytes-like` or as `None`.
        ConnectionError
            No internet connection.
        DiscordException
        
        Notes
        -----
        The method's endpoint has long ratelimit reset, so consider using timeout and checking ratelimits with
        ``RatelimitProxy``.
        """
        data={}
        
        if (password is None):
            if not self.is_bot:
                raise ValueError('Password is must for non bots!')
        else:
            data['password']=password

        if (name is None):
            pass
        elif isinstance(name,str):
            name_ln=len(name)
            if name_ln<2 or name_ln>32:
                raise ValueError(f'The length of the name can be between 2-32, got {name_ln}')
            data['username']=name
        else:
            raise TypeError(f'`name` can be passed as type str, got {name.__class__.__name__}.')
        
        if (avatar is not _spaceholder):
            if avatar is None:
                avatar_data = None
            else:
                avatar_type = avatar.__class__
                if not issubclass(avatar_type, (bytes, bytearray, memoryview)):
                    raise TypeError(f'`avatar` can be passed as `bytes-like` or None, got {avatar_type.__name__}.')
            
                extension = get_image_extension(avatar)
                if extension not in VALID_ICON_FORMATS_EXTENDED:
                    raise ValueError(f'Invalid image extension: `{extension}`.')
                
                if (not self.premium_type.value) and (extension == 'gif'):
                    raise ValueError('Only premium users can have `gif` avatar!')
                
                avatar_data = image_to_base64(avatar)
            
            data['avatar'] = avatar_data
        
        if not self.is_bot:
            if (email is not None):
                data['email']=email
            if (new_password is not None):
                data['new_password']=new_password
        
        data = await self.http.client_edit(data)
        self._update_no_return(data)
        
        if not self.is_bot:
            self.email=data['email']
            try:
                self.token=data['token']
            except KeyError:
                pass
        
        if house is _spaceholder:
            pass
        elif house is None:
            await self.hypesquad_house_leave()
        else:
            await self.hypesquad_house_change(house)
    
    async def client_edit_nick(self, guild, nick, reason=None):
        """
        Changes the client's nick at the specified Guild. A nick name's length can be between 1-32. An extra argument
        reason is accepted as well, what will show zp at the respective guild's audit logs.
        
        Parameters
        ----------
        guild : ``Guild``
            The guild where the client's nickname will be changed.
        nick : `str` or `None`
            The client's new nickname. Pass it as `None` or with length `0` to remove it.
        reason : `str`, Optional
            Will show up at the respective guild's audit logs.
        
        Raises
        ------
        ValueError
            If the nick's length is over `32`.
        TypeError
            If the nick is not `None` or `str` instance.
        ConnectionError
            No internet connection.
        DiscordException
        
        Notes
        -----
        No request is done if the client's actual nickname at the guild is same as the method would change it too.
        """
        if (nick is None):
            pass
        elif isinstance(nick, str):
            nick_ln=len(nick)
            if nick_ln>32:
                raise ValueError(f'The length of the `nick` can be between 1-32, got {nick_ln}')
            if nick_ln==0:
                nick=None
        else:
            raise TypeError(f'`nick` can be str instance, got {nick.__class__.__name__}')
        
        try:
            actual_nick=self.guild_profiles[guild].nick
        except KeyError:
            # we arent at the guild ->  will raise propably
            should_edit_nick=True
        else:
            if nick is None:
                if actual_nick is None:
                    should_edit_nick=False
                else:
                    should_edit_nick=True
            else:
                if actual_nick is None:
                    should_edit_nick=True
                elif nick==actual_nick:
                    should_edit_nick=False
                else:
                    should_edit_nick=True
        
        if should_edit_nick:
            await self.http.client_edit_nick(guild.id,{'nick':nick},reason)

    async def client_connections(self):
        """
        Requests the client's connections. For a bot account this request will always return an empty list.
        
        Returns
        -------
        connections : `list` of ``Connection`` objects
        
        Raises
        ------
        ConnectionError
            No internet connection.
        """
        data = await self.http.client_connections()
        return [Connection(connection_data) for connection_data in data]

    async def client_edit_presence(self, activity=None, status=None, afk=False):
        """
        Changes the client's presence (status and activity). If a parameter is not defined, it will not be changed.
        
        Parameters
        ----------
        activity : ``ActivityBase`` instance, Optional
            The new activity of the Client.
        status : `str` or ``Status``, Optional
            The new status of the client.
        afk : `bool`, Optional
            Whether the client is afk or not (?).
        
        Raises
        ------
        TypeError:
            - If the status is not `str` or ``Status`` instance.
            - If activity is not ``ActivityBase`` instance, except ``ActivityCustom``.
        ValueError:
            - If the status `str` instance, but not any of the predefined ones.
        """
        if status is None:
            status=self._status
        elif isinstance(status,str):
            try:
                status=Status.INSTANCES[status]
            except KeyError as err:
                raise ValueError(f'Invalid status {status}') from err
            self._status=status
        elif isinstance(status,Status):
            self._status=status
        else:
            raise TypeError(f'`status` can be type `str` or `{Status.__name__}`, got {status.__class__.__name__}')
        
        status=status.value
        
        if activity is None:
            activity=self._activity
        elif isinstance(activity, ActivityBase) and (type(activity) is not ActivityCustom):
            self._activity=activity
        else:
            raise TypeError(f'`activity` should have been passed as `{ActivityBase.__name__} instance (except {ActivityCustom.__name__}), got: {activity.__class__.__name__}.')
        
        if activity is ActivityUnknown:
            activity=None
        elif (activity is not None):
            if self.is_bot:
                activity=activity.botdict()
            else:
                activity=activity.hoomandict()
        
        if status=='idle':
            since=int(time_now()*1000.)
        else:
            since=0.0
        
        data = {
            'op': DiscordGateway.PRESENCE,
            'd' : {
                'game'  : activity,
                'since' : since,
                'status': status,
                'afk'   : afk,
                    },
                }
        
        await self.gateway.send_as_json(data)
    
    async def activate_authorization_code(self, redirect_url, code, scopes):
        """
        Activates a user's oauth2 code.
        
        Parameters
        ----------
        redirect_url : `str`
            The url, where the activation page redirected to.
        code : `str`
            The code, what is included with the redirect url after a successfull activation.
        scopes : `list` of `str`
            A list of oauth2 scopes to request.
        
        Returns
        -------
        access : ``OA2Access`` or `None`
            If the code, the redirect url or the scopes are invalid, the methods returns `None`.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        
        See Also
        --------
        parse_oauth2_redirect_url : Parses `redirect_url` and the `code` from a full url.
        """
        data = {
            'client_id'     : self.id,
            'client_secret' : self.secret,
            'grant_type'    : 'authorization_code',
            'code'          : code,
            'redirect_uri'  : redirect_url,
            'scope'         : ' '.join(scopes),
                }
        
        data = await self.http.oauth2_token(data, multidict_titled())
        if len(data)==1:
            return
        
        return AO2Access(data,redirect_url)
    
    async def owners_access(self, scopes):
        """
        Similar to ``.activate_authorization_code``, but it requests the application's owner's access. It does not
        requires the redirect_url and the code argument either.
        
        Parameters
        ----------
        scopes : `list` of `str`
            A list of oauth2 scopes to request.
        
        Returns
        -------
        access : ``OA2Access``
            The oauth2 access of the client's application's owner.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        
        Notes
        -----
        Does not work if the client's application is owned by a team.
        """
        data = {
            'grant_type'    : 'client_credentials',
            'scope'         : ' '.join(scopes),
                }
        
        headers = multidict_titled()
        headers[AUTHORIZATION] = BasicAuth(str(self.id), self.secret).encode()
        data = await self.http.oauth2_token(data, headers)
        return AO2Access(data,'')
    
    #needs `email` or/and `identify` scopes granted for more data
    async def user_info(self, access):
        """
        Request the a user's information with oauth2 access token. By default a bot account should be able to request
        every public infomation about a user (but you do not need oauth2 for that). If the access token has email
        or/and identify scopes, then more information should show up like this.
        
        Parameters
        ----------
        access : ``AO2Access`` or ``UserOA2``
        
        Returns
        -------
        oauth2_user : ``UserOA2``
            The requested user object.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        headers=multidict_titled()
        headers[AUTHORIZATION]=f'Bearer {access.access_token}'
        data = await self.http.user_info(headers)
        return UserOA2(data,access)
    
    async def user_connections(self, access):
        """
        Requests a user's connections. This method will work only if the access token has the `'connections'` scope. At
        the returned list includes the user's hidden connections as well.
        
        Parameters
        ----------
        access : ``AO2Access`` or ``UserOA2``
        
        Returns
        -------
        connections : `list` of ``Connection`` objects
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        headers=multidict_titled()
        headers[AUTHORIZATION]=f'Bearer {access.access_token}'
        data = await self.http.user_connections(headers)
        return [Connection(connection_data) for connection_data in data]
    
    async def renew_access_token(self, access):
        """
        Renews the access token of an ``OA2Access``.
        
        Parameters
        ----------
        access : ``AO2Access`` or ``UserOA2``
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        
        Notes
        -----
        By default access tokens expire after one week.
        """
        redirect_url = access.redirect_url
        if redirect_url:
            data = {
                'client_id'     : self.id,
                'client_secret' : self.secret,
                'grant_type'    : 'refresh_token',
                'refresh_token' : access.refresh_token,
                'redirect_uri'  : redirect_url,
                'scope'         : ' '.join(access.scopes)
                    }
        else:
            data = {
                'client_id'     : self.id,
                'client_secret' : self.secret,
                'grant_type'    : 'client_credentials',
                'scope'         : ' '.join(access.scopes),
                    }
        
        data = await self.http.oauth2_token(data, multidict_titled())
        
        access._renew(data)
    
    async def guild_user_add(self, guild, access_or_compuser, user=None, nick=None, roles=[], mute=False, deaf=False):
        """
        Adds the passed to the guild. The user must have granted you the `'guilds.join'` oauth2 scope.
        
        Parameters
        ----------
        guild : ``Guild``
            The guild, where the user is going to be added.
        access_or_compuser: ``OA2Access`` or ``UserOA2``
            The access of the user, who will be addded.
        user : ``User``, Optional
            Defines which user will be added to the guild. The `access_or_compuser` must refer to this specified user.
            This field is optional, if access is passed as an ``UserOA2`` object.
        nick : `str`, Optional
            The nickname, which with the user will be added.
        roles : `list` of ``Role`` objects, Optional
            The user will be added with the specified roles.
        mute : `bool`, Optional
            Whether the user should be added as muted.
        deaf : `bool`, Optional
            Whether the user should be added as deafen.
        
        Raises
        ------
        ValueError
            - Nick was passed as `str` and it's length is over 32.
        TypeError:
            - If user was passed as None and `access_or_compuser` was passed as ``AO2Access``.
            - If access_or_compuser was not passed as ``AO2Access``, neither ``UserOA2``.
        ConnectionError
            No internet connection.
        DiscordException
        """
        if type(access_or_compuser) is AO2Access:
            access=access_or_compuser
            if user is None:
                raise TypeError('`user` can not be None if `access_or_compuser` is passed as `AO2Access`.')
        elif type(access_or_compuser) is UserOA2:
            access=access_or_compuser.access
            if user is None:
                user=access_or_compuser
        else:
            raise TypeError(f'Invalid `access_or_compuser` type, expected {AO2Access.__name__} or {UserOA2.__name__}, got {access_or_compuser.__class__.__name__}.')
        
        data={'access_token':access.access_token}
        if (nick is not None):
            nick_ln=len(nick)
            if nick_ln!=0:
                if nick_ln>32:
                    raise ValueError(f'The length of the nick can be between 1-32, got {nick!r}.')
                data['nick']=nick
        
        if roles:
            data['roles']=[role.id for role in roles]
        
        if mute:
            data['mute']=mute
        
        if deaf:
            data['deaf']=deaf
        
        await self.http.guild_user_add(guild.id,user.id,data)
    
    async def user_guilds(self, access):
        """
        Requests a user's guilds with it's ``OA2Access``. The user must provide the `'guilds'` oauth2  scope for this
        request to succeed.
        
        Parameters
        ----------
        access: ``OA2Access`` or ``UserOA2``
            The access of the user, who's guilds will be requested.
        
        Returns
        -------
        guilds : `list of ``Guild`` objects
            The guilds of the respective user. Not loaded guilds will show up as partial ones.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        headers=multidict_titled()
        headers[AUTHORIZATION]=f'Bearer {access.access_token}'
        data = await self.http.user_guilds(headers)
        return [PartialGuild(guild_data) for guild_data in data]
    
    async def achievement_get_all(self):
        """
        Requests all the achievements of the client's application and returns them.
        
        Returns
        -------
        achievements : `list` of ``Achievement`` objects
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        data = await self.http.achievement_get_all(self.application.id)
        return [Achievement(achievement_data) for achievement_data in data]
    
    async def achievement_get(self, achievement_id):
        """
        Requests one of the client's achievements by it's id.
        
        Returns
        -------
        achievement : ``Achievement``
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        data = await self.http.achievement_get(self.application.id, achievement_id)
        return Achievement(data)
    
    async def achievement_create(self, name, description, icon, secret=False, secure=False):
        """
        Creates an achievment for the client's application and returns it.
        
        Parameters
        ----------
        name : `str`
            The achievement's name.
        description : `str`
            The achievement's description.
        icon : `bytes-like`
            The achievement's icon. Can have `'jpg'`, `'png'`, `'webp'` or `'gif'` format.
        secret : `bool`, Optional
            Secret achievements will *not* be shown to the user until they've unlocked them.
        secure : `bool`, Optional
            Secure achievements can only be set via HTTP calls from your server, not by a game client using the SDK.
        
        Returns
        -------
        achievement : ``Achievement``
            The created achievement entity.
        
        Raises
        ------
        ValueError
            If the ``icon``'s format is not any of the expected ones.
        TypeError
            If ``icon`` was not passed as `bytes-like`.
        ConnectionError
            No internet connection.
        DiscordException
        """
        icon_type = icon.__class__
        if not issubclass(icon_type, (bytes, bytearray, memoryview)):
            raise TypeError(f'`icon` can be passed as `bytes-like`, got {icon_type.__name__}.')
        
        extension = get_image_extension(icon)
        if extension not in VALID_ICON_FORMATS_EXTENDED:
            raise ValueError(f'Invalid icon type: `{extension}`.')
        
        icon_data = image_to_base64(icon)
        
        data = {
            'name'          : {
                'default'   : name,
                    },
            'description'   : {
                'default'   : description,
                    },
            'secret'        : secret,
            'secure'        : secure,
            'icon'          : icon_data,
                }
        
        data = await self.http.achievement_create(self.application.id,data)
        return Achievement(data)
    
    async def achievement_edit(self, achievement, name=None ,description=None, secret=None, secure=None,
            icon=_spaceholder):
        """
        Edits the passed achievemnt with the specified parameters. All parameter is optional.
        
        Parameters
        ----------
        achievement : ``Achievement``
            The achievement, what will be edited.
        name : `str`, Optional
            The new name of the achievement.
        description : `str`, Optional
            The achievemnt's new description.
        secret : `bool`, Optional
            The achievement's new secret value.
        secure : `bool`, Optional
            The achievement's new secure value.
        icon : `bytes-like`, Optional
            The achievement's new icon.
        
        Returns
        -------
        achievement : ``Achievement``
            After a successful edit, the passed achievement is updated and returned.
        
        Raises
        ------
        ValueError
            If the ``icon``'s format is not any of the expected ones.
        TypeError
            If ``icon`` was not passed as `bytes-like`.
        ConnectionError
            No internet connection.
        DiscordException
        """
        data={}
        
        if (name is not None):
            data['name'] = {
                'default'   : name,
                    }
        
        if (description is not None):
            data['description'] = {
                'default'   : description,
                    }
        
        if (secret is not None):
            data['secret']=secret
        
        if (secure is not None):
            data['secure']=secure
        
        if (icon is not _spaceholder):
            icon_type = icon.__class__
            if not issubclass(icon_type, (bytes, bytearray, memoryview)):
                raise TypeError(f'`icon` can be passed as `bytes-like`, got {icon_type.__name__}.')
            
            extension = get_image_extension(icon)
            if extension not in VALID_ICON_FORMATS_EXTENDED:
                raise ValueError(f'Invalid icon type: `{extension}`.')
            
            data['icon'] = image_to_base64(icon)
        
        data = await self.http.achievement_edit(self.application.id,achievement.id,data)
        achievement._update_no_return(data)
        return achievement
    
    async def achievement_delete(self, achievement):
        """
        Deletes the passed achievement.
        
        Parameters
        ----------
        achievement : ``Achievement``
            The achievement to delete.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        await self.http.achievement_delete(self.application.id,achievement.id)
    #
    # This endpoint is unintentionally documented and will never work
    # https://github.com/discordapp/discord-api-docs/issues/1230
    
    # DiscordException UNAUTHORIZED (401): 401: Unauthorized
    async def user_achievements(self, access):
        """
        Requests the achievements of a user with it's oauth2 access.
        
        Parameters
        ----------
        access : ``OA2Access`` or ``UserOA2``
            The access of the user, who's achievements will be requested.
        
        Returns
        -------
        achievements : `list` of ``Achievement`` objects
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        
        Notes
        -----
        This endpoint is unintentionally documented and will never work. For reference:
        ``https://github.com/discordapp/discord-api-docs/issues/1230``.
        """
        headers=multidict_titled()
        headers[AUTHORIZATION]=f'Bearer {access.access_token}'
        
        data = await self.http.user_achievements(self.application.id,headers)
        return [Achievement(achievement_data) for achievement_data in data]
    
    # https://github.com/discordapp/discord-api-docs/issues/1230
    # Seems like first update must come from game SDK.
    # Only secure updates are supported, if they are even.
    
    # when updating secure achievement:
    #     DiscordException NOT FOUND (404), code=10029: Unknown Entitlement
    # when updating non secure:
    #     DiscordException FORBIDDEN (403), code=40001: Unauthorized
    async def user_achievement_update(self, user, achievement, percent_complete):
        """
        Updates the `user`'s achievement with the given percentage. The  achevement should be `secure`. This
        method only updates the achievement's percentage.
        
        Parameters
        ----------
        user : ``User`` or ``Client``
            The user, who's achievement will be updated.
        achievement : ``Achievement``
            The achievement, which's state will be updated
        percent_complete : `int`
            The completion percentage of the achievement.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        
        Notes
        -----
        This endpoint cannot grant achievement, but can it even update them?. For reference:
        ``https://github.com/discordapp/discord-api-docs/issues/1230``.
        """
        data={'percent_complete':percent_complete}
        await self.http.user_achievement_update(user.id,self.application.id,achievement.id,data)
    
    #hooman only
    async def application_get(self, application_id):
        """
        Requst a specific application by it's id.
        
        Parameters
        ----------
        application_id : `int`
            The `id` of the application to request.

        Returns
        -------
        application : ``Application``
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        
        Notes
        -----
        This endpoint does not support bot accounts.
        """
        data = await self.http.application_get(application_id)
        return Application(data)
    
    def _delete(self):
        """
        Cleares up the client's references. By default this is not called when a client is stopped. This method should
        be used when you want to get rid of every allocated objects by the client. Take care, local modules might still
        have active references to the client or to some other objects, what could cause them to not garbage collect.
        
        Raises
        ------
        RuntimeError
            If called when the client is still running.
        
        Examples
        --------
        >>> from hata import Client, GUILDS
        >>> import gc
        >>> TOKEN = 'a token goes here'
        >>> client = Client(TOKEN)
        >>> client.start()
        >>> len(GUILDS)
        4
        >>> client.stop()
        >>> client._delete()
        >>> client = None
        >>> gc.collect()
        680
        >>> len(GUILDS)
        0
        """
        if self.running:
            raise RuntimeError(f'{self.__class__.__name__}._delete called from a running client.')

        CLIENTS.remove(self)
        client_id=self.id
        alterego=object.__new__(User)
        for attrname in User.__slots__:
            if attrname.startswith('__'):
                continue
            setattr(alterego,attrname,getattr(self,attrname))
        
        if CACHE_USER:
            USERS[client_id]=alterego
            guild_profiles=self.guild_profiles
            for guild in guild_profiles:
                guild.users[client_id]=self
                for channel in guild.channels:
                    for overwrite in channel.overwrites:
                        if overwrite.target is alterego:
                            overwrite.target=self
            
            for client in CLIENTS:
                if (client is not self) and client.running:
                    for relationship in client.relationships:
                        if relationship.user is self:
                            relationship.user=alterego
                    
        else:
            try:
                del USERS[client_id]
            except KeyError:
                pass
            guild_profiles=self.guild_profiles
            for guild in guild_profiles:
                try:
                    del guild[client_id]
                except KeyError:
                    pass

        self.relationships.clear()
        for channel in self.group_channels.values():
            users=channel.users
            for index in range(users):
                if users[index].id==client_id:
                    users[index]=alterego
                    continue

        self.private_channels.clear()
        self.group_channels.clear()
        self.application._fillup()
        self.events.clear()
        
        self.guild_profiles     = {}
        self.status             = Status.offline
        self.statuses           = {}
        self._activity          = ActivityUnknown
        self.activities         = []
        self.ready_state        = None
    
    async def download_url(self,url):
        """
        Requests an url and returns the response's content. A shortcut option for doing a get request with the
        client's http and reading it.
        
        Parameters
        ----------
        url : `str`
            The url to request.

        Returns
        -------
        response_data : `bytes`
        
        Raises
        ------
        ConnectionError
            No internet connection.
        """
        async with self.http.get(url) as response:
            return (await response.read())

    async def download_attachment(self, attachment):
        """
        Downloads an attachment object's file. This method always prefers the proxy url of the attachment if applicable.
        
        Parameters
        ----------
        attachment : ``Attachment``
            The attachment object, which's file will be requested.
        
        Returns
        -------
        response_data : `bytes`
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        url = attachment.proxy_url
        if (url is None) or (not url.startswith(CDN_ENDPOINT)):
            url = attachment.url
        async with self.http.get(url) as response:
            return (await response.read())
    
    #loggin
    async def client_login_static(self):
        """
        The first step at loggin in is requesting the client's user data. This method is also used to check whether
        the token of the client is valid.
        
        Returns
        -------
        response_data : `dict` of (`str` : `Any`)
            Decoded json data got from Discord.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        InvalidToken
            When the token of the client is invalid.
        """
        while True:
            try:
                data = await self.http.client_user()
            except DiscordException as err:
                status = err.status
                if status == 401:
                    raise InvalidToken() from err
                
                if status >= 500:
                    sleep(2.5, KOKORO)
                    continue
                
                raise
            
            break
        
        return data
    
    #channels
    
    async def channel_group_leave(self, channel):
        """
        Leaves the client from the specified group channel.
        
        Parameters
        ----------
        channel : ``ChannelGroup``
            The channel to leave from.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        await self.http.channel_group_leave(channel.id)
    
    async def channel_group_user_add(self, channel, *users):
        """
        Adds the users to the given group channel.
        
        Parameters
        ----------
        channel : ``ChannelGroup``
            The channel to add the `users` to.
        *users : ``User`` or ``Client`` objects
            The users to add to the `channel`.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        for user in users:
            await self.http.channel_group_user_add(channel.id,user.id)

    async def channel_group_user_delete(self, channel, *users):
        """
        Removes the users from the given group channel.
        
        Parameters
        ----------
        channel : ``ChannelGroup``
            The channel from where the `users` will be removed.
        *users : ``User`` or ``Client`` objects
            The users to remove from the `channel`.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        for user in users:
            await self.http.channel_group_user_delete(channel.id,user.id)
    
    async def channel_group_edit(self, channel, name=_spaceholder, icon=_spaceholder):
        """
        Edits the given group channel. Only the provided parameters will be edited.
        
        Parameters
        ----------
        channel : ``ChannelGroup``
            The channel to edit.
        name : `None` or `str`, Optional
            The new name of the channel. By passing `None` or an empty string you can remove the actual one.
        icon : `None` or `bytes-like`, Optional
            The new icon of the channel. By passing `None` your can remove the actual one.
        
        Raises
        ------
        TypeError
            - If `name` is neither `None` or `str` instance.
            - If `icon` is neither `None` or `bytes-like`.
        ValueError
            - If `name` is passed as `str`, but it's length is `1`, or over `100`.
            - If `icon` is passed as `bytes-like`, but it's format is not any of the expected formats.
        ConnectionError
            No internet connection.
        DiscordException
        
        Notes
        -----
        No request is done if no optional paremeter is provided.
        """
        data={}
        
        if (name is not _spaceholder):
            if (name is None):
                pass
            elif isinstance(name, str):
                name_ln=len(name)
                if name_ln==1 or name_ln>100:
                    raise ValueError(f'`channel`\'s `.name`\'s length can be between 2-100, got {name!r}.')
                
                if name_ln==0:
                    name=None
            else:
                raise TypeError(f'`name` can be `None` or `str` instance, got {name.__class__.__name__}.')
            
            data['name']=name
        
        if (icon is not _spaceholder):
            if icon is None:
                icon_data = None
            else:
                icon_type = icon.__class__
                if not issubclass(icon_type, (bytes, bytearray, memoryview)):
                    raise TypeError(f'`icon` can be passed as `bytes-like`, got {icon_type.__name__}.')
            
                extension = get_image_extension(icon)
                if extension not in VALID_ICON_FORMATS:
                    raise ValueError(f'Invalid icon type: `{extension}`.')
                
                icon_data = image_to_base64(icon)
            
            data['icon'] = icon_data
        
        if data:
            await self.http.channel_group_edit(channel.id,data)
    
    #user only
    async def channel_group_create(self, users):
        """
        Creates a group channel with the given users.
        
        Parameters
        ----------
        users : `list` of (``Usser`` or ``Client``) objects
            The users to create the channel with.
        
        Returns
        -------
        channel : ``ChannelGroup``
            The created group channel.
        
        Raises
        ------
        ValueError
            If `users` contains less than 2 users.
        ConnectionError
            No internet connection.
        DiscordException
        
        Notes
        -----
        This endpoint does not support bot accounts.
        """
        if len(users)<2:
            raise ValueError('ChannelGroup must be created with 2 or more users')
        
        data={'recipients':[user.id for user in users]}
        data=await self.http.channel_group_create(self.id,data)
        return ChannelGroup(data,self)
    
    async def channel_private_create(self, user):
        """
        Parameters
        ----------
        user : ``User`` or ``Client`` object
            The user to create the private with.
        
        Returns
        -------
        channel : ``ChannelPrivate``
            The created private channel.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        try:
            channel=self.private_channels[user.id]
        except KeyError:
            data=await self.http.channel_private_create({'recipient_id':user.id})
            channel=ChannelPrivate(data,self)
        return channel

    #returns an empty list for bots
    async def channel_private_get_all(self):
        """
        Request the client's private + group channels and returns them in a list. At the case of bot accounts the
        request returns an empty list, so we skip it.
        
        Returns
        -------
        channnels : `list` of (``ChannelPrivate`` or ``ChannelGroup``) objects
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        result=[]
        if (not self.is_bot):
            data = await self.http.channel_private_get_all()
            for channel_data in data:
                channel=CHANNEL_TYPES[channel_data['type']](data,self)
                result.append(channel)
        
        return result

    async def channel_move(self, channel, visual_position, category=_spaceholder, lock_permissions=False, reason=None):
        """
        Moves a guild channel to the given visual position under it's category, or guild. If the algorithm can not
        place the channel exactly on that location, it will place it as close, as it can. If there is nothing to
        move, then the request is skipped.
        
        Parameters
        ----------
        channel : ``ChannelGuildBase`` instance
            The channel to be moved.
        visual_position : `int`
            The visual position where the channel should go.
        category : `None` or ``ChannelGroup`` or ``Guild``, Optional
            If not set, then the channel will keep it's current parent. If the argument is set ``Guild`` instance or to
            `None`, then the  channel will be moved under the guild itself, Or if passed as ``ChannelCategory.md``,
            then the channel will be moved under it.
        lock_permissions : `bool`, Optional
            If you want to sync the permissions with the new category set it to `True`. Defaults to `False`.
        reason : `str`, Optional
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        ValueError
            - If the `channel` would be between guilds.
            - If catgory channel would be moved under an other category.
        TypeError
            If `category` was not passed as `None`, or as ``Guild`` or ``ChannelCategory`` instance.
        ConnectionError
            No internet connection.
        DiscordException
        
        Notes
        -----
        This method also fixes the messy channel positions of Discord to an intuitive one.
        """
        guild = channel.guild
        if guild is None:
            return
        
        if category is _spaceholder:
            category=channel.category
        elif category is None:
            category=guild
        elif type(category) is Guild:
            if guild is not category:
                raise ValueError('Can not move channel between guilds!')
        elif type(category) is ChannelCategory:
            if category.guild is not guild:
                raise ValueError('Can not move channel between guilds!')
        else:
            raise TypeError(f'Invalid type {channel.__class__.__name__}')
        
        if type(channel) is type(category):
            raise ValueError('Cant move category under category!')
        
        if channel.category is category and category.channels.index(channel)==visual_position:
            return #saved 1 request
        
        #making sure
        visual_position=int(visual_position) 
        
        #quality python code incoming :ok_hand:
        ordered=[]
        indexes=[0,0,0,0,0,0,0] #for the 7 channel type (type 1 and 3 wont be used)

        #loop preparations
        outer_channels=guild.channels
        index_0=0
        limit_0=len(outer_channels)
        #inner loop preparations
        index_1=0
        #loop start
        while True:
            if index_0==limit_0:
                break
            channel_=outer_channels[index_0]
            #loop block start
            
            type_=channel_.type
            type_index=indexes[type_]
            indexes[type_]=type_index+1
            
            ordered.append((index_0,index_1,type_index,channel_),)
            
            if type_==4:
                #reset type_indexes
                indexes[0]=indexes[2]=indexes[5]=indexes[6]=0
                #loop preparations
                inner_channels=channel_.channels
                limit_1=len(inner_channels)
                #loop start
                while True:
                    if index_1==limit_1:
                        break
                    channel_=inner_channels[index_1]
                    #loop block start
                    
                    type_=channel_.type
                    type_index=indexes[type_]
                    indexes[type_]=type_index+1
                    
                    ordered.append((index_0,index_1,type_index,channel_),)
                    
                    #loop block end
                    index_1=index_1+1
                #reseting inner
                index_1=0
                #loop ended
            
            #loop block end
            index_0=index_0+1
        #loop ended
        
        #prepare loop
        index_0=0
        limit_0=len(ordered)
        #loop start
        while True:
            if index_0==limit_0:
                break
            info_line=ordered[index_0]
            #loop block start
            
            if info_line[3] is channel:
                original_position=index_0
                break

            #loop block end
            index_0=index_0+1
        #loop ended

        restricted_positions=[]
        
        index_0=0
        limit_0=len(ordered)
        last_index=-1
        if type(category) is Guild:
            #loop start
            while True:
                if index_0==limit_0:
                    break
                info_line=ordered[index_0]
                #loop block start
                
                if info_line[0]>last_index:
                    last_index+=1
                    restricted_positions.append(index_0)
                
                #loop block end
                index_0=index_0+1
            #loop ended
        else:
            #loop start
            while True:
                if index_0==limit_0:
                    break
                info_line=ordered[index_0]
                category_index=index_0 #we might need it
                #loop block start
                if info_line[3] is category:
                    index_0=index_0+1
                    #loop preapre
                    #loop start
                    while True:
                        if index_0==limit_0:
                            break
                        info_line=ordered[index_0]
                        #loop block start

                        if info_line[3].type==4:
                            break
                        restricted_positions.append(index_0)
                        
                        #loop block end
                        index_0=index_0+1
                    #loop ended
                    break
                
                #loop block end
                index_0=index_0+1
            #loop ended
                
        index_0=(4,2,0).index(channel.ORDER_GROUP)
        before=(4,2,0)[index_0:]
        after =(4,2,0)[:index_0+1]

        possible_indexes=[]
        if restricted_positions:
            #loop prepare
            index_0=0
            limit_0=len(restricted_positions)-1
            info_line=ordered[restricted_positions[index_0]]
            #loop at 0 block start
            
            if info_line[3].ORDER_GROUP in after:
                possible_indexes.append((0,restricted_positions[index_0],),)
                
            #loop at 0 block ended
            while True:
                if index_0==limit_0:
                    break
                info_line=ordered[restricted_positions[index_0]]
                #next step mixin
                index_0=index_0+1
                info_line_2=ordered[restricted_positions[index_0]]
                #loop block start

                if info_line[3].ORDER_GROUP in before and info_line_2[3].ORDER_GROUP in after:
                    possible_indexes.append((index_0,restricted_positions[index_0],),)

                #loop block end
            if limit_0:
                info_line=info_line_2
            #loop at -1 block start
            
            if info_line[3].ORDER_GROUP in before:
                possible_indexes.append((index_0+1,restricted_positions[index_0]+1,),)

            #loop at -1 block ended
            #loop ended
        else:
            #empty category
            possible_indexes.append((0,category_index+1,),)
            
        #GOTO start 
        while True:
            #GOTO block start
            
            #loop prepare
            index_0=0
            limit_0=len(possible_indexes)
            info_line=possible_indexes[index_0]
            
            #loop at 0 block start
            if info_line[0]>visual_position:
                result_position=info_line[1]
                
                #GOTO end 
                break
                #GOTO ended
            
            #loop at 0 block ended
            
            #setup GOTO from loop start
            end_goto=False
            #setup GOTO from loop ended
            
            index_0=index_0+1
            while True:
                if index_0==limit_0:
                    break
                info_line=possible_indexes[index_0]
                #loop block start

                if info_line[0]==visual_position:
                    result_position=info_line[1]
                    
                    #GOTO end inner 1
                    end_goto=True
                    break
                    #GOTO ended inner 1

                #loop block end
                index_0=index_0+1
            #loop ended

            #GOTO end
            if end_goto:
                break
            #GOTO ended

            result_position=info_line[1]

            #GOTO block ended
            break
        #GOTO ended
            
        ordered.insert(result_position,ordered[original_position])
        higher_flag=(result_position<original_position)
        if higher_flag:
            original_position=original_position+1
        else:
            result_position=result_position-1
        del ordered[original_position]
        
        if channel.type==4:
            channels_to_move=[]

            #loop prepare
            index_0=original_position
            limit_0=len(ordered)
            #loop start
            while True:
                if index_0==limit_0:
                    break
                info_line=ordered[index_0]
                #loop block start

                if info_line[3].type==4:
                    break
                channels_to_move.append(info_line)
                
                #loop block end
                index_0=index_0+1
            #loop ended

            insert_to=result_position+1
            
            #loop prepare
            index_0=len(channels_to_move)
            limit_0=0
            #loop start
            while True:
                index_0=index_0-1
                info_line=channels_to_move[index_0]
                #loop block start
                
                ordered.insert(insert_to,info_line)
                
                #loop block end
                if index_0==limit_0:
                    break
            #loop ended

            delete_from=original_position
            if higher_flag:
                delete_from=delete_from+len(channels_to_move) #len(channels_to_move)

            #loop prepare
            index_0=0
            limit_0=len(channels_to_move)
            #loop start
            while True:
                if index_0==limit_0:
                    break
                info_line=ordered[index_0]
                #loop block start

                del ordered[delete_from]
                
                #loop block end
                index_0=index_0+1
            #loop ended
                
        indexes[0]=indexes[2]=indexes[4]=indexes[5]=indexes[6]=0 #reset

        #loop preparations
        index_0=0
        limit_0=len(ordered)
        #loop start
        while True:
            if index_0==limit_0:
                break
            channel_=ordered[index_0][3]
            #loop block start
            
            type_=channel_.type
            type_index=indexes[type_]
            indexes[type_]=type_index+1
            
            ordered[index_0]=(type_index,channel_)

            #loop block step
            index_0=index_0+1
            #loop block continue
            
            if type_==4:
                #reset type_indexes
                indexes[0]=indexes[2]=indexes[5]=indexes[6]=0
                #loop preparations
                #loop start
                while True:
                    if index_0==limit_0:
                        break
                    channel_=ordered[index_0][3]
                    #loop block start
                    
                    type_=channel_.type
                    if type_==4:
                        break
                    type_index=indexes[type_]
                    indexes[type_]=type_index+1

                    ordered[index_0]=(type_index,channel_)
                    
                    #loop block end
                    index_0=index_0+1
                
            #loop block end
        #loop ended

        bonus_data={'lock_permissions':lock_permissions}
        if category is guild:
            bonus_data['parent_id']=None
        else:
            bonus_data['parent_id']=category.id
        
        data=[]
        for position,channel_ in ordered:
            if channel is channel_:
                data.append({'id':channel_.id,'position':position,**bonus_data})
                continue
            if channel_.position!=position:
                data.append({'id':channel_.id,'position':position})

        await self.http.channel_move(guild.id,data,reason)

    async def channel_edit(self, channel, name=None, topic=None, nsfw=None, slowmode=None, user_limit=None,
            bitrate=None, type_=128, reason=None):
        """
        Edits the given guild channel. Different channel types accept different parameters and they ignore the rest.
        Only the passed parameters will be edited of the channel.
        
        Parameters
        ----------
        channel : ``ChannelGuildBase`` instance
            The channel to edit.
        name : `str`, Optional
            The `channel`'s new name.
        topic : `str`, Optional
            The new topic of the `channel`.
        nsfw : `bool`, Optional
            Whether the `channel` will be nsfw or not.
        slowmode : `int`, Optional
            The new slowmode value of the `channel`.
        user_limit : `int`, Optional
            The new user limit of the `channel`.
        bitrate : `int`, Optional
            The new bitrate of the `channel`.
        type_ : `int`, Optional
            The `channel`'s new type value.
        reason : `str`, Optional
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        TypeError
            - If the given `channel` is not ``ChannelGuildBase`` instance.
            - If the given `channel`'s type cannot be changed, but the parameter is passed.
        ValueError
            - If `name`'s length is under `2` or over `100`.
            - If `topic`'s length is over `1024`.
            - If channel type is changed, but not to an expected one.
            - If `slowmode` is not between `0` and `21600`.
            - If `bitrate` is not `8000`-`96000`. `128000` max for vip, or `128000`, `256000`, `384000` max depending
                on the premium tier of the respective guild.
            - If `user_limit` is negative or over `99`.
        ConnectionError
            No internet connection.
        DiscordException
        """
        if not isinstance(channel,ChannelGuildBase):
            raise TypeError(f'Only Guild channels can be edited with this method, got {channel.__class__.__name__}.')
        
        data={}
        value=channel.type
        if (name is not None):
            name_ln=len(name)
            if name_ln<2 or name_ln>100:
                raise ValueError(f'Invalid `name` length, can be between 2-100, got {name_ln}')
            data['name']=name
        
        if value in (0,5):
            if (topic is not None):
                topic_ln=len(topic)
                if topic_ln>1024:
                    raise ValueError(f'Invalid topic length can be between 0-1024, go {topic_ln}')
                data['topic']=topic
        
        if type_<128:
            INTERCHANGE=channel.INTERCHANGE
            if len(INTERCHANGE)==1:
                raise TypeError(f'You can not switch channel type of this channel type')
            if type_ not in INTERCHANGE:
                raise ValueError(f'You can switch chanel type from {value} to {type_}')
            if type_!=value:
                data['type']=type_
        
        if value in (0,5,6):
            if (nsfw is not None):
                data['nsfw']=nsfw
        
        if value==0:
            if (slowmode is not None):
                if slowmode<0 or slowmode>21600:
                    raise ValueError(f'`slowmode` should be between 0 and 21600, got: {slowmode}.')
                data['rate_limit_per_user']=slowmode
        
        elif value==2:
            if bitrate<8000 or bitrate>channel.guild.bitrate_limit:
                raise ValueError('`bitrate` should be 8000-96000. 128000 max for vip, or 128000, 256000, 384000 '
                    f'max depending on premium tier, got {bitrate!r}.')
            data['bitrate']=bitrate
            
            if (user_limit is not None):
                if user_limit<0 or user_limit>99:
                    raise ValueError(f'`user_limit` should be betwwen 0 and 99, got {user_limit!r}.')
                data['user_limit']=user_limit
        
        await self.http.channel_edit(channel.id,data,reason)
    
    async def channel_create(self, guild, category=None, *args, reason=None, **kwargs):
        """
        Creates a new channel at the given `given`. If the channel is successfully created returns it. The unused
        parameters of the created channel's type are ignored.
        
        Parameters
        ----------
        guild : ``Guild``
        category : ``ChannelCategory`` or ``Guild`` or `None`, Optional
            The category of the created channel. If passed as `None`, so by default, the created channel's catetory
            will be it's guild.
        *args : Arguments
            Additional arguments to describe the created channel.
        reason : `str`, Optional
            Shows up at the `guild`'s audit logs.
        **kwargs : Keyword arguments
            Additional keyword arguments to describe the created channel.
        
        Other Parameters
        ----------------
        name : `str`
            The new channel's name.
        type _ : `int` or ``ChannelGuildBase`` subclass
            The new channel's type.
        overwrites : `list` of ``cr_p_overwrite_object`` returns, Optional
            A list of permission overwrites of the new channel. The list should contain json serializable permission
            overwrites made by the ``cr_p_overwrite_object`` function.
        topic : `str`, Optional
            The created channel's topic.
        nsfw : `bool`, Optional.
            Whether the new channel should be masrked as nsfw.
        slowmode : `int`, Optional
            The new channel's slowmode value.
        bitrate : `int`, Optional
            The new channel's bitrate.
        user_limit : `int`, Optional
            The new channel's user limit.
        
        Returns
        -------
        channel : ``ChannelGuildBase`` instance
            The created channel.
        
        Raises
        ------
        TypeError
            - If `category` was not passed as `None`, or ``Guild`` neither as ``ChannelCategory`` instance.
            - If `type_` was not passed as `int` or as ``ChannelGuildBase`` instance.
        ValueError
            - If `type_` was passed as `int`, but as negative or if there is no channel type for the given value.
            - If `name`'s length is under `2` or over `100`.
            - If `topic`'s length is over `1024`.
            - If channel type is changed, but not to an expected one.
            - If `slowmode` is not between `0` and `21600`.
            - If `bitrate` is not `8000`-`96000`. `128000` max for vip, or `128000`, `256000`, `384000` max depending
                on the premium tier of the guild.
            - If `user_limit` is negative or over `99`.
        ConnectionError
            No internet connection.
        DiscordException
        """
        if category is None:
            category_id = None
        elif type(category) is ChannelCategory:
            category_id = category.id
        elif type(category) is Guild:
            category_id = None
        else:
            raise TypeError(f'For `category` type {category.__class__.__name__} is not acceptable.')
        
        data=cr_pg_channel_object(*args, **kwargs, bitrate_limit=guild.bitrate_limit, category_id=category_id)
        data = await self.http.channel_create(guild.id,data,reason)
        return CHANNEL_TYPES[data['type']](data,self,guild)
    
    async def channel_delete(self, channel, reason=None):
        """
        Deletes the specified guild channel.
        
        Parameters
        ----------
        channel : ``ChannelGuildBase`` instance
            The channel to delete.
        reason : `str`, Optional
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        
        Notes
        -----
        If a category channel is deleted, it's subchannels will not be removed, instead they will move under the guild.
        """
        await self.http.channel_delete(channel.id,reason)

    async def channel_follow(self, source_channel, target_channel):
        """
        Follows the `source_channel` with the `target_channel`. Returns the webhook, what will crosspost the published
        messages.
        
        Parameters
        ----------
        source_channel : ``ChannelText`` instance
            The channel what will be followed. Must be an announcements (type 5) channel.
        target_channel : ``ChannelText`` instance
            The target channel where the webhook messages will be sent. Can be any guild text channel type.
        
        Returns
        -------
        webhook : ``Webhook``
            The webhook what will crosspost the published messages. This webhook has no `.token` set.
        
        Raises
        ------
        TypeError
            - If the `source_channel` is not an announcements channel.
            - If the `target_channel` is not a guild text channel.
        ConnectionError
            No internet connection.
        DiscordException
        """
        if source_channel.type!=5:
            raise TypeError(f'`source_channel` must be type 5 (announcements) channel, got `{source_channel}`.')
        if target_channel.type not in ChannelText.INTERCHANGE:
            raise TypeError(f'`target_channel` must be type 0 or 5 (any guild text channel), got  `{target_channel}`.')
        
        data = {
            'webhook_channel_id': target_channel.id,
                }
        
        data = await self.http.channel_follow(source_channel.id,data)
        webhook = await Webhook._from_follow_data(data, source_channel, target_channel, self)
        return webhook
    
    #messages
    
    async def message_logs(self, channel, limit=100, after=None, around=None, before=None):
        """
        Requests messages from the given text channel. The `after`, `around` and the `before` arguments are mutually
        exclusive and they can be passed as `int`, or as a ``DiscordEntitiy`` instance or as a `datetime` object.
        If there is at least 1 message overlap between the received and the loaded messages, the wrapper will chain
        the channel's message history up. If this happens the channel will get on a queue to have it's messages again
        limited to the default one, but requesting old messages more times, will cause it to extend.
        
        Parameters
        ----------
        channel : ``ChannelTextBase`` instance
            The channel from where we want to request the messages.
        limit : `int`, Optiomal
            The amount of messages to request. Can be between 1 and 100.
        after : `int`, ``DiscordEntity`` or `datetime`, Optional
            The timestamp after the requested messages were created.
        around : `int`, ``DiscordEntity`` or `datetime`, Optional
            The timestamp around the requested messages were created.
        before : `int`, ``DiscordEntity`` or `datetime`, Optional
            The timestamp before the requested messages were created.
        
        Returns
        -------
        messages : `list` of ``Message`` objects
        
        Raises
        ------
        TypeError
            If `after`, `around` or `before` was passed with an unexpected type.
        ValueError
            If `limit` is under `1` or over `100`.
        ConnectionError
            No internet connection.
        DiscordException
        
        See Also
        --------
        .message_logs_fromzero : Familiar to this method, but it requests only the newest messages of the channel and
            makes sure they are chained up with the channel's message history.
        .message_at_index : A toplevel method to get a message at the specified index at the given channel.
            Usually used to load the channel's message history to that point.
        .messages_in_range : A toplevel method to get all the messages till the specified index at the given channel.
        .message_iterator : An iterator over a channel's message history.
        """
        if limit<1 or limit>100:
            raise ValueError(f'limit must be in between 1 and 100, got {limit!r}.')
        
        data={'limit':limit}
        
        if (after is not None):
            data['after']=log_time_converter(after)
        
        if (around is not None):
            data['around']=log_time_converter(around)
        
        if (before is not None):
            data['before']=log_time_converter(before)
        
        data = await self.http.message_logs(channel.id,data)
        return channel._process_message_chunk(data)
    
    #if u have 0-1-2 messages at a channel, and you wanna store the messages.
    #the other wont store it, because it wont see anything what allows channeling
    async def message_logs_fromzero(self, channel, limit=100):
        """
        If the `channel` has `1` or less messages loaded use this method instead of ``.message_logs`` to request the
        newest messages there, because this method makes sure, the returned messages will be chained at the
        channel's message history.
        
        Parameters
        ----------
        channel : ``ChannelTextBase`` instance
            The channel from where we want to request the messages.
        limit : `int`, Optiomal
            The amount of messages to request. Can be between 1 and 100.
        
        Returns
        -------
        messages : `list` of ``Message`` objects
        
        Raises
        ------
        ValueError
            If `limit` is under `1` or over `100`.
        ConnectionError
            No internet connection.
        DiscordException
        """
        if limit<1 or limit>100:
            raise ValueError(f'limit must be in <1,100>, got {limit}')
        
        data = {'limit':limit,'before':9223372036854775807}
        data = await self.http.message_logs(channel.id,data)
        if data:
            channel._create_new_message(data[0])
            messages = channel._process_message_chunk(data)
        else:
            messages = []
        
        return messages

    async def message_get(self, channel, message_id):
        """
        Requests a specific message by it's id at the given `channel`.
        
        Parameters
        ----------
        channel : ``ChannelTextBase`` instance
            The channel from where we want to request the message.
        message_id : `int`
            The message's id.
        
        Returns
        -------
        message : ``Message``
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        data = await self.http.message_get(channel.id,message_id)
        return channel._create_unknown_message(data)
    
    async def message_create(self, channel, content=None, embed=None, file=None, allowed_mentions=_spaceholder,
            tts=False, nonce=None):
        """
        Creates and returns a message at the given `channel`. If there is nothing to send, then returns `None`.
        
        Parameters
        ----------
        channel : ``ChannelTextBase`` instance
            The text channel where the message will be sent.
        content : `str`, Optional
            The content of the message.
        embed : ``Embed`` or ``EmbedCore`` instance or any compatible object
            The embedded content of the message.
        file : `Any`, Optional
            A file to send. Check ``._create_file_form`` for details.
        allowed_mentions : `None` or `list` of `Any`, Optional
            Which user or role can the message ping (or everyone). Check ``._parse_allowed_mentions`` for details.
        tts : `bool`, Optional
            Whether the message is text-to-speech.
        nonce : `str`, Optional
            Used for optimisting message sending. Will shop up at the message's data.
        
        Returns
        -------
        message : ``Message`` or `None`
            Returns `None` if there is nothing to send.
        
        Raises
        ------
        TypeError
            - If `allowed_mentions` when correct type, but an invalid value would been sent.
            - If ivalid file type would be sent.
        ValueError
            - If more than `10` files would be sent.
            - If `allowed_mentions` contains an element of invalid type.
        ConnectionError
            No internet connection.
        DiscordException
        
        See Also
        --------
        .webhook_send : Sending a message with a ``Webbhook``.
        """
        data={}
        contains_content=False
        
        if (content is not None) and content:
            data['content']=content
            contains_content=True
        
        if (embed is not None):
            data['embed']=embed.to_data()
            contains_content=True
        
        if tts:
            data['tts']=True
        
        if (nonce is not None):
            data['nonce']=nonce
        
        if (allowed_mentions is not _spaceholder):
            data['allowed_mentions']=self._parse_allowed_mentions(allowed_mentions)
        
        if file is None:
            to_send=data
        else:
            to_send=self._create_file_form(data,file)
            if to_send is None:
                to_send=data
            else:
                contains_content=True
        
        if not contains_content:
            return None
        
        data = await self.http.message_create(channel.id, to_send)
        return channel._create_new_message(data)
    
    @staticmethod
    def _create_file_form(data, file):
        """
        Creates a `multipart/form-data` form from the message's data and from the file data. If there is no files to
        send, will return `None` to tell the caller, that nothing is added to the overall data.
        
        Parameters
        ----------
        data : `dict` of `Any`
            The data created by the ``.message_create`` method.
        file : `dict` of (`file-name`, `io`) items, `list` of (`file-name`, `io`) elements, tuple (`file-name`, `io`), `io`
            The files to send.
        
        Returns
        -------
        form : `None` or `Formdata`
            Returns a `Formdata` of the files and from the message's data. If there are no files to send, returns `None`
            instead.
        
        Raises
        ------
        ValueError
            When more than `10` file is registered to send.
        
        Notes
        -----
        Accepted `io` types with check order are:
        - `BodyPartReader` instance
        - `bytes`, `bytearray`, `memoryview` instance
        - `str` instance
        - `BytesIO` instance
        - `StringIO` instance
        - `TextIOBase` instance
        - `BufferedReader`, `BufferedRandom` instance
        - `IOBase` instance
        - ``AsyncIO`` instance
        - `async-iterable`
        
        Raises `TypeError` at the case of invalid `io` type .
        
        There are two predefined datatypes specialized to send files:
        - ``ReuBytesIO``
        - ``ReuAsyncIO``
        
        If a buffer is sent, then when the request is done, it is closed. So if the request fails, we would not be
        able to resend the file, except if we have a datatype, what instead of closing on `.close()` just seeks to
        `0` (or later if needed) on close, instead of really closing instantly. These datatypes implement a
        `.real_close()` method, but they do `real_close` on `__exit__` as well.
        """
        form=Formdata()
        form.add_field('payload_json',to_json(data))
        files=[]
        
        #checking structure
        
        #case 1 dict like
        if hasattr(file,'items'):
            files.extend(file.items())
        
        #case 2 tuple => file, filename pair
        elif isinstance(file,tuple):
            files.append(file)
        
        #case 3 list like
        elif isinstance(file,(list,deque)):
            for element in file:
                if type(element) is tuple:
                    name,io=element
                else:
                    io=element
                    name=''
                
                if not name:
                    #guessing name
                    name=getattr(io,'name','')
                    if name:
                        _,name=splitpath(name)
                    else:
                        name=str(random_id())
                        
                files.append((name,io),)
        
        #case 4 file itself
        else:
            name=getattr(file,'name','')
            #guessing name
            if name:
                _,name=splitpath(name)
            else:
                name=str(random_id())
            
            files.append((name,file),)
        
        #checking the amount of files
        #case 1 one file
        if len(files)==1:
            name,io=files[0]
            form.add_field('file',io,filename=name,content_type='application/octet-stream')
        #case 2, no files -> return None, we should use the already existing data
        elif len(files)==0:
            return None
        #case 3 maximum 10 files
        elif len(files)<11:
            for index,(name,io) in enumerate(files):
                form.add_field(f'file{index}s',io,filename=name,content_type='application/octet-stream')
        
        #case 4 more than 10 files
        else:
            raise ValueError('You can send maximum 10 files at once.')
        
        return form
    
    @staticmethod
    def _parse_allowed_mentions(allowed_mentions):
        """
        If `allowed_mentions` is passed as `None`, then returns a `dict`, what will cause all mentions to be disabled.
        
        If passed as an `iterable`, then it's elements will be checked. They can be either type `str`
        (any value from `('everyone', 'users', 'roles')`), ``UserBase`` or ``Role`` instances.
        
        Passing `everyone` will allow the message to mention `@everyone` (permissions can overwrite this behaviour).
        
        Passing `'users'` will allow the message to mention all the users, meanwhile passing ``UserBase`` instances
        allow to mentioned the respective users. Using `users` and ``UserBase`` instances is mutually exclusive,
        and the wrapper will register only `users` to avoid getting ``DiscordException``.
        
        `'roles'` and ``Role`` instances follow the same rules as `'users'` and the ``UserBase`` instances.
        
        Parameters
        ----------
        allowed_mentions : `None` or `list` of (`str` , `UserBase` instances, `Role` objects)
            Which user or role can the message ping (or everyone).
        
        Returns
        -------
        allowed_mentions : `dict` of (`str`, `Any`) items
        
        Raises
        ------
        TypeError
            If `allowed_mentions` contains an element of invalid type.
        ValueError
            If `allowed_mentions` contains en element of correct type, but an invalid value.
        """
        
        if (allowed_mentions is None) or (not allowed_mentions):
            return {'parse':[]}
        
        allow_everyone = False
        allow_users = False
        allow_roles = False
        
        allowed_users = None
        allowed_roles = None
        
        for element in allowed_mentions:
            if type(element) is str:
                if element=='everyone':
                    allow_everyone=True
                    continue
                
                if element=='users':
                    allow_users=True
                    continue
                
                if element=='roles':
                    allow_roles=True
                    continue
                
                raise ValueError(f'`allowed_mentions` contains a not valid `str` element: `{element!r}`. Type`str` elements can be one of: (\'everyone\', \'users\', \'roles\').')
            
            if isinstance(element,UserBase):
                if allowed_users is None:
                    allowed_users = []
                
                allowed_users.append(element.id)
                continue
            
            if type(element) is Role:
                if allowed_roles is None:
                    allowed_roles = []
                
                allowed_roles.append(element.id)
                continue
            
            raise TypeError(f'`allowed_mentions` contains an element of an invalid type: `{element!r}`. The allowed types are: `str`, `Role` and any`UserBase` instance.')
        
        
        result = {}
        parse_all_of=None
        
        if allow_everyone:
            if parse_all_of is None:
                parse_all_of = []
                result['parse'] = parse_all_of
            
            parse_all_of.append('everyone')
        
        if allow_users:
            if parse_all_of is None:
                parse_all_of = []
                result['parse'] = parse_all_of
            
            parse_all_of.append('users')
        else:
            if (allowed_users is not None):
                result['users']=allowed_users
        
        if allow_roles:
            if parse_all_of is None:
                parse_all_of = []
                result['parse'] = parse_all_of
            
            parse_all_of.append('roles')
        else:
            if (allowed_roles is not None):
                result['roles']=allowed_roles
        
        return result
    
    async def message_delete(self, message, reason=None):
        """
        Deletes the given message.
        
        Parameters
        ----------
        message : ``Message``
            The message to delete.
        reason : `str`, Optional
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        
        Notes
        -----
        The ratelimit group is different for own or for messages newer than 2 weeks than for message's of others,
        which are older than 2 weeks.
        """
        if (message.author == self) or (message.id > int((time_now()-1209590.)*1000.-DISCORD_EPOCH)<<22):
            # own or new
            await self.http.message_delete(message.channel.id,message.id,reason)
        else:
            await self.http.message_delete_b2wo(message.channel.id,message.id,reason)
    
    
    async def message_delete_multiple(self, messages, reason=None):
        """
        Deletes the given messages. The messages needs to be from the same channel.
        
        Parameters
        ----------
        messages : `list` of ``Message`` objects
            The messages to delete.
        reason : `str`, Optional
            Shows up at the respective guild's audit logs.

        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        
        Notes
        -----
        This method uses up 3 different ratelimit groups parallelly to maximalize the deletion speed.
        """
        if not messages:
            return
        
        channel=messages[0].channel
        channel_id=channel.id

        if not isinstance(channel,ChannelGuildBase):
            # Bulk delete is available only at guilds. At private or group
            # channel you can delete only yours tho.
            for message in messages:
                await self.http.message_delete(channel_id,message.id,reason)
                
            return
        
        message_group_new       = deque()
        message_group_old       = deque()
        message_group_old_own   = deque()
        
        bulk_delete_limit = int((time_now()-1209600.)*1000.-DISCORD_EPOCH)<<22 # 2 weeks
        
        for message in messages:
            message_id=message.id
            own=(message.author==self)
            
            if message_id>bulk_delete_limit:
                message_group_new.append((own,message_id),)
                continue
            
            if own:
                group = message_group_old_own
            else:
                group = message_group_old
            
            group.append(message_id)
            continue
        
        tasks = []
        
        delete_mass_task= None
        delete_new_task = None
        delete_old_task = None
        
        while True:
            if delete_mass_task is None:
                message_limit=len(message_group_new)
                
                # 0 is all good, but if it is more, lets check them
                if message_limit:
                    message_ids=[]
                    message_count=0
                    limit = int((time_now()-1209590.)*1000.-DISCORD_EPOCH)<<22 # 2 weeks -10s
                    
                    while message_group_new:
                        own,message_id=message_group_new.popleft()
                        if message_id>limit:
                            message_ids.append(message_id)
                            message_count=message_count+1
                            if message_count==100:
                                break
                            continue
                        
                        if (message_id+20971520000) < limit:
                            continue
                        
                        # If the message is really older than the limit,
                        # with ingoring the 10 second, then we move it.
                        if own:
                            group = message_group_old_own
                        else:
                            group = message_group_old
                        
                        group.appendleft(message_id)
                        continue
                    
                    if message_count:
                        if message_count==1:
                            if (delete_new_task is None):
                                message_id=message_ids[0]
                                delete_new_task = Task(self.http.message_delete(channel_id,message_id,None), KOKORO)
                                tasks.append(delete_new_task)
                        else:
                            delete_mass_task = Task(self.http.message_delete_multiple(channel_id,{'messages':message_ids},None), KOKORO)
                            tasks.append(delete_mass_task)
                
            if delete_old_task is None:
                if message_group_old:
                    message_id=message_group_old.popleft()
                    delete_old_task = Task(self.http.message_delete_b2wo(channel_id,message_id,reason), KOKORO)
                    tasks.append(delete_old_task)
            
            if delete_new_task is None:
                if message_group_new:
                    group = message_group_new
                elif message_group_old_own:
                    group = message_group_old_own
                else:
                    group = None
                
                if (group is not None):
                    message_id=message_group_old_own.popleft()
                    delete_new_task = Task(self.http.message_delete(channel_id,message_id,reason), KOKORO)
                    tasks.append(delete_new_task)
            
            if not tasks:
                # It can happen, that there are no more tasks left,  at that case
                # we check if there is more message left. Only at
                # `message_group_new` can be anymore message, because there is a
                # time intervallum of 10 seconds, what we do not move between
                # categories.
                if not message_group_new:
                    break
                
                # We really have at least 1 message at that interval.
                own,message_id = message_group_new.popleft()
                # We will delete that message with old endpoint if not own, to make
                # Sure it will not block the other endpoint for 2 minutes with any chance.
                if own:
                    delete_new_task = Task(self.http.message_delete(channel_id,message_id,None), KOKORO)
                else:
                    delete_old_task = Task(self.http.message_delete_b2wo(channel_id,message_id,None), KOKORO)
                
                tasks.append(delete_old_task)
                
            done, pending = await WaitTillFirst(tasks, KOKORO)
    
            for task in done:
                tasks.remove(task)
                try:
                    result = task.result()
                except (DiscordException,ConnectionError):
                    for task in tasks:
                        task.cancel()
                    raise
                
                if task is delete_mass_task:
                    delete_mass_task=None
                    continue
                
                if task is delete_new_task:
                    delete_new_task=None
                    continue
                
                if task is delete_old_task:
                    delete_old_task=None
                    continue
                 
                # Should not happen
                continue

    #deletes from more channels
    async def message_delete_multiple2(self, messages, reason=None):
        """
        Similar to ``.message_delete_multiple`, but it accepts messages from different channels. Groups them up by
        channel and creates ``.message_delete_multiple`` tasks for them. Returns when all the task are finished.
        If any exception was rasised meanwhile, then returns each of them in a list.
        
        Parameters
        ----------
        messages : `list` of ``Message`` objects
            The messages to delete.
        reason : `str`, Optional
            Shows up at the respective guild's audit logs.

        Returns
        -------
        exceptions : `None`, `list` of (`ConnectionError` or ``DiscordException``) instances
        """
        delete_system={}
        for message in messages:
            channel_id=message.channel.id
            try:
                delete_system[channel_id].append(message)
            except KeyError:
                delete_system[channel_id]=[message]
        
        tasks = []
        for messages in delete_system.values():
            task=Task(self.message_delete_multiple(messages,reason), KOKORO)
            tasks.append(task)
        
        await WaitTillAll(tasks, KOKORO)
        
        exceptions = []
        for task in tasks:
            exception=task.exception()
            if exception is None:
                continue
            
            exceptions.append(exceptions)
            if  __debug__:
                task.__silence__()
        
        if exceptions:
            return exceptions
        
    async def message_delete_sequence(self, channel, after=None, before=None, limit=None, filter=None, reason=None):
        """
        Deletes messages between an intervallum determined by `before` and `after`. They can be passed as `int`, or as
        a ``DiscordEntitiy`` instance or as a `datetime` object.
        
        Parameters
        ----------
        channel : ``ChannelTextBase`` instance
            The channel, where the deletion should take place.
        after : `int`, ``DiscordEntity`` or `datetime`, Optional
            The timestamp after the messages were created, which will be deleted.
        before : `int`, ``DiscordEntity`` or `datetime`, Optional
            The timestamp before the messages were created, which will be deleted.
        limit : `int`, Optional
            The maximal amount of messages to delete.
        filter : `callable`, Optional
            A callable filter, what should accept a message object as argument and return either `True` or `False`.
        reason : `str`, Optional
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        TypeError
            If `after` or `before` was passed with an unexpected type.
        ConnectionError
            No internet connection.
        DiscordException
        
        Notes
        -----
        This method uses up 4 different ratelimit groups parallelly to maximalize the request and the deletion speed.
        """
        # Check permissions
        permissions=channel.cached_permissions_for(self)
        if not permissions.can_manage_messages:
            return
        
        before  = 9223372036854775807 if before is None else log_time_converter(before)
        after   = 0 if after is None else log_time_converter(after)
        limit   = 9223372036854775807 if limit is None else limit
        
        # Check for reversed intervals
        if before<after:
            return
        
        # Check if we are done already
        if limit<=0:
            return
        
        message_group_new       = deque()
        message_group_old       = deque()
        message_group_old_own   = deque()
        
        # Check if we can request more messages
        if channel.message_history_reached_end or (not permissions.can_read_message_history):
            should_request=False
        else:
            should_request=True
        
        last_message_id = before
        
        messages_=channel.messages
        if messages_:
            before_index=message_relativeindex(messages_,before)
            after_index=message_relativeindex(messages_,after)
            if before_index!=after_index:
                time_limit = int((time_now()-1209600.)*1000.-DISCORD_EPOCH)<<22
                while True:
                    if before_index==after_index:
                        break
                    
                    message_ = messages_[before_index]
                    before_index=before_index+1
                    
                    if (filter is not None):
                        if not filter(message_):
                            continue
                    
                    last_message_id=message_.id
                    own = (message_.author==self)
                    if last_message_id > time_limit:
                        message_group_new.append((own,last_message_id,),)
                    else:
                        if own:
                            group=message_group_old_own
                        else:
                            group=message_group_old
                        group.append(last_message_id)
                    
                    # Check if we reached the limit
                    limit=limit-1
                    if limit:
                        continue
                    should_request=False
                    break
        
        tasks               = []
        
        get_mass_task       = None
        delete_mass_task    = None
        delete_new_task     = None
        delete_old_task     = None
        
        channel_id=channel.id
        
        while True:
            if should_request and (get_mass_task is None):
                request_data = {
                    'limit' : 100,
                    'before': last_message_id,
                        }
                
                get_mass_task = Task(self.http.message_logs(channel_id,request_data), KOKORO)
                tasks.append(get_mass_task)
            
            if (delete_mass_task is None):
                message_limit=len(message_group_new)
                # If there are more messages, we are waiting for other tasks
                if message_limit:
                    time_limit = int((time_now()-1209590.)*1000.-DISCORD_EPOCH)<<22 # 2 weeks -10s
                    collected = 0
                    
                    while True:
                        if collected==message_limit:
                            break
                        
                        if collected==100:
                            break
                        
                        own,message_id=message_group_new[collected]
                        if message_id<time_limit:
                            break
                        
                        collected=collected+1
                        continue
                    
                    if collected==0:
                        pass
                    elif collected==1:
                        # Delete the message if we dont delete a new message already
                        if (delete_new_task is None):
                            # We collected 1 message -> We cannot use mass delete on this.
                            own,message_id=message_group_new.popleft()
                            delete_new_task = Task(self.http.message_delete(channel_id,message_id,reason=reason), KOKORO)
                            tasks.append(delete_new_task)
                    else:
                        message_ids=[]
                        while collected:
                            collected = collected-1
                            own,message_id=message_group_new.popleft()
                            message_ids.append(message_id)
                        
                        delete_mass_task = Task(self.http.message_delete_multiple(channel_id,{'messages':message_ids},reason=reason), KOKORO)
                        tasks.append(delete_mass_task)
                    
                    # After we checked what is at this group, lets move the others from it's end, if needed ofc
                    message_limit=len(message_group_new)
                    if message_limit:
                        # timelimit -> 2 week
                        time_limit = time_limit-20971520000
                        
                        while True:
                            # Cannot start at index = len(...), so we instantly do -1
                            message_limit = message_limit-1
                            
                            own, message_id = message_group_new[message_limit]
                            # Check if we should not move -> leave
                            if message_id>time_limit:
                                break
                            
                            del message_group_new[message_limit]
                            if own:
                                group = message_group_old_own
                            else:
                                group = message_group_old
                                
                            group.appendleft(message_id)
                            
                            if message_limit:
                                continue
                            
                            break
            
            if (delete_new_task is None):
                # Check old own messages only, mass delete speed is pretty good by itself.
                if message_group_old_own:
                    message_id=message_group_old_own.popleft()
                    delete_new_task = Task(self.http.message_delete(channel_id,message_id,reason=reason), KOKORO)
                    tasks.append(delete_new_task)
            
            if (delete_old_task is None):
                if message_group_old:
                    message_id=message_group_old.popleft()
                    delete_old_task = Task(self.http.message_delete_b2wo(channel_id,message_id,reason=reason), KOKORO)
                    tasks.append(delete_old_task)
            
            if not tasks:
                # It can happen, that there are no more tasks left,  at that case
                # we check if there is more message left. Only at
                # `message_group_new` can be anymore message, because there is a
                # time intervallum of 10 seconds, what we do not move between
                # categories.
                if not message_group_new:
                    break
                
                # We really have at least 1 message at that interval.
                own,message_id = message_group_new.popleft()
                # We will delete that message with old endpoint if not own, to make
                # Sure it will not block the other endpoint for 2 minutes with any chance.
                if own:
                    delete_new_task = Task(self.http.message_delete(channel_id,message_id,reason=reason), KOKORO)
                    task=delete_new_task
                else:
                    delete_old_task = Task(self.http.message_delete_b2wo(channel_id,message_id,reason=reason), KOKORO)
                    task=delete_old_task
                
                tasks.append(task)
            
            done, pending = await WaitTillFirst(tasks, KOKORO)
            
            for task in done:
                tasks.remove(task)
                try:
                    result = task.result()
                except (DiscordException,ConnectionError):
                    for task in tasks:
                        task.cancel()
                    raise
                
                if task is get_mass_task:
                    get_mass_task=None
                    
                    received_count=len(result)
                    if received_count<100:
                        should_request=False
                        
                        # We got 0 messages, move on the next task
                        if received_count==0:
                            continue
                    
                    # We dont really care about the limit, because we check
                    # message id when we delete too.
                    time_limit = int((time_now()-1209600.)*1000.-DISCORD_EPOCH)<<22 # 2 weeks
                    
                    for message_data in result:
                        if (filter is None):
                            last_message_id=int(message_data['id'])
    
                            # Did we reach the after limit?
                            if last_message_id<after:
                                should_request=False
                                break
                            
                            # If filter is `None`, we just have to decide, if we
                            # were the author or nope.
                            
                            # Try to get user id, first start it with trying to get
                            # author data. The default author_id will be 0, because
                            # thats sure not the id of the client.
                            try:
                                author_data=message_data['author']
                            except KeyError:
                                author_id=0
                            else:
                                # If we have author data, lets select the user's data
                                # from it
                                try:
                                    user_data=author_data['user']
                                except KeyError:
                                    user_data=author_data
                                
                                try:
                                    author_id=user_data['id']
                                except KeyError:
                                    author_id=0
                                else:
                                    author_id=int(author_id)
                        else:
                            message_=channel._create_unknown_message(message_data)
                            last_message_id=message_.id
                            
                            # Did we reach the after limit?
                            if last_message_id<after:
                                should_request=False
                                break
                            
                            if not filter(message_):
                                continue
                            
                            author_id=message_.author.id
                        
                        own = (author_id == self.id)
                        
                        if last_message_id>time_limit:
                            message_group_new.append((own,last_message_id,),)
                        else:
                            if own:
                                group = message_group_old_own
                            else:
                                group = message_group_old
                            
                            group.append(last_message_id)
                        
                        # Did we reach the amount limit?
                        limit = limit-1
                        if limit:
                            continue
                        
                        should_request=False
                        break
                
                if task is delete_mass_task:
                    delete_mass_task=None
                    continue
                
                if task is delete_new_task:
                    delete_new_task=None
                    continue
                
                if task is delete_old_task:
                    delete_old_task=None
                    continue
                 
                # Should not happen
                continue
    
    async def message_edit(self, message, content=None, embed=_spaceholder, allowed_mentions=_spaceholder,
            suppress=None):
        """
        Edits the given `message`.
        
        Parameters
        ----------
        message : ``Message``
            The message to edit.
        content : `str`, Optional
            The new content of the message. By passing it as `''`, you can remove the old.
        embed : `None` or ``Embed`` or ``EmbedCore`` instance or any compatible object, Optional
            The new embedded content of the message. By passing it as `None`, you can remove the old.
        allowed_mentions : `None` or `list` of `Any`, Optional
            Which user or role can the message ping (or everyone). Check ``._parse_allowed_mentions``
            for details.
        suppress : `bool`, Optional
            Whether the message's embeds should be suppressed or unsuppressed.
        
        Raises
        ------
        TypeError
            If `allowed_mentions` when correct type, but an invalid value would been sent.
        ValueError
            If `allowed_mentions` cantains an element of invalid type.
        ConnectionError
            No internet connection.
        DiscordException
        
        See Also
        --------
        .message_suppress_embeds : For suppressing only the embeds of the message.
        """
        data={}
        if (content is not None):
            data['content']=content
        
        if (embed is not _spaceholder):
            if embed is None:
                embed_data=None
            else:
                embed_data=embed.to_data()
            
            data['embed']=embed_data
        
        if (allowed_mentions is not _spaceholder):
            data['allowed_mentions']=self._parse_allowed_mentions(allowed_mentions)
        
        if (suppress is not None):
            if suppress:
                flags=message.flags|0b00000100
            else:
                flags=message.flags&0b11111011
            data['flags']=flags
        
        await self.http.message_edit(message.channel.id, message.id, data)

    async def message_suppress_embeds(self, message ,suppress=True):
        """
        Suppresses or unsuppressed the given message's embeds.
        
        Parameters
        ----------
        message : ``Message`` object
            The message, what's embeds will be (un)suppressed.
        suppress : `bool`, Optional
            Whether the message's embeds would be suppressed or unsuppressed.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        await self.http.message_suppress_embeds(message.channel.id,message.id,{'suppress':suppress})
    
    async def message_crosspost(self, message):
        """
        Crossposts the given message. The message's channel must be an announcements (type 5) channel.
        
        Parameters
        ----------
        message : ``Message`` object
            The message to crosspost.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        await self.http.message_crosspost(message.channel.id, message.id)
    
    async def message_pin(self, message):
        """
        Pins the given message.
        
        Parameters
        ----------
        message : ``Message`` object
            The message to pin.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        await self.http.message_pin(message.channel.id,message.id)
    
    async def message_unpin(self, message):
        """
        Unpins the given message.
        
        Parameters
        ----------
        message : ``Message`` object
            The message to unpin.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        await self.http.message_unpin(message.channel.id,message.id)

    async def channel_pins(self, channel):
        """
        Returns the pinned messages at the given channel.
        
        Parameters
        ----------
        channel : ``ChannelTextBase`` instance
            The channel from were the pinned messages will be requested.
        
        Returns
        -------
        messages : `list` of ``Message`` objects
            The pinned messages at the given channel.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        data = await self.http.channel_pins(channel.id)
        return [channel._create_unknown_message(message_data) for message_data in data]


    async def _load_messages_till(self, channel, index):
        """
        An internal function to load the messages at the given channel till the given index. Should not be called if
        the channel reached it's message history's end.
        
        Parameters
        ----------
        channel : ``ChannelTextBase`` instance
            The channel from where the messages will be requested.
        index : `int`
            Till which index the messages should be requested at the given channel.
        
        Raises
        ------
        IndexError
            If `index` could not be reached, because there is no more message at the given channel.
        ConnectionError
            No internet connection.
        DiscordException
        """
        while True:
            ln = len(channel.messages)
            loadto = index-ln
            
            # we want to load it till the exact index, so if `loadto` is `0`, thats not enough!
            if loadto < 0:
                break
            
            if loadto < 98:
                planned = loadto+2
            else:
                planned = 100
            
            if ln:
                result = await self.message_logs(channel, planned, before=channel.messages[ln-2].id)
            else:
                result = await self.message_logs_fromzero(channel,planned)
            
            if len(result)<planned:
                channel.message_history_reached_end=True
                raise IndexError(index)
        
        channel._turn_message_keep_limit_on_at += index
    
    async def message_at_index(self, channel, index):
        """
        Returns the message at the given channel at the specific index. Can be used to load `index` amount of messages
        at the channel.
        
        Parameters
        ----------
        channel : ``ChannelTextBase``
            The channel from were the messages will be requested.
        index : `int`
            The index of the target message.
        
        Returns
        -------
        message : ``Message`` object
        
        Raises
        ------
        IndexError
            If `index` could not be reached, because there is no more message at the given channel.
        PermissionError
            If the client cannot read the channel's message history.
        ConnectionError
            No internet connection.
        DiscordException
        """
        messages = channel.messages
        if index<len(messages):
            return messages[index]
        
        if channel.message_history_reached_end:
            raise IndexError(index)
        
        if not channel.cached_permissions_for(self).can_read_message_history:
            raise PermissionError('Client can\'t read message history')
        
        await self._load_messages_till(channel,index)
        # access it again, because it might be modified
        return channel.messages[index]
    
    async def messages_in_range(self, channel, start=0, end=100):
        """
        Returns a list of the message between the `start` - `end` area. If the client has no permission to request
        messages, or there are no messages at the given area returns an empty list.
        
        Parameters
        ----------
        channel : ``ChannelTextBase`` instance
            The channel from were the messages will be requested.
        start : `int`, Optional
            The first message's index at the channel to be requested. Defaults to `0`.
        end : `int`
            The last message's index at the channel to be requested. Deffaults to `100`.
        
        Returns
        -------
        messages : `list` of ``Message`` objects
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        if end>=len(channel.messages) and (not channel.message_history_reached_end) and \
               channel.cached_permissions_for(self).can_read_message_history:
            try:
                await self._load_messages_till(channel,end)
            except IndexError:
                pass
        
        result = []
        messages = channel.messages
        for index in range(start,min(end,len(messages))):
            result.append(messages[index])
        
        return result
    
    def message_iterator(self, channel, chunksize=99):
        """
        Returns an asynchronous message iterator over the given text channel.
        
        Parameters
        ----------
        channel : ``ChannelTextBase`` instance
            The channel from were the messages will be requested.
        chunksize : `int`, Optional
            The amount of messages to request when the currently loaded history is exhausted. For message chaining
            it is preferably `99`.
        
        Returns
        -------
        message_iterator : ``MessageIterator``
        """
        return MessageIterator(self, channel, chunksize)

    async def typing(self, channel):
        """
        Sends a typing event to the given channel.
        
        Parameters
        ----------
        channel : ``ChannelTextBase`` instance
            The channel where the typing event will be sent.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        
        Notes
        -----
        The client will be shown up as typing for 8 seconds, or till it sends a message at the respective channel.
        """
        await self.http.typing(channel.id)

    #with context
    def keep_typing(self, channel, timeout=300.):
        """
        Returns a ``Typer`` object, what will keep sending typing events at the given channel. It can be used as a
        context manager.
        
        Parameters
        ----------
        channel ``ChannelTextBase`` instance
            The channel where the typing events will be sent.
        timeout : `float`, Optional
            The maximal duration for the ``Typer`` to keep typing.
        
        Returns
        -------
        typer : ``Typer``
        """
        return Typer(self, channel, timeout)

    #reactions:

    async def reaction_add(self, message, emoji):
        """
        Adds a reaction on the given message.
        
        Parameters
        ----------
        message : ``Message`` object
            The message on which the reaction will be put on.
        emoji : ``Emoji`` object
            The emoji to react with
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        await self.http.reaction_add(message.channel.id,message.id,emoji.as_reaction)

    async def reaction_delete(self, message, emoji, user):
        """
        Removes the specified reaction of the user from the given message.
        
        Parameters
        ----------
        message : ``Message`` object
            The message from which the reaction will be removed.
        emoji : ``Emoji`` object
            The emoji to remove.
        user : ``UserBase`` instance
            The user, who's reaction will be removed.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        await self.http.reaction_add(message.channel.id,message.id,emoji.as_reaction)
        if self==user:
            await self.http.reaction_delete_own(message.channel.id,message.id,emoji.as_reaction)
        else:
            await self.http.reaction_delete(message.channel.id,message.id,emoji.as_reaction,user.id)

    async def reaction_delete_emoji(self, message, emoji):
        """
        Removes all the reaction of the specified emoji from the given message.
        
        Parameters
        ----------
        message : ``Message`` object
            The message from which the reactions will be removed.
        emoji : ``Emoji`` object
            The reaction to remove.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        await self.http.reaction_delete_emoji(message.channel.id,message.id,emoji.as_reaction)

    async def reaction_delete_own(self, message, emoji):
        """
        Removes the specified reaction of the client from the given message.
        
        Parameters
        ----------
        message : ``Message`` object
            The message from which the reaction will be removed.
        emoji : ``Emoji`` object
            The emoji to remove.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        await self.http.reaction_delete_own(message.channel.id,message.id,emoji.as_reaction)

    async def reaction_clear(self, message):
        """
        Removes all the reactions from the given message.
        
        Parameters
        ----------
        message : ``Message`` object
            The message from which the reactions will be cleared.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        await self.http.reaction_clear(message.channel.id,message.id)
    
    # before is not supported
    
    async def reaction_users(self, message, emoji, limit=None, after=None):
        """
        Requests the users, who reacted on the given message with the given emoji.
    
        If the message has no reacters at all or no reacters with that emoji, returns an empty list. If we know the
        emoji's every reacters we query the parameters from that.
        
        Parameters
        ----------
        message : ``Message`` object
            The message, what's reactions will be requested.
        emoji : ``Emoji`` object
            The emoji, what's reacters will be requested.
        limit : `int`
            The amount of users to request. Can be between `1` and `100`. Defaults to 25 by Discord.
        after : `int`, ``DiscordEntity`` or `datetime`, Optional
            The timestamp after the message's reacters were created.
        
        Returns
        -------
        users : `list` of (``Client`` or ``User``) objects
        
        Raises
        ------
        TypeError
            - If `after` was passed with an unexpected type.
            - If `limit` was not passed as `int`.
        ValueError
            If `limit` was passed as `int`, but is under `1` or over `100`.
        ConnectionError
            No internet connection.
        DiscordException
        
        Notes
        -----
        `before` argument is not supported by Discord.
        """
        reactions = message.reactions
        try:
            line=reactions[emoji]
        except KeyError:
            return []
        
        if line.unknown:
            data={}
            if (limit is not None):
                if type(limit) is not int:
                    raise TypeError(f'`limit` can be `None` or type `int`, got `{limit!r}`.')
                
                if limit<1 or limit>100:
                    raise ValueError(f'`limit` can be between 1-100, got `{limit!r}`.')
                
                data['limit']=limit
            
            if (after is not None):
                data['after']=log_time_converter(after)
            
            #if (before is not None):
            #    data['before']=log_time_converter(before)
            
            data = await self.http.reaction_users(message.channel.id,message.id,emoji.as_reaction,data)
            
            users=[User(user_data) for user_data in data]
            reactions._update_some_users(emoji,users)
            
        else:
            #if we know every reacters:
            if limit is None:
                limit=25
            elif type(limit) is not int:
                raise TypeError(f'`limit` can be `None` or type `int`, got `{limit!r}`')
            elif limit<1 or limit>100:
                raise ValueError(f'`limit` can be between 1-100, got `{limit!r}`')
            
            #before = 9223372036854775807 if before is None else log_time_converter(before)
            after = 0 if after is None else log_time_converter(after)
            users=line.filter_after(limit,after)
        
        return users
    
    async def reaction_users_all(self, message, emoji):
        """
        Requests the all the users, which reacted on the message with the given message.
        
        If the message has no reacters at all or no reacters with that emoji returns an empty list. If the emoji's
        every reacters are known, then do requests are done.
        
        Parameters
        ----------
        message : ``Message`` object
            The message, what's reactions will be requested.
        emoji : ``Emoji`` object
            The emoji, what's reacters will be requested.
        
        Returns
        -------
        users : `list` of (``Client`` or ``User``) objects
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        reactions = message.reactions
        if not reactions:
            return []
        
        try:
            line=reactions[emoji]
        except KeyError:
            return []
        
        if line.unknown:
            limit=len(line)
            data={'limit':100,'after':0}
            users=[]
            reaction=emoji.as_reaction
            
            while limit>0:
                user_datas = await self.http.reaction_users(message.channel.id,message.id,reaction,data)
                users.extend(User(user_data) for user_data in user_datas)
                
                data['after']=users[-1].id
                limit-=100
            
            reactions._update_all_users(emoji,users)
        else:
            #we copy
            users=list(line)
        
        return users
    
    async def reaction_load_all(self, message):
        """
        Requests all the reacters for every emoji on the given message.
        
        Like the other reaction getting methods, this method prefers using the internal cache as well over doing a
        request.
        
        Parameters
        ----------
        message : ``Message`` object
            The message, what's reactions will be requested.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        reactions = message.reactions
        if not reactions:
            return
        
        users=[]
        data={'limit':100,'after':0}
        for emoji,line in reactions.items():
            if not line.unknown:
                continue
            
            reaction=emoji.as_reaction
            data['after']=0
            limit=len(line)
            while limit>0:
                
                user_datas = await self.http.reaction_users(message.channel.id,message.id,reaction,data)
                users.extend(User(user_data) for user_data in user_datas)
                
                data['after']=users[-1].id
                limit-=100

            message.reactions._update_all_users(emoji,users)
            users.clear()
    
    # Guild
    
    async def guild_preview(self, guild_id):
        """
        Requests the preview of a public guild.
        
        Parameters
        ----------
        guild_id : `int`
            The id of the guild, what's preview will be requested
        
        Returns
        -------
        preview : ``GuildPreview``
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        data = await self.http.guild_preview(guild_id)
        return GuildPreview(data)
    
    async def guild_user_delete(self, guild, user, reason=None):
        """
        Removes the given user from the guild.
        
        Parameters
        ----------
        guild : ``Guild`` object
            The guild from where the user will be removed.
        user : ``User`` or ``Client`` instance
            The user to delete from the guild.
        reason : `str`, Optional
            Shows up at the guild's audit logs.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        await self.http.guild_user_delete(guild.id,user.id,reason)
    
    async def guild_ban_add(self, guild ,user, delete_message_days=0, reason=None):
        """
        Bans the given user from the guild.
        
        Parameters
        ----------
        guild : ``Guild`` object
            The guild from where the user will be banned.
        user : ``User`` or ``Client`` instance
            The user to ban from the guild.
        delete_message_days : `int`, optional
            How much days back the user's messages should be deleted. Can be between 0 and 7.
        reason : `str`, Optional
            Shows up at the guild's audit logs.
        
        Raises
        ------
        ValueError
            If `delete_message_days` is negative or over `7`.
        ConnectionError
            No internet connection.
        DiscordException
        """
        data={}
        if delete_message_days:
            if delete_message_days<1 or delete_message_days>7:
                raise ValueError(f'`delete_message_days` can be between 0-7, got {delete_message_days}')
            data['delete-message-days']=delete_message_days
        await self.http.guild_ban_add(guild.id,user.id,data,reason)
    
    async def guild_ban_delete(self, guild, user, reason=None):
        """
        Unbans the user from the given guild.
        
        Parameters
        ----------
        guild : ``Guild`` object
            The guild from where the user will be unbanned.
        user : ``User`` or ``Client`` instance
            The user to unban at the guild.
        reason : `str`, Optional
            Shows up at the guild's audit logs.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        await self.http.guild_ban_delete(guild.id,user.id,reason)
    
    async def guild_sync(self, guild_id):
        """
        Syncs a guild by it's id with the wrapper. Used internally if desync is detected when parsing dispatch events.
        
        Parameters
        ----------
        guild_id : `int`
            The id of the guild to sync.

        Returns
        -------
        guild : ``Guild``
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        # sadly guild_get does not returns channel and voice state data
        # at least we can request the channels
        try:
            guild=GUILDS[guild_id]
        except KeyError:
            data = await self.http.guild_get(guild_id)
            channel_datas = await self.http.guild_channels(guild_id)
            data['channels']=channel_datas
            user_data = await self.http.guild_user_get(guild_id,self.id)
            data['members']=[user_data]
            guild=Guild(data,self)
        else:
            data = await self.http.guild_get(guild_id)
            guild._sync(data)
            channel_datas = await self.http.guild_channels(guild_id)
            guild._sync_channels(channel_datas)
            
            user_data = await self.http.guild_user_get(guild_id,self.id)
            try:
                profile=self.guild_profiles[guild]
            except KeyError:
                self.guild_profiles[guild]=GuildProfile(user_data,guild)
                if guild not in guild.clients:
                    guild.clients.append(self)
            else:
                profile._update_no_return(user_data,guild)
        
        return guild

##    # Disable user syncing, takes too much time
##    async def _guild_sync_postprocess(self,guild):
##        for client in CLIENTS:
##            try:
##                user_data = await self.http.guild_user_get(guild.id,client.id)
##           except (DiscordException, ConnectionError):
##                continue
##            try:
##                profile=client.guild_profiles[guild]
##            except KeyError:
##                client.guild_profiles[guild]=GuildProfile(user_data,guild)
##                if client not in guild.clients:
##                    guild.clients.append(client)
##            else:
##                profile._update_no_return(user_data,guild)
##
##        if not CACHE_USER:
##            return
##
##        old_ids=set(guild.users)
##        data={'limit':1000,'after':'0'}
##        while True:
##            user_datas = await self.http.guild_users(guild.id,data)
##            for user_data in user_datas:
##                user=User._create_and_update(user_data,guild)
##                try:
##                    old_ids.remove(user.id)
##                except KeyError:
##                    pass
##             if len(user_datas)<1000:
##                 break
##             data['after']=user_datas[999]['user']['id']
##        del data
##
##        for id_ in old_ids:
##            try:
##               user=guild.users.pop(id_)
##           except KeyError:
##               continue #huh?
##           try:
##               del user.guild_profiles[guild]
##           except KeyError:
##               pass #huh??
    
    async def guild_leave(self, guild):
        """
        The client leaves the given guild.
        
        Parameters
        ----------
        guild : ``Guild``
            The guild from where the client will leave.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        await self.http.guild_leave(guild.id)
    
    async def guild_delete(self, guild):
        """
        Deletes the given guild. The client must be the owner of the guild.
        
        Parameters
        ----------
        guild : ``Guild`` object
            The guild to delete.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        await self.http.guild_delete(guild.id)
    
    async def guild_create(self         , name                                  ,
            icon                        = None                                  ,
            roles                       = []                                    ,
            channels                    = []                                    ,
            afk_channel_id              = None                                  ,
            system_channel_id           = None                                  ,
            afk_timeout                 = None                                  ,
            region                      = VoiceRegion.eu_central                ,
            verification_level          = VerificationLevel.medium              ,
            message_notification_level  = MessageNotificationLevel.only_mentions,
            content_filter_level        = ContentFilterLevel.disabled           ,
                ):
        """
        Creates a guild with the given parameter. A user account cant be member of 100 guilds maximum and a bot
        account can create a guild only if it is member of less than 10 guilds.
        
        Parameters
        ----------
        name : `str`
            The name of the new guild.
        icon : `None` or `bytes-like`, Optional
            The icon of the new guild.
        roles : `list` of ``cr_p_role_object`` returns, Optional
            A list of roles of the new guild. It should contain json serializable roles made by the
            ``cr_p_role_object`` function.
        channels : `list` of ``cr_pg_channel_object`` returns, Optional
            A list of channels of the new guild.  It should contain json serializable channels made by the
            ``cr_p_role_object`` function.
        afk_channel_id : `int`, Optional
            The id of the guild's afk channel. The id should be one of the channel's id from `channels`.
        system_channel_id: `int`, Optional
            The id of the guild's system channel. The id should be one of the channel's id from `channels`.
        afk_timeout : `int`, Optional
            The afk timeout for the users at the guild's afk channel.
        region : ``VoiceRegion``, Optional
            The voice region of the new guild.
        verification_level : ``VerificationLevel``, Optional
            The verification level of the new guild.
        message_notification_level : ``MessageNotificationLevel``, Optional
            The message notification level of the new guild.
        content_filter_level : ``ContentFilterLevel``, Optional
            The content filter level of the guild.
        
        Returns
        -------
        guild : ``Guild`` object
            A partial guild made from the received data.
        
        Raises
        ------
        TypeError
            - If `icon` is neither `None` or `bytes-like`.
        ValueError
            - If the client cannot create more guilds.
            - If the `name`'s length is less than 2 or longer than 100 characters.
            - If `icon` is passed as `bytes-like`, but it's format is not a valid image format.
            - If `afk_timeout` was passed and not as one of: `60, 300, 900, 1800, 3600`.
        ConnectionError
            No internet connection.
        DiscordException
        """
        if len(self.guild_profiles)>(99,9)[self.is_bot]:
            if self.is_bot:
                message='Bots cannot create a new server if they have 10 or more.'
            else:
                message='Hooman cannot have more than 100 guilds.'
            raise ValueError(message)
        
        name_ln=len(name)
        if name_ln<2 or name_ln>100:
            raise ValueError(f'Guild\'s name\'s length can be between 2-100, got {name_ln}')
        
        if icon is None:
            icon_data = None
        else:
            icon_type = icon.__class__
            if not issubclass(icon_type, (bytes, bytearray, memoryview)):
                raise TypeError(f'`icon` can be passed as `bytes-like`, got {icon_type.__name__}.')
            
            extension = get_image_extension(icon)
            if extension not in VALID_ICON_FORMATS:
                raise ValueError(f'Invalid icon type: `{extension}`.')
            
            icon_data = image_to_base64(icon)
        
        data = {
            'name'                          : name,
            'icon'                          : icon_data,
            'region'                        : region.id,
            'verification_level'            : verification_level.value,
            'default_message_notifications' : message_notification_level.value,
            'explicit_content_filter'       : content_filter_level.value,
            'roles'                         : roles,
            'channels'                      : channels,
                }
        
        if (afk_channel_id is not None):
            data['afk_channel_id'] = afk_channel_id
        
        if (system_channel_id is not None):
            data['system_channel_id'] = system_channel_id
        
        if (afk_timeout is not None):
            if afk_timeout not in (60,300,900,1800,3600):
                raise ValueError(f'Afk timeout should be 60, 300, 900, 1800, 3600 seconds!, got `{afk_timeout!r}`')
            data['afk_timeout']=afk_timeout
        
        data = await self.http.guild_create(data)
        #we can create only partial, because the guild data is not completed usually
        return PartialGuild(data)
    
    #kicks inactive users
    async def guild_prune(self, guild, days, roles=[], count=False, reason=None):
        """
        Kicks the members of the guild which were inactive since x days.
        
        Parameters
        ----------
        guild : ``Guild`` object
            Where the pruning will be executed.
        days : `int`
            The amount of days since atleast the users need to inactive. Needs to be at least `1`.
        roles : `list` of `Role` objects, Optional
            By default pruning will kick only the users without any roles, but it can defined which roles to include.
        count : `bool`, Optional
            Whether the method should return how much user were pruned, but if the guild is large it will be set to
            `False` anyways. Defaults to `False`.
        reason : `str`, Optional
            Will show up at the guild's audit logs.
        
        Returns
        -------
        count : `None` or `int`
            The number of pruned users or `None` if `count` is set to `False`.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        
        See Also
        --------
        .guild_prune_estimate : Returns how much user would be pruned if ``.guild_prune`` would be called.
        """
        if count and guild.is_large:
            count=False
        
        data = {
            'days'                  : days,
            'compute_prune_count'   : count,
                }
        
        if roles:
            data['include_roles'] = [role.id for role in roles]
        
        data = await self.http.guild_prune(guild.id,data,reason)
        return data['pruned']
    
    async def guild_prune_estimate(self, guild, days, roles=[]):
        """
        Returns the amount users, who would been pruned, if ``.guild_prune`` would be called.
        
        Parameters
        ----------
        guild : ``Guild`` object
            Where the counting of prunable users will be done.
        days : `int`
            The amount of days since atleast the users need to inactive. Needs to be at least `1`.
        roles : `list` of ``Role`` objects, Optional
            By default pruning would kick only the users without any roles, but it can be defined which roles to include.
        
        Returns
        -------
        count : `int`
            The amount of users who would be pruned.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        data = {
            'days'  : days,
                }
        
        if roles:
            data['include_roles'] = [role.id for role in roles]
        
        data = await self.http.guild_prune_estimate(guild.id,data)
        return data['pruned']
    
    async def guild_edit(self, guild, name=None, icon=_spaceholder, invite_splash=_spaceholder,
            discovery_splash=_spaceholder, banner=_spaceholder, afk_channel=_spaceholder, system_channel=_spaceholder,
            rules_channel=_spaceholder, public_updates_channel=_spaceholder, owner=None, region=None, afk_timeout=None,
            verification_level=None, content_filter=None, message_notification=None, description=_spaceholder,
            system_channel_flags=None, add_feature=None, remove_feature=None, reason=None):
        """
        Edis the guild with the given parameters.
        
        Parameters
        ----------
        guild : ``Guild``
            The guild to edit.
        name : `str`, Optional
            The guild's new name.
        icon : `None` or `bytes-like`, Optional
            The new icon of the guild. Can be `'jpg'`, `'png'`, `'webp'` image's raw data. If the guild has
            `ANIMATED_ICON` feature, it can be `'gif'` as well. By passing `None` you can remove the current one.
        invite_splash : `None` or `bytes-like`, Optional
            The new invite splash of the guild. Can be `'jpg'`, `'png'`, `'webp'` image's raw data. The guild must have
            `INVITE_SPLASH` feature. By passing it as `None` you can remove the current one.
        discovery_splash : `None` or `bytes-like`, Optional
            The new splash of the guild. Can be `'jpg'`, `'png'`, `'webp'` image's raw data. The guild must have
            `DISCOVERABLE` feature. By passing it as `None` you can remove the current one.
        banner : `None` or `bytes-like`, Optional
            The new splash of the guild. Can be `'jpg'`, `'png'`, `'webp'` image's raw data. The guild must have
            `BANNER` feature. By passing it as `None` you can remove the current one.
        afk_channel : `None` or ``ChannelVoice`` object, Optional
            The new afk channel of the guild. You can remove the current one by passing is as `None`.
        system_channel : `None` or ``ChannelText`` object, Optional
            The new system channel of the guild. You can remove the current one by passing is as `None`.
        rules_channel : `None` or ``ChannelText`` object, Optional
            The new rules channel of the guild. The guild must be a Community guild. You can remove the current
            one by passing is as `None`.
        public_updates_channel : `None` or ``ChannelText`` object, Optional
            The new public updates channel of the guild. The guild must be a Community guild. You can remove the
            current one by passing is as `None`.
        owner : ``User`` or ``Client`` object, Optional
            The new owner of the guild. You must be the owner of the guild to transfer ownership.
        region : ``VoiceRegion``, Optional
            The new voice region of the guild.
        afk_timeout : `int`, Optional
            The new afk timeout for the users at the guild's afk channel.
        verification_level : ``VerificationLevel``, Optional
            The new verification level of the guild.
        content_filter : ``ContentFilterLevel``, Optional
            The new content filter level of the guild.
        message_notification : ``MessageNotificationLevel``, Optional
            The new message notification level of the guild.
        description : `None` or `str` instance, Optional
            The new description of the guild. By passing `None`, or an empty string you can remove the current one. The
            guild must be a Community guild.
        system_channel_flags : ``SystemChannelFlag``, Optional
            The guild's system channel's new flags.
        add_feature : (`str`, ``GuildFeature``) or (`iterable` of (`str`, ``GuildFeature``)), Optional
            Guild feature(s) to add to the guild.
        remove_feature : (`str`, ``GuildFeature``) or (`iterable` of (`str`, ``GuildFeature``)), Optional
            Guild feature(s) to remove from the guild's.
        reason : `str`, Optional
            Shows up at the guild's audit logs.
        
        Raises
        ------
        TypeError
            - If `icon`, `invite_splash`, `discovery_splash`, `banner` is neither `None` or `bytes-like`.
            - If `add_feature` or `remove_feature` was not given neither as `str`, as ``GuildFeature`` or as as
                `iterable` of `str` or ``GuildFeature`` instances.
        ValueError
            - If name is shorter than 2 or longer than 100 characters.
            - If `icon`, `invite_splash`, `discovery_splash` or `banner` was passed as `bytes-like`, but it's format
                is not any of the expected formats.
            - If `discovery_splash` was gvien meanwhile teh guild is not discoverable.
            - If `rules_channel`, `description` or `public_updates_channel` was passed meanwhile the guild is not
                Community guild.
            - If `invite_splash` was passed meanwhile the guild has no `INVITE_SPLASH` feature.
            - If `banner` was passed meanwhile the guild has no `BANNER` feature.
            - If `owner` was passed meanwhile the client is not the owner of the guild.
            - If `afk_timeout` was passed and not as one of: `60, 300, 900, 1800, 3600`.
        ConnectionError
            No internet connection.
        DiscordException
        """
        data={}
        
        if (name is not None):
            name_ln=len(name)
            if name_ln<2 or name_ln>100:
                raise ValueError(f'Guild\'s name\'s length can be between 2-100, got {name_ln}: {name!r}.')
            data['name']=name
        
        if (icon is not _spaceholder):
            if icon is None:
                icon_data = None
            else:
                icon_type = icon.__class__
                if not issubclass(icon_type, (bytes, bytearray, memoryview)):
                    raise TypeError(f'`icon` can be passed as `bytes-like`, got {icon_type.__name__}.')
                
                extension = get_image_extension(icon)
                if extension not in (VALID_ICON_FORMATS_EXTENDED if (GuildFeature.animated_icon in guild.features) else VALID_ICON_FORMATS):
                    raise ValueError(f'Invalid icon type: `{extension}`.')
                
                icon_data = image_to_base64(icon)
            
            data['icon'] = icon_data
        
        if (banner is not _spaceholder):
            if GuildFeature.banner not in guild.features:
                raise ValueError('The guild has no `BANNER` feature.')
            
            if banner is None:
                banner_data = None
            else:
                banner_type = banner.__class__
                if not issubclass(banner_type, (bytes, bytearray, memoryview)):
                    raise TypeError(f'`banner` can be passed as `bytes-like`, got {banner_type.__name__}.')
                
                extension = get_image_extension(banner)
                if extension not in VALID_ICON_FORMATS:
                    raise ValueError(f'Invalid banner type: `{extension}`.')
                
                banner_data = image_to_base64(banner)
            
            data['banner'] = banner_data
        
        if (invite_splash is not _spaceholder):
            if GuildFeature.invite_splash not in guild.features:
                raise ValueError('The guild has no `INVITE_SPLASH` feature.')
            
            if invite_splash is None:
                invite_splash_data = None
            else:
                invite_splash_type = invite_splash.__class__
                if not issubclass(invite_splash_type, (bytes, bytearray, memoryview)):
                    raise TypeError(f'`invite_splash` can be passed as `bytes-like`, got '
                        f'{invite_splash_type.__name__}.')
                
                extension = get_image_extension(invite_splash)
                if extension not in VALID_ICON_FORMATS:
                    raise ValueError(f'Invalid invite splash type: `{extension}`.')
                
                invite_splash_data = image_to_base64(invite_splash)
                
            data['splash'] = invite_splash_data
        
        if (discovery_splash is not _spaceholder):
            if GuildFeature.discoverable not in guild.features:
                raise ValueError('The guild is not discoverable and `discovery_splash` was given.')
            
            if discovery_splash is None:
                discovery_splash_data = None
            else:
                discovery_splash_type = discovery_splash.__class__
                if not issubclass(discovery_splash_type, (bytes, bytearray, memoryview)):
                    raise TypeError(f'`discovery_splash` can be passed as `bytes-like`, got '
                        f'{discovery_splash_type.__name__}.')
                
                extension = get_image_extension(discovery_splash)
                if extension not in VALID_ICON_FORMATS:
                    raise ValueError(f'Invalid discovery_splash type: `{extension}`.')
                
                discovery_splash_data = image_to_base64(discovery_splash)
            
            data['discovery_splash'] = discovery_splash_data
        
        if (afk_channel is not _spaceholder):
            data['afk_channel_id']=None if afk_channel is None else afk_channel.id
        
        if (system_channel is not _spaceholder):
            data['system_channel_id']=None if system_channel is None else system_channel.id
        
        if (rules_channel is not _spaceholder):
            if not COMMUNITY_FEATURES&guild.features:
                raise ValueError('The guild is not Community guild and `rules_channel` was given.')
            data['rules_channel_id']=None if rules_channel is None else rules_channel.id
        
        if (public_updates_channel is not _spaceholder):
            if not COMMUNITY_FEATURES&guild.features:
                raise ValueError('The guild is not Community guild and `public_updates_channel` was given.')
            data['public_updates_channel_id']=None if public_updates_channel is None else public_updates_channel.id
        
        if (owner is not None):
            if (guild.owner!=self):
                raise ValueError('You must be owner to transfer ownership')
            data['owner_id']=owner.id
        
        if (region is not None):
            data['region']=region.id
        
        if afk_timeout is not None:
            if afk_timeout not in (60,300,900,1800,3600):
                raise ValueError(f'Afk timeout should be 60, 300, 900, 1800, 3600  seconds, got `{afk_timeout!r}`')
            data['afk_timeout']=afk_timeout
        
        if (verification_level is not None):
            data['verification_level']=verification_level.value
        
        if (content_filter is not None):
            data['explicit_content_filter']=content_filter.value
        
        if (message_notification is not None):
            data['default_message_notifications']=message_notification.value
        
        if (description is not _spaceholder):
            if not COMMUNITY_FEATURES&guild.features:
                raise ValueError('The guild is not Community guild and `description` was given.')
            
            if (description is not None) and (not description):
                description = None
            data['description']=description
        
        if (system_channel_flags is not None):
            data['system_channel_flags']=system_channel_flags
        
        if (add_feature is not None) or (remove_feature is not None):
            features = set(feature.value for feature in guild.features)
            
            for container, operation, variable_name in (
                        (add_feature, set.add, 'add_feature', ),
                        (remove_feature, set.remove, 'remove_feature', ),
                    ):
                
                if container is None:
                    continue
                
                # GOTO
                while True:
                    type_ = type(container)
                    if type_ is GuildFeature:
                        feature = add_feature.value
                    elif type_ is str:
                        feature = add_feature
                    elif issubclass(type_, str):
                        feature = str(add_feature)
                    elif hasattr(type_, '__iter__'):
                        index = 0
                        for feature in container:
                            type_ = type(feature)
                            if type_ is GuildFeature:
                                feature = feature.value
                            elif type_ is str:
                                feature = feature
                            elif issubclass(type_, str):
                                feature = str(feature)
                            else:
                                raise TypeError(f'`{variable_name}` was given as `iterable` so it expected to have '
                                    f'`str` or `{GuildFeature.__name__}` elements, but as element {index!r} got '
                                    f'{type_.__name__}.')
                            
                            try:
                                operation(features, feature)
                            except KeyError:
                                pass
                            
                            index +=1
                            continue
                        
                        break
                    else:
                        raise TypeError(f'`{variable_name}` can be given as `str`, as `{GuildFeature.__name__}` or as '
                            f'`iterable` of `str` or `{GuildFeature.__name__}`, got {type_.__name__}.')
                    
                    try:
                        operation(features, feature)
                    except KeyError:
                        pass
                    
                    break
            
            data['features'] = features
        
        await self.http.guild_edit(guild.id,data,reason)

    async def guild_bans(self, guild):
        """
        Returns the guild's bans.
        
        Parameters
        ----------
        guild : ``Guild`` object
            The guild, what's bans will be requested
        
        Returns
        -------
        bans : `list` of `tuple` ((``Client`` or ``User`` object), (`None` or `str`)) elements
            User, reason pairs for each ban entry.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        data=await self.http.guild_bans(guild.id)
        return [(User(ban_data['user']),ban_data.get('reason',None)) for ban_data in data]

    async def guild_ban_get(self, guild, user_id):
        """
        Returns the guild's ban entry for the given user id.
        
        Parameters
        ----------
        guild : ``Guild`` object
            The guild where the user banned.
        user_id : `int`
            The user's id, who's entry is requested.

        Returns
        -------
        user : ``Client`` or ``User`` object
        reason : `None` or `str`
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        data = await self.http.guild_ban_get(guild.id,user_id)
        return User(data['user']),data.get('reason',None)
    
    async def guild_embed_get(self, guild):
        """
        Returns the given guild's embed.
        
        Parameters
        ----------
        guild : ``Guild``
            The guild, what's embed is requested.
        
        Returns
        -------
        guild_embed : ``GuildEmbed``
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        
        Notes
        -----
        This function is symbolic, because `guild_edit` dispatch event updates the guild's embed and `Guild.embed`
        returns it.
        """
        data = await self.http.guild_embed_get(guild.id)
        return GuildEmbed(data,guild)
    
    async def guild_embed_edit(self, guild, enabled=None, channel=_spaceholder):
        """
        Edits the guild's embed with the given arguments.
        
        Parameters
        ----------
        guild : ``Guild`` object
            The guild to edit.
        enabled : `bool`, Optional
            Whether the guild's embed should be enabled.
        channel : `None` or ``ChannelText`` instance
            The new embed channel of the guild. Pass it as `None` to remove it.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        data={}
        if (enabled is not None):
            data['enabled']=enabled
        
        if (channel is not _spaceholder):
            data['channel_id']=None if channel is None else channel.id
        
        await self.http.guild_embed_edit(guild.id,data)
    
    async def guild_widget_get(self, guild_or_id):
        """
        Returns the guild's widget.
        
        Parameters
        ----------
        guild_or_id : ``Guild`` or `int`
            The guild or the guild's id, what's widget will be requested.
        
        Returns
        -------
        guild_widget : `None` or ``GuildWidget``
            If the guild has it's widget disabled returns `None` instead.
        
        Raises
        ------
        TypeError
            If `guild_or_id` was not passed as ``Guild`` or `int` instance.
        ConnectionError
            No internet connection.
        DiscordException
        """
        if type(guild_or_id) is Guild:
            guild_id=guild_or_id.id
        elif type(guild_or_id) is int:
            guild_id=guild_or_id
        else:
            raise TypeError(f'Excepted `{Guild.__name__}` or `int` (id), got `{guild_or_id!r}`')
        
        try:
            data = await self.http.guild_widget_get(guild_id)
        except DiscordException as err:
            if err.response.status==403: #Widget Disabled -> return None
                return
            raise
        
        return GuildWidget(data)
    
    async def guild_discovery_get(self, guild):
        """
        Requests and returns the guild's discovery metadata.
        
        The client must have `manage_guild` permission to execute this method.
        
        Parameters
        ----------
        guild : ``Guild``
            The guild what's disoovery will be requested.
        
        Returns
        -------
        guild_discovery : ``GuildDiscovery``
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        guild_discovery_data = await self.http.guild_discovery_get(guild.id)
        return GuildDiscovery(guild_discovery_data, guild)
    
    async def guild_discovery_edit(self, guild_or_discovery, primary_category=_spaceholder, keywords=_spaceholder,
            emoji_discovery=_spaceholder):
        """
        Edits the guild's discovery metadata.
        
        The client must have `manage_guild` permission to execute this method.
        
        Parameters
        ----------
        guild_or_discovery : ``Guild`` or ``GuildDiscovery``
            The guild what's discovery metadata will be edited or an existing discovery metadata object.
        primary_category : `None` or ``DiscoveryCategory`` or `int`, Optional
            The guild discovery's new primary category's id. Can be given as a ``DiscoveryCategory`` object as well.
            If given as `None`, then resets the guild discovery's primary category id to it's default, what is `0`.
        keywords : `None` or (`iterable` of `str`), Optional
            The guild discovery's new keywords. Can be given as `None` to reset to the default value, what is `None`,
            or as an `iterable` of strings.
        emoji_discovery : `None`, `bool` or `int` (`0`, `1`), Optional
            Whether the guild info should be shown when the respective guild's emojis are clicked. If passed as `None`
            then will reset the guild discovery's `emoji_discovery` value to it's default, what is `True`.
        
        Returns
        -------
        guild_discovery : ``GuildDiscovery``
            Updated guild discovery object.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        TypeError
            - If `guild_or_discovery` was neither passed as type ``Guild`` or ``GuildDiscovery``.
            - If `primary_category_id` was not given neither as `None`, `int` or as ``DiscoveryCategory`` instance.
            - If `keywords` was not passed neither as `None` or `iterable` of `str`.
            - If `emoji_discovery` was not passed neither as `None`, `bool` or `int` (`0`, `1`).
        ValueError
            - If `primary_category_id` was given as not primary ``DiscoveryCategory`` object.
            - If `emoji_discovery` was given as `int` instance, but not as `0` or `1`.
        DiscordException
        """
        if type(guild_or_discovery) is Guild:
            guild_id = guild_or_discovery.id
        elif type(guild_or_discovery) is GuildDiscovery:
            guild_id = guild_or_discovery.guild.id
        else:
            raise TypeError(f'`guild_or_discovery` can be `{Guild.__name__}` or `{GuildDiscovery.__name__}` instance, '
                f'got {guild_or_discovery.__class__.__name__}.')
        
        data = {}
        
        if (primary_category is not _spaceholder):
            if (primary_category is None):
                primary_category_id = None
            else:
                primary_category_type = primary_category.__class__
                if primary_category_type is DiscoveryCategory:
                    # If name is set means that we should know whether the category is loaded, or just it's `.id`
                    # is known.
                    if (primary_category.name and (not primary_category.primary)):
                        raise ValueError(f'The given `primary_category_id` was not given as a primary '
                            f'`{DiscoveryCategory.__name__}`, got {primary_category!r}.')
                    primary_category_id = primary_category.id
                elif primary_category_type is int:
                    primary_category_id = primary_category
                elif issubclass(primary_category_type, int):
                    primary_category_id = int(primary_category)
                else:
                    raise TypeError(f'`primary_category` can be given as `None`, `int` instance, or as '
                        f'`{DiscoveryCategory.__name__}` object, got {primary_category_type.__name__}.')
            
            data['primary_category_id'] = primary_category_id
        
        if (keywords is not _spaceholder):
            if (keywords is None):
                pass
            elif (not isinstance(keywords,str)) and hasattr(type(keywords),'__iter__'):
                keywords_processed = set()
                index = 0
                for keyword in keywords:
                    if (type(keyword) is str):
                        pass
                    elif isinstance(keyword,str):
                        keyword = str(keyword)
                    else:
                        raise TypeError(f'`keywords` can be `None` or `iterable` of `str`. Got `iterable`, but it\'s '
                            f'elemnet at index {index} is not `str` instance, got {keyword.__class__.__name__}.')
                    
                    keywords_processed.add(keyword)
                    index +=1
                
                keywords = keywords_processed
            else:
                raise TypeError(f'`keywords` can be `None` or `iterable` of `str`. Got {keywords.__class__.__name__}.')
        
            data['keywords'] = keywords
        
        if (emoji_discovery is not _spaceholder):
            if (emoji_discovery is None) or (type(emoji_discovery) is bool):
                pass
            elif isinstance(emoji_discovery, int):
                if emoji_discovery == 0:
                    emoji_discovery = False
                elif emoji_discovery == 1:
                    emoji_discovery = True
                else:
                    raise ValueError(f'`emoji_discovery` was given as `int` instance, but not as `0`, or `1`, got '
                        f'{emoji_discovery!r}.')
            else:
                raise TypeError(f'`emoji_discovery` can be given as `None`, `bool` or as `int` instance as `0` or '
                    f'`1`, got {emoji_discovery.__class__.__name__}.')
            
            data['emoji_discoverability_enabled'] = emoji_discovery
        
        guild_discovery_data = await self.http.guild_discovery_edit(guild_id, data)
        if type(guild_or_discovery) is Guild:
            guild_discovery = GuildDiscovery(guild_discovery_data, guild_or_discovery)
        else:
            guild_discovery = guild_or_discovery
            guild_discovery._update_no_return(guild_discovery_data)
        
        return guild_discovery
    
    async def guild_discovery_add_subcategory(self, guild_or_discovery, category):
        """
        Adds a discovery subcategory to the guild.
        
        The client must have `manage_guild` permission to execute this method.
        
        Parameters
        ----------
        guild_or_discovery : ``Guild`` or ``GuildDiscovery``
            The guild to what the discovery subcategory will be added.
        category : ``DiscoveryCategory`` or `int`
            The discovery category or it's id what will be added as a subcategory.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        TypeError
            - If `guild_or_discovery` was neither passed as type ``Guild`` or ``GuildDiscovery``.
            - If `category` was not passed neither as ``DiscoveryCategory`` or as `int` instance.
        DiscordException
        
        Notes
        -----
        A guild can have maximum `5` discovery subcategories.
        
        If `guild_or_discovery` was given as ``GuildDiscovery``, then it will be updated.
        """
        if type(guild_or_discovery) is Guild:
            guild_id = guild_or_discovery.id
        elif type(guild_or_discovery) is GuildDiscovery:
            guild_id = guild_or_discovery.guild.id
        else:
            raise TypeError(f'`guild_or_discovery` can be `{Guild.__name__}` or `{GuildDiscovery.__name__}` instance, '
                f'got {guild_or_discovery.__class__.__name__}.')
        
        category_type = category.__class__
        if category_type is DiscoveryCategory:
            category_id = category.id
        elif category_type is int:
            category_id = category
        elif issubclass(category_type, int):
            category_id = int(category)
        else:
            raise TypeError(f'`category` can be given either as `int` or as `{DiscoveryCategory.__name__} instance, '
                f'got {category_type.__name__}.')
        
        await self.http.guild_discovery_add_subcategory(guild_id, category_id)
        
        if type(guild_or_discovery) is GuildDiscovery:
            guild_or_discovery.sub_categories.add(category_id)
    
    async def guild_discovery_delete_subcategory(self, guild_or_discovery, category):
        """
        Removes a discovery subcategory of the guild.
        
        The client must have `manage_guild` permission to execute this method.
        
        Parameters
        ----------
        guild_or_discovery : ``Guild`` or ``GuildDiscovery``
            The guild to what the discovery subcategory will be removed from.
        category : ``DiscoveryCategory`` or `int`
            The discovery category or it's id what will be removed from the subcategories.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        TypeError
            - If `guild_or_discovery` was neither passed as type ``Guild`` or ``GuildDiscovery``.
            - If `category` was not passed neither as ``DiscoveryCategory`` or as `int` instance.
        DiscordException
        
        Notes
        -----
        A guild can have maximum `5` discovery subcategories.
        
        If `guild_or_discovery` was given as ``GuildDiscovery``, then it will be updated.
        """
        if type(guild_or_discovery) is Guild:
            guild_id = guild_or_discovery.id
        elif type(guild_or_discovery) is GuildDiscovery:
            guild_id = guild_or_discovery.guild.id
        else:
            raise TypeError(f'`guild_or_discovery` can be `{Guild.__name__}` or `{GuildDiscovery.__name__}` instance, '
                f'got {guild_or_discovery.__class__.__name__}.')
        
        category_type = category.__class__
        if category_type is DiscoveryCategory:
            category_id = category.id
        elif category_type is int:
            category_id = category
        elif issubclass(category_type, int):
            category_id = int(category)
        else:
            raise TypeError(f'`category` can be given either as `int` or as `{DiscoveryCategory.__name__} instance, '
                f'got {category_type.__name__}.')
        
        await self.http.guild_discovery_delete_subcategory(guild_id, category_id)
        
        if type(guild_or_discovery) is GuildDiscovery:
            try:
                guild_or_discovery.sub_categories.remove(category_id)
            except KeyError:
                pass
    
    async def discovery_categories(self):
        """
        Returns a list of discovery categories, which can be used when editing guild discovery.
        
        Returns
        -------
        discovery_categories : `list` of ``DiscoveryCategory``
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        discovery_category_datas = await self.http.discovery_categories()
        return [DiscoveryCategory.from_data(discovery_category_data) for discovery_category_data in discovery_category_datas]
    
    # Add cached, so even tho the first request fails with `ConnectionError` will not be raised.
    discovery_categories = DiscoveryCategoryRequestCacher(discovery_categories, 3600.0,
        cached=list(DISCOVERY_CATEGORIES.values()))
    
    async def discovery_validate_term(self, term):
        """
        Checks whether the given discovery search term is valid.
        
        Parameters
        ----------
        term : `str`
        
        Returns
        -------
        valid : `bool`
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        data = await self.http.discovery_validate_term({'term': term})
        return data['valid']
    
    discovery_validate_term = DiscoveryTermRequestCacher(discovery_validate_term, 86400.0,
        RATELIMIT_GROUPS.discovery_validate_term)
    
    async def guild_users(self, guild):
        """
        Requests all the users of the guild and returns them.
        
        Parameters
        ----------
        guild : ``Guild``
            The guild what's users will be requested.
        
        Returns
        -------
        users : `list` of (``User`` or ``Client``) objects
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        
        Notes
        -----
        If user caching is allowed, these users should be already loaded if the client finished starting up.
        This method takes a long time to finish for huge guilds.
        """
        data={'limit':1000,'after':'0'}
        result=[]
        while True:
            user_datas = await self.http.guild_users(guild.id,data)
            for user_data in user_datas:
                user=User(user_data,guild)
                result.append(user)
            if len(user_datas)<1000:
                break
            data['after']=user_datas[999]['user']['id']
        return result
    
    async def guild_get_all(self):
        """
        Requests all the guilds of the client.
        
        Returns
        -------
        guilds : `list` of ``Guilds` objects
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        
        Notes
        -----
        If the client finished starting up, all the guilds should be already loaded.
        """
        result=[]
        params={'after':0}
        while True:
            data = await self.http.guild_get_all(params)
            result.extend(PartialGuild(guild_data) for guild_data in data)
            if len(data)<100:
                break
            params['after']=result[-1].id
        
        return result
    
    async def guild_regions(self, guild):
        """
        Requests the available voice regions for the given guild and returns them and the optiomal ones.
        
        Parameters
        ----------
        guild : ``Guild``
            The guild, what's regions will be requested.
        
        Returns
        -------
        voice_regions : `list` of ``VoiceRegion`` objects
            The available voice reions for the guild.
        optimals : `list` of ``VoiceRegion`` objects
            The optimal voice regions for the guild.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        data = await self.http.guild_regions(guild.id)
        results=[]
        optimals=[]
        for voice_region_data in data:
            region=VoiceRegion.from_data(voice_region_data)
            results.append(region)
            if voice_region_data['optimal']:
                optimals.append(region)
        return results, optimals

    async def guild_sync_channels(self, guild):
        """
        Requests the given guild's channels and if there any desync between the wrapper and Discord, applies the
        changes.
        
        Parameters
        ----------
        guild : ``Guild``
            The guild, what's channels will be requested.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        data = await self.http.guild_channels(guild.id)
        guild._sync_channels(data)

    async def guild_sync_roles(self, guild):
        """
        Requests the given guild's roles and if there any desync between the wrapper and Discord, applies the
        changes.
        
        Parameters
        ----------
        guild : ``Guild``
            The guild, what's roles will be requested.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        data = await self.http.guild_roles(guild.id)
        guild._sync_roles(data)
    
    async def audit_logs(self, guild, limit=100, before=None, after=None, user=None, event=None,):
        """
        Request a batch of audit logs of the guild and returns them. The `after`, `around` and the `before` arguments
        are mutually exclusive and they can be passed as `int`, or as a ``DiscordEntitiy`` instance or as a `datetime`
        object.
        
        Parameters
        ----------
        guild : ``Guild``
            The guild, what's audit logs will be requested.
        limit : `int`, Optional
            The amount of audit logs to request. Can b between 1 and 100. Defaults to 100.
        before : `int`, ``DiscordEntity` or `datetime`, Optional
            The timestamp before the audit log entries wer created.
        after : `int`, ``DiscordEntity`` or `datetime`, Optional
            The timestamp after the audit log entries wer created.
        user : ``Client`` or ``User`` object, Optional
            Whether the audit logs should be filtered only to those, which were created by the given user.
        event : ``AuditLogEvent``, Optional
            Whether the audit logs should be filtered only on the given event.
        
        Returns
        -------
        audit_log : ``AuditLog``
            A container what contains the ``AuditLogEntry``-s.
        
        Raises
        ------
        ValueError
            If `limit` is under `1` or over `100`.
        ConnectionError
            No internet connection.
        DiscordException
        """
        if limit<1 or limit>100:
            raise ValueError(f'Limit can be in <1,100>, got {limit}')
        
        data={'limit':limit}
        
        if (before is not None):
            data['before']=log_time_converter(before)
        
        if (after is not None):
            data['after']=log_time_converter(after)
        
        if (user is not None):
            data['user_id']=user.id
        
        if (event is not None):
            data['action_type']=event.value
        
        data = await self.http.audit_logs(guild.id,data)
        return AuditLog(data,guild)
    
    def audit_log_iterator(self, guild, user=None, event=None):
        """
        Returns an audit log iterator for the given guild.
        
        Parameters
        ----------
        guild : ``Guild``
            The guild, what's audit logs will be requested.
        user : ``Client`` or ``User`` object, Optional
            Whether the audit logs should be filtered only to those, which were created by the given user.
        event : ``AuditLogEvent``, Optional
            Whether the audit logs should be filtered only on the given event.
        
        Returns
        -------
        audit_log_iterator : ``AuditLogIterator``
        """
        return AuditLogIterator(self, guild, user=user, event=event)
    
    #users
    
    async def user_edit(self, guild, user, nick=_spaceholder, deaf=None, mute=None, voice_channel=_spaceholder,
            roles=None, reason=None):
        """
        Edits the user at the given guild.
        
        Parameters
        ----------
        guild : ``Guild``
            Where the user will be edited.
        user : ``User`` or ``Client`` object
            The user to edit
        nick : `None` or `str`, Optional
            The new nick of the user. You can remove the current one by passing it as `None` or as an empty string.
        deaf : `bool`, Optional
            Whether the user should be deafen at the voice channels.
        mute : `bool`, Optional
            Whether the user should be muted at the voice channels.
        voice_channel : `None` or ``ChannelVoice`` object, Optional
            Moves the user to the given voice channel. Only applicable if the user is already at a voice channel.
            Pass it as `None` to kick the user from it's voice channel.
        roles : `list` of ``Role`` objects, Optional
            The new roles of the user.
        reason : `str`, Optional
            Will show up at the guild's audit logs.
        
        Raises
        ------
        ValueError
            If `nick` was passed as `str` and it's length is over `32`.
        ConnectionError
            No internet connection.
        DiscordException
        """
        data={}
        if (nick is not _spaceholder):
            if (nick is not None):
                nick_ln=len(nick)
                if nick_ln>32:
                    raise ValueError(f'The length of the nick can be between 1-32, got {nick_ln}')
                if nick_ln==0:
                    nick=None
            
            should_edit_nick=False
            try:
                actual_nick=user.guild_profiles[guild].nick
            except KeyError:
                # user cache disabled, or the user is not at the guild -> will raise later
                should_edit_nick=True
            else:
                if (nick is None):
                    if (actual_nick is None):
                        should_edit_nick=False
                    else:
                        should_edit_nick=True
                else:
                    if (actual_nick is None):
                        should_edit_nick=True
                    elif actual_nick==nick:
                        should_edit_nick=False
                    else:
                        should_edit_nick=True
            
            if should_edit_nick:
                if self==user:
                    await self.http.client_edit_nick(guild.id,{'nick':nick},reason)
                else:
                    data['nick']=nick
                    
        if (deaf is not None):
            data['deaf']=deaf
            
        if (mute is not None):
            data['mute']=mute
            
        if (voice_channel is not _spaceholder):
            data['channel_id']=None if voice_channel is None else voice_channel.id
            
        if (roles is not None):
            data['roles']=[role.id for role in roles]
            
        await self.http.user_edit(guild.id,user.id,data,reason)

    async def user_role_add(self, user, role, reason=None):
        """
        Adds the role on the user.
        
        Parameters
        ----------
        user : ``Client`` or ``User``
            The user who will get the role.
        role : ``Role``
            The role to add on the user.
        reason : `str`, Optional
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        # If the role is partial, it's guild is None.
        guild = role.guild
        if guild is None:
            return
        
        await self.http.user_role_add(guild.id,user.id,role.id,reason)

    async def user_role_delete(self, user, role, reason=None):
        """
        Deletes the role from the user.
        
        Parameters
        ----------
        user : ``Client`` or ``User``
            The user from who the role will be removed.
        role : ``Role``
            The role to remove from the user.
        reason : `str`, Optional
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        # If the role is partial, it's guild is None.
        guild = role.guild
        if guild is None:
            return
        
        await self.http.user_role_delete(guild.id,user.id,role.id,reason)

    async def user_voice_move(self, user, voice_channel):
        """
        Moves the user to the givn voice channel. The user must be in a voice channel at the respective guild already.
        
        Parameters
        ----------
        user : ``Client`` or ``User``
            The user to move.
        voice_channel : ``ChannelVoice``
            The channel where the user will be moved.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        # If the channel is partial, it's guild is None.
        guild = voice_channel
        if guild is None:
            return
       
        await self.http.user_move(guild.id,user.id,{'channel_id':voice_channel.id})
    
    async def user_voice_kick(self, user, guild):
        """
        Kicks the user from the guild's voice channels. The user must be in a voice channel at the guild.
        
        Parameters
        ----------
        user : ``Client`` or ``User``
            The user who will be kicked from the voice channel.
        guild : ``Guild``
            The guild from what's voice channel the user will be kicked.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        await self.http.user_move(guild.id,user.id,{'channel_id':None})
    
    async def user_get(self, user_id):
        """
        Gets an user by it's id. If the user is already loaded updates it.
        
        Parameters
        ----------
        user_id : `int`
            The user's id, who will be requested.
        
        Returns
        -------
        user : ``Client`` or ``User``
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        data = await self.http.user_get(user_id)
        return User._create_and_update(data)
    
    async def guild_user_get(self, guild, user_id):
        """
        Gets an user and it's profile at a guild. The user must be the member of the guild. If the user is already
        loaded updates it.
        
        Parameters
        ----------
        guild : ``Guild``
            The guild, where the user is.
        user_id : `int`
            The user's id, who will be requested.
        
        Returns
        -------
        user : ``Client`` or ``User``
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        data = await self.http.guild_user_get(guild.id, user_id)
        return User._create_and_update(data, guild)
    
    async def guild_user_search(self, guild, query, limit=1):
        """
        Gets an user and it's profile at a guild by it's name. If the users are already loaded updates it.
        
        Parameters
        ----------
        guild : ``Guild``
            The guild, where the user is.
        query : `name`
            The query string with what the user's name or nick should start.
        limit : `int`, Optional
            The maximal amount of users to return. Can bebetween `1` and `1000`. Defaults to `1`.
        
        Returns
        -------
        users : `list` of (``Client`` or ``User``)
        
        Raises
        ------
        ValueError
            If limit is not between `1` and `1000`.
        ConnectionError
            No internet connection.
        DiscordException
        """
        data = {'query': query}
        
        if limit == 1:
            # default limit is `0`, so not needed to send it.
            pass
        elif limit > 0 and limit < 1000:
            data['limit'] = limit
        else:
            raise ValueError('`limit` can be betwwen 1 and 1000, got `{limit}`')
        
        data = await self.http.guild_user_search(guild.id, data)
        return [User._create_and_update(user_data, guild) for user_data in data]
    
    #integrations
    
    #TODO: decide if we should store integrations at Guild objects
    async def integration_get_all(self, guild):
        """
        Requests the integrations of the given guild.
        
        Parameters
        ----------
        guild : ``Guild``
            The guild, what's intgrations will be requested.
        
        Returns
        -------
        integrations : `list` of ``Integration`` objects
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        data = await self.http.integration_get_all(guild.id)
        return [Integration(integration_data) for integration_data in data]
    
    #TODO: what is integration id?
    async def integration_create(self, guild, integration_id, type_):
        """
        Creates an integration at the given guild.
        
        Parameters
        ----------
        guild : ``Guild``
            The guild to what the integration will be attached to.
        integration_id : ``int``
            The integration's id.
        type_ : `str`
            The integration's type (`'twitch'`, `'youtube'`, etc.).
        
        Returns
        -------
        integration : ``Integration``
            The created integrated.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        data = {
            'id'    : integration_id,
            'type'  : type_,
                }
        data = await self.http.integration_create(guild.id,data)
        return Integration(data)

    async def integration_edit(self, integration, expire_behavior=None, expire_grace_period=None, enable_emojis=True):
        """
        Edits the given integration.
        
        Parameters
        ----------
        integration : ``Integration``
            The integration to edit.
        expire_behavior : `int`, Optional
            Can be `0` for kick or `1` for role  remove.
        expire_grace_period : `int`, Optional
            The time in days, after the subscribtion will be ignored. Can be `1`, `3`, `7`, `14` or `30`.
        enable_emojis : `bool`, Optional
            Twitch only.
        
        Raises
        ------
        TypeError
            - If `expire_behavior` was not passed as `int`.
            - If `expire_grace_period` was not passed as `int`.
            - If `enable_emojis` was not passed as `bool`.
        ValueError
            - If `expire_behavior` was passed as `int`, but not any of: `0`, `1`.
            - If `expire_grace_period` was passed as `int`, but not any of `1`, `3`, `7`, `14`, `30`.
        ConnectionError
            No internet connection.
        DiscordException
        """
        guild = integration.role.guild
        if guild is None:
            return
        
        if expire_behavior is None:
            expire_behavior=integration.expire_behavior
        elif type(expire_behavior) is int:
            if expire_behavior not in (0,1):
                raise ValueError(f'`expire_behavior` should be 0 for kick, 1 for remove role, got {expire_behavior!r}.')
        else:
            raise TypeError(f'`expire_behavior` should be type `int`, got {expire_behavior.__class__.__name__}.')
        if expire_grace_period is None:
            expire_grace_period=integration.expire_grace_period
        elif type(expire_grace_period) is int:
            if expire_grace_period not in (1,3,7,14,30):
                raise ValueError(f'`expire_grace_period` should be 1, 3, 7, 14, 30, got {expire_grace_period!r}.')
        else:
            raise TypeError(f'`expire_grace_period` should be type `int`, got {expire_grace_period.__class__.__name__}.')
        
        data = {
            'expire_behavior'       : expire_behavior,
            'expire_grace_period'   : expire_grace_period,
                }
        
        if integration.type=='twitch' and (enable_emojis is not None):
            if type(enable_emojis) is not bool:
                raise TypeError(f'`enable_emojis` should be `bool`, got {enable_emojis.__class__.__name__}.')
            data['enable_emoticons']=enable_emojis
        
        await self.http.integration_edit(guild.id,integration.id,data)
    
    async def integration_delete(self, integration):
        """
        Deletes the given integration.
        
        Parameters
        ----------
        integration : ``Integation``
            The integration what will be deleted.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        guild = integration.role.guild
        if guild is None:
            return
        
        await self.http.integration_delete(guild.id,integration.id)
    
    async def integration_sync(self, integration):
        """
        Sync th givn integration's state.
        Parameters
        ----------
        integration : ``Integation``
            The integration to sync.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        guild = integration.role.guild
        if guild is None:
            return
        
        await self.http.integration_sync(guild.id,integration.id)
    
    async def permission_ow_edit(self, channel, overwrite, allow, deny, reason=None):
        """
        Edits the given prmission overwrite.
        
        Parameters
        ----------
        channel : ˙˙ChannelGuildBase`` instance
            The channel where the permission overwrite is.
        overwrite : ``PermOW``
            The permission overwrite to edit.
        allow : ``Permission``
            The permission overwrite's new allowed permission's value.
        deny : ``Permission``
            The permission overwrite's new denied permission's value.
        reason : `str`, Optional
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        data = {
            'allow' : allow,
            'deny'  : deny,
            'type'  : overwrite.type
                }
        await self.http.permission_ow_create(channel.id,overwrite.target.id,data,reason)
    
    async def permission_ow_delete(self, channel, overwrite, reason=None):
        """
        Deletes the given permission overwrite.
        
        Parameters
        ----------
        channel : ˙˙ChannelGuildBase`` instance
            The channel where the permission overwrite is.
        overwrite : ``PermOW``
            The permission overwrite to delete.
        reason : `str`, Optional
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        await self.http.permission_ow_delete(channel.id,overwrite.target.id,reason)
    
    async def permission_ow_create(self, channel, target, allow, deny, reason=None):
        """
        Creates a permission overwrite at the given channel.
        
        Parameters
        ----------
        channel : ``ChannelGuildBase`` instance
            The channel to what the permission ovrwrite will be added.
        target : ``Role`` or ``UserBase`` instance
            The permission overwrite's target.
        allow : ``Permission``
            The permission overwrite's allowed permission's value.
        deny : ``Permission``
            The permission overwrite's denied permission's value.
        reason : `str`, Optional
            Shows up at the respective guild's audit logs.
        
        Returns
        -------
        permission_overwrit : PermOW
            A permission overwrite, what estimatedly is same as the one what Discord will create.
        
        Raises
        ------
        TypeError
            If `target` was not passed neither as ``Role`` or as ``UserBase`` instance.
        ConnectionError
            No internet connection.
        DiscordException
        """
        if type(target) is Role:
            type_='role'
        elif isinstance(target, UserBase):
            type_='member'
        else:
            raise TypeError(f'`target` can be either `{Role.__name__}` or `{UserBase.__name__}` instance, got {target.__class__.__name__}.')
        
        data = {
            'target': target.id,
            'allow' : allow,
            'deny'  : deny,
            'type'  : type_,
                }
        
        await self.http.permission_ow_create(channel.id,target.id,data,reason)
        return PermOW.custom(target, allow, deny)
    
    # Webhook management
    
    async def webhook_create(self, channel, name, avatar=None):
        """
        Creates a webhook at the given channel.
        
        Parameters
        ----------
        channel : ``ChannelText``
            The channel of the created webhook.
        name : `str`
            The name of the new webhook. It's lngth can be between `1` and `80`.
        avatar : `bytes-like`, Optional
            The webhook's avatar. Can be `'jpg'`, `'png'`, `'webp' or `'gif'` image's raw data. However if set as
            `'gif'`, it will not have any animation.
            
        Returns
        -------
        webhook : ``Webhook``
            The created webhook.
        
        Raises
        ------
        TypeError
            If `avatar` was passed, but not as `bytes-like`.
        ValueError
            - If `name`'s length is under `1` or over `80`.
            - If `avatar` was passed as `bytes-like`, but it's format is not `'jpg'`, `'png'`, `'webp' or `'gif'`.
        ConnectionError
            No internet connection.
        DiscordException
        """
        name_ln=len(name)
        if name_ln==0 or name_ln>80:
            raise ValueError(f'`name` length can be between 1-80, got {name!r}')
        
        data={'name':name}
        
        if (avatar is not None):
            avatar_type = avatar.__class__
            if not issubclass(avatar_type, (bytes, bytearray, memoryview)):
                raise TypeError(f'`icon` can be passed as `bytes-like`, got {avatar_type.__name__}.')
            
            extension = get_image_extension(avatar)
            if extension not in VALID_ICON_FORMATS_EXTENDED:
                raise ValueError(f'Invalid icon type: `{extension}`.')
            
            data['avatar'] = image_to_base64(avatar)
        
        data = await self.http.webhook_create(channel.id, data)
        return Webhook(data)

    async def webhook_get(self, webhook_id):
        """
        Requests the webhook by it's id.
        
        Parameters
        ----------
        webhook_id : `int`
            The webhook's id.
        
        Returns
        -------
        webhook : ``Webhook``
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        
        See Also
        --------
        .webhook_get_token : Getting webhook with Discord's webhook API.
        
        Notes
        -----
        If the webhook already loaded and if it's guild's webhooks are up to date, no request is done.
        """
        try:
            webhook=USERS[webhook_id]
        except KeyError:
            data = await self.http.webhook_get(webhook_id)
            return Webhook(data)
        else:
            channel=webhook.channel
            if (channel is not None):
                guild = channel.guild
                if (guild is not None) and guild.webhooks_uptodate:
                    return webhook
            
            data = await self.http.webhook_get(webhook_id)
            webhook._update_no_return(data)
            return webhook
    
    async def webhook_get_token(self, webhook_id, webhook_token):
        """
        Requests the webhook through Discord's webhook API.
        
        Parameters
        ----------
        webhook_id : `int`
            The webhook's id.
        webhook_token : `str`
            The webhook's token.
        
        Returns
        -------
        webhook : ``Webhook``
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        
        Notes
        -----
        If the webhook already loaded and if it's guild's webhooks are up to date, no request is done.
        """
        try:
            webhook=USERS[webhook_id]
        except KeyError:
            webhook = PartialWebhook(webhook_id,webhook_token)
        else:
            channel = webhook.channel
            if (channel is not None):
                guild = channel.guild
                if (guild is not None) and guild.webhooks_uptodate:
                    return webhook

            data = await self.http.webhook_get_token(webhook)
            webhook._update_no_return(data)
            return webhook

    async def webhook_update(self, webhook):
        """
        Updates the given webhook.
        
        Parameters
        ----------
        webhook : ``Webhook``
            The webhook to update.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        
        See Also
        --------
        .webhook_update_token : Updating webhook with Discord webhook API.
        """
        data = await self.http.webhook_get(webhook.id)
        webhook._update_no_return(data)

    async def webhook_update_token(self, webhook):
        """
        Updates the given webhook through Discord's webhook API.
        
        Parameters
        ----------
        webhook : ``Webhook``
            The webhook to update.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        data = await self.http.webhook_get_token(webhook)
        webhook._update_no_return(data)
        
    async def webhook_get_channel(self, channel):
        """
        Requests the webhooks of the channel.
        
        Parameters
        ----------
        channel : ``ChannelText``
            The channel, what's webhooks will be requested.
        
        Returns
        -------
        webhooks : `list` of ``Webhook` objects
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        
        Notes
        -----
        No request is done, if the passed channel is partial, or if the channel's guild's webhooks are up to date.
        """
        guild = channel.guild
        if guild is None:
            return []
        
        if guild.webhooks_uptodate:
            return [webhook for webhook in guild.webhooks.values() if webhook.channel is channel]
        
        data = await self.http.webhook_get_channel(channel.id)
        return [Webhook(data) for data in data]
    
    async def webhook_get_guild(self, guild):
        """
        Requests the webhooks of the given guild.
        
        Parameters
        ----------
        guild : ``Guild``
            The guild, what's webhooks will be requested.
        
        Returns
        -------
        webhooks : `list` of ``Webhook` objects
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        
        Notes
        -----
        No request is done, if the guild's webhooks are up to date.
        """
        if guild.webhooks_uptodate:
            return list(guild.webhooks.values())
        
        old_ids=list(guild.webhooks)
        
        result=[]
        
        data=await self.http.webhook_get_guild(guild.id)
        for webhook_data in data:
            webhook=Webhook(webhook_data)
            result.append(webhook)
            try:
                old_ids.remove(webhook.id)
            except ValueError:
                pass
            
        if old_ids:
            for id_ in old_ids:
                guild.webhooks[id_]._delete()

        guild.webhooks_uptodate=True
        
        return result
        
    async def webhook_delete(self, webhook):
        """
        Delets the webhook.
        
        Parameters
        ----------
        webhook : ``Webhook``
            The webhook to delete.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        
        See Also
        --------
        .webhook_delete_token : Deleting webhook with Discord's webhook API.
        """
        await self.http.webhook_delete(webhook.id)

    async def webhook_delete_token(self, webhook):
        """
        Deletes the webhook through Discord's webhook API.
        
        Parameters
        ----------
        webhook : ``Webhook``

        Parameters
        ----------
        webhook : ``Webhook``
            The webhook to delete.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        await self.http.webhook_delete_token(webhook)
            
    #later there gonna be more stuff thats why 2 different
    async def webhook_edit(self, webhook, name=None, avatar=_spaceholder, channel=None):
        """
        Edits and updates the given webhook.
        
        Parameters
        ----------
        webhook : ``Webhook``
            The webhook to edit.
        name : `str`, Optional
            The webhook's new name. It's length can be between `1` and `80`.
        avatar : `None` or `bytes-like`, Optional
            The webhook's new avatar. Can be `'jpg'`, `'png'`, `'webp' or `'gif'` image's raw data. However if set as
            `'gif'`, it will not have any animation. If passed as `None`, will remove the webhook's current avatar.
        channel : ``ChannelText``
            The webhook's name channel.
        
        Raises
        ------
        TypeError
            If `avatar` was passed, but not as `bytes-like`.
        ValueError
            - If `name`'s length is under `1` or over `80`.
            - If `avatar` was passed as `bytes-like`, but it's format is not `'jpg'`, `'png'`, `'webp' or `'gif'`.
        ConnectionError
            No internet connection.
        DiscordException
        
        See Also
        --------
        .webhook_edit_token : Editing webhook with Discord's webhook API.
        """
        data={}
        
        if (name is not None):
            name_ln=len(name)
            if name_ln==0 or name_ln>80:
                raise ValueError(f'The length of the name can be between 1-80, got {name!r}')
            
            data['name']=name
        
        if (avatar is not _spaceholder):
            if avatar is None:
                avatar_data = None
            else:
                avatar_type = avatar.__class__
                if not issubclass(avatar_type, (bytes, bytearray, memoryview)):
                    raise TypeError(f'`icon` can be passed as `bytes-like`, got {avatar_type.__name__}.')
            
                extension = get_image_extension(avatar)
                if extension not in VALID_ICON_FORMATS_EXTENDED:
                    raise ValueError(f'Invalid icon type: `{extension}`.')
                
                avatar_data = image_to_base64(avatar)
            
            data['avatar'] = avatar_data
        
        if (channel is not None):
            data['channel_id']=channel.id
        
        if not data:
            return #save 1 request
        
        data = await self.http.webhook_edit(webhook.id,data)
        webhook._update_no_return(data)
        
    async def webhook_edit_token(self, webhook, name=None, avatar=_spaceholder): #channel is ignored!
        """
        Edits and updates the given webhook through Discord's webhook API.
        
        Parameters
        ----------
        webhook : ``Webhook``
            The webhook to edit.
        name : `str`, Optional
            The webhook's new name. It's length can be between `1` and `80`.
        avatar : `None` or `bytes-like`, Optional
            The webhook's new avatar. Can be `'jpg'`, `'png'`, `'webp' or `'gif'` image's raw data. However if set as
            `'gif'`, it will not have any animation. If passed as `None`, will remove the webhook's current avatar.
        
        Raises
        ------
        TypeError
            If `avatar` was passed, but not as `bytes-like`.
        ValueError
            - If `name`'s length is under `1` or over `80`.
            - If `avatar` was passed as `bytes-like`, but it's format is not `'jpg'`, `'png'`, `'webp' or `'gif'`.
        ConnectionError
            No internet connection.
        DiscordException
        
        Notes
        -----
        This endpoint cannot edit the webhook's channel, like ``.webhook_edit``.
        """
        data={}
        
        if (name is not None):
            name_ln=len(name)
            if name_ln==0 or name_ln>80:
                raise ValueError(f'The length of the name can be between 1-80, got {name_ln}')
            
            data['name']=name
        
        if (avatar is not _spaceholder):
            if avatar is None:
                avatar_data = None
            else:
                avatar_type = avatar.__class__
                if not issubclass(avatar_type, (bytes, bytearray, memoryview)):
                    raise TypeError(f'`icon` can be passed as `bytes-like`, got {avatar_type.__name__}.')
                
                extension = get_image_extension(avatar)
                if extension not in VALID_ICON_FORMATS_EXTENDED:
                    raise ValueError(f'Invalid icon type: `{extension}`.')
                
                avatar_data = image_to_base64(avatar)
            
            data['avatar'] = avatar_data
        
        if not data:
            return #save 1 request
        
        data = await self.http.webhook_edit_token(webhook,data)
        webhook._update_no_return(data)
   
    async def webhook_send(self, webhook, content=None, embed=None, file=None, allowed_mentions=_spaceholder,
            tts=False, name=None, avatar_url=None, wait=False):
        """
        Sends a message with the given webhook. If there is nothing to send, or if `wait` was not passed as `True`
        returns `None`.
        
        Parameters
        ----------
        webhook : ``Webhook``
            The webhook through what will the message be sent.
        content : `str`, Optional
            The content of the message.
        embed : ``Embed`` or ``EmbedCore`` instances of any compatible object, or a `tuple`, `list` or `deque` of them
            The embedded content of the message.
        file : `Any`, Optional
            A file to send. Check ``._create_file_form`` for details.
        allowed_mentions : `None` or `list` of `Any`, Optional
            Which user or role can the message ping (or everyone). Check ``._parse_allowed_mentions`` for details.
        tts : `bool`, Optional
            Whether the message is text-to-speech.
        name : `str`, Optional
            The mesage's author's new name. Default to the webhook's name by Discord.
        avatar_url : `str`, Optional
            The message's author's avatar's url. Defaults to the webhook's avatar' url by Discord.
        wait : `bool`, Optional
            Whether we should wait for the message to send and receive it's data as well.
        
        Returns
        -------
        message : ``Message`` or `None`
            Returns `None` if there is nothing to send.
        
        Raises
        ------
        TypeError
            - If `allowed_mentions` when correct type, but an invalid value would been sent.
            - If ivalid file type would be sent.
            - If `embed` was not passed as an embed like, or a `tuple`, `list` or `deque` of them.
        ValueError
            - If more than `10` files would be sent.
            - If `allowed_mentions` contains an element of invalid type.
            - If `name` was passed, but with length under `1` or over `32`.
        ConnectionError
            No internet connection.
        DiscordException
        """
        data={}
        contains_content=False
        
        if (embed is not None):
            if isinstance(embed,(tuple,list,deque)):
                embed_amount=len(embed)
                if embed_amount>10:
                    raise ValueError(f'There can be only 10 embed maximum, got {embed_amount}.')
                
                if embed_amount!=0:
                    data['embeds']=[embed.to_data() for embed in embed]
                    contains_content=True
            else:
                #check case, when it is not embed like
                converter=getattr(type(embed),'to_data')
                if converter is None:
                    raise TypeError(f'Expected embed like or `tuple`, `list` or `deque` of embed likes, got `{embed.__class__.__name__}`.')
                
                data['embeds']=[converter(embed)]
                contains_content=True
        
        if (content is not None) and content:
            data['content']=content
            contains_content=True
        
        if (allowed_mentions is not _spaceholder):
            data['allowed_mentions']=self._parse_allowed_mentions(allowed_mentions)
        
        if tts:
            data['tts']=True
        
        if (avatar_url is not None):
            data['avatar_url']=avatar_url
        
        if (name is not None):
            name_ln=len(name)
            if name_ln>32:
                raise ValueError(f'The length of the name can be between 1-32, got {name!r}.')
            if name_ln!=0:
                data['username']=name
        
        if file is None:
            to_send=data
        else:
            to_send=self._create_file_form(data,file)
            if to_send is None:
                to_send=data
            else:
                contains_content=True
        
        if not contains_content:
            return None
        
        data = await self.http.webhook_send(webhook,to_send,wait)
        
        if wait:
            channel=webhook.channel
            if channel is None:
                channel=ChannelText.precreate(int(data['channel_id']))
            return channel._create_new_message(data)
    
    async def emoji_get(self, guild, emoji_id):
        """
        Requests the emoji by it's id at the given guild. If the client's logging in is finished, then it should have
        it's every emoji loaded already.
        
        Parameters
        ----------
        guild : ``Guild``
            The guild, where the emoji is.
        emoji_id : `int`
            The id of the emoji.
        
        Returns
        -------
        emoji : ``Emoji``
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        data = await self.http.emoji_get(guild.id, emoji_id)
        return Emoji(data,guild)
    
    async def guild_sync_emojis(self,guild):
        """
        Syncs the given guild's emojis with the wrapper.
        
        Parameters
        ----------
        guild : ``Guild``
            The guild, what's emojis will be synced.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        data = await self.http.guild_emojis(guild.id)
        guild._sync_emojis(data)
    
    async def emoji_create(self, guild, name, image, roles=[], reason=None):
        """
        Creates an emoji at the givn guild.
        
        Parameters
        ----------
        guild : ``Guild``
            The guild, where the emoji will be created.
        name : `str`
            The emoji's name. It's length can be beween `2` and `32`.
        image : `bytes-like`
            The emoji's icon.
        roles : `list` of `Role` objects, Optional
            Whether the created emoji should be limited only to users with any of the specified roles.
        reason : `str`, Optional
            Will show up at the guild's audit logs.
        
        Raises
        ------
        ValueError
            If the `name`'s length is under `2`, or over `32`.
        ConnectionError
            No internet connection.
        DiscordException
        
        Notes
        -----
        Only some characters can be in the emoji's name, so every other character is filtered out.
        """
        image=image_to_base64(image)
        name=''.join(_VALID_NAME_CHARS.findall(name))
        
        name_ln=len(name)
        if name_ln<2 or name_ln>32:
            raise ValueError(f'The length of the emoji can be between 2-32, got {name!r}.')
        
        data={
            'name'      : name,
            'image'     : image,
            'role_ids'  : [role.id for role in roles]
                }
        
        await self.http.emoji_create(guild.id,data,reason)

    async def emoji_delete(self, emoji, reason=None):
        """
        Deletes th given emoji.
        
        Parameters
        ----------
        emoji : ``Emoji``
            The emoji to delete.
        reason : `str`, Optional
            Will show up at the respective guild's audit logs.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        guild = emoji.guild
        if guild is None:
            return
        
        await self.http.emoji_delete(guild.id,emoji.id,reason=reason)

    async def emoji_edit(self, emoji, name=None, roles=_spaceholder, reason=None):
        """
        Edits the given emoji.
        
        Parameters
        ----------
        emoji : ``Emoji``
            The emoji to edit.
        name : `str`, Optional.
            The emoji's new name.
        roles : `None` or `list` of ``Role`` objects, Optional
            The roles to what is the role limited. By passing it as `None`, or as an empty `list` you can remove the
            current ones.
        reason : `str`, Optional
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        ValueError
            If the `name`'s length is under `2`, or over `32`.
        ConnectionError
            No internet connection.
        DiscordException
        """
        guild = emoji.guild
        if guild is None:
            return
        
        data={}
        
        # name is required
        if (name is None):
            data['name']=emoji.name
        else:
            name=''.join(_VALID_NAME_CHARS.findall(name))
            name_ln=len(name)
            if name_ln<2 or name_ln>32:
                raise ValueError(f'The length of `name` can be between 2-32, got {name!r}.')
            
            data['name']=name
        
        # roles are not required
        if (roles is not _spaceholder):
            if (roles is not None):
                roles = [role.id for role in roles]
            
            data['roles'] = roles
        
        await self.http.emoji_edit(guild.id,emoji.id,data,reason)
        
    # Invite management
        
    async def vanity_invite(self, guild):
        """
        Returns the vanity invite of the givn guild.
        
        Parameters
        ----------
        guild : ``Guild``
            The guild, what's invite will be returned.
        
        Returns
        -------
        invite : `None` or ``Invite``
            The vanity invite of the `guild`, or `None` if it has no vanity invite.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        vanity_code = guild.vanity_code
        if vanity_code is None:
            return None
        
        data = await self.http.invite_get(vanity_code,{})
        return Invite._create_vanity(guild,data)

    async def vanity_edit(self, guild, code, reason=None):
        """
        Edits the given guild's vanity invite's code.
        
        Parameters
        ----------
        guild : ``Guild``
            Th guild, what's invite will be edited.
        code : `str`
            The new code of the guild's vanity invite.
        reason : `str`, Optional
            Shows up at the guild's audit logs.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        await self.http.vanity_edit(guild.id,{code:'code'},reason)
    
    async def invite_create(self, channel, max_age=0, max_uses=0, unique=True, temporary=False):
        """
        
        Parameters
        ----------
        channel : ``ChannelText``, ``ChannelVoice``, ``ChannelGroup`` or ``ChannelStore``
            The channel of the created invite.
        max_age : `int`, Optional
            After how much time (in seconds) will the invite expire. Defaults is never.
        max_uses : `int`, Optional
            How much times can the invite be used. Defaults to unlimited.
        unique : `bool`, Optional
            Whether the created invite should be unique. Defaults to `True`.
        temporary : `bool`, Optional
            Whether the invite should give only temporary membership. Defaults to `False`.
        
        Returns
        -------
        invite : ``Invite``
        
        Raises
        ------
        TypeError
            If the passed's channel is ``ChannelPrivate`` or ``ChannelCategory``.
        ConnectionError
            No internet connection.
        DiscordException
        """
        if channel.type in (1,4):
            raise TypeError(f'Cannot create invite from {channel.__class__.__name__}.')
        
        data = {
            'max_age'   : max_age,
            'max_uses'  : max_uses,
            'temporary' : temporary,
            'unique'    : unique,
                }
        
        data = await self.http.invite_create(channel.id,data)
        return Invite(data)

    # 'target_user_id' :
    #     DiscordException BAD REQUEST (400), code=50035: Invalid Form Body
    #     target_user_type.GUILD_INVITE_INVALID_TARGET_USER_TYPE('Invalid target user type')
    # 'target_user_type', as 0:
    #     DiscordException BAD REQUEST (400), code=50035: Invalid Form Body
    #     target_user_type.BASE_TYPE_CHOICES('Value must be one of (1,).')
    # 'target_user_type', as 1:
    #     DiscordException BAD REQUEST (400), code=50035: Invalid Form Body
    #     target_user_type.GUILD_INVITE_INVALID_TARGET_USER_TYPE('Invalid target user type')
    # 'target_user_id' and 'target_user_type' together:
    #    DiscordException BAD REQUEST (400), code=50035: Invalid Form Body
    #    target_user_id.GUILD_INVITE_INVALID_STREAMER('The specified user is currently not streaming in this channel')
    # 'target_user_id' and 'target_user_type' with not correct channel:
    #    DiscordException BAD REQUEST (400), code=50035: Invalid Form Body
    #    target_user_id.GUILD_INVITE_INVALID_STREAMER('The specified user is currently not streaming in this channel')
    
    async def stream_invite_create(self, guild, user, max_age=0, max_uses=0, unique=True, temporary=False):
        """
        Creates an STREAM invite at the given guild for the specific user. The user must be streaming at the guild,
        when the invite is created.
        
        Parameters
        ----------
        guild : ``Guild``
            The guild where the user streams
        user : ``Client`` or ``User``
            The streaming user.
        max_age : `int`, Optional
            After how much time (in seconds) will the invite expire. Defaults is never.
        max_uses : `int`, Optional
            How much times can the invite be used. Defaults to unlimited.
        unique : `bool`, Optional
            Whether the created invite should be unique. Defaults to `True`.
        temporary : `bool`, Optional
            Whether the invite should give only temporary membership. Defaults to `False`.
        
        Returns
        -------
        invite : ``Invite``
        
        Raises
        ------
        ValueError
            If the user is not streaming at the guild.
        ConnectionError
            No internet connection.
        DiscordException
        """
        user_id=user.id
        try:
            voice_state=guild.voice_states[user_id]
        except KeyError:
            raise ValueError('The user must stream at a voice channel of the guild!') from None
        
        if not voice_state.self_stream:
            raise ValueError('The user must stream at a voice channel of the guild!')
        
        data = {
            'max_age'           : max_age,
            'max_uses'          : max_uses,
            'temporary'         : temporary,
            'unique'            : unique,
            'target_user_id'    : user_id,
            'target_user_type'  : 1,
                }
        
        data = await self.http.invite_create(voice_state.channel.id,data)
        return Invite(data)
    
    #u cannot create invite from guild, but this chooses a prefered channel
    async def invite_create_pref(self, guild, *args, **kwargs):
        """
        Creates an invite to the guild's preferred channel.
        
        Parameters
        ----------
        guild . ``Guild``
            The guild to her the invite will be created to.
        *args : Arguments
            Additional arguments to describe the created invite.
        **kwargs : Keyword arguments
            Additional keyword arguments to describe the created invite.
        
        Other Parameters
        ----------------
        max_age : `int`, Optional
            After how much time (in seconds) will the invite expire. Defaults is never.
        max_uses : `int`, Optional
            How much times can the invite be used. Defaults to unlimited.
        unique : `bool`, Optional
            Whether the created invite should be unique. Defaults to `True`.
        temporary : `bool`, Optional
            Whether the invite should give only temporary membership. Defaults to `False`.
        
        Returns
        -------
        invite : ``Invite``
        
        Raises
        ------
        ValueError
            If the guild has no channel to create invite to.
        ConnectionError
            No internet connection.
        DiscordException
        """
        while True:
            if not guild.channels:
                raise ValueError('The guild has no channels (yet?), try waiting for dispatch or create a channel')

            channel=guild.system_channel
            if channel is not None:
                break
            
            channel=guild.embed_channel
            if channel is not None:
                break
            
            channel=guild.widget_channel
            if channel is not None:
                break
            
            for channel_type in (0,2):
                for channel in guild.channels:
                    if channel.type==4:
                        for channel in channel.channels:
                            if channel.type==channel_type:
                                break
                    if channel.type==channel_type:
                        break
                if channel.type==channel_type:
                    break
            else:
                raise ValueError('The guild has only category channels and cannot create invite from them!')
            break
        
        # Check permission, because it can save a lot of time >.>
        if not channel.cached_permissions_for(self).can_create_instant_invite:
            return None
        
        try:
            return (await self.invite_create(channel,*args,**kwargs))
        except DiscordException as err:
            if err.code in (
                    ERROR_CODES.unknown_channel, # the channel was deleted meanwhile
                    ERROR_CODES.missing_permissions, # permissons changed meanwhile
                        ):
                return None
            raise
    
    async def invite_get(self, invite_code, with_count=True):
        """
        Requests a partial invite with the given code.
        
        Parameters
        ----------
        invite_code : `str`
            The invites code.
        with_count : `bool`, Optional
            Whether the invite should contain the respective guild's user and online user count. Defaults to `True`.
        
        Returns
        -------
        invite : ``Invite``
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        data = await self.http.invite_get(invite_code,{'with_counts':with_count})
        return Invite(data)
    
    async def invite_update(self, invite, with_count=True):
        """
        Updates the given invite. Because this method uses the same endpoint as ``.invite_get``, no new information
        is received if `with_count` is passed as `False`.
        
        Parameters
        ----------
        invite : ``Invite``
            The invite to update.
        with_count : `bool`, Optional
            Whether the invite should contain the respective guild's user and online user count. Defaults to `True`.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        data = await self.http.invite_get(invite.code,{'with_counts':with_count})
        invite._update_no_return(data)

    async def invite_get_guild(self, guild):
        """
        Gets the invites of the given guild.
        
        Parameters
        ----------
        guild : ``Guild``
            The guild, what's invites will be requested.
        
        Returns
        -------
        invites : `list` of ``Invite`` objects
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        data=await self.http.invite_get_guild(guild.id)
        return [Invite(invite_data) for invite_data in data]

    async def invite_get_channel(self, channel):
        """
        Gets the invites of the given channel.
        
        Parameters
        ----------
        channel : ``ChannelBase`` instance
            The channel, what's invites will be requested.
        
        Returns
        -------
        invites : `list` of ``Invite`` objects
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        data = await self.http.invite_get_channel(channel.id)
        return [Invite(invite_data) for invite_data in data]

    async def invite_delete(self, invite, reason=None):
        """
        Deletes the given invite.
        
        Parameters
        ----------
        invite : ``Invite``
            The invite to delete.
        reason : `str`, Optional
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        await self.http.invite_delete(invite.code,reason)

    async def invite_delete_by_code(self, invite_code, reason=None):
        """
        Deletes the invite by it's code and returns it.
        
        Parameters
        ----------
        invite_code : ``str``
            The invite's code to delete.
        reason : `str`, Optional
            Shows up at the respective guild's audit logs.
        
        Returns
        -------
        invite : ``Invite``
            The deleted invite.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        data = await self.http.invite_delete(invite_code,reason)
        return Invite(data)
    
    # Role management

    async def role_edit(self, role, name=None, color=None, separated=None, mentionable=None, permissions=None,
            position=None, reason=None):
        """
        Edits the role with the given parameters.
        
        Parameters
        ----------
        role : ``Role``
            The role to edit.
        name : `str`, Optional
            The role's new name.
        color : ``Color`` or `int` Optional
            The role's new color.
        separated : `bool`, Optional
            Whether the users with this role should be shown up as separated from the others.
        mentionable : `bool`, Optional
            Whether the role should be mentionable.
        permissions : ``Permission`` or `int`, Optional
            The new permission value of the role.
        position : `int`, Optional
            The role's new position.
        reason : `str`, Optional
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        ValueError
            - If default role would be moved.
            - If any role would be moved to position `0`.
            - If `name`'s length is under `2` or over `32`.
        ConnectionError
            No internet connection.
        DiscordException
        """
        guild = role.guild
        if guild is None:
            return
        
        if (position is not None):
            await self.role_move(role,position,reason)
        
        data={}
        
        if (name is not None):
            name_ln=len(name)
            if name_ln<2 or name_ln>32:
                raise ValueError(f'The name of the role can be between 2-32, got {name!r}.')
            data['name']=name
        
        if (color is not None):
            data['color']=color
        
        if (separated is not None):
            data['hoist']=separated
        
        if (mentionable is not None):
            data['mentionable']=mentionable
        
        if (permissions is not None):
            data['permissions']=permissions
        
        if data:
            await self.http.role_edit(guild.id,role.id,data,reason)
    
    async def role_delete(self, role, reason=None):
        """
        Deletes the given role.
        
        Parameters
        ----------
        role : ``Role``
            The role to delete
        reason : `str`, Optional
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        guild = role.guild
        if guild is None:
            return
        
        await self.http.role_delete(guild.id,role.id,reason)
    
    async def role_create(self, guild, name=None, permissions=None, color=None, separated=None, mentionable=None,
            reason=None):
        """
        Creates a role at the given guild.
        
        Parameters
        ----------
        guild : ``Guild``
            The guild where the role will be created.
        name : `str`, Optional
            The created role's name.
        color : ``Color`` or `int` Optional
            The created role's color.
        separated : `bool`, Optional
            Whether the users with the created role should show up as separated from the others.
        mentionable : `bool`, Optional
            Whether the created role should be mentionable.
        permissions : ``Permission`` or `int`, Optional
            The permission value of the created role.
        reason : `str`, Optional
            Shows up at the guild's audit logs.
        
        Raises
        ------
        ValueError
            If `name`'s length is under `2` or over `32`.
        ConnectionError
            No internet connection.
        DiscordException
        """
        data={}
        if (name is not None):
            name_ln=len(name)
            if name_ln<2 or name_ln>32:
                raise ValueError(f'Role\'s name\'s length can be between 2-32, got {name!r}.')
            data['name']=name
        
        if (permissions is not None):
            data['permissions']=permissions
        
        if (color is not None):
            data['color']=color
        
        if (separated is not None):
            data['hoist']=separated
        
        if (mentionable is not None):
            data['mentionable']=mentionable
        
        data = await self.http.role_create(guild.id,data,reason)
        return Role(data,guild)
    
    async def role_move(self, role, position, reason=None):
        """
        Moves the given role.
        
        Parameters
        ----------
        role : ``Role``
            The role to move
        position : `int`
            The position to move the given role.
        reason : `str`, Optional
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        ValueError
            - If default role would be moved.
            - If any role would be moved to position `0`.
        ConnectionError
            No internet connection.
        DiscordException
        """
        guild=role.guild
        if guild is None:
            # The role is partial, we cannot move it, because there is nowhere to move it >.>
            return
        
        # Is there nothing to move?
        if role.position==position:
            return
        
        # Default role cannot be moved to position not 0
        if role.position==0:
            if position!=0:
                raise ValueError(f'Default role cannot be moved: `{role!r}`.')
        # non default role cannot be moved to position 0
        else:
            if position==0:
                raise ValueError(f'Role cannot be moved to position `0`.')
        
        data = guild.roles.change_on_switch(role, position, key=lambda role, pos:{'id':role.id,'position':pos})
        if not data:
            return
        
        await self.http.role_move(guild.id,data,reason)
    
    async def role_reorder(self, roles, reason=None):
        """
        Moves more roles at their guild to the specifie positions.
        
        Partial roles are ignored and if passed any, every role's position after it is reduced. If there are roles
        passed with different guilds, then `ValueError` will be raised. If there are roles passed with the same
        position, then their positions will be sorted out.
        
        Parameters
        ----------
        roles : (`dict` like or `iterable`) of `tuple` (``Role``, `int`) items
            A `dict` or any `iterable`, which contains `(Role, position)` items.
        reason : `str`, Optional
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        TypeError
            If `roles`'s format is not any of the expected ones.
        ValueError
            - If default role would be moved.
            - If any role would be moved to position `0`.
            - If roles from more guilds are passed.
        ConnectionError
            No internet connection.
        DiscordException
        """
        # Nothing to move, nice
        if not roles:
            return
        
        # Lets check `roles` structure
        roles_valid=[]
        
        # Is `roles` passed as dictlike?
        if hasattr(type(roles),'items'):
            for item in roles.items():
                if type(item) is not tuple:
                    raise TypeError(f'`roles` passed as dictlike, but when iterating it\'s `.items` returned not a `tuple`, got `{item!r}`')
                
                if len(item)!=2:
                    raise TypeError(f'`roles` passed as dictlike, but when iterating it\'s `.items` returned a `tuple`, but not with length `2`, got `{item!r}`')
                
                if (type(item[0]) is not Role) or (type(item[1]) is not int):
                    raise TypeError(f'Items should be `{Role.__name__}`, `int` pairs, but got `{item!r}`')
                
                roles_valid.append(item)
        
        # Is `roles` passed as other iterable
        elif hasattr(type(roles),'__iter__'):
            for item in roles:
                if type(item) is not tuple:
                    raise TypeError(f'`roles` passed as other iterable, but when iterating returned not a `tuple`, got `{item!r}`')
                
                if len(item)!=2:
                    raise TypeError(f'`roles` passed as other iterable, but when iterating returned a `tuple`, but not with length `2`, got `{item!r}`')
                
                if (type(item[0]) is not Role) or (type(item[1]) is not int):
                    raise TypeError(f'Items should be `{Role.__name__}`, `int` pairs, but got `{item!r}`')
                
                roles_valid.append(item)
        
        # `roles` has an unknown format
        else:
            raise TypeError(
                f'`roles` should have been passed as dictlike with (`{Role.__name__}, `int`) items, or as other '
                f'iterable with (`{Role.__name__}, `int`) elements, but got `{roles!r}`')
        
        # Check default and moving to default position
        index=0
        limit=len(roles_valid)
        while True:
            if index==limit:
                break
            
            role, position = roles_valid[index]
            # Default role cannot be moved
            if role.position==0:
                if position!=0:
                    raise ValueError(f'Default role cannot be moved: `{role!r}`.')
                
                # default and moving to default, lets delete it
                del roles_valid[index]
                limit = limit-1
                continue
                
            else:
                # Role cannot be moved to default position
                if position==0:
                    raise ValueError(f'Role cannot be moved to position `0`.')
            
            index = index+1
            continue
        
        if not limit:
            return
        
        # Check dupe roles
        roles=set()
        ln=0
        
        for role, position in roles_valid:
            roles.add(role)
            if len(roles)==ln:
                raise ValueError(f'{Role.__name__} `{role!r}` is duped.')
            
            ln=ln+1
            continue
        
        # Now that we have the roles, lets order them
        roles_valid.sort(key = lambda item : item[1])
        
        # We have all the roles sorted, but they can have dupe positions too
        index=0
        limit=len(roles_valid)
        last_position=0
        while True:
            role, position = roles_valid[index]
            
            if last_position!=position:
                last_position=position
                
                index=index+1
                if index==limit:
                    break
                
                continue
            
            # Oh no, we need to reorder
            # First role cannot get here, becuase it cannot have position 0.
            roles=[roles_valid[index-1][0],role]
            
            sub_index=index+1
            
            while True:
                if sub_index==limit:
                    break
                
                role, position = roles_valid[sub_index]
                if position!=last_position:
                    break
                
                roles.append(role)
                sub_index=sub_index+1
                continue
            
            # We have all the roles with the same target position.
            # Now we order them by their actual position.
            roles.sort()
            
            index=index-1
            sub_index=0
            sub_limit=len(roles)
            while True:
                real_index=sub_index+index
                role=roles[sub_index]
                real_position=last_position+sub_index
                roles_valid[real_index]=(role,real_position)
                
                sub_index=sub_index+1
                if sub_index==sub_limit:
                    break
                
                continue
            
            added_position=sub_limit-1
            
            real_index=sub_index+index
            while True:
                if real_index==limit:
                    break
                
                role, position = roles_valid[real_index]
                real_position=position+added_position
                roles_valid[real_index]=(role,real_position)
                
                real_index=real_index+1
                continue
            
            
            index=index+sub_limit
            last_position=last_position+added_position
            
            if index==limit:
                break
            
            continue
        
        # We have all the roles in order. Filter out partial roles.
        index=0
        push=0
        while True:
            role, position = roles_valid[index]
            
            if role.guild is None:
                push=push+1
                del roles_valid[index]
                limit=limit-1
            
            else:
                if push:
                    roles_valid[index]=(role,position-push)
                
                index=index+1
            
            if index==limit:
                break
            
            continue
        
        # Did we get down to 0 role?
        if limit==0:
            return
        
        # Check role guild
        guild = roles_valid[0][0].guild
        
        index=1
        while True:
            if index==limit:
                break
            
            guild_ = roles_valid[index][0].guild
            index=index+1
            
            if guild is guild_:
                continue
            
            raise ValueError(f'There were roles passed at least from two different guilds: `{guild!r}` and `{guild_!r}`.')
        
        # Lets cut out every other role from the guild's
        roles_leftover=set(guild.all_role.values())
        for item in roles_valid:
            role=item[0]
            roles_leftover.remove(role)
        
        roles_leftover=sorted(roles_leftover)
    
        target_order=[]
        
        index_valid=0
        index_leftover=0
        limit_valid=len(roles_valid)
        limit_leftover=len(roles_leftover)
        position_target=0
        
        while True:
            if index_valid==limit_valid:
                while True:
                    if index_leftover==limit_leftover:
                        break
                    
                    role = roles_leftover[index_leftover]
                    index_leftover = index_leftover+1
                    target_order.append(role)
                    continue
                
                break
            
            if index_leftover==limit_leftover:
                while True:
                    if index_valid==limit_valid:
                        break
                    
                    role = roles_valid[index_valid][0]
                    index_valid = index_valid+1
                    target_order.append(role)
                    continue
                
                
                break
            
            role, position = roles_valid[index_valid]
            if position==position_target:
                position_target = position_target+1
                index_valid = index_valid+1
                target_order.append(role)
                continue
            
            role = roles_leftover[index_leftover]
            position_target = position_target+1
            index_leftover = index_leftover+1
            target_order.append(role)
            continue
        
        data = []
        
        for index, role in enumerate(target_order):
            position=role.position
            if index==position:
                continue
            
            data.append({'id':role.id,'position':index})
            continue
        
        # Nothing to move
        if not data:
            return
        
        await self.http.role_move(guild.id,data,reason)
    
    # Relationship related
    #hooman only
    async def relationship_delete(self, relationship):
        """
        Deletes the given relationship.
        
        Parameters
        ----------
        relationship : ``Relationship``
            The relationship to delete.

        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        await self.http.relationship_delete(relationship.user.id)
    
    #hooman only
    async def relationship_create(self, user, relationship_type=None):
        """
        Creates a relationship with the given user.
        
        Parameters
        ----------
        user : ``Client`` or ``User``
            The user with who the relationsthip will be created.
        relationship_type : ``RelationshipType``, Optional
            The type of the relationship.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        data={}
        if (relationship_type is not None):
            data['type']=relationship_type.value
        await self.http.relationship_create(user.id,data)

    #hooman only
    async def relationship_friend_request(self, user):
        """
        Sends a friend request to the given user.
        
        Parameters
        ----------
        user : ``Client`` or ``User``
            The user, who will receive the friend request.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        data = {
            'username'      : user.name,
            'discriminator' : str(user.discriminator)
                }
        await self.http.relationship_friend_request(data)
    
    #bot only!
    async def update_application_info(self):
        """
        Updates the client's application's info.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        
        Notes
        -----
        Meanwhile the clients logs in this method is called.
        """
        if self.is_bot:
            data = await self.http.client_application_info()
            self.application(data)
    
    async def client_gateway(self):
        """
        Requests the gateway information for the client.
        
        Only `1` request can be done at a time and every other will yield the result of first started one.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        
        Raises
        ------
        ConnectionError
            No internet connection or if the request raised any ``DiscordException``.
        InvalidToken
            When the client's token is invalid.
        DiscordException
        """
        if self._gateway_requesting:
            gateway_waiter = self._gateway_waiter
            if gateway_waiter is None:
                gateway_waiter = self._gateway_waiter = Future(KOKORO)
            
            return await gateway_waiter
        
        self._gateway_requesting = True
        
        try:
            http = self.http
            if self.is_bot:
                func = http.client_gateway_bot
            else:
                func = http.client_gateway_hooman
            
            while True:
                try:
                    data = await func()
                except DiscordException as err:
                    status = err.status
                    if status == 401:
                        await self.disconnect()
                        raise InvalidToken() from err
                    
                    if status >= 500:
                        sleep(2.5, KOKORO)
                        continue
                    
                    raise
                
                break
            
            self._gateway_max_concurrency = data['session_start_limit'].get('max_concurrency', 1)
        except BaseException as err:
            self._gateway_requesting = False
            gateway_waiter = self._gateway_waiter
            if (gateway_waiter is not None):
                self._gateway_waiter = None
                gateway_waiter.set_exception_if_pending(err)
            
            raise
        
        self._gateway_requesting = False
        gateway_waiter = self._gateway_waiter
        if (gateway_waiter is not None):
            self._gateway_waiter = None
            gateway_waiter.set_result_if_pending(data)
        
        return data
    
    async def client_gateway_url(self):
        """
        Requests the client's gateway url. To avoid unreasoned requests when sharding, if this request was done at the
        last `60` seconds then returns the last generated url.
        
        Raises
        ------
        ConnectionError
            No internet connection or if the request raised any ``DiscordException``.
        InvalidToken
            When the client's token is invalid.
        DiscordException
        
        Returns
        -------
        gateway_url : `str`
            The url to what the gateways' webscoket will be connected.
        """
        if self._gateway_time > (monotonic()+60.0):
            return self._gateway_url
        
        data = await self.client_gateway()
        self._gateway_url = gateway_url = data['url']+'?encoding=json&v=6&compress=zlib-stream'
        self._gateway_time = monotonic()
        
        return gateway_url
    
    async def client_gateway_reshard(self, force=False):
        """
        Reshards the client. And also updates it's gatewas url as a sidenote.
        
        > Should be called only if every shard is down.
        
        Parameters
        ----------
        force : `bool`
            Whether the the client should reshard to lower amount of shards if needed.
        
        Raises
        ------
        ConnectionError
            No internet connection or if the request raised any ``DiscordException``.
        InvalidToken
            When the client's token is invalid.
        DiscordException
        """
        data = await self.client_gateway()
        self._gateway_url = data['url']+'?encoding=json&v=6&compress=zlib-stream'
        self._gateway_time = monotonic()
        
        old_shard_count = self.shard_count
        if old_shard_count == 0:
            old_shard_count = 1
        
        new_shard_count = data['shards']
        
        # Do we have more shards already?
        if (not force) and (old_shard_count >= new_shard_count):
            return
        
        if new_shard_count == 1:
            new_shard_count = 0
        
        self.shard_count = new_shard_count
        
        gateway = self.gateway
        if type(gateway) is DiscordGateway:
            if new_shard_count:
                self.gateway = DiscordGatewaySharder(self)
        else:
            if new_shard_count:
                gateway.reshard()
            else:
                self.gateway = DiscordGateway(self)
    
    #user account only
    async def hypesquad_house_change(self, house):
        """
        Changes the client's hypesquad house.
        
        Parameters
        ----------
        house : ``HypesquadHouse``

        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        await self.http.hypesquad_house_change({'house_id':house.value})
    
    #user account only
    async def hypesquad_house_leave(self):
        """
        Leaves the client from it's current hypesquad house.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
        """
        await self.http.hypesquad_house_leave()
    
    def start(self):
        """
        Starts the clients's connecting to Discord. If the client is already running, raises `RuntimeError`.
        
        The return of the method depends on the thread, from which it was called from.
        
        Returns
        -------
        task : `bool`, `Task` or `TaskAsyncWrapper`
            - If the method was called from the client's thread (KOKORO), then returns a `Task`. The task will return
                `True`, if connecting was successful.
            - If the method was called from an `EventThread`, but not from the client's, then returns a
                `TaskAsyncWrapper`. The task will return `True`, if connecting was successful.
            - If the method was called from any other thread, then waits for the connecter task to finish and returns
                `True`, if it was successful.
        
        Raises
        ------
        RuntimeError
            If the client is already running.
        """
        if self.running:
            raise RuntimeError(f'{self!r} is already running!')
        
        task = Task(self.connect(),KOKORO)
        
        thread = current_thread()
        if thread is KOKORO:
            return task
        
        if isinstance(thread,EventThread):
            # Asyncwrap wakes up KOKORO
            return task.asyncwrap(thread)
        
        KOKORO.wakeup()
        return task.syncwrap().wait()
    
    def stop(self):
        """
        Starts disconneting the client.
        
        The return of the method depends on the thread, from which it was called from.
        
        Returns
        -------
        task : `None`, `Task` or `TaskAsyncWrapper`
            - If the method was called from the client's thread (KOKORO), then returns a `Task`.
            - If the method was called from an `EventThread`, but not from the client's, then returns a
                `TaskAsyncWrapper`.
            - If the method was called from any other thread, returns `None` when disconnecting finished.
        """
        task = Task(self.disconnect(),KOKORO)
        
        thread = current_thread()
        if thread is KOKORO:
            return task
        
        if isinstance(thread,EventThread):
            # Asyncwrap wakes up KOKORO
            return task.asyncwrap(thread)
        
        KOKORO.wakeup()
        task.syncwrap().wait()
    
    async def connect(self):
        """
        Starts connecting the client to Discord, fills up the undefined events and creates the task, what will keep
        receiving the data from Discord (``._connect``).
        
        If you want to start the connecting process consider using the toplevel ``.start`` or ``start_clients`` instead.
        
        Returns
        -------
        success : `bool`
            Whether the client could be started.
        
        Raises
        ------
        RuntimeError
            If the client is already running.
        """
        if self.running:
            raise RuntimeError(f'{self!r} is already running!')
        
        try:
            data = await self.client_login_static()
        except BaseException as err:
            if isinstance(err, ConnectionError) and err.args[0]=='Invalid adress':
                after=(
                    'Connection failed, could not connect to Discord.\n Please check your internet connection / has '
                    'Python rights to use it?\n'
                        )
            else:
                after=None
            
            before = [
                'Exception occured at calling ',
                self.__class__.__name__,
                '.connect\n',
                    ]
            
            await KOKORO.render_exc_async(err,before,after)
            return False
        
        if type(data) is not dict:
            sys.stderr.write(''.join([
                'Connection failed, could not connect to Discord.\n'
                'Received invalid data:\n',
                repr(data),'\n']))
            return False
        
        self._init_on_ready(data)
        await self.client_gateway_reshard()
        await self.gateway.start()
        
        if self.is_bot:
            task = Task(self.update_application_info(), KOKORO)
            if __debug__:
                task.__silence__()
        
        # Check it twice, because meanwhile logging on, connect calls are not limited
        if self.running:
            raise RuntimeError(f'{self!r} is already running!')
        
        self.running=True
        PARSER_DEFAULTS.register(self)
        Task(self._connect(), KOKORO)
        return True
    
    async def _connect(self):
        """
        Connects the client's gateway(s) to Discord and reconnects them if needed.
        """
        try:
            while True:
                try:
                    await self.gateway.run()
                except (GeneratorExit, CancelledError) as err:
                    # For now only here. These errors occured randomly for me since I made the wrapper, only once-once,
                    # and it was not the wrapper causing them, so it is time to say STOP.
                    # I also know `GeneratorExit` will show up as RuntimeError, but it is already a RuntimeError.
                    self._freeze_voice()
                    try:
                        await KOKORO.render_exc_async(err,[
                            'Ignoring unexpected outer Task or coroutine cancellation at ',
                            repr(self),
                            '._connect:\n',
                                ],)
                    except (GeneratorExit, CancelledError) as err:
                        sys.stderr.write(
                            f'Ignoring unexpected outer Task or coroutine cancellation at {self!r}._connect as '
                            f'{err!r} meanwhile rendering an exception for the same reason.\n The client will '
                            f'reconnect.\n')
                    continue
                
                except DiscordGatewayException as err:
                    if err.code in DiscordGatewayException.RESHARD_ERROR_CODES:
                        sys.stderr.write(
                            f'{err.__class__.__name__} occured, at {self!r}._connect:\n'
                            f'{err!r}\n'
                            f'The client will reshard itself and reconnect.\n'
                                )
                        
                        await self.client_gateway_reshard(force=True)
                        continue
                    
                    raise
                
                else:
                    if not self.running:
                        break
                    
                    self._freeze_voice()
                    while True:
                        try:
                            await sleep(5.0, KOKORO)
                            try:
                                # We are down, why not reshard instantly?
                                await self.client_gateway_reshard()
                            except ConnectionError:
                                continue
                            else:
                                break
                        except (GeneratorExit, CancelledError) as err:
                            try:
                                await KOKORO.render_exc_async(err,[
                                    'Ignoring unexpected outer Task or coroutine cancellation at ',
                                    repr(self),
                                    '._connect:\n',
                                        ],)
                            except (GeneratorExit, CancelledError) as err:
                                sys.stderr.write(
                                    f'Ignoring unexpected outer Task or coroutine cancellation at {self!r}._connect as '
                                    f'{err!r} meanwhile rendering an exception for the same reason.\n The client will '
                                    f'reconnect.\n')
                            continue
                    continue
        except BaseException as err:
            if isinstance(err, InvalidToken) or \
                    (isinstance(err, DiscordGatewayException) and err.code in DiscordGatewayException.INTENT_ERROR_CODES):
                sys.stderr.write(
                    f'{err.__class__.__name__} occured, at {self!r}._connect:\n'
                    f'{err!r}\n'
                        )
            else:
                await KOKORO.render_exc_async(err,[
                    'Unexpected exception occured at ',
                    repr(self),
                    '._connect\n',
                        ],
                    'If you can reproduce this bug, Please send me a message or open an issue whith your code, and with '
                    'every detail how to reproduce it.\n'
                    'Thanks!\n')
        
        finally:
            try:
                await self.gateway.close()
            finally:
                PARSER_DEFAULTS.unregister(self)
                self.running = False
                
                if not self.guild_profiles:
                    return
                
                to_remove=[]
                for guild in self.guild_profiles:
                    guild._delete(self)
                    if guild.clients:
                        continue
                    to_remove.append(guild)
                
                if to_remove:
                    for guild in to_remove:
                        del self.guild_profiles[guild]
                
                #needs to delete the references for cleanup
                guild=None
                to_remove=None
    
    async def join_voice_channel(self, channel):
        """
        Joins a voice client to the channel. If there is an already existing voice client at the respective guild,
        moves it.
        
        If not every library is installed, raises `RuntimeError`, or if the voice client fails to connect raises
        `TimeoutError`.
        
        Parameters
        ----------
        channel : ``ChannelVoice``
            The channel to join to.
        
        Returns
        -------
        voice_client : ``VoiceClient``
        
        Raises
        ------
        RuntimeError
            If not every library is installed to join voice.
        TimeoutError
            If voice client fails to connect the given channel.
        """
        guild = channel.guild
        if guild is None:
            raise TimeoutError(f'Cannot join channel without guild: {channel!r}')
        
        try:
            voice_client=self.voice_clients[guild.id]
        except KeyError:
            voice_client = await VoiceClient(self,channel)
        else:
            if voice_client.channel is not channel:
                gateway=self._gateway_for(guild)
                await gateway._change_voice_state(guild.id,channel.id)
        
        return voice_client

    async def _delay_ready(self):
        """
        Delays the client's "ready" till it receives all of it guild's data. If caching is allowed (so by default),
        then it waits additional time till it requests all the members of it's guilds.
        """
        ready_state=self.ready_state
        try:
            if self.is_bot:
                await ready_state
            
            if ready_state.guilds and CACHE_USER:
                await self._request_members2(ready_state.guilds)
                
            self.ready_state=None
                
        except CancelledError:
            pass
        else:
            Task(_with_error(self,self.events.ready(self)), KOKORO)
    
    async def _request_members2(self, guilds):
        """
        Requests the members of the client's guilds. Called after the client is started up and user aching is
        enabled (so by default).
        
        Parameters
        ----------
        guilds : `list` of ``Guild`` objects
            The guilds, which users should be requested.
        """
        event_handler = self.events.guild_user_chunk
        
        try:
            waiter = event_handler.waiters.pop('0000000000000000')
        except KeyError:
            pass
        else:
            waiter.cancel()
        
        event_handler.waiters['0000000000000000'] = waiter = MassUserChunker(len(guilds))
        
        shard_count = self.shard_count
        if shard_count:
            guilds_by_shards=[[] for x in range(shard_count)]
            for guild in guilds:
                shard_index=(guild.id>>22)%shard_count
                guilds_by_shards[shard_index].append(guild)
            
            tasks = []
            gateways = self.gateway.gateways
            for index in range(shard_count):
                task = Task(self._request_members_loop(gateways[index], guilds_by_shards[index]), KOKORO)
                tasks.append(task)
            
            done, pending = await WaitTillExc(tasks, KOKORO)
            for task in pending:
                task.cancel()
            
            for task in done:
                task.result()
            
        else:
            await self._request_members_loop(self.gateway, guilds)

        
        try:
            await waiter
        except CancelledError:
            try:
                del event_handler.waiters['0000000000000000']
            except KeyError:
                pass
    
    @staticmethod
    async def _request_members_loop(gateway, guilds):
        sub_data = {
            'guild_id'  : 0,
            'query'     : '',
            'limit'     : 0,
            'presences' : CACHE_PRESENCE,
            'nonce'     : '0000000000000000',
                }
        
        data = {
            'op'    : DiscordGateway.REQUEST_MEMBERS,
            'd'     : sub_data
                }
        
        for guild in guilds:
            sub_data['guild_id'] = guild.id
            await gateway.send_as_json(data)
            await sleep(0.6, KOKORO)
    
    async def _request_members(self, guild):
        """
        Requests the members of the given guild. Called when the client joins a guild and user caching is enabled
        (so by default).
        
        Parameters
        ----------
        guild : ``Guild``
            The guild, what's members will be requested.
        """
        event_handler = self.events.guild_user_chunk
        
        self._user_chunker_nonce = nonce = self._user_chunker_nonce+1
        nonce = nonce.__format__('0>16x')
        
        event_handler.waiters[nonce] = waiter = MassUserChunker(1)
        
        data = {
            'op'            : DiscordGateway.REQUEST_MEMBERS,
            'd' : {
                'guild_id'  : guild.id,
                'query'     : '',
                'limit'     : 0,
                'presences' : CACHE_PRESENCE,
                'nonce'     : nonce
                    },
                }
        
        gateway=self._gateway_for(guild)
        await gateway.send_as_json(data)
        
        try:
            await waiter
        except CancelledError:
            try:
                del event_handler.waiters[nonce]
            except KeyError:
                pass
    
    async def request_members(self, guild, name, limit=1):
        """
        Requests the members of the given guild by their name.
        
        This method uses the client's gateway to request the users. If any of the parameters do not match their
        expected value or if timeout occures, returns an empty list instead of raising.
        
        Parameters
        ----------
        guild : ``Guild``
            The guild, what's members will be requested.
        name : `str`
            The received user's name or nick should start with this string.
        limit : `int`
            The amount of users to received. Limited to `100`.
        
        Returns
        -------
        users : `list` of (``Client`` or ``User``) objects
        """
        #do we really need these checks?
        if limit > 100:
            limit = 100
        elif limit < 1:
            return []
        
        if not 0<len(name)<33:
            return []
        
        event_handler = self.events.guild_user_chunk
        
        self._user_chunker_nonce = nonce = self._user_chunker_nonce+1
        nonce = nonce.__format__('0>16x')
        
        event_handler.waiters[nonce] = waiter = SingleUserChunker()
        
        data = {
            'op'            : DiscordGateway.REQUEST_MEMBERS,
            'd' : {
                'guild_id'  : guild.id,
                'query'     : name,
                'limit'     : limit,
                'presences' : CACHE_PRESENCE,
                'nonce'     : nonce,
                    },
                }
        
        gateway=self._gateway_for(guild)
        await gateway.send_as_json(data)
        
        try:
            return await waiter
        except CancelledError:
            try:
                del event_handler.waiters[nonce]
            except KeyError:
                pass
            
            return []
    
    async def disconnect(self):
        """
        Disconnects the client and closes it's wewbsocket(s). Till the client goes offline, it might take even over
        than `1` minute. Because bot accounts can not logout, so they need to wait for timeout.
        """
        if not self.running:
            return
        
        self.running=False
        shard_count=self.shard_count
        if shard_count:
            for gateway in self.gateway.gateways:
                gateway.kokoro.cancel()
            
            for voice_client in self.voice_clients.values():
                await voice_client.disconnect()
            
            if (not self.is_bot):
                await self.http.client_logout()
            
            for gateway in self.gateway.gateways:
                websocket=gateway.websocket
                if (websocket is not None) and websocket.open:
                    await gateway.close()
        else:
            self.gateway.kokoro.cancel()
            
            for voice_client in self.voice_clients.values():
                await voice_client.disconnect()
            
            if (not self.is_bot):
                await self.http.client_logout()
            
            websocket=self.gateway.websocket
            if (websocket is not None) and websocket.open:
                await self.gateway.close()
    
    def voice_client_for(self, message):
        """
        Returns the voice client for the given message's guild if it has any.
        
        Parameters
        ----------
        message : ``Message``
            The message what's voice client will be looked up.
        
        Returns
        -------
        voice_client : `None` or ``VoiceClient``
            The voice client if applicable.
        """
        guild = message.channel.guild
        if guild is None:
            return
        
        return self.voice_clients.get(guild.id,None)
    
    def get_guild(self, name, default=None):
        """
        Tries to find a guild by it's name. If there is no guild with the given name, then returns the passed
        default value.
        
        Parameters
        ----------
        name : `str`
            The guild's name to search.
        default : `Any`, Optional
            The default value, what will be returned if the guild was not found.
        
        Returns
        -------
        guild : ``Guild`` or `default`
        """
        if 1<len(name)<101:
            for guild in self.guild_profiles.keys():
                if guild.name==name:
                    return guild
        
        return default
    
    get_ratelimits_of = methodize(RatelimitProxy)
    
    @property
    def owner(self):
        """
        Returns the client's owner if applicable.
        
        If the client is a user account, or if it's ``.update_application_info`` was not called yet, then returns
        ``ZEROUSER``. If the client is owned by a ``Team``, then returns the team's owner.
        
        Returns
        -------
        owner : ``User``, ``Client``
        """
        application_owner=self.application.owner
        if type(application_owner) is Team:
            return application_owner.owner
        return application_owner
    
    def is_owner(self, user):
        """
        Returns whether the passed user is one of the client's owners.
        
        Parameters
        ----------
        user : ``Client`` or ``User`` object
            The user who will be checked.
        
        Returns
        -------
        is_owner : `bool`
        """
        application_owner=self.application.owner
        if type(application_owner) is Team:
            if user in application_owner.accepted:
                return True
        else:
            if application_owner == user:
                return True
        
        additional_owner_ids = self._additional_owner_ids
        if (additional_owner_ids is not None) and (user.id in additional_owner_ids):
            return True
        
        return False
    
    def add_additional_owners(self, *users):
        """
        Adds additional users to be passed at the ``.is_owner`` check.
        
        Parameters
        ----------
        *users : `int` or ``UserBase`` instances
            The `.id` of the a user or the user itself to be added.
        
        Raises
        ------
        TypeError
            A user was passed with invalid type.
        """
        limit = len(users)
        if limit == 0:
            return
        
        index = 0
        while True:
            user = users[index]
            index +=1
            if not isinstance(user,(int,UserBase)):
                raise TypeError(f'User {index} was not passed neither as `int` or as `{UserBase.__name__}` instance, '
                    f'got {user.__class__.__name__}.')
            
            if index==limit:
                break
        
        additional_owner_ids = self._additional_owner_ids
        if additional_owner_ids is None:
            additional_owner_ids = self._additional_owner_ids = set()
        
        for user in users:
            if type(user) is int:
                pass
            elif isinstance(user, int):
                user = int(user)
            else:
                user = user.id
            
            additional_owner_ids.add(user)
    
    def remove_additional_owners(self, *users):
        """
        Removes additonal owners added by the ``.add_additional_owners`` method.
        
        Parameters
        ----------
        *users : `int` or ``UserBase`` instances
            The `.id` of the a user or the user itself to be removed.
        
        Raises
        ------
        TypeError
            A user was passed with invalid type.
        """
        limit = len(users)
        if limit == 0:
            return
        
        index = 0
        while True:
            user = users[index]
            index +=1
            if not isinstance(user,(int,UserBase)):
                raise TypeError(f'User {index} was not passed neither as `int` or as `{UserBase.__name__}` instance, '
                    f'got {user.__class__.__name__}.')
            
            if index==limit:
                break
        
        additional_owner_ids = self._additional_owner_ids
        if additional_owner_ids is None:
            additional_owner_ids = self._additional_owner_ids = set()
        
        for user in users:
            if type(user) is int:
                pass
            elif isinstance(user, int):
                user = int(user)
            else:
                user = user.id
            
            try:
                additional_owner_ids.remove(user)
            except KeyError:
                pass
    
    @property
    def owners(self):
        """
        Returns the owners of the client.
        
        Returns
        -------
        owners : `set` of (``Client`` or ``User``)
        """
        owners = set()
        
        application_owner = self.application.owner
        if type(application_owner) is Team:
            owners.update(application_owner.accepted)
        else:
            owners.add(application_owner)
        
        additional_owner_ids = self._additional_owner_ids
        if (additional_owner_ids is not None):
            for user_id in additional_owner_ids:
                user = PartialUser(user_id)
                owners.add(user)
        
        return owners
    
    def _update(self, data):
        """
        Updates the client and returns it's old attribtes in a `dict` with `attribute-name`, `old-value` relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `Any`) items
            All item in the returned dict is optional.
        
        Returned Data Structure
        -----------------------
        +-----------------------+-------------------+
        | Keys                  | Values            |
        +=======================+===================+
        | avatar                | ``Icon``          |
        +-----------------------+-------------------+
        | discriminator         | `int`             |
        +-----------------------+-------------------+
        | email                 | `str`             |
        +-----------------------+-------------------+
        | flags                 | ``UserFlag``      |
        +-----------------------+-------------------+
        | locale                | `str              |
        +-----------------------+-------------------+
        | mfa                   | `bool`            |
        +-----------------------+-------------------+
        | name                  | `str              |
        +-----------------------+-------------------+
        | premium_type          | ``PremiumType``   |
        +-----------------------+-------------------+
        | verified              | `bool`            |
        +-----------------------+-------------------+
        """
        old_attributes = {}
            
        name=data['username']
        if self.name!=name:
            old_attributes['name']=self.name
            self.name=name
                
        discriminator=int(data['discriminator'])
        if self.discriminator!=discriminator:
            old_attributes['discriminator']=self.discriminator
            self.discriminator=discriminator

        self._update_avatar(data, old_attributes)
        
        email=data.get('email','')
        if self.email!=email:
            old_attributes['email']=self.email
            self.email=email
        
        premium_type=PremiumType.INSTANCES[data.get('premium_type',0)]
        if self.premium_type is not premium_type:
            old_attributes['premium_type']=premium_type
            self.premium_type=premium_type
        
        system=data.get('system',False)
        if self.system!=system:
            old_attributes['system']=self.system
            self.system=system
        
        verified=data.get('verified',False)
        if self.verified!=verified:
            old_attributes['verified']=self.verified
            self.verified=verified
        
        mfa=data.get('mfa_enabled',False)
        if self.mfa!=mfa:
            old_attributes['mfa']=self.mfa
            self.mfa=mfa

        flags=UserFlag(data.get('flags',0))
        if self.flags!=flags:
            old_attributes['flags']=self.flags
            self.flags=flags

        locale=parse_locale(data)
        if self.locale!=locale:
            old_attributes['locale']=self.locale
            self.locale=locale

        return old_attributes

    def _update_no_return(self,data):
        """
        Updates the client by overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        """
        self.name=data['username']
        
        self.discriminator=int(data['discriminator'])
        
        self._set_avatar(data)
        
        self.system=data.get('system',False)
        
        self.verified=data.get('verified',False)
        
        self.email=data.get('email','')

        self.premium_type=PremiumType.INSTANCES[data.get('premium_type',0)]
        
        self.mfa=data.get('mfa_enabled',False)

        self.flags=UserFlag(data.get('flags',0))

        self.locale=parse_locale(data)
    
    def _update_profile_only(self, data, guild):
        """
        Used only when user caching is disabled. Updates the client's guild profile for the given guild and returns
        the changed old attributes in a `dict` with `attribute-name`, `old-value` relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        guild : ``Guild``
            The respective guild of the guild profile.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `Any`) items
            All item in the returned dict is optional.
        
        Returned Data Structure
        -----------------------
        +---------------+-----------------------+
        | Keys          | Values                |
        +===============+=======================+
        | nick          | `str` / `None`        |
        +---------------+-----------------------+
        | roles         | `list` of ``Role``    |
        +---------------+-----------------------+
        | boosts_since  | `datetime` / `None`   |
        +---------------+-----------------------+
        """
        try:
            profile=self.guild_profiles[guild]
        except KeyError:
            self.guild_profiles[guild]=GuildProfile(data,guild)
            guild.users[self.id]=self
            return {}
        return profile._update(data,guild)
    
    def _update_profile_only_no_return(self, data, guild):
        """
        Used only when user caching is disabled. Updates the client's guild profile for the given guild.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        guild : ``Guild``
            The respective guild of the guild profile.
        """
        try:
            profile=self.guild_profiles[guild]
        except KeyError:
            self.guild_profiles[guild]=GuildProfile(data,guild)
            guild.users[self.id]=self
        else:
            profile._update_no_return(data,guild)
    
    @property
    def friends(self):
        """
        Returns the client's friends.
        
        Returns
        -------
        relationships : `list` of ``Relationship`` objects
        """
        type_=RelationshipType.friend
        return [rs for rs in self.relationships.values() if rs.type is type_]

    @property
    def blocked(self):
        """
        Returns the client's blocked relationships.
        
        Returns
        -------
        relationships : `list` of ``Relationship`` objects
        """
        type_=RelationshipType.blocked
        return [rs for rs in self.relationships.values() if rs.type is type_]

    @property
    def received_requests(self):
        """
        Returns the received friend requests of the client.
        
        Returns
        -------
        relationships : `list` of ``Relationship`` objects
        """
        type_=RelationshipType.pending_incoiming
        return [rs for rs in self.relationships.values() if rs.type is type_]

    @property
    def sent_requests(self):
        """
        Returns the sent friend requests of the client.
        
        Returns
        -------
        relationships : `list` of ``Relationship`` objects
        """
        type_=RelationshipType.pending_outgoing
        return [rs for rs in self.relationships.values() if rs.type is type_]
    
    def _freeze_voice(self):
        """
        Freezes the client's voice clients.
        """
        for voice_client in self.voice_clients.values():
            voice_client._freeze()
    
    def _freeze_voice_for(self, gateway):
        """
        Freezes the client's voice clients for the specific gateway.
        
        Parameters
        ----------
        gateway  : ``DiscordGateway``
            The gateway, what's voice clients will be freezed.
        """
        voice_clients=self.voice_clients
        
        shard_count=self.shard_count
        if shard_count:
            target_shard_id=gateway.shard_id
            for voice_client in voice_clients.values():
                guild = voice_client.channel.guild
                if guild is None:
                    Task(voice_client.disconnect(),KOKORO)
                    continue
                
                if (guild.id>>22)%shard_count==target_shard_id:
                    voice_client._freeze()
            return
        
        for voice_client in voice_clients.values():
            voice_client._freeze()
    
    def _unfreeze_voice_for(self, gateway):
        """
        Unfreezes the client's voice clients for the specific gateway.
        
        Parameters
        ----------
        gateway  : ``DiscordGateway``
            The gateway, what's voice clients will be unfreezed.
        """
        voice_clients=self.voice_clients
        if not voice_clients:
            return
        
        shard_count=self.shard_count
        if shard_count:
            target_shard_id=gateway.shard_id
            for voice_client in voice_clients.values():
                guild=voice_client.channel.guild
                if guild is None:
                    Task(voice_client.disconnect(),KOKORO)
                    continue
                
                if (guild.id>>22)%shard_count==target_shard_id:
                    voice_client._unfreeze()
            return
        
        for voice_client in voice_clients.values():
            voice_client._unfreeze()
    
    def _gateway_for(self, guild):
        """
        Returns the coresponding gateway of the client to the passed guild.
        
        Parameters
        ----------
        guild : ``Guild`` or `None`
            The guild what's gateway will be returned.
        
        Returns
        -------
        gateway : ``DiscordGateway``
        """
        shard_count=self.shard_count
        if shard_count:
            if guild is None:
                return self.gateway.gateways[0]
            
            guild_id=guild.id
            shard_index=(guild_id>>22)%shard_count
            
            return self.gateway.gateways[shard_index]
        
        return self.gateway

class Typer(object):
    """
    A typer what will keep sending typing events to the given channel with the client. Can be used as a context
    manager.
    
    After entered as a context manager sends a typing event each `8` seconds to the given channel.
    
    Attributes
    ----------
    client : ``Client``
        The client what will send the typing events.
    channel : ``ChannelTextBase`` instance
        The channel where the typing events will be sent.
    timeout : `float`
        The leftover timeout till the typer will send typings. Is reduced every time, when the typer sent a typing
        event. If goes under `0.0` the typer stops sending more events.
    waiter : `Future` or `None`
        The sleeping future what will wakeup ``.run``.
    """
    __slots__=('channel', 'client', 'timeout', 'waiter',)
    def __init__(self, client, channel, timeout=300.):
        """
        Parameters
        ----------
        client : ``Client``
            The client what will send the typing events.
        channel : ``ChannelTextBase`` instance
            The channel where the typing events will be sent.
        timeout : `float`, Optional
            The maximal amount of time till the client will keep sending typing events. Defaults to `300.0`.
        """
        self.client = client
        self.channel= channel
        self.waiter = None
        self.timeout= timeout
    
    def __enter__(self):
        """Enters the typer's context block by ensuring it's ``.run`` method."""
        Task(self.run(),self.client.loop)
        return self
    
    async def run(self):
        """
        The coroutine what keeps sending the typing requests.
        """
        # js client's typing is 8s
        loop=self.client.loop
        while self.timeout>0.:
            self.timeout-=8.
            self.waiter = waiter = sleep(8.,loop)
            await self.client.http.typing(self.channel.id)
            await waiter
        
        self.waiter=None
    
    def cancel(self):
        """
        If the context manager is still active, cancels it.
        """
        self.timeout=0.
        waiter = self.waiter
        if (waiter is not None):
            self.waiter = None
            waiter.cancel()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exits the typer's context block by cancelling it."""
        self.cancel()

client_core.Client = Client
message.Client = Client
webhook.Client = Client
channel.Client = Client

del client_core
del re
del URLS
del message
del webhook
del RATELIMIT_GROUPS
del DISCOVERY_CATEGORIES
