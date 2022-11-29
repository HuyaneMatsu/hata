__all__ = ('Client', )

import sys, warnings
from json import JSONDecodeError
from math import inf

from scarletio import (
    CancelledError, CompoundMetaType, EventThread, Future, LOOP_TIME, Task, WaitTillAll, export, from_json,
    methodize, run_coroutine, sleep, write_exception_async
)

from ...env import CACHE_USER
from ...ext import get_and_validate_setup_functions, run_setup_functions

from ..activity import ACTIVITY_UNKNOWN, Activity, ActivityType
from ..application import Application, Team

from ..core import APPLICATION_ID_TO_CLIENT, CLIENTS, GUILDS, KOKORO, USERS
from ..events.core import register_client, unregister_client
from ..events.event_handler_manager import EventHandlerManager
from ..events.handling_helpers import ensure_shutdown_event_handlers, ensure_voice_client_shutdown_event_handlers
from ..events.intent import IntentFlag
from ..exceptions import (
    DiscordException, DiscordGatewayException, INTENT_ERROR_CODES, InvalidToken, RESHARD_ERROR_CODES
)
from ..gateway.client_gateway import (
    DiscordGateway, DiscordGatewaySharder
)
from ..guild import Guild
from ..http import DiscordHTTPClient, RateLimitProxy
from ..localization.utils import DEFAULT_LOCALE, Locale, get_locale
from ..message import Message
from ..preconverters import (
    preconvert_bool, preconvert_color, preconvert_discriminator, preconvert_flag, preconvert_preinstanced_type,
    preconvert_snowflake, preconvert_str
)
from ..user import (
    ClientUserBase, ClientUserPBase, GuildProfile, PremiumType, RelationshipType, Status, User,
    UserBase, UserFlag, create_partial_user_from_id
)

from .compounds import CLIENT_COMPOUNDS
from .functionality_helpers import _check_is_client_duped, try_get_user_id_from_token
from .ready_state import ReadyState


AUTO_CLIENT_ID_LIMIT = 1 << 22


@export
class Client(
    ClientUserPBase,
    *CLIENT_COMPOUNDS,
    build = True,
    metaclass = CompoundMetaType.with_(ClientUserPBase),
):
    """
    Discord client class used to interact with the Discord API.
    
    Attributes
    ----------
    id : `int`
        The client's unique identifier number.
    
    name : str
        The client's username.
    
    discriminator : `int`
        The client's discriminator. Given to avoid overlapping names.
    
    avatar_hash : `int`
        The client's avatar's hash in `uint128`.
    
    avatar_type : ``IconType``
        The client's avatar's type.
    
    banner_color : `None`, ``Color``
        The user's banner color if has any.
    
    banner_hash : `int`
        The user's banner's hash in `uint128`.
    
    banner_type : ``IconType``
        The user's banner's type.
    
    guild_profiles : `dict` of (`int`, ``GuildProfile``) items
        A dictionary, which contains the client's guild profiles. If a client is member of a guild, then it should
        have a respective guild profile accordingly.
    
    bot : `bool`
        Whether the client is a bot or a user account.
    
    flags : ``UserFlag``
        The client's user flags.
    
    thread_profiles : `None`, `dict` (``Channel``, ``ThreadProfile``) items
        A Dictionary which contains the thread profiles for the user in thread channel - thread profile relation.
        Defaults to `None`.
    
    activities : `None`, `list` of ``Activity``
        A list of the client's activities. Defaults to `None`.
    
    status : `Status`
        The client's display status.
    
    statuses : `dict` of (`str`, `str`) items
        The client's statuses for each platform.
    
    _activity : ``Activity``
        The client's preferred activity.
    
    _additional_owner_ids : `None`, `set` of `int`
        Additional users' (as id) to be passed by the ``.is_owner`` check.
    
    _gateway_max_concurrency : `int`
        The max amount of shards, which can be launched at the same time.
    
    _gateway_requesting : `bool`
        Whether the client already requests it's gateway.
    
    _gateway_time : `float`
        The last timestamp when ``._gateway_url`` was updated.
    
    _gateway_url : `str`
        Cached up gateway url, what is invalidated after `1` minute. Used to avoid unnecessary requests when launching
        up more shards.
    
    _gateway_waiter : `None`, ``Future``
        When client gateway is being requested multiple times at the same time, this future is set and awaited at the
        secondary requests.
    
    _should_request_users : `bool`
        Whether the client should try to request the users of it's guilds.
    
    _status : ``Status``
        The client's preferred status.
    
    _user_chunker_nonce : `int`
        The last nonce in int used for requesting guild user chunks. The default value is `0`, what means the next
        request will start at `1`.
        
        Nonce `0` is allocated for the case, when all the guild's users are requested.
    
    application : ``Application``
        The bot account's application. The application data of the client is requested meanwhile it logs in.
    
    email : `None`, `str`
        The client's email.
    
    events : ``EventHandlerManager``
        Contains the event handlers of the client. New event handlers can be added through it as well.
    
    gateway : ``DiscordGateway``, ``DiscordGatewaySharder``
        The gateway of the client towards Discord. If the client uses sharding, then ``DiscordGatewaySharder`` is used
        as gateway.
    
    group_channels : `dict` of (`int`, ``Channel``) items
        The group channels of the client. They can be accessed by their id as the key.
    
    guilds : `set` of ``Guild``
        The guilds, where the client is in.
    
    http : ``DiscordHTTPClient``
        The http session of the client. Can be used as a normal http session, or for lower level interactions with the
        Discord API.
    
    intents : ``IntentFlag``
        The intent flags of the client.
    
    locale : ``Locale``
        The preferred locale by the client.
    
    mfa : `bool`
        Whether the client has two factor authorization enabled on the account.
    
    premium_type : ``PremiumType``
        The Nitro subscription type of the client.
    
    private_channels : `dict` of (`int`, ``Channel``) items
        Stores the private channels of the client. The channels' other recipient' ids are the keys, meanwhile the
        channels are the values.
    
    ready_state : ``ReadyState``, `None`
        The client on login fills up it's ``.ready_state`` with ``Guild`` objects, which will have their members
        requested.
        
        When receiving a `READY` dispatch event, the client's ``.ready_state`` is set as a ``ReadyState`` and
        a ``._delay_ready`` task is started, what delays the handle-able `ready` event, till every user from the
        received guilds is cached up. When done, ``.ready_state`` is set back to `None`.
    
    relationships : `dict` of (`int`, ``Relationship``) items
        Stores the relationships of the client. The relationships' users' ids are the keys and the relationships
        themselves are the values.
    
    running : `bool`
        Whether the client is running or not. When the client is stopped, this attribute is set as `False` what causes
        it's heartbeats to stop and it's gateways to close and not reconnect.
    
    secret : `str`
        The client's secret used when interacting with oauth2 endpoints.
    
    shard_count : `int`
        The client's shard count. Set as `0` if the bot is not using sharding.
    
    token : `str`
        The client's token.
    
    verified : `bool`
        Whether the email of the client is verified.
    
    voice_clients : `dict` of (`int`, ``VoiceClient``) items
        Each bot can join a channel at every ``Guild`` and meanwhile they do, they have an active voice client for that
        guild. This attribute stores these voice clients. They keys are the guilds' ids, meanwhile the values are
        the voice clients.
    
    
    Class Attributes
    ----------------
    loop : ``EventThread``
        The event loop of the client. Every client uses the same one.
    _next_auto_id : `int`
        Auto id generator for clients without identifier.
    
    See Also
    --------
    - ``UserBase`` : The superclass of ``Client`` and of other user classes.
    - ``User`` : The default type of Discord users.
    - ``Webhook`` : Discord webhook entity.
    - ``WebhookRepr`` : Discord webhook's user representation.
    - ``Oauth2User`` : A user class with extended oauth2 attributes.
    
    Notes
    -----
    Client supports weakreferencing and dynamic attribute names as well for extension support.
    """
    __slots__ = (
        '__dict__', '_activity', '_additional_owner_ids', '_gateway_max_concurrency', '_gateway_requesting',
        '_gateway_time', '_gateway_url', '_gateway_waiter', '_should_request_users', '_status', '_user_chunker_nonce',
        'application', 'email', 'events', 'gateway', 'group_channels', 'guilds', 'http', 'intents', 'locale', 'mfa',
        'premium_type', 'private_channels', 'ready_state', 'relationships', 'running', 'secret', 'shard_count',
        'token', 'verified', 'voice_clients'
    )
    
    loop = KOKORO
    _next_auto_id = 1
    
    def __new__(
        cls,
        token,
        *,
        activity = ACTIVITY_UNKNOWN,
        additional_owners = None,
        application_id = None,
        bot = True,
        client_id = None,
        extensions = None,
        http_debug_options = None,
        intents = -1,
        is_bot = ...,
        secret = None,
        shard_count = 0,
        should_request_users = True,
        status = None,
        **kwargs
    ):
        """
        Creates a new ``Client`` with the given parameters.
        
        Parameters
        ----------
        token : `str`
            A valid Discord token, what the client can use to interact with the Discord API.
        
        activity : ``Activity`` = `ACTIVITY_UNKNOWN`, Optional (Keyword only)
            The client's preferred activity.
         
        additional_owners : `None`, `int`, ``ClientUserBase``, `iterable` of (`int`, ``ClientUserBase``) = `None` \
                , Optional (Keyword only)
            Additional users to return `True` if ``is_owner` is called.
        
        application_id : `None`, `int`, `str` = `None`, Optional (Keyword only)
            The client's application id. If passed as `str`, will be converted to `int`. Defaults to `None`.
        
        bot : `bool` = `True` Optional (Keyword only)
            Whether the client is a bot user or a user account.
        
        client_id : `None`, `int`, `str` = `None`, Optional (Keyword only)
            The client's `.id`. If passed as `str` will be converted to `int`. Defaults to `None`.
            
            When more `Client` is started up, it is recommended to define their id initially. The wrapper can detect the
            clients' id-s only when they are logging in, so the wrapper  needs to check if a ``User`` alter_ego of the
            client exists anywhere, and if does will replace it.
        
        extensions : `None`, `str`, `iterable` of `str` = `None`, Optional (Keyword only)
            The extension's name to setup on the client.
        
        http_debug_options: `None`, `str`, `iterable` of `str` = `None`, Optional (Keyword only)
            Http client debug options for the client.
        
        intents : ``IntentFlag`` = `-1`, Optional (Keyword only)
             By default the client will launch up using all the intent flags. Negative values will be interpreted as
             using all the intents, meanwhile if passed as positive, non existing intent flags are removed.
        
        secret: `None`, `str` = `None`, Optional (Keyword only)
            Client secret used when interacting with oauth2 endpoints.
        
        shard_count : `int` = `0`, Optional (Keyword only)
            The client's shard count. If passed as lower as the recommended one, will reshard itself.
        
        should_request_users : `int` = `False`, Optional (Keyword only)
            Whether the client should try to request the users of it's guilds.
        
        status : `None`, `str`, ``Status`` = `None`, Optional (Keyword only)
            The client's preferred status.
        
        **kwargs : keyword parameters
            Additional predefined attributes for the client.
        
        Other Parameters
        ----------------
        
        avatar : `None`, ``Icon``, `str`, Optional (Keyword only)
            The client's avatar.
            
            > Mutually exclusive with `avatar_type` and `avatar_hash`.
        
        avatar_type : ``IconType``, Optional (Keyword only)
            The client's avatar's type.
            
            > Mutually exclusive with `avatar_type`.
            
        avatar_hash : `int`, Optional (Keyword only)
            The client's avatar hash.
            
            > Mutually exclusive with `avatar`.
        
        banner : `None`, ``Icon``, `str`, Optional (Keyword only)
            The client's banner.
            
            > Mutually exclusive with `banner_type` and `banner_hash`.
        
        banner_color : `None`, ``Color``, Optional (Keyword only)
            The user's banner color.
        
        banner_type : ``IconType``, Optional (Keyword only)
            The client's banner's type.
            
            > Mutually exclusive with `banner_type`.
        
        banner_hash : `int`, Optional (Keyword only)
            The client's banner hash.
            
            > Mutually exclusive with `banner`.
        
        discriminator : `int`, `str`, Optional (Keyword only)
            The client's ``.discriminator``. Is accepted as `str` as well and will be converted to `int`.
        
        flags : ``UserFlag``, `int`, Optional (Keyword only)
            The client's ``.flags``. If not passed as ``UserFlag``, then will be converted to it.
        
        name : `str`, Optional (Keyword only)
            The client's ``.name``.
        
        **kwargs : keyword parameters
            Additional parameters to pass to extension setup functions.
            
            > If any required parameter by an extension is missing `RuntimeError` is raised, meanwhile if any extra
            > is given, `RuntimeWarning` is dropped.
        
        Returns
        -------
        client : ``Client``
        
        Raises
        ------
        TypeError
            If any parameter's type is bad or if unexpected parameter is passed.
        ValueError
            If an parameter's type is good, but it's value is unacceptable.
        RuntimeError
            Creating the same client multiple times is not allowed.
        """
        # ---- Required Parameters ----
        
        # token
        if (type(token) is str):
            pass
        elif isinstance(token, str):
            token = str(token)
        else:
            raise TypeError(f'`token` can be `str`, got {token.__class__.__name__}; {token!r}')
        
        # ---- Optional Client Parameters ----
        
        # activity
        if (not isinstance(activity, Activity)) or (activity.type is ActivityType.custom):
            raise TypeError(
                f'`activity` can be `{Activity.__name__}` (except `{ActivityType.custom.name}`), got '
                f'{activity.__class__.__name__}; {activity!r}.')
        
        # additional owners
        if additional_owners is None:
            additional_owner_ids = None
        else:
            additional_owner_ids = set()
            
            if isinstance(additional_owners, ClientUserBase):
                additional_owner_ids.add(additional_owners.id)
            elif type(additional_owners) is int:
                additional_owner_ids.add(additional_owners)
            elif isinstance(additional_owners, int):
                additional_owner_ids.add(int(additional_owners))
            else:
                iter_ = getattr(type(additional_owners), '__iter__', None)
                if iter_ is None:
                    raise TypeError(
                        f'`additional_owners` can be `iterable`, got {additional_owners.__class__.__name__}; '
                        f'{additional_owners!r}.'
                    )
                
                for additional_owner in iter_(additional_owners):
                    if type(additional_owner) is int:
                        pass
                    elif isinstance(additional_owner, int):
                        additional_owner = int(additional_owner)
                    elif isinstance(additional_owner, ClientUserBase):
                        additional_owner = additional_owner.id
                    else:
                        raise TypeError(
                            f'`additional_owners` contains a non `int`, `{ClientUserBase.__name__}` , got '
                            f'{additional_owner.__class__.__name__}; {additional_owner!r}.'
                        )
                    
                    additional_owner_ids.add(additional_owner)
                
                if (not additional_owner_ids):
                    additional_owner_ids = None
        
        # application_id
        if (application_id is None):
            application_id = 0
        else:
            application_id = preconvert_snowflake(application_id, 'application_id')
        
        application = Application._create_empty(application_id)
        

        # bot
        
        if is_bot is not ...:
            warnings.warn(
                (
                    f'`{cls.__name__}.__new__`\'s `is_bot` parameter is deprecated and will be removed in 2023 August. '
                    'Please use `bot` parameter instead. sus'
                ),
                FutureWarning,
                stacklevel = 2,
            )
            bot = is_bot
        
        bot = preconvert_bool(bot, 'bot')
        
        # client_id
        if client_id is None:
            client_id = try_get_user_id_from_token(token)
        else:
            client_id = preconvert_snowflake(client_id, 'client_id')
        
        # extensions
        # They will eb checked at the end
        
        # http_debug_options
        processed_http_debug_options = None
        
        if (http_debug_options is not None):
            if isinstance(http_debug_options, str):
                if type(http_debug_options) is not str:
                    http_debug_options = str(http_debug_options)
                
                if not http_debug_options.islower():
                    http_debug_options = http_debug_options.lower()
                
                processed_http_debug_options = {http_debug_options}
            else:
                iterator = getattr(type(http_debug_options), '__iter__', None)
                if (iterator is None):
                    raise TypeError(
                        f'`http_debug_options` can be `str`, `iterable` of `str`, got '
                        f'{http_debug_options.__class__.__name__}; {http_debug_options!r}.'
                    )
                
                for http_debug_option in iterator(http_debug_options):
                    
                    if type(http_debug_option) is str:
                        pass
                    elif isinstance(http_debug_option, str):
                        http_debug_option = str(http_debug_option)
                    else:
                        raise TypeError(
                            f'{http_debug_options} contains a non `str`, got '
                            f'{http_debug_options.__class__.__name__}; {http_debug_options!r}.'
                        )
                    
                    if not http_debug_option.islower():
                        http_debug_option = http_debug_option.lower()
                    
                    if processed_http_debug_options is None:
                        processed_http_debug_options = set()
                    
                    processed_http_debug_options.add(http_debug_option)
        
        # intents
        intents = preconvert_flag(intents, 'intents', IntentFlag)
        
        # secret
        if (secret is None) or type(secret is str):
            pass
        elif isinstance(secret, str):
            secret = str(secret)
        else:
            raise TypeError(f'`secret` can be `str`, got `{secret.__class__.__name__}`; {secret!r}.')
        
        # shard count
        if (type(shard_count) is int):
            pass
        elif isinstance(shard_count, int):
            shard_count = int(shard_count)
        else:
            raise TypeError(
                f'`shard_count` can be `int`, got {shard_count.__class__.__name__}; {shard_count!r}.'
            )
        
        if shard_count < 0:
            raise ValueError(
                f'`shard_count` can be non negative `int`, got {shard_count!r}.'
            )
        
        # Default shard count to `0` if we received `1`.
        if shard_count == 1:
            shard_count = 0
        
        # should_request_users
        should_request_users = preconvert_bool(should_request_users, 'should_request_users')
        
        # status
        if (status is not None):
            status = preconvert_preinstanced_type(status, 'status', Status)
            if status is Status.offline:
                status = Status.invisible
        
        if (status is None):
            status = Status.online
        
        
        # ---- Optional presettable user Parameters ----
        
        # kwargs
        if kwargs:
            processable = []
            
            # kwargs.avatar & kwargs.avatar_type & kwargs.avatar_hash
            cls.avatar.preconvert(kwargs, processable)
            
            # kwargs.banner & kwargs.banner_type & kwargs.banner_hash
            cls.banner.preconvert(kwargs, processable)
            
            try:
                banner_color = kwargs.pop('banner_color')
            except KeyError:
                pass
            else:
                banner_color = preconvert_color(banner_color, 'banner_color', True)
                processable.append(('banner_color', banner_color))
            
            # kwargs.discriminator
            try:
                discriminator = kwargs.pop('discriminator')
            except KeyError:
                pass
            else:
                discriminator = preconvert_discriminator(discriminator)
                processable.append(('discriminator', discriminator))
            
            # kwargs.flags
            try:
                flags = kwargs.pop('flags')
            except KeyError:
                pass
            else:
                flags = preconvert_flag(flags, 'flags', UserFlag)
                processable.append(('flags', flags))
            
            # kwargs.name
            try:
                name = kwargs.pop('name')
            except KeyError:
                pass
            else:
                name = preconvert_str(name, 'name', 2, 32)
                processable.append(('name', name))
            
            if not processable:
                processable = None
        
        else:
            processable = None
        
        
        # ---- Setup extensions ----
        
        # extensions
        setup_functions = get_and_validate_setup_functions(extensions, kwargs)
        
        
        # ---- Auto generate initial id if un-detected ----
        
        if client_id < AUTO_CLIENT_ID_LIMIT:
            client_id = cls._next_auto_id
            cls._next_auto_id = client_id + 1
        
        
        # ---- Build object ----
        
        # Set all Attributes
        
        self = object.__new__(cls)
        
        ClientUserPBase._set_default_attributes(self)
        self.bot = bot
        self.id = client_id
        
        self._activity = activity
        self._additional_owner_ids = additional_owner_ids
        self._gateway_max_concurrency = 1
        self._gateway_requesting = False
        self._gateway_time = -inf
        self._gateway_url = ''
        self._gateway_waiter = None
        self._should_request_users = should_request_users
        self._status = status
        self._user_chunker_nonce = 0
        self.application = application
        self.email = None
        self.events = EventHandlerManager(self)
        self.group_channels = {}
        self.guilds = set()
        self.http = DiscordHTTPClient(bot, token, debug_options=processed_http_debug_options)
        self.intents = intents
        self.locale = DEFAULT_LOCALE
        self.mfa = False
        self.premium_type = PremiumType.none
        self.private_channels = {}
        self.ready_state = None
        self.relationships = {}
        self.running = False
        self.secret = secret
        self.shard_count = shard_count
        self.token = token
        self.verified = False
        self.voice_clients = {}
        
        # These might require other attributes to be set
        self.gateway = (DiscordGatewaySharder if shard_count else DiscordGateway)(self)
        
        # Setup additional user related attributes
        if (processable is not None):
            for item in processable:
                setattr(self, *item)
        
        # Check whether the client is duped
        if client_id > AUTO_CLIENT_ID_LIMIT:
            _check_is_client_duped(self, client_id)
            self._maybe_replace_alter_ego()
        
        # Setup extensions
        run_setup_functions(self, setup_functions, kwargs)
        
        # Register client
        CLIENTS[client_id] = self
        
        # Register client by application id
        if application_id:
            APPLICATION_ID_TO_CLIENT[application_id] = self
        
        
        return self
    
    
    def _maybe_replace_alter_ego(self):
        """
        Replaces the type ``User`` alter_ego of the client if applicable.
        """
        client_id = self.id
        
        # GOTO
        while True:
            if CACHE_USER:
                try:
                    alter_ego = USERS[client_id]
                except KeyError:
                    # Go Out
                    break
                else:
                    if alter_ego is not self:
                        # we already exists, we need to go tru everything and replace our self.
                        guild_profiles = alter_ego.guild_profiles
                        self.guild_profiles = guild_profiles
                        for guild_id in guild_profiles.keys():
                            try:
                                guild = GUILDS[guild_id]
                            except KeyError:
                                continue
                            
                            guild.users[client_id] = self
            
            # This part should run at both case, except when there is no alter_ego detected when caching users.
            for client in CLIENTS.values():
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
        
        USERS[client_id] = self
    
    
    def _init_on_ready(self, data):
        """
        Fills up the client's instance attributes on login. If there is an already existing User object with the same
        id, the client will replace it at channel participants, at ``USERS`` weakreference dictionary, at
        ``guild.users``. This replacing is avoidable, if at the creation of the client the ``.client_id`` parameter is
        set.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data requested from Discord by the ``.client_login_static`` method.
        
        Raises
        ------
        RuntimeError
            Creating the same client multiple times is not allowed.
        """
        client_id = int(data['id'])
        _check_is_client_duped(self, client_id)
        
        self_id = self.id
        if self_id != client_id:
            if CLIENTS.get(self_id, None) is self:
                del CLIENTS[self_id]
            
            if USERS.get(self_id, None) is self:
                del USERS[self_id]
            
            CLIENTS[client_id] = self
            self.id = client_id
        
        self._maybe_replace_alter_ego()
        
        self.name = data['username']
        self.discriminator = int(data['discriminator'])
        self._set_avatar(data)
        self._set_banner(data)
        self.mfa = data.get('mfa_enabled', False)
        self.verified = data.get('verified', False)
        self.email = data.get('email', None)
        self.flags = UserFlag(data.get('flags', 0))
        self.premium_type = PremiumType.get(data.get('premium_type', 0))
        self.locale = get_locale(data.get('locale', None))
    
    
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
        Custom client's status is always `'web'`, so other than `''`, `'web'` will not be returned.
        """
        if self.status in (Status.offline, Status.invisible):
            return ''
        
        return 'web'
    
    
    def _delete(self):
        """
        Clears up the client's references. By default this is not called when a client is stopped. This method should
        be used when you want to get rid of every allocated objects by the client. Take care, local modules might still
        have active references to the client or to some other objects, what could cause them to not garbage collect.
        
        Raises
        ------
        RuntimeError
            If called when the client is still running.
        
        Examples
        --------
        ```py
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
        ```
        """
        if self.running:
            raise RuntimeError(f'`{self.__class__.__name__}._delete` called from a running client: {self!r}')
        
        client_id = self.id
        if CLIENTS.get(client_id, None) is self:
            del CLIENTS[client_id]
        
        
        application_id = self.application.id
        if APPLICATION_ID_TO_CLIENT.get(application_id, None) is self:
            del APPLICATION_ID_TO_CLIENT[application_id]
        
        if USERS.get(client_id, None) is self:
            alter_ego = User._from_client(self)
            USERS[client_id] = alter_ego
            
            guild_profiles = self.guild_profiles
            for guild_id in guild_profiles.keys():
                try:
                    guild = GUILDS[guild_id]
                except KeyError:
                    continue
                
                guild.users[client_id] = alter_ego
            
            for client in CLIENTS.values():
                if (client is not self) and client.running:
                    for relationship in client.relationships:
                        if relationship.user is alter_ego:
                            relationship.user = alter_ego
            
            thread_profiles = self.thread_profiles
            if (thread_profiles is not None):
                for channel in thread_profiles.keys():
                    thread_users = channel.thread_users
                    if (thread_users is not None):
                        thread_users[client_id] = alter_ego
            
            self.relationships.clear()
            for channel in self.group_channels.values():
                users = channel.users
                for index in range(len(users)):
                    if users[index].id == client_id:
                        users[index] = alter_ego
                        continue
        
        self.private_channels.clear()
        self.group_channels.clear()
        self.events.clear()
        
        self.guild_profiles.clear()
        self.thread_profiles = None
        self.status = Status.offline
        self.statuses.clear()
        self._activity = ACTIVITY_UNKNOWN
        self.activities = None
        self.ready_state = None
    
    
    # login
    async def client_login_static(self):
        """
        The first step at login in is requesting the client's user data. This method is also used to check whether
        the token of the client is valid.
        
        This method is a coroutine.
        
        Returns
        -------
        response_data : `dict` of (`str` : `Any`)
            Decoded json data got from Discord.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        InvalidToken
            When the token of the client is invalid.
        """
        while True:
            try:
                data = await self.http.client_user_get()
            except DiscordException as err:
                status = err.status
                if status == 401:
                    raise InvalidToken() from err
                
                if status >= 500:
                    await sleep(2.5, KOKORO)
                    continue
                
                raise
            
            return data
    
    
    async def update_application_info(self):
        """
        Updates the client's application's info.
        
        This method is a coroutine.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        Meanwhile the clients logs in this method is called to ensure that the client's application info is loaded.
        
        This endpoint is available only for bot accounts.
        """
        if self.bot:
            data = await self.http.application_get_own()
            application = self.application
            old_application_id = application.id
            application = application.from_data_own(data)
            self.application = application
            new_application_id = application.id
            
            if old_application_id != new_application_id:
                if APPLICATION_ID_TO_CLIENT.get(old_application_id, None) is self:
                    del APPLICATION_ID_TO_CLIENT[old_application_id]
                
                APPLICATION_ID_TO_CLIENT[new_application_id] = self
    
    
    async def client_gateway(self):
        """
        Requests the gateway information for the client.
        
        Only `1` request can be done at a time and every other will yield the result of first started one.
        
        This method is a coroutine.
        
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
            If any exception was received from the Discord API.
        """
        if self._gateway_requesting:
            gateway_waiter = self._gateway_waiter
            if gateway_waiter is None:
                gateway_waiter = self._gateway_waiter = Future(KOKORO)
            
            return await gateway_waiter
        
        self._gateway_requesting = True
        
        try:
            while True:
                if self.bot:
                    coroutine = self.http.client_gateway_bot()
                else:
                    coroutine = self.http.client_gateway_hooman()
                try:
                    data = await coroutine
                except DiscordException as err:
                    status = err.status
                    if status == 401:
                        await self.disconnect()
                        raise InvalidToken() from err
                    
                    if status >= 500:
                        await sleep(2.5, KOKORO)
                        continue
                    
                    raise
                
                break
            
            try:
                session_start_limit_data = data['session_start_limit']
            except KeyError:
                gateway_max_concurrency = 1
            else:
                gateway_max_concurrency = session_start_limit_data.get('max_concurrency', 1)
                
                try:
                    remaining = session_start_limit_data['remaining']
                except KeyError:
                    pass
                else:
                    if remaining < 100:
                        warnings.warn(
                            f'`Remaining session start limit reached low amount: {remaining!r}.',
                            RuntimeWarning,
                        )
            
            self._gateway_max_concurrency = gateway_max_concurrency
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
        
        This method is a coroutine.
        
        Raises
        ------
        ConnectionError
            No internet connection or if the request raised any ``DiscordException``.
        InvalidToken
            When the client's token is invalid.
        DiscordException
            If any exception was received from the Discord API.
        
        Returns
        -------
        gateway_url : `str`
            The url to what the gateways' websocket will be connected.
        """
        if self._gateway_time > (LOOP_TIME() - 60.0):
            return self._gateway_url
        
        data = await self.client_gateway()
        self._gateway_url = gateway_url = data['url']
        self._gateway_time = LOOP_TIME()
        
        return gateway_url
    
    
    async def client_gateway_reshard(self, force=False):
        """
        Reshards the client. And also updates it's gateway's url as a side note.
        
        Should be called only if every shard is down.
        
        This method is a coroutine.
        
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
            If any exception was received from the Discord API.
        """
        data = await self.client_gateway()
        self._gateway_url = data['url']
        self._gateway_time = LOOP_TIME()
        
        old_shard_count = self.shard_count
        if old_shard_count == 0:
            old_shard_count = 1
        
        new_shard_count = data.get('shards', 1)
        
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
    
    
    def start(self):
        """
        Starts the clients' connecting to Discord. If the client is already running, raises `RuntimeError`.
        
        The return of the method depends on the thread, from which it was called from.
        
        Returns
        -------
        task : `bool`, ``Task``, ``FutureAsyncWrapper``
            - If the method was called from the client's thread (KOKORO), then returns a ``Task``. The task will return
                `True`, if connecting was successful.
            - If the method was called from an ``EventThread``, but not from the client's, then returns a
                `FutureAsyncWrapper`. The task will return `True`, if connecting was successful.
            - If the method was called from any other thread, then waits for the connector task to finish and returns
                `True`, if it was successful.
        
        Raises
        ------
        RuntimeError
            If the client is already running.
        """
        if self.running:
            raise RuntimeError(f'{self!r} is already running!')
        
        return run_coroutine(self.connect(), KOKORO)
    
    
    def stop(self):
        """
        Starts disconnecting the client.
        
        The return of the method depends on the thread, from which it was called from.
        
        Returns
        -------
        task : `None`, ``Task``, ``FutureAsyncWrapper``
            - If the method was called from the client's thread (KOKORO), then returns a ``Task``.
            - If the method was called from an ``EventThread``, but not from the client's, then returns a
                `FutureAsyncWrapper`.
            - If the method was called from any other thread, returns `None` when disconnecting finished.
        """
        return run_coroutine(self.disconnect(), KOKORO)
    
    
    async def connect(self):
        """
        Starts connecting the client to Discord, fills up the undefined events and creates the task, what will keep
        receiving the data from Discord (``._connect``).
        
        If you want to start the connecting process consider using the top-level ``.start``, ``start_clients`` instead.
        
        This method is a coroutine.
        
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
        except GeneratorExit:
            raise
        
        except BaseException as err:
            if isinstance(err, ConnectionError) and err.args[0] == 'Invalid address':
                after = (
                    'Connection failed, could not connect to Discord.\n Please check your internet connection / has '
                    'Python rights to use it?\n'
                )
            else:
                after = None
            
            before = [
                'Exception occurred at calling ',
                self.__class__.__name__,
                '.connect\n',
            ]
            
            await write_exception_async(err, before, after, loop=KOKORO)
            return False
        
        # Some Discord implementations send string response for some weird reason.
        if isinstance(data, str):
            try:
                data = from_json(data)
            except JSONDecodeError:
                pass
        
        if not isinstance(data, dict):
            sys.stderr.write(
                ''.join([
                    (
                        'Connection failed, could not connect to Discord.\n'
                        'Received invalid data:\n'
                    ),
                    repr(data),
                    '\n',
                ])
            )
            return False
        
        self._init_on_ready(data)
        
        await self.client_gateway_reshard()
        await self.gateway.start()
        
        if self.bot:
            task = Task(self.update_application_info(), KOKORO)
            if __debug__:
                task.__silence__()
        
        # Check it twice, because meanwhile logging in, connect calls are not limited
        if self.running:
            raise RuntimeError(f'{self!r} is already running!')
        
        self.running = True
        register_client(self)
        Task(self._connect(), KOKORO)
        return True
    
    
    async def _connect(self):
        """
        Connects the client's gateway(s) to Discord and reconnects them if needed.
        
        This method is a coroutine.
        """
        try:
            while True:
                ready_state = self.ready_state
                if (ready_state is not None):
                    self.ready_state = None
                    ready_state.cancel()
                    ready_state = None
                
                try:
                    await self.gateway.run()
                except (GeneratorExit, CancelledError) as err:
                    # For now only here. These errors occurred randomly for me since I made the wrapper, only once-once,
                    # and it was not the wrapper causing them, so it is time to say STOP.
                    # I also know `GeneratorExit` will show up as RuntimeError, but it is already a RuntimeError.
                    try:
                        await write_exception_async(
                            err,
                            [
                                'Ignoring unexpected outer Task or coroutine cancellation at ',
                                repr(self),
                                '._connect:\n',
                            ],
                            loop = KOKORO,
                        )
                    except (GeneratorExit, CancelledError) as err:
                        sys.stderr.write(
                            f'Ignoring unexpected outer Task or coroutine cancellation at {self!r}._connect as '
                            f'{err!r} meanwhile rendering an exception for the same reason.\n'
                            f'The client will reconnect.\n'
                        )
                    continue
                
                except DiscordGatewayException as err:
                    if err.code in RESHARD_ERROR_CODES:
                        sys.stderr.write(
                            f'{err.__class__.__name__} occurred, at {self!r}._connect:\n'
                            f'{err!r}\n'
                            f'The client will reshard itself and reconnect.\n'
                        )
                        
                        await self.client_gateway_reshard(force=True)
                        continue
                    
                    raise
                
                else:
                    if not self.running:
                        break
                    
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
                                write_exception_async(
                                    err,
                                    [
                                        'Ignoring unexpected outer Task or coroutine cancellation at ',
                                        repr(self),
                                        '._connect:\n',
                                    ],
                                    loop = KOKORO,
                                )
                            except (GeneratorExit, CancelledError) as err:
                                sys.stderr.write(
                                    f'Ignoring unexpected outer Task or coroutine cancellation at {self!r}._connect as '
                                    f'{err!r} meanwhile rendering an exception for the same reason.\n'
                                    f'The client will reconnect.\n'
                                )
                            continue
                    continue
        except BaseException as err:
            if (
                isinstance(err, InvalidToken) or
                (
                    isinstance(err, DiscordGatewayException) and
                    (err.code in INTENT_ERROR_CODES)
                )
            ):
                sys.stderr.write(
                    f'{err.__class__.__name__} occurred, at {self!r}._connect:\n'
                    f'{err!r}\n'
                )
            else:
                write_exception_async(
                    err,
                    [
                        'Unexpected exception occurred at ',
                        repr(self),
                        '._connect\n',
                    ],
                    (
                        'If you can reproduce this bug, Please send me a message or open an issue with your code, and '
                        'with every detail how to reproduce it.\n'
                        'Thanks!\n'
                    ),
                    loop = KOKORO,
                )
            
            await ensure_shutdown_event_handlers(self)
        
        finally:
            try:
                await self.gateway.close()
            finally:
                unregister_client(self)
                self.running = False
                
                if not self.guild_profiles:
                    return
                
                to_remove = []
                for guild_id in self.guild_profiles.keys():
                    try:
                        guild = GUILDS[guild_id]
                    except KeyError:
                        continue
                    
                    guild._delete(self)
                    if not guild.partial:
                        continue
                    
                    to_remove.append(guild_id)
                
                if to_remove:
                    for guild_id in to_remove:
                        try:
                            del self.guild_profiles[guild_id]
                        except KeyError:
                            pass
                
                # need to delete the references for cleanup
                guild = None
                to_remove = None
                
                ready_state = self.ready_state
                if (ready_state is not None):
                    self.ready_state = None
                    ready_state.cancel()
                    ready_state = None
    
    
    def _delay_ready(self, guild_datas, shard_id):
        """
        Delays the client's "ready" till it receives all of it guild's data. If caching is allowed (so by default),
        then it waits additional time till it requests all the members of it's guilds.
        
        Parameters
        ----------
        guild_datas : `list` of `dict` (`str`, `Any`) items
            Partial data for all the guilds to request the users of.
        shard_id : `int`
            The received shard's identifier.
        """
        ready_state = self.ready_state
        if (ready_state is None):
            ready_state = ReadyState(self)
            self.ready_state = ready_state
        
        ready_state.shard_ready(self, guild_datas, shard_id)
    
    
    
    async def disconnect(self):
        """
        Disconnects the client and closes it's websocket(s). Till the client goes offline, it might take even over
        than `1` minute. Because bot accounts can not logout, so they need to wait for timeout.
        
        This method is a coroutine.
        """
        if not self.running:
            return
        
        self.running = False
        shard_count = self.shard_count
        
        # cancel shards
        if shard_count:
            for gateway in self.gateway.gateways:
                gateway.kokoro.cancel()
        else:
            self.gateway.kokoro.cancel()
        
        await ensure_voice_client_shutdown_event_handlers(self)
        
        # Log off if user account
        if (not self.bot):
            await self.http.client_logout()
        
        
        # Close gateways
        if shard_count:
            tasks = []
            for gateway in self.gateway.gateways:
                websocket = gateway.websocket
                if (websocket is not None) and websocket.open:
                    tasks.append(Task(gateway.close(), KOKORO))
            
            if tasks:
                future = WaitTillAll(tasks, KOKORO)
                tasks = None # clear references
                await future
                future = None # clear references
            else:
                tasks = None # clear references
            
        else:
            websocket = self.gateway.websocket
            if (websocket is not None) and websocket.open:
                await self.gateway.close()
        
        gateway = None # clear references
        websocket = None # clear references
        
        await ensure_shutdown_event_handlers(self)
    
    
    def voice_client_for(self, message):
        """
        Returns the voice client for the given message's guild if it has any.
        
        Parameters
        ----------
        message : ``Message``
            The message what's voice client will be looked up.
        
        Returns
        -------
        voice_client : `None`, ``VoiceClient``
            The voice client if applicable.
        """
        guild_id = message.guild_id
        if guild_id is None:
            voice_client = None
        else:
            voice_client = self.voice_clients.get(guild_id, None)
        return voice_client
    
    
    def get_guild(self, name, default = None):
        """
        Tries to find a guild by it's name. If there is no guild with the given name, then returns the passed
        default value.
        
        Parameters
        ----------
        name : `str`
            The guild's name to search.
        default : `None`, `Any` = `None`, Optional
            The default value, what will be returned if the guild was not found.
        
        Returns
        -------
        guild : ``Guild``, `default`
        
        Raises
        ------
        AssertionError
            - If `name` was not given as `str`.
            - If `name` length is out of the expected range [2:100].
        
        """
        if __debug__:
            if not isinstance(name, str):
                raise AssertionError(
                    f'`name` can be `str`, got {name.__class__.__name__}; {name!r}.'
                )
            
            name_length = len(name)
            if name_length < 2 or name_length > 100:
                raise AssertionError(
                    f'`name` length can be in range [1:100], got {name_length!r}; {name!r}.'
                )
        
        for guild_id in self.guild_profiles.keys():
            try:
                guild = GUILDS[guild_id]
            except KeyError:
                continue
            
            if guild.name == name:
                return guild
        
        return default
    
    
    get_rate_limits_of = methodize(RateLimitProxy)
    
    
    @property
    def owner(self):
        """
        Returns the client's owner if applicable.
        
        If the client is a user account, or if it's ``.update_application_info`` was not called yet, then returns
        ``ZEROUSER``. If the client is owned by a ``Team``, then returns the team's owner.
        
        Returns
        -------
        owner : ``ClientUserBase``
        """
        application_owner = self.application.owner
        if isinstance(application_owner, Team):
            owner = application_owner.owner
        else:
            owner = application_owner
        
        return owner
    
    
    def is_owner(self, user):
        """
        Returns whether the passed user is one of the client's owners.
        
        Parameters
        ----------
        user : ``ClientUserBase``
            The user who will be checked.
        
        Returns
        -------
        is_owner : `bool`
        """
        application_owner = self.application.owner
        if isinstance(application_owner, Team):
            if user in application_owner.accepted:
                return True
        else:
            if application_owner is user:
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
        *users : `int`, ``UserBase``
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
            index += 1
            if not isinstance(user, (int, UserBase)):
                raise TypeError(
                    f'`users[{index}]` is not `int`, `{UserBase.__name__}`, got {user.__class__.__name__}; {user!r}; '
                    f'users={users!r}.'
                )
            
            if index == limit:
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
        Removes additional owners added by the ``.add_additional_owners`` method.
        
        Parameters
        ----------
        *users : `int`, ``UserBase``
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
            index += 1
            if not isinstance(user, (int, UserBase)):
                raise TypeError(
                    f'`users[{index}]` is not `int`, `{UserBase.__name__}`, got {user.__class__.__name__}; {user!r}; '
                    f'users={users!r}.'
                )
            
            if index == limit:
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
            
            additional_owner_ids.discard(user)
    
    
    @property
    def owners(self):
        """
        Returns the owners of the client.
        
        Returns
        -------
        owners : `set` of ``ClientUserBase``
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
                user = create_partial_user_from_id(user_id)
                owners.add(user)
        
        return owners
    
    
    def _difference_update_attributes(self, data):
        """
        Updates the client and returns it's old attributes in a `dict` with `attribute-name`, `old-value` relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `Any`) items
            All item in the returned dictionary is optional.
            
            +-----------------------+-----------------------+
            | Keys                  | Values                |
            +=======================+=======================+
            | avatar                | ``Icon``              |
            +-----------------------+-----------------------+
            | banner                | ``Icon``              |
            +-----------------------+-----------------------+
            | banner_color          | `None`, ``Color``     |
            +-----------------------+-----------------------+
            | discriminator         | `int`                 |
            +-----------------------+-----------------------+
            | email                 | `None`, `str`         |
            +-----------------------+-----------------------+
            | flags                 | ``UserFlag``          |
            +-----------------------+-----------------------+
            | locale                | ``Locale``            |
            +-----------------------+-----------------------+
            | mfa                   | `bool`                |
            +-----------------------+-----------------------+
            | name                  | `str                  |
            +-----------------------+-----------------------+
            | premium_type          | ``PremiumType``       |
            +-----------------------+-----------------------+
            | verified              | `bool`                |
            +-----------------------+-----------------------+
        """
        old_attributes = ClientUserPBase._difference_update_attributes(self, data)
        
        email = data.get('email', None)
        if self.email != email:
            old_attributes['email'] = self.email
            self.email = email
        
        
        premium_type = PremiumType.get(data.get('premium_type', 0))
        if self.premium_type is not premium_type:
            old_attributes['premium_type'] = premium_type
            self.premium_type = premium_type
        
        
        verified = data.get('verified', False)
        if self.verified != verified:
            old_attributes['verified'] = self.verified
            self.verified = verified
        
        
        mfa = data.get('mfa_enabled', False)
        if self.mfa != mfa:
            old_attributes['mfa'] = self.mfa
            self.mfa = mfa
        
        
        locale = get_locale(data.get('locale', None))
        if self.locale is not locale:
            old_attributes['locale'] = self.locale
            self.locale = locale
        
        
        return old_attributes
    
    
    def _set_attributes(self, data):
        """
        Updates the client by overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        """
        ClientUserPBase._update_attributes(self, data)
        
        self.verified = data.get('verified', False)
        
        self.email = data.get('email', None)
        
        self.premium_type = PremiumType.get(data.get('premium_type', 0))
        
        self.mfa = data.get('mfa_enabled', False)
        
        self.locale = get_locale(data.get('locale', None))
    
    
    def _difference_update_profile_only(self, data, guild):
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
        +-------------------+-------------------------------+
        | Keys              | Values                        |
        +===================+===============================+
        | avatar            | ``Icon``                      |
        +-------------------+-------------------------------+
        | boosts_since      | `None`, `datetime`            |
        +-------------------+-------------------------------+
        | nick              | `None`, `str`                 |
        +-------------------+-------------------------------+
        | pending           | `bool`                        |
        +-------------------+-------------------------------+
        | role_ids          | `None`, `tuple` of `int`      |
        +-------------------+-------------------------------+
        | timed_out_until   | `None`, `datetime`            |
        +-------------------+-------------------------------+
        """
        try:
            profile = self.guild_profiles[guild.id]
        except KeyError:
            self.guild_profiles[guild.id] = GuildProfile.from_data(data)
            guild.users[self.id] = self
            return {}
        
        return profile._difference_update_attributes(data)
    
    
    def _update_profile_only(self, data, guild):
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
            profile = self.guild_profiles[guild.id]
        except KeyError:
            self.guild_profiles[guild.id] = GuildProfile.from_data(data)
            guild.users[self.id] = self
        else:
            profile._update_attributes(data)
    
    
    @property
    def friends(self):
        """
        Returns the client's friends.
        
        Returns
        -------
        relationships : `list` of ``Relationship`` objects
        """
        type_ = RelationshipType.friend
        return [relationship for relationship in self.relationships.values() if relationship.type is type_]
    
    
    @property
    def blocked(self):
        """
        Returns the client's blocked relationships.
        
        Returns
        -------
        relationships : `list` of ``Relationship`` objects
        """
        type_ = RelationshipType.blocked
        return [relationship for relationship in self.relationships.values() if relationship.type is type_]
    
    
    @property
    def received_requests(self):
        """
        Returns the received friend requests of the client.
        
        Returns
        -------
        relationships : `list` of ``Relationship`` objects
        """
        type_ = RelationshipType.pending_incoming
        return [relationship for relationship in self.relationships.values() if relationship.type is type_]
    
    
    @property
    def sent_requests(self):
        """
        Returns the sent friend requests of the client.
        
        Returns
        -------
        relationships : `list` of ``Relationship`` objects
        """
        type_ = RelationshipType.pending_outgoing
        return [relationship for relationship in self.relationships.values() if relationship.type is type_]
    
    
    def gateway_for(self, guild_id):
        """
        Returns the corresponding gateway of the client to the passed guild.
        
        Parameters
        ----------
        guild_id : `int`
            The respective guild's identifier, what's gateway will be returned.
            
            Pass it as `0` to get the default gateway.
        
        Returns
        -------
        gateway : ``DiscordGateway``
        """
        gateway = self.gateway
        shard_count = self.shard_count
        if shard_count:
            gateway = gateway.gateways[(guild_id >> 22) % shard_count]
        
        return gateway
    
    
    @classmethod
    def _from_client(cls, client):
        """
        Creates a client alter ego.
        
        Parameters
        ----------
        client : ``Client``
            The client to copy.
        
        Raises
        ------
        RuntimeError
            Not applicable for ``Client``-s.
        """
        raise RuntimeError('Cannot create client copy from client.')
    
    
    @classmethod
    def _create_empty(cls, user_id):
        """
        Creates a user instance with the given `user_id` and with the default user attributes.
        
        Parameters
        ----------
        user_id : `int`
            The user's id.
        
        Raises
        ------
        RuntimeError
            Not applicable for ``Client``-s.
        """
        raise RuntimeError('Cannot create empty client.')
