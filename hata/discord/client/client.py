__all__ = ('Client', )

import re, reprlib, sys, warnings
from collections import deque
from datetime import datetime
from json import JSONDecodeError
from math import inf
from time import time as time_now

from scarletio import (
    CancelledError, EventThread, Future, IgnoreCaseMultiValueDictionary, LOOP_TIME, Task, WaitTillAll, WaitTillFirst,
    change_on_switch, export, from_json, future_or_timeout, methodize, run_coroutine, sleep
)
from scarletio.web_common import BasicAuth, Formdata
from scarletio.web_common.headers import AUTHORIZATION

from ...env import API_VERSION, CACHE_PRESENCE, CACHE_USER
from ...ext import get_and_validate_setup_functions, run_setup_functions

from ..activity import ACTIVITY_UNKNOWN, ActivityBase, ActivityCustom
from ..allowed_mentions import parse_allowed_mentions
from ..application import Application, EULA, Team
from ..bases import maybe_snowflake, maybe_snowflake_pair
from ..channel import (
    AUTO_ARCHIVE_DEFAULT, AUTO_ARCHIVE_OPTIONS, CHANNEL_TYPES, CHANNEL_TYPE_MAP, ChannelBase, ChannelCategory,
    ChannelDirectory, ChannelGroup, ChannelGuildBase, ChannelGuildMainBase, ChannelGuildUndefined, ChannelPrivate,
    ChannelStage, ChannelStore, ChannelText, ChannelTextBase, ChannelThread, ChannelVoice, ChannelVoiceBase,
    MessageIterator, VideoQualityMode, cr_pg_channel_object, create_partial_channel_from_id, message_relative_index
)
from ..color import Color
from ..core import (
    APPLICATIONS, APPLICATION_COMMANDS, APPLICATION_ID_TO_CLIENT, CHANNELS, CLIENTS, DISCOVERY_CATEGORIES, EMOJIS,
    EULAS, GUILDS, KOKORO, MESSAGES, ROLES, SCHEDULED_EVENTS, USERS
)
from ..embed import EmbedImage
from ..emoji import Emoji
from ..events.core import register_client, unregister_client
from ..events.event_handler_manager import EventHandlerManager
from ..events.handling_helpers import (
    WaitForHandler, ensure_shutdown_event_handlers, ensure_voice_client_shutdown_event_handlers
)
from ..events.intent import IntentFlag
from ..exceptions import (
    DiscordException, DiscordGatewayException, ERROR_CODES, INTENT_ERROR_CODES, InvalidToken, RESHARD_ERROR_CODES
)
from ..gateway.client_gateway import (
    DiscordGateway, DiscordGatewaySharder, PRESENCE as GATEWAY_OPERATION_CODE_PRESENCE,
    REQUEST_MEMBERS as GATEWAY_OPERATION_CODE_REQUEST_MEMBERS
)
from ..guild import (
    AuditLog, AuditLogEvent, AuditLogIterator, COMMUNITY_FEATURES, ContentFilterLevel, DiscoveryCategory, Guild,
    GuildDiscovery, GuildFeature, GuildPreview, GuildWidget, MessageNotificationLevel, SystemChannelFlag,
    VerificationLevel, VerificationScreen, VerificationScreenStep, VoiceRegion, WelcomeChannel, WelcomeScreen,
    create_partial_guild_from_data, create_partial_guild_from_id
)
from ..http import (
    DiscordHTTPClient, RateLimitProxy, VALID_ICON_MEDIA_TYPES, VALID_ICON_MEDIA_TYPES_EXTENDED,
    VALID_STICKER_IMAGE_MEDIA_TYPES, is_media_url, rate_limit_groups
)
from ..integration import Integration
from ..interaction import (
    ApplicationCommand, ApplicationCommandPermission, ApplicationCommandPermissionOverwrite,
    ApplicationCommandPermissionOverwriteTargetType, INTERACTION_RESPONSE_TYPES, InteractionEvent, InteractionForm,
    InteractionResponseContext, InteractionType
)
from ..interaction.application_command import (
    APPLICATION_COMMAND_LIMIT_GLOBAL, APPLICATION_COMMAND_LIMIT_GUILD, APPLICATION_COMMAND_PERMISSION_OVERWRITE_MAX
)
from ..invite import Invite, InviteTargetType
from ..message import Attachment, Message, MessageFlag, MessageReference, MessageRepr
from ..message.utils import process_message_chunk
from ..message.utils import try_resolve_interaction_message
from ..oauth2 import Achievement, Connection, OA2Access, UserOA2
from ..oauth2.helpers import DEFAULT_LOCALE, parse_locale
from ..permission import Permission, PermissionOverwrite, PermissionOverwriteTargetType
from ..permission.permission import (
    PERMISSION_MASK_CREATE_INSTANT_INVITE, PERMISSION_MASK_MANAGE_MESSAGES, PERMISSION_MASK_READ_MESSAGE_HISTORY
)
from ..preconverters import (
    preconvert_bool, preconvert_color, preconvert_discriminator, preconvert_flag, preconvert_preinstanced_type,
    preconvert_snowflake, preconvert_str
)
from ..role import Role
from ..scheduled_event import PrivacyLevel, ScheduledEvent, ScheduledEventEntityType, ScheduledEventStatus
from ..stage import Stage
from ..sticker import Sticker, StickerPack
from ..user import (
    ClientUserBase, ClientUserPBase, GuildProfile, HypesquadHouse, PremiumType, RelationshipType, Status, User,
    UserBase, UserFlag, create_partial_user_from_id, thread_user_create
)
from ..utils import (
    DISCORD_EPOCH, MEDIA_TYPE_TO_EXTENSION, Relationship, datetime_to_timestamp, get_image_media_type, image_to_base64,
    log_time_converter
)
from ..voice import VoiceClient
from ..webhook import Webhook, create_partial_webhook_from_id

from .functionality_helpers import (
    DiscoveryCategoryRequestCacher, DiscoveryTermRequestCacher, ForceUpdateCache, MassUserChunker,
    MultiClientMessageDeleteSequenceSharder, SingleUserChunker, _check_is_client_duped,
    _message_delete_multiple_private_task, _message_delete_multiple_task,
    application_command_autocomplete_choice_parser, channel_move_sort_key, request_channel_thread_channels,
    role_move_key, role_reorder_valid_roles_sort_key, try_get_user_id_from_token
)
from .ready_state import ReadyState
from .request_helpers import (
    add_file_to_message_data, get_achievement_and_id, get_achievement_id, get_channel_and_id, get_channel_id,
    get_channel_id_and_message_id, get_components_data, get_emoji_from_reaction, get_guild_and_guild_text_channel_id,
    get_guild_and_id, get_guild_and_id_and_scheduled_event_id, get_guild_discovery_and_id, get_guild_id,
    get_guild_id_and_channel_id, get_guild_id_and_emoji_id, get_guild_id_and_role_id,
    get_guild_id_and_scheduled_event_id, get_message_and_channel_id_and_message_id, get_reaction, get_role_id,
    get_scheduled_event_guild_id_and_id, get_stage_channel_id, get_sticker_and_id, get_sticker_pack_and_id,
    get_user_and_id, get_user_id, get_user_id_nullable, get_webhook_and_id, get_webhook_and_id_token, get_webhook_id,
    get_webhook_id_token, validate_content_and_embed, validate_message_to_delete
)
from .utils import BanEntry, Typer, UserGuildPermission


_VALID_NAME_CHARS = re.compile('([0-9A-Za-z_]+)')

MESSAGE_FLAG_VALUE_INVOKING_USER_ONLY = MessageFlag().update_by_keys(invoking_user_only=True)
MESSAGE_FLAG_VALUE_SUPPRESS_EMBEDS = MessageFlag().update_by_keys(embeds_suppressed=True)

AUTO_CLIENT_ID_LIMIT = 1 << 22

STICKER_PACK_CACHE = ForceUpdateCache()


@export
class Client(ClientUserPBase):
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
    is_bot : `bool`
        Whether the client is a bot or a user account.
    partial : `bool`
        Partial clients have only their id set. If any other data is set, it might not be in sync with Discord.
    thread_profiles : `None`, `dict` (``ChannelThread``, ``ThreadProfile``) items
        A Dictionary which contains the thread profiles for the user in thread channel - thread profile relation.
        Defaults to `None`.
    activities : `None`, `list` of ``ActivityBase``
        A list of the client's activities. Defaults to `None`.
    status : `Status`
        The client's display status.
    statuses : `dict` of (`str`, `str`) items
        The client's statuses for each platform.
    email : `None`, `str`
        The client's email.
    flags : ``UserFlag``
        The client's user flags.
    locale : `str`
        The preferred locale by the client.
    mfa : `bool`
        Whether the client has two factor authorization enabled on the account.
    premium_type : ``PremiumType``
        The Nitro subscription type of the client.
    verified : `bool`
        Whether the email of the client is verified.
    application : ``Application``
        The bot account's application. The application data of the client is requested meanwhile it logs in.
    events : ``EventHandlerManager``
        Contains the event handlers of the client. New event handlers can be added through it as well.
    gateway : ``DiscordGateway``, ``DiscordGatewaySharder``
        The gateway of the client towards Discord. If the client uses sharding, then ``DiscordGatewaySharder`` is used
        as gateway.
    guilds : `set` of ``Guild``
        The guilds, where the client is in.
    http : ``DiscordHTTPClient``
        The http session of the client. Can be used as a normal http session, or for lower level interactions with the
        Discord API.
    intents : ``IntentFlag``
        The intent flags of the client.
    private_channels : `dict` of (`int`, ``ChannelPrivate``) items
        Stores the private channels of the client. The channels' other recipient' ids are the keys, meanwhile the
        channels are the values.
    group_channels : `dict` of (`int`, ``ChannelGroup``) items
        The group channels of the client. They can be accessed by their id as the key.
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
    voice_clients : `dict` of (`int`, ``VoiceClient``) items
        Each bot can join a channel at every ``Guild`` and meanwhile they do, they have an active voice client for that
        guild. This attribute stores these voice clients. They keys are the guilds' ids, meanwhile the values are
        the voice clients.
    _activity : ``ActivityBase``
        The client's preferred activity.
    _additional_owner_ids : `None`, `set` of `int`
        Additional users' (as id) to be passed by the ``.is_owner`` check.
    _gateway_url : `str`
        Cached up gateway url, what is invalidated after `1` minute. Used to avoid unnecessary requests when launching
        up more shards.
    _gateway_requesting : `bool`
        Whether the client already requests it's gateway.
    _gateway_time : `float`
        The last timestamp when ``._gateway_url`` was updated.
    _gateway_max_concurrency : `int`
        The max amount of shards, which can be launched at the same time.
    _gateway_waiter : `None`, ``Future``
        When client gateway is being requested multiple times at the same time, this future is set and awaited at the
        secondary requests.
    _status : ``Status``
        The client's preferred status.
    _user_chunker_nonce : `int`
        The last nonce in int used for requesting guild user chunks. The default value is `0`, what means the next
        request will start at `1`.
        
        Nonce `0` is allocated for the case, when all the guild's users are requested.
    
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
    - ``UserOA2`` : A user class with extended oauth2 attributes.
    
    Notes
    -----
    Client supports weakreferencing and dynamic attribute names as well for extension support.
    """
    __slots__ = (
        'email', 'locale', 'mfa', 'premium_type', 'verified', # OAUTH 2
        '__dict__', '_additional_owner_ids', '_activity', '_gateway_requesting', '_gateway_time', '_gateway_url',
        '_gateway_max_concurrency', '_gateway_waiter', '_status', '_user_chunker_nonce', 'application', 'events',
        'gateway', 'guilds', 'http', 'intents', 'private_channels', 'ready_state', 'group_channels', 'relationships',
        'running', 'secret', 'shard_count', 'token', 'voice_clients'
    )
    
    loop = KOKORO
    _next_auto_id = 1
    
    def __new__(cls, token, *, secret=None, client_id=None, application_id=None, activity=ACTIVITY_UNKNOWN,
            status=None, is_bot=True, shard_count=0, intents=-1, additional_owners=None, extensions=None,
            http_debug_options=None, **kwargs):
        """
        Creates a new ``Client`` with the given parameters.
        
        Parameters
        ----------
        token : `str`
            A valid Discord token, what the client can use to interact with the Discord API.
        
        secret: `None`, `str` = `None`, Optional (Keyword only)
            Client secret used when interacting with oauth2 endpoints.
        
        client_id : `None`, `int`, `str` = `None`, Optional (Keyword only)
            The client's `.id`. If passed as `str` will be converted to `int`. Defaults to `None`.
            
            When more `Client` is started up, it is recommended to define their id initially. The wrapper can detect the
            clients' id-s only when they are logging in, so the wrapper  needs to check if a ``User`` alter_ego of the
            client exists anywhere, and if does will replace it.
        
        application_id : `None`, `int`, `str` = `None`, Optional (Keyword only)
            The client's application id. If passed as `str`, will be converted to `int`. Defaults to `None`.
        
        activity : ``ActivityBase`` = `ACTIVITY_UNKNOWN`, Optional (Keyword only)
            The client's preferred activity.
        
        status : `None`, `str`, ``Status`` = `None`, Optional (Keyword only)
            The client's preferred status.
        
        is_bot : `bool` = `True` Optional (Keyword only)
            Whether the client is a bot user or a user account.
        
        shard_count : `int` = `0`, Optional (Keyword only)
            The client's shard count. If passed as lower as the recommended one, will reshard itself.
        
        intents : ``IntentFlag`` = `-1`, Optional (Keyword only)
             By default the client will launch up using all the intent flags. Negative values will be interpreted as
             using all the intents, meanwhile if passed as positive, non existing intent flags are removed.
         
        additional_owners : `None`, `int`, ``ClientUserBase``, `iterable` of (`int`, ``ClientUserBase``) = `None` \
                , Optional (Keyword only)
            Additional users to return `True` if ``is_owner` is called.
        
        extensions : `None`, `str`, `iterable` of `str` = `None`, Optional (Keyword only)
            The extension's name to setup on the client.
        
        http_debug_options: `None`, `str`, `iterable` of `str` = `None`, Optional (Keyword only)
            Http client debug options for the client.
        
        **kwargs : keyword parameters
            Additional predefined attributes for the client.
        
        Other Parameters
        ----------------
        name : `str`, Optional (Keyword only)
            The client's ``.name``.
        
        discriminator : `int`, `str`, Optional (Keyword only)
            The client's ``.discriminator``. Is accepted as `str` as well and will be converted to `int`.
        
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
        
        flags : ``UserFlag``, `int`, Optional (Keyword only)
            The client's ``.flags``. If not passed as ``UserFlag``, then will be converted to it.
        **kwargs : keyword parameters
            Additional parameters to pass to extension setuppers.
            
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
        # token
        if (type(token) is str):
            pass
        elif isinstance(token, str):
            token = str(token)
        else:
            raise TypeError(f'`token` can be `str`, got {token.__class__.__name__}; {token!r}')
        
        # secret
        if (secret is None) or type(secret is str):
            pass
        elif isinstance(secret, str):
            secret = str(secret)
        else:
            raise TypeError(f'`secret` can be `str`, got `{secret.__class__.__name__}`; {secret!r}.')
        
        # client_id
        if client_id is None:
            client_id = try_get_user_id_from_token(token)
        else:
            client_id = preconvert_snowflake(client_id, 'client_id')
        
        # application_id
        if (application_id is None):
            application_id = 0
        else:
            application_id = preconvert_snowflake(application_id, 'application_id')
        
        application = Application._create_empty(application_id)
        
        # activity
        if (not isinstance(activity, ActivityBase)) or (type(activity) is ActivityCustom):
            raise TypeError(
                f'`activity` can be `{ActivityBase.__name__}` (except `{ActivityCustom.__name__}`), got '
                f'{activity.__class__.__name__}; {activity!r}.')
        
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
            raise TypeError(
                f'`shard_count` can be `int`, got {shard_count.__class__.__name__}; {shard_count!r}.'
            )
        
        if shard_count < 0:
            raise ValueError(
                f'`shard_count` can be non negative `int`, got {shard_count!r}.'
            )
        
        # Default to `0`
        if shard_count == 1:
            shard_count = 0
        
        # intents
        intents = preconvert_flag(intents, 'intents', IntentFlag)
        
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
            
            # kwargs.banner & kwargs.banner_type & kwargs.banner_hash
            cls.banner.preconvert(kwargs, processable)
            
            # kwargs.flags
            try:
                flags = kwargs.pop('flags')
            except KeyError:
                pass
            else:
                flags = preconvert_flag(flags, 'flags', UserFlag)
                processable.append(('flags', flags))
            
            try:
                banner_color = kwargs.pop('banner_color')
            except KeyError:
                pass
            else:
                banner_color = preconvert_color(banner_color, 'banner_color', True)
                processable.append(('banner_color', banner_color))
        
        else:
            processable = None
        
        if (status is None):
            _status = Status.online
        else:
            _status = status
        
        setup_functions = get_and_validate_setup_functions(extensions, kwargs)
        
        
        if client_id < AUTO_CLIENT_ID_LIMIT:
            client_id = cls._next_auto_id
            cls._next_auto_id = client_id + 1
        
        self = object.__new__(cls)
        
        ClientUserPBase._set_default_attributes(self)
        
        self.mfa = False
        self.verified = False
        self.email = None
        self.premium_type = PremiumType.none
        self.locale = DEFAULT_LOCALE
        self.token = token
        self.secret = secret
        self.is_bot = is_bot
        self.shard_count = shard_count
        self.intents = intents
        self.running = False
        self.relationships = {}
        self._status = _status
        self._activity = activity
        self._additional_owner_ids = additional_owner_ids
        self._gateway_url = ''
        self._gateway_time = -inf
        self._gateway_max_concurrency = 1
        self._gateway_requesting = False
        self._gateway_waiter = None
        self._user_chunker_nonce= 0
        self.group_channels = {}
        self.private_channels = {}
        self.voice_clients = {}
        self.guilds = set()
        self.id = client_id
        self.ready_state = None
        self.application = application
        self.gateway = (DiscordGatewaySharder if shard_count else DiscordGateway)(self)
        self.http = DiscordHTTPClient(self, debug_options=processed_http_debug_options)
        self.events = EventHandlerManager(self)
        
        if (processable is not None):
            for item in processable:
                setattr(self, *item)
        
        if client_id > AUTO_CLIENT_ID_LIMIT:
            _check_is_client_duped(self, client_id)
            self._maybe_replace_alter_ego()
        
        
        run_setup_functions(self, setup_functions, kwargs)

        
        CLIENTS[client_id] = self
        
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
        self.locale = parse_locale(data)
    
    
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
            for index in range(users):
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
    
    
    async def download_attachment(self, attachment):
        """
        Downloads an attachment object's file. This method always prefers the proxy url of the attachment if applicable.
        
        This method is a coroutine.
        
        Parameters
        ----------
        attachment : ``Attachment``, ``EmbedImage``
            The attachment object, which's file will be requested.
        
        Returns
        -------
        response_data : `bytes`
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If `attachment` was not given as ``Attachment`` nor ``EmbedImage``.
        """
        if __debug__:
            if not isinstance(attachment, (Attachment, EmbedImage)):
                raise AssertionError(
                    f'`attachment` can be `{Attachment.__name__}`, `{EmbedImage.__name__}`, got '
                    f'{attachment.__class__.__name__}; {attachment!r}.'
                )
        
        url = attachment.proxy_url
        if (url is None) or is_media_url(url):
           url = attachment.url
        
        async with self.http.get(url) as response:
            return (await response.read())
    
    
    async def client_edit(self, *, avatar=..., banner=..., banner_color=..., bio=..., name=..., # Generic
        password=..., new_password=..., email=..., house=... # User account only
    ):
        """
        Edits the client. Only the provided parameters will be changed. Every parameter what refers to a user
        account is not tested.
        
        This method is a coroutine.
        
        Parameters
        ----------
        avatar : `None`, `bytes-like`, Optional (Keyword only)
            An `'jpg'`, `'png'`, `'webp'` image's raw data. If the client is premium account, then it can be
            `'gif'` as well. By passing `None` you can remove the client's current avatar.
        
        banner : `None`, `bytes-like`, Optional (Keyword only)
            An `'jpg'`, `'png'`, `'webp'`, 'gif'` image's raw data. By passing `None` you can remove the client's
            current avatar.
        
        banner_color : `None`, ``Color``, `int`, Optional (Keyword only)
            The new banner color of the client. By passing it as `None` you can remove the client's current one.
        
        bio : `None`, `str`, Optional (Keyword only)
            The new bio of the client. By passing it as `None`, you can remove the client's current one.
        
        name : `str`, Optional (Keyword only)
            The client's new name.
        
        password : `str`, Optional (Keyword only)
            The actual password of the client.
        
        new_password : `str`, Optional (Keyword only)
            The client's new password.
        
        email : `str`, Optional (Keyword only)
            The client's new email.
        
        house : `int`, ``HypesquadHouse``, `None`, Optional (Keyword only)
            Remove or change the client's hypesquad house.
        
        Raises
        ------
        TypeError
            - If `avatar` was not given as `None`, neither as `bytes-like`.
            - If `house` was not given as `int`  neither as ``HypesquadHouse``.
            - If `banner` was not given as `None`, neither as `bytes-like`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `name` was given but not as `str`.
            - If `name`'s length is out of range [2:32].
            - If `avatar`'s type in unsettable for the client.
            - If `password` was not given meanwhile the client is not bot.
            - If `password` was not given as `str`.
            - If `email` was given, but not as `str`.
            - If `new_password` was given, but not as `str`.
            - If `bio` is neither `None` nor `str`.
            - If `bio`'s length is out of range [0:190].
            - if `banner_color` is neither `None` nor `int`.
        
        Notes
        -----
        The method's endpoint has long rate limit reset, so consider using timeout and checking rate limits with
        ``RateLimitProxy``.
        
        The `password`, `new_password`, `email` and the `house` parameters are only for user accounts.
        """
        data = {}
        
        
        if (avatar is not ...):
            if avatar is None:
                avatar_data = None
            else:
                if not isinstance(avatar, (bytes, bytearray, memoryview)):
                    raise TypeError(
                        f'`avatar` can be `None`, `bytes-like`, got {avatar.__class__.__name__}; '
                        f'{reprlib.repr(avatar)}.'
                    )
                
                if __debug__:
                    media_type = get_image_media_type(avatar)
                    
                    if self.premium_type.value:
                        valid_icon_media_types = VALID_ICON_MEDIA_TYPES_EXTENDED
                    else:
                        valid_icon_media_types = VALID_ICON_MEDIA_TYPES
                    
                    if media_type not in valid_icon_media_types:
                        raise AssertionError(
                            f'Invalid `avatar` type for the client: {media_type}; got {reprlib.repr(avatar)}.'
                        )
                
                avatar_data = image_to_base64(avatar)
            
            data['avatar'] = avatar_data
        
        
        if (banner is not ...):
            if banner is None:
                banner_data = None
            else:
                if not isinstance(banner, (bytes, bytearray, memoryview)):
                    raise TypeError(
                        f'`banner` can be `None`, `bytes-like`, got {banner.__class__.__name__}; '
                        f'{reprlib.repr(banner)}.'
                    )
                
                if __debug__:
                    media_type = get_image_media_type(banner)
                    
                    if media_type not in VALID_ICON_MEDIA_TYPES_EXTENDED:
                        raise AssertionError(
                            f'Invalid `banner` type for the client: {media_type}; got {reprlib.repr(banner)}.'
                        )
                
                banner_data = image_to_base64(banner)
            
            data['banner'] = banner_data
        
        
        if (banner_color is not ...):
            if __debug__:
                if (banner_color is not None) and (not isinstance(banner_color, int)):
                    raise AssertionError(
                        f'`banner_color` can be `None`, `{Color.__name__}`, `int`, got '
                        f'{banner_color.__name__}; {banner_color!r}.'
                    )
            
            data['accent_color'] = banner_color
        
        
        if (bio is not ...):
            if bio is None:
                bio = ''
            else:
                if __debug__:
                    if not isinstance(bio, str):
                        raise AssertionError(
                            f'`bio` can be `None`, `str`, got {bio.__class__.__name__}; {bio!r}.'
                        )
                    
                    bio_length = len(bio)
                    if bio_length > 190:
                        raise AssertionError(
                            f'`bio` length can be in range [0:190], got {bio_length!r}; {bio!r}.'
                        )
            
            data['bio'] = bio
        
        
        if (name is not ...):
            if __debug__:
                if not isinstance(name, str):
                    raise AssertionError(
                        f'`name` can be `str`, got {name.__class__.__name__}; {name!r}.'
                    )
                
                name_length = len(name)
                if name_length < 2 or name_length > 32:
                    raise AssertionError(
                        f'The length of the name can be in range [2:32], got {name_length}; {name!r}.'
                    )
            
            data['username'] = name
        
        
        if not self.is_bot:
            if __debug__:
                if password is ...:
                    raise AssertionError(
                        f'`password` is must for non bots, got {password!r}.'
                    )
                
                if not isinstance(password, str):
                    raise AssertionError(
                        f'`password` can be `str`, got {password.__class__.__name__}; {password!r}.'
                    )
            
            data['password'] = password
            
            
            if (email is not ...):
                if __debug__:
                    if not isinstance(email, str):
                        raise AssertionError(
                            f'`email` can be `str`, got {email.__class__.__name__}; {email!r}.'
                        )
                
                data['email'] = email
            
            
            if (new_password is not ...):
                if __debug__:
                    if not isinstance(new_password, str):
                        raise AssertionError(
                            f'`new_password` can be `str`, got {new_password.__class__.__name__}; '
                            f'{new_password!r}.'
                        )
                
                data['new_password'] = new_password
            
            
            if house is not ...:
                if house is None:
                    await self.hypesquad_house_leave()
                else:
                    await self.hypesquad_house_change(house)
        
        
        data = await self.http.client_edit(data)
        self._set_attributes(data)
        
        
        if not self.is_bot:
            self.email = data['email']
            try:
                token = data['token']
            except KeyError:
                pass
            else:
                self.token = token
    
    
    async def client_guild_profile_edit(self, guild, *, nick=..., avatar=..., timed_out_until=..., reason=None):
        """
        Edits the client guild profile in the given guild. Nick and guild specific avatars can be edited on this way.
        
        An extra `reason` is accepted as well, which will show up at the respective guild's audit logs.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : `None`, `int`, ``Guild``
            The guild where the client's nickname will be changed. If `guild` is given as `None`, then the function
            returns instantly.
        nick : `None`, `str`, Optional (Keyword only)
            The client's new nickname. Pass it as `None` to remove it. Empty strings are interpreted as `None`.
        avatar : `None`, `bytes-like`, Optional (Keyword only)
            The client's new guild specific avatar.
            
            Can be a `'jpg'`, `'png'`, `'webp'` image's raw data. If the client is premium account, then it can be
            `'gif'` as well. By passing `None` you can remove the client's current avatar.
        
        timed_out_until : `None`, `datetime`, Optional (Keyword only)
            Till when the client is timed out. Pass it as `None` to remove it.
        
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Will show up at the respective guild's audit logs.
        
        Raises
        ------
        TypeError
            - `guild` was not given neither as ``Guild``, `int`.
            - If `avatar` is neither `None` nor `bytes-like`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If the nick's length is out of range [1:32].
            - If the nick was not given neither as `None`, `str`.
            - If `avatar`'s type is incorrect.
            - If `timed_out_until` is neither `None` nor `datetime`.
        """
        # Security debug checks.
        if __debug__:
            if (nick is not None):
                if not isinstance(nick, str):
                    raise AssertionError(
                        f'`nick` can be `None`, `str`, got {nick.__class__.__name__}; {nick!r}.'
                    )
                
                nick_length = len(nick)
                if nick_length > 32:
                    raise AssertionError(
                        f'`nick` length can be in range [1:32], got {nick_length}; {nick!r}.'
                    )
                
                # Translate empty nick to `None`
                if nick_length == 0:
                    nick = None
        else:
            # Non debug mode: Translate empty nick to `None`
            if (nick is not None) and (not nick):
                nick = None
        
        
        # Check whether we should edit the nick.
        if guild is None:
            # `guild` can be `None` if `guild` parameter was given as `int`.
            should_edit_nick = True
        else:
            try:
                guild_profile = self.guild_profiles[guild.id]
            except KeyError:
                # we aren't at the guild probably ->  will raise the request for us, if really
                should_edit_nick = True
            else:
                should_edit_nick = (guild_profile.nick != nick)
        
        data = {}
        
        if should_edit_nick:
            data['nick'] = nick
        
        if (avatar is not ...):
            if avatar is None:
                avatar_data = None
            else:
                if not isinstance(avatar, (bytes, bytearray, memoryview)):
                    raise TypeError(
                        f'`avatar` can be `None`, `bytes-like`, got {avatar.__class__.__name__}; '
                        f'{reprlib.repr(avatar)}.'
                    )
                
                if __debug__:
                    media_type = get_image_media_type(avatar)
                    
                    if self.premium_type.value:
                        valid_icon_media_types = VALID_ICON_MEDIA_TYPES_EXTENDED
                    else:
                        valid_icon_media_types = VALID_ICON_MEDIA_TYPES
                    
                    if media_type not in valid_icon_media_types:
                        raise AssertionError(
                            f'Invalid `avatar` type for the client: {media_type}, got {reprlib.repr(avatar)}.'
                        )
                
                avatar_data = image_to_base64(avatar)
            
            data['avatar'] = avatar_data
        
        if (timed_out_until is not ...):
            if timed_out_until is None:
                timed_out_until_raw = None
            else:
                if __debug__:
                    if not isinstance(timed_out_until, datetime):
                        raise AssertionError(
                            f'`timed_out_until` can be `None`, `datetime`, got {timed_out_until.__class__.__name__}; '
                            f'{timed_out_until!r}.'
                        )
                
                timed_out_until_raw = datetime_to_timestamp(timed_out_until)
            
            data['communication_disabled_until'] = timed_out_until_raw
        
        if data:
            await self.http.client_guild_profile_edit(guild_id, data, reason)
    
    
    async def client_connection_get_all(self):
        """
        Requests the client's connections.
        
        This method is a coroutine.
        
        Returns
        -------
        connections : `list` of ``Connection`` objects
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        For a bot account this request will always return an empty list.
        """
        data = await self.http.client_connection_get_all()
        return [Connection(connection_data) for connection_data in data]
    
    
    async def edit_presence(self, **kwargs):
        """
        Changes the client's presence (status and activity). If a parameter is not defined, it will not be changed.
        
        This method is a coroutine.
        
        Parameters
        ----------
        activity : ``ActivityBase``, Optional (Keyword only)
            The new activity of the Client.
        status : `str`, ``Status``, Optional (Keyword only)
            The new status of the client.
        afk : `bool` = `False`, Optional (Keyword only)
            Whether the client is afk or not (?).
        
        Raises
        ------
        TypeError:
            - If the status is not `str`, ``Status``.
            - If activity is not ``ActivityBase``, except ``ActivityCustom``.
        ValueError:
            - If the status `str`, but not any of the predefined ones.
        AssertionError
            - If `afk` was not given as `bool`.
        
        Notes
        -----
        This method is an alternative version of ``.client_edit_presence`` till further decision.
        """
        return await self.client_edit_presence(**kwargs)
    
    
    async def client_edit_presence(self, *, activity=..., status=..., afk=False):
        """
        Changes the client's presence (status and activity). If a parameter is not defined, it will not be changed.
        
        This method is a coroutine.
        
        Parameters
        ----------
        activity : ``ActivityBase``, Optional (Keyword only)
            The new activity of the Client.
        status : `str`, ``Status``, Optional (Keyword only)
            The new status of the client.
        afk : `bool` = `False`, Optional (Keyword only)
            Whether the client is afk or not (?).
        
        Raises
        ------
        TypeError:
            - If the status is not `str`, ``Status``.
            - If activity is not ``ActivityBase``, except ``ActivityCustom``.
        ValueError:
            - If the status `str`, but not any of the predefined ones.
        AssertionError
            - If `afk` was not given as `bool`.
        """
        if status is ...:
            status = self._status
        else:
            status = preconvert_preinstanced_type(status, 'status', Status)
            self._status = status
        
        status = status.value
        
        if activity is ...:
            activity = self._activity
        elif activity is None:
            self._activity = ACTIVITY_UNKNOWN
        elif isinstance(activity, ActivityBase) and (not isinstance(activity, ActivityCustom)):
            self._activity = activity
        else:
            raise TypeError(
                f'`activity` can be `{ActivityBase.__name__}` (except `{ActivityCustom.__name__}`), got: '
                f'{activity.__class__.__name__}; {activity!r}.'
            )
        
        if activity is None:
            pass
        elif activity is ACTIVITY_UNKNOWN:
            activity = None
        else:
            if self.is_bot:
                activity = activity.bot_dict()
            else:
                activity = activity.user_dict()
        
        if status == 'idle':
            since = int(time_now() * 1000.)
        else:
            since = 0
        
        if __debug__:
            if not isinstance(afk, bool):
                raise AssertionError(
                    f'`afk` can be `bool`, got {afk.__class__.__name__}; {afk!r}.'
                )
        
        data = {
            'op': GATEWAY_OPERATION_CODE_PRESENCE,
            'd': {
                'game': activity,
                'since': since,
                'status': status,
                'afk': afk,
            },
        }
        
        await self.gateway.send_as_json(data)
    
    
    async def activate_authorization_code(self, redirect_url, code, scopes):
        """
        Activates a user's oauth2 code.
        
        This method is a coroutine.
        
        Parameters
        ----------
        redirect_url : `str`
            The url, where the activation page redirected to.
        code : `str`
            The code, what is included with the redirect url after a successful activation.
        scopes : `str`, `list` of `str`
            Scope or a  list of oauth2 scopes to request.
        
        Returns
        -------
        access : ``OA2Access``, `None`
            If the code, the redirect url or the scopes are invalid, the methods returns `None`.
        
        Raises
        ------
        TypeError
            If `Scopes` wasn't neither as `str` not `list` of `str`s.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `redirect_url` was not given as `str`.
            - If `code` was not given as `str`.
            - If `scopes` is empty.
            - If `scopes` contains empty string.
        
        See Also
        --------
        ``parse_oauth2_redirect_url`` : Parses `redirect_url` and the `code` from a full url.
        """
        if __debug__:
            if not isinstance(redirect_url, str):
                raise AssertionError(
                    f'`redirect_url` can be `str`, got {redirect_url.__class__.__name__}; {redirect_url!r}.'
                )
            
            if not isinstance(code, str):
                raise AssertionError(
                    f'`code` can be `str`, got {code.__class__.__name__}; {code!r}.'
                )
        
        if isinstance(scopes, str):
            if __debug__:
                if not scopes:
                    raise AssertionError(
                        f'`scopes` cannot be empty, got {scopes!r}.'
                    )
        
        elif isinstance(scopes, list):
            if __debug__:
                if not scopes:
                    raise AssertionError(
                        f'`scopes` cannot be empty, got {scopes!r}.'
                    )
                
                for index, scope in enumerate(scopes):
                    if not isinstance(scope, str):
                        raise AssertionError(
                            f'`scopes` element `{index}` is not `str`, got '
                            f'{scope.__class__.__name__}; {scope!r}; scopes={scopes!r}.'
                        )
                    
                    if not scope:
                        raise AssertionError(
                            f'`scopes` element `{index}` is an empty string; got {scopes!r}.'
                        )
            
            scopes = ' '.join(scopes)
        
        else:
            raise TypeError(
                f'`scopes` can be `str`, `list` of `str`, got {scopes.__class__.__name__}; {scopes!r}.'
            )
        
        data = {
            'client_id': self.id,
            'client_secret': self.secret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_url,
            'scope': scopes,
        }
        
        data = await self.http.oauth2_token(data, IgnoreCaseMultiValueDictionary())
        if len(data) == 1:
            return
        
        return OA2Access(data, redirect_url)
    
    
    async def owners_access(self, scopes):
        """
        Similar to ``.activate_authorization_code``, but it requests the application's owner's access. It does not
        requires the redirect_url and the code parameter either.
        
        This method is a coroutine.
        
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
        TypeError
            If `Scopes` is neither `str` nor `list` of `str`s.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `redirect_url` was not given as `str`.
            - If `code` was not given as `str`.
            - If `scopes` is empty.
            - If `scopes` contains empty string.
        
        Notes
        -----
        Does not work if the client's application is owned by a team.
        """
        if isinstance(scopes, str):
            if __debug__:
                if not scopes:
                    raise AssertionError(
                        f'`scopes` cannot be empty, got {scopes!r}.'
                    )
        
        elif isinstance(scopes, list):
            if __debug__:
                if not scopes:
                    raise AssertionError(
                        f'`scopes` cannot be empty, got {scopes!r}.'
                    )
                
                for index, scope in enumerate(scopes):
                    if not isinstance(scope, str):
                        raise AssertionError(
                            f'`scopes` element `{index}` is not `str`, got '
                            f'{scope.__class__.__name__}; {scope!r}; scopes={scopes!r}.'
                        )
                    
                    if not scope:
                        raise AssertionError(
                            f'`scopes` element `{index}` is an empty string; got {scopes!r}.'
                        )
            
            scopes = ' '.join(scopes)
        
        else:
            raise TypeError(
                f'`scopes` can be `str`, `list` of `str`, got {scopes.__class__.__name__}; {scopes!r}.'
            )
        
        data = {
            'grant_type': 'client_credentials',
            'scope': scopes,
        }
        
        headers = IgnoreCaseMultiValueDictionary()
        headers[AUTHORIZATION] = BasicAuth(str(self.id), self.secret).encode()
        data = await self.http.oauth2_token(data, headers)
        return OA2Access(data, '')
    
    
    async def user_info_get(self, access):
        """
        Request the a user's information with oauth2 access token. By default a bot account should be able to request
        every public information about a user (but you do not need oauth2 for that). If the access token has email
        or/and identify scopes, then more information should show up like this.
        
        This method is a coroutine.
        
        Parameters
        ----------
        access : ``OA2Access``, ``UserOA2``, `str`
            Oauth2 access to the respective user or it's access token.
        
        Returns
        -------
        oauth2_user : ``UserOA2``
            The requested user object.
        
        Raises
        ------
        TypeError
            If `access` was not given neither as ``OA2Access``, ``UserOA2``  or `str`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        Needs `'email'` or / and `'identify'` scopes granted for more data
        """
        if isinstance(access, (OA2Access, UserOA2)):
            access_token = access.access_token
        elif isinstance(access, str):
            access_token = access
        else:
            raise TypeError(
                f'`access` can be `{OA2Access.__name__}`, `{UserOA2.__name__}`, `str`, got '
                f'{access.__class__.__name__}; {access!r}.'
            )
        
        headers = IgnoreCaseMultiValueDictionary()
        headers[AUTHORIZATION] = f'Bearer {access_token}'
        data = await self.http.user_info_get(headers)
        return UserOA2(data, access)
        
    
    async def user_connection_get_all(self, access):
        """
        Requests a user's connections. This method will work only if the access token has the `'connections'` scope. At
        the returned list includes the user's hidden connections as well.
        
        This method is a coroutine.
        
        Parameters
        ----------
        access : ``OA2Access``, ``UserOA2``, `str`
            Oauth2 access to the respective user or it's access token.
        
        Returns
        -------
        connections : `list` of ``Connection``
            The user's connections.
        
        Raises
        ------
        TypeError
            If `access` was not given neither as ``OA2Access``, ``UserOA2``  or `str`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If the given `access` not grants `'connections'` scope.
        """
        if isinstance(access, (OA2Access, UserOA2)):
            if __debug__:
                if 'connections' not in access.scopes:
                    raise AssertionError(
                        f'The given `access` not grants `\'connections\'` scope, what is required, '
                        f'got {access!r}.'
                    )
            
            access_token = access.access_token
        elif isinstance(access, str):
            access_token = access
        else:
            raise TypeError(
                f'`access` can be `{OA2Access.__name__}`, `{UserOA2.__name__}`, `str`'
                f', got {access.__class__.__name__}; {access!r}.'
            )
        
        headers = IgnoreCaseMultiValueDictionary()
        headers[AUTHORIZATION] = f'Bearer {access_token}'
        data = await self.http.user_connection_get_all(headers)
        return [Connection(connection_data) for connection_data in data]
    
    
    async def renew_access_token(self, access):
        """
        Renews the access token of an ``OA2Access``.
        
        This method is a coroutine.
        
        Parameters
        ----------
        access : ``OA2Access``, ``UserOA2``
            Oauth2 access to the respective user.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If `access` was not given neither as ``OA2Access``, ``UserOA2``.
        
        Notes
        -----
        By default access tokens expire after one week.
        """
        if __debug__:
            if not isinstance(access, (OA2Access, UserOA2)):
                raise AssertionError(
                    f'`access` can be `{OA2Access.__name__}`, `{UserOA2.__name__}`'
                    f', got {access.__class__.__name__}; {access!r}.'
                )
        
        redirect_url = access.redirect_url
        if redirect_url:
            data = {
                'client_id': self.id,
                'client_secret': self.secret,
                'grant_type': 'refresh_token',
                'refresh_token': access.refresh_token,
                'redirect_uri': redirect_url,
                'scope': ' '.join(access.scopes)
            }
        else:
            data = {
                'client_id': self.id,
                'client_secret': self.secret,
                'grant_type': 'client_credentials',
                'scope': ' '.join(access.scopes),
            }
        
        data = await self.http.oauth2_token(data, IgnoreCaseMultiValueDictionary())
        
        access._renew(data)
    
    
    async def guild_user_add(self, guild, access, user=None, *, nick=None, roles=None, mute=False, deaf=False):
        """
        Adds the passed to the guild. The user must have granted you the `'guilds.join'` oauth2 scope.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, where the user is going to be added.
        
        access: ``OA2Access``, ``UserOA2``, `str`
            The access of the user, who will be added.
        
        user : `None`, ```ClientUserBase`` = `None`, `int`, Optional
            Defines which user will be added to the guild. The `access` must refer to this specified user.
            
            This field is optional if access is passed as an ``UserOA2`` object.
        
        nick : `None`, `str` = `None`, Optional (Keyword only)
            The nickname, which with the user will be added.
        
        roles : `None`, `list` of (``Role``, `int`) = `None`, Optional (Keyword only)
            The roles to add the user with.
        
        mute : `bool` = `False`, Optional (Keyword only)
            Whether the user should be added as muted.
        
        deaf : `bool` = `False`, Optional (Keyword only)
            Whether the user should be added as deafen.
        
        Raises
        ------
        TypeError:
            - If `user` was not given neither as `None`, ``ClientUserBase``, `int`.
            - If `user` was passed as `None` and `access` was passed as ``OA2Access``, `str`.
            - If `access` was not given as ``OA2Access``, ``UserOA2``, nether as `str`.
            - If the given `access` not grants `'guilds.join'` scope.
            - If `guild` was not given neither as ``Guild``, not `int`.
            - If `roles` contain not ``Role``, nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `user` and `access` refers to a different user.
            - If the nick's length is over `32`.
            - If the nick was not given neither as `None`, `str`.
            - If `mute` was not given as `bool`.
            - If `deaf` was not given as `bool`.
            - If `roles` was not given neither as `None`, `list`.
        """
        user_id = get_user_id_nullable(user)
        
        
        if isinstance(access, OA2Access):
            access_token = access.access_token
            
            if __debug__:
                if 'guilds.join' not in access.scopes:
                    raise AssertionError(
                        f'The given `access` not grants `\'guilds.join\'` scope, what is required, '
                        f'got {access!r}.'
                    )
        
        elif isinstance(access, UserOA2):
            access_token = access.access_token
            if __debug__:
                if 'guilds.join' not in access.scopes:
                    raise AssertionError(
                        f'The given `access` not grants `\'guilds.join\'` scope, what is required, '
                        f'got access={access!r}, scopes={access.scopes!r}.'
                    )
                
                if user_id and (user_id != access.id):
                    raise AssertionError(
                        f'The given `user` and `access` refers to different users, got user={user!r}, '
                        f'access={access!r}.'
                    )
            
            user_id = access.id
        
        elif isinstance(access, str):
            access_token = access
        
        else:
            raise TypeError(
                f'`access` can be `{OA2Access.__name__}`, `{UserOA2.__name__}`, `str`, got '
                f'{access.__class__.__name__}; {access!r}.'
            )
        
        
        if not user_id:
            raise TypeError(
                f'`user` was not detectable neither from `user` nor from `access` parameters, got '
                f'user={user!r}, access={access!r}.'
            )
        
        
        guild_id = get_guild_id(guild)
        
        
        data = {'access_token': access_token}
        
        
        # Security debug checks.
        if __debug__:
            if (nick is not None):
                if not isinstance(nick, str):
                    raise AssertionError(
                        f'`nick` can be `None`, `str`, got {nick.__class__.__name__}; {nick!r}.'
                    )
                
                nick_length = len(nick)
                if nick_length > 32:
                    raise AssertionError(
                        f'`nick` length can be in range [0:32], got {nick_length}; {nick!r}.'
                    )
        
        if (nick is not None) and nick:
            data['nick'] = nick
        
        
        if (roles is not None):
            if __debug__:
                if not isinstance(roles, list):
                    raise AssertionError(
                        f'`roles` can be `list` of (`{Role.__name__}`, `int`), got '
                        f'{roles.__class__.__name__}; {roles!r}.'
                    )
            
            if roles:
                role_ids = set()
                
                for index, role in enumerate(roles):
                    if isinstance(role, Role):
                        role_id = role.id
                    else:
                        role_id = maybe_snowflake(role)
                        if role_id is None:
                            raise TypeError(
                                f'`roles[{index}]` is neither `{Role.__name__}`, `int`, got '
                                f'{role.__class__.__name__}; {role!r}; roles={roles!r}.'
                            )
                    
                    role_ids.add(role_id)
                
                data['roles'] = role_ids
        
        
        if __debug__:
            if not isinstance(mute, bool):
                raise AssertionError(
                    f'`mute` can be `bool`, got {mute.__class__.__name__}; {mute!r}.'
                )
        
        if mute:
            data['mute'] = mute
        
        
        if __debug__:
            if not isinstance(deaf, bool):
                raise AssertionError(
                    f'`deaf` can be `bool`, got {deaf.__class__.__name__}; {deaf!r}.'
                )
        
        if deaf:
            data['deaf'] = deaf
        
        
        await self.http.guild_user_add(guild_id, user_id, data)
    
    
    async def user_guild_get_all(self, access):
        """
        Requests a user's guilds with it's ``OA2Access``. The user must provide the `'guilds'` oauth2  scope for this
        request to succeed.
        
        This method is a coroutine.
        
        Parameters
        ----------
        access: ``OA2Access``, ``UserOA2``, `str`
            The access of the user, who's guilds will be requested.
        
        Returns
        -------
        guilds_and_permissions : `list` of `tuple` (``Guild``, ``UserGuildPermission``)
            The guilds and the user's permissions in each of them. Not loaded guilds will show up as partial ones.
        
        Raises
        ------
        TypeError
            If `access` was not given neither as ``OA2Access``, ``UserOA2``  or `str`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If the given `access` not grants `'guilds'` scope.
        """
        if isinstance(access, (OA2Access, UserOA2)):
            if __debug__:
                if 'connections' not in access.scopes:
                    raise AssertionError(
                        f'The given `access` not grants `\'guilds\'` scope, what is required, '
                        f'got {access!r}.'
                    )
            
            access_token = access.access_token
        elif isinstance(access, str):
            access_token = access
        else:
            raise TypeError(
                f'`access` can be `{OA2Access.__name__}`, `{UserOA2.__name__}` `str`'
                f', got {access.__class__.__name__}; {access!r}.'
            )
        
        headers = IgnoreCaseMultiValueDictionary()
        headers[AUTHORIZATION] = f'Bearer {access_token}'
        data = await self.http.user_guild_get_all(headers)
        return [(create_partial_guild_from_data(guild_data), UserGuildPermission(guild_data)) for guild_data in data]
    
    
    async def achievement_get_all(self):
        """
        Requests all the achievements of the client's application and returns them.
        
        This method is a coroutine.
        
        Returns
        -------
        achievements : `list` of ``Achievement`` objects
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        data = await self.http.achievement_get_all(self.application.id)
        return [Achievement(achievement_data) for achievement_data in data]
    
    
    async def achievement_get(self, achievement_id):
        """
        Requests one of the client's achievements by it's id.
        
        This method is a coroutine.
        
        Parameters
        ----------
        achievement_id : `int`
            The achievement's id.
        
        Returns
        -------
        achievement : ``Achievement``
        
        Raises
        ------
        TypeError
            If `achievement_id` was not given as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        achievement_id_c = maybe_snowflake(achievement_id)
        if achievement_id_c is None:
            raise TypeError(
                f'`achievement_id` can be `int`, got {achievement_id.__class__.__name__}; {achievement_id!r}.'
            )
        
        data = await self.http.achievement_get(self.application.id, achievement_id_c)
        return Achievement(data)
    
    
    async def achievement_create(self, name, description, icon, *, secret=False, secure=False):
        """
        Creates an achievement for the client's application and returns it.
        
        This method is a coroutine.
        
        Parameters
        ----------
        name : `str`
            The achievement's name.
        description : `str`
            The achievement's description.
        icon : `bytes-like`
            The achievement's icon. Can have `'jpg'`, `'png'`, `'webp'`, `'gif'` format.
        secret : `bool` = `False`, Optional (Keyword only)
            Secret achievements will *not* be shown to the user until they've unlocked them.
        secure : `bool` = `False`, Optional (Keyword only)
            Secure achievements can only be set via HTTP calls from your server, not by a game client using the SDK.
        
        Returns
        -------
        achievement : ``Achievement``
            The created achievement entity.
        
        Raises
        ------
        TypeError
            If `icon` was not passed as `bytes-like`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If the `icon`'s format is not any of the expected ones.
            - If `name` was not given as `str`.
            - If `description` was not given as `str`.
            - If `secret` was not given as `bool`.
            - If `secure` was not given as `bool`.
        """
        if __debug__:
            if not isinstance(name, str):
                raise AssertionError(
                    f'`name` can be `str`, got {name.__class__.__name__}; {name!r}.'
                )
            
            if not isinstance(description, str):
                raise AssertionError(
                    f'`description` can be `str`, got {description.__class__.__name__}; {description!r}.'
                )
        
        if not isinstance(icon, (bytes, bytearray, memoryview)):
            raise TypeError(
                f'`icon` can be `bytes-like`, got {icon.__class__.__name__}; {reprlib.repr(icon)}.'
            )
        
        if __debug__:
            media_type = get_image_media_type(icon)
            if media_type not in VALID_ICON_MEDIA_TYPES_EXTENDED:
                raise AssertionError(
                    f'Invalid `icon` type for achievement: {media_type}; got {reprlibrepr(icon)}.'
                )
        
        icon_data = image_to_base64(icon)
        
        if __debug__:
            if not isinstance(secret, bool):
                raise AssertionError(
                    f'`secret` can be `bool`, got {secret.__class__.__name__}; {secret!r}.'
                )
            
            if not isinstance(secure, bool):
                raise AssertionError(
                    f'`secure` can be `bool`, got {secure.__class__.__name__}; {secure!r}.'
                )
        
        data = {
            'name' : {
                'default' : name,
            },
            'description' : {
                'default' : description,
            },
            'secret' : secret,
            'secure' : secure,
            'icon'   : icon_data,
        }
        
        data = await self.http.achievement_create(self.application.id, data)
        return Achievement(data)
    
    
    async def achievement_edit(self, achievement, *, name=..., description=..., secret=..., secure=..., icon=...):
        """
        Edits the passed achievement with the specified parameters. All parameter is optional.
        
        This method is a coroutine.
        
        Parameters
        ----------
        achievement : ``Achievement``, `int`
            The achievement, what will be edited.
        name : `str`, Optional (Keyword only)
            The new name of the achievement.
        description : `str`, Optional (Keyword only)
            The achievement's new description.
        secret : `bool`, Optional (Keyword only)
            The achievement's new secret value.
        secure : `bool`, Optional (Keyword only)
            The achievement's new secure value.
        icon : `bytes-like`, Optional (Keyword only)
            The achievement's new icon.
        
        Returns
        -------
        achievement : ``Achievement``
            After a successful edit, the passed achievement is updated and returned.
        
        Raises
        ------
        TypeError
            - If ``icon`` was not passed as `bytes-like`.
            - If `achievement` was not given neither as ``Achievement``, neither as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `name` was not given as `str`.
            - If `description` was not given as `str`.
            - If `secret` was not given as `bool`.
            - If `secure` was not given as `str`.
            - If `icon`'s format is not any of the expected ones.
        """
        achievement, achievement_id = get_achievement_and_id(achievement)
        
        data = {}
        
        if (name is not ...):
            if __debug__:
                if not isinstance(name, str):
                    raise AssertionError(
                        f'`name` can be `str`, got {name.__class__.__name__}; {name!r}.'
                    )
            
            data['name'] = {
                'default': name,
            }
        
        if (description is not ...):
            if __debug__:
                if not isinstance(description, str):
                    raise AssertionError(
                        f'`description` can be `str`, got {description.__class__.__name__}; {description!r}.'
                    )
            
            data['description'] = {
                'default': description,
            }
        
        if (secret is not ...):
            if __debug__:
                if not isinstance(secret, bool):
                    raise AssertionError(
                        f'`secret` can be `bool`, got {secret.__class__.__name__}; {secret!r}.'
                    )
            
            data['secret'] = secret
        
        if (secure is not ...):
            if __debug__:
                if not isinstance(secret, bool):
                    raise AssertionError(
                        f'`secure` can be `bool`, got {secure.__class__.__name__}; {secure!r}.'
                    )
            
            data['secure'] = secure
        
        if (icon is not ...):
            icon_type = icon.__class__
            if not isinstance(icon, (bytes, bytearray, memoryview)):
                raise TypeError(
                    f'`icon` can be `bytes-like`, got {icon_type.__name__}; {reprlib.repr(icon_type)}.'
                )
            
            if __debug__:
                media_type = get_image_media_type(icon)
                if media_type not in VALID_ICON_MEDIA_TYPES_EXTENDED:
                    raise ValueError(
                        f'Invalid `icon` type for achievement: {media_type}; got {reprlib.repr(icon_type)!r}.'
                    )
            
            data['icon'] = image_to_base64(icon)
        
        data = await self.http.achievement_edit(self.application.id, achievement_id, data)
        if achievement is None:
            achievement = Achievement(data)
        else:
            achievement._update_attributes(data)
        return achievement
    
    
    async def achievement_delete(self, achievement):
        """
        Deletes the passed achievement.
        
        This method is a coroutine.
        
        Parameters
        ----------
        achievement : ``Achievement``, `int`
            The achievement to delete.
        
        Raises
        ------
        TypeError
            If `achievement` was not given neither as ``Achievement``, neither as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        achievement_id = get_achievement_id(achievement)
        
        await self.http.achievement_delete(self.application.id, achievement_id)
    
    
    async def user_achievement_get_all(self, access):
        """
        Requests the achievements of a user with it's oauth2 access.
        
        This method is a coroutine.
        
        Parameters
        ----------
        access : ``OA2Access``, ``UserOA2``, `str`.
            The access of the user, who's achievements will be requested.
        
        Returns
        -------
        achievements : `list` of ``Achievement`` objects
        
        Raises
        ------
        TypeError
            If `access` was not given neither as ``OA2Access``, ``UserOA2``  or `str`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        This endpoint is unintentionally documented and will never work. For reference:
        ``https://github.com/discordapp/discord-api-docs/issues/1230``.
        
        Always drops `DiscordException UNAUTHORIZED (401): 401: Unauthorized`.
        """
        if isinstance(access, (OA2Access, UserOA2)):
            access_token = access.access_token
        elif isinstance(access, str):
            access_token = access
        else:
            raise TypeError(
                f'`access` can be `{OA2Access.__name__}`, `{UserOA2.__name__}`, `str`, got '
                f'{access.__class__.__name__}; {access!r}.'
            )
        
        
        headers = IgnoreCaseMultiValueDictionary()
        headers[AUTHORIZATION] = f'Bearer {access_token}'
        
        data = await self.http.user_achievement_get_all(self.application.id, headers)
        return [Achievement(achievement_data) for achievement_data in data]
    
    
    async def user_achievement_update(self, user, achievement, percent_complete):
        """
        Updates the `user`'s achievement with the given percentage. The  achievement should be `secure`. This
        method only updates the achievement's percentage.
        
        This method is a coroutine.
        
        Parameters
        ----------
        user : ``ClientUserBase``, `int`
            The user, who's achievement will be updated.
        achievement : ``Achievement``, `int`
            The achievement, which's state will be updated
        percent_complete : `int`
            The completion percentage of the achievement.
        
        Raises
        ------
        TypeError
            - If `user` was not given neither as ``ClientUserBase`` nor `int`.
            - If `achievement` was not given neither as ``Achievement``, neither as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `percent_complete` was not given as `int`.
            - If `percent_complete` is out of range [0:100].
        
        Notes
        -----
        This endpoint cannot grant achievement, but can it even update them?. For reference:
        ``https://github.com/discordapp/discord-api-docs/issues/1230``.
        
        Only secure updates are supported, if they are even.
        - When updating secure achievement: `DiscordException NOT FOUND (404), code=10029: Unknown Entitlement`
        - When updating non secure: `DiscordException FORBIDDEN (403), code=40001: Unauthorized`
        """
        user_id = get_user_id(user)
        
        achievement_id = get_achievement_id(achievement)
        
        if __debug__:
            if not isinstance(percent_complete, int):
                raise AssertionError(
                    f'`percent_complete` can be `int`, got {percent_complete.__class__.__name__}; {percent_complete!r}.'
                )
            
            if percent_complete < 0 or percent_complete > 100:
                raise AssertionError(
                    f'`percent_complete` is out of range [0:100], got {percent_complete!r}.'
                )
        
        data = {'percent_complete': percent_complete}
        await self.http.user_achievement_update(user_id, self.application.id, achievement_id, data)
    
    
    async def application_get(self, application):
        """
        Requests a specific application by it's id.
        
        This method is a coroutine.
        
        Parameters
        ----------
        application : ``Application``, `int`
            The application or it's identifier to request.
        
        Returns
        -------
        application : ``Application``
        
        Raises
        ------
        TypeError
            If `application` was not given neither as ``Application`` nor as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        This endpoint does not support bot accounts.
        """
        if isinstance(application, Application):
            application_id = application.id
        else:
            application_id = maybe_snowflake(application)
            if application_id is None:
                raise TypeError(
                    f'`application` can be `{Application.__name__}`, `int`, got '
                    f'{application.__class__.__name__}; {application!r}.'
                )
            
            application = APPLICATIONS.get(application_id, None)
            
        application_data = await self.http.application_get(application_id)
        if application is None:
            application = Application(application_data)
        else:
            application._update_attributes(application_data)
        
        return application
    
    async def eula_get(self, eula):
        """
        Requests the eula with the given id.
        
        This method is a coroutine.
        
        Parameters
        ----------
        eula : `int`
            The `id` of the eula to request.

        Returns
        -------
        eula : ``EULA``
        
        Raises
        ------
        TypeError
            If `eula` was not given neither as ``EULA`` not as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        if isinstance(eula, EULA):
            eula_id = eula.id
        else:
            eula_id = maybe_snowflake(eula)
            if eula_id is None:
                raise TypeError(
                    f'`eula` can be `{EULA.__name__}`, `int`, got {eula.__class__.__name__}; {eula!r}.'
                )
            
            eula = EULAS.get(eula_id, None)
        
        eula_data = await self.http.eula_get(eula_id)
        if eula is None:
            eula = EULA(eula_data)
        else:
            eula._update_attributes(eula_data)
        
        return eula
    
    
    async def application_get_all_detectable(self):
        """
        Requests the detectable applications
        
        This method is a coroutine.
        
        Returns
        -------
        applications : `list` of ``Application``
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        applications_data = await self.http.application_get_all_detectable()
        return [Application(application_data) for application_data in applications_data]
    
    
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
            
            break
        
        return data
    
    # channels
    
    async def channel_group_leave(self, channel):
        """
        Leaves the client from the specified group channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``ChannelGroup``, `int`
            The channel to leave from.
        
        Raises
        ------
        TypeError
            If `channel` was not given neither as ``ChannelGroup`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id = get_channel_id(channel, ChannelGroup)
        
        await self.http.channel_group_leave(channel_id)
    
    
    async def channel_group_user_add(self, channel, *users):
        """
        Adds the users to the given group channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``ChannelGroup``, `int`
            The channel to add the `users` to.
        *users : ``ClientUserBase``, `int`s
            The users to add to the `channel`.
        
        Raises
        ------
        TypeError
            - If `channel` was not given neither as ``ChannelGroup`` nor `int`.
            - If `users` contains non ``ClientUserBase``, neither `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id = get_channel_id(channel, ChannelGroup)
        
        user_ids = set()
        for user in users:
            user_id = get_user_id(user)
            user_ids.add(user_id)
        
        for user_id in user_ids:
            await self.http.channel_group_user_add(channel_id, user_id)
    
    
    async def channel_group_user_delete(self, channel, *users):
        """
        Removes the users from the given group channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : `ChannelGroup``, `int`
            The channel from where the `users` will be removed.
        *users : ``ClientUserBase``, `int`s
            The users to remove from the `channel`.
        
        Raises
        ------
        TypeError
            - If `channel` was not given neither as ``ChannelGroup`` nor `int`.
            - If `users` contains non ``ClientUserBase``, neither `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id = get_channel_id(channel, ChannelGroup)
        
        user_ids = set()
        for user in users:
            user_id = get_user_id(user)
            user_ids.add(user_id)
        
        for user_id in user_ids:
            await self.http.channel_group_user_delete(channel_id, user_id)
    
    
    async def channel_group_edit(self, channel, *, name=..., icon=...):
        """
        Edits the given group channel. Only the provided parameters will be edited.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``ChannelGroup``, `int`
            The channel to edit.
        name : `None`, `str`, Optional (Keyword only)
            The new name of the channel. By passing `None` or an empty string you can remove the actual one.
        icon : `None`, `bytes-like`, Optional (Keyword only)
            The new icon of the channel. By passing `None` your can remove the actual one.
        
        Raises
        ------
        TypeError
            - If `channel` was not given neither as ``ChannelGroup`` nor `int`.
            - If `name` is neither `None`, `str`.
            - If `icon` is neither `None`, `bytes-like`.
        ValueError
            - If `name` is passed as `str`, but it's length is `1`, or over `100`.
            - If `icon` is passed as `bytes-like`, but it's format is not any of the expected formats.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `name` was not given neither as `None`, `str`.
            - If `name`'s length is out of range `[1:100]`.
        Notes
        -----
        No request is done if no optional parameter is provided.
        """
        channel_id = get_channel_id(channel, ChannelGroup)
        
        data = {}
        
        if (name is not ...):
            if __debug__:
                if (name is not None):
                    if not isinstance(name, str):
                        raise AssertionError(
                            f'`name` can be `None`, `str`, got {name.__class__.__name__}; {name!r}.'
                        )
                    
                    name_length = len(name)
                    if (name_length < 1) or (name_length > 100):
                        raise AssertionError(
                            f'`name` length can be in range [1:100], got {name_length}; {name!r}.'
                        )
                    
                    # Translate empty nick to `None`
                    if name_length == 0:
                        name = None
            else:
                # Non debug mode: Translate empty nick to `None`
                if (name is not None) and (not name):
                    name = None
            
            data['name'] = name
        
        if (icon is not ...):
            if icon is None:
                icon_data = None
            else:
                icon_type = icon.__class__
                if not issubclass(icon_type, (bytes, bytearray, memoryview)):
                    raise TypeError(
                        f'`icon` can be `None`, `bytes-like`, got {icon_type.__name__}; {reprlib.repr(icon_type)}.'
                    )
            
                media_type = get_image_media_type(icon)
                if media_type not in VALID_ICON_MEDIA_TYPES:
                    raise ValueError(
                        f'Invalid `icon` type: {media_type}; got {reprlib.repr(icon_type)}.'
                    )
                
                icon_data = image_to_base64(icon)
            
            data['icon'] = icon_data
        
        if data:
            await self.http.channel_group_edit(channel_id, data)
    
    
    async def channel_group_create(self, *users):
        """
        Creates a group channel with the given users.
        
        This method is a coroutine.
        
        Parameters
        ----------
        *users : ``ClientUserBase``, `int`s
            The users to create the channel with.
        
        Returns
        -------
        channel : ``ChannelGroup``
            The created group channel.
        
        Raises
        ------
        TypeError
            If `users` contain not only ``User`, ``Client``, `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If the total amount of users is less than `2`.
        
        Notes
        -----
        This endpoint does not support bot accounts.
        """
        user_ids = set()
        for user in users:
            user_id = get_user_id(user)
            user_ids.add(user_id)
        
        user_ids.add(self.id)
        
        if __debug__:
            user_ids_length = len(user_ids)
            if user_ids_length < 2:
                raise AssertionError(
                    f'`{ChannelGroup.__name__}` can be created at least with at least `2` users,  got '
                    f'{user_ids_length}; {users!r}.'
                )
        
        data = {'recipients': user_ids}
        data = await self.http.channel_group_create(self.id, data)
        return ChannelGroup(data, self, 0)
    
    
    async def channel_private_create(self, user):
        """
        Creates a private channel with the given user. If there is an already cached private channel with the user,
        returns that.
        
        This method is a coroutine.
        
        Parameters
        ----------
        user : ``ClientUserBase``, `int`
            The user to create the private with.
        
        Returns
        -------
        channel : ``ChannelPrivate``
            The created private channel.
        
        Raises
        ------
        TypeError
            If `user` was not given neither as ``ClientUserBase`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        user_id = get_user_id(user)
        
        try:
            channel = self.private_channels[user_id]
        except KeyError:
            data = await self.http.channel_private_create({'recipient_id': user_id})
            channel = ChannelPrivate(data, self, 0)
        
        return channel
    
    
    async def channel_private_get_all(self):
        """
        Request the client's private + group channels and returns them in a list. At the case of bot accounts the
        request returns an empty list, so we skip it.
        
        This method is a coroutine.
        
        Returns
        -------
        channels : `list` of (``ChannelPrivate``, ``ChannelGroup``) objects
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channels = []
        if (not self.is_bot):
            data = await self.http.channel_private_get_all()
            for channel_data in data:
                channel = CHANNEL_TYPE_MAP.get(channel_data['type'], ChannelGuildUndefined)(channel_data, self, 0)
                channels.append(channel)
        
        return channels
    
    
    async def channel_move(self, channel, visual_position, *, parent=..., lock_permissions=False, reason=None):
        """
        Moves a guild channel to the given visual position under it's parent, or guild. If the algorithm can not
        place the channel exactly on that location, it will place it as close, as it can. If there is nothing to
        move, then the request is skipped.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``ChannelGuildMainBase``
            The channel to be moved.
        visual_position : `int`
            The visual position where the channel should go.
        parent : `None`, ``ChannelCategory``, Optional (Keyword only)
            If not set, then the channel will keep it's current parent. If the parameter is set ``Guild`` or to
            `None`, then the  channel will be moved under the guild itself, Or if passed as ``ChannelCategory``,
            then the channel will be moved under it.
        lock_permissions : `bool` = `False`, Optional (Keyword only)
            If you want to sync the permissions with the new category set it to `True`. Defaults to `False`.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        ValueError
            - If the `channel` would be between guilds.
            - If parent channel would be moved under an other category.
        TypeError
            - If `ChannelGuildBase` was not passed as ``ChannelGuildMainBase``.
            - If `parent` was not given as `None`, ``ChannelCategory``.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        This method also fixes the messy channel positions of Discord to an intuitive one.
        """
        # Check channel type
        if not isinstance(channel, ChannelGuildMainBase):
            raise TypeError(
                f'`channel` can be `{ChannelGuildMainBase.__name__}`, got {channel.__class__.__name__}; {channel!r}.'
            )
        
        # Check whether the channel is partial.
        guild = channel.guild
        if guild is None:
            # Cannot move partial channels, leave
            return
        
        # Check parent
        if parent is ...:
            parent = channel.parent
        elif parent is None:
            parent = None
        elif isinstance(parent, ChannelCategory):
            if parent.guild is not guild:
                raise ValueError(
                    f'Can not move channel between guilds! Channel\'s guild: {guild!r}; Category\'s '
                    f'guild: {parent.guild!r}'
                )
        else:
            raise TypeError(
                f'`parent` can be `None` or {ChannelCategory.__name__}`, got {parent.__class__.__name__}; {parent!r}.'
            )
        
        # Cannot put category under category
        if isinstance(channel, ChannelCategory) and isinstance(parent, ChannelCategory):
            raise ValueError(
                f'Can not move category channel under category channel. channel={channel!r}; parent={parent!r}'
            )
        
        if not isinstance(visual_position, int):
            raise TypeError(
                f'`visual_position` can be `int`, got {visual_position.__class__.__name__}; '
                f'{visual_position!r}.'
            )
        
        if not isinstance(lock_permissions, bool):
            raise TypeError(
                f'`lock_permissions` can be `bool`, got {lock_permissions.__class__.__name__}; {lock_permissions!r}.'
            )
        
        # Cap at 0
        if visual_position < 0:
            visual_position = 0
        
        # If the channel is where it should be, we can leave.
        if channel.parent is parent and parent.channel_list.index(channel) == visual_position:
            return
        
        # Create a display state, where each channel is listed.
        # Categories are inside of a tuple, where they are the first element of it and their channels are the second.
        display_state = guild.channel_list
        
        for index in range(len(display_state)):
            iter_channel = display_state[index]
            if isinstance(iter_channel, ChannelCategory):
                display_state[index] = iter_channel, iter_channel.channel_list
        
        # Generate a state where the channels are theoretically ordered with tuples
        display_new = []
        for iter_channel in display_state:
            if isinstance(iter_channel, tuple):
                iter_channel, sub_channels = iter_channel
                display_sub_channels = []
                for sub_channel in sub_channels:
                    channel_key = (sub_channel.ORDER_GROUP, sub_channel.position, sub_channel.id, None)
                    display_sub_channels.append(channel_key)
            else:
                display_sub_channels = None
            
            channel_key = (iter_channel.ORDER_GROUP, iter_channel.position, iter_channel.id, display_sub_channels)
            
            display_new.append(channel_key)
        
        # We have 2 display states, we will compare the old to the new one when calculating differences, but we didn't
        # move our channel yet!
        
        # We get from where we will move from.
        old_parent = channel.parent
        if isinstance(old_parent, Guild):
            move_from = display_new
        else:
            old_parent_id = old_parent.id
            for channel_key in display_new:
                if channel_key[2] == old_parent_id:
                    move_from = channel_key[3]
                    break
            
            else:
                # If no breaking was not done, our channel not exists, lol
                return
        
        # We got from which thing we will move from, so we remove first
        
        channel_id = channel.id
        
        for index in range(len(move_from)):
            channel_key = move_from[index]
            
            if channel_key[2] == channel_id:
                channel_key_to_move = channel_key
                del move_from[index]
                break
        
        else:
            # If breaking was not done, our channel not exists, lol
            return
        
        # We get to where we will move to.
        if parent is None:
            move_to = display_new
        else:
            new_parent_id = parent.id
            for channel_key in display_new:
                if channel_key[2] == new_parent_id:
                    move_to = channel_key[3]
                    break
            
            else:
                # If no breaking was not done, our channel not exists, lol
                return
        
        # Move, yayyy
        move_to.insert(visual_position, channel_key_to_move)
        # Reorder
        move_to.sort(key=channel_move_sort_key)
        
        # Now we resort every channel in the guild and categories, mostly for security issues
        to_sort_all = [display_new]
        for channel_key in display_new:
            display_sub_channels = channel_key[3]
            if display_sub_channels is not None:
                to_sort_all.append(display_sub_channels)
        
        ordered = []
        
        for to_sort in to_sort_all:
            expected_channel_order_group = 0
            channel_position = 0
            for sort_key in to_sort:
                channel_order_group = sort_key[0]
                channel_id = sort_key[2]
                
                if channel_order_group != expected_channel_order_group:
                    expected_channel_order_group = channel_order_group
                    channel_position = 0
                
                ordered.append((channel_position, channel_id))
                channel_position += 1
                continue
        
        bonus_data = {'lock_permissions': lock_permissions}
        if parent is None:
            parent_id = None
        else:
            parent_id = parent.id
        bonus_data['parent_id'] = parent_id
        
        data = []
        channels = guild.channels
        for position, channel_id in ordered:
            channel_ = channels[channel_id]
            
            if channel is channel_:
                data.append({'id': channel_id, 'position': position, **bonus_data})
                continue
            
            if channel_.position != position:
                data.append({'id': channel_id, 'position': position})
        
        await self.http.channel_move(guild.id, data, reason)
    
    
    async def channel_edit(self, channel, *, name=..., topic=..., nsfw=..., slowmode=..., user_limit=...,
            bitrate=..., region=..., video_quality_mode=..., type_=..., default_auto_archive_after=..., banner=...,
            reason=None):
        """
        Edits the given guild channel. Different channel types accept different parameters, so make sure to not pass
        out of place parameters. Only the passed parameters will be edited of the channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``ChannelGuildBase``, `int`
            The channel to edit.
        name : `str`, Optional (Keyword only)
            The `channel`'s new name.
        topic : `str`, Optional (Keyword only)
            The new topic of the `channel`.
        nsfw : `bool`, Optional (Keyword only)
            Whether the `channel` will be nsfw or not.
        slowmode : `int`, Optional (Keyword only)
            The new slowmode value of the `channel`.
        user_limit : `int`, Optional (Keyword only)
            The new user limit of the `channel`.
        bitrate : `int`, Optional (Keyword only)
            The new bitrate of the `channel`.
        type_ : `int`, Optional (Keyword only)
            The `channel`'s new type value.
        region : `None`, ``VoiceRegion``, `str`, Optional (Keyword only)
            The channel's new voice region.
            
            > By giving as `None`, you can remove the old value.
        video_quality_mode : ``VideoQualityMode``, `int`, Optional (Keyword only)
            The channel's new video quality mode.
        default_auto_archive_after : `None`, `int`, Optional (Keyword only)
            The default duration (in seconds) for newly created threads to automatically archive the themselves. Can be
            one of: `3600`, `86400`, `259200`, `604800`.
        banner : `None`, `bytes-like`, Optional (Keyword only)
             The new banner of the channel. Can be `'jpg'`, `'png'`, `'webp'` image's raw data. by passing it as
            `None`, you can remove the current one.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        TypeError
            - If the given `channel` is not ``ChannelGuildBase``, `int`.
            - If `region` was not given neither as `None`, `str` nor ``VoiceRegion``.
            - If `video_quality_mode` was not given neither as ``VideoQualityMode` nor as `int`.
        AssertionError
            - If `name` was not given as `str`.
            - If `name`'s length is out of range `[1:100]`.
            - If `topic` was not given as `str`.
            - If `topic`'s length is over `1024`, `120` depending on channel type.
            - If `topic` was given, but the given channel is not ``ChannelText`` nor ``ChannelStage``.
            - If `type_` was given, but the given channel is not ``ChannelText``.
            - If `type_` was not given as `int`.
            - If `type_` cannot be interchanged to the given value.
            - If `nsfw` was given meanwhile the channel is not ``ChannelText``, ``ChannelStore``.
            - If `nsfw` was not given as `bool`.
            - If `slowmode` was given, but the channel is not ``ChannelText``.
            - If `slowmode` was not given as `int`.
            - If `slowmode` was given, but it's value is less than `0` or greater than `21600`.
            - If `bitrate` was given, but the channel is not ``ChannelVoiceBase``.
            - If `bitrate` was not given as `int`.
            - If `bitrate`'s value is out of the expected range.
            - If `user_limit` was given, but the channel is not ``ChannelVoiceBase``.
            - If `user_limit` was not given as `int`.
            - If `user_limit` was given, but is out of the expected [0:99] range.
            - If `region` was given, but the respective channel type is not ``ChannelVoiceBase``.
            - If `video_quality_mode` was given,but the respective channel type is not ``ChannelVoice``
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel, channel_id = get_channel_and_id(channel, ChannelGuildBase)
        
        data = {}
        
        if (name is not ...):
            if __debug__:
                if not isinstance(name, str):
                    raise AssertionError(
                        f'`name` can be `str`, got {name.__class__.__name__}; {name!r}.'
                    )
                
                name_length = len(name)
                
                if name_length < 1 or name_length > 100:
                    raise AssertionError(
                        f'`name` length can be in range [1:100], got {name_length}; {name!r}.'
                    )
            
            data['name'] = name
        
        
        if (topic is not ...):
            if __debug__:
                if (channel is not None):
                    if not isinstance(channel, (ChannelText, ChannelStage)):
                        raise AssertionError(
                            f'`topic` is a valid parameter only for `{ChannelText.__name__}` and for '
                            f'`{ChannelStage.__name__}`, got {channel.__class__.__name__}; {channel!r}.'
                        )
                
                if not isinstance(topic, str):
                    raise AssertionError(
                        f'`topic` can be `str`, got {topic.__class__.__name__}; {topic!r}.'
                    )
                
                if channel is None:
                    topic_length_limit = 1024
                elif isinstance(channel, ChannelText):
                    topic_length_limit = 1024
                else:
                    topic_length_limit = 120
                
                topic_length = len(topic)
                
                if topic_length > topic_length_limit:
                    raise AssertionError(
                        f'`topic` length can be in range [0:{topic_length_limit}], got {topic_length}; {topic!r}.'
                    )
            
            data['topic'] = topic
        
        
        if (type_ is not ...):
            if __debug__:
                if (channel is not None):
                    if not isinstance(channel, ChannelText):
                        raise AssertionError(
                            f'`type_` is a valid parameter only for `{ChannelText.__name__}`-s'
                            f', got {channel.__class__.__name__}; {channel!r}.'
                        )
                
                if not isinstance(type_, int):
                    raise AssertionError(
                        f'`type_` can be `int`, got {type_.__class__.__name__}.; {type_!r}'
                    )
                
                if type_ not in ChannelText.INTERCHANGE:
                    raise AssertionError(
                        f'`type_` can be interchanged to `{ChannelText.INTERCHANGE}`, got {type_!r}.'
                    )
            
            data['type'] = type_
        
        
        if (nsfw is not ...):
            if __debug__:
                if (channel is not None):
                    if not isinstance(channel, (ChannelText, ChannelStore)):
                        raise AssertionError(
                            f'`nsfw` is a valid parameter only for `{ChannelText.__name__}` and '
                            f'`{ChannelStore.__name__}`, got {channel.__class__.__name__}; {channel!r}.'
                        )
                
                if not isinstance(nsfw, bool):
                    raise AssertionError(
                        f'`nsfw` can be `bool`, got {nsfw.__class__.__name__}; {nsfw!r}.'
                    )
            
            data['nsfw'] = nsfw
        
        
        if (slowmode is not ...):
            if __debug__:
                if (channel is not None):
                    if not isinstance(channel, ChannelText):
                        raise AssertionError(
                            f'`slowmode` is a valid parameter only for `{ChannelText.__name__}`-s'
                            f', got {channel.__class__.__name__}; {channel!r}.'
                        )
                
                if not isinstance(slowmode, int):
                    raise AssertionError(
                        f'`slowmode` can be `int`, got {slowmode.__class__.__name__}; {slowmode!r}.'
                    )
                
                if slowmode < 0 or slowmode > 21600:
                    raise AssertionError(
                        f'`slowmode` can be in range [0:21600], got {slowmode!r}.'
                    )
            
            data['rate_limit_per_user'] = slowmode
        
        
        if (bitrate is not ...):
            if __debug__:
                if (channel is not None):
                    if not isinstance(channel, ChannelVoiceBase):
                        raise AssertionError(
                            f'`bitrate` is a valid parameter only for `{ChannelVoiceBase.__name__}`-s'
                            f', got {channel.__class__.__name__}; {channel!r}.'
                        )
                    
                if not isinstance(bitrate, int):
                    raise AssertionError(
                        f'`bitrate` can be `int`, got {bitrate.__class__.__name__}; {bitrate!r}.'
                    )
                
                # Get max bitrate
                if channel is None:
                    bitrate_limit = 384000
                else:
                    guild = channel.guild
                    if guild is None:
                        bitrate_limit = 384000
                    else:
                        bitrate_limit = guild.bitrate_limit
                
                if bitrate < 8000 or bitrate > bitrate_limit:
                    raise AssertionError(
                        f'`bitrate` is out of the expected [8000:{bitrate_limit}] range, got {bitrate!r}.'
                    )
            
            data['bitrate'] = bitrate
        
        
        if (user_limit is not ...):
            if __debug__:
                if (channel is not None):
                    if not isinstance(channel, ChannelVoiceBase):
                        raise AssertionError(
                            f'`user_limit` is a valid parameter only for `{ChannelVoiceBase.__name__}`-s'
                            f', got {channel.__class__.__name__}; {channel!r}.'
                        )
                
                if user_limit < 0 or user_limit > 99:
                    raise AssertionError(
                        f'`user_limit`\'s value is out of the expected [0:99] range, got {user_limit!r}.'
                    )
            
            data['user_limit'] = user_limit
        
        
        if (region is not ...):
            if __debug__:
                if (channel is not None):
                    if not isinstance(channel, ChannelVoiceBase):
                        raise AssertionError(
                            f'`region` is a valid parameter only for `{ChannelVoiceBase.__name__}`-s'
                            f', got {channel.__class__.__name__}; {channel!r}.'
                        )
            
            if region is None:
                region_value = None
            elif isinstance(region, VoiceRegion):
                region_value = region.value
            elif isinstance(region, str):
                region_value = region
            else:
                raise TypeError(
                    f'`region` can be `None`, `str`, `{VoiceRegion.__name__}`, got {region.__class__.__name__}; '
                    f'{region!r}.'
                )
            
            data['rtc_region'] = region_value
        
        
        if (video_quality_mode is not ...):
            if __debug__:
                if (channel is not None):
                    if not isinstance(channel, ChannelVoice):
                        raise AssertionError(
                            f'`video_quality_mode` is a valid parameter only for `{ChannelVoice.__name__}`, '
                            f'got {channel.__class__.__name__}; {channel!r}.'
                        )
            
            if isinstance(video_quality_mode, VideoQualityMode):
                video_quality_mode_value = video_quality_mode.value
            elif isinstance(video_quality_mode, int):
                video_quality_mode_value = video_quality_mode
            else:
                raise TypeError(
                    f'`video_quality_mode` can be `None`, `str`, `{VideoQualityMode.__name__}`, got '
                    f'{video_quality_mode.__class__.__name__}; {video_quality_mode!r}.')
            
            data['video_quality_mode'] = video_quality_mode_value
        
        
        if (default_auto_archive_after is not ...):
            if __debug__:
                if not issubclass(channel_type, (ChannelText, ChannelForum)):
                    raise AssertionError(
                        f'`default_auto_archive_after` is a valid parameter only for `{ChannelText.__name__}`-s'
                        f', got {channel_type.__name__}; {channel!r}.'
                    )
                
                if not isinstance(default_auto_archive_after, int):
                    raise AssertionError(
                        f'`default_auto_archive_after` can be `None`, `datetime`, got '
                        f'{default_auto_archive_after.__class__.__name__}; {default_auto_archive_after!r}.'
                    )
                
                if default_auto_archive_after not in AUTO_ARCHIVE_OPTIONS:
                    raise AssertionError(
                        f'`default_auto_archive_after` can be any of: '
                        f'{AUTO_ARCHIVE_OPTIONS}, got {default_auto_archive_after}.'
                    )
            
            channel_data['default_auto_archive_duration'] = default_auto_archive_after // 60
        
        
        if (banner is not ...):
            if __debug__:
                if (channel is not None):
                    if not isinstance(channel, ChannelText):
                        raise AssertionError(
                            f'`banner` is a valid parameter only for `{ChannelText.__name__}`-s'
                            f', got {channel.__class__.__name__}; {channel!r}.'
                        )
            
            if banner is None:
                banner_data = None
            else:
                if not isinstance(banner, (bytes, bytearray, memoryview)):
                    raise TypeError(
                        f'`banner` can be `None`, `bytes-like`, got '
                        f'{banner.__class__.__name__}; got {reprlib.repr(banner)}.'
                    )
                
                if __debug__:
                    media_type = get_image_media_type(banner)
                    if media_type not in VALID_ICON_MEDIA_TYPES:
                        raise AssertionError(
                            f'Invalid `banner` type: {media_type}; got {reprlib.repr(banner)}.'
                        )
                
                banner_data = image_to_base64(banner)
            
            data['banner'] = banner_data
        
        
        await self.http.channel_edit(channel_id, data, reason)
    
    
    async def channel_create(self, guild, name, type_=ChannelText, *, reason=None, **kwargs):
        """
        Creates a new channel at the given `guild`. If the channel is successfully created returns it.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild where the channel will be created.
        name : `str`
            The created channel's name.
        type_ : `int`, ``ChannelGuildBase`` subclass = ``ChannelText``, Optional
            The type of the created channel. Defaults to ``ChannelText``.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the `guild`'s audit logs.
        **kwargs : Keyword parameters
            Additional keyword parameters to describe the created channel.
        
        Other Parameters
        ----------------
        permission_overwrites : `list` of ``cr_p_permission_overwrite_object`` returns, Optional (Keyword only)
            A list of permission overwrites of the channel. The list should contain json serializable permission
            overwrites made by the ``cr_p_permission_overwrite_object`` function.
        topic : `str`, Optional (Keyword only)
            The channel's topic.
        nsfw : `bool`, Optional (Keyword only)
            Whether the channel is marked as nsfw.
        slowmode : `int`, Optional (Keyword only)
            The channel's slowmode value.
        bitrate : `int`, Optional (Keyword only)
            The channel's bitrate.
        user_limit : `int`, Optional (Keyword only)
            The channel's user limit.
        parent : `None`, ``ChannelCategory``, `int`, Optional (Keyword only)
            The channel's parent. If the channel is under a guild, leave it empty.
        category : `None`, ``ChannelCategory``, ``Guild``, `int`, Optional (Keyword only)
            Deprecated, please use `parent` parameter instead.
        region : `None`, ``VoiceRegion``, `str`, Optional (Keyword only)
            The channel's voice region.
        video_quality_mode : `None`, ``VideoQualityMode``, `int`, Optional (Keyword only)
            The channel's video quality mode.
        default_auto_archive_after : `None`, `int`
            The default duration (in seconds) for newly created threads to automatically archive the themselves. Can be
            one of: `3600`, `86400`, `259200`, `604800`.
        banner : `None`, `bytes-like`, Optional (Keyword only)
             The new banner of the channel. Can be `'jpg'`, `'png'`, `'webp'` image's raw data.
        
        Returns
        -------
        channel : `None`, ``ChannelGuildBase``
            The created channel. Returns `None` if the respective `guild` is not cached.
        
        Raises
        ------
        TypeError
            - If `guild` was not given as ``Guild``, `int`.
            - If `type_` was not passed as `int`, ``ChannelGuildBase``.
            - If `parent` was not given as `None`, ``ChannelCategory``, `int`.
            - If `region` was not given either as `None`, `str` nor ``VoiceRegion``.
        AssertionError
            - If `type_` was given as `int`, and is less than `0`.
            - If `type_` was given as `int` and exceeds the defined channel type limit.
            - If `name` was not given as `str`.
            - If `name`'s length is out of range `[1:100]`.
            - If `permission_overwrites` was not given as `None`, neither as `list` of `dict`-s.
            - If `topic` was not given as `str`.
            - If `topic`'s length is over `1024`.
            - If `topic` was given, but the respective channel type is not ``ChannelText``.
            - If `nsfw` was given meanwhile the respective channel type is not ``ChannelText``, ``ChannelStore``.
            - If `nsfw` was not given as `bool`.
            - If `slowmode` was given, but the respective channel type is not ``ChannelText``.
            - If `slowmode` was not given as `int`.
            - If `slowmode` was given, but it's value is less than `0` or greater than `21600`.
            - If `bitrate` was given, but the respective channel type is not ``ChannelVoice``.
            - If `bitrate` was not given as `int`.
            - If `bitrate`'s value is out of the expected range.
            - If `user_limit` was given, but the respective channel type is not ``ChannelVoice``.
            - If `user_limit` was not given as `int`.
            - If `user_limit` was given, but is out of the expected [0:99] range.
            - If `parent` was given, but the respective channel type cannot be put under other categories.
            - If `region` was given, but the respective channel type is not ``ChannelVoice``.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild, guild_id = get_guild_and_id(guild)
        
        data = cr_pg_channel_object(name, type_, **kwargs, guild=guild)
        data = await self.http.channel_create(guild_id, data, reason)
        
        return CHANNEL_TYPE_MAP.get(data['type'], ChannelGuildUndefined)(data, self, guild_id)
    
    
    async def channel_delete(self, channel, *, reason=None):
        """
        Deletes the specified guild channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``ChannelGuildBase``, `int`
            The channel to delete.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        TypeError
            If the given `channel` is not ``ChannelGuildBase``, `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        If a category channel is deleted, it's sub-channels will not be removed, instead they will move under the guild.
        """
        channel_id = get_channel_id(channel, ChannelGuildBase)
        
        await self.http.channel_delete(channel_id, reason)
    
    
    async def channel_follow(self, source_channel, target_channel):
        """
        Follows the `source_channel` with the `target_channel`. Returns the webhook, what will crosspost the published
        messages.
        
        This method is a coroutine.
        
        Parameters
        ----------
        source_channel : ``ChannelText``, `int`
            The channel what will be followed. Must be an announcements (type 5) channel.
        target_channel : ``ChannelText``, `int`instance
            The target channel where the webhook messages will be sent. Can be any guild text channel type.
        
        Returns
        -------
        webhook : ``Webhook``
            The webhook what will crosspost the published messages. This webhook has no `.token` set.
        
        Raises
        ------
        TypeError
            - If the `source_channel` was not given neither as ``ChannelText`` nor `int`.
            - If the `target_channel` was not given neither as ``ChannelText`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `source_channel` is not announcement channel.
        """
        source_channel, source_channel_id = get_channel_and_id(source_channel, ChannelText)
        if source_channel is None:
            source_channel = create_partial_channel_from_id(source_channel_id, 5, 0)
        else:
            if __debug__:
                if source_channel.type != 5:
                    raise AssertionError(
                        f'`source_channel` must be type 5 (announcements) channel, got {source_channel}.'
                    )
        
        target_channel_id = get_channel_id(target_channel, ChannelText)
        
        data = {
            'webhook_channel_id': target_channel_id,
        }
        
        data = await self.http.channel_follow(source_channel_id, data)
        webhook = await Webhook._from_follow_data(data, source_channel, target_channel_id, self)
        return webhook
    
    # messages
    
    async def message_get_chunk(self, channel, limit=100, *, after=None, around=None, before=None):
        """
        Requests messages from the given text channel. The `after`, `around` and the `before` parameters are mutually
        exclusive and they can be `int`, or as a ``DiscordEntity`` or as a `datetime` object.
        If there is at least 1 message overlap between the received and the loaded messages, the wrapper will chain
        the channel's message history up. If this happens the channel will get on a queue to have it's messages again
        limited to the default one, but requesting old messages more times, will cause it to extend.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``ChannelTextBase``, `int`
            The channel from where we want to request the messages.
        limit : `int` = `100`, Optional
            The amount of messages to request. Can be between 1 and 100.
        after : `None`, `int`, ``DiscordEntity``, `datetime` = `None`, Optional (Keyword only)
            The timestamp after the requested messages were created.
        around : `None`, `int`, ``DiscordEntity``, `datetime` = `None`, Optional (Keyword only)
            The timestamp around the requested messages were created.
        before : `None`, `int`, ``DiscordEntity``, `datetime` = `None`, Optional (Keyword only)
            The timestamp before the requested messages were created.
        
        Returns
        -------
        messages : `list` of ``Message``
        
        Raises
        ------
        TypeError
            - If `channel` was not given neither as ``ChannelTextBase`` nor `int`.
            - If `after`, `around`, `before` was passed with an unexpected type.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `limit` was not given as `int`.
            - If `limit` is out of range [1:100].
        
        See Also
        --------
        - ``.message_get_chunk_from_zero`` : Familiar to this method, but it requests only the newest messages of the channel
            and makes sure they are chained up with the channel's message history.
        - ``.message_get_at_index`` : A top-level method to get a message at the specified index at the given channel.
            Usually used to load the channel's message history to that point.
        - ``.message_get_all_in_range`` : A top-level method to get all the messages till the specified index at the given
            channel.
        - ``.message_iterator`` : An iterator over a channel's message history.
        """
        channel, channel_id = get_channel_and_id(channel, ChannelTextBase)
        
        if __debug__:
            if not isinstance(limit, int):
                raise AssertionError(
                    f'`limit` can be `int`, got {limit.__class__.__name__}; {limit!r}.'
                )
            
            if (limit < 1) or (limit > 100):
                raise AssertionError(
                    f'`limit` is out from the expected [1:100] range, got {limit!r}.'
                )
        
        data = {'limit': limit}
        
        if (after is not None):
            data['after'] = log_time_converter(after)
        
        if (around is not None):
            data['around'] = log_time_converter(around)
        
        if (before is not None):
            data['before'] = log_time_converter(before)
        
        # Set some collection delay.
        channel._add_message_collection_delay(60.0)
        
        message_datas = await self.http.message_get_chunk(channel_id, data)
        return process_message_chunk(message_datas, channel)
    
    
    # If you have 0-1 messages at a channel, and you wanna store the messages. The other wont store it, because it
    # wont see anything what allows channeling.
    async def message_get_chunk_from_zero(self, channel, limit=100):
        """
        If the `channel` has `1` or less messages loaded use this method instead of ``.message_get_chunk`` to request the
        newest messages there, because this method makes sure, the returned messages will be chained at the
        channel's message history.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``ChannelTextBase``
            The channel from where we want to request the messages.
        limit : `int` = `100`, Optional
            The amount of messages to request. Can be between 1 and 100.
        
        Returns
        -------
        messages : `list` of ``Message`` objects
        
        Raises
        ------
        TypeError
            If `channel` was not given neither as ``ChannelTextBase`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `limit` was not given as `int`.
            - If `limit` is out of range [1:100].
        """
        channel, channel_id = get_channel_and_id(channel, ChannelTextBase)
        
        if __debug__:
            if not isinstance(limit, int):
                raise AssertionError(
                    f'`limit` can be `int`, got {limit.__class__.__name__}; {limit!r}.'
                )
            
            if (limit < 1) or (limit > 100):
                raise AssertionError(
                    f'`limit` is out from the expected [1:100] range, got {limit!r}.'
                )
        
        # Set some collection delay.
        channel._add_message_collection_delay(60.0)
        
        data = {'limit': limit, 'before': 9223372036854775807}
        data = await self.http.message_get_chunk(channel_id, data)
        if data:
            if (channel is not None):
                # Call this method first, so the channel's messages will be set even if message caching is at 0
                channel._maybe_increase_queue_size()
                
                channel._create_new_message(data[0])
            
            messages = process_message_chunk(data, channel)
        else:
            messages = []
        
        return messages
    
    
    async def message_get(self, channel, message_id):
        """
        Requests a specific message by it's id at the given `channel`.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``ChannelTextBase``, `int`
            The channel from where we want to request the message.
        message_id : `int`
            The message's id.
        
        Returns
        -------
        message : ``Message``
        
        Raises
        ------
        TypeError
            If `channel` was not given neither as ``ChannelTextBase`` nor `int`.
            If `message_id` was not given as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id = get_channel_id(channel, ChannelTextBase)
        
        message_id_value = maybe_snowflake(message_id)
        if message_id_value is None:
            raise TypeError(
                f'`message_id` can be `int`, got {message_id.__class__.__name__}; {message_id!r}.'
            )
        
        message_data = await self.http.message_get(channel_id, message_id_value)
        
        return Message(message_data)
    
    
    async def message_create(self, channel, content=None, *, allowed_mentions=...,  components=None, embed=None,
            file=None, nonce=None, reply_fail_fallback=False,  sticker=None, suppress_embeds=False, tts=False):
        """
        Creates and returns a message at the given `channel`. If there is nothing to send, then returns `None`.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``ChannelTextBase``, `int`, ``Message``, ``MessageRepr``, ``MessageReference``,
                `tuple` (`int`, `int`)
            The text channel where the message will be sent, or the message on what you want to reply.
        
        content : `None`, `str`, ``EmbedBase``, `Any` = `None`, Optional
            The message's content if given. If given as `str` or empty string, then no content will be sent, meanwhile
            if any other non `str`, ``EmbedBase`` is given, then will be casted to string.
            
            If given as ``EmbedBase``, then is sent as the message's embed.
        
        allowed_mentions : `None`,  `str`, ``UserBase``, ``Role``, `list` of (`str`, ``UserBase``, ``Role`` )
                , Optional (Keyword only)
            Which user or role can the message ping (or everyone). Check ``parse_allowed_mentions`` for details.
        
        components : `None`, ``ComponentBase``, (`tuple`, `list`) of (``ComponentBase``, (`tuple`, `list`) of
                ``ComponentBase``) = `None`, Optional (Keyword only)
            Components attached to the message.
            
            > `components` do not count towards having any content in the message.
        
        embed : ``EmbedBase``, `list` of ``EmbedBase`` = `None`, Optional (Keyword only)
            The embedded content of the message.
            
            If `embed` and `content` parameters are both given as  ``EmbedBase``, then `TypeError` is raised.
        
        file : `None`, `Any` = `None`, Optional (Keyword only)
            A file or files to send. Check ``create_file_form`` for details.
        
        reply_fail_fallback : `bool` = `False`, Optional (Keyword only)
            Whether normal message should be sent if the referenced message is deleted. Defaults to `False`.
        
        nonce : `None`, `str` = `None`, Optional (Keyword only)
            Used for optimistic message sending. Will shop up at the message's data.
        
        sticker : `None`, ``Sticker``, `int`, (`list`, `set`, `tuple`) of (``Sticker``, `int`) = `None` \
                , Optional (Keyword only)
            Sticker or stickers to send within the message.
        
        suppress_embeds : `bool` = `False`, Optional (Keyword only)
            Whether the message's embeds should be suppressed initially.
        
        tts : `bool` = `False`, Optional (Keyword only)
            Whether the message is text-to-speech.
        
        Returns
        -------
        message : ``Message``, `None`
            Returns `None` if there is nothing to send.
        
        Raises
        ------
        TypeError
            - If `embed` was not given neither as ``EmbedBase`` nor as `list`, `tuple` of ``EmbedBase``-s.
            - If `allowed_mentions` contains an element of invalid type.
            - `content` parameter was given as ``EmbedBase``, meanwhile `embed` parameter was given as well.
            - If invalid file type would be sent.
            - If `channel`'s type is incorrect.
            - If `sticker` was not given neither as `None`, ``Sticker``, `int`, (`list`, `tuple`) of \
                (``Sticker``, `int).
            - If `components` type is incorrect.
        ValueError
            - If `allowed_mentions`'s elements' type is correct, but one of their value is invalid.
            - If more than `10` files would be sent.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `tts` was not given as `bool`.
            - If `nonce` was not given neither as `None` nor as `str`.
            - If `reply_fail_fallback` was not given as `bool`.
            - If `embed` contains a non ``EmbedBase`` element.
            - If `suppress_embeds` is not `bool`.
            - If both `content` and `embed` fields are embeds.
        
        See Also
        --------
        ``.webhook_message_create`` : Sending a message with a ``Webhook``.
        """
        
        # Channel check order:
        # 1.: ChannelTextBase -> channel
        # 2.: Message -> channel + reply
        # 3.: int (str) -> channel
        # 4.: MessageRepr -> channel + reply
        # 5.: MessageReference -> channel + reply
        # 6.: `tuple` (`int`, `int`) -> channel + reply
        # 7.: raise
        
        if isinstance(channel, ChannelTextBase):
            message_id = None
            channel_id = channel.id
        elif isinstance(channel, Message):
            message_id = channel.id
            channel_id = channel.channel_id
            channel = CHANNELS.get(channel_id, None)
        else:
            channel_id = maybe_snowflake(channel)
            if (channel_id is not None):
                message_id = None
                channel = CHANNELS.get(channel_id, None)
            elif isinstance(channel, MessageRepr):
                message_id = channel.id
                channel_id = channel.channel_id
                channel = CHANNELS.get(channel_id, None)
            elif isinstance(channel, MessageReference):
                message_id = channel.message_id
                channel_id = channel.channel_id
                channel = CHANNELS.get(channel_id, None)
            else:
                snowflake_pair = maybe_snowflake_pair(channel)
                if snowflake_pair is None:
                    raise TypeError(
                        f'`channel` can be `{ChannelTextBase.__name__}`, `{Message.__name__}`, '
                        f'`{MessageRepr.__name__}`, `{MessageReference.__name__}`, `int`, `tuple` (`int`, `int`), '
                        f'got {channel.__class__.__name__}; {channel!r}.'
                    )
                
                channel_id, message_id = snowflake_pair
                channel = CHANNELS.get(channel_id, None)
        
        content, embed = validate_content_and_embed(content, embed, False)
        
        # Sticker check order:
        # 1.: None -> None
        # 2.: Sticker -> [sticker.id]
        # 3.: int (str) -> [sticker]
        # 4.: (list, tuple) of (Sticker, int (str)) -> [sticker.id / sticker, ...] / None
        # 5.: raise
        
        if sticker is None:
            sticker_ids = None
        else:
            sticker_ids = []
            if isinstance(sticker, Sticker):
                sticker_id = sticker.id
                sticker_ids.append(sticker_id)
            else:
                sticker_id = maybe_snowflake(sticker)
                if sticker_id is None:
                    if isinstance(sticker, (list, tuple)):
                        for sticker_element in sticker:
                            if isinstance(sticker_element, Sticker):
                                sticker_id = sticker_element.id
                            else:
                                sticker_id = maybe_snowflake(sticker_element)
                                if sticker_id is None:
                                    raise TypeError(
                                        f'`sticker` can contain only `{Sticker.__name__}`, `int` elements, '
                                        f'got {sticker_element.__class__.__name__}; {sticker_element!r}; '
                                        f'sticker={sticker!r}.'
                                    )
                            
                            sticker_ids.append(sticker_id)
                        
                        if not sticker_ids:
                            sticker_ids = None
                    else:
                        raise TypeError(
                            f'`sticker` can be `None`, `{Sticker.__name__}`, `int`, '
                            f'(`list`, `tuple`) of (`{Sticker.__name__}`, `int`), got '
                            f'{sticker.__class__.__name__}; {sticker!r}.'
                        )
                else:
                    sticker_ids.append(sticker_id)
        
        components = get_components_data(components, False)
        
        if __debug__:
            
            if (nonce is not None) and (not isinstance(nonce, str)):
                raise AssertionError(
                    f'`nonce` can be `None`, `str`, got {nonce.__class__.__name__}; {nonce!r}.'
                )
            
            if not isinstance(reply_fail_fallback, bool):
                raise AssertionError(
                    f'`reply_fail_fallback` can be `bool`, got {reply_fail_fallback.__class__.__name__}; '
                    f'{reply_fail_fallback!r}.')
            
            if not isinstance(suppress_embeds, bool):
                raise AssertionError(
                    f'`suppress_embeds` can be `bool`, got {suppress_embeds.__class__.__name__}; {suppress_embeds!r}.'
                )
        
            if not isinstance(tts, bool):
                raise AssertionError(
                    f'`tts` can be `bool`, got {tts.__class__.__name__}, {tts!r}.'
                )
        
        # Build payload
        message_data = {}
        contains_content = False
        
        if (content is not None):
            message_data['content'] = content
            contains_content = True
        
        if (embed is not None):
            message_data['embeds'] = [embed.to_data() for embed in embed]
            contains_content = True
        
        if (sticker_ids is not None):
            message_data['sticker_ids'] = sticker_ids
            contains_content = True
        
        if (components is not None):
            message_data['components'] = components
        
        if tts:
            message_data['tts'] = True
        
        if (nonce is not None):
            message_data['nonce'] = nonce
        
        if (allowed_mentions is not ...):
            message_data['allowed_mentions'] = parse_allowed_mentions(allowed_mentions)
        
        if (message_id is not None):
            message_reference_data = {'message_id': message_id}
            
            if reply_fail_fallback:
                message_reference_data['fail_if_not_exists'] = False
            
            message_data['message_reference'] = message_reference_data
        
        if suppress_embeds:
            message_data['flags'] = MESSAGE_FLAG_VALUE_SUPPRESS_EMBEDS
        
        message_data = add_file_to_message_data(message_data, file, contains_content, False)
        if message_data is None:
            return
        
        message_data = await self.http.message_create(channel_id, message_data)
        if (channel is not None):
            return channel._create_new_message(message_data)
    
    
    async def message_delete(self, message, *, reason=None):
        """
        Deletes the given message.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message : ``Message``, ``MessageReference``, ``MessageRepr``, `tuple` (`int`, `int`)
            The message to delete.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        TypeError
            If message was not given neither as ``Message``, ``MessageReference``, ``MessageRepr``, neither as
            `tuple` (`int`, `int`).
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        The rate limit group is different for own or for messages newer than 2 weeks than for message's of others,
        which are older than 2 weeks.
        """
        
        channel_id, message_id, message = validate_message_to_delete(message)
        
        if (message is None):
            author = None
        else:
            if not message.is_deletable():
                return
            
            author = message.author
        
        if (author is self) or (message_id > int((time_now() - 1209590.) * 1000.-DISCORD_EPOCH) << 22):
            # own or new
            coroutine = self.http.message_delete(channel_id, message_id, reason)
        else:
            coroutine = self.http.message_delete_b2wo(channel_id, message_id, reason)
        
        await coroutine
        # If the coroutine raises, do not switch `message.deleted` to `True`.
        if (message is not None):
            message.deleted = True
    
    
    async def message_delete_multiple(self, messages, *, reason=None):
        """
        Deletes the given messages. The messages can be from different channels as well.
        
        This method is a coroutine.
        
        Parameters
        ----------
        messages : (`list`, `set`, `tuple`) of \
                (``Message``, ``MessageReference``, ``MessageRepr``, `tuple` (`int`, `int`))
            The messages to delete.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        TypeError
            If a message was not given neither as ``Message``, ``MessageReference``, ``MessageRepr``, neither as
            `tuple` (`int`, `int`).
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If `messages` was not given neither as `list`, `set` nor as `tuple`.
        
        Notes
        -----
        This method uses up 3 different rate limit groups parallelly to maximize the deletion speed.
        """
        if __debug__:
            if not isinstance(messages, (list, set, tuple)):
                raise AssertionError(
                    f'`messages` can be `list`, `set`, `tuple`, got {messages.__class__.__name__}; {messages!r}.'
                )
        
        if not messages:
            return
        
        bulk_delete_limit = int((time_now() - 1209600.) * 1000.-DISCORD_EPOCH) << 22 # 2 weeks
        
        by_channel = {}
        
        for message in messages:
            channel_id, message_id, message = validate_message_to_delete(message)
            if (message is not None) and (not message.is_deletable()):
                continue
            
            if message is None:
                own = False
            else:
                if message.author is self:
                    own = True
                else:
                    own = False
            
            try:
                message_group_new, message_group_old, message_group_old_own = by_channel[channel_id]
            except KeyError:
                message_group_new = deque()
                message_group_old = deque()
                message_group_old_own = deque()
                by_channel[channel_id] = (message_group_new, message_group_old, message_group_old_own)
            
            if message_id > bulk_delete_limit:
                message_group_new.append((own, message_id),)
                continue
            
            if own:
                group = message_group_old_own
            else:
                group = message_group_old
            
            group.append(message_id)
            continue
        
        tasks = []
        for channel_id, groups in by_channel.items():
            try:
                channel = CHANNELS[channel_id]
            except KeyError:
                is_private = False
            else:
                if isinstance(channel, ChannelGuildBase):
                    is_private = False
                else:
                    is_private = True
            
            if is_private:
                function = _message_delete_multiple_private_task
            else:
                function = _message_delete_multiple_task
            
            task = Task(function(self, channel_id, groups, reason), KOKORO)
            tasks.append(task)
        
        await WaitTillAll(tasks, KOKORO)
        
        last_exception = None
        for task in tasks:
            exception = task.exception()
            if exception is None:
                continue
            
            if last_exception is None:
                last_exception = exception
            else:
                if isinstance(exception, ConnectionError):
                    # This is the lowest priority exception, never overwrite older ones.
                    pass
                elif isinstance(exception, DiscordException):
                    # Do overwrite only `ConnectionError`.
                    if isinstance(last_exception, ConnectionError):
                        last_exception = exception
                else:
                    # Do not overwrite same tier exceptions again, only `ConnectionError` and `DiscordException`
                    if isinstance(last_exception, (ConnectionError, DiscordException)):
                        last_exception = exception
            
            task.cancel()
        
        if (last_exception is not None):
            raise last_exception
    
        
    async def message_delete_sequence(self, channel, *, after=None, before=None, limit=None, filter=None, reason=None):
        """
        Deletes messages between an interval determined by `before` and `after`. They can be `int`, or as
        a ``DiscordEntity`` or as a `datetime` object.
        
        If the client has no `manage_messages` permission at the channel, then returns instantly.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``ChannelTextBase``
            The channel, where the deletion should take place.
        after : `None`, `int`, ``DiscordEntity``, `datetime` = `None`, Optional (Keyword only)
            The timestamp after the messages were created, which will be deleted.
        before : `None`, `int`, ``DiscordEntity``, `datetime` = `None`, Optional (Keyword only)
            The timestamp before the messages were created, which will be deleted.
        limit : `None`, `int` = `None`, Optional (Keyword only)
            The maximal amount of messages to delete.
        filter : `None`, `callable` = `None`, Optional (Keyword only)
            A callable filter, what should accept a message object as parameter and return either `True`, `False`.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        TypeError
            If `after`, `before` was passed with an unexpected type.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If `channel` was not given as ``ChannelTextBase``.
        
        Notes
        -----
        This method uses up 4 different rate limit groups parallelly to maximize the request and the deletion speed.
        """
        if __debug__:
            if not isinstance(channel, ChannelTextBase):
                raise AssertionError(
                    f'`channel` can `{ChannelTextBase.__name__}`, got {channel.__class__.__name__}; {channel!r}.'
                )
        
        # Check permissions
        permissions = channel.cached_permissions_for(self)
        if not permissions & PERMISSION_MASK_MANAGE_MESSAGES:
            return
        
        before = 9223372036854775807 if before is None else log_time_converter(before)
        after = 0 if after is None else log_time_converter(after)
        limit = 9223372036854775807 if limit is None else limit
        
        # Check for reversed intervals
        if before < after:
            return
        
        # Check if we are done already
        if limit <= 0:
            return
        
        message_group_new = deque()
        message_group_old = deque()
        message_group_old_own = deque()
        
        # Check if we can request more messages
        if channel.message_history_reached_end or (not permissions & PERMISSION_MASK_READ_MESSAGE_HISTORY):
            should_request = False
        else:
            should_request = True
        
        last_message_id = before
        
        messages_ = channel.messages
        if (messages_ is not None) and messages_:
            before_index = message_relative_index(messages_, before)
            after_index = message_relative_index(messages_, after)
            if before_index != after_index:
                time_limit = int((time_now() - 1209600.) * 1000.-DISCORD_EPOCH) << 22
                while True:
                    if before_index == after_index:
                        break
                    
                    message_ = messages_[before_index]
                    before_index += 1
                    
                    # Ignore invoking user only messages! Desu!
                    if not message_.is_deletable():
                        continue
                    
                    if (filter is not None):
                        if not filter(message_):
                            continue
                    
                    last_message_id = message_.id
                    own = (message_.author is self)
                    if last_message_id > time_limit:
                        message_group_new.append((own, last_message_id,),)
                    else:
                        if own:
                            group = message_group_old_own
                        else:
                            group = message_group_old
                        group.append(last_message_id)
                    
                    # Check if we reached the limit
                    limit -= 1
                    if limit:
                        continue
                    
                    should_request = False
                    break
        
        tasks = []
        
        get_mass_task = None
        delete_mass_task = None
        delete_new_task = None
        delete_old_task = None
        
        channel_id = channel.id
        
        while True:
            if should_request and (get_mass_task is None):
                request_data = {
                    'limit': 100,
                    'before': last_message_id,
                }
                
                get_mass_task = Task(self.http.message_get_chunk(channel_id, request_data), KOKORO)
                tasks.append(get_mass_task)
            
            if (delete_mass_task is None):
                message_limit = len(message_group_new)
                # If there are more messages, we are waiting for other tasks
                if message_limit:
                    time_limit = int((time_now() - 1209590.) * 1000.-DISCORD_EPOCH) << 22 # 2 weeks -10s
                    collected = 0
                    
                    while True:
                        if collected == message_limit:
                            break
                        
                        if collected == 100:
                            break
                        
                        own, message_id = message_group_new[collected]
                        if message_id < time_limit:
                            break
                        
                        collected += 1
                        continue
                    
                    if collected == 0:
                        pass
                    
                    elif collected == 1:
                        # Delete the message if we don't delete a new message already
                        if (delete_new_task is None):
                            # We collected 1 message -> We cannot use mass delete on this.
                            own, message_id = message_group_new.popleft()
                            delete_new_task = Task(self.http.message_delete(channel_id, message_id, reason),
                                KOKORO)
                            tasks.append(delete_new_task)
                    else:
                        message_ids = []
                        while collected:
                            collected -= 1
                            own, message_id = message_group_new.popleft()
                            message_ids.append(message_id)
                        
                        delete_mass_task = Task(self.http.message_delete_multiple(channel_id, {'messages': message_ids},
                            reason), KOKORO)
                        tasks.append(delete_mass_task)
                    
                    # After we checked what is at this group, lets move the others from it's end, if needed ofc
                    message_limit = len(message_group_new)
                    if message_limit:
                        # time limit -> 2 week
                        time_limit = time_limit - 20971520000
                        
                        while True:
                            # Cannot start at index = len(...), so we instantly do -1
                            message_limit -= 1
                            
                            own, message_id = message_group_new[message_limit]
                            # Check if we should not move -> leave
                            if message_id > time_limit:
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
                    message_id = message_group_old_own.popleft()
                    delete_new_task = Task(self.http.message_delete(channel_id, message_id, reason), KOKORO)
                    tasks.append(delete_new_task)
            
            if (delete_old_task is None):
                if message_group_old:
                    message_id = message_group_old.popleft()
                    delete_old_task = Task(self.http.message_delete_b2wo(channel_id, message_id, reason), KOKORO)
                    tasks.append(delete_old_task)
            
            if not tasks:
                # It can happen, that there are no more tasks left, at that case we check if there is more message
                # left. Only at `message_group_new` can be anymore message, because there is a time interval of
                # 10 seconds, what we do not move between categories.
                if not message_group_new:
                    break
                
                # We really have at least 1 message at that interval.
                own, message_id = message_group_new.popleft()
                # We will delete that message with old endpoint if not own, to make sure it will not block the other
                # endpoint for 2 minutes with any chance.
                if own:
                    delete_new_task = Task(self.http.message_delete(channel_id, message_id, reason), KOKORO)
                    task = delete_new_task
                else:
                    delete_old_task = Task(self.http.message_delete_b2wo(channel_id, message_id, reason), KOKORO)
                    task = delete_old_task
                
                tasks.append(task)
            
            done, pending = await WaitTillFirst(tasks, KOKORO)
            
            for task in done:
                tasks.remove(task)
                try:
                    result = task.result()
                except:
                    for task in tasks:
                        task.cancel()
                    raise
                
                if task is get_mass_task:
                    get_mass_task = None
                    
                    received_count = len(result)
                    if received_count < 100:
                        should_request = False
                        
                        # We got 0 messages, move on the next task
                        if received_count == 0:
                            continue
                    
                    # We don't really care about the limit, because we check message id when we delete too.
                    time_limit = int((time_now() - 1209600.) * 1000.-DISCORD_EPOCH) << 22 # 2 weeks
                    
                    for message_data in result:
                        if (filter is None):
                            last_message_id = int(message_data['id'])
    
                            # Did we reach the after limit?
                            if last_message_id < after:
                                should_request = False
                                break
                            
                            # If filter is `None`, we just have to decide, if we were the author or nope.
                            
                            # Try to get user id, first start it with trying to get author data. The default author_id
                            # will be 0, because that's sure not the id of the client.
                            try:
                                author_data = message_data['author']
                            except KeyError:
                                author_id = 0
                            else:
                                # If we have author data, lets select the user's data from it
                                try:
                                    user_data = author_data['user']
                                except KeyError:
                                    user_data = author_data
                                
                                try:
                                    author_id = user_data['id']
                                except KeyError:
                                    author_id = 0
                                else:
                                    author_id = int(author_id)
                        else:
                            message_ = Message(message_data)
                            last_message_id = message_.id
                            
                            # Did we reach the after limit?
                            if last_message_id < after:
                                should_request = False
                                break
                            
                            if not filter(message_):
                                continue
                            
                            author_id = message_.author.id
                        
                        own = (author_id == self.id)
                        
                        if last_message_id > time_limit:
                            message_group_new.append((own, last_message_id,),)
                        else:
                            if own:
                                group = message_group_old_own
                            else:
                                group = message_group_old
                            
                            group.append(last_message_id)
                        
                        # Did we reach the amount limit?
                        limit -= 1
                        if limit:
                            continue
                        
                        should_request = False
                        break
                
                if task is delete_mass_task:
                    delete_mass_task = None
                    continue
                
                if task is delete_new_task:
                    delete_new_task = None
                    continue
                
                if task is delete_old_task:
                    delete_old_task = None
                    continue
                 
                # Should not happen
                continue
    
    
    async def multi_client_message_delete_sequence(self, channel, *, after=None, before=None, limit=None, filter=None,
            reason=None):
        """
        Deletes messages between an interval determined by `before` and `after`. They can be `int`, or as
        a ``DiscordEntity`` or as a `datetime` object.
        
        Not like ``.message_delete_sequence``, this method uses up all he clients at the respective channel to delete
        messages an not only the one from what it was called from.
        
        If non of the clients have `manage_messages` permission, then returns instantly.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``ChannelTextBase``
            The channel, where the deletion should take place.
        after : `None`, `int`, ``DiscordEntity``, `datetime` = `None`, Optional (Keyword only)
            The timestamp after the messages were created, which will be deleted.
        before : `None`, `int`, ``DiscordEntity``, `datetime` = `None`, Optional (Keyword only)
            The timestamp before the messages were created, which will be deleted.
        limit : `None`, `int` = `None`, Optional (Keyword only)
            The maximal amount of messages to delete.
        filter : `None`, `callable` = `None`, Optional (Keyword only)
            A callable filter, what should accept a message object as parameter and return either `True`, `False`.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        TypeError
            If `after`, `before` was passed with an unexpected type.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If `channel` is not ``ChannelTextBase``.
        
        Notes
        -----
        This method uses up to 4 different endpoint groups too as ``.message_delete_sequence``, but tries to
        parallelize the them between more clients as well.
        """
        if __debug__:
            if not isinstance(channel, ChannelTextBase):
                raise AssertionError(
                    f'`channel` can be `{ChannelTextBase.__name__}`, got {channel.__class__.__name__}; {channel!r}.'
                )
        
        # Check permissions
        sharders = []
        
        for client in channel.clients:
            sharder = MultiClientMessageDeleteSequenceSharder(client, channel)
            if sharder is None:
                continue
            
            sharders.append(sharder)
        
        if not sharders:
            return
        
        for sharder in sharders:
            if sharder.can_manage_messages:
                break
        else:
            return
        
        before = 9223372036854775807 if before is None else log_time_converter(before)
        after = 0 if after is None else log_time_converter(after)
        limit = 9223372036854775807 if limit is None else limit
        
        # Check for reversed intervals
        if before < after:
            return
        
        # Check if we are done already
        if limit <= 0:
            return
        
        message_group_new = deque()
        message_group_old = deque()
        message_group_old_own = deque()
        
        # Check if we can request more messages
        if channel.message_history_reached_end:
            should_request = False
        else:
            for sharder in sharders:
                if sharder.can_read_message_history:
                    should_request = True
                    break
            else:
                should_request = False
        
        last_message_id = before
        
        is_own_getter = {}
        for index in range(len(sharders)):
            is_own_getter[sharders[index].client.id] = index
        
        messages_ = channel.messages
        if (messages_ is not None) and messages_:
            before_index = message_relative_index(messages_, before)
            after_index = message_relative_index(messages_, after)
            if before_index != after_index:
                time_limit = int((time_now() - 1209600.) * 1000.-DISCORD_EPOCH) << 22
                while True:
                    if before_index == after_index:
                        break
                    
                    message_ = messages_[before_index]
                    before_index += 1
                    
                    if not message_.is_deletable():
                        continue
                    
                    if (filter is not None):
                        if not filter(message_):
                            continue
                    
                    last_message_id = message_.id
                    who_s = is_own_getter.get(message_.author.id, -1)
                    if last_message_id > time_limit:
                        message_group_new.append((who_s, last_message_id,),)
                    else:
                        if who_s == -1:
                            message_group_old.append(last_message_id)
                        else:
                            message_group_old_own.append((who_s, last_message_id,),)
                    
                    # Check if we reached the limit
                    limit -= 1
                    if limit:
                        continue
                    
                    should_request = False
                    break
        
        tasks = []
        # Handle requesting together, since we need to know, till where the last request yielded.
        get_mass_task = None
        # Loop the sharders when requesting, so rate limits are used up.
        get_mass_task_next = 0
        
        channel_id = channel.id
        
        while True:
            if should_request and (get_mass_task is None):
                # Will break since `should_request` is set to `True` only if at least of the sharders have
                # `read_message_history` permission
                while True:
                    if get_mass_task_next >= len(sharders):
                        get_mass_task_next = 0
                    
                    sharder = sharders[get_mass_task_next]
                    if sharder.can_read_message_history:
                        break
                    
                    get_mass_task_next += 1
                    continue
                
                request_data = {
                    'limit': 100,
                    'before': last_message_id,
                }
                
                get_mass_task = Task(sharder.client.http.message_get_chunk(channel_id, request_data), KOKORO)
                tasks.append(get_mass_task)
            
            for sharder in sharders:
                if (sharder.can_manage_messages) and (sharder.delete_mass_task is None):
                    message_limit = len(message_group_new)
                    # If there are more messages, we are waiting for other tasks
                    if message_limit:
                        time_limit = int((time_now() - 1209590.) * 1000.-DISCORD_EPOCH) << 22 # 2 weeks -10s
                        collected = 0
                        
                        while True:
                            if collected == message_limit:
                                break
                            
                            if collected == 100:
                                break
                            
                            who_s, message_id = message_group_new[collected]
                            if message_id < time_limit:
                                break
                            
                            collected += 1
                            continue
                        
                        if collected == 0:
                            pass
                        
                        elif collected == 1:
                            # Delete the message if we don't delete a new message already
                            for sub_sharder in sharders:
                                if (sub_sharder.can_manage_messages) and (sharder.delete_new_task is None):
                                    # We collected 1 message -> We cannot use mass delete on this.
                                    who_s, message_id = message_group_new.popleft()
                                    delete_new_task = Task(sub_sharder.client.http.message_delete(channel_id,
                                        message_id, reason=reason), KOKORO)
                                    sub_sharder.delete_new_task = delete_new_task
                                    tasks.append(delete_new_task)
                                    break
                        else:
                            message_ids = []
                            while collected:
                                collected -= 1
                                who_s, message_id = message_group_new.popleft()
                                message_ids.append(message_id)
                            
                            delete_mass_task = Task(sharder.client.http.message_delete_multiple(channel_id,
                                {'messages': message_ids}, reason), KOKORO)
                            sharder.delete_mass_task = delete_mass_task
                            tasks.append(delete_mass_task)
                        
                        # After we checked what is at this group, lets move the others from it's end, if needed ofc
                        message_limit = len(message_group_new)
                        if message_limit:
                            # time limit -> 2 week
                            time_limit = time_limit - 20971520000
                            
                            while True:
                                # Cannot start at index = len(...), so we instantly do -1
                                message_limit -= 1
                                
                                who_s, message_id = message_group_new[message_limit]
                                # Check if we should not move -> leave
                                if message_id > time_limit:
                                    break
                                
                                del message_group_new[message_limit]
                                if who_s == -1:
                                    message_group_old.appendleft(message_id)
                                else:
                                    message_group_old_own.appendleft((who_s, message_group_old,),)
                                
                                if message_limit:
                                    continue
                                
                                break
            
            # Check old own messages only, mass delete speed is pretty good by itself.
            if message_group_old_own:
                # Check who's is the last message. And delete with it. These speed is pretty fast.
                # I doubt it needs further speedup, since deleting not own messages are the bottleneck of message
                # deletions.
                who_s, message_id = message_group_old_own[0]
                sharder = sharders[who_s]
                if sharder.delete_new_task is None:
                    del message_group_old_own[0]
                    delete_new_task = Task(sharder.client.http.message_delete(channel_id, message_id, reason), KOKORO)
                    sharder.delete_new_task = delete_new_task
                    tasks.append(delete_new_task)
            
            if message_group_old:
                for sharder in sharders:
                    if (sharder.delete_old_task is None):
                        message_id = message_group_old.popleft()
                        delete_old_task = Task(sharder.client.http.message_delete_b2wo(channel_id, message_id, reason),
                            KOKORO)
                        sharder.delete_old_task = delete_old_task
                        tasks.append(delete_old_task)
                        
                        if not message_group_old:
                            break
            
            if not tasks:
                # It can happen, that there are no more tasks left, at that case we check if there is more message
                # left. Only at `message_group_new` can be anymore message, because there is a time interval of
                # 10 seconds, what we do not move between categories.
                if not message_group_new:
                    break
                
                # We really have at least 1 message at that interval.
                who_s, message_id = message_group_new.popleft()
                # We will delete that message with old endpoint if not own, to make sure it will not block the other
                # endpoint for 2 minutes with any chance.
                if who_s == -1:
                    for sharder in sharders:
                        if sharder.can_manage_messages:
                            task = Task(sharder.client.http.message_delete_b2wo(channel_id, message_id, reason), KOKORO)
                            sharder.delete_old_task = task
                            break
                else:
                    sharder = sharders[who_s]
                    task = Task(sharder.client.http.message_delete(channel_id, message_id, reason), KOKORO)
                    sharder.delete_new_task = task
                
                tasks.append(task)
            
            done, pending = await WaitTillFirst(tasks, KOKORO)
            
            for task in done:
                tasks.remove(task)
                try:
                    result = task.result()
                except:
                    for task in tasks:
                        task.cancel()
                    raise
                
                if task is get_mass_task:
                    get_mass_task = None
                    
                    received_count = len(result)
                    if received_count < 100:
                        should_request = False
                        
                        # We got 0 messages, move on the next task
                        if received_count == 0:
                            continue
                    
                    # We don't really care about the limit, because we check message id when we delete too.
                    time_limit = int((time_now() - 1209600.) * 1000.-DISCORD_EPOCH) << 22 # 2 weeks
                    
                    for message_data in result:
                        if (filter is None):
                            last_message_id = int(message_data['id'])
                            
                            # Did we reach the after limit?
                            if last_message_id < after:
                                should_request = False
                                break
                            
                            # If filter is `None`, we just have to decide, if we were the author or nope.
                            
                            # Try to get user id, first start it with trying to get author data. The default author_id
                            # will be 0, because that's sure not the id of the client.
                            try:
                                author_data = message_data['author']
                            except KeyError:
                                author_id = 0
                            else:
                                # If we have author data, lets select the user's data from it
                                try:
                                    user_data = author_data['user']
                                except KeyError:
                                    user_data = author_data
                                
                                try:
                                    author_id = user_data['id']
                                except KeyError:
                                    author_id = 0
                                else:
                                    author_id = int(author_id)
                        else:
                            message_ = Message(message_data)
                            last_message_id = message_.id
                            
                            # Did we reach the after limit?
                            if last_message_id < after:
                                should_request = False
                                break
                            
                            if not filter(message_):
                                continue
                            
                            author_id = message_.author.id
                        
                        who_s = is_own_getter.get(author_id, -1)
                        
                        if last_message_id > time_limit:
                            message_group_new.append((who_s, last_message_id,),)
                        else:
                            if who_s == -1:
                                message_group_old.append(last_message_id)
                            else:
                                message_group_old_own.append((who_s, last_message_id,),)
                        
                        # Did we reach the amount limit?
                        limit -= 1
                        if limit:
                            continue
                        
                        should_request = False
                        break
                
                for sharder in sharders:
                    if task is sharder.delete_mass_task:
                        sharder.delete_mass_task = None
                        break
                    
                    if task is sharder.delete_new_task:
                        sharder.delete_new_task = None
                        break
                    
                    if task is sharder.delete_old_task:
                        sharder.delete_old_task = None
                        break
                
                # Else case should happen.
                continue
    
    
    async def message_edit(self, message, content=..., *, embed=..., file=..., allowed_mentions=..., components=...,
            suppress=..., suppress_embeds=...):
        """
        Edits the given `message`.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message : ``Message``, ``MessageRepr``, ``MessageReference``, `tuple` (`int`, `int`)
            The message to edit.
        content : `None`, `str`, ``EmbedBase``, `Any`, Optional
            The new content of the message.
            
            If given as `str` then the message's content will be edited with it. If given as any non ``EmbedBase``
            instance, then it will be cased to string first.
            
            If given as ``EmbedBase``, then the message's embeds will be edited with it.
        embed : `None`, ``EmbedBase``, `list` of ``EmbedBase``, Optional (Keyword only)
            The new embedded content of the message. By passing it as `None`, you can remove the old.
            
            If `embed` and `content` parameters are both given as  ``EmbedBase``, then `AssertionError` is
            raised.
        
        file : `None`, `Any`, Optional (Keyword only)
            A file or files to send. Check ``create_file_form`` for details.
        
        allowed_mentions : `None`,  `str`, ``UserBase``, ``Role``, `list` of (`str`, ``UserBase``, ``Role`` )
                , Optional (Keyword only)
            Which user or role can the message ping (or everyone). Check ``parse_allowed_mentions``
            for details.
        components : `None`, ``ComponentBase``, (`tuple`, `list`) of (``ComponentBase``, (`tuple`, `list`) of
                ``ComponentBase``), Optional (Keyword only)
            Components attached to the message.
            
            Pass it as `None` remove the actual ones.
        
        suppress : `bool`, Optional (Keyword only)
            Whether the message's embeds should be suppressed or unsuppressed.
            
            Deprecated, please use `suppress_embeds` parameter instead.
        
        suppress_embeds : `bool`, Optional (Keyword only)
            Whether the message's embeds should be suppressed or unsuppressed.
        
        Raises
        ------
        TypeError
            - If `embed` was not given neither as ``EmbedBase`` nor as `list`, `tuple` of ``EmbedBase``-s.
            - If `allowed_mentions` contains an element of invalid type.
            - `content` parameter was given as ``EmbedBase``, meanwhile `embed` parameter was given as well.
            - If `message`'s type is incorrect.
            - If `components` type is incorrect.
        ValueError
            - If `allowed_mentions` contains an element of invalid type.
            - If more than `10` files would be sent.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `suppress_embeds` was not given as `bool`.
            - If `embed` contains a non ``EmbedBase`` element.
            - If both `content` and `embed` fields are embeds.
        
        See Also
        --------
        - ``.message_suppress_embeds`` : For suppressing only the embeds of the message.
        - ``.webhook_message_edit`` : Editing messages sent by webhooks.
        
        Notes
        -----
        Do not updates he given message object, so dispatch event events can still calculate differences when received.
        """
        message, channel_id, message_id = get_message_and_channel_id_and_message_id(message)
        
        content, embed = validate_content_and_embed(content, embed, True)
        
        components = get_components_data(components, True)
        
        if (suppress is not ...):
            warnings.warn(
                (
                    f'`{self.__class__.__name__.__name__}.message_edit`\'s `suppress` parameter is deprecated, and '
                    f'will be removed in 2022 May. Please use `suppress_embeds` instead.'
                ),
                FutureWarning,
            )
            
            suppress_embeds = suppress
        
        if __debug__:
            if (suppress_embeds is not ...) and (not isinstance(suppress_embeds, bool)):
                raise AssertionError(
                    f'`suppress_embeds` can be `bool`, got {suppress_embeds.__class__.__name__}; {suppress_embeds!r}.'
                )
        
        # Build payload
        message_data = {}
        
        if (content is not ...):
            message_data['content'] = content
        
        if (embed is not ...):
            if (embed is not None):
                embed = [embed.to_data() for embed in embed]
            
            message_data['embeds'] = embed
        
        if (allowed_mentions is not ...):
            message_data['allowed_mentions'] = parse_allowed_mentions(allowed_mentions)
        
        if (components is not ...):
            message_data['components'] = components
        
        if (suppress is not ...):
            if message is None:
                flags = 0
            else:
                flags = message.flags
            
            if suppress_embeds:
                flags |= MESSAGE_FLAG_VALUE_SUPPRESS_EMBEDS
            else:
                flags &= ~MESSAGE_FLAG_VALUE_SUPPRESS_EMBEDS
            
            message_data['flags'] = flags
        
        message_data = add_file_to_message_data(message_data, file, True, True)
        if (message_data is None):
            return
        
        await self.http.message_edit(channel_id, message_id, message_data)
    
    
    async def message_suppress_embeds(self, message, suppress_embeds=True):
        """
        Suppresses or unsuppressed the given message's embeds.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message : ``Message``, ``MessageRepr``, ``MessageReference``, `tuple` (`int`, `int`)
            The message, what's embeds will be (un)suppressed.
        suppress_embeds : `bool` = `True`, Optional
            Whether the message's embeds would be suppressed or unsuppressed.
        
        Raises
        ------
        TypeError
            If `message` was not given neither as ``Message``, ``MessageRepr`, ``MessageReference`` neither as `tuple`
            (`int`, `int`) instance.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If `suppress` was not given as `bool`.
        """
        message, channel_id, message_id = get_message_and_channel_id_and_message_id(message)
        
        if __debug__:
            if not isinstance(suppress_embeds, bool):
                raise AssertionError(
                    f'`suppress_embeds` can be `bool`, got {suppress_embeds.__class__.__name__}; {suppress_embeds!r}.'
                )
        
        if message is None:
            flags = 0
        else:
            flags = message.flags
        
        if suppress_embeds:
            flags |= MESSAGE_FLAG_VALUE_SUPPRESS_EMBEDS
        else:
            flags &= ~MESSAGE_FLAG_VALUE_SUPPRESS_EMBEDS
        
        await self.http.message_edit(channel_id, message_id, {'flags': flags})
    
    
    async def message_crosspost(self, message):
        """
        Crossposts the given message. The message's channel must be an announcements (type 5) channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message : ``Message``, ``MessageRepr``, ``MessageReference``, `tuple` (`int`, `int`)
            The message to crosspost.
        
        Raises
        ------
        TypeError
            If `message` was not given neither as ``Message``, ``MessageRepr`, ``MessageReference`` nor as
            `tuple` (`int`, `int`) instance.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id, message_id = get_channel_id_and_message_id(message)
        
        await self.http.message_crosspost(channel_id, message_id)
    
    
    async def message_pin(self, message):
        """
        Pins the given message.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message : ``Message``, ``MessageRepr``, ``MessageReference``, `tuple` (`int`, `int`)
            The message to pin.
        
        Raises
        ------
        TypeError
            If `message` was not given neither as ``Message``, ``MessageRepr`, ``MessageReference`` nor as
            `tuple` (`int`, `int`) instance.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id, message_id = get_channel_id_and_message_id(message)
        
        await self.http.message_pin(channel_id, message_id)
    
    
    async def message_unpin(self, message):
        """
        Unpins the given message.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message : ``Message``, ``MessageRepr``, ``MessageReference``, `tuple` (`int`, `int`)
            The message to unpin.
        
        Raises
        ------
        TypeError
            If `message` was not given neither as ``Message``, ``MessageRepr`, ``MessageReference`` nor as
            `tuple` (`int`, `int`) instance.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id, message_id = get_channel_id_and_message_id(message)
        
        await self.http.message_unpin(channel_id, message_id)
    
    
    async def channel_pin_get_all(self, channel):
        """
        Returns the pinned messages at the given channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``ChannelTextBase``, `int`
            The channel from were the pinned messages will be requested.
        
        Returns
        -------
        messages : `list` of ``Message`` objects
            The pinned messages at the given channel.
        
        Raises
        ------
        TypeError
            If `channel` was not given neither as ``ChannelTextBase`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id = get_channel_id(channel, ChannelTextBase)
        
        data = await self.http.channel_pin_get_all(channel_id)
        
        return [Message(message_data) for message_data in data]
    
    
    async def _load_messages_till(self, channel, index):
        """
        An internal function to load the messages at the given channel till the given index. Should not be called if
        the channel reached it's message history's end.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``ChannelTextBase``
            The channel from where the messages will be requested.
        index : `int`
            Till which index the messages should be requested at the given channel.
        
        Returns
        -------
        result_state : `int`
            can return the following variables describing a state:
            
            +-----------+---------------------------------------------------------------------------+
            | Value     | Description                                                               |
            +-----------+---------------------------------------------------------------------------+
            | 0         | Success.                                                                  |
            +-----------+---------------------------------------------------------------------------+
            | 1         | `index` could not be reached, there is no more messages at the channel.   |
            +-----------+---------------------------------------------------------------------------+
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        while True:
            messages = channel.messages
            if messages is None:
                ln = 0
            else:
                ln = len(channel.messages)
            
            load_to = index - ln
            
            # we want to load it till the exact index, so if `load_to` is `0`, that's not enough!
            if load_to < 0:
                result_state = 0
                break
            
            if load_to < 98:
                planned = load_to + 2
            else:
                planned = 100
            
            if ln:
                result = await self.message_get_chunk(channel, planned, before=messages[ln - 1].id + 1)
            else:
                result = await self.message_get_chunk_from_zero(channel, planned)
            
            if len(result) < planned:
                channel.message_history_reached_end = True
                result_state = 1
                break
        
        # Set some collection delay.
        channel._add_message_collection_delay(float(index))
        
        return result_state
    
    
    async def message_get_at_index(self, channel, index):
        """
        Returns the message at the given channel at the specific index. Can be used to load `index` amount of messages
        at the channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``ChannelTextBase``, `int`.
            The channel from were the messages will be requested.
        index : `int`
            The index of the target message.
        
        Returns
        -------
        message : ``Message`` object
        
        Raises
        ------
        TypeError
            If `channel` was not given neither as ``ChannelTextBase`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `index` was not given as `int`.
            - If `index` is out of range [0:].
        """
        if __debug__:
            if not isinstance(index, int):
                raise AssertionError(
                    f'`index` can be `int`, got {index.__class__.__name__}; {index!r}.'
                )
            
            if index < 0:
                raise AssertionError(
                    f'`index` is out from the expected [0:] range, got {index!r}.'
                )
        
        channel, channel_id = get_channel_and_id(channel, ChannelTextBase)
        if channel is None:
            messages = await self.message_get_chunk_from_zero(channel_id, min(index + 1, 100))
            
            if messages:
                channel = messages[0].channel
            else:
                raise IndexError(index)
        
        messages = channel.messages
        if (messages is not None) and (index < len(messages)):
            raise IndexError(index)
        
        if channel.message_history_reached_end:
            raise IndexError(index)
        
        if await self._load_messages_till(channel, index):
            raise IndexError(index)
        
        # access it again, because it might be modified
        messages = channel.messages
        if messages is None:
            raise IndexError(index)
        
        return messages[index]
    
    
    async def message_get_all_in_range(self, channel, start=0, end=100):
        """
        Returns a list of the message between the `start` - `end` area. If the client has no permission to request
        messages, or there are no messages at the given area returns an empty list.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``ChannelTextBase``, `int`
            The channel from were the messages will be requested.
        start : `int` = `0`, Optional
            The first message's index at the channel to be requested. Defaults to `0`.
        end : `int` = `100`, Optional
            The last message's index at the channel to be requested. Defaults to `100`.
        
        Returns
        -------
        messages : `list` of ``Message`` objects
        
        Raises
        ------
        TypeError
            If `channel` was not given neither as ``ChannelTextBase`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `start` was not given as `int`.
            - If `start` is out of range [0:].
            - If `end` was not given as `int`.
            - If `end` is out of range [0:].
        """
        if __debug__:
            if not isinstance(start, int):
                raise AssertionError(
                    f'`start` can be `int`, got {start.__class__.__name__}; {start!r}.'
                )
            
            if start < 0:
                raise AssertionError(
                    f'`start` is out from the expected [0:] range, got {start!r}.'
                )
        
            if not isinstance(end, int):
                raise AssertionError(
                    f'`end` can be `int`, got {end.__class__.__name__}; {end!r}.'
                )
            
            if end < 0:
                raise AssertionError(
                    f'`end` is out from the expected [0:] range, got {end!r}.'
                )
        
        channel, channel_id = get_channel_and_id(channel, ChannelTextBase)
        if channel is None:
            messages = await self.message_get_chunk_from_zero(channel_id, min(end + 1, 100))
            
            if messages:
                channel = messages[0].channel
            else:
                return []
        
        if end <= start:
            return []
        
        messages = channel.messages
        if messages is None:
            ln = 0
        else:
            ln = len(messages)
        
        if (end >= ln) and (not channel.message_history_reached_end) and \
               channel.cached_permissions_for(self) & PERMISSION_MASK_READ_MESSAGE_HISTORY:
            
            try:
                await self._load_messages_till(channel, end)
            except BaseException as err:
                if isinstance(err, DiscordException) and err.code in (
                    ERROR_CODES.unknown_message, # message deleted
                    ERROR_CODES.unknown_channel, # message's channel deleted
                    ERROR_CODES.missing_access, # client removed
                    ERROR_CODES.missing_permissions, # permissions changed meanwhile
                    ERROR_CODES.cannot_message_user, # user has dm-s disallowed
                ):
                    pass
                else:
                    raise
        
        result = []
        messages = channel.messages
        if (messages is not None):
            for index in range(start, min(end, len(messages))):
                result.append(messages[index])
        
        return result
    
    
    async def message_iterator(self, channel, *, chunk_size=99):
        """
        Returns an asynchronous message iterator over the given text channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``ChannelTextBase``  or `int`
            The channel from were the messages will be requested.
        chunk_size : `int` = `99`, Optional (Keyword only)
            The amount of messages to request when the currently loaded history is exhausted. For message chaining
            it is preferably `99`.
        
        Returns
        -------
        message_iterator : ``MessageIterator``
        
        Raises
        ------
        TypeError
            If `channel` was not given neither as ``ChannelTextBase`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `chunk_size` was not given as `int`.
            - If `chunk_size` is out of range [1:].
        """
        return await MessageIterator(self, channel, chunk_size)
    
    
    async def typing(self, channel):
        """
        Sends a typing event to the given channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``ChannelTextBase``, `int`
            The channel where typing will be triggered.
        
        Raises
        ------
        TypeError
            If `channel` was not given neither as ``ChannelTextBase`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        The client will be shown up as typing for 8 seconds, or till it sends a message at the respective channel.
        """
        channel_id = get_channel_id(channel, ChannelTextBase)
        
        await self.http.typing(channel_id)
    
    
    def keep_typing(self, channel, timeout=300.0):
        """
        Returns a context manager which will keep sending typing events at the channel. Can be used to indicate that
        the bot is working.
        
        Parameters
        ----------
        channel ``ChannelTextBase``, `int`
            The channel where typing will be triggered.
        timeout : `float` = `300.0`, Optional
            The maximal duration for the ``Typer`` to keep typing.
        
        Returns
        -------
        typer : ``Typer``
        
        Raises
        ------
        TypeError
            If `channel` was not given neither as ``ChannelTextBase`` nor `int`.
        
        Examples
        --------
        ```py
        with client.keep_typing(channel):
            # Do some things
            await client.message_create(channel, 'Ayaya')
        ```
        """
        channel_id = get_channel_id(channel, ChannelTextBase)
        
        return Typer(self, channel_id, timeout)
    
    # Reactions:
    
    async def reaction_add(self, message, emoji):
        """
        Adds a reaction on the given message.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message : ``Message``, ``MessageRepr``, ``MessageReference``, `tuple` (`int`, `int`)
            The message on which the reaction will be put on.
        emoji : ``Emoji``, `str`
            The emoji to react with.
        
        Raises
        ------
        TypeError
            - If `message` was not given neither as ``Message``, ``MessageRepr`, ``MessageReference`` nor as
                `tuple` (`int`, `int`) instance.
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
        message : ``Message``, ``MessageRepr``, ``MessageReference``, `tuple` (`int`, `int`)
            The message from which the reaction will be removed.
        emoji : ``Emoji``, `str`
            The emoji to remove.
        user : ```ClientUserBase``, `int`
            The user, who's reaction will be removed.
        
        Raises
        ------
        TypeError
            - If `message` was not given neither as ``Message``, ``MessageRepr`, ``MessageReference`` neither as `tuple`
                (`int`, `int`) instance.
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
        message : ``Message``, ``MessageRepr``, ``MessageReference``, `tuple` (`int`, `int`)
            The message from which the reactions will be removed.
        emoji : ``Emoji``, `str`
            The reaction to remove.
        
        Raises
        ------
        TypeError
            - If `message` was not given neither as ``Message``, ``MessageRepr`, ``MessageReference`` neither as `tuple`
                (`int`, `int`) instance.
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
        message : ``Message``, ``MessageRepr``, ``MessageReference``, `tuple` (`int`, `int`)
            The message from which the reaction will be removed.
        emoji : ``Emoji``, `str`
            The emoji to remove.
        
        Raises
        ------
        TypeError
            - If `message` was not given neither as ``Message``, ``MessageRepr`, ``MessageReference`` neither as `tuple`
                (`int`, `int`) instance.
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
        message : ``Message``, ``MessageRepr``, ``MessageReference``, `tuple` (`int`, `int`)
            The message from which the reactions will be cleared.
        
        Raises
        ------
        TypeError
            If `message` was not given neither as ``Message``, ``MessageRepr`, ``MessageReference`` neither as `tuple`
            (`int`, `int`) instance.
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
        message : ``Message``, ``MessageRepr``, ``MessageReference``, `tuple` (`int`, `int`)
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
            - If `message` was not given neither as ``Message``, ``MessageRepr`, ``MessageReference`` neither as `tuple`
                (`int`, `int`) instance.
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
        
        users = [User(user_data) for user_data in data]
        
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
        message : ``Message``, ``MessageRepr``, ``MessageReference``, `tuple` (`int`, `int`)
            The message, what's reactions will be requested.
        emoji : ``Emoji``, `str`
            The emoji, what's reactors will be requested.
        
        Returns
        -------
        users : `list` of ``ClientUserBase``
        
        Raises
        ------
        TypeError
            - If `message` was not given neither as ``Message``, ``MessageRepr`, ``MessageReference`` neither as `tuple`
                (`int`, `int`) instance.
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
            users.extend(User(user_data) for user_data in user_datas)
            
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
        message : ``Message``, ``MessageRepr``, ``MessageReference``, `tuple` (`int`, `int`)
            The message, what's reactions will be requested.
        
        Returns
        -------
        message : ``Message``
        
        Raises
        ------
        TypeError
            If `message` was not given neither as ``Message``, ``MessageRepr`, ``MessageReference`` neither as `tuple`
            (`int`, `int`) instance.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id, message_id = get_channel_id_and_message_id(message)
        message = MESSAGES.get(message_id, None)
        if (message is None):
            message = await self.message_get(channel_id, message_id)
        
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
                    users.extend(User(user_data) for user_data in user_datas)
                    
                    if len(user_datas) < 100:
                        break
                    
                    data['after'] = users[-1].id
                
                reactions._update_all_users(emoji, users)
                users.clear()
        
        return message
    
    
    # Guild
    
    async def guild_preview_get(self, guild):
        """
        Requests the preview of a public guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The id of the guild, what's preview will be requested
        
        Returns
        -------
        preview : ``GuildPreview``
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as ``Guild`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id = get_guild_id(guild)
        
        data = await self.http.guild_preview_get(guild_id)
        return GuildPreview(data)
    
    
    async def guild_user_delete(self, guild, user, *, reason=None):
        """
        Removes the given user from the guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild from where the user will be removed.
        user : ``ClientUserBase``, `int`
            The user to delete from the guild.
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
        
        await self.http.guild_user_delete(guild_id, user_id, reason)
    
    
    async def welcome_screen_get(self, guild):
        """
        Requests the given guild's welcome screen.
        
        You need to have `manage guild` permission to request the welcome screen if the guild has it disabled.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, what's welcome screen will be requested.
        
        Returns
        -------
        welcome_screen : `None`, ``WelcomeScreen``
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as ``Guild`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        If the guild has no welcome screen enabled, will not do any request.
        """
        guild_id = get_guild_id(guild)
        
        welcome_screen_data = await self.http.welcome_screen_get(guild_id)
        if welcome_screen_data is None:
            welcome_screen = None
        else:
            welcome_screen = WelcomeScreen.from_data(welcome_screen_data)
        
        return welcome_screen
    
    
    async def welcome_screen_edit(self, guild, *, enabled=..., description=..., welcome_channels=...):
        """
        Edits the given guild's welcome screen.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, what's welcome screen will be edited.
        enabled : `bool`, Optional (Keyword only)
            Whether the guild's welcome screen should be enabled.
        description : `None`, `str`, Optional (Keyword only)
            The welcome screen's new description. It's length can be in range [0:140].
        welcome_channels : `None`, ``WelcomeChannel`` or  (`tuple`, `list`) of ``WelcomeChannel``
                , Optional (Keyword only)
            The channels mentioned on the welcome screen.
        
        Returns
        -------
        welcome_screen : `None or ``WelcomeScreen``
            The updated welcome screen. Always returns `None` if no change was propagated.
        
        Raises
        ------
        TypeError
            - If `guild` was not given neither as ``Guild`` nor `int`.
            - If `welcome_channels` was not given neither as `None`, ``WelcomeChannel`` nor as (`tuple`, `list`) of
                ``WelcomeChannel``-s.
            - If `welcome_channels` contains a non ``WelcomeChannel``.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `enabled` was not given as `bool`.
            - If `description` was not given neither as `None`, `str`.
            - If `description`'s length is out of range [0:140].
            - If `welcome_channels`'s length is out of range [0:5].
        """
        guild_id = get_guild_id(guild)
        
        data = {}
        
        if (enabled is not ...):
            if __debug__:
                if not isinstance(enabled, bool):
                    raise AssertionError(
                        f'`enabled` can be `bool`, got {enabled.__class__.__name__}; {enabled!r}.'
                    )
            
            data['enabled'] = enabled
        
        if (description is not ...):
            if __debug__:
                if (description is not None):
                    if not isinstance(description, str):
                        raise AssertionError(
                            f'`description` can be `None`, `str`, got {description.__class__.__name__}; '
                            f'{description!r}.'
                        )
                
                    description_length = len(description)
                    if description_length > 300:
                        raise AssertionError(
                            f'`description` length can be in range [0:140], got {description_length!r}; '
                            f'{description!r}.'
                        )
                
            if (description is not None) and (not description):
                description = None
            
            data['description'] = description
        
        if (welcome_channels is not ...):
            welcome_channel_datas = []
            if welcome_channel_datas is None:
                pass
            elif isinstance(welcome_channels, WelcomeChannel):
                welcome_channel_datas.append(welcome_channels.to_data())
            elif isinstance(welcome_channels, (list, tuple)):
                if __debug__:
                    welcome_channels_length = len(welcome_channels)
                    if welcome_channels > 5:
                        raise AssertionError(
                            f'`welcome_channels` length can be in range [0:5], got '
                            f'{welcome_channels_length!r}; {welcome_channels!r}.'
                        )
                
                for index, welcome_channel in enumerate(welcome_channels):
                    if not isinstance(welcome_channel, WelcomeChannel):
                        raise TypeError(
                            f'`welcome_channels[{index}]` is not `{WelcomeChannel.__name__}` , got '
                            f'{welcome_channel.__class__.__name__}; {welcome_channel!r}; '
                            f'welcome_channels={welcome_channels!r}.'
                        )
                    
                    welcome_channel_datas.append(welcome_channel.to_data())
            else:
                raise TypeError(
                    f'`welcome_channels` can be `None`, `{WelcomeChannel.__name__}`, '
                    f'(`list`, `tuple`) of `{WelcomeChannel.__name__}, got '
                    f'{welcome_channels.__class__.__name__}; {welcome_channels!r}.'
                )
            
            data['welcome_channels'] = welcome_channel_datas
        
        if data:
            data = await self.http.welcome_screen_edit(guild_id, data)
            if data:
                welcome_screen = WelcomeScreen.from_data(data)
            else:
                welcome_screen = None
        else:
            welcome_screen = None
        
        return welcome_screen
    
    
    async def verification_screen_get(self, guild):
        """
        Requests the given guild's verification screen.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, what's verification screen will be requested.

        Returns
        -------
        verification_screen : `None`, ``VerificationScreen``
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as ``Guild`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        If the guild has no verification screen enabled, will not do any request.
        """
        guild, guild_id = get_guild_and_id(guild)
        
        if (guild is None) or (GuildFeature.verification_screen_enabled in guild.features):
            verification_screen_data = await self.http.verification_screen_get(guild_id)
            if verification_screen_data is None:
                verification_screen = None
            else:
                verification_screen = VerificationScreen.from_data(verification_screen_data)
        else:
            verification_screen = None
        
        return verification_screen
    
    
    async def verification_screen_edit(self, guild, *, enabled=..., description=..., steps=...):
        """
        Requests the given guild's verification screen.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, what's verification screen will be requested.
        enabled : `bool`, Optional (Keyword only)
            Whether the guild should have verification screen enabled.
        description : `None`, `str`, Optional (Keyword only)
            The guild's new description showed on the verification screen. It's length can be in range [0:300].
        steps : `None`, ``VerificationScreenStep`` or  (`tuple`, `list`) of ``VerificationScreenStep``
                , Optional (Keyword only)
            The new steps of the verification screen.
        
        Returns
        -------
        verification_screen : `None`, ``VerificationScreen``
            The updated verification screen. Always returns `None` if no change was propagated.
        
        Raises
        ------
        TypeError
            - If `guild` was not given neither as ``Guild`` nor `int`.
            - If `steps` was not given neither as `None`, ``VerificationScreenStep`` nor as (`tuple`, `list`) of
                ``VerificationScreenStep``-s.
            - If `steps` contains a non ``VerificationScreenStep``.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `enabled` was not given as `bool`.
            - If `description` was not given neither as `None`, `str`.
            - If `description`'s length is out of range [0:300].
        
        Notes
        -----
        When editing steps, `DiscordException Internal Server Error (500): 500: Internal Server Error` will be dropped.
        """
        guild_id = get_guild_id(guild)
        
        data = {}
        
        if (enabled is not ...):
            if __debug__:
                if not isinstance(enabled, bool):
                    raise AssertionError(
                        f'`enabled` can be `bool`, got {enabled.__class__.__name__}; {enabled!r}.'
                    )
            
            data['enabled'] = enabled
        
        if (description is not ...):
            if __debug__:
                if (description is not None):
                    if not isinstance(description, str):
                        raise AssertionError(
                            f'`description` can be `None`, `str`, got {description.__class__.__name__}; '
                            f'{description!r}.'
                        )
                    
                    description_length = len(description)
                    if description_length > 300:
                        raise AssertionError(
                            f'`description` length can be in range [0:300], got '
                            f'{description_length!r}; {description!r}.'
                        )
            
            if (description is not None) and (not description):
                description = None
            
            data['description'] = description
        
        if (steps is not ...):
            step_datas = []
            if steps is None:
                pass
        
            elif isinstance(steps, VerificationScreenStep):
                step_datas.append(steps.to_data())
            
            elif isinstance(steps, (list, tuple)):
                for index, step in enumerate(steps):
                    if not isinstance(step, VerificationScreenStep):
                        raise TypeError(
                            f'`steps[{index}]` is not `{VerificationScreenStep.__name__}`, got '
                            f'{step.__class__.__name__}; {step!r}; steps={steps!r}.'
                        )
                    
                    step_datas.append(step.to_data())
            else:
                raise TypeError(
                    f'`steps` can be `None`, `{VerificationScreenStep.__name__}`, '
                    f'(`list`, `tuple`) of `{VerificationScreenStep.__name__}, got '
                    f'{steps.__class__.__name__}; {steps!r}.'
                )
            
            data['form_fields'] = step_datas
        
        if data:
            data['version'] = datetime_to_timestamp(datetime.utcnow())
            data = await self.http.verification_screen_edit(guild_id, data)
            if data is None:
                verification_screen = None
            else:
                verification_screen = VerificationScreen.from_data(data)
        else:
            verification_screen = None
        
        return verification_screen
    
    
    async def guild_ban_add(self, guild, user, *, delete_message_days=0, reason=None):
        """
        Bans the given user from the guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild from where the user will be banned.
        user : ``ClientUserBase``, `int`
            The user to ban from the guild.
        delete_message_days : `int` = `0`, Optional (Keyword only)
            How much days back the user's messages should be deleted. Can be in range [0:7].
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
        AssertionError
            - `delete_message_days` was not given as `int`.
            - `delete_message_days` is out of range [0:delete_message_days].
        """
        guild_id = get_guild_id(guild)
        user_id = get_user_id(user)
        
        if __debug__:
            if not isinstance(delete_message_days, int):
                raise AssertionError(
                    f'`delete_message_days` can be `int`, got {delete_message_days.__class__.__name__}; '
                    f'{delete_message_days!r}.'
                )
        
        data = {}
        
        if delete_message_days:
            if __debug__:
                if delete_message_days < 1 or delete_message_days > 7:
                    raise AssertionError(
                        f'`delete_message_days` can be in range [0:7], got {delete_message_days!r}.'
                    )
            
            data['delete_message_days'] = delete_message_days
        
        if (reason is not None) and reason:
            data['reason'] = reason
        
        await self.http.guild_ban_add(guild_id, user_id, data, reason)
    
    
    async def guild_ban_delete(self, guild, user, *, reason=None):
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
        
        await self.http.guild_ban_delete(guild_id, user_id, reason)
    
    
    async def guild_get(self, guild):
        """
        Gets or updates the guild.
        
        > The client must be in the guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild to request.
        
        Returns
        -------
        guild : ``Guild``
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as ``Guild`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
        """
        guild, guild_id = get_guild_and_id(guild)
        data = await self.http.guild_get(guild_id, {'with_counts': True})
        
        if guild is None:
            channel_datas = await self.http.guild_channel_get_all(guild_id)
            data['channels'] = channel_datas
            user_data = await self.http.guild_user_get(guild_id, self.id)
            data['members'] = [user_data]
            guild = Guild(data, self)
        else:
            guild._sync(data)
        
        return guild
    
    
    async def guild_sync(self, guild):
        """
        Syncs a guild by it's id with the wrapper. Used internally if de-sync is detected when parsing dispatch events.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild to sync.

        Returns
        -------
        guild : ``Guild``
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as ``Guild`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        # sadly guild_get does not returns channel and voice state data at least we can request the channels
        guild, guild_id = get_guild_and_id(guild)
        
        if guild is None:
            data = await self.http.guild_get(guild_id, None)
            channel_datas = await self.http.guild_channel_get_all(guild_id)
            data['channels'] = channel_datas
            user_data = await self.http.guild_user_get(guild_id, self.id)
            data['members'] = [user_data]
            guild = Guild(data, self)
        else:
            data = await self.http.guild_get(guild_id, None)
            guild._sync(data)
            channel_datas = await self.http.guild_channel_get_all(guild_id)
            guild._sync_channels(channel_datas)
            
            user_data = await self.http.guild_user_get(guild_id, self.id)
            try:
                profile = self.guild_profiles[guild.id]
            except KeyError:
                self.guild_profiles[guild.id] = GuildProfile(user_data)
                if guild not in guild.clients:
                    guild.clients.append(self)
            else:
                profile._update_attributes(user_data)
        
        return guild

##    # Disable user syncing, takes too much time
##    async def _guild_sync_post_process(self, guild):
##        for client in CLIENTS.values():
##            try:
##                user_data = await self.http.guild_user_get(guild.id, client.id)
##           except (DiscordException, ConnectionError):
##                continue
##            try:
##                profile = client.guild_profiles[guild.id]
##            except KeyError:
##                client.guild_profiles[guild.id] = GuildProfile(user_data)
##                if client not in guild.clients:
##                    guild.clients.append(client)
##            else:
##                profile._update_attributes(user_data)
##
##        if not CACHE_USER:
##            return
##
##        old_ids = set(guild.users)
##        data = {'limit': 1000, 'after': '0'}
##        while True:
##            user_datas = await self.http.guild_users(guild.id, data)
##            for user_data in user_datas:
##                user = User._create_and_update(user_data, guild)
##                try:
##                    old_ids.remove(user.id)
##                except KeyError:
##                    pass
##
##             if len(user_datas)< 1 000:
##                 break
##
##             data['after'] = user_datas[999]['user']['id']
##
##        del data
##
##        for id_ in old_ids:
##            try:
##               user = guild.users.pop(id_)
##           except KeyError:
##               continue #huh?
##           try:
##               del user.guild_profiles[guild.id]
##           except KeyError:
##               pass # huh??
    
    async def guild_leave(self, guild):
        """
        The client leaves the given guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild from where the client will leave.
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as ``Guild`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id = get_guild_id(guild)
        
        await self.http.guild_leave(guild_id)
    
    
    async def guild_delete(self, guild):
        """
        Deletes the given guild. The client must be the owner of the guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild to delete.
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as ``Guild`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id = get_guild_id(guild)
        
        await self.http.guild_delete(guild_id)
    
    
    async def guild_create(self, name, *, icon=None, roles=None, channels=None, afk_channel_id=None,
            system_channel_id=None, afk_timeout=None, region=VoiceRegion.eu_central,
            verification_level=VerificationLevel.medium, message_notification=MessageNotificationLevel.only_mentions,
            content_filter=ContentFilterLevel.disabled, boost_progress_bar_enabled=None):
        """
        Creates a guild with the given parameter. Bot accounts can create guilds only when they have less than 10.
        User account guild limit is 100, meanwhile staff guild limit is 200.
        
        This method is a coroutine.
        
        Parameters
        ----------
        name : `str`
            The name of the new guild.
        icon : `None`, `bytes-like` = `None`, Optional (Keyword only)
            The icon of the new guild.
        roles : `None`, `list` of ``cr_p_role_object`` returns = `None`, Optional (Keyword only)
            A list of roles of the new guild. It should contain json serializable roles made by the
            ``cr_p_role_object`` function.
        channels : `None`, `list` of ``cr_pg_channel_object`` returns = `None`, Optional (Keyword only)
            A list of channels of the new guild.  It should contain json serializable channels made by the
            ``cr_p_role_object`` function.
        afk_channel_id : `None`, `int` = `None`, Optional (Keyword only)
            The id of the guild's afk channel. The id should be one of the channel's id from `channels`.
        system_channel_id: `int`, Optional (Keyword only)
            The id of the guild's system channel. The id should be one of the channel's id from `channels`.
        afk_timeout : `None`, `int` = `None`, Optional (Keyword only)
            The afk timeout for the users at the guild's afk channel.
        region : ``VoiceRegion``, `str` = `VoiceRegion.eu_central`, Optional (Keyword only)
            The voice region of the new guild.
        verification_level : ``VerificationLevel``, `int` = `VerificationLevel.medium`, Optional (Keyword only)
            The verification level of the new guild.
        message_notification : ``MessageNotificationLevel``, `int` = `MessageNotificationLevel.only_mentions`
                , Optional (Keyword only)
            The message notification level of the new guild.
        content_filter : ``ContentFilterLevel``, `int` = `ContentFilterLevel.disabled`, Optional (Keyword only)
            The content filter level of the guild.
        boost_progress_bar_enabled : `None`, `bool` = `None`, Optional (Keyword only)
            Whether the guild has the boost progress bar should be enabled.
        
        Returns
        -------
        guild : ``Guild`` object
            A partial guild made from the received data.
        
        Raises
        ------
        TypeError
            - If `icon` is neither `None`, `bytes-like`.
            - If `region` was not given neither as ``VoiceRegion`` nor `str`.
            - If `verification_level` was not given neither as ``VerificationLevel`` not `int`.
            - If `content_filter` was not given neither as ``ContentFilterLevel`` not `int`.
            - If `message_notification` was not given neither as ``MessageNotificationLevel`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If the client cannot create more guilds.
            - If `name` was not given as `str`.
            - If the `name`'s length is out of range [2:100].
            - If `icon` is passed as `bytes-like`, but it's format is not a valid image format.
            - If `afk-timeout` was not given as `int`.
            - If `afk_timeout` was passed and not as one of: `60, 300, 900, 1800, 3600`.
            - If `boost_progress_bar_enabled` was not given as `bool`.
        """
        if __debug__:
            if self.is_bot:
                guild_create_limit = 10
            elif self.flags.staff:
                guild_create_limit = 200
            elif (self.premium_type is PremiumType.nitro):
                guild_create_limit = 200
            else:
                guild_create_limit = 100
            
            if len(self.guilds) >= guild_create_limit:
                raise AssertionError(
                    f'Guild count over creation limit; limit={guild_create_limit}; count={len(self.guilds)!r}.'
                )
        
        
        if __debug__:
            if not isinstance(name, str):
                raise AssertionError(
                    f'`name` can be `str`, got {name.__class__.__name__}; {name!r}.'
                )
            
            name_length = len(name)
            if name_length < 2 or name_length > 100:
                raise AssertionError(
                    f'`name` length can be in range [2:100], got {name_length!r}; {name!r}.'
                )
        
        
        if icon is None:
            icon_data = None
        else:
            icon_type = icon.__class__
            if not issubclass(icon_type, (bytes, bytearray, memoryview)):
                raise TypeError(
                    f'`icon` can be `None`, `bytes-like`, got {icon_type.__name__}; {reprlib.repr(icon)}.'
                )
            
            if __debug__:
                media_type = get_image_media_type(icon)
                if media_type not in VALID_ICON_MEDIA_TYPES:
                    raise AssertionError(
                        f'Invalid `icon` type: {media_type}; {reprlib.repr(icon)}.'
                    )
            
            icon_data = image_to_base64(icon)
        
        
        if isinstance(region, VoiceRegion):
            region_value = region.value
        elif isinstance(region, str):
            region_value = region
        else:
            raise TypeError(
                f'`region` can be `{VoiceRegion.__name__}`, `str`, got '
                f'{region.__class__.__name__}; {region!r}.'
            )
        
        
        if isinstance(verification_level, VerificationLevel):
            verification_level_value = verification_level.value
        elif isinstance(verification_level, int):
            verification_level_value = verification_level
        else:
            raise TypeError(
                f'`verification_level` can be `{VerificationLevel.__name__}`, `int`, got '
                f'{verification_level.__class__.__name__}; {verification_level!r}.'
            )
        
        
        if isinstance(message_notification, MessageNotificationLevel):
            message_notification_value = message_notification.value
        elif isinstance(message_notification, int):
            message_notification_value = message_notification
        else:
            raise TypeError(
                f'`message_notification` can be `{MessageNotificationLevel.__name__}`, `int`, got '
                f'{message_notification.__class__.__name__}; {message_notification!r}.'
            )
        
        
        if isinstance(content_filter, ContentFilterLevel):
            content_filter_value = content_filter.value
        elif isinstance(content_filter, int):
            content_filter_value = content_filter
        else:
            raise TypeError(
                f'`content_filter` can be {ContentFilterLevel.__name__}, `int` , got '
                f'{content_filter.__class__.__name__}; {content_filter!r}.'
            )
        
        if roles is None:
            roles = []
        
        if channels is None:
            channels = []
        
        data = {
            'name': name,
            'icon': icon_data,
            'region': region_value,
            'verification_level': verification_level_value,
            'default_message_notifications': message_notification_value,
            'explicit_content_filter': content_filter_value,
            'roles': roles,
            'channels': channels,
        }
        
        if (afk_channel_id is not None):
            if __debug__:
                if not isinstance(afk_channel_id, int):
                    raise AssertionError(
                        f'`afk_channel_id` can be `int`, got {afk_channel_id.__class__.__name__}; {afk_channel_id!r}.'
                    )
            
            data['afk_channel_id'] = afk_channel_id
        
        if (system_channel_id is not None):
            if __debug__:
                if not isinstance(system_channel_id, int):
                    raise AssertionError(
                        f'`system_channel_id` can be `int`, got {system_channel_id.__class__.__name__}; '
                        f'{system_channel_id!r}.'
                    )
            
            data['system_channel_id'] = system_channel_id
        
        if (afk_timeout is not None):
            if __debug__:
                if not isinstance(afk_timeout, int):
                    raise AssertionError(
                        f'`afk_timeout` can be `int`, got {afk_timeout.__class__.__name__}; {afk_timeout!r}.'
                    )
                
                if afk_timeout not in (60, 300, 900, 1800, 3600):
                    raise AssertionError(
                        f'`afk_timeout` can be 60, 300, 900, 1800, 3600 seconds; got {afk_timeout!r}.'
                    )
            
            data['afk_timeout'] = afk_timeout
        
        if (boost_progress_bar_enabled is not None):
            if __debug__:
                if not isinstance(boost_progress_bar_enabled, bool):
                    raise AssertionError(
                        f'`boost_progress_bar_enabled` can be `bool`, got '
                        f'{boost_progress_bar_enabled.__class__.__name__}; {boost_progress_bar_enabled!r}.'
                    )
            
            data['premium_progress_bar_enabled'] = boost_progress_bar_enabled
        
        
        data = await self.http.guild_create(data)
        # we can create only partial, because the guild data is not completed usually
        return create_partial_guild_from_data(data)
    
    
    async def guild_prune(self, guild, days, *, roles=None, count=False, reason=None):
        """
        Kicks the members of the guild which were inactive since x days.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            Where the pruning will be executed.
        days : `int`
            The amount of days since at least the users need to inactive. Can be in range [1:30].
        roles : `None`, `list` of (``Role``, `int`) = `None`, Optional (Keyword only)
            By default pruning will kick only the users without any roles, but it can defined which roles to include.
        count : `bool` = `False`, Optional (Keyword only)
            Whether the method should return how much user were pruned, but if the guild is large it will be set to
            `False` anyways. Defaults to `False`.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Will show up at the guild's audit logs.
        
        Returns
        -------
        count : `None`, `int`
            The number of pruned users or `None` if `count` is set to `False`.
        
        Raises
        ------
        TypeError
            - If `guild` was not given neither as ``Guild`` nor `int`.
            - If `roles` contain not ``Role``, neither `int` element.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `roles` was given neither as `None`, `list`.
            - If `count` was not given as `bool`.
            - If `days` was not given as `int`.
            - If `days` is out of range [1:30].
        
        See Also
        --------
        ``.guild_prune_estimate`` : Returns how much user would be pruned if ``.guild_prune`` would be called.
        """
        guild, guild_id = get_guild_and_id(guild)
        
        if __debug__:
            if not isinstance(count, bool):
                raise AssertionError(
                    f'`count` can be `bool`, got {count.__class__.__name__}; {count!r}.'
                )
        
        if count and (guild is not None) and guild.is_large:
            count = False
        
        if __debug__:
            if not isinstance(days, int):
                raise AssertionError(
                    f'``days` can be `int`, got {days.__class__.__name__}; {days!r}.'
                )
            
            if days < 1 or days > 30:
                raise AssertionError(
                    f'`days can be in range [1:30], got {days!r}.'
                )
        
        data = {
            'days': days,
            'compute_prune_count': count,
        }
        
        if (roles is not None):
            if __debug__:
                if not isinstance(roles, list):
                    raise AssertionError(
                        f'`roles` can be `None`m `list` of (`{Role.__name__}`, `int`)'
                        f', got {roles.__class__.__name__}; {roles!r}.')
            
            role_ids = set()
            for index, role in enumerate(roles):
                if isinstance(role, Role):
                    role_id = role.id
                else:
                    role_id = maybe_snowflake(role)
                    if role_id is None:
                        raise TypeError(
                            f'`roles[{index}]` is not `{Role.__name__}`, `int`,'
                            f' got {role.__class__.__name__}; {role!r}; roles={roles!r}.'
                        )
                
                role_ids.add(role_id)
            
            if role_ids:
                data['include_roles'] = role_ids
        
        data = await self.http.guild_prune(guild_id, data, reason)
        return data.get('pruned', None)
    
    
    async def guild_prune_estimate(self, guild, days, *, roles=None):
        """
        Returns the amount users, who would been pruned, if ``.guild_prune`` would be called.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`.
            Where the counting of prunable users will be done.
        days : `int`
            The amount of days since at least the users need to inactive. Can be in range [1:30].
        roles : `None`, `list` of (``Role``, `int`) = `None`, Optional (Keyword only)
            By default pruning would kick only the users without any roles, but it can be defined which roles to
            include.
        
        Returns
        -------
        count : `int`
            The amount of users who would be pruned.
        
        Raises
        ------
        TypeError
            - If `guild` was not given neither as ``Guild`` nor `int`.
            - If `roles` contain not ``Role``, neither `int` element.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `roles` was given neither as `None`, `list`.
            - If `days` was not given as `int`.
            - If `days` is out of range [1:30].
        """
        guild_id = get_guild_id(guild)
        
        if __debug__:
            if not isinstance(days, int):
                raise AssertionError(f'`days can be `int`, got {days.__class__.__name__}.')
            
            if days < 1 or days > 30:
                raise AssertionError(f'`days can be in range [1:30], got {days!r}.')
        
        data = {
            'days': days,
        }
        
        if (roles is not None):
            if __debug__:
                if not isinstance(roles, list):
                    raise AssertionError(
                        f'`roles` can be `None`, `list` of (`{Role.__name__}`, `int`)'
                        f', got {roles.__class__.__name__}; {roles!r}.'
                    )
            
            role_ids = set()
            for role in roles:
                role_id = get_role_id(role)
                role_ids.add(role_id)
            
            if role_ids:
                data['include_roles'] = role_ids
        
        data = await self.http.guild_prune_estimate(guild_id, data)
        return data.get('pruned', None)
    
    
    async def guild_edit(self, guild, *, name=..., icon=..., invite_splash=..., discovery_splash=..., banner=...,
            afk_channel=..., system_channel=..., rules_channel=..., public_updates_channel=..., owner=..., region=...,
            afk_timeout=..., verification_level=..., content_filter=..., message_notification=..., description=...,
            preferred_locale=..., system_channel_flags=..., add_feature=..., remove_feature=...,
            boost_progress_bar_enabled=..., reason=None):
        """
        Edits the guild with the given parameters.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild to edit.
        name : `str`, Optional (Keyword only)
            The guild's new name.
        icon : `None`, `bytes-like`, Optional (Keyword only)
            The new icon of the guild. Can be `'jpg'`, `'png'`, `'webp'` image's raw data. If the guild has
            `ANIMATED_ICON` feature, it can be `'gif'` as well. By passing `None` you can remove the current one.
        invite_splash : `None`, `bytes-like`, Optional (Keyword only)
            The new invite splash of the guild. Can be `'jpg'`, `'png'`, `'webp'` image's raw data. The guild must have
            `INVITE_SPLASH` feature. By passing it as `None` you can remove the current one.
        discovery_splash : `None`, `bytes-like`, Optional (Keyword only)
            The new splash of the guild. Can be `'jpg'`, `'png'`, `'webp'` image's raw data. The guild must have
            `DISCOVERABLE` feature. By passing it as `None` you can remove the current one.
        banner : `None`, `bytes-like`, Optional (Keyword only)
            The new banner of the guild. Can be `'jpg'`, `'png'`, `'webp'` image's raw data. The guild must have
            `BANNER` feature. By passing it as `None` you can remove the current one.
        afk_channel : `None`, ``ChannelVoice``, `int`, Optional (Keyword only)
            The new afk channel of the guild. You can remove the current one by passing is as `None`.
        system_channel : `None`, ``ChannelText``, `int`, Optional (Keyword only)
            The new system channel of the guild. You can remove the current one by passing is as `None`.
        rules_channel : `None`, ``ChannelText``, `int`, Optional (Keyword only)
            The new rules channel of the guild. The guild must be a Community guild. You can remove the current
            one by passing is as `None`.
        public_updates_channel : `None`, ``ChannelText``, `int`, Optional (Keyword only)
            The new public updates channel of the guild. The guild must be a Community guild. You can remove the
            current one by passing is as `None`.
        owner : ``ClientUserBase``, `int`, Optional (Keyword only)
            The new owner of the guild. You must be the owner of the guild to transfer ownership.
        region : ``VoiceRegion``, Optional (Keyword only)
            The new voice region of the guild.
        afk_timeout : `int`, Optional (Keyword only)
            The new afk timeout for the users at the guild's afk channel.
            
            Can be one of: `60, 300, 900, 1800, 3600`.
        verification_level : ``VerificationLevel``, `int`, Optional (Keyword only)
            The new verification level of the guild.
        content_filter : ``ContentFilterLevel``, `int`, Optional (Keyword only)
            The new content filter level of the guild.
        message_notification : ``MessageNotificationLevel``, Optional (Keyword only)
            The new message notification level of the guild.
        description : `None`, `str`, Optional (Keyword only)
            The new description of the guild. By passing `None`, or an empty string you can remove the current one. The
            guild must be a Community guild.
        preferred_locale : `str`, Optional (Keyword only)
            The guild's preferred locale. The guild must be a Community guild.
        system_channel_flags : ``SystemChannelFlag``, Optional (Keyword only)
            The guild's system channel's new flags.
        add_feature : (`str`, ``GuildFeature``) or (`iterable` of (`str`, ``GuildFeature``)), Optional (Keyword only)
            Guild feature(s) to add to the guild.
            
            If `guild` is given as an id, then `add_feature` should contain all the features of the guild to set.
        remove_feature : (`str`, ``GuildFeature``) or (`iterable` of (`str`, ``GuildFeature``)), Optional (Keyword only)
            Guild feature(s) to remove from the guild's.
        boost_progress_bar_enabled : `bool`, Optional (Keyword only)
            Whether the guild has the boost progress bar should be enabled.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the guild's audit logs.
        
        Raises
        ------
        TypeError
            - If `guild` was not given neither as ``Guild``, `str`.
            - If `icon`, `invite_splash`, `discovery_splash`, `banner` is neither `None`, `bytes-like`.
            - If `add_feature`, `remove_feature` was not given neither as `str`, ``GuildFeature``,
                `iterable` of `str`, ``GuildFeature``-s.
            - If `afk_channel` was given, but not as `None`, ``ChannelVoice``, neither as `int`.
            - If `system_channel`, `rules_channel`, `public_updates_channel` was given, but not as `None`,
                ``ChannelText``, neither as `int`.
            - If `owner` was not given neither as ``ClientUserBase``, `int`.
            - If `region` was given neither as ``VoiceRegion``, `str`.
            - If `verification_level` was not given neither as ``VerificationLevel``, `int`.
            - If `content_filter` was not given neither as ``ContentFilterLevel``, `int`.
            - If `description` was not given either as `None`, `str`.
        AssertionError
            - If `icon`, `invite_splash`, `discovery_splash`, `banner` was passed as `bytes-like`, but it's format
                is not any of the expected formats.
            - If `banner` was given meanwhile the guild has no `BANNER` feature.
            - If `rules_channel`, `description`, `preferred_locale`, `public_updates_channel` was passed meanwhile
                the guild is not Community guild.
            - If `owner` was passed meanwhile the client is not the owner of the guild.
            - If `afk_timeout` was passed and not as one of: `60, 300, 900, 1800, 3600`.
            - If `name` is shorter than `2` or longer than `100` characters.
            - If `discovery_splash` was given meanwhile the guild is not discoverable.
            - If `invite_splash` was passed meanwhile the guild has no `INVITE_SPLASH` feature.
            - If `name` was not given as `str`.
            - If `afk_timeout` was not given as `int`.
            - If `system_channel_flags` was not given as `SystemChannelFlag`, `int`.
            - If `preferred_locale` was not given as `str`.
            - If `boost_progress_bar_enabled` was not given as `bool`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        data = {}
        
        guild, guild_id = get_guild_and_id(guild)
        
        if (name is not ...):
            if __debug__:
                if not isinstance(name, str):
                    raise AssertionError(
                        f'`name` can be `str`, got {name.__class__.__name__}; {name!r}.'
                    )
                
                name_length = len(name)
                if name_length < 2 or name_length > 100:
                    raise ValueError(
                        f'Guild\'s name\'s length can be between 2-100, got {name_length}: {name!r}.'
                    )
            
            data['name'] = name
        
        
        if (icon is not ...):
            if icon is None:
                icon_data = None
            
            else:
                if not isinstance(icon, (bytes, bytearray, memoryview)):
                    raise TypeError(
                        f'`icon` can be `None`, `bytes-like`, got {icon.__class__.__name__}; {reprlib.repr(icon)}.'
                    )
                
                if __debug__:
                    media_type = get_image_media_type(icon)
                    
                    if guild is None:
                        valid_icon_media_types = VALID_ICON_MEDIA_TYPES_EXTENDED
                    else:
                        if GuildFeature.animated_icon in guild.features:
                            valid_icon_media_types = VALID_ICON_MEDIA_TYPES_EXTENDED
                        else:
                            valid_icon_media_types = VALID_ICON_MEDIA_TYPES
                    
                    if media_type not in valid_icon_media_types:
                        raise AssertionError(
                            f'Invalid `icon` type for the guild: {media_type}; got {reprlib.repr(icon)}.'
                        )
                
                icon_data = image_to_base64(icon)
            
            data['icon'] = icon_data
        
        
        if (banner is not ...):
            if __debug__:
                if (guild is not None) and (GuildFeature.banner not in guild.features):
                    raise AssertionError(
                        f'The guild has no `BANNER` feature, meanwhile `banner` is given; got {reprlib.repr(banner)}; '
                        f'guild={guild!r}.'
                    )
            
            if banner is None:
                banner_data = None
            else:
                if not isinstance(banner, (bytes, bytearray, memoryview)):
                    raise TypeError(
                        f'`banner` can be `None`, `bytes-like`, got '
                        f'{banner.__class__.__name__}; got {reprlib.repr(banner)}.'
                    )
                
                if __debug__:
                    media_type = get_image_media_type(banner)
                    if media_type not in VALID_ICON_MEDIA_TYPES:
                        raise AssertionError(
                            f'Invalid `banner` type: {media_type}; got {reprlib.repr(banner)}.'
                        )
                
                banner_data = image_to_base64(banner)
            
            data['banner'] = banner_data
        
        
        if (invite_splash is not ...):
            if __debug__:
                if (guild is not None) and (GuildFeature.invite_splash not in guild.features):
                    raise AssertionError(
                        f'The guild has no `INVITE_SPLASH` feature, meanwhile `invite_splash` is given; got '
                        f'{reprlib.repr(invite_splash)}; guild={guild!r}.'
                    )
            
            if invite_splash is None:
                invite_splash_data = None
            else:
                if not isinstance(invite_splash, (bytes, bytearray, memoryview)):
                    raise TypeError(
                        f'`invite_splash` can be `None`, `bytes-like`, got '
                        f'{invite_splash.__class__.__name__}; {reprlib.repr(invite_splash)}.'
                    )
                
                if __debug__:
                    media_type = get_image_media_type(invite_splash)
                    if media_type not in VALID_ICON_MEDIA_TYPES:
                        raise AssertionError(
                            f'Invalid `invite_splash` type: {media_type}; got {reprlib.repr(invite_splash)}.'
                        )
                
                invite_splash_data = image_to_base64(invite_splash)
            
            data['splash'] = invite_splash_data
        
        
        if (discovery_splash is not ...):
            if __debug__:
                if (guild is not None) and (GuildFeature.discoverable not in guild.features):
                    raise AssertionError(
                        f'The guild is not discoverable, but `discovery_splash` was given; '
                        f'got {reprlib.repr(discovery_splash)}; guild={guild!r}.'
                    )
            
            if discovery_splash is None:
                discovery_splash_data = None
            else:
                if not isinstance(discovery_splash, (bytes, bytearray, memoryview)):
                    raise TypeError(
                        f'`discovery_splash` can be `None`, `bytes-like`, got '
                        f'{discovery_splash.__class__.__name__}; {reprlib.repr(discovery_splash)}.'
                    )
                
                if __debug__:
                    media_type = get_image_media_type(discovery_splash)
                    if media_type not in VALID_ICON_MEDIA_TYPES:
                        raise AssertionError(
                            f'Invalid `discovery_splash` type: {media_type}; got {reprlib.repr(discovery_splash)}.'
                        )
                
                discovery_splash_data = image_to_base64(discovery_splash)
            
            data['discovery_splash'] = discovery_splash_data
        
        
        if (afk_channel is not ...):
            if afk_channel is None:
                afk_channel_id = None
            elif isinstance(afk_channel, ChannelVoice):
                afk_channel_id = afk_channel.id
            else:
                afk_channel_id = maybe_snowflake(afk_channel)
                if afk_channel_id is None:
                    raise TypeError(
                        f'`afk_channel` can be `None`, `{ChannelVoice.__name__}`, `int` , got '
                        f'{afk_channel.__class__.__name__}; {afk_channel!r}.')
            
            data['afk_channel_id'] = afk_channel_id
        
        
        if (system_channel is not ...):
            if system_channel is None:
                system_channel_id = None
            elif isinstance(system_channel, ChannelText):
                system_channel_id = system_channel.id
            else:
                system_channel_id = maybe_snowflake(system_channel)
                if system_channel_id is None:
                    raise TypeError(
                        f'`system_channel` can be `None`, `{ChannelText.__name__}`, `int`, got '
                        f'{system_channel.__class__.__name__}; {system_channel!r}.'
                    )
            
            data['system_channel_id'] = system_channel_id
        
        
        if (rules_channel is not ...):
            if __debug__:
                if (guild is not None) and (not COMMUNITY_FEATURES.intersection(guild.features)):
                    raise AssertionError(
                        f'The guild is not Community guild and `rules_channel` was given; got {rules_channel!r}; '
                        f'guild={guild!r}.'
                    )
            
            if rules_channel is None:
                rules_channel_id = None
            elif isinstance(rules_channel, ChannelText):
                rules_channel_id = rules_channel.id
            else:
                rules_channel_id = maybe_snowflake(rules_channel)
                if rules_channel_id is None:
                    raise TypeError(
                        f'`rules_channel` can be `None`, `{ChannelText.__name__}`, `int` , got '
                        f'{rules_channel.__class__.__name__}.'
                    )
            
            data['rules_channel_id'] = rules_channel_id
        
        
        if (public_updates_channel is not ...):
            if __debug__:
                if (guild is not None) and (not COMMUNITY_FEATURES.intersection(guild.features)):
                    raise AssertionError(
                        f'The guild is not Community guild and `public_updates_channel` was given, got '
                        f'{public_updates_channel!r}; guild={guild!r}.'
                    )
            
            if public_updates_channel is None:
                public_updates_channel_id = None
            elif isinstance(public_updates_channel, ChannelText):
                public_updates_channel_id = public_updates_channel.id
            else:
                public_updates_channel_id = maybe_snowflake(public_updates_channel)
                if public_updates_channel_id is None:
                    raise TypeError(
                        f'`public_updates_channel` can be `None`, `{ChannelText.__name__}`, `int`, got '
                        f'{public_updates_channel.__class__.__name__}; {public_updates_channel!r}.'
                    )
            
            data['public_updates_channel_id'] = public_updates_channel_id
        
        
        if (owner is not ...):
            if __debug__:
                if (guild is not None) and (guild.owner_id != self.id):
                    raise AssertionError(
                        f'You must be owner to transfer ownership; got {owner!r}; actual owner={guild.owner!r}; '
                        f'guild={guild!r}.'
                    )
            
            if isinstance(owner, ClientUserBase):
                owner_id = owner.id
            else:
                owner_id = maybe_snowflake(owner)
                if owner_id is None:
                    raise TypeError(
                        f'`owner` can be `{UserBase.__name__}`, `int`, got {owner.__class__.__name__}; {owner!r}.'
                    )
            
            
            data['owner_id'] = owner_id
        
        
        if (region is not ...):
            if isinstance(region, VoiceRegion):
                region_value = region.value
            elif isinstance(region, str):
                region_value = region
            else:
                raise TypeError(
                    f'`region` can be `{VoiceRegion.__name__}`, `str`, got {region.__class__.__name__}; {region!r}.'
                )
            
            data['region'] = region_value
        
        
        if (afk_timeout is not ...):
            if __debug__:
                if not isinstance(afk_timeout, int):
                    raise AssertionError(
                        f'`afk_timeout` can be `int`, got {afk_timeout.__class__.__name__}; {afk_timeout!r}.'
                    )
                
                if afk_timeout not in (60, 300, 900, 1800, 3600):
                    raise AssertionError(
                        f'`afk_timeout` can be one of (60, 300, 900, 1800, 3600) seconds, got {afk_timeout!r}.'
                    )
            
            data['afk_timeout'] = afk_timeout
        
        
        if (verification_level is not ...):
            if isinstance(verification_level, VerificationLevel):
                verification_level_value = verification_level.value
            elif isinstance(verification_level, int):
                verification_level_value = verification_level
            else:
                raise TypeError(
                    f'`verification_level` can be `{VerificationLevel.__name__}`, `int`, got '
                    f'{verification_level.__class__.__name__}; {verification_level!r}.'
                )
            
            data['verification_level'] = verification_level_value
        
        
        if (content_filter is not ...):
            if isinstance(content_filter, ContentFilterLevel):
                content_filter_value = content_filter.value
            elif isinstance(content_filter, int):
                content_filter_value = content_filter
            else:
                raise TypeError(
                    f'`content_filter` can be `{ContentFilterLevel.__name__}`, `int`, got '
                    f'{content_filter.__class__.__name__}; {content_filter!r}.'
                )
            
            data['explicit_content_filter'] = content_filter_value
        
        
        if (message_notification is not ...):
            if isinstance(message_notification, MessageNotificationLevel):
                message_notification_value = message_notification.value
            elif isinstance(message_notification, int):
                message_notification_value = message_notification
            else:
                raise TypeError(
                    f'`message_notification` can be `{MessageNotificationLevel.__name__}`, `int`, got '
                    f'{message_notification.__class__.__name__}; {message_notification!r}.'
                )
            
            data['default_message_notifications'] = message_notification_value
        
        
        if (description is not ...):
            if __debug__:
                if (guild is not None) and (not COMMUNITY_FEATURES.intersection(guild.features)):
                    raise AssertionError(
                        f'The guild is not Community guild and `description` was given, got {description!r}; '
                        f'guild={guild!r}.'
                    )
            
            if description is None:
                pass
            elif isinstance(description, str):
                if not description:
                    description = None
            else:
                raise TypeError(
                    f'`description` can be `None`, `str`, got {description.__class__.__name__}; {description!r}.'
                )
            
            data['description'] = description
        
        
        if (preferred_locale is not ...):
            if __debug__:
                if (guild is not None) and (not COMMUNITY_FEATURES.intersection(guild.features)):
                    raise AssertionError(
                        f'The guild is not Community guild and `preferred_locale` was given, got {preferred_locale!r}, '
                        f'guild={guild!r}'
                    )
                
                if not isinstance(preferred_locale, str):
                    raise AssertionError(
                        f'`preferred_locale` can be `str`, got {preferred_locale.__class__.__name__}; '
                        f'{preferred_locale!r}.'
                    )
            
            data['preferred_locale'] = preferred_locale
        
        
        if (system_channel_flags is not ...):
            if __debug__:
                if not isinstance(system_channel_flags, int):
                    raise AssertionError(
                        f'`system_channel_flags` can be `{SystemChannelFlag.__name__}`, `int`, got '
                        f'{system_channel_flags.__class__.__name__}; {system_channel_flags!r}.'
                    )
            
            data['system_channel_flags'] = system_channel_flags
        
        
        if (add_feature is not ...) or (remove_feature is not ...):
            # Collect actual
            features = set()
            if (guild is not None):
                for feature in guild.features:
                    features.add(feature.value)
            
            # Collect added
            # Use GOTO
            while True:
                if add_feature is ...:
                    break
                
                if isinstance(add_feature, GuildFeature):
                    feature = add_feature.value
                elif isinstance(add_feature, str):
                    feature = add_feature
                else:
                    iter_func = getattr(type(add_feature), '__iter__', None)
                    if iter_func is None:
                        raise TypeError(
                            f'`add_feature` can be `str`, `{GuildFeature.__name__}`, `iterable` of '
                            f'(`str`, `{GuildFeature.__name__}`), got {add_feature.__class__.__name__}; '
                            f'{add_feature!r}.'
                        )
                    
                    for index, feature in enumerate(iter_func(add_feature)):
                        if isinstance(feature, GuildFeature):
                            feature = feature.value
                        elif isinstance(feature, str):
                            pass
                        else:
                            raise TypeError(
                                f'`add_feature` was given as `iterable` so it expected to have '
                                f'`{GuildFeature.__name__}`, `str` elements, but element `{index!r}` is '
                                f'{feature.__class__.__name__}; {feature!r}; add_feature={add_feature!r}.'
                            )
                        
                        features.add(feature)
                        continue
                    
                    break # End GOTO
                
                features.add(feature)
                break # End GOTO
            
            # Collect removed
            
            while True:
                if remove_feature is ...:
                    break
                
                if isinstance(remove_feature, GuildFeature):
                    feature = remove_feature.value
                elif isinstance(remove_feature, str):
                    feature = remove_feature
                else:
                    iter_func = getattr(type(remove_feature), '__iter__', None)
                    if iter_func is None:
                        raise TypeError(
                            f'`remove_feature` can be `str`, `{GuildFeature.__name__}`, `iterable` of '
                            f'(`str`, `{GuildFeature.__name__}`), got {remove_feature.__class__.__name__}; '
                            f'{remove_feature!r}.'
                        )
                    
                    for index, feature in enumerate(iter_func(remove_feature)):
                        if isinstance(feature, GuildFeature):
                            feature = feature.value
                        elif isinstance(feature, str):
                            pass
                        else:
                            raise TypeError(
                                f'`remove_feature` was given as `iterable` so it expected to have '
                                f'`{GuildFeature.__name__}`, `str` elements, but element `{index!r}` is '
                                f'{feature.__class__.__name__}; {feature!r}; remove_feature={remove_feature!r}.'
                            )
                        
                        features.discard(feature)
                        continue
                    
                    break # End GOTO
                
                features.discard(feature)
                break # End GOTO
            
            data['features'] = features
        
        
        if (boost_progress_bar_enabled is not ...):
            if __debug__:
                if not isinstance(boost_progress_bar_enabled, bool):
                    raise AssertionError(
                        f'`boost_progress_bar_enabled` can be `bool`, got '
                        f'{boost_progress_bar_enabled.__class__.__name__}; {boost_progress_bar_enabled!r}.'
                    )
            
            data['premium_progress_bar_enabled'] = boost_progress_bar_enabled
        
        
        await self.http.guild_edit(guild_id, data, reason)
    
    
    async def guild_ban_get_all(self, guild):
        """
        Returns the guild's bans.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, what's bans will be requested
        
        Returns
        -------
        bans : `list` of ``BanEntry`` elements
            User, reason pairs for each ban entry.
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as ``Guild``, `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id = get_guild_id(guild)
        
        data = await self.http.guild_ban_get_all(guild_id)
        return [BanEntry(User(ban_data['user']), ban_data.get('reason', None)) for ban_data in data]
    
    
    async def guild_ban_get(self, guild, user):
        """
        Returns the guild's ban entry for the given user id.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild where the user banned.
        user : ``ClientUserBase``, `int`
            The user's id, who's entry is requested.
        
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
        
        data = await self.http.guild_ban_get(guild_id, user_id)
        return BanEntry(User(data['user']), data.get('reason', None))
    
    
    async def guild_widget_get(self, guild):
        """
        Returns the guild's widget.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild or the guild's id, what's widget will be requested.
        
        Returns
        -------
        guild_widget : `None`, ``GuildWidget``
            If the guild has it's widget disabled returns `None` instead.
        
        Raises
        ------
        TypeError
            If `guild` was not passed neither as ``Guild``, `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id = get_guild_id(guild)
        
        try:
            data = await self.http.guild_widget_get(guild_id)
        except DiscordException as err:
            if err.response.status == 403: # Widget Disabled -> return None
                return
            raise
        
        return GuildWidget(data)
    
    
    async def guild_discovery_get(self, guild):
        """
        Requests and returns the guild's discovery metadata.
        
        The client must have `manage_guild` permission to execute this method.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``
            The guild what's discovery will be requested.
        
        Returns
        -------
        guild_discovery : ``GuildDiscovery``
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_discovery_data = await self.http.guild_discovery_get(guild.id)
        return GuildDiscovery(guild_discovery_data, guild)
    
    
    async def guild_discovery_edit(self, guild, *, primary_category=..., keywords=..., emoji_discovery=...):
        """
        Edits the guild's discovery metadata.
        
        The client must have `manage_guild` permission to execute this method.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, ``GuildDiscovery``, `int`
            The guild what's discovery metadata will be edited or an existing discovery metadata object.
        primary_category : `None`, ``DiscoveryCategory``, `int`, Optional (Keyword only)
            The guild discovery's new primary category's id. Can be given as a ``DiscoveryCategory`` object as well.
            If given as `None`, then resets the guild discovery's primary category id to it's default, what is `0`.
        keywords : `None`, (`iterable` of `str`), Optional (Keyword only)
            The guild discovery's new keywords. Can be given as `None` to reset to the default value, what is `None`,
            or as an `iterable` of strings.
        emoji_discovery : `None`, `bool`, Optional (Keyword only)
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
            - If `guild` was neither given as ``Guild``, ``GuildDiscovery``, `int`.
            - If `primary_category_id` was not given neither as `None`, `int`, ``DiscoveryCategory``.
            - If `keywords` was not passed neither as `None`, `iterable` of `str`.
            - If `emoji_discovery` was not given as `None`, `bool`.
        ValueError
            - If `primary_category_id` was given as not primary ``DiscoveryCategory`` object.
            - If `emoji_discovery` was given as `int`, but not as `0`, `1`.
        DiscordException
            If any exception was received from the Discord API.
        """
        if isinstance(guild, Guild):
            guild_id = guild.id
        elif isinstance(guild, GuildDiscovery):
            guild_id = guild.guild.id
        else:
            guild_id = maybe_snowflake(guild)
            if guild_id is None:
                raise TypeError(
                    f'`guild` can be `{Guild.__name__}`, `{GuildDiscovery.__name__}`, `int`, got '
                    f'{guild.__class__.__name__}; {guild!r}.'
                )
        
        data = {}
        
        if (primary_category is not ...):
            if (primary_category is None):
                primary_category_id = None
            else:
                primary_category_type = primary_category.__class__
                if primary_category_type is DiscoveryCategory:
                    # If name is set means that we should know whether the category is loaded, or just it's `.id`
                    # is known.
                    if (primary_category.name and (not primary_category.primary)):
                        raise ValueError(
                            f'The given `primary_category_id` is not a primary `{DiscoveryCategory.__name__}`, '
                            f'got {primary_category!r}.'
                        )
                    primary_category_id = primary_category.id
                
                elif primary_category_type is int:
                    primary_category_id = primary_category
                
                elif issubclass(primary_category_type, int):
                    primary_category_id = int(primary_category)
                
                else:
                    raise TypeError(
                        f'`primary_category` can be `None`, `int`, `{DiscoveryCategory.__name__}`, '
                        f'got {primary_category_type.__name__}; {primary_category!r}.'
                    )
            
            data['primary_category_id'] = primary_category_id
        
        if (keywords is not ...):
            if (keywords is None):
                pass
            elif (not isinstance(keywords, str)) and hasattr(type(keywords), '__iter__'):
                keywords_processed = set()
                index = 0
                for keyword in keywords:
                    if (type(keyword) is str):
                        pass
                    
                    elif isinstance(keyword, str):
                        keyword = str(keyword)
                    
                    else:
                        raise TypeError(
                            f'`keywords[{index}]` is not `str`, got {keyword.__class__.__name__}; {keyword!r}; '
                            f'keywords={keyword!r}.'
                        )
                    
                    keywords_processed.add(keyword)
                    index += 1
                
                keywords = keywords_processed
            else:
                raise TypeError(
                    f'`keywords` can be `None`, `iterable` of `str`, got {keywords.__class__.__name__}; {keywords!r}.'
                )
            
            data['keywords'] = keywords
        
        if (emoji_discovery is not ...):
            if (emoji_discovery is not None) and (not isinstance(emoji_discovery, bool)):
                raise TypeError(
                    f'`emoji_discovery` can be `None`, `bool`, got {emoji_discovery.__class__.__name__}; '
                    f'{emoji_discovery!r}.'
                )
            
            data['emoji_discoverability_enabled'] = emoji_discovery
        
        guild_discovery_data = await self.http.guild_discovery_edit(guild_id, data)
        
        if isinstance(guild, Guild):
            guild_discovery = GuildDiscovery(guild_discovery_data, guild)
        
        else:
            guild_discovery = guild
            guild_discovery._update_attributes(guild_discovery_data)
        
        return guild_discovery
    
    
    async def guild_discovery_add_subcategory(self, guild, category):
        """
        Adds a discovery subcategory to the guild.
        
        The client must have `manage_guild` permission to execute this method.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, ``GuildDiscovery``, `int`
            The guild to what the discovery subcategory will be added.
        category : ``DiscoveryCategory``, `int`
            The discovery category or it's id what will be added as a subcategory.
        
        Raises
        ------
        TypeError
            - If `guild` was not given neither as ``Guild``, ``GuildDiscovery``, neither as `int`.
            - If `category` was not passed neither as ``DiscoveryCategory``, `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        A guild can have maximum `5` discovery subcategories.
        
        If `guild` was given as ``GuildDiscovery``, then it will be updated.
        """
        guild_discovery, guild_id = get_guild_discovery_and_id(guild)
        
        category_type = category.__class__
        if category_type is DiscoveryCategory:
            category_id = category.id
        elif category_type is int:
            category_id = category
        elif issubclass(category_type, int):
            category_id = int(category)
        else:
            raise TypeError(
                f'`category` can be `int`, `{DiscoveryCategory.__name__}`, got {category_type.__name__}; {category!r}.'
            )
        
        await self.http.guild_discovery_add_subcategory(guild_id, category_id)
        
        if (guild_discovery is not None):
            guild_discovery.sub_categories.add(category_id)
    
    
    async def guild_discovery_delete_subcategory(self, guild, category):
        """
        Removes a discovery subcategory of the guild.
        
        The client must have `manage_guild` permission to execute this method.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, ``GuildDiscovery``, `int`
            The guild to what the discovery subcategory will be removed from.
        category : ``DiscoveryCategory``, `int`
            The discovery category or it's id what will be removed from the subcategories.
        
        Raises
        ------
        TypeError
            - If `guild` was not given neither as ``Guild``, ``GuildDiscovery``, neither as `int`.
            - If `category` was not passed neither as ``DiscoveryCategory``, `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        A guild can have maximum `5` discovery subcategories.
        
        If `guild` was given as ``GuildDiscovery``, then it will be updated.
        """
        guild_discovery, guild_id = get_guild_discovery_and_id(guild)
        
        category_type = category.__class__
        if category_type is DiscoveryCategory:
            category_id = category.id
        elif category_type is int:
            category_id = category
        elif issubclass(category_type, int):
            category_id = int(category)
        else:
            raise TypeError(
                f'`category` can be `int`, `{DiscoveryCategory.__name__}`, got {category_type.__name__}; {category!r}.'
            )
        
        await self.http.guild_discovery_delete_subcategory(guild_id, category_id)
        
        if (guild_discovery is not None):
            guild_discovery.sub_categories.discard(category_id)
    
    
    async def _discovery_category_get_all(self):
        """
        Returns a list of discovery categories, which can be used when editing guild discovery.
        
        This method is a coroutine.
        
        Returns
        -------
        discovery_categories : `list` of ``DiscoveryCategory``
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        discovery_category_datas = await self.http.discovery_category_get_all()
        return [DiscoveryCategory.from_data(discovery_category_data)
            for discovery_category_data in discovery_category_datas]
    
    
    # Add cached, so even tho the first request fails with `ConnectionError` will not be raised.
    discovery_category_get_all = DiscoveryCategoryRequestCacher(
        _discovery_category_get_all,
        3600.0,
        list(DISCOVERY_CATEGORIES.values()),
    )
    
    
    async def discovery_validate_term(self, term):
        """
        Checks whether the given discovery search term is valid.
        
        This method is a coroutine.
        
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
            If any exception was received from the Discord API.
        """
        data = await self.http.discovery_validate_term({'term': term})
        return data['valid']
    
    discovery_validate_term = DiscoveryTermRequestCacher(
        discovery_validate_term,
        86400.0,
        rate_limit_groups.discovery_validate_term,
    )
    
    
    async def guild_user_get_all(self, guild):
        """
        Requests all the users of the guild and returns them.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild what's users will be requested.
        
        Returns
        -------
        users : `list` of ``ClientUserBase`` objects
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as ``Guild``, nor as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        If user caching is allowed, these users should be already loaded if the client finished starting up.
        This method takes a long time to finish for huge guilds.
        
        When using it with user account, the client's token will be invalidated.
        """
        guild, guild_id = get_guild_and_id(guild)
        
        data = {'limit': 1000, 'after': 0}
        users = []
        while True:
            user_datas = await self.http.guild_user_get_chunk(guild_id, data)
            if guild is None:
                guild = create_partial_guild_from_id(guild_id)
            
            for user_data in user_datas:
                user = User(user_data, guild)
                users.append(user)
            
            if len(user_datas) < 1000:
                break
            
            data['after'] = user.id
        
        return users
    
    
    async def guild_get_all(self):
        """
        Requests all the guilds of the client.
        
        This method is a coroutine.
        
        Returns
        -------
        guilds : `list` of ``Guild``
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        If the client finished starting up, all the guilds should be already loaded.
        """
        result = []
        params = {'after': 0}
        while True:
            data = await self.http.guild_get_all(params)
            result.extend(create_partial_guild_from_data(guild_data) for guild_data in data)
            if len(data) < 100:
                break
            params['after'] = result[-1].id
        
        return result
    
    
    async def guild_voice_region_get_all(self, guild):
        """
        Requests the available voice regions for the given guild and returns them and the optional ones.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, what's regions will be requested.
        
        Returns
        -------
        voice_regions : `list` of ``VoiceRegion`` objects
            The available voice regions for the guild.
        optimals : `list` of ``VoiceRegion`` objects
            The optimal voice regions for the guild.
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as ``Guild``, nor as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id = get_guild_id(guild)
        
        data = await self.http.guild_voice_region_get_all(guild_id)
        voice_regions = []
        optimals = []
        for voice_region_data in data:
            region = VoiceRegion.from_data(voice_region_data)
            voice_regions.append(region)
            if voice_region_data['optimal']:
                optimals.append(region)
        
        return voice_regions, optimals
    
    
    async def voice_region_get_all(self):
        """
        Returns all the voice regions.
        
        This method is a coroutine.
        
        Returns
        -------
        voice_regions : `list` of ``VoiceRegion`` objects
            Received voice regions.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        data = await self.http.voice_region_get_all()
        voice_regions = []
        for voice_region_data in data:
            region = VoiceRegion.from_data(voice_region_data)
            voice_regions.append(region)
        
        return voice_regions
    
    
    async def guild_sync_channels(self, guild):
        """
        Requests the given guild's channels and if there any de-sync between the wrapper and Discord, applies the
        changes.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, what's channels will be requested.
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as ``Guild``, nor as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild, guild_id = get_guild_and_id(guild)
        
        data = await self.http.guild_channel_get_all(guild_id)
        if guild is None:
            guild = create_partial_guild_from_id(guild_id)
        
        guild._sync_channels(data)
    
    
    async def guild_sync_roles(self, guild):
        """
        Requests the given guild's roles and if there any de-sync between the wrapper and Discord, applies the
        changes.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, what's roles will be requested.
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as ``Guild``, nor as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild, guild_id = get_guild_and_id(guild)
        
        data = await self.http.guild_role_get_all(guild_id)
        if guild is None:
            guild = create_partial_guild_from_id(guild_id)
        
        guild._sync_roles(data)
    
    
    async def audit_log_get_chunk(self, guild, limit=100, *, before=None, after=None, user=None, event=None):
        """
        Request a batch of audit logs of the guild and returns them. The `after`, `around` and the `before` parameters
        are mutually exclusive and they can be `int`, or as a ``DiscordEntity`` or as a `datetime`
        object.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, what's audit logs will be requested.
        limit : `int` = `100`, Optional
            The amount of audit logs to request. Can be between 1 and 100. Defaults to 100.
        before : `None`, `int`, ``DiscordEntity``, `datetime` = `None`, Optional (Keyword only)
            The timestamp before the audit log entries wer created.
        after : `None`, `int`, ``DiscordEntity``, `datetime` = `None`, Optional (Keyword only)
            The timestamp after the audit log entries wer created.
        user : `None`, ```ClientUserBase``, `int` = `None`, Optional (Keyword only)
            Whether the audit logs should be filtered only to those, which were created by the given user.
        event : `None`, ``AuditLogEvent``, `int` = `None`, Optional (Keyword only)
            Whether the audit logs should be filtered only on the given event.
        
        Returns
        -------
        audit_log : ``AuditLog``
            A container what contains the ``AuditLogEntry``-s.
        
        Raises
        ------
        TypeError
            - If `guild` was not given neither as ``Guild``, nor as `int`.
            - If `after`, `before` was passed with an unexpected type.
            - If `user` is neither `None`, ``ClientUserBase``, `int`.
            - If `event` is neither `None`, ``AuditLogEvent``, `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `limit` was not given as `int`.
            - If `limit` is out of the expected range [1:100].
        """
        guild, guild_id = get_guild_and_id(guild)
        
        if __debug__:
            if not isinstance(limit, int):
                raise AssertionError(
                    f'`limit` can be `int`, got {limit.__class__.__name__}; {limit!r}.'
                )
            
            if limit < 1 or limit > 100:
                raise ValueError(
                    f'`limit` out of the expected range [1:100], got {limit!r}.'
                )
        
        data = {'limit': limit}
        
        if (before is not None):
            data['before'] = log_time_converter(before)
        
        if (after is not None):
            data['after'] = log_time_converter(after)
        
        if (user is not None):
            if isinstance(user, ClientUserBase):
                user_id = user.id
            
            else:
                user_id = maybe_snowflake(user)
                if user_id is None:
                    raise TypeError(
                        f'`user` can be `{ClientUserBase.__name__}`, `int`, got {user.__class__.__name__}; {user!r}.'
                    )
            
            data['user_id'] = user_id
        
        if (event is not None):
            if isinstance(event, AuditLogEvent):
                event_value = event.value
            elif isinstance(event, int):
                event_value = event
            else:
                raise TypeError(
                    f'`event` can be `None`, `{AuditLogEvent.__name__}`, `int`, got '
                    f'{event.__class__.__name__}; {event!r}.'
                )
            
            data['action_type'] = event_value
        
        data = await self.http.audit_log_get_chunk(guild_id, data)
        if guild is None:
            guild = create_partial_guild_from_id(guild_id)
        
        return AuditLog(data, guild)
    
    
    async def audit_log_iterator(self, guild, *, user=None, event=None):
        """
        Returns an audit log iterator for the given guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, what's audit logs will be requested.
        user : `None`, ``ClientUserBase``, `int` = `None`, Optional (Keyword only)
            Whether the audit logs should be filtered only to those, which were created by the given user.
        event : `None`, ``AuditLogEvent``, `int` = `None`, Optional (Keyword only)
            Whether the audit logs should be filtered only on the given event.
        
        Returns
        -------
        audit_log_iterator : ``AuditLogIterator``
        """
        return await AuditLogIterator(self, guild, user=user, event=event)
    
    # users
    
    async def user_guild_profile_edit(self, guild, user, *, nick=..., deaf=..., mute=..., voice_channel=...,
            roles=..., timed_out_until=..., reason=None):
        """
        Edits the user's guild profile at the given guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            Where the user will be edited.
        user : ``ClientUserBase``, `int`
            The user to edit
        nick : `None`, `str`, Optional (Keyword only)
            The new nick of the user. You can remove the current one by passing it as `None`, an empty string.
        deaf : `bool`, Optional (Keyword only)
            Whether the user should be deafen at the voice channels.
        mute : `bool`, Optional (Keyword only)
            Whether the user should be muted at the voice channels.
        voice_channel : `None`, ``ChannelVoiceBase``, `int` , Optional (Keyword only)
            Moves the user to the given voice channel. Only applicable if the user is already at a voice channel.
            
            Pass it as `None` to kick the user from it's voice channel.
        roles : `None`, (`tuple`, `set`, `list`) of (``Role``, `int`), Optional (Keyword only)
            The new roles of the user. Give it as `None` to remove all of the user's roles.
        timed_out_until : `None`, `datetime`, Optional (Keyword only)
            Till when the client is timed out. Pass it as `None` to remove it.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Will show up at the guild's audit logs.
        
        Raises
        ------
        TypeError
            - If `guild` was not given neither as ``Guild`` neither as `int`.
            - If `user` was not given neither as ``ClientUserBase``, neither as `int`.
            - If `voice_channel` was not given neither as `None`, ``ChannelVoiceBase``, neither as `int`.
            - If `roles` contains neither ``Role``, `int` element.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `nick` was not given neither as `None`, `str`.
            - If `nick` length is out of the expected range [0:32].
            - If `deaf` was not given as `bool`.
            - If `mute` was not given as `bool`.
            - If `roles` is not `None`, `set`, `tuple`, `list`.
            - If `timed_out_until` is neither `None` nor `datetime`.
        """
        guild, guild_id = get_guild_and_id(guild)
        user, user_id = get_user_and_id(user)
        
        data = {}
        if (nick is not ...):
            if __debug__:
                if (nick is not None):
                    if not isinstance(nick, str):
                        raise AssertionError(
                            f'`nick` can be `None`, `str`, got {nick.__class__.__name__}; {nick!r}.'
                        )
                    
                    nick_length = len(nick)
                    if nick_length > 32:
                        raise AssertionError(
                            f'`nick` length can be in range [0:32], got {nick_length}; {nick!r}.'
                        )
            
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
            if __debug__:
                if not isinstance(deaf, bool):
                    raise AssertionError(
                        f'`deaf` can be `bool`, got {deaf.__class__.__name__}; {deaf!r}.'
                    )
            
            data['deaf'] = deaf
            
        if (mute is not ...):
            if __debug__:
                if not isinstance(mute, bool):
                    raise AssertionError(
                        f'`mute` can be `bool`, got {mute.__class__.__name__}; {mute!r}.'
                    )
            
            data['mute'] = mute
            
        if (voice_channel is not ...):
            if voice_channel is None:
                voice_channel_id = None
            elif isinstance(voice_channel, ChannelVoiceBase):
                voice_channel_id = voice_channel.id
            else:
                voice_channel_id = maybe_snowflake(voice_channel)
                if voice_channel_id is None:
                    raise TypeError(
                        f'`voice_channel` can be `None`, `{ChannelVoiceBase.__name__}`, `int`, got '
                        f'{voice_channel.__class__.__name__}; {voice_channel!r}.'
                    )
            
            data['channel_id'] = voice_channel_id
        
        if (roles is not ...):
            role_ids = set()
            if (roles is not None):
                if __debug__:
                    if not isinstance(roles, (list, set, tuple)):
                        raise AssertionError(
                            f'`roles` can be `None`, `list`, `set`, `tuple`, got '
                            f'{roles.__class__.__name__}; {roles!r}.'
                        )
                
                for role in roles:
                    if isinstance(role, Role):
                        role_id = role.id
                    else:
                        role_id = maybe_snowflake(role)
                        if role_id is None:
                            raise TypeError(
                                f'`roles` contains not `{Role.__name__}`, `int` element, got '
                                f'{role.__class__.__name__}; {role!r}; roles={roles!r}.'
                            )
                    
                    role_ids.add(role_id)
            
            data['roles'] = role_ids
        
        if (timed_out_until is not ...):
            if timed_out_until is None:
                timed_out_until_raw = None
            else:
                if __debug__:
                    if not isinstance(timed_out_until, datetime):
                        raise AssertionError(
                            f'`timed_out_until` can be `None`, `datetime`, got '
                            f'{timed_out_until.__class__.__name__}.'
                        )
                
                timed_out_until_raw = datetime_to_timestamp(timed_out_until)
            
            data['communication_disabled_until'] = timed_out_until_raw
        
        await self.http.user_guild_profile_edit(guild_id, user_id, data, reason)
    
    
    async def user_role_add(self, user, role, *, reason=None):
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
        snowflake_pair = get_guild_id_and_role_id(role)
        if snowflake_pair is None:
            return
        guild_id, role_id = snowflake_pair
        user_id = get_user_id(user)
        
        await self.http.user_role_add(guild_id, user_id, role_id, reason)
    
    
    async def user_role_delete(self, user, role, *, reason=None):
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
        snowflake_pair = get_guild_id_and_role_id(role)
        if snowflake_pair is None:
            return
        guild_id, role_id = snowflake_pair
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
        channel : ``ChannelVoiceBase``, `tuple` (`int`, `int`)
            The channel where the user will be moved.
        
        Raises
        ------
        TypeError
            - If `user` was not given neither as ``ClientUserBase``, neither as `int`.
            - If `channel` was not given neither as ``ChannelVoiceBase`` nor as `tuple` of (`int`, `int`).
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        snowflake_pair = get_guild_id_and_channel_id(channel, ChannelVoiceBase)
        if snowflake_pair is None:
            return
        guild_id, channel_id = snowflake_pair
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
        channel : ``ChannelStage``, `tuple` (`int`, `int`)
            The channel where the user will be moved.
        
        Raises
        ------
        TypeError
            - If `user` was not given neither as ``ClientUserBase``, neither as `int`.
            - If `channel` was not given neither as ``ChannelStage`` nor as `tuple` of (`int`, `int`).
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        snowflake_pair = get_guild_id_and_channel_id(channel, ChannelStage)
        if snowflake_pair is None:
            return
        guild_id, channel_id = snowflake_pair
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
        channel : ``ChannelStage``, `tuple` (`int`, `int`)
            The channel where the user will be moved.
        
        Raises
        ------
        TypeError
            - If `user` was not given neither as ``ClientUserBase``, neither as `int`.
            - If `channel` was not given neither as ``ChannelStage`` nor as `tuple` of (`int`, `int`).
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        snowflake_pair = get_guild_id_and_channel_id(channel, ChannelStage)
        if snowflake_pair is None:
            return
        guild_id, channel_id = snowflake_pair
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
    
    
    async def stage_create(self, channel, topic, *, privacy_level=PrivacyLevel.guild_only):
        """
        Edits the given stage channel.
        
        Will trigger a `stage_create` event.
        
        > The endpoint has a long rate limit, so please use ``.stage_edit`` to edit just the stage's topic.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``ChannelStage``, `int`
            The channel to edit.
        topic : `None`, `str`
            The new topic of the stage.
        privacy_level : ``PrivacyLevel``, `int` = `PrivacyLevel.guild_only`, Optional (Keyword only)
            The new privacy level of the stage. Defaults to guild only.
        
        Returns
        -------
        stage : ``Stage``
            The created stage instance.
        
        Raises
        ------
        TypeError
            - If `channel` was not given as ``ChannelStage`` neither as `int`.
            - If `privacy_level` was not given neither as ``PrivacyLevel`` nor as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `topic` was not given neither as `None`, `str`.
            - If `topic`'s length is out of range [1:120].
        """
        channel_id = get_channel_id(channel, ChannelStage)
        
        if topic is None:
            topic = ''
        else:
            if __debug__:
                if not isinstance(topic, str):
                    raise AssertionError(
                        f'`topic` can be `None`, `str`, got {topic.__class__.__name__}; {topic!r}.'
                    )
                
                topic_length = len(topic)
                if (topic_length < 1) or (topic_length > 120):
                    raise AssertionError(
                        f'`topic` length can be in range [1:120], got {topic_length!r}; {topic!r}.'
                    )
        
        if isinstance(privacy_level, PrivacyLevel):
            privacy_level = privacy_level.value
        elif isinstance(privacy_level, int):
            privacy_level = privacy_level
        else:
            raise TypeError(
                f'`privacy_level` can be `{PrivacyLevel.__name__}`, `int` , got '
                f'{privacy_level.__class__.__name__}; {privacy_level!r}.'
            )
        
        data = {
            'channel_id': channel_id,
            'topic': topic,
            'privacy_level': privacy_level,
        }
        
        data = await self.http.stage_create(data)
        return Stage(data)
    
    
    async def stage_edit(self, stage, topic=..., *, privacy_level=...):
        """
        Edits the given stage channel.
        
        Will trigger a `stage_edit` event.
        
        This method is a coroutine.
        
        Parameters
        ----------
        stage : ``Stage``, ``ChannelStage``, `int`
            The stage to edit. Can be given as it's channel's identifier.
        topic : `str`
            The new topic of the stage.
        privacy_level : ``PrivacyLevel``, `int`, Optional (Keyword only)
            The new privacy level of the stage.
        
        Raises
        ------
        TypeError
            - If `stage` was not given as ``Stage``, ``ChannelStage`` neither as `int`.
            - If `privacy_level` was not given neither as ``PrivacyLevel`` nor as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `topic` was not given neither as `None` nor as `str`.
            - If `topic`'s length is out of range [1:120].
        """
        channel_id = get_stage_channel_id(stage)
        
        data = {}
        
        if (topic is not ...):
            if __debug__:
                if not isinstance(topic, str):
                    raise AssertionError(
                        f'`topic` can be `None`, `str`, got {topic.__class__.__name__}; {topic!r}.'
                    )
                
                topic_length = len(topic)
                if (topic_length < 1) or (topic_length > 120):
                    raise AssertionError(
                        f'`topic` length can be in range [1:120], got {topic_length!r}; {topic!r}.'
                    )
            
            data['topic'] = topic
        
        
        if (privacy_level is not ...):
            if isinstance(privacy_level, PrivacyLevel):
                privacy_level = privacy_level.value
            elif isinstance(privacy_level, int):
                privacy_level = privacy_level
            else:
                raise TypeError(
                    f'`privacy_level` can be `{PrivacyLevel.__name__}`, `int` , got '
                    f'{privacy_level.__class__.__name__}; {privacy_level!r}.'
                )
            
            data['privacy_level'] = privacy_level
        
        
        if not data:
            return
        
        await self.http.stage_edit(channel_id, data)
        # We receive data, but ignore it, so we can dispatch it.
    
    
    async def stage_delete(self, stage):
        """
        Deletes the given stage channel.
        
        Will trigger a `stage_delete` event.
        
        This method is a coroutine.
        
        Parameters
        ----------
        stage : ``Stage``, ``ChannelStage``, `int`
            The stage to delete. Can be given as it's channel's identifier.
        
        Raises
        ------
        TypeError
            If `stage` was not given as ``Stage``, ``ChannelStage`` neither as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id = get_stage_channel_id(stage)
        
        await self.http.stage_delete(channel_id)
        # We receive no data.
    
    
    async def stage_get(self, channel):
        """
        Gets the stage of the given stage channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``ChannelStage``, `int`
            The stage's channel's identifier.
        
        Raises
        ------
        TypeError
            If `channel` was not given as ``ChannelStage`` neither as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id = get_channel_id(channel, ChannelStage)
        
        data = await self.http.stage_get(channel_id)
        return Stage(data)
    
    # Scheduled events
    
    async def scheduled_event_create(self, guild, name, start, *, description=None, end=None,
            privacy_level=PrivacyLevel.guild_only, location=None, stage=None, voice=None, reason=None):
        """
        Creates a guild scheduled events.
        
        To define, where the event will take place, use the `location`, `stage`, `voice` parameters.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, where to create the scheduled event.
        name : `str`
            The event's name. It's length can be in range [1:100].
        start : `datetime``
            When the event will start.
        description : `None`, `str` = `None`, Optional (Keyword only)
            The event's description. It's length can be in range [0:1000].
        end : `None`, `datetime` = `None`, Optional (Keyword only)
            When the event will end.
        privacy_level : ``PrivacyLevel``, `int` = `None`, Optional (Keyword only)
            The privacy level of the event. Whether it is global or guild only.
        location : `None`, `str` = `None`, Optional (Keyword only)
            The location, where the event will take place.
        stage : `None`, ``ChannelStage``, `int` = `None`, Optional (Keyword only)
            The stage channel, where the event will take place.
        voice : `None`, ``ChannelVoice``, `int` = `None`, Optional (Keyword only)
            The voice channel, where the event will take place.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        Returns
        -------
        scheduled_event : ``ScheduledEvent``
            The created event.
        
        Raises
        ------
        TypeError
            - If `guild` is neither ``Guild``, nor `int`.
            - If `privacy_level` is neither ``PrivacyLevel``, nor `int`.
            - If `stage` is neither ``ChannelStage``, nor `int`.
            - If `voice` is neither ``ChannelVoice``, nor `int`.
            - If neither `location`, `stage`, `voice` parameters is given.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `name` is not `str`.
            - If `name`'s length is out of the expected range.
            - If `description is neither `None` nor `str`.
            - If `description`'s length is out of the expected range.
            - If `location` is not `str`.
            - If `start` is not `datetime`.
            - If `end `is neither `None`, nor `datetime`.
        """
        guild_id = get_guild_id(guild)
        
        if __debug__:
            if not isinstance(name, str):
                raise AssertionError(
                    f'`name` can be `str`, got {name.__class__.__name__}; {name!r}.'
                )
            
            name_length = len(name)
            if (name_length < 1) or (name_length > 100):
                raise AssertionError(
                    f'`name` length can be in range [1:100], got {name_length!r}; {name!r}.'
                )
        
        if __debug__:
            if not isinstance(start, datetime):
                raise AssertionError(
                    f'`start` can be `datetime`, got {start.__class__.__name__}; {start!r}.'
                )
            
            if (end is not None) and (not isinstance(end, datetime)):
                raise AssertionError(
                    f'`end` can be `None`, `datetime`, got {end.__class__.__name__}; {end!r}.'
                )
        
        if isinstance(privacy_level, PrivacyLevel):
            privacy_level_value = privacy_level.value
        elif isinstance(privacy_level, int):
            privacy_level_value = privacy_level
        else:
            raise TypeError(
                f'`privacy_level` can be `{PrivacyLevel.__name__}` `int`, got '
                f'{privacy_level.__class__.__name__}; {privacy_level!r}.'
            )
        
        if (description is not None):
            if __debug__:
                if (not isinstance(description, str)):
                    raise AssertionError(
                        f'`description` can be `None`, `str`, got {description.__class__.__name__}, {description!r}.'
                    )
                
                description_length = len(description)
                if description_length > 1000:
                    raise AssertionError(
                        f'description length can be in range [0:1000], got {description_length!r}; {description!r}.'
                    )
            
            if not description:
                description = None
        
        if (location is not None):
            if __debug__:
                if not isinstance(location, str):
                    raise AssertionError(
                        f'`location` can be `str`, got {location.__class__.__name__}; {location!r}.'
                    )
            
            channel_id = None
            entity_metadata = {'location': location}
            entity_type = ScheduledEventEntityType.location
        
        elif (stage is not None):
            channel_id = get_channel_id(stage, ChannelStage)
            entity_metadata = None
            entity_type = ScheduledEventEntityType.stage
        
        elif (voice is not None):
            channel_id = get_channel_id(voice, ChannelVoice)
            entity_metadata = None
            entity_type = ScheduledEventEntityType.voice
            
        else:
            raise TypeError(
                f'Either `location`, `stage`, `voice` parameters are required.'
            )
        
        data = {
            'name' : name,
            'privacy_level': privacy_level_value,
            'channel_id': channel_id,
            'entity_metadata': entity_metadata,
            'entity_type': entity_type.value,
            'scheduled_start_time': datetime_to_timestamp(start),
        }
        
        if (description is not None):
            data['description'] = description
        
        if (end is not None):
            data['scheduled_end_time'] = datetime_to_timestamp(end)
        
        data = await self.http.scheduled_event_create(guild_id, data, reason)
        return ScheduledEvent(data)
    
    # In theory you can edit the target entity is as well, but we will ignore it for now.
    
    async def scheduled_event_edit(self, scheduled_event, *, name=..., description=..., start=..., end=...,
            privacy_level=..., status=..., location=..., stage=..., voice=..., reason=None):
        """
        Edits the given scheduled event.
        
        This method is a coroutine.
        
        Parameters
        ----------
        scheduled_event : ``ScheduledEvent``, `tuple`, (`int`, `int`)
            The scheduled event to edit.
        name : `str`, Optional (Keyword only)
            The new name of the scheduled event. It's length can be in range [1:100].
        description : `None`, `str`, Optional (Keyword only)
            The new description of the scheduled event. It's length can be in range [0:1000].
            
            Pass it as `None` to remove the old one.
        
        start : `datetime`, Optional (Keyword only)
            The new start of the scheduled event.
        
        end : `None`, `datetime`
            The end of the of the scheduled event.
            
            Pass it as `None` to remove the old end.
        
        privacy_level : ``PrivacyLevel``, `int`, Optional (Keyword only)
            The privacy level of the event. Whether it is global or guild only.
        
        status : `str`, ``ScheduledEventStatus``, Optional (Keyword only)
            Thew new status of the scheduled event.
        
        location : `str`, Optional (Keyword only)
            The new location, where the event will take place.
        
        stage : ``ChannelStage``, `int`, Optional (Keyword only)
            The new stage channel, where the event will take place.
        
        voice : ``ChannelVoice``, `int`, Optional (Keyword only)
            The new voice channel, where the event will take place.
        
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        TypeError
            - If `scheduled_event` is neither ``ScheduledEvent``, nor `tuple` (`int`, `int`).
            - If `privacy_level` is neither ``PrivacyLevel``, nor `int`.
            - If `stage` is neither ``ChannelStage``, nor `int`.
            - If `voice` is neither ``ChannelVoice``, nor `int`.
            - If `privacy_level` is neither ``PrivacyLevel``, nor `int`.
            - If `status` is neither ``ScheduledEventStatus``, nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `name` is not `str`.
            - If `name`'s length is out of the expected range.
            - If `description is neither `None` nor `str`.
            - If `description`'s length is out of the expected range.
            - If `location` is not `str`.
            - If `start` is not `datetime`.
            - If `end `is neither `None`, nor `datetime`.
        """
        guild_id, scheduled_event_id = get_guild_id_and_scheduled_event_id(scheduled_event)
        
        data = {}
        
        if (name is not ...):
            if __debug__:
                if not isinstance(name, str):
                    raise AssertionError(
                        f'`name` can be `str`, got {name.__class__.__name__}; {name!r}.'
                    )
                
                name_length = len(name)
                if (name_length < 1) or (name_length > 100):
                    raise AssertionError(
                        f'`name` length can be in range [1:100], got {name_length!r}; {name!r}.'
                    )
            
            data['name'] = name
        
        
        if (description is not ...):
            if description is None:
                description = ''
            else:
                if __debug__:
                    if (not isinstance(description, str)):
                        raise AssertionError(
                            f'`description` can be `None`, `str`, got '
                            f'{description.__class__.__name__}; {description!r}.'
                        )
                    
                    description_length = len(description)
                    if description_length > 1000:
                        raise AssertionError(
                            f'description length can be in range [0:1000], got '
                            f'{description_length!r}; {description!r}.'
                        )
            
            data['description'] = description
        
        if (start is not ...):
            if __debug__:
                if not isinstance(start, datetime):
                    raise AssertionError(
                        f'`start` can be `datetime`, got {start.__class__.__name__}; {start!r}.'
                    )
            
            data['scheduled_start_time'] = datetime_to_timestamp(start)
        
        if (end is not ...):
            if __debug__:
                if (end is not None) and (not isinstance(end, datetime)):
                    raise AssertionError(
                        f'`end` can be `None`, `datetime`, got {end.__class__.__name__}; {end!r}.'
                    )
            
            data['scheduled_end_time'] = None if end is None else datetime_to_timestamp(end)
        
        if (privacy_level is not ...):
            if isinstance(privacy_level, PrivacyLevel):
                privacy_level_value = privacy_level.value
            elif isinstance(privacy_level, int):
                privacy_level_value = privacy_level
            else:
                raise TypeError(
                    f'`privacy_level` can be `{PrivacyLevel.__name__}`, `int`, got '
                    f'{privacy_level.__class__.__name__}; {privacy_level!r}.'
                )
            
            data['privacy_level'] = privacy_level_value
        
        if (status is not ...):
            if isinstance(status, ScheduledEventStatus):
                status_value = status.value
            elif isinstance(status, int):
                status_value = status
            else:
                raise TypeError(
                    f'`status` can be `{ScheduledEventStatus.__name__}`, `int` , got '
                    f'{status.__class__.__name__}; {status!r}.'
                )
            
            data['status'] = status_value
        
        if (location is not ...) or (stage is not ...) or (voice is not ...):
            if (location is not ...):
                if __debug__:
                    if not isinstance(location, str):
                        raise AssertionError(
                            f'`location` can be `str`, got {location.__class__.__name__}; {location!r}.'
                        )
                
                channel_id = None
                entity_metadata = {'location': location}
                entity_type = ScheduledEventEntityType.location
            
            elif (stage is not ...):
                channel_id = get_channel_id(stage, ChannelStage)
                entity_metadata = None
                entity_type = ScheduledEventEntityType.stage
            
            # elif (voice is not ...):
            else:
                channel_id = get_channel_id(voice, ChannelVoice)
                entity_metadata = None
                entity_type = ScheduledEventEntityType.voice
            
            data['channel_id'] = channel_id
            data['entity_metadata'] = entity_metadata
            data['entity_type'] = entity_type.value
        
        
        if data:
            await self.http.scheduled_event_edit(guild_id, scheduled_event_id, data, reason)
    
    
    async def scheduled_event_delete(self, scheduled_event):
        """
        Edits the given scheduled event.
        
        This method is a coroutine.
        
        Parameters
        ----------
        scheduled_event : ``ScheduledEvent``, `tuple` (`int`, `int`)
            The scheduled event to edit.
        
        Raises
        ------
        TypeError
            If `scheduled_event` is neither ``ScheduledEvent``, nor `tuple` (`int`, `int`).
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id, scheduled_event_id = get_guild_id_and_scheduled_event_id(scheduled_event)
        await self.http.scheduled_event_delete(guild_id, scheduled_event_id)
    
    
    async def scheduled_event_get(self, scheduled_event, *, force_update=False):
        """
        Gets the given scheduled event.
        
        This method is a coroutine.
        
        Parameters
        ----------
        scheduled_event : ``ScheduledEvent``, `tuple` `int` and `int`
            The scheduled event to get.
        force_update : `bool` = `False`, Optional (Keyword only)
            Whether the scheduled event should be requested even if it supposed to be up to date.
        
        Returns
        -------
        scheduled_event : ``ScheduledEvent``
        
        Raises
        ------
        TypeError
            If `scheduled_event` is neither ``ScheduledEvent``, nor `tuple` (`int`, `int`) instance.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        scheduled_event, guild_id, scheduled_event_id = get_scheduled_event_guild_id_and_id(scheduled_event)
        if (scheduled_event is None) or force_update:
            data = await self.http.scheduled_event_get(guild_id, scheduled_event_id, {'with_user_count', None})
        
            if scheduled_event is None:
                try:
                    scheduled_event = SCHEDULED_EVENTS[scheduled_event_id]
                except KeyError:
                    scheduled_event = ScheduledEvent(data)
                else:
                    scheduled_event._update_attributes(data)
                    scheduled_event._update_counts_only(data)
            else:
                scheduled_event = ScheduledEvent(data)
        
        return scheduled_event
    
    
    async def scheduled_event_get_all_guild(self, guild):
        """
        Gets the given guild's scheduled event.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild to get it's scheduled of.
        
        Returns
        -------
        scheduled_events : `list` of ``ScheduledEvent``
        
        Raises
        ------
        TypeError
            If `guild` is neither ``Guild`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id = get_guild_id(guild)
        scheduled_event_datas = await self.http.scheduled_event_get_all_guild(guild_id, {'with_user_count': True})
        return [ScheduledEvent(scheduled_event_data) for scheduled_event_data in scheduled_event_datas]
    
    
    async def scheduled_event_user_get_chunk(self, scheduled_event, *, limit=None, before=None, after=None):
        """
        Requests a chunk user subscribed to a scheduled event.
        
        This method is a coroutine.
        
        Parameters
        ----------
        scheduled_event : ``ScheduledEvent``, `tuple` `int` and `int`
            The scheduled event to get.
        limit : `None`, `int` = `None`, Optional (Keyword only)
            The amount of messages to request. Can be between 1 and 100.
        after : `None`, `int`, ``DiscordEntity``, `datetime` = `None`, Optional (Keyword only)
            The timestamp after the subscribed users were created.
        before : `None`, `int`, ``DiscordEntity``, `datetime` = `None`, Optional (Keyword only)
            The timestamp before the subscribed users were created.
        
        Returns
        -------
        users : `list` of ``ClientUserBase``
        
        Raises
        ------
        TypeError
            - If `scheduled_event` is neither ``ScheduledEvent``, nor `tuple` (`int`, `int`) instance.
            - If `after`, `before` was passed with an unexpected type.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `limit` was not given as `int`.
            - If `limit` is out of range [1:100].
        """
        guild, guild_id, scheduled_event_id = get_guild_and_id_and_scheduled_event_id(scheduled_event)
        
        if limit is None:
            limit = 100
        else:
            if __debug__:
                if not isinstance(limit, int):
                    raise AssertionError(
                        f'`limit` can be `int`, got {limit.__class__.__name__}; {limit!r}.'
                    )
                
                if (limit < 1) or (limit > 100):
                    raise AssertionError(
                        f'`limit` is out from the expected [1:100] range, got {limit!r}.'
                    )
        
        data = {}
        
        if limit != 100:
            data['limit'] = limit
        
        if (after is not None):
            data['after'] = log_time_converter(after)
        
        if (before is not None):
            data['before'] = log_time_converter(before)
        
        if (guild is not None):
            data['with_member'] = True
        
        scheduled_event_user_datas = await self.http.scheduled_event_user_get_chunk(guild_id, scheduled_event_id, data)
        
        users = []
        for scheduled_event_user_data in scheduled_event_user_datas:
            user_data = scheduled_event_user_data['user']
            if (guild is not None):
                try:
                    guild_profile_data = scheduled_event_user_data['member']
                except KeyError:
                    pass
                else:
                    user_data['member'] = guild_profile_data
            
            user = User(user_data, guild)
            users.append(user)
        
        return users
    
    
    async def scheduled_event_user_get_all(self, scheduled_event):
        """
        Requests a chunk user subscribed to a scheduled event.
        
        This method is a coroutine.
        
        Parameters
        ----------
        scheduled_event : ``ScheduledEvent``, `tuple` `int` and `int`
            The scheduled event to get.
        
        Returns
        -------
        users : `list` of ``ClientUserBase``
        
        Raises
        ------
        TypeError
            - If `scheduled_event` is neither ``ScheduledEvent``, nor `tuple` (`int`, `int`) instance.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild, guild_id, scheduled_event_id = get_guild_and_id_and_scheduled_event_id(scheduled_event)
        
        data = {'after': 0}
        
        if (guild is not None):
            data['with_member'] = True
        
        users = []
        
        while True:
            scheduled_event_user_datas = await self.http.scheduled_event_user_get_chunk(
                guild_id,
                scheduled_event_id,
                data,
            )
            
            for scheduled_event_user_data in scheduled_event_user_datas:
                user_data = scheduled_event_user_data['user']
                if (guild is not None):
                    try:
                        guild_profile_data = scheduled_event_user_data['member']
                    except KeyError:
                        pass
                    else:
                        user_data['member'] = guild_profile_data
                
                user = User(user_data, guild)
                users.append(user)
            
            if len(scheduled_event_user_datas) < 100:
                break
            
            data['after'] = users[-1].id
        
        return users
    
    # Thread
    
    async def guild_thread_get_all_active(self, guild):
        """
        Gets all the active threads of the given guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild to get it's threads of.
        
        Returns
        -------
        threads : `list` of ``ChannelThread``
        
        Raises
        ------
        TypeError
            If `guild` is neither ``Guild`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id = get_guild_id(guild)
        
        data = await self.http.guild_thread_get_all_active(guild_id)
        
        thread_channel_datas = data['threads']
        
        thread_channels = [
            ChannelThread(thread_channel_data, self, guild_id) for thread_channel_data in thread_channel_datas
        ]
        
        thread_user_datas = data['members']
        for thread_user_data in thread_user_datas:
            thread_channel_id = int(thread_user_data['id'])
            try:
                thread_channel = CHANNELS[thread_channel_id]
            except KeyError:
                continue
    
            user_id = int(thread_user_data['user_id'])
            user = create_partial_user_from_id(user_id)
            
            thread_user_create(thread_channel, user, thread_user_data)
        
        return thread_channels
    
    
    async def thread_create(self, message_or_channel, name, *, auto_archive_after=None, type_=None, invitable=True):
        """
        Creates a new thread derived from the given message or channel.
        
        > For private thread channels the guild needs to have level 2 boost level.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message_or_channel : ``ChannelText``, ``Message``, ``MessageRepr``, ``MessageReference``, `int`, \
                `tuple` (`int`, `int`)
            The channel or message to create thread from.
            
            > If given as a channel instance, will create a private thread, else a public one.
        
        name : `str`
            The created thread's name.
        
        auto_archive_after : `None`, `int` = `None`, Optional (Keyword only)
            The duration in seconds after the thread auto archives. Can be any of `3600`, `86400`, `259200`, `604800`.
            
            > For `259200` seconds (or 3 days) or `604800` seconds (or 7 days) auto archive duration the guild needs
            > to be boosted.
        
        type_ : `None`, `int` = `None`, Optional (Keyword only)
            The thread channel's type to create. Can be either `10`,`11`,`12`.
        
        invitable : `bool` = `True`, Optional (Keyword only)
            Whether non-moderators can invite other non-moderators to the threads. Only applicable for private threads.
            
            Applicable for private threads. Defaults to `True`.
        
        Returns
        -------
        thread_channel : ``ChannelThread``
        
        Raises
        ------
        TypeError
            If `message`'s type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `name` is not `str`.
            - If `name`'s length is out of range [2:100].
            - If `auto_archive_after` is neither `int`, nor `bool`.
            - If `auto_archive_after` is not any of the expected ones.
            - If `invitable` is not `bool`.
        """
        # Message check order
        # 1.: Message
        # 2.: MessageRepr
        # 3.: MessageReference
        # 4.: None -> raise
        # 5.: `tuple` (`int`, `int`)
        # 6.: raise
        #
        # Message cannot be detected by id, only cached ones, so ignore that case.
        
        if isinstance(message_or_channel, ChannelBase):
            if message_or_channel.type not in CHANNEL_TYPES.GROUP_CAN_CONTAIN_THREADS:
                raise TypeError(
                    f'{message_or_channel!r} do not supports thread creation.'
                )
            
            message_id = None
            channel = message_or_channel
            channel_id = channel.id
            guild = channel.guild
        elif isinstance(message_or_channel, Message):
            message_id = message_or_channel.id
            channel_id = message_or_channel.channel_id
            channel = CHANNELS.get(channel_id, None)
            guild = channel.guild
        else:
            channel_id = maybe_snowflake(message_or_channel)
            if (channel_id is not None):
                message_id = None
                channel = CHANNELS.get(channel_id, None)
                guild = None
            elif isinstance(message_or_channel, MessageRepr):
                message_id = message_or_channel.id
                channel_id = message_or_channel.channel_id
                channel = CHANNELS.get(channel_id, None)
                guild = message_or_channel.guild
            elif isinstance(message_or_channel, MessageReference):
                message_id = message_or_channel.message_id
                channel_id = message_or_channel.channel_id
                channel = CHANNELS.get(channel_id, None)
                guild = message_or_channel.guild
            else:
                snowflake_pair = maybe_snowflake_pair(message_or_channel)
                if snowflake_pair is None:
                    raise TypeError(
                        f'`message_or_channel` can be `{ChannelTextBase.__name__}`, `{Message.__name__}`, '
                        f'`{MessageRepr.__name__}`, `{MessageReference.__name__}`, `int`, `tuple` (`int`, `int`)'
                        f', got {message_or_channel.__class__.__name__}; {message_or_channel!r}.'
                    )
                
                channel_id, message_id = snowflake_pair
                channel = CHANNELS.get(channel_id)
                guild = None
        
        if __debug__:
            if not isinstance(name, str):
                raise AssertionError(
                    f'`name` can be `str`, got {name.__class__.__name__}; {name!r}.'
                )
            
            name_length = len(name)
            
            if (name_length) < 2 or (name_length > 100):
                raise AssertionError(
                    f'`name` length can be in range [2:100], got {name_length}; {name!r}.'
                )
        
        if auto_archive_after is None:
            if channel is None:
                auto_archive_after = AUTO_ARCHIVE_DEFAULT
            else:
                auto_archive_after = channel.default_auto_archive_after
        else:
            if __debug__:
                if not isinstance(auto_archive_after, int):
                    raise AssertionError(
                        f'`auto_archive_after` can be `None`, `datetime`, got '
                        f'{auto_archive_after.__class__.__name__}; {auto_archive_after!r}.'
                    )
                
                if auto_archive_after not in AUTO_ARCHIVE_OPTIONS:
                    raise AssertionError(
                        f'`auto_archive_after` can be any of: {AUTO_ARCHIVE_OPTIONS}, got {auto_archive_after!r}.'
                    )
        
        if type_ is None:
            type_ = CHANNEL_TYPES.guild_thread_public
        else:
            type_ = preconvert_int_options(type_, 'type_', CHANNEL_TYPES.GROUP_THREAD)
        
        if __debug__:
            if not isinstance(invitable, bool):
                raise AssertionError(
                    f'`invitable` can be `bool`, got {invitable.__class__.__name__}; {invitable!r}.'
                )
        
        data = {
            'name': name,
            'auto_archive_duration': auto_archive_after // 60,
            'type': type_,
        }
        
        if (type_ == CHANNEL_TYPES.guild_thread_private) and (not invitable):
            data['invitable'] = invitable
        
        
        if message_id is None:
            coroutine = self.http.thread_create(channel_id, data)
        else:
            coroutine = self.http.thread_create_from_message(channel_id, message_id, data)
        
        channel_data = await coroutine
        if guild is None:
            guild_id = channel_data.get('guild_id', None)
            if (guild_id is None):
                guild = None
            else:
                guild_id = int(guild_id)
                guild = GUILDS.get(guild_id, None)
        
        return ChannelThread(channel_data, self, guild.id)
    
    
    async def thread_join(self, thread_channel):
        """
        Joins the client to the given thread channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        thread_channel : ``ChannelThread``, `int`
            The channel to join to, or it's identifier.
        
        Raises
        ------
        TypeError
            If `thread_channel`'s type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id = get_channel_id(thread_channel, ChannelThread)
        
        await self.http.thread_join(channel_id)
    
    
    async def thread_leave(self, thread_channel):
        """
        Leaves the client to the given thread channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        thread_channel : ``ChannelThread``, `int`
            The channel to join to, or it's identifier.
        
        Raises
        ------
        TypeError
            If `thread_channel`'s type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id = get_channel_id(thread_channel, ChannelThread)
        
        await self.http.thread_leave(channel_id)
    
    
    async def thread_user_get(self, thread_channel, user):
        """
        Gets a user's thread profile inside of a thread channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        thread_channel : ``ChannelThread``, `int`
            The channel to get the user's thread profile of.
        user : ``ClientUserBase``, `int`
            The user to get it's thread profile of.
        
        Returns
        -------
        user : ``ClientUserBase``
            The user, who's thread profile was requested.
        
        Raises
        ------
        TypeError
            - If `thread_channel`'s type is incorrect.
            - If `user`'s type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel, channel_id = get_channel_and_id(thread_channel, ChannelThread)
        user, user_id = get_user_and_id(user)
        
        thread_user_data = await self.http.thread_user_get(channel_id, user_id)
        
        if user is None:
            user = create_partial_user_from_id(user_id)
        
        if channel is None:
            channel = create_partial_channel_from_id(channel_id, 12, 0)
        
        thread_user_create(channel, user, thread_user_data)
        
        return user
    
    
    async def thread_user_add(self, thread_channel, user):
        """
        Adds the user to the thread channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        thread_channel : ``ChannelThread``, `int`
            The channel to add the user to, or it's identifier.
        user : ``ClientUserBase``, `int`
            The user to add to the the thread.
        
        Raises
        ------
        TypeError
            - If `thread_channel`'s type is incorrect.
            - If `user`'s type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id = get_channel_id(thread_channel, ChannelThread)
        user_id = get_user_id(user)
        
        if user_id == self.id:
            coroutine = self.http.thread_join(channel_id)
        else:
            coroutine = self.http.thread_user_add(channel_id, user_id)
        await coroutine
    
    
    async def thread_user_delete(self, thread_channel, user):
        """
        Deletes the user to the thread channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        thread_channel : ``ChannelThread``, `int`
            The channel to remove the user from, or it's identifier.
        user : ``ClientUserBase``, `int`
            The user to remove from the thread.
        
        Raises
        ------
        TypeError
            - If `thread_channel`'s type is incorrect.
            - If `user`'s type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id = get_channel_id(thread_channel, ChannelThread)
        user_id = get_user_id(user)
        
        if user_id == self.id:
            coroutine = self.http.thread_leave(channel_id)
        else:
            coroutine = self.http.thread_user_delete(channel_id, user_id)
        await coroutine
    
    
    async def thread_user_get_all(self, thread_channel):
        """
        Gets all the users of a thread channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        thread_channel : ``ChannelThread``, `int`
            The channel to get it's users of.
        
        Returns
        -------
        users : `list` of ``ClientUserBase``
            The created users.
        
        Raises
        ------
        TypeError
            If `thread_channel`'s type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        thread_channel, channel_id = get_channel_and_id(thread_channel, ChannelThread)
        
        thread_user_datas = await self.http.thread_user_get_all(channel_id)
        
        if thread_channel is None:
            thread_channel = create_partial_channel_from_id(channel_id, 12, 0)
        
        users = []
        for thread_user_data in thread_user_datas:
            user_id = int(thread_user_data['user_id'])
            user = create_partial_user_from_id(user_id)
            users.append(user)
            
            thread_user_create(thread_channel, user, thread_user_data)
        
        return users
    
    
    async def channel_thread_get_all_active(self, channel):
        """
        Requests all the active threads of the given channel.
        
        Parameters
        ----------
        channel : ``ChannelText``, `int`
            The channel to request the thread of, or it's identifier.
        
        Returns
        -------
        thread_channels : `list` of ``ChannelThread``
        
        Raises
        ------
        TypeError
            If `channel`'s type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild, channel_id = get_guild_and_guild_text_channel_id(channel)
        return await request_channel_thread_channels(self, guild, channel_id,
            type(self.http).channel_thread_get_chunk_active)
    
    
    async def channel_thread_get_all_archived_private(self, channel):
        """
        Requests all the archived private of the given channel.
        
        Parameters
        ----------
        channel : ``ChannelText``, `int`
            The channel to request the thread of, or it's identifier.
        
        Returns
        -------
        thread_channels : `list` of ``ChannelThread``
        
        Raises
        ------
        TypeError
            If `channel`'s type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild, channel_id = get_guild_and_guild_text_channel_id(channel)
        return await request_channel_thread_channels(self, guild, channel_id,
            type(self.http).channel_thread_get_chunk_archived_private)
    
    
    async def channel_thread_get_all_archived_public(self, channel):
        """
        Requests all the archived public threads of the given channel.
        
        Parameters
        ----------
        channel : ``ChannelText``, `int`
            The channel to request the thread of, or it's identifier.
        
        Returns
        -------
        thread_channels : `list` of ``ChannelThread``
        
        Raises
        ------
        TypeError
            If `channel`'s type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild, channel_id = get_guild_and_guild_text_channel_id(channel)
        return await request_channel_thread_channels(self, guild, channel_id,
            type(self.http).channel_thread_get_chunk_archived_public)
    
    
    async def channel_thread_get_all_self_archived(self, channel):
        """
        Requests all the archived private threads by the client.
        
        Parameters
        ----------
        channel : ``ChannelText``, `int`
            The channel to request the thread of, or it's identifier.
        
        Returns
        -------
        thread_channels : `list` of ``ChannelThread``
        
        Raises
        ------
        TypeError
            If `channel`'s type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild, channel_id = get_guild_and_guild_text_channel_id(channel)
        return await request_channel_thread_channels(self, guild, channel_id,
            type(self.http).channel_thread_get_chunk_self_archived)
    
    
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
            The maximal amount of users to return. Can be in range [1:1000], defaults to `1`.
        
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
            - If `query` was not given as `str`.
            - If `query`'s length is out of the expected range [1:32].
            - If `limit` was not given as `str`.
            - If `limit` is out fo expected range [1:1000].
        """
        guild, guild_id = get_guild_and_id(guild)
        
        if __debug__:
            if not isinstance(query, str):
                raise AssertionError(
                    f'`query` can be `str`, got {query.__class__.__name__}; {query!r}.'
                )
            
            query_length = len(query)
            if query_length < 1 or query_length > 1000:
                raise AssertionError(
                    f'`query` length can be in range [1:1000], got {query_length!r}; {query!r}.'
                )
            
            if not isinstance(limit, int):
                raise AssertionError(
                f'`limit` can be `int`, got {limit.__class__.__name__}; {limit!r}.'
                )
            
            if limit < 0 or limit > 1000:
                raise AssertionError(
                    f'`limit` can be in range [1:1000], got {limit!r}.'
                )
                
        data = {'query': query}
        
        if limit != 1:
            data['limit'] = limit
        
        data = await self.http.guild_user_search(guild_id, data)
        
        if guild is None:
            guild = create_partial_guild_from_id(guild_id)
        
        return [User._create_and_update(user_data, guild) for user_data in data]
    
    # integrations
    
    #TODO: decide if we should store integrations at Guild objects
    if API_VERSION > 7:
        async def integration_get_all(self, guild):
            """
            Requests the integrations of the given guild.
            
            This method is a coroutine.
            
            Parameters
            ----------
            guild : ``Guild``, `int`
                The guild, what's integrations will be requested.
            
            Returns
            -------
            integrations : `list` of ``Integration``
            
            Raises
            ------
            TypeError
                If `guild` was not given neither as ``Guild`` nor `int`.
            ConnectionError
                No internet connection.
            DiscordException
                If any exception was received from the Discord API.
            """
            guild_id = get_guild_id(guild)
            
            integration_datas = await self.http.integration_get_all(guild_id, None)
            return [Integration(integration_data) for integration_data in integration_datas]
    
    else:
        async def integration_get_all(self, guild):
            """
            Requests the integrations of the given guild.
            
            This method is a coroutine.
            
            Parameters
            ----------
            guild : ``Guild``, `int`
                The guild, what's integrations will be requested.
            
            Returns
            -------
            integrations : `list` of ``Integration``
            
            Raises
            ------
            TypeError
                If `guild` was not given neither as ``Guild`` nor `int`.
            ConnectionError
                No internet connection.
            DiscordException
                If any exception was received from the Discord API.
            """
            guild_id = get_guild_id(guild)
            
            integration_datas = await self.http.integration_get_all(guild_id, {'include_applications': True})
            return [Integration(integration_data) for integration_data in integration_datas]
    
    
    async def integration_create(self, guild, integration_id, type_):
        """
        Creates an integration at the given guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
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
        TypeError
            - If `guild` was not given neither as ``Guild`` nor `int`.
            - If `integration_id` was not given as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If `type_` is not given as `str`.
        """
        guild_id = get_guild_id(guild)
        
        integration_id_value = maybe_snowflake(integration_id)
        if integration_id_value is None:
            raise TypeError(
                f'`integration_id` can be `int`, got {integration_id.__class__.__name__}; {integration_id!r}.'
            )
        
        if __debug__:
            if not isinstance(type_, str):
                raise AssertionError(
                    f'`type_` can be `str`, got {type_.__class__.__name__}; {type_!r}.'
                )
        
        data = {
            'id'   : integration_id_value,
            'type' : type_,
        }
        
        data = await self.http.integration_create(guild_id, data)
        return Integration(data)
    
    
    async def integration_edit(self, integration, *, expire_behavior=..., expire_grace_period=...,
            enable_emojis=...):
        """
        Edits the given integration.
        
        This method is a coroutine.
        
        Parameters
        ----------
        integration : ``Integration``
            The integration to edit.
        expire_behavior : `int`, Optional (Keyword only)
            Can be `0` for kick or `1` for role  remove.
        expire_grace_period : `int`, Optional (Keyword only)
            The time in days, after the subscription will be ignored. Can be any of `(1, 3, 7, 14, 30)`.
        enable_emojis : `bool`, Optional (Keyword only)
            Whether the users can use the integration's emojis in Discord.
        
        Raises
        ------
        TypeError
            - If `expire_behavior` was not passed as `int`.
            - If `expire_grace_period` was not passed as `int`.
            - If `enable_emojis` was not passed as `bool`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `integration` was not given as ``Integration``.
            - If `expire_behavior` was not given neither as `None` nor as `int`.
            - If `expire_grace_period` was not given neither as `None` nor as `int`.
            - If `expire_behavior` is not any of: `(0, 1)`.
            - If `expire_grace_period` is not any of `(1, 3, 7, 14, 30)`.
            - If `enable_emojis` is neither `None`, `bool`.
        """
        if __debug__:
            if not isinstance(integration, Integration):
                raise AssertionError(
                    f'`integration` can be `{Integration.__name__}`, got '
                    f'{integration.__class__.__name__}; {integration!r}.'
                )
        
        detail = integration.detail
        if detail is None:
            return
        
        role = detail.role
        if role is None:
            return
        
        data = {}
        
        if expire_behavior is not ...:
            if __debug__:
                if not isinstance(expire_behavior, int):
                    raise AssertionError(
                        f'`expire_behavior` can be `None`, `int`, got '
                        f'{expire_behavior.__class__.__name__}; {expire_behavior!r}.'
                    )
                
                if expire_behavior not in (0, 1):
                    raise AssertionError(
                        f'`expire_behavior` should be 0 for kick, 1 for remove role, got {expire_behavior!r}.'
                    )
            
            data['expire_behavior'] = expire_behavior
        
        if expire_grace_period is not ...:
            if __debug__:
                if not isinstance(expire_grace_period, int):
                    raise AssertionError(
                        f'`expire_grace_period` can be `None`, `int`, got '
                        f'{expire_grace_period.__class__.__name__}.'
                    )
                
                if expire_grace_period not in (1, 3, 7, 14, 30):
                    raise AssertionError(
                        f'`expire_grace_period` can be one of `(1, 3, 7, 14, 30)`, got {expire_grace_period!r}.'
                    )
                
            data['expire_grace_period'] = expire_grace_period
   
        
        if (enable_emojis is not ...):
            if __debug__:
                if not isinstance(enable_emojis, bool):
                    raise AssertionError(
                        f'`enable_emojis` can be `None`, `bool`, got '
                        f'{enable_emojis.__class__.__name__}; {enable_emojis!r}.'
                    )
            
            data['enable_emoticons'] = enable_emojis
        
        await self.http.integration_edit(role.guild_id, integration.id, data)
    
    
    async def integration_delete(self, integration):
        """
        Deletes the given integration.
        
        This method is a coroutine.
        
        Parameters
        ----------
        integration : ``Integration``
            The integration what will be deleted.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If `integration` was not given as ``Integration``.
        """
        if __debug__:
            if not isinstance(integration, Integration):
                raise AssertionError(
                    f'`integration` can be `{Integration.__name__}`, got {integration.__class__.__name__}; '
                    f'{integration!r}.'
                )
        
        detail = integration.detail
        if detail is None:
            return
        
        role = detail.role
        if role is None:
            return
        
        await self.http.integration_delete(role.guild_id, integration.id)
    
    
    async def integration_sync(self, integration):
        """
        Sync the given integration's state.
        
        This method is a coroutine.
        
        Parameters
        ----------
        integration : ``Integration``
            The integration to sync.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If `integration` was not given as ``Integration``.
        """
        if __debug__:
            if not isinstance(integration, Integration):
                raise AssertionError(
                    f'`integration` can be `{Integration.__name__}`, got {integration.__class__.__name__}; '
                    f'{integration!r}.'
                )
        
        detail = integration.detail
        if detail is None:
            return
        
        role = detail.role
        if role is None:
            return
        
        await self.http.integration_sync(role.guild_id, integration.id)
    
    
    async def permission_overwrite_edit(self, channel, permission_overwrite, *, allow=..., deny=..., reason=None):
        """
        Edits the given permission overwrite.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ˙˙ChannelGuildMainBase``, `int`
            The channel where the permission overwrite is.
        permission_overwrite : ``PermissionOverwrite``
            The permission overwrite to edit.
        allow : `None`, ``Permission``, `int`, Optional (Keyword only)
            The permission overwrite's new allowed permission's value.
        deny : `None`, ``Permission``, `int`, Optional (Keyword only)
            The permission overwrite's new denied permission's value.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        TypeError
            If `channel` was not given neither as ``ChannelGuildMainBase`` nor as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `permission_overwrite` was not given as ``PermissionOverwrite``.
            - If `allow` was not given neither as `None`, ``Permission`` not other `int`.
            - If `deny` was not given neither as `None`, ``Permission`` not other `int`.
        """
        channel_id = get_channel_id(channel, ChannelGuildMainBase)
        
        if __debug__:
            if not isinstance(permission_overwrite, PermissionOverwrite):
                raise AssertionError(
                    f'`permission_overwrite` can be `{PermissionOverwrite.__name__}`, got '
                    f'{overwrite.__class__.__name__}; {overwrite!r}.'
                )
        
        if allow is ...:
            allow = permission_overwrite.allow
        else:
            if __debug__:
                if not isinstance(allow, int):
                    raise AssertionError(
                        f'`allow` can be `None`, `{Permission.__name__}`, `int`, got '
                        f'{allow.__class__.__name__}; {allow!r}.'
                    )
        
        if deny is ...:
            deny = permission_overwrite.deny
        else:
            if __debug__:
                if not isinstance(deny, int):
                    raise AssertionError(
                        f'`deny` can be `None`, `{Permission.__name__}`, `int`, got '
                        f'{deny.__class__.__name__}; {deny!r}.'
                    )
        
        data = {
            'allow': allow,
            'deny': deny,
            'type': permission_overwrite.target_type.value
        }
        
        await self.http.permission_overwrite_create(channel_id, overwrite.target.id, data, reason)
    
    
    async def permission_overwrite_delete(self, channel, permission_overwrite, *, reason=None):
        """
        Deletes the given permission overwrite.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ˙˙ChannelGuildMainBase``
            The channel where the permission overwrite is.
        permission_overwrite : ``PermissionOverwrite``
            The permission overwrite to delete.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.

        Raises
        ------
        TypeError
            If `channel` was not given neither as ``ChannelGuildMainBase`` nor as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If `permission_overwrite` was not given as ``PermissionOverwrite``.
        """
        channel_id = get_channel_id(channel, ChannelGuildMainBase)
        
        if __debug__:
            if not isinstance(permission_overwrite, PermissionOverwrite):
                raise AssertionError(
                    f'`permission_overwrite` can be `{PermissionOverwrite.__name__}`, got '
                    f'{permission_overwrite.__class__.__name__}; {permission_overwrite!r}.'
                )
        
        await self.http.permission_overwrite_delete(channel_id, permission_overwrite.target_id, reason)
    
    
    async def permission_overwrite_create(self, channel, target, allow, deny, *, reason=None):
        """
        Creates a permission overwrite at the given channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``ChannelGuildMainBase``, `int`
            The channel to what the permission overwrite will be added.
        target : ``Role``, ``ClientUserBase``
            The permission overwrite's target.
        allow : ``Permission``, `int`
            The permission overwrite's allowed permission's value.
        deny : ``Permission``, `int`
            The permission overwrite's denied permission's value.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        Returns
        -------
        permission_overwrite : ``PermissionOverwrite``
            A permission overwrite, what estimatedly is same as the one what Discord will create.
        
        Raises
        ------
        TypeError
            - If `channel` was not given neither as ``ChannelGuildMainBase`` nor as `int`.
            - If `target` was not passed neither as ``Role``,``User``, neither as ``Client``.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `allow` was not given neither as ``Permission`` nor as other `int`.
            - If `deny ` was not given neither as ``Permission`` not as other `int`.
        """
        channel_id = get_channel_id(channel, ChannelGuildMainBase)
        
        if isinstance(target, Role):
            permission_overwrite_target_type = PermissionOverwriteTargetType.role
        elif isinstance(target, ClientUserBase):
            permission_overwrite_target_type = PermissionOverwriteTargetType.user
        else:
            raise TypeError(
                f'`target` can be `{Role.__name__}`, `{ClientUserBase.__name__}`, got '
                f'{target.__class__.__name__}; {target!r}.'
            )
        
        if __debug__:
            if not isinstance(allow, int):
                raise AssertionError(
                    f'`allow` can be `{Permission.__name__}`, `int`, got {allow.__class__.__name__}; {allow!r}.'
                )
        
            if not isinstance(deny, int):
                raise AssertionError(
                    f'`deny` can be `{Permission.__name__}`, `int`, got {deny.__class__.__name__}; {deny!r}.'
                )
        
        data = {
            'target': target.id,
            'allow': allow,
            'deny': deny,
            'type': permission_overwrite_target_type.value,
        }
        
        await self.http.permission_overwrite_create(channel_id, target.id, data, reason)
        return PermissionOverwrite.custom(target, allow, deny)
    
    # Webhook management
    
    async def webhook_create(self, channel, name, *, avatar=None):
        """
        Creates a webhook at the given channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``ChannelText``, `int`
            The channel of the created webhook.
        name : `str`
            The name of the new webhook. It's length can be in range [1:80].
        avatar : `None`, `bytes-like` = `None`, Optional (Keyword only)
            The webhook's avatar. Can be `'jpg'`, `'png'`, `'webp'`, `'gif'` image's raw data. However if set as
            `'gif'`, it will not have any animation.
            
        Returns
        -------
        webhook : ``Webhook``
            The created webhook.
        
        Raises
        ------
        TypeError
            - If `channel` was not given neither as ``ChannelText`` nor as `int`.
            - If `avatar` was not given neither as `None`, `bytes-like`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `name` was not given as `str`.
            - If `name` range is out of the expected range [1:80].
            - If `avatar`'s type is not any of the expected ones: `'jpg'`, `'png'`, `'webp'`, `'gif'`.
        """
        channel_id = get_channel_id(channel, ChannelText)
        
        if __debug__:
            if not isinstance(name, str):
                raise AssertionError(
                    f'`name` can be `str`, got {name.__class__.__name__}; {name!r}.'
                )
            
            name_length = len(name)
            if name_length < 1 or name_length > 80:
                raise AssertionError(
                    f'`name` length can be in range [1:80], got {name_length!r}; {name!r}.'
                )
        
        data = {'name': name}
        
        if (avatar is not None):
            if not isinstance(avatar, (bytes, bytearray, memoryview)):
                raise TypeError(
                    f'`avatar` can `None`, `bytes-like`, got {avatar.__name__}; {reprlib.repr(avatar)}.'
                )
            
            if __debug__:
                media_type = get_image_media_type(avatar)
                if media_type not in VALID_ICON_MEDIA_TYPES_EXTENDED:
                    raise AssertionError(
                        f'Invalid `avatar` media type: {media_type}; got {reprlib.repr(avatar)}.'
                    )
            
            data['avatar'] = image_to_base64(avatar)
        
        data = await self.http.webhook_create(channel_id, data)
        return Webhook(data)
    
    
    async def webhook_get(self, webhook):
        """
        Requests the webhook by it's id.
        
        This method is a coroutine.
        
        Parameters
        ----------
        webhook : ``Webhook``, `int`
            The webhook to update or the webhook's id to get.
        
        Returns
        -------
        webhook : ``Webhook``
        
        Raises
        ------
        TypeError
            If `webhook` was not given neither as ``Webhook`` neither as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        See Also
        --------
        ``.webhook_get_token`` : Getting webhook with Discord's webhook API.
        
        Notes
        -----
        If the webhook already loaded and if it's guild's webhooks are up to date, no request is done.
        """
        webhook, webhook_id = get_webhook_and_id(webhook)
        
        data = await self.http.webhook_get(webhook_id)
        if webhook is None:
            webhook = Webhook(data)
        else:
            webhook._update_attributes(data)
        
        return webhook
    
    
    async def webhook_get_token(self, webhook):
        """
        Requests the webhook through Discord's webhook API. The client do not needs to be in the guild of the webhook.
        
        This method is a coroutine.
        
        Parameters
        ----------
        webhook : ``Webhook``, `tuple` (`int`, `str`)
            The webhook to update or the webhook's id and token.
        
        Returns
        -------
        webhook : ``Webhook``
        
        Raises
        ------
        TypeError
            If `webhook` was not given neither as ``Webhook`` neither as a `tuple` (`int`, `str`).
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        If the webhook already loaded and if it's guild's webhooks are up to date, no request is done.
        """
        webhook, webhook_id, webhook_token = get_webhook_and_id_token(webhook)
        
        if (webhook is None):
            webhook = create_partial_webhook_from_id(webhook_id, webhook_token)
        
        data = await self.http.webhook_get_token(webhook_id, webhook_token)
        webhook._set_attributes(data)
        return webhook
    
    
    async def webhook_get_all_channel(self, channel):
        """
        Requests all the webhooks of the channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``ChannelText``, `int`
            The channel, what's webhooks will be requested.
        
        Returns
        -------
        webhooks : `list` of ``Webhook` objects
        
        Raises
        ------
        TypeError
            If `channel` was not given neither as ``ChannelText``, neither as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
            
            You may expect the following exceptions:
            
            +---------------+-----------------------+---------------------------------------------------------------+
            | Error code    | Internal name         | Reason                                                        |
            +===============+=======================+===============================================================+
            | 10003         | unknown_channel       | The channel not exists.                                       |
            +---------------+-----------------------+---------------------------------------------------------------+
            | 50013         | missing_permissions   | You need `manage_webhooks` permission. (Or the client has no  |
            |               |                       | access to the channel.)                                       |
            +---------------+-----------------------+---------------------------------------------------------------+
            | 60003         | MFA_required          | You need to have multi-factor authorization to do this        |
            |               |                       | operation (guild setting dependent). For bot accounts it      |
            |               |                       | means their owner needs mfa.                                  |
            +---------------+-----------------------+---------------------------------------------------------------+
            
            > Discord drops `Forbidden (403), code=50013: Missing Permissions` instead of
            > `Forbidden (403), code=50001: Missing Access`.
        
        AssertionError
            If `channel` was given as a channel's identifier but it detectably not refers to a ``ChannelText``.
        
        Notes
        -----
        No request is done, if the passed channel is partial, or if the channel's guild's webhooks are up to date.
        """
        channel_id = get_channel_id(channel, ChannelText)
        
        data = await self.http.webhook_get_all_channel(channel_id)
        return [Webhook(webhook_data) for webhook_data in data]
    
    
    async def webhook_get_own_channel(self, channel):
        """
        Requests the webhooks of the given channel and returns the first owned one.
        
        Parameters
        ----------
        channel : ``ChannelText``, `int`
            The channel, what's webhooks will be requested.
        
        Returns
        -------
        webhooks : `list` of ``Webhook` objects
        """
        webhooks = await self.webhook_get_all_channel(channel)
        
        application_id = self.application.id
        for webhook in webhooks:
            if webhook.application_id == application_id:
                return webhook
        
        return None
    
    
    async def webhook_get_all_guild(self, guild):
        """
        Requests the webhooks of the given guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, what's webhooks will be requested.
        
        Returns
        -------
        webhooks : `list` of ``Webhook` objects
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as ``Guild`` nor as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        No request is done, if the guild's webhooks are up to date.
        """
        guild_id = get_guild_id(guild)
        
        webhook_datas = await self.http.webhook_get_all_guild(guild_id)
        return [Webhook(webhook_data) for webhook_data in webhook_datas]
    
    
    async def webhook_delete(self, webhook):
        """
        Deletes the webhook.
        
        This method is a coroutine.
        
        Parameters
        ----------
        webhook : ``Webhook``, `int`
            The webhook to delete.
        
        Raises
        ------
        TypeError
            If `webhook` was not given neither as ``Webhook``, `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        See Also
        --------
        ``.webhook_delete_token`` : Deleting webhook with Discord's webhook API.
        """
        webhook_id = get_webhook_id(webhook)
        
        await self.http.webhook_delete(webhook_id)
    
    
    async def webhook_delete_token(self, webhook):
        """
        Deletes the webhook through Discord's webhook API.
        
        This method is a coroutine.
        
        Parameters
        ----------
        webhook : ``Webhook``, `tuple` (`int`, `str`)
            The webhook to delete.

        Parameters
        ----------
        webhook : ``Webhook``
            The webhook to delete.
        
        Raises
        ------
        TypeError
            If `webhook` was not given neither as ``Webhook`` neither as a `tuple` (`int`, `str`).
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        webhook_id, webhook_token = get_webhook_id_token(webhook)
        
        await self.http.webhook_delete_token(webhook_id, webhook_token)
    
    # later there gonna be more stuff that's why 2 different
    async def webhook_edit(self, webhook, *, name=..., avatar=..., channel=...):
        """
        Edits and updates the given webhook.
        
        This method is a coroutine.
        
        Parameters
        ----------
        webhook : ``Webhook``, `int`
            The webhook to edit.
        name : `str`, Optional (Keyword only)
            The webhook's new name. It's length can be in range [1:80].
        avatar : `None`, `bytes-like`, Optional (Keyword only)
            The webhook's new avatar. Can be `'jpg'`, `'png'`, `'webp'`, `'gif'` image's raw data. However if set as
            `'gif'`, it will not have any animation. If passed as `None`, will remove the webhook's current avatar.
        channel : ``ChannelText``, `int`, Optional (Keyword only)
            The webhook's channel.
        
        Raises
        ------
        TypeError
            - If `webhook` was not given neither as ``Webhook`` neither as `int`.
            - If `avatar` was not given neither as `None` nor as `bytes-like`.
            - If `channel` was not given neither as ``ChannelText`` neither as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `name` was given but not as `str`.
            - If `name`'s length is out of range [1:80].
            - If `avatar`'s type is not any of the expected ones: `'jpg'`, `'png'`, `'webp'`, `'gif'`.
        
        See Also
        --------
        ``.webhook_edit_token`` : Editing webhook with Discord's webhook API.
        """
        webhook_id = get_webhook_id(webhook)
        
        data = {}
        
        if (name is not ...):
            if __debug__:
                if not isinstance(name, str):
                    raise AssertionError(
                        f'`name` can be `str`, got {name.__class__.__name__}; {name!r}.'
                    )
                
                name_length = len(name)
                if name_length < 1 or name_length > 80:
                    raise AssertionError(
                        f'The length of the name can be in range [1:80], got {name_length}; {name!r}.'
                    )
            
            data['name'] = name
        
        if (avatar is not ...):
            if avatar is None:
                avatar_data = None
            else:
                if not isinstance(avatar, (bytes, bytearray, memoryview)):
                    raise TypeError(
                        f'`avatar` can be `None`, `bytes-like`, got {avatar.__class__.__name__}; '
                        f'{reprlib.repr(avatar)}.'
                    )
                
                if __debug__:
                    media_type = get_image_media_type(avatar)
                    
                    if self.premium_type.value:
                        valid_icon_media_types = VALID_ICON_MEDIA_TYPES_EXTENDED
                    else:
                        valid_icon_media_types = VALID_ICON_MEDIA_TYPES
                    
                    if media_type not in valid_icon_media_types:
                        raise AssertionError(
                            f'Invalid `avatar` type for the client: {media_type}; got {reprlib.repr(avatar)}.'
                        )
                
                avatar_data = image_to_base64(avatar)
            
            data['avatar'] = avatar_data
        
        if (channel is not ...):
            if isinstance(channel, ChannelText):
                channel_id = channel.id
            else:
                channel_id = maybe_snowflake(channel)
                if channel_id is None:
                    raise TypeError(
                        f'`channel` can be `{ChannelText.__name__}`, `int`, got {channel.__class__.__name__}; '
                        f'{channel!r}.'
                    )
            
            data['channel_id'] = channel_id
        
        if not data:
            return # Save 1 request
        
        data = await self.http.webhook_edit(webhook_id, data)
        webhook._set_attributes(data)
    
    
    async def webhook_edit_token(self, webhook, *, name=..., avatar=...):
        """
        Edits and updates the given webhook through Discord's webhook API.
        
        This method is a coroutine.
        
        Parameters
        ----------
        webhook : ``Webhook``, `tuple` (`int`, `str`)
            The webhook to edit.
        name : `str`, Optional (Keyword only)
            The webhook's new name. It's length can be between `1` and `80`.
        avatar : `None`, `bytes-like`, Optional (Keyword only)
            The webhook's new avatar. Can be `'jpg'`, `'png'`, `'webp'`, `'gif'` image's raw data. However if set as
            `'gif'`, it will not have any animation. If passed as `None`, will remove the webhook's current avatar.
        
        Returns
        -------
        webhook : ``Webhook``
            The updated webhook.
        
        Raises
        ------
        TypeError
            - If `webhook` was not given neither as ``Webhook`` neither as a `tuple` (`int`, `str`).
            - If `avatar` was not given neither as `None` nor as `bytes-like`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `name` was given but not as `str`.
            - If `name`'s length is out of range [1:80].
            - If `avatar`'s type is not any of the expected ones: `'jpg'`, `'png'`, `'webp'`, `'gif'`.
        
        Notes
        -----
        This endpoint cannot edit the webhook's channel, like ``.webhook_edit``.
        """
        webhook, webhook_id, webhook_token = get_webhook_and_id_token(webhook)
        
        data = {}
        
        if (name is not ...):
            if __debug__:
                if not isinstance(name, str):
                    raise AssertionError(
                        f'`name` can be `None`, `str`, got {name.__class__.__name__}; {name!r}.'
                    )
                
                name_length = len(name)
                if name_length < 1 or name_length > 80:
                    raise AssertionError(
                        f'`name`\'s length can be in range [1:80], got {name_length}; {name!r}.'
                    )
            
            data['name'] = name
        
        if (avatar is not ...):
            if avatar is None:
                avatar_data = None
            else:
                if not isinstance(avatar, (bytes, bytearray, memoryview)):
                    raise TypeError(
                        f'`avatar` can be `None`, `bytes-like`, got {avatar.__class__.__name__}; '
                        f'{reprlib.repr(avatar)}.'
                    )
                
                if __debug__:
                    media_type = get_image_media_type(avatar)
                    
                    if self.premium_type.value:
                        valid_icon_media_types = VALID_ICON_MEDIA_TYPES_EXTENDED
                    else:
                        valid_icon_media_types = VALID_ICON_MEDIA_TYPES
                    
                    if media_type not in valid_icon_media_types:
                        raise AssertionError(
                            f'Invalid avatar type for the client: {media_type}; got {reprlib.repr(avatar)}.'
                        )
                
                avatar_data = image_to_base64(avatar)
            
            data['avatar'] = avatar_data
        
        if not data:
            return # Save 1 request
        
        data = await self.http.webhook_edit_token(webhook_id, webhook_token, data)
        
        if webhook is None:
            webhook = Webhook(data)
        else:
            webhook._set_attributes(data)
        
        return webhook
    
    
    async def webhook_message_create(self, webhook, content=None, *, embed=None, file=None, allowed_mentions=...,
            components=None, tts=False, name=None, avatar_url=None, thread=None, wait=False):
        """
        Sends a message with the given webhook. If there is nothing to send, or if `wait` was not passed as `True`
        returns `None`.
        
        This method is a coroutine.
        
        Parameters
        ----------
        webhook : ``Webhook``, `tuple` (`int`, `str`)
            The webhook through what will the message be sent.
        
        content : `None`, `str`, ``EmbedBase``, `Any` = `None`, Optional
            The message's content if given. If given as `str` or empty string, then no content will be sent, meanwhile
            if any other non `str`, ``EmbedBase`` is given, then will be casted to string.
            
            If given as ``EmbedBase``, then is sent as the message's embed.
            
        embed : `None`, ``EmbedBase``, `list` of ``EmbedBase`` = `None`, Optional (Keyword only)
            The embedded content of the message.
            
            If `embed` and `content` parameters are both given as  ``EmbedBase``, then `AssertionError` is
            raised.
        
        file : `None`, `Any` = `None`, Optional (Keyword only)
            A file or files to send. Check ``create_file_form`` for details.
        
        allowed_mentions : `None`, `str`, ``UserBase``, ``Role``, `list` of (`str`, ``UserBase``, ``Role`` )
                , Optional (Keyword only)
            
            Which user or role can the message ping (or everyone). Check ``parse_allowed_mentions`` for details.
        
        components : `None`, ``ComponentBase``, (`tuple`, `list`) of (``ComponentBase``, (`tuple`, `list`) of
                ``ComponentBase``) = `None`, Optional (Keyword only)
            Components attached to the message.
            
            > `components` do not count towards having any content in the message.
        
        tts : `bool` = `False`, Optional (Keyword only)
            Whether the message is text-to-speech.
        
        name : `None`, `str` = `None`, Optional (Keyword only)
            The message's author's new name. Default to the webhook's name by Discord.
        
        avatar_url : `None`, `str` = `None`, Optional (Keyword only)
            The message's author's avatar's url. Defaults to the webhook's avatar' url by Discord.
        
        thread : `None`, `ChannelThread`, `int` = `None`, Optional (Keyword only)
            The thread of the webhook's channel where the message should be sent.
        
        wait : `None`, `bool` = `None`, Optional (Keyword only)
            Whether we should wait for the message to send and receive it's data as well.
        
        Returns
        -------
        message : ``Message``, `None`
            Returns `None` if there is nothing to send or if `wait` was given as `False` (so by default).
        
        Raises
        ------
        TypeError
            - If `webhook` was not given neither as ``Webhook`` neither as a `tuple` (`int`, `str`).
            - If `allowed_mentions` contains an element of invalid type.
            - If `embed` was not given neither as ``EmbedBase`` nor as `list`, `tuple` of ``EmbedBase``-s.
            - `content` parameter was given as ``EmbedBase``, meanwhile `embed` parameter was given as well.
            - If invalid file type would be sent.
            - If `thread` was not given either as `None`, ``ChannelThread`` nor as `int`.
            - If `components` type is incorrect.
        ValueError
            - If `allowed_mentions`'s elements' type is correct, but one of their value is invalid.
            - If more than `10` files would be sent.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `name` was not passed neither as `None`, `str`.
            - If `name` was passed as `str`, but it's length is out of range [1:32].
            - If `avatar_url` was not given as `str`.
            - If `tts` was not given as `bool`.
            - If `wait` was not given as `bool`.
            - If `embed` contains a non ``EmbedBase`` element.
            - If both `content` and `embed` fields are embeds.
        
        See Also
        --------
        - ``.message_create`` : Create a message with your client.
        - ``.webhook_message_edit`` : Edit a message created by a webhook.
        - ``.webhook_message_delete`` : Delete a message created by a webhook.
        - ``.webhook_message_get`` : Get a message created by a webhook.
        """
        webhook, webhook_id, webhook_token = get_webhook_and_id_token(webhook)
        
        if thread is None:
            thread_id = 0
        elif isinstance(thread, ChannelThread):
            thread_id = thread.id
        else:
            thread_id = maybe_snowflake(thread)
            if thread_id is None:
                raise TypeError(
                    f'`thread` can be `None`, `{ChannelThread.__name__}`, `int`, '
                    f'got {thread.__class__.__name__}; {thread!r}.'
                )
        
        content, embed = validate_content_and_embed(content, embed, False)
        
        components = get_components_data(components, False)
        
        if __debug__:
            if not isinstance(tts, bool):
                raise AssertionError(
                    f'`tts` can be `bool`, got {tts.__class__.__name__}; {tts!r}.'
                )
            
            if not isinstance(wait, bool):
                raise AssertionError(
                    f'`wait` can be `bool`, got {wait.__class__.__name__}; {wait!r}.'
                )
        
        message_data = {}
        contains_content = False
        
        if (content is not None):
            message_data['content'] = content
            contains_content = True
        
        if (embed is not None):
            message_data['embeds'] = [embed.to_data() for embed in embed]
            contains_content = True
        
        if (allowed_mentions is not ...):
            message_data['allowed_mentions'] = parse_allowed_mentions(allowed_mentions)
        
        if (components is not None):
            message_data['components'] = components
        
        if tts:
            message_data['tts'] = True
        
        if (avatar_url is not None):
            if __debug__:
                if not isinstance(avatar_url, str):
                    raise AssertionError(
                        f'`avatar_url` can be `None`, `str`, got {avatar_url.__class__.__name__}; {avatar_url!r}.'
                    )
            
            message_data['avatar_url'] = avatar_url
        
        if (name is not None):
            if __debug__:
                if not isinstance(name, str):
                    raise AssertionError(
                        f'`name` cane be given either as `None`, `str instance, got '
                        f'{name.__class__.__name__}; {name!r}.'
                    )
                
                name_length = len(name)
                if name_length > 32:
                    raise AssertionError(
                        f'`name` length can be in range [1:32], got {name_length}; {name!r}.'
                    )
            
            if name:
                message_data['username'] = name
        
        message_data = add_file_to_message_data(message_data, file, contains_content, False)
        if message_data is None:
            return
        
        query_parameters = None
        if wait:
            if query_parameters is None:
                query_parameters = {}
            
            query_parameters['wait'] = wait
        
        if thread_id:
            if query_parameters is None:
                query_parameters = {}
            
            query_parameters['thread_id'] = thread_id
        
        message_data = await self.http.webhook_message_create(webhook_id, webhook_token, message_data, query_parameters)
        
        if not wait:
            return
        
        # Use goto
        while True:
            if (webhook is not None):
                channel = webhook.channel
                if (channel is not None):
                    break
            
            channel_id = int(message_data['channel_id'])
            channel = create_partial_channel_from_id(channel_id, 0, 0)
            break
        
        return channel._create_new_message(message_data)
    
    
    async def webhook_message_edit(self, webhook, message, content=..., *, embed=..., file=..., allowed_mentions=...,
            components=...):
        """
        Edits the message sent by the given webhook. The message's author must be the webhook itself.
        
        Parameters
        ----------
        webhook : ``Webhook``, `tuple` (`int`, `str`)
            The webhook who created the message.
        
        message : ``Message``, ``MessageRepr``, `int`
            The webhook's message to edit.
        
        content : `None`, `str`, ``EmbedBase``, `Any`, Optional
            The new content of the message.
            
            If given as `str` then the message's content will be edited with it. If given as any non ``EmbedBase``
            instance, then it will be cased to string first.
            
            If given as ``EmbedBase``, then the message's embeds will be edited with it.
        
        embed : `None`, ``EmbedBase``, `list` of ``EmbedBase``, Optional (Keyword only)
            The new embedded content of the message. By passing it as `None`, you can remove the old.
            
            > If `embed` and `content` parameters are both given as  ``EmbedBase``, then `AssertionError` is
            raised.
        
        file : `None`, `Any`, Optional (Keyword only)
            A file or files to send. Check ``create_file_form`` for details.
        
        allowed_mentions : `None`,  `str`, ``UserBase``, ``Role``, `list` of (`str`, ``UserBase``, ``Role`` )
                , Optional (Keyword only)
            Which user or role can the message ping (or everyone). Check ``parse_allowed_mentions``
            for details.
        
        components : `None`, ``ComponentBase``, (`tuple`, `list`) of (``ComponentBase``, (`tuple`, `list`) of
                ``ComponentBase``), Optional (Keyword only)
            Components attached to the message.
        
        Raises
        ------
        TypeError
            - If `webhook` was not given neither as ``Webhook`` neither as a `tuple` (`int`, `str`).
            - If `allowed_mentions` contains an element of invalid type.
            - If `embed` was not given neither as ``EmbedBase`` nor as `list`, `tuple` of ``EmbedBase``-s.
            - `content` parameter was given as ``EmbedBase``, meanwhile `embed` parameter was given as well.
            - `message` was given as `None`. Make sure to use ``Client.webhook_message_create`` with `wait=True` and by
                giving any content to it as well.
            - `message` was not given neither as ``Message``, ``MessageRepr``  or `int`.
            - If `components` type is incorrect.
        ValueError
            - If `allowed_mentions`'s elements' type is correct, but one of their value is invalid.
            - If more than `10` file would be sent.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `message` was detectably not sent by the `webhook`.
            - If `embed` contains a non ``EmbedBase`` element.
            - If both `content` and `embed` fields are embeds.
        
        See Also
        --------
        - ``.message_edit`` : Edit your own messages.
        - ``.webhook_message_create`` : Create a message with a webhook.
        - ``.webhook_message_delete`` : Delete a message created by a webhook.
        - ``.webhook_message_get`` : Get a message created by a webhook.
        
        Notes
        -----
        Embed messages ignore suppression with their endpoint, not like ``.message_edit`` endpoint.
        
        Editing the message with empty string is broken.
        """
        webhook_id, webhook_token = get_webhook_id_token(webhook)
        
        # Detect message id
        # 1.: Message
        # 2.: int (str)
        # 3.: MessageRepr
        # 4.: None -> raise
        # 5.: raise
        
        if isinstance(message, Message):
            if __debug__:
                if message.author.id != webhook_id:
                    raise AssertionError(
                        f'The message was not sent by the webhook, got {message!r}.'
                    )
                
            message_id = message.id
        else:
            message_id = maybe_snowflake(message)
            if (message_id is not None):
                pass
            
            elif isinstance(message, MessageRepr):
                # Cannot check author id, skip
                message_id = message.id
            
            elif message is None:
                raise TypeError(
                    f'`message` was given as `None`. Make sure to use '
                    f'`{self.__class__.__name__}.webhook_message_create` with giving content and by passing '
                    f'`wait` parameter as `True` as well.'
                )
            
            else:
                raise TypeError(
                    f'`message` can be `{Message.__name__}`, `{MessageRepr.__name__}`, int`, got '
                    f'{message.__class__.__name__}; {message!r}.'
                )
        
        content, embed = validate_content_and_embed(content, embed, True)
        
        components = get_components_data(components, True)
        
        # Build payload
        message_data = {}
        
        # Discord docs say, content can be nullable, but nullable content is just ignored.
        if (content is not ...):
            message_data['content'] = content
        
        if (embed is not ...):
            if (embed is not None):
                embed = [embed.to_data() for embed in embed]
            
            message_data['embeds'] = embed
        
        if (allowed_mentions is not ...):
            message_data['allowed_mentions'] = parse_allowed_mentions(allowed_mentions)
        
        if (components is not ...):
            message_data['components'] = components
        
        message_data = add_file_to_message_data(message_data, file, True, True)
        
        # We receive the new message data, but we do not update the message, so dispatch events can get the difference.
        await self.http.webhook_message_edit(webhook_id, webhook_token, message_id, message_data)
    
    
    async def webhook_message_delete(self, webhook, message):
        """
        Deletes the message sent by the webhook.
        
        This method is a coroutine.
        
        Parameters
        ----------
        webhook : ``Webhook``, `tuple` (`int`, `str`)
            The webhook who created the message.
        message : ``Message``, ``MessageRepr``, `int`
            The webhook's message to delete.
        
        Raises
        ------
        TypeError
            - If `message` was not given neither as ``Message``, ``MessageRepr`` neither as `int`.
            - If `webhook` was not given neither as ``Webhook`` neither as a `tuple` (`int`, `str`).
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If `message` was detectably not sent by the `webhook`.
        
        See Also
        --------
        - ``.message_delete`` : Delete a message.
        - ``.webhook_message_create`` : Create a message with a webhook.
        - ``.webhook_message_edit`` : Edit a message created by a webhook.
        - ``.webhook_message_get`` : Get a message created by a webhook.
        """
        webhook_id, webhook_token = get_webhook_id_token(webhook)
        
        # Detect message id
        # 1.: Message
        # 2.: int
        # 3.: MessageRepr
        # 4.: None -> raise
        # 5.: raise
        
        if isinstance(message, Message):
            if __debug__:
                if message.author.id != webhook_id:
                    raise AssertionError(
                        f'The message was not sent by the webhook, got {message!r}.'
                    )
            
            message_id = message.id
        
        else:
            message_id = maybe_snowflake(message)
            if (message_id is not None):
                pass
            
            elif isinstance(message, MessageRepr):
                # Cannot check author id, skip
                message_id = message.id
            
            elif message is None:
                raise TypeError(
                    f'`message` was given as `None`. Make sure to use '
                    f'`{self.__class__.__name__}.webhook_message_create` with giving content and by passing '
                    f'`wait` parameter as `True` as well.'
                )
            
            else:
                raise TypeError(
                    f'`message` can be `{Message.__name__}`, `{MessageRepr.__name__}`, int`, got '
                    f'{message.__class__.__name__}; {message!r}.'
                )
        
        await self.http.webhook_message_delete(webhook_id, webhook_token, message_id)
    
    
    async def webhook_message_get(self, webhook, message_id):
        """
        Gets a previously sent message with the webhook.
        
        This method is a coroutine.
        
        Parameters
        ----------
        webhook : ``Webhook``, `tuple` (`int`, `str`)
            The webhook who created the message.
        message_id : `int`
            The webhook's message's identifier to get.
        
        Returns
        -------
        message : ``Message``
        
        Raises
        ------
        TypeError
            - If `webhook` was not given neither as ``Webhook`` neither as a `tuple` (`int`, `str`).
            - If `message_id` was not given as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        See Also
        --------
        - ``.message_get`` : Get a message.
        - ``.webhook_message_create`` : Create a message with a webhook.
        - ``.webhook_message_edit`` : Edit a message created by a webhook.
        - ``.webhook_message_delete`` : Delete a message created by a webhook.
        """
        webhook_id, webhook_token = get_webhook_id_token(webhook)
        
        message_id_value = maybe_snowflake(message_id)
        if message_id_value is None:
            raise TypeError(
                f'`message_id` can be `int`, got {message_id.__class__.__name__}; {message_id!r}.'
            )
        
        message_data = await self.http.webhook_message_get(webhook_id, webhook_token, message_id_value)
        return Message(message_data)
    
    
    async def emoji_get(self, guild, emoji):
        """
        Requests the emoji by it's id at the given guild. If the client's logging in is finished, then it should have
        it's every emoji loaded already.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, where the emoji is.
        emoji : ``Emoji``, `int`
            The emoji to get.
        
        Returns
        -------
        emoji : ``Emoji``
        
        Raises
        ------
        TypeError
            - If `guild` was not given neither as ``Guild`` nor as `int`.
            - If `emoji` was not given neither as ``Emoji`` nor as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild, guild_id = get_guild_and_id(guild)
        
        if isinstance(emoji, Emoji):
            emoji_id = emoji.id
        else:
            emoji_id = maybe_snowflake(emoji)
            if emoji_id is None:
                raise TypeError(
                    f'`emoji` can be `{Emoji.__name__}`, `int`, got {emoji.__class__.__name__}; {emoji!r}.'
                )
            
            emoji = EMOJIS.get(emoji, None)
        
        emoji_data = await self.http.emoji_get(guild_id, emoji_id)
        
        if (emoji is None) or emoji.partial:
            if guild is None:
                guild = create_partial_guild_from_id(guild_id)
        
            emoji = Emoji(emoji_data, guild_id)
        else:
            emoji._update_attributes(emoji_data)
        
        return emoji
    
    
    async def guild_sync_emojis(self, guild):
        """
        Syncs the given guild's emojis with the wrapper.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, what's emojis will be synced.
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as ``Guild`` nor as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild, guild_id = get_guild_and_id(guild)
        
        data = await self.http.emoji_guild_get_all(guild_id)
        
        if guild is None:
            guild = create_partial_guild_from_id(guild_id)
        
        guild._sync_emojis(data)
    
    
    async def emoji_create(self, guild, name, image, *, roles=None, reason=None):
        """
        Creates an emoji at the given guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, where the emoji will be created.
        name : `str`
            The emoji's name. It's length can be between `2` and `32`.
        image : `bytes-like`
            The emoji's icon.
        roles : None`, (`list`, `set`, `tuple`) of (``Role``, `int`) = `None`, Optional (Keyword only)
            Whether the created emoji should be limited only to users with any of the specified roles.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Will show up at the guild's audit logs.
        
        Returns
        -------
        emoji : ``Emoji``
            The created emoji.
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as ``Guild`` nor as `int`.
            If `roles` contains a non ``Role``, `int` element.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `name` was not given as `str`.
            - If `name` length is out of the expected range [1:32].
            - If `roles` was not given neither as `None`, `list`, `tuple`, `set`.
        Notes
        -----
        Only some characters can be in the emoji's name, so every other character is filtered out.
        """
        guild_id = get_guild_id(guild)
        
        if __debug__:
            if not isinstance(name, str):
                raise AssertionError(
                    f'`name` can be `str`, got {name.__class__.__name__}; {name!r}.'
                )
        
        name = ''.join(_VALID_NAME_CHARS.findall(name))
        
        if __debug__:
            name_length = len(name)
            if name_length < 2 or name_length > 32:
                raise AssertionError(
                    f'`name` length can be in range [2:32], got {name_length!r}; {name!r}.'
                )
        
        role_ids = set()
        if (roles is not None):
            if __debug__:
                if not isinstance(roles, (list, set, tuple)):
                    raise AssertionError(
                        f'`roles` can be `None`, `list`, `set`, `tuple`, got {roles.__class__.__name__}; {roles!r}.'
                    )
            
            for role in roles:
                if isinstance(role, Role):
                    role_id = role.id
                else:
                    role_id = maybe_snowflake(role)
                    if role_id is None:
                        raise TypeError(
                            f'`roles` contains not `{Role.__name__}`, `int` element, '
                            f'got {role.__class__.__name__}; {role!r}; roles={roles!r}.'
                        )
                
                role_ids.add(role_id)
            
        image = image_to_base64(image)
        
        data = {
            'name': name,
            'image': image,
            'roles': role_ids
        }
        
        data = await self.http.emoji_create(guild_id, data, reason)
        
        emoji = Emoji(data, guild_id)
        emoji.user = self
        return emoji
    
    
    async def emoji_delete(self, emoji, *, reason=None):
        """
        Deletes the given emoji.
        
        This method is a coroutine.
        
        Parameters
        ----------
        emoji : ``Emoji``
            The emoji to delete.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Will show up at the respective guild's audit logs.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If `emoji` was not given as ``Emoji``.
        """
        snowflake_pair = get_guild_id_and_emoji_id(emoji)
        if (snowflake_pair is None):
            return
        guild_id, emoji_id = snowflake_pair
        await self.http.emoji_delete(guild_id, emoji_id, reason=reason)
    
    
    async def emoji_edit(self, emoji, *, name=..., roles=..., reason=None):
        """
        Edits the given emoji.
        
        This method is a coroutine.
        
        Parameters
        ----------
        emoji : ``Emoji``
            The emoji to edit.
        name : `str`, Optional (Keyword only)
            The emoji's new name. It's length can be in range [2:32].
        roles : `None`, (`list`, `set`, `tuple`) of (``Role``, `int`), Optional (Keyword only)
            The roles to what is the role limited. By passing it as `None`, or as an empty `list` you can remove the
            current ones.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        TypeError
            If `roles` contains a non ``Role``, `int` element.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `emoji` was not given as ``Emoji``.
            - If `name` was not given as `str`.
            - If `name` length is out of the expected range [1:32].
            - If `roles` was not given neither as `None`, `list`, `tuple`, `set`.
        """
        if __debug__:
            if not isinstance(emoji, Emoji):
                raise AssertionError(
                    f'`emoji` can be `{Emoji.__name__}`, got {emoji.__class__.__name__}; {emoji!r}.'
                )
        
        guild = emoji.guild
        if guild is None:
            return
        
        data = {}
        
        # name is required
        if (name is ...):
            name = emoji.name
        else:
            if __debug__:
                if not isinstance(name, str):
                    raise AssertionError(
                        f'`name` can be `str`, got {name.__class__.__name__}; {name!r}.'
                    )
            
            name = ''.join(_VALID_NAME_CHARS.findall(name))
            
            if __debug__:
                name_length = len(name)
                if name_length < 2 or name_length > 32:
                    raise AssertionError(
                        f'`name` length can be in range [2:32], got {name_length!r}; {name!r}.'
                    )
        
        data['name'] = name
        
        # roles are not required
        if (roles is not ...):
            role_ids = set()
            if (roles is not None):
                if __debug__:
                    if not isinstance(roles, (list, set, tuple)):
                        raise AssertionError(
                            f'`roles` can be `None`, `list`, `set`, `tuple`, got '
                            f'{roles.__class__.__name__}; {roles!r}.'
                        )
                
                for role in roles:
                    if isinstance(role, Role):
                        role_id = role.id
                    else:
                        role_id = maybe_snowflake(role)
                        if role_id is None:
                            raise TypeError(
                                f'`roles` contains not `{Role.__name__}`, `int` element, got '
                                f'{role.__class__.__name__}; {role!r}; roles={roles!r}.'
                            )
                    
                    role_ids.add(role_id)
            
            data['roles'] = role_ids
        
        await self.http.emoji_edit(guild.id, emoji.id, data, reason)
    
    # Invite management
    
    async def vanity_invite_get(self, guild):
        """
        Returns the vanity invite of the given guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, what's invite will be returned.
        
        Returns
        -------
        invite : `None`, ``Invite``
            The vanity invite of the `guild`, `None` if it has no vanity invite.
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as ``Guild`` nor as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild, guild_id = get_guild_and_id(guild)
        
        if (guild is None) or guild.partial:
            invite_data = await self.http.vanity_invite_get(guild_id)
            vanity_code = invite_data['code']
        else:
            vanity_code = guild.vanity_code
        
        if vanity_code is None:
            return None
        
        if guild is None:
            guild = create_partial_guild_from_id(guild_id)
        
        invite_data = await self.http.invite_get(vanity_code, {})
        return Invite._create_vanity(guild, invite_data)
    
    
    async def vanity_invite_edit(self, guild, vanity_code, *, reason=None):
        """
        Edits the given guild's vanity invite's code.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``
            The guild, what's invite will be edited.
        vanity_code : `str`
            The new code of the guild's vanity invite.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the guild's audit logs.
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as ``Guild`` nor as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If `vanity_code` was not given as `str`.
        """
        guild_id = get_guild_id(guild)
        
        if __debug__:
            if not isinstance(vanity_code, str):
                raise AssertionError(
                    f'`vanity_code` can be `str`, got {vanity_code.__class__.__name__}; {vanity_code!r}.'
                )
        
        await self.http.vanity_invite_edit(guild_id, {'code': vanity_code}, reason)
    
    
    async def invite_create(self, channel, *, max_age=0, max_uses=0, unique=True, temporary=False):
        """
        Creates an invite at the given channel with the given parameters.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``ChannelText``, ``ChannelVoice``, ``ChannelGroup``, ``ChannelStore``, ``ChannelDirectory``, `int`
            The channel of the created invite.
        max_age : `int` = `0`, Optional (Keyword only)
            After how much time (in seconds) will the invite expire. Defaults is never.
        max_uses : `int` = `0`, Optional (Keyword only)
            How much times can the invite be used. Defaults to unlimited.
        unique : `bool` = `True`, Optional (Keyword only)
            Whether the created invite should be unique.
        temporary : `bool` = `False`, Optional (Keyword only)
            Whether the invite should give only temporary membership.
        
        Returns
        -------
        invite : ``Invite``
        
        Raises
        ------
        TypeError
            If `channel` was not given neither as ``ChannelText``, ``ChannelVoice``, ``ChannelGroup``,
                ``ChannelStore``, ``ChannelDirectory``, neither as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `max_age` was not given as `int`.
            - If `max_uses` was not given as `int`.
            - If `unique` was not given as `bool`.
            - If `temporary` was not given as `bool`.
        """
        if isinstance(channel, (ChannelText, ChannelVoice, ChannelGroup, ChannelStore, ChannelStore)):
            channel_id = channel.id
        else:
            channel_id = maybe_snowflake(channel)
            if channel_id is None:
                raise TypeError(
                    f'`channel` can be `{ChannelText.__name__}`, `{ChannelVoice.__name__}`, '
                    f'`{ChannelGroup.__name__}`, `{ChannelStore.__name__}`, `{ChannelStore.__name__}`, `int`, got '
                    f'{channel.__class__.__name__}; {channel!r}.')
        
        if __debug__:
            if not isinstance(max_age, int):
                raise AssertionError(
                    f'`max_age` can be `int`, got {max_age.__class__.__name__}; {max_age!r}.'
                )
            
            if not isinstance(max_uses, int):
                raise AssertionError(
                    f'`max_uses` can be `int`, got {max_uses.__class__.__name__}; {max_uses!r}.'
                )
            
            if not isinstance(unique, bool):
                raise AssertionError(
                    f'`unique` can be `bool`, got {unique.__class__.__name__}; {unique!r}.'
                )
            
            if not isinstance(temporary, bool):
                raise AssertionError(
                    f'`temporary` can be `bool`, got {temporary.__class__.__name__}; {temporary!r}.'
                )
        
        data = {
            'max_age': max_age,
            'max_uses': max_uses,
            'temporary': temporary,
            'unique': unique,
        }
        
        data = await self.http.invite_create(channel_id, data)
        return Invite(data, False)
    
    # 'target_user_id' :
    #     DiscordException BAD REQUEST (400), code=50035: Invalid Form Body
    #     target_user_type.GUILD_INVITE_INVALID_TARGET_USER_TYPE('Invalid target user type')
    # 'target_type', as 0:
    #     DiscordException BAD REQUEST (400), code=50035: Invalid Form Body
    #     target_user_type.BASE_TYPE_CHOICES('Value must be one of (1,).')
    # 'target_type', as 1:
    #     DiscordException BAD REQUEST (400), code=50035: Invalid Form Body
    #     target_user_type.GUILD_INVITE_INVALID_TARGET_USER_TYPE('Invalid target user type')
    # 'target_user_id' and 'target_user_type' together:
    #     DiscordException BAD REQUEST (400), code=50035: Invalid Form Body
    #     target_user_id.GUILD_INVITE_INVALID_STREAMER('The specified user is currently not streaming in this channel')
    # 'target_user_id' and 'target_user_type' with not correct channel:
    #     DiscordException BAD REQUEST (400), code=50035: Invalid Form Body
    #     target_user_id.GUILD_INVITE_INVALID_STREAMER('The specified user is currently not streaming in this channel')
    
    async def stream_invite_create(self, guild, user, *, max_age=0, max_uses=0, unique=True, temporary=False):
        """
        Creates an STREAM invite at the given guild for the specific user. The user must be streaming at the guild,
        when the invite is created.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``
            The guild where the user streams.
        user : ```ClientUserBase``, `int`
            The streaming user.
        max_age : `int` = `0`, Optional (Keyword only)
            After how much time (in seconds) will the invite expire. Defaults is never.
        max_uses : `int` = `0`, Optional (Keyword only)
            How much times can the invite be used. Defaults to unlimited.
        unique : `bool` = `True`, Optional (Keyword only)
            Whether the created invite should be unique.
        temporary : `bool` = `False`, Optional (Keyword only)
            Whether the invite should give only temporary membership.
        
        Returns
        -------
        invite : ``Invite``
        
        Raises
        ------
        TypeError
            If `user` was not given neither as ``ClientUserBase`` neither as `int`.
        ValueError
            If the user is not streaming at the guild.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `guild` was not given as ``Guild``.
            - If `max_age` was not given as `int`.
            - If `max_uses` was not given as `int`.
            - If `unique` was not given as `bool`.
            - If `temporary` was not given as `bool`.
        """
        if __debug__:
            if not isinstance(guild, Guild):
                raise AssertionError(
                    f'`guild` can be `{Guild.__name__}`, got {guild.__class__.__name__}; {guild!r}.'
                )
        
        if isinstance(user, ClientUserBase):
            user_id = user.id
        else:
            user_id = maybe_snowflake(user)
            if user_id is None:
                raise TypeError(
                    f'`user` can be `{ClientUserBase.__name__}`, `int`, got {user.__class__.__name__}; {user!r}.'
                )
        
        try:
            voice_state = guild.voice_states[user_id]
        except KeyError:
            raise ValueError(
                f'The user must stream at a voice channel of the guild. Got user={user!r}; guild={guild!r}.'
            ) from None
        
        if not voice_state.self_stream:
            raise ValueError(
                f'The user must stream at a voice channel of the guild. Got user={user!r}; guild={guild!r}.'
            )
        
        if __debug__:
            if not isinstance(max_age, int):
                raise AssertionError(
                    f'`max_age` can be `int`, got {max_age.__class__.__name__}; {max_age!r}.'
                )
            
            if not isinstance(max_uses, int):
                raise AssertionError(
                    f'`max_uses` can be `int`, got {max_uses.__class__.__name__}; {max_uses!r}.'
                )
            
            if not isinstance(unique, bool):
                raise AssertionError(
                    f'`unique` can be `bool`, got {unique.__class__.__name__}; {unique!r}.'
                )
            
            if not isinstance(temporary, bool):
                raise AssertionError(
                    f'`temporary` can be `bool`, got {temporary.__class__.__name__}; {temporary!r}.'
                )
        
        data = {
            'max_age': max_age,
            'max_uses': max_uses,
            'temporary': temporary,
            'unique': unique,
            'target_user_id': user_id,
            'target_type': InviteTargetType.stream.value,
        }
        
        data = await self.http.invite_create(voice_state.channel.id, data)
        return Invite(data, False)
    
    # Could not find correct application:
    #    DiscordException Bad Request (400), code=50035: Invalid Form Body
    #    target_application_id.GUILD_INVITE_INVALID_APPLICATION('The specified application is not embedded')
    
    async def application_invite_create(self, channel, application, *, max_age=0, max_uses=0, unique=True,
            temporary=False):
        """
        Creates an EMBEDDED_APPLICATION invite to the specified voice channel. The application must have must have
        `embedded` flag.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``ChannelText``, ``ChannelVoice``, ``ChannelGroup``, ``ChannelStore``,
                ``ChannelDirectory``, `int
            The target channel of the invite.
        application : ``Application``, `int`
            The embedded application to open in the voice channel.
            
            > The application must have `EMBEDDED_APPLICATION` flag.
        max_age : `int` = `0`, Optional (Keyword only)
            After how much time (in seconds) will the invite expire. Defaults is never.
        max_uses : `int` = `0`, Optional (Keyword only)
            How much times can the invite be used. Defaults to unlimited.
        unique : `bool` = `True`, Optional (Keyword only)
            Whether the created invite should be unique.
        temporary : `bool` = `False`, Optional (Keyword only)
            Whether the invite should give only temporary membership.
        
        Returns
        -------
        invite : ``Invite``
        
        Raises
        ------
        TypeError
            - If `channel` was not given neither as ``ChannelText``, ``ChannelVoice``, ``ChannelGroup``,
                ``ChannelStore``, ``ChannelDirectory``, neither as `int`.
            - If `application` was not given neither as ``Application`` nor as`int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `guild` was not given as ``Guild``.
            - If `max_age` was not given as `int`.
            - If `max_uses` was not given as `int`.
            - If `unique` was not given as `bool`.
            - If `temporary` was not given as `bool`.
        """
        if isinstance(channel, ChannelVoice):
            channel_id = channel.id
        else:
            channel_id = maybe_snowflake(channel)
            if channel_id is None:
                raise TypeError(
                    f'`channel` can be `{ChannelVoice.__name__}`, `int`, got '
                    f'{channel.__class__.__name__}; {channel!r}.'
                )
        
        if isinstance(application, Application):
            application_id = application.id
        else:
            application_id = maybe_snowflake(application)
            if application_id is None:
                raise TypeError(
                    f'`application` can be `{Application.__name__}`, `int`, got '
                    f'{application.__class__.__name__}; {application!r}.'
                )
        
        if __debug__:
            if not isinstance(max_age, int):
                raise AssertionError(
                    f'`max_age` can be `int`, got {max_age.__class__.__name__}; {max_age!r}.'
                )
            
            if not isinstance(max_uses, int):
                raise AssertionError(
                    f'`max_uses` can be `int`, got {max_uses.__class__.__name__}; {max_uses!r}.'
                )
            
            if not isinstance(unique, bool):
                raise AssertionError(
                    f'`unique` can be `bool`, got {unique.__class__.__name__}; {unique!r}.'
                )
            
            if not isinstance(temporary, bool):
                raise AssertionError(
                    f'`temporary` can be `bool`, got {temporary.__class__.__name__}; {temporary!r}.'
                )
        
        data = {
            'max_age': max_age,
            'max_uses': max_uses,
            'temporary': temporary,
            'unique': unique,
            'target_application_id': application_id,
            'target_type': InviteTargetType.embedded_application.value,
        }
        
        data = await self.http.invite_create(channel_id, data)
        return Invite(data, False)
    
    
    async def invite_create_preferred(self, guild, **kwargs):
        """
        Creates an invite to the guild's preferred channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild . ``Guild``
            The guild to her the invite will be created to.
        **kwargs : Keyword parameters
            Additional keyword parameters to describe the created invite.
        
        Other Parameters
        ----------------
        max_age : `int` = `0`, Optional (Keyword only)
            After how much time (in seconds) will the invite expire. Defaults is never.
        max_uses : `int` = `0`, Optional (Keyword only)
            How much times can the invite be used. Defaults to unlimited.
        unique : `bool` = `True`, Optional (Keyword only)
            Whether the created invite should be unique.
        temporary : `bool` = `False`, Optional (Keyword only)
            Whether the invite should give only temporary membership.
        
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
            If any exception was received from the Discord API.
        AssertionError
            - If `guild` was not given as ``Guild``.
            - If `max_age` was not given as `int`.
            - If `max_uses` was not given as `int`.
            - If `unique` was not given as `bool`.
            - If `temporary` was not given as `bool`.
        """
        if __debug__:
            if not isinstance(guild, Guild):
                raise AssertionError(
                    f'`guild` can be `{Guild.__name__}`, got {guild.__class__.__name__}; {guild!r}.'
                )
        
        while True:
            if not guild.channels:
                raise ValueError(
                    f'The guild has no channels (yet?), try waiting for dispatch or create a channel. '
                    f'Got guild={guild!r}.'
                )

            channel = guild.system_channel
            if channel is not None:
                break
            
            channel = guild.widget_channel
            if channel is not None:
                break
            
            for channel_type in (CHANNEL_TYPES.guild_text, CHANNEL_TYPES.guild_voice):
                for channel in guild.channels.values():
                    if channel.type == CHANNEL_TYPES.guild_category:
                        for channel in channel.channels:
                            if channel.type == channel_type:
                                break
                    if channel.type == channel_type:
                        break
                if channel.type == channel_type:
                    break
            else:
                raise ValueError(
                    f'The guild has only category channels and cannot create invite from them. '
                    f'Got guild={guild!r}.'
                )
            break
        
        # Check permission, because it can save a lot of time >.>
        if not channel.cached_permissions_for(self) & PERMISSION_MASK_CREATE_INSTANT_INVITE:
            return None
        
        try:
            return (await self.invite_create(channel, **kwargs))
        except DiscordException as err:
            if err.code in (
                ERROR_CODES.unknown_channel, # the channel was deleted meanwhile
                ERROR_CODES.missing_permissions, # permissions changed meanwhile
                ERROR_CODES.missing_access, # client removed
            ):
                return None
            raise
    
    
    async def invite_get(self, invite, *, with_count=True):
        """
        Requests a partial invite with the given code.
        
        This method is a coroutine.
        
        Parameters
        ----------
        invite : ``Invite``, `str`
            The invites code.
        with_count : `bool` = `True`, Optional (Keyword only)
            Whether the invite should contain the respective guild's user and online user count.
        
        Returns
        -------
        invite : ``Invite``
        
        Raises
        ------
        TypeError
            If `invite` was not given neither ``Invite`` nor `str`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If `invite_code` was not given as `str`.
            If `with_count`was not given as `bool`.
        """
        if isinstance(invite, Invite):
            invite_code = invite.code
        elif isinstance(invite, str):
            invite_code = invite
            invite = None
        else:
            raise TypeError(
                f'`invite`` can be `{Invite.__name__}`, `str`, got {invite.__class__.__name__}; '
                f'{invite!r}.'
            )
        
        if __debug__:
            if not isinstance(with_count, bool):
                raise AssertionError(
                    f'`with_count` can be `bool`, got {with_count.__class__.__name__}; '
                    f'{with_count!r}.'
                )
        
        invite_data = await self.http.invite_get(invite_code, {'with_counts': with_count})
        
        if invite is None:
            invite = Invite(invite_data, False)
        else:
            if invite.partial:
                updater = Invite._update_attributes
            else:
                updater = Invite._update_counts_only
            
            updater(invite, invite_data)
        
        return invite
    
    
    async def invite_get_all_guild(self, guild):
        """
        Gets the invites of the given guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, what's invites will be requested.
        
        Returns
        -------
        invites : `list` of ``Invite`` objects
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as ``Guild`` nor as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id = get_guild_id(guild)
        
        invite_datas = await self.http.invite_get_all_guild(guild_id)
        return [Invite(invite_data, False) for invite_data in invite_datas]
    
    
    async def invite_get_all_channel(self, channel):
        """
        Gets the invites of the given channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``ChannelText``, ``ChannelVoice``, ``ChannelGroup``, ``ChannelStore``, ``ChannelDirectory``, `int`
            The channel, what's invites will be requested.
        
        Returns
        -------
        invites : `list` of ``Invite`` objects
        
        Raises
        ------
        TypeError
            If `channel` was not given neither as ``ChannelText``, ``ChannelVoice``, ``ChannelGroup``,
            ``ChannelStore``, ``ChannelDirectory``, neither as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        if isinstance(channel, (ChannelText, ChannelVoice, ChannelGroup, ChannelStore, ChannelDirectory)):
            channel_id = channel.id
        else:
            channel_id = maybe_snowflake(channel)
            if channel_id is None:
                raise TypeError(
                    f'`channel` can be `{ChannelText.__name__}`, `{ChannelVoice.__name__}`, '
                    f'`{ChannelGroup.__name__}`, `{ChannelStore.__name__}`, `{ChannelDirectory.__name__}`, `int`, got '
                    f'{channel.__class__.__name__}; {channel!r}.'
                )
        
        invite_datas = await self.http.invite_get_all_channel(channel_id)
        return [Invite(invite_data, False) for invite_data in invite_datas]
    
    
    async def invite_delete(self, invite, *, reason=None):
        """
        Deletes the given invite.
        
        This method is a coroutine.
        
        Parameters
        ----------
        invite : ``Invite``
            The invite to delete.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        TypeError
            If `invite` was not given neither ``Invite`` nor `str`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        if isinstance(invite, Invite):
            invite_code = invite.code
        elif isinstance(invite, str):
            invite_code = invite
            invite = None
        else:
            raise TypeError(
                f'`invite`` can be `{Invite.__name__}`, `str`, got {invite.__class__.__name__}; {invite!r}.'
            )
        
        invite_data = await self.http.invite_delete(invite_code, reason)
        
        if invite is None:
            invite = Invite(invite_data, False)
        else:
            invite._update_attributes(invite_data)
        
        return invite
    
    # Role management
    
    async def role_edit(self, role, *, name=..., color=..., separated=..., mentionable=..., permissions=...,
            position=..., icon=..., reason=None):
        """
        Edits the role with the given parameters.
        
        This method is a coroutine.
        
        Parameters
        ----------
        role : ``Role``, `tuple` (`int`, `int`)
            The role to edit.
        name : `str`, Optional (Keyword only)
            The role's new name. It's length ca be in range [2:32].
        color : ``Color``, `int`, Optional (Keyword only)
            The role's new color.
        separated : `bool`, Optional (Keyword only)
            Whether the users with this role should be shown up as separated from the others.
        mentionable : `bool`, Optional (Keyword only)
            Whether the role should be mentionable.
        permissions : ``Permission``, `int`, Optional (Keyword only)
            The new permission value of the role.
        position : `int`, Optional (Keyword only)
            The role's new position.
        icon : `None`, ``Emoji``, `bytes-like`, Optional (Keyword only)
            The new icon of the role. Can be `'jpg'`, `'png'`, `'webp'`, `'gif'` image's raw data.
            
            Pass it as an ``Emoji`` to set role's icon to it.
            
            Pass it as `None` to remove the role's current icon.
        
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        TypeError
            - If `role` was not given neither as ``Role`` nor as `tuple` of (`int`, `int`).
            - If `icon` is neither `None`, `bytes-like`.
        ValueError
            - If default role would be moved.
            - If any role would be moved to position `0`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `name` was not given neither as `None` nor `str`.
            - If `name` length is out of range [2:32].
            - If `color` was not given as `None`, ``Color`` nor as other `int`.
            - If `separated` was not given as `None`, nor as `bool`.
            - If `mentionable` was not given as `None`, nor as `bool˛`.
            - If `permissions` was not given as `None`, ``Permission``, neither as other `int`.
            - If `icon` was passed as `bytes-like`, but it's format is not any of the expected formats.
        """
        snowflake_pair = get_guild_id_and_role_id(role)
        if snowflake_pair is None:
            raise TypeError(
                f'`role` can be `{Role.__name__}`, `tuple` (`int`, `int`), got '
                f'{role.__class__.__name__}; {role!r}.'
            )
        
        guild_id, role_id = snowflake_pair
        
        if (position is not None):
            await self.role_move((guild_id, role_id), position, reason=reason)
        
        data = {}
        
        if (name is not ...):
            if __debug__:
                if not isinstance(name, str):
                    raise AssertionError(
                        f'`name` can be `None`, `str`, got {name.__class__.__name__}; {name!r}.'
                    )
                
                name_length = len(name)
                if name_length < 2 or name_length > 32:
                    raise AssertionError(
                        f'`name` length can be in range [2:32], got {name_length!r}; {name!r}.'
                    )
            
            data['name'] = name
        
        if (color is not ...):
            if __debug__:
                if not isinstance(color, int):
                    raise AssertionError(
                        f'`color` can be `None`, `{Color.__name__}`, `int`, got {color.__class__.__name__}.'
                    )
            
            data['color'] = color
        
        if (separated is not ...):
            if __debug__:
                if not isinstance(separated, bool):
                    raise AssertionError(
                        f'`separated` can be `None`, `bool`, got {separated.__class__.__name__}; {separated!r}.'
                    )
            
            data['hoist'] = separated
        
        if (mentionable is not ...):
            if __debug__:
                if not isinstance(mentionable, bool):
                    raise AssertionError(
                        f'`mentionable` can be `None`, `bool`, got {mentionable.__class__.__name__}.'
                    )
            
            data['mentionable'] = mentionable
        
        if (permissions is not ...):
            if __debug__:
                if not isinstance(permissions, int):
                    raise AssertionError(
                        f'`permissions` can be `None`, `{Permission.__name__}`, `int`, got '
                        f'{permissions.__class__.__name__}; {permissions!r}.'
                    )
            
            data['permissions'] = permissions
        
        if (icon is not ...):
            if icon is None:
                data['icon'] = None
            
            elif isinstance(icon, Emoji):
                if icon.is_unicode_emoji():
                    data['unicode_emoji'] = icon.unicode
                elif icon.is_custom_emoji():
                    async with self.http.get(icon.url) as response:
                        icon = await response.read()
                    
                    data['icon'] = image_to_base64(icon)
                
                # no more cases
            
            elif isinstance(icon, (bytes, bytearray, memoryview)):
                if __debug__:
                    media_type = get_image_media_type(icon)
                    
                    if media_type not in VALID_ICON_MEDIA_TYPES_EXTENDED:
                        raise AssertionError(
                            f'Invalid `icon` type for the role: {media_type}; got {reprlib.repr(icon)}.'
                        )
                
                data['icon'] = image_to_base64(icon)
            
            else:
                raise TypeError(
                    f'`icon` can be `None`, `{Emoji.__name__}`, `bytes-like`, got '
                    f'{icon.__class__.__name__}; {reprlib.repr(icon)}.'
                )
        
        
        if data:
            await self.http.role_edit(guild_id, role_id, data, reason)
    
    
    async def role_delete(self, role, *, reason=None):
        """
        Deletes the given role.
        
        This method is a coroutine.
        
        Parameters
        ----------
        role : ``Role``, `tuple` (`int`, `int`)
            The role to delete
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        TypeError
            If `role` was not given neither as ``Role`` nor as `tuple` of (`int`, `int`).
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        snowflake_pair = get_guild_id_and_role_id(role)
        if snowflake_pair is None:
            raise TypeError(
                f'`role` can be `{Role.__name__}`, `tuple` (`int`, `int`), got {role.__class__.__name__}; {role!r}.'
            )
        
        guild_id, role_id = snowflake_pair
        
        await self.http.role_delete(guild_id, role_id, reason)
    
    
    async def role_create(self, guild, *, name=None, permissions=None, color=None, separated=None, mentionable=None,
            icon=None, reason=None):
        """
        Creates a role at the given guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild where the role will be created.
        name : `None`, `str` = `None`, Optional (Keyword only)
            The created role's name. It's length can be in range [2:32].
        color : `None`, ``Color``, `int` = `None`, Optional (Keyword only)
            The created role's color.
        separated : `None`, `bool` = `None`, Optional (Keyword only)
            Whether the users with the created role should show up as separated from the others.
        mentionable : `None`, `bool` = `None`, Optional (Keyword only)
            Whether the created role should be mentionable.
        permissions : `None`, ``Permission``, `int` = `None`, Optional (Keyword only)
            The permission value of the created role.
        icon : `None`, ``Emoji``, `bytes-like` = `None`, Optional (Keyword only)
            The icon for the role.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the guild's audit logs.
        
        Raises
        ------
        TypeError
            - If `guild` was not given neither as ``Guild`` nor as `int`.
            - If `icon` is neither `None`, ``Emoji``,  or `bytes-like`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `name` was not given neither as `None` nor `str`.
            - If `name` length is out of range [2:32].
            - If `color` was not given as `None`, ``Color`` nor as other `int`.
            - If `separated` was not given as `None`, nor as `bool`.
            - If `mentionable` was not given as `None`, nor as `bool˛`.
            - If `permissions` was not given as `None`, ``Permission``, neither as other `int`.
            - If `icon` is passed as `bytes-like`, but it's format is not a valid image format.
        """
        guild, guild_id = get_guild_and_id(guild)
        
        data = {}
        
        if (name is not None):
            if __debug__:
                if not isinstance(name, str):
                    raise AssertionError(
                        f'`name` can be `None`, `str`, got {name.__class__.__name__}; {name!r}.'
                    )
                
                name_length = len(name)
                if name_length < 2 or name_length > 32:
                    raise AssertionError(
                        f'`name` length can be in range [2:32], got {name_length!r}; {name!r}.'
                    )
            
            data['name'] = name
        
        if (permissions is not None):
            if __debug__:
                if not isinstance(color, int):
                    raise AssertionError(
                        f'`permissions` can be `None`, `{Permission.__name__}`, `int`, got '
                        f'{permissions.__class__.__name__}; {permissions!r}.'
                    )
            
            data['permissions'] = permissions
        
        if (color is not None):
            if __debug__:
                if not isinstance(color, int):
                    raise AssertionError(
                        f'`color` can be `None`, `{Color.__name__}`, `int`, got {color.__class__.__name__}; {color!r}.'
                    )
            
            data['color'] = color
        
        if (separated is not None):
            if __debug__:
                if not isinstance(separated, bool):
                    raise AssertionError(
                        f'`separated` can be `None`, `bool`, got {separated.__class__.__name__}; {separated!r}.'
                    )
            
            data['hoist'] = separated
        
        if (mentionable is not None):
            if __debug__:
                if not isinstance(mentionable, bool):
                    raise AssertionError(
                        f'`mentionable` can be `None`, `bool`, got {mentionable.__class__.__name__}; {mentionable!r}.'
                    )
            
            data['mentionable'] = mentionable
        
        if icon is None:
            pass
        
        elif isinstance(icon, Emoji):
            if icon.is_unicode_emoji():
                data['unicode_emoji'] = icon.unicode
            
            elif icon.is_custom_emoji():
                async with self.http.get(icon.url) as response:
                    icon = await response.read()
                
                data['icon'] = image_to_base64(icon)
            
            # no more cases
        
        elif not isinstance(icon, (bytes, bytearray, memoryview)):
            if __debug__:
                media_type = get_image_media_type(icon)
                
                if media_type not in VALID_ICON_MEDIA_TYPES_EXTENDED:
                    raise AssertionError(
                        f'Invalid `icon` type for the role: {media_type}; got {reprlib.repr(icon)}.'
                    )
            
            data['icon'] = image_to_base64(icon)
        
        else:
            raise TypeError(
                f'`icon` can be `None`, `{Emoji.__name__}`, `bytes-like`, got '
                f'{icon.__class__.__name__}; {reprlib.repr(icon)}.'
            )
        
        
        data = await self.http.role_create(guild_id, data, reason)
        
        if guild is None:
            guild = create_partial_guild_from_id(guild_id)
        
        return Role(data, guild)
    
    
    async def role_move(self, role, position, *, reason=None):
        """
        Moves the given role.
        
        This method is a coroutine.
        
        Parameters
        ----------
        role : ``Role``, `tuple` of (`int`, `int`)
            The role to move.
        position : `int`
            The position to move the given role.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        TypeError
            If `role` was not given neither as ``Role`` nor as `tuple` of (`int`, `int`).
        ValueError
            - If default role would be moved.
            - If any role would be moved to position `0`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        if isinstance(role, Role):
            guild_id = role.guild_id
        else:
            snowflake_pair = maybe_snowflake_pair(role)
            if snowflake_pair is None:
                raise TypeError(
                    f'`role` can be `{Role.__name__}`, `tuple` (`int`, `int`), got '
                    f'{role.__class__.__name__}; {role!r}.'
                )
            
            guild_id, role_id = snowflake_pair
            role = None
        
        guild = GUILDS.get(guild_id, None)
        if (guild is None) or guild.partial:
            guild = await self.guild_sync(guild_id)
        
        if role is None:
            try:
                role = ROLES[role_id]
            except KeyError:
                # Noice
                return
        
        # Is there nothing to move?
        if role.position == position:
            return
        
        # Default role cannot be moved to position not 0
        if role.position == 0:
            if position != 0:
                raise ValueError(
                    f'Default role cannot be moved, got {role!r}.'
                )
        # non default role cannot be moved to position 0
        else:
            if position == 0:
                raise ValueError(
                    f'Role cannot be moved to position `0`, got {role!r}.'
                )
        
        data = change_on_switch(guild.role_list, role, position, key=role_move_key)
        if not data:
            return
        
        await self.http.role_move(guild_id, data, reason)
    
    
    async def _role_reorder_roles_element_validator(self, item):
        """
        Validates a role-position pair.
        
        This method is a coroutine.
        
        Parameters
        ----------
        item : `tuple` (``Role`` or (`tuple` (`int, `int`), `int`) items or `Any`
            A `dict`, `list`, `set`, `tuple`, which contains role-position items.
        
        Returns
        -------
        role : ``Role``
            The validated role.
        guild : ``None`, ``Guild``
            The role's guild.
        
        Yields
        ------
        item : `None`, `tuple` (``Role``, ``Guild``, `int`)
        
        Raises
        ------
        TypeError
            If `item` has invalid format.
        """
        if not isinstance(item, tuple):
            raise TypeError(
                f'`roles` item can be `tuple`, got {item.__class__.__name__}; {item!r}.'
            )
        
        item_length = len(item)
        if item_length != 2:
            raise TypeError(
                f'`roles` item length can be `2`, got {item_length!r}; {item!r}.'
            )
        
        role, position = item
        if isinstance(role, Role):
            guild_id = role.guild_id
        
        else:
            snowflake_pair = maybe_snowflake_pair(role)
            if snowflake_pair is None:
                raise TypeError(
                    f'`roles` item[0] can be `{Role.__name__}`, `tuple` (`int`, `int`), got '
                    f'{role.__class__.__name__}; {role!r}.'
                )
            
            guild_id, role_id = snowflake_pair
            role = None
        
        guild = GUILDS.get(guild_id, None)
        if (guild is None) or guild.partial:
            guild = await self.guild_sync(guild_id)
        
        if role is None:
            role = ROLES.get(role_id, None)
        
        if not isinstance(position, int):
            raise TypeError(
                f'`position` can be `int`, got {position.__class__.__name__}; {position!r}.'
            )
        
        return role, guild, position
    
    
    async def _role_reorder_roles_validator(self, roles):
        """
        Validates `roles` parameter of ``.role_reorder``.
        
        This method is an asynchronous generator.
        
        Parameters
        ----------
        `roles`: (`dict` like or `iterable`) of `tuple` (``Role`` or (`tuple` (`int, `int`), `int`) items
            A `dict`, `list`, `set`, `tuple`, which contains role-position items.
        
        Yields
        ------
        item : `None`, `tuple` (``Role``, ``Guild``, `int`)
        
        Raises
        ------
        TypeError
            If `roles`'s format is not any of the expected ones.
        """
        if isinstance(roles, dict):
            for item in roles.items():
                yield await self._role_reorder_roles_element_validator(item)
        elif isinstance(roles, (list, set, tuple)):
            for item in roles:
                yield await self._role_reorder_roles_element_validator(item)
        else:
            raise TypeError(
                f'`roles` can be `dict-like` with (`{Role.__name__}, `int`) items, or as other '
                f'iterable with (`{Role.__name__}, `int`) elements, got {roles!r}.'
            )
    
    
    async def role_reorder(self, roles, *, reason=None):
        """
        Moves more roles at their guild to the specific positions.
        
        Partial roles are ignored and if passed any, every role's position after it is reduced. If there are roles
        passed with different guilds, then `ValueError` will be raised. If there are roles passed with the same
        position, then their positions will be sorted out.
        
        This method is a coroutine.
        
        Parameters
        ----------
        roles : (`dict` like or `iterable`) of `tuple` (``Role`` or (`tuple` (`int, `int`), `int`) items
            A `dict`, `list`, `set`, `tuple`, which contains role-position items.
        reason : `None`, `str` = `None`, Optional (Keyword only)
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
            If any exception was received from the Discord API.
        """
        # Lets check `roles` structure
        roles_valid = []
        
        guild = None
        
        # Is `roles` passed as dict-like?
        async for element in self._role_reorder_roles_validator(roles):
            if element is None:
                continue
            
            role, maybe_guild, position = element
            if maybe_guild is None:
                pass
            if guild is None:
                guild = maybe_guild
            else:
                if guild is not maybe_guild:
                    raise ValueError(
                        f'`roles` are from multiple guilds, got {roles!r}; guild_1={guild!r}; '
                        f'guild_2={guild!r}.'
                    )
            
            roles_valid.append((role, position))
        
        # Nothing to move, nice
        if not roles_valid:
            return
        
        # Check default and moving to default position
        index = 0
        limit = len(roles_valid)
        while True:
            if index == limit:
                break
            
            role, position = roles_valid[index]
            # Default role cannot be moved
            if (role is not None) and (role.position == 0):
                if position != 0:
                    raise ValueError(
                        f'Default role cannot be moved, got {role!r}; roles={roles!r}.'
                    )
                
                # default and moving to default, lets delete it
                del roles_valid[index]
                limit -= 1
                continue
                
            else:
                # Role cannot be moved to default position
                if position == 0:
                    raise ValueError(
                        f'Role cannot be moved to position `0`, got {role!r}; roles={roles!r}.'
                    )
            
            index += 1
            continue
        
        if not limit:
            return
        
        # Check dupe roles
        roles = set()
        ln = 0
        
        for role, position in roles_valid:
            if role is None:
                continue
            
            roles.add(role)
            if len(roles) == ln:
                raise ValueError(
                    f'`{Role.__name__}`: {role!r} is duped, got {roles!r}.'
                )
            
            ln += 1
            continue
        
        # Now that we have the roles, lets order them
        roles_valid.sort(key=role_reorder_valid_roles_sort_key)
        
        # Cut out non roles.
        limit = len(roles_valid)
        index = 0
        negate_position = 0
        while (index < limit):
            role, position = roles_valid[index]
            if role is None:
                del roles_valid[-1]
                limit -= 1
                negate_position += 1
            else:
                
                if negate_position:
                    roles_valid[index] = (role, position - negate_position)
                
                index += 1
        
        # Remove dupe indexes
        index = 0
        limit = len(roles_valid)
        last_position = 0
        increase_position = 0
        while (index < limit):
            role, position = roles_valid[index]
            if position == last_position:
                increase_position += 1
            
            if increase_position:
                roles_valid[index] = (role, position + increase_position)
            
            last_position = position
            index += 1
            continue
        
        
        # Lets cut out every other role from the guild's
        roles_leftover = set(guild.roles.values())
        for item in roles_valid:
            role = item[0]
            roles_leftover.remove(role)
        
        roles_leftover = sorted(roles_leftover)
    
        target_order = []
        
        index_valid = 0
        index_leftover = 0
        limit_valid = len(roles_valid)
        limit_leftover = len(roles_leftover)
        position_target = 0
        
        while True:
            if index_valid == limit_valid:
                while True:
                    if index_leftover == limit_leftover:
                        break
                    
                    role = roles_leftover[index_leftover]
                    index_leftover += 1
                    target_order.append(role)
                    continue
                
                break
            
            if index_leftover == limit_leftover:
                while True:
                    if index_valid == limit_valid:
                        break
                    
                    role = roles_valid[index_valid][0]
                    index_valid += 1
                    target_order.append(role)
                    continue
                
                
                break
            
            role, position = roles_valid[index_valid]
            if position == position_target:
                position_target += 1
                index_valid += 1
                target_order.append(role)
                continue
            
            role = roles_leftover[index_leftover]
            position_target = position_target + 1
            index_leftover = index_leftover + 1
            target_order.append(role)
            continue
        
        data = []
        
        for index, role in enumerate(target_order):
            position = role.position
            if index == position:
                continue
            
            data.append(role_move_key(role, index))
            continue
        
        # Nothing to move
        if not data:
            return
        
        await self.http.role_move(guild.id, data, reason)
    
    # Application Command & Interaction related
    
    async def application_command_global_get(self, application_command):
        """
        Requests the given global application command.
        
        Parameters
        ----------
        application_command : ``ApplicationCommand``, `int`
            The application command, or it's id to request.
        
        Returns
        -------
        application_commands : ``ApplicationCommand``
            The received application command.
        
        Raises
        ------
        TypeError
            If `application_command` was not given neither as ``ApplicationCommand`` not as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If the client's application is not yet synced.
        """
        application_id = self.application.id
        if __debug__:
            if application_id == 0:
                raise AssertionError(
                    'The client\'s application is not yet synced.'
                )
        
        if isinstance(application_command, ApplicationCommand):
            application_command_id = application_command.id
        else:
            application_command_id = maybe_snowflake(application_command)
            if application_command_id is None:
                raise TypeError(
                    f'`application_command` can be `{ApplicationCommand.__name__}`, `int`, got '
                    f'{application_command.__class__.__name__}; {application_command!r}.'
                )
            
            application_command = APPLICATION_COMMANDS.get(application_command_id, None)
        
        application_command_data = await self.http.application_command_global_get(application_id,
            application_command_id)
        
        if application_command is None:
            application_command = ApplicationCommand.from_data(application_command_data)
        else:
            application_command._update_attributes(application_command_data)
        
        return application_command
    
    
    async def application_command_global_get_all(self):
        """
        Requests the client's global application commands.
        
        This method is a coroutine.
        
        Returns
        -------
        application_commands : `list` of ``ApplicationCommand``
            The received application commands.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If the client's application is not yet synced.
        """
        application_id = self.application.id
        if __debug__:
            if application_id == 0:
                raise AssertionError(
                    'The client\'s application is not yet synced.'
                )
        
        data = await self.http.application_command_global_get_all(application_id)
        return [ApplicationCommand.from_data(application_command_data) for application_command_data in data]
    
    
    async def application_command_global_create(self, application_command):
        """
        Creates a new global application command.
        
        > If there is an application command with the given name, will overwrite that instead.
        >
        > Each day only maximum only 200 global application command can be created.
        
        This method is a coroutine.
        
        Parameters
        ----------
        application_command : ``ApplicationCommand``
            The application command to create.
        
        Returns
        -------
        application_command : ``ApplicationCommand``
            The created application command.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If the client's application is not yet synced.
            - If `application_command` was not given as ``ApplicationCommand``.
        
        Notes
        -----
        The command will be available in all guilds after 1 hour.
        """
        application_id = self.application.id
        if __debug__:
            if application_id == 0:
                raise AssertionError(
                    'The client\'s application is not yet synced.'
                )
        
        if __debug__:
            if not isinstance(application_command, ApplicationCommand):
                raise AssertionError(
                    f'`application_command` can be `{ApplicationCommand.__name__}`, got '
                    f'{application_command.__class__.__name__}; {application_command!r}.'
                )
        
        data = application_command.to_data()
        data = await self.http.application_command_global_create(application_id, data)
        return ApplicationCommand.from_data(data)
    
    
    async def application_command_global_edit(self, old_application_command, new_application_command):
        """
        Edits a global application command.
        
        This method is a coroutine.
        
        Parameters
        ----------
        old_application_command : ``ApplicationCommand``, `int`
            The application command to edit. Can be given as the application command's id as well.
        new_application_command : ``ApplicationCommand``
            The application command to edit to.
        
        Returns
        -------
        application_command : ``ApplicationCommand``
            The edited application command.
        
        Raises
        ------
        TypeError
            If `old_application_command` was not given neither as ``ApplicationCommand`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If the client's application is not yet synced.
            - If `new_application_command` was not given as ``ApplicationCommand``.
        
        Notes
        -----
        The updates will be available in all guilds after 1 hour.
        """
        if isinstance(old_application_command, ApplicationCommand):
            application_command_id = old_application_command.id
        else:
            application_command_id = maybe_snowflake(old_application_command)
            if application_command_id is None:
                raise TypeError(
                    f'`old_application_command` can be `{ApplicationCommand.__name__}`, `int`, got '
                    f'{old_application_command.__class__.__name__}; {old_application_command!r}.'
                )
            
            old_application_command = None
        
        application_id = self.application.id
        if __debug__:
            if application_id == 0:
                raise AssertionError(
                    'The client\'s application is not yet synced.'
                )
        
        if __debug__:
            if not isinstance(new_application_command, ApplicationCommand):
                raise AssertionError(
                    f'`new_application_command` can be `{ApplicationCommand.__name__}`, got '
                    f'{new_application_command.__class__.__name__}; {new_application_command!r}.'
                )
        
        data = new_application_command.to_data()
        
        # Handle https://github.com/discord/discord-api-docs/issues/2525
        if (old_application_command is not None) and (old_application_command.name == data['name']):
            del data['name']
        
        await self.http.application_command_global_edit(application_id, application_command_id, data)
        return ApplicationCommand._from_edit_data(data, application_command_id, application_id)
    
    
    async def application_command_global_delete(self, application_command):
        """
        Deletes the given application command.
        
        Parameters
        ----------
        application_command : ``ApplicationCommand``, `int`
            The application command delete edit. Can be given as the application command's id as well.
        
        Raises
        ------
        TypeError
            If `application_command` was not given neither as ``ApplicationCommand`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If the client's application is not yet synced.
        """
        application_id = self.application.id
        if __debug__:
            if application_id == 0:
                raise AssertionError(
                    'The client\'s application is not yet synced.'
                )
        
        if isinstance(application_command, ApplicationCommand):
            application_command_id = application_command.id
        else:
            application_command_id = maybe_snowflake(application_command)
            if application_command_id is None:
                raise TypeError(
                    f'`application_command` can be `{ApplicationCommand.__name__}`, `int`, got '
                    f'{application_command.__class__.__name__}; {application_command!r}.'
                )
        
        await self.http.application_command_global_delete(application_id, application_command_id)
    
    
    async def application_command_global_update_multiple(self, application_commands):
        """
        Takes an iterable of application commands, and updates the actual global ones.
        
        If a command exists with the given name, edits it, if not, will creates a new one.
        
        > The created application commands count to the daily limit.
        
        This method is a coroutine.
        
        Parameters
        ----------
        application_commands : `iterable` of ``ApplicationCommand``
            The application commands to update the existing ones with.
        
        Returns
        -------
        application_commands : `list` of ``ApplicationCommand``
            The edited and created application commands.
        
        Raises
        ------
        ValueError
            If more than `100` ``ApplicationCommand`` is given.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If the client's application is not yet synced.
            - If an application command was not given as ``ApplicationCommand``.
            - If `application_commands` is not iterable.
        
        Notes
        -----
        The commands will be available in all guilds after 1 hour.
        """
        application_id = self.application.id
        if __debug__:
            if application_id == 0:
                raise AssertionError('The client\'s application is not yet synced.')
        
        application_command_datas = []
        
        if __debug__:
            if getattr(type(application_commands), '__iter__', None) is None:
                raise AssertionError(
                    f'`application_commands` can be an `iterable`, got '
                    f'{application_commands.__class__.__name__}; {application_commands!r}.'
                )
        
        application_command_count = 0
        for application_command in application_commands:
            if __debug__:
                if not isinstance(application_command, ApplicationCommand):
                    raise AssertionError(
                        f'`application_commands` contains a not `{ApplicationCommand.__name__}` element, got: '
                        f'{application_command.__class__.__name__}; {application_command!r}; '
                        f'application_commands={application_commands!r}.'
                    )
            
            if application_command_count == APPLICATION_COMMAND_LIMIT_GLOBAL:
                raise ValueError(
                    f'Maximum {APPLICATION_COMMAND_LIMIT_GLOBAL} application command can be given, got '
                    f'{application_command_count!r}; {application_commands!r}.'
                )
            
            application_command_count += 1
            application_command_datas.append(application_command.to_data())
        
        if application_command_datas:
            application_command_datas = await self.http.application_command_global_update_multiple(application_id,
                application_command_datas)
            
            application_command_datas = [ApplicationCommand.from_data(application_command_data) \
                for application_command_data in application_command_datas]
        else:
            application_command_datas = []
        
        return application_command_datas
    
    
    async def application_command_guild_get(self, guild, application_command):
        """
        Requests the given guild application command.
        
        Parameters
        ----------
        application_command : ``ApplicationCommand``, `int`
            The application command, or it's id to request.
        
        Returns
        -------
        application_commands : ``ApplicationCommand``
            The received application command.
        
        Raises
        ------
        TypeError
            - If `guild` was not given neither as``Guild`` nor `int`.
            - If `application_command` was not given neither as ``ApplicationCommand`` not as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If the client's application is not yet synced.
        """
        application_id = self.application.id
        if __debug__:
            if application_id == 0:
                raise AssertionError(
                    'The client\'s application is not yet synced.'
                )
        
        guild_id = get_guild_id(guild)
        
        if isinstance(application_command, ApplicationCommand):
            application_command_id = application_command.id
        else:
            application_command_id = maybe_snowflake(application_command)
            if application_command_id is None:
                raise TypeError(
                    f'`application_command` can be `{ApplicationCommand.__name__}`, `int`, got '
                    f'{application_command.__class__.__name__}; {application_command!r}.'
                )
            
            application_command = APPLICATION_COMMANDS.get(application_command_id, None)
        
        application_command_data = await self.http.application_command_guild_get(application_id, guild_id,
            application_command_id)
        
        if application_command is None:
            application_command = ApplicationCommand.from_data(application_command_data)
        else:
            application_command._update_attributes(application_command_data)
        
        return application_command
    
    
    async def application_command_guild_get_all(self, guild):
        """
        Requests the client's global application commands.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, which application commands will be requested.
        
        Returns
        -------
        application_commands : `list` of ``ApplicationCommand``
            The received application commands.
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as``Guild`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If the client's application is not yet synced.
        """
        application_id = self.application.id
        if __debug__:
            if application_id == 0:
                raise AssertionError(
                    'The client\'s application is not yet synced.'
                )
        
        guild_id = get_guild_id(guild)
        
        data = await self.http.application_command_guild_get_all(application_id, guild_id)
        return [ApplicationCommand.from_data(application_command_data) for application_command_data in data]
    
    
    async def application_command_guild_create(self, guild, application_command):
        """
        Creates a new guild application command.
        
        > If there is an application command with the given name, will overwrite that instead.
        >
        > Each day only maximum only 200 guild application command can be created at each guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, where application commands will be created.
        application_command : ``ApplicationCommand``
            The application command to create.
        
        Returns
        -------
        application_command : ``ApplicationCommand``
            The created application command.
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as``Guild`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If the client's application is not yet synced.
            - If `application_command` was not given as ``ApplicationCommand``.
        """
        application_id = self.application.id
        if __debug__:
            if application_id == 0:
                raise AssertionError(
                    'The client\'s application is not yet synced.'
                )
        
        guild_id = get_guild_id(guild)
        
        if __debug__:
            if not isinstance(application_command, ApplicationCommand):
                raise AssertionError(
                    f'`application_command` can be `{ApplicationCommand.__name__}`, got '
                    f'{application_command.__class__.__name__}; {application_command!r}.'
                )
        
        data = application_command.to_data()
        data = await self.http.application_command_guild_create(application_id, guild_id, data)
        return ApplicationCommand.from_data(data)
    
    
    async def application_command_guild_edit(self, guild, old_application_command, new_application_command):
        """
        Edits a guild application command.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, to what the application command is bound to.
        old_application_command : ``ApplicationCommand``, `int`
            The application command to edit. Can be given as the application command's id as well.
        new_application_command : ``ApplicationCommand``
            The application command to edit to.
        
        Raises
        ------
        TypeError
            - If `guild` was not given neither as``Guild`` nor `int`.
            - If `old_application_command` was not given neither as ``ApplicationCommand`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If the client's application is not yet synced.
            - If `new_application_command` was not given as ``ApplicationCommand``.
        """
        if isinstance(old_application_command, ApplicationCommand):
            application_command_id = old_application_command.id
        else:
            application_command_id = maybe_snowflake(old_application_command)
            if application_command_id is None:
                raise TypeError(
                    f'`old_application_command` can be `{ApplicationCommand.__name__}`, `int`, got '
                    f'{old_application_command.__class__.__name__}; {old_application_command!r}.'
                )
            
            old_application_command = None
        
        application_id = self.application.id
        if __debug__:
            if application_id == 0:
                raise AssertionError(
                    'The client\'s application is not yet synced.'
                )
        
        guild_id = get_guild_id(guild)
        
        if __debug__:
            if not isinstance(new_application_command, ApplicationCommand):
                raise AssertionError(
                    f'`new_application_command` can be `{ApplicationCommand.__name__}`, got '
                    f'{new_application_command.__class__.__name__}; {new_application_command!r}.'
                )
        
        data = new_application_command.to_data()
        
        # Handle https://github.com/discord/discord-api-docs/issues/2525
        if (old_application_command is not None) and (old_application_command.name == data['name']):
            del data['name']
        
        await self.http.application_command_guild_edit(application_id, guild_id, application_command_id, data)
    
    
    async def application_command_guild_delete(self, guild, application_command):
        """
        Deletes the given application command.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, to what the application command is bound to.
        application_command : ``ApplicationCommand``, `int`
            The application command delete edit. Can be given as the application command's id as well.
        
        Raises
        ------
        TypeError
            - If `guild` was not given neither as``Guild`` nor `int`.
            - If `application_command` was not given neither as ``ApplicationCommand`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If the client's application is not yet synced.
        """
        application_id = self.application.id
        if __debug__:
            if application_id == 0:
                raise AssertionError(
                    'The client\'s application is not yet synced.'
                )
        
        guild_id = get_guild_id(guild)
        
        if isinstance(application_command, ApplicationCommand):
            application_command_id = application_command.id
        else:
            application_command_id = maybe_snowflake(application_command)
            if application_command_id is None:
                raise TypeError(
                    f'`application_command` can be `{ApplicationCommand.__name__}`, `int` , got '
                    f'{application_command.__class__.__name__}; {application_command!r}.'
                )
        
        await self.http.application_command_guild_delete(application_id, guild_id, application_command_id)
    
    
    async def application_command_guild_update_multiple(self, guild, application_commands):
        """
        Takes an iterable of application commands, and updates the guild's actual ones.
        
        If a command exists with the given name, edits it, if not, will creates a new one.
        
        > The created application commands count to the daily limit.
        
        This method is a coroutine.
        
        Parameters
        ----------
        application_commands : `iterable` of ``ApplicationCommand``
            The application commands to update the existing ones with.
        
        Returns
        -------
        application_commands : `list` of ``ApplicationCommand``
            The edited and created application commands.
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as``Guild`` nor `int`.
        ValueError
            If more than `100` ``ApplicationCommand`` is given.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If the client's application is not yet synced.
            - If an application command was not given as ``ApplicationCommand``.
            - If `application_commands` is not iterable.
        """
        application_id = self.application.id
        if __debug__:
            if application_id == 0:
                raise AssertionError(
                    'The client\'s application is not yet synced.'
                )
        
        guild_id = get_guild_id(guild)
        
        application_command_datas = []
        
        if __debug__:
            if getattr(type(application_commands), '__iter__', None) is None:
                raise AssertionError(
                    f'`application_commands` can be an `iterable`, got '
                    f'{application_commands.__class__.__name__}; {application_commands!r}.'
                )
        
        application_command_count = 0
        for application_command in application_commands:
            if __debug__:
                if not isinstance(application_command, ApplicationCommand):
                    raise AssertionError(
                        f'`application_commands` can contain `{ApplicationCommand.__name__}` elements, got: '
                        f'{application_command.__class__.__name__}; {application_command!r}; '
                        f'application_commands={application_commands!r}.'
                    )
            
            if application_command_count == APPLICATION_COMMAND_LIMIT_GUILD:
                raise ValueError(
                    f'Maximum {APPLICATION_COMMAND_LIMIT_GUILD} application command can be given, got '
                    f'{application_command_count!r}; {application_commands!r}.'
                )
            
            application_command_count += 1
            application_command_datas.append(application_command.to_data())
        
        if application_command_datas:
            application_command_datas = await self.http.application_command_guild_update_multiple(application_id,
                guild_id, application_command_datas)
            
            application_command_datas = [ApplicationCommand.from_data(application_command_data) \
                for application_command_data in application_command_datas]
        else:
            application_command_datas = []
        
        return application_command_datas
    
    
    async def application_command_permission_get(self, guild, application_command):
        """
        Returns the permissions set for the given `application_command` in the given `guild`.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The respective guild.
        application_command : ``ApplicationCommand``, `int`
            The respective application command.
        
        Returns
        -------
        permission : ``ApplicationCommandPermission``
            The requested permissions.
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as``Guild`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If the client's application is not yet synced.
            - If an application command was not given neither as ``ApplicationCommand``, `int`.
        
        Notes
        -----
        Íf the application command has no permission overwrites in the guild, Discord will drop the following error:
        
        ```py
        DiscordException Not Found (404), code=10066: Unknown application command permissions
        ```
        """
        application_id = self.application.id
        if __debug__:
            if application_id == 0:
                raise AssertionError(
                    'The client\'s application is not yet synced.'
                )
        
        guild_id = get_guild_id(guild)
        
        if isinstance(application_command, ApplicationCommand):
            application_command_id = application_command.id
        else:
            application_command_id = maybe_snowflake(application_command)
            if application_command_id is None:
                raise TypeError(
                    f'`application_command` can be `{ApplicationCommand.__name__}`, `int`, got '
                    f'{application_command.__class__.__name__}; {application_command!r}.'
                )
        
        permission_data = await self.http.application_command_permission_get(application_id, guild_id,
            application_command_id)
        
        return ApplicationCommandPermission.from_data(permission_data)
    
    
    async def application_command_permission_edit(self, guild, application_command, permission_overwrites):
        """
        Edits the permissions of the given `application_command` in the given `guild`.
        
        > The new permissions will permission overwrite the existing permission of an application command.
        >
        > A command will lose it's permissions on rename.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The respective guild.
        application_command : ``ApplicationCommand``, `int`
            The respective application command.
        permission_overwrites : `None`, (`tuple`, `list` of `set`) of ``ApplicationCommandPermissionOverwrite``
            The new permission overwrites of the given application command inside of the guild.
            
            Give it as `None` to remove all existing one.
        
        Returns
        -------
        permissions : ``ApplicationCommandPermission``
            The application command's new permissions.
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as``Guild`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If the client's application is not yet synced.
            - If an application command was not given neither as ``ApplicationCommand``, `int`.
            - If `permission_overwrites` was not given as `None`, `tuple`, `list`, `set`.
            - If `permission_overwrites` contains a non ``ApplicationCommandPermissionOverwrite`` element.
            - If `permission_overwrites` contains more than 10 elements.
        """
        application_id = self.application.id
        if __debug__:
            if application_id == 0:
                raise AssertionError(
                    'The client\'s application is not yet synced.'
                )
        
        guild_id = get_guild_id(guild)
        
        if isinstance(application_command, ApplicationCommand):
            application_command_id = application_command.id
        else:
            application_command_id = maybe_snowflake(application_command)
            if application_command_id is None:
                raise TypeError(
                    f'`application_command` can be `{ApplicationCommand.__name__}`, `int`, got '
                    f'{application_command.__class__.__name__}; {application_command!r}.'
                )
        
        permission_overwrite_datas = []
        if (permission_overwrites is not None):
            if __debug__:
                if not isinstance(permission_overwrites, (list, set, tuple)):
                    raise AssertionError(
                        f'`permission_overwrites` can be `None`, `list`, `tuple` or '
                        f'`set`, got {permission_overwrites.__class__.__name__}; {permission_overwrites!r}.'
                    )
            
            for permission_overwrite in permission_overwrites:
                if __debug__:
                    if not isinstance(permission_overwrite, ApplicationCommandPermissionOverwrite):
                        raise AssertionError(
                            f'`permission_overwrites` can contain `{ApplicationCommandPermissionOverwrite.__name__}` '
                            f'elements, got {permission_overwrite.__class__.__name__}; {permission_overwrite!r}; '
                            f'permission_overwrites={permission_overwrites!r}.'
                        )
                
                # We update channel permission overwrites with id of 0
                if (
                        permission_overwrite.target_type is ApplicationCommandPermissionOverwriteTargetType.channel and
                        permission_overwrite.target_id == 0
                ):
                    permission_overwrite.target_id = guild_id - 1
                
                permission_overwrite_datas.append(permission_overwrite.to_data())
            
            if __debug__:
                permission_overwrite_datas_length = len(permission_overwrite_datas)
                if permission_overwrite_datas_length > APPLICATION_COMMAND_PERMISSION_OVERWRITE_MAX:
                    raise AssertionError(
                        f'`permission_overwrites` can contain up to `{APPLICATION_COMMAND_PERMISSION_OVERWRITE_MAX}` '
                        f'permission_overwrites, got {permission_overwrite_datas_length!r}; '
                        f'{permission_overwrites!r}.'
                    )
        
        data = {'permissions': permission_overwrite_datas}
        permission_data = await self.http.application_command_permission_edit(application_id, guild_id,
            application_command_id, data)
        
        return ApplicationCommandPermission.from_data(permission_data)
    
    
    async def application_command_permission_get_all_guild(self, guild):
        """
        Returns the permissions set for application commands in the given `guild`.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild to request application command permissions from.
        
        Returns
        -------
        permission : `list` of ``ApplicationCommandPermission``
            The requested permissions for all the application commands in the guild.
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as``Guild`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If the client's application is not yet synced.
        """
        application_id = self.application.id
        if __debug__:
            if application_id == 0:
                raise AssertionError(
                    'The client\'s application is not yet synced.'
                )
        
        guild_id = get_guild_id(guild)
        
        permission_datas = await self.http.application_command_permission_get_all_guild(application_id, guild_id)
        
        return [ApplicationCommandPermission.from_data(permission_data) for permission_data in permission_datas]
    
    
    async def interaction_application_command_acknowledge(self, interaction, wait=True, *,
            show_for_invoking_user_only=False):
        """
        Acknowledges the given application command interaction.
        
        This method is a coroutine.
        
        Parameters
        ----------
        interaction : ``InteractionEvent``
            Interaction to acknowledge
        wait : `bool` = `True`, Optional
            Whether the interaction should be ensured asynchronously.
        show_for_invoking_user_only : `bool` = `False`, Optional (Keyword only)
            Whether the sent message should only be shown to the invoking user. Defaults to `False`.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If `interaction` was not given an ``InteractionEvent``.
        
        Notes
        -----
        If the interaction is already timed or out or was used, you will get:
        
        ```
        DiscordException Not Found (404), code=10062: Unknown interaction
        ```
        """
        if __debug__:
            if not isinstance(interaction, InteractionEvent):
                raise AssertionError(
                    f'`interaction` can be `{InteractionEvent.__name__}`, got '
                    f'{interaction.__class__.__name__}; {interaction!r}.'
                )
        
        # Do not ack twice
        if not interaction.is_unanswered():
            return
        
        data = {'type': INTERACTION_RESPONSE_TYPES.source}
        
        if show_for_invoking_user_only:
            data['data'] = {'flags': MESSAGE_FLAG_VALUE_INVOKING_USER_ONLY}
        
        context = InteractionResponseContext(interaction, True, show_for_invoking_user_only)
        coroutine = self.http.interaction_response_message_create(interaction.id, interaction.token, data)
        
        if wait:
            async with context:
                await coroutine
        else:
            await context.ensure(coroutine)
    
    
    async def interaction_application_command_autocomplete(self, interaction, choices):
        """
        Forwards auto completion choices for the user.
        
        This method is a coroutine.
        
        Parameters
        ----------
        interaction : ``InteractionEvent``
            Interaction to acknowledge
        choices : `None`, `iterable` of `str`
            Choices to show for the user.
        
        Raises
        ------
        TypeError
            If `choice` is neither `None` nor `iterable`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If `interaction` was not given an ``InteractionEvent``.
        
        Notes
        -----
        If the interaction is already timed or out or was used, you will get:
        
        ```
        DiscordException Not Found (404), code=10062: Unknown interaction
        ```
        """
        if __debug__:
            if not isinstance(interaction, InteractionEvent):
                raise AssertionError(
                    f'`interaction` can be `{InteractionEvent.__name__}`, got '
                    f'{interaction.__class__.__name__}; {interaction!r}.'
                )
        
        # Do not auto complete twice
        if not interaction.is_unanswered():
            return
        
        choices = application_command_autocomplete_choice_parser(choices)
        
        data = {
            'type': INTERACTION_RESPONSE_TYPES.application_command_autocomplete_result,
            'data': {
                'choices': choices,
            },
        }
        
        async with InteractionResponseContext(interaction, True, False):
            await self.http.interaction_response_message_create(interaction.id, interaction.token, data)
    
    
    async def interaction_form_send(self, interaction, form):
        """
        Responds on an interaction with a form.
        
        This function is a coroutine.
        
        Parameters
        ----------
        interaction : ``InteractionEvent``
            Interaction to respond to.
        form : ``InteractionForm``
            The to respond with.
        
        Raises
        ------
        RuntimeError
            If cannot respond with a form on the given `interaction`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `interaction` is not ``InteractionEvent``.
            - If `form` is not is not ``InteractionForm``.
        
        Notes
        -----
        Discord do not returns message data, so the method cannot return a ``Message`` either.
        
        If the interaction is already timed or out or was used, you will get:
        
        ```
        DiscordException Not Found (404), code=10062: Unknown interaction
        ```
        """
        if __debug__:
            if not isinstance(interaction, InteractionEvent):
                raise AssertionError(f'`interaction` can be `{InteractionEvent.__name__}`, got '
                    f'{interaction.__class__.__name__}; {interaction!r}.'
                )
        
        if not interaction.is_unanswered():
            warnings.warn(
                (
                    f'`{self.__class__.__name__}.interaction_response_form` called on an interaction already '
                    f'acknowledged /answered: {interaction!r}. Returning `None`.'
                ),
                ResourceWarning
            )
            
            return None
        
        if __debug__:
            if not isinstance(form, InteractionForm):
                raise AssertionError(f'`form` can be `{InteractionForm.__name__}`, got '
                    f'{form.__class__.__name__}.')
        
        if (
            (interaction.type is not InteractionType.application_command) and
            (interaction.type is not InteractionType.message_component)
        ):
            raise RuntimeError(
                f'Only `application_command` and `message_component` interactions can be answered with '
                f'form, got `{interaction.type.name}`; {interaction!r}; form={form!r}.'
            )
        
        # Build payload
        data = {
            'data': form.to_data(),
            'type': INTERACTION_RESPONSE_TYPES.form
        }
        
        async with InteractionResponseContext(interaction, False, True):
            await self.http.interaction_response_message_create(interaction.id, interaction.token, data)
        
        return None
    
    
    async def interaction_response_message_create(self, interaction, content=None, *, allowed_mentions=...,
            components=None, embed=None, show_for_invoking_user_only=False, suppress_embeds=False, tts=False):
        """
        Sends an interaction response. After receiving an ``InteractionEvent``, you should acknowledge it within
        `3` seconds to perform followup actions.
        
        Not like ``.message_create``, this endpoint can be called without any content to still acknowledge the
        interaction event. This method also wont return a ``Message`` object (thank to Discord), but at least
        ``.interaction_followup_message_create`` will. To edit or delete this message, you can use
        ``.interaction_response_message_edit`` and ``interaction_response_message_delete``.
        
        This method is a coroutine.
        
        Parameters
        ----------
        interaction : ``InteractionEvent``
            Interaction to respond to.
        
        content : `None`, `str`, ``EmbedBase``, `Any` = `None`, Optional
            The interaction response's content if given. If given as `str` or empty string, then no content will be
            sent, meanwhile if any other non `str`, ``EmbedBase`` is given, then will be casted to string.
            
            If given as ``EmbedBase``, then is sent as the message's embed.
        
        allowed_mentions : `None`, `str`, ``UserBase``, ``Role``, `list` of (`str`, ``UserBase``, ``Role`` )
                , Optional (Keyword only)
            Which user or role can the message ping (or everyone). Check ``parse_allowed_mentions`` for details.
        
        components : `None`, ``ComponentBase``, (`tuple`, `list`) of (``ComponentBase``, (`tuple`, `list`) of
                ``ComponentBase``) = `None`, Optional (Keyword only)
            Components attached to the message.
            
            > `components` do not count towards having any content in the message.
        
        embed : `None`, ``EmbedBase``, `list` of ``EmbedBase`` = `None`, Optional (Keyword only)
            The embedded content of the interaction response.
            
            If `embed` and `content` parameters are both given as ``EmbedBase``, then `AssertionError` is
            raised.
        
        suppress_embeds : `bool` = `False`, Optional (Keyword only)
            Whether the message's embeds should be suppressed initially.
        
        show_for_invoking_user_only : `bool` = `False`, Optional (Keyword only)
            Whether the sent message should only be shown to the invoking user. Defaults to `False`.
        
        tts : `bool` = `False`, Optional (Keyword only)
            Whether the message is text-to-speech.
        
        Raises
        ------
        TypeError
            - If `allowed_mentions` contains an element of invalid type.
            - If `embed` was not given neither as ``EmbedBase`` nor as `list`, `tuple` of ``EmbedBase``-s.
            - If `content` parameter was given as ``EmbedBase``, meanwhile `embed` parameter was given as well.
            - If `components` type is incorrect.
        ValueError
            If `allowed_mentions`'s elements' type is correct, but one of their value is invalid.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `interaction` was not given an ``InteractionEvent``.
            - If `tts` was not given as `bool`.
            - If `show_for_invoking_user_only` was not given as `bool`.
            - If `embed` contains a non ``EmbedBase`` element.
            - If both `content` and `embed` fields are embeds.
            - If `suppress_embeds` is not `bool`.
        
        Notes
        -----
        Discord do not returns message data, so the method cannot return a ``Message`` either.
        
        If the interaction is already timed or out or was used, you will get:
        
        ```
        DiscordException Not Found (404), code=10062: Unknown interaction
        ```
        """
        if __debug__:
            if not isinstance(interaction, InteractionEvent):
                raise AssertionError(
                    f'`interaction` can be `{InteractionEvent.__name__}`, got '
                    f'{interaction.__class__.__name__}; {interaction!r}.'
                )
        
        
        content, embed = validate_content_and_embed(content, embed, False)
        
        components = get_components_data(components, False)
        
        if __debug__:
            if not isinstance(show_for_invoking_user_only, bool):
                raise AssertionError(
                    f'`show_for_invoking_user_only` can be `bool`, got '
                    f'{show_for_invoking_user_only.__class__.__name__}; {show_for_invoking_user_only!r}.'
                )
            
            if not isinstance(suppress_embeds, bool):
                raise AssertionError(
                    f'`suppress_embeds` can be `bool`, got {suppress_embeds.__class__.__name__}; {suppress_embeds!r}.'
                )
            
            if not isinstance(tts, bool):
                raise AssertionError(
                    f'`tts` can be `bool`, got {tts.__class__.__name__}; {tts!r}.'
                )
        
        # Build payload
        
        message_data = {}
        contains_content = False
        
        if (content is not None):
            message_data['content'] = content
            contains_content = True
        
        if (embed is not None):
            message_data['embeds'] = [embed.to_data() for embed in embed]
            contains_content = True
        
        if (allowed_mentions is not ...):
            message_data['allowed_mentions'] = parse_allowed_mentions(allowed_mentions)
        
        if (components is not None):
            message_data['components'] = components
        
        if tts:
            message_data['tts'] = True
        
        if message_data:
            is_deferring = False
        else:
            is_deferring = True
        
        flags = 0
        
        if show_for_invoking_user_only:
            flags |= MESSAGE_FLAG_VALUE_INVOKING_USER_ONLY
        
        if suppress_embeds:
            flags |= MESSAGE_FLAG_VALUE_SUPPRESS_EMBEDS
        
        if flags:
            message_data['flags'] = flags
            contains_content = True
        
        data = {}
        if contains_content:
            data['data'] = message_data
        
        if is_deferring:
            response_type = INTERACTION_RESPONSE_TYPES.source
        else:
            response_type = INTERACTION_RESPONSE_TYPES.message_and_source
        
        data['type'] = response_type
        
        async with InteractionResponseContext(interaction, is_deferring, show_for_invoking_user_only):
            await self.http.interaction_response_message_create(interaction.id, interaction.token, data)
        
        # No message data is returned by Discord, return `None`.
        return None
    
    
    async def interaction_component_acknowledge(self, interaction, wait=True):
        """
        Acknowledges the given component interaction.
        
        This method is a coroutine.
        
        Parameters
        ----------
        interaction : ``InteractionEvent``
            Interaction to acknowledge
        wait : `bool` = `True`, Optional
            Whether the interaction should be ensured asynchronously.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If `interaction` was not given an ``InteractionEvent``.
        
        Notes
        -----
        If the interaction is already timed or out or was used, you will get:
        
        ```
        DiscordException Not Found (404), code=10062: Unknown interaction
        ```
        """
        if __debug__:
            if not isinstance(interaction, InteractionEvent):
                raise AssertionError(
                    f'`interaction` can be `{InteractionEvent.__name__}`, got '
                    f'{interaction.__class__.__name__}; {interaction!r}.'
                )
        
        # Do not ack twice
        if not interaction.is_unanswered():
            return
        
        data = {'type': INTERACTION_RESPONSE_TYPES.component}
        
        context = InteractionResponseContext(interaction, True, False)
        coroutine = self.http.interaction_response_message_create(interaction.id, interaction.token, data)
        
        
        if wait:
            async with context:
                await coroutine
        else:
            await context.ensure(coroutine)
    
    
    async def interaction_response_message_edit(self, interaction, content=..., *, embed=..., file=...,
            allowed_mentions=..., components=...):
        """
        Edits the given `interaction`'s source response. If the source interaction event was only deferred, this call
        will send the message as well.
        
        This method is a coroutine.
        
        Parameters
        ----------
        interaction : ``InteractionEvent``
            Interaction, what's source response message will be edited.
        
        content : `None`, `str`, ``EmbedBase``, `Any`, Optional
            The new content of the message.
            
            If given as ``EmbedBase``, then the message's embeds will be edited with it.
        
        embed : `None`, ``EmbedBase``, `list` of ``EmbedBase``, Optional (Keyword only)
            The new embedded content of the message. By passing it as `None`, you can remove the old.
            
            If `embed` and `content` parameters are both given as  ``EmbedBase``, then `AssertionError` is
            raised.
        
        file : `None`, `Any`, Optional (Keyword only)
            A file or files to send. Check ``create_file_form`` for details.
        
        allowed_mentions : `None`, `str`, ``UserBase``, ``Role``, `list` of (`str`, ``UserBase``, ``Role`` )
                , Optional (Keyword only)
            Which user or role can the message ping (or everyone). Check ``parse_allowed_mentions`` for details.
        
        components : `None`, ``ComponentBase``, (`tuple`, `list`) of (``ComponentBase``, (`tuple`, `list`) of
                ``ComponentBase``), Optional (Keyword only)
            Components attached to the message.
            
            Pass it as `None` remove the actual ones.
        
        Raises
        ------
        TypeError
            - If `allowed_mentions` contains an element of invalid type.
            - If `embed` was not given neither as ``EmbedBase`` nor as `list`, `tuple` of ``EmbedBase``-s.
            - If `content` parameter was given as ``EmbedBase``, meanwhile `embed` parameter was given as well.
        ValueError
            If `allowed_mentions`'s elements' type is correct, but one of their value is invalid.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `interaction` was not given as ``InteractionEvent``.
            - If the client's application is not yet synced.
            - If `embed` contains a non ``EmbedBase`` element.
            - If both `content` and `embed` fields are embeds.
        
        Notes
        -----
        Cannot editing interaction messages, which were created with `show_for_invoking_user_only=True`:
        
        ```
        DiscordException Not Found (404), code=10008: Unknown Message
        ```
        """
        application_id = self.application.id
        if __debug__:
            if application_id == 0:
                raise AssertionError('The client\'s application is not yet synced.')
        
        if __debug__:
            if not isinstance(interaction, InteractionEvent):
                raise AssertionError(f'`interaction` can be `{InteractionEvent.__name__}`, got '
                    f'{interaction.__class__.__name__}; {interaction!r}.')
        
        content, embed = validate_content_and_embed(content, embed, True)
        
        components = get_components_data(components, True)
        
        # Build payload
        message_data = {}
        
        # Discord docs say, content can be nullable, but nullable content is just ignored.
        if (content is not ...):
            message_data['content'] = content
        
        if (embed is not ...):
            if (embed is not None):
                embed = [embed.to_data() for embed in embed]
            
            message_data['embeds'] = embed
        
        if (allowed_mentions is not ...):
            message_data['allowed_mentions'] = parse_allowed_mentions(allowed_mentions)
        
        if (components is not ...):
            message_data['components'] = components
        
        message_data = add_file_to_message_data(message_data, file, True, True)
        
        async with InteractionResponseContext(interaction, False, False):
            await self.http.interaction_response_message_edit(application_id, interaction.id, interaction.token,
                message_data)
    
    
    async def interaction_component_message_edit(self, interaction, content=..., *, embed=..., allowed_mentions=...,
            components=...):
        """
        Edits the given component interaction's source message.
        
        This method is a coroutine.
        
        Parameters
        ----------
        interaction : ``InteractionEvent``
            Interaction, what's source response message will be edited.
        
        content : `None`, `str`, ``EmbedBase``, `Any`, Optional
            The new content of the message.
            
            If given as ``EmbedBase``, then the message's embeds will be edited with it.
        
        embed : `None`, ``EmbedBase``, `list` of ``EmbedBase``, Optional (Keyword only)
            The new embedded content of the message. By passing it as `None`, you can remove the old.
            
            If `embed` and `content` parameters are both given as  ``EmbedBase``, then `AssertionError` is
            raised.
        
        allowed_mentions : `None`, `str`, ``UserBase``, ``Role``, `list` of (`str`, ``UserBase``, ``Role`` )
                , Optional (Keyword only)
            Which user or role can the message ping (or everyone). Check ``parse_allowed_mentions`` for details.
        
        Raises
        ------
        TypeError
            - If `allowed_mentions` contains an element of invalid type.
            - If `embed` was not given neither as ``EmbedBase`` nor as `list`, `tuple` of ``EmbedBase``-s.
            - If `content` parameter was given as ``EmbedBase``, meanwhile `embed` parameter was given as well.
        ValueError
            If `allowed_mentions`'s elements' type is correct, but one of their value is invalid.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `interaction` was not given as ``InteractionEvent``.
            - If the client's application is not yet synced.
            - If `embed` contains a non ``EmbedBase`` element.
            - If both `content` and `embed` fields are embeds.
        """
        if __debug__:
            if not isinstance(interaction, InteractionEvent):
                raise AssertionError(
                    f'`interaction` can be `{InteractionEvent.__name__}`, got '
                    f'{interaction.__class__.__name__}; {interaction!r}.'
                )
        
        content, embed = validate_content_and_embed(content, embed, True)
        
        components = get_components_data(components, True)
        
        # Build payload
        message_data = {}
        
        if (content is not ...):
            message_data['content'] = content
        
        if (embed is not ...):
            if (embed is not None):
                embed = [embed.to_data() for embed in embed]
            
            message_data['embeds'] = embed
        
        if (allowed_mentions is not ...):
            message_data['allowed_mentions'] = parse_allowed_mentions(allowed_mentions)
        
        if (components is not ...):
            message_data['components'] = components
        
        data = {
            'data': message_data,
            'type': INTERACTION_RESPONSE_TYPES.component_message_edit,
        }
        
        
        async with InteractionResponseContext(interaction, False, False):
            await self.http.interaction_response_message_create(interaction.id, interaction.token, data)
    
    
    async def interaction_response_message_delete(self, interaction):
        """
        Deletes the given `interaction`'s source response message.
        
        This method is a coroutine.
        
        Parameters
        ----------
        interaction : ``InteractionEvent``
            Interaction, what's source response message will be deleted.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `interaction` was not given as ``InteractionEvent``.
            - If the client's application is not yet synced.
        """
        application_id = self.application.id
        if __debug__:
            if application_id == 0:
                raise AssertionError(
                    'The client\'s application is not yet synced.'
                )
        
        if __debug__:
            if not isinstance(interaction, InteractionEvent):
                raise AssertionError(
                    f'`interaction` can be `{InteractionEvent.__name__}`, got '
                    f'{interaction.__class__.__name__}; {interaction!r}.'
                )
        
        await self.http.interaction_response_message_delete(application_id, interaction.id, interaction.token)
    
    
    async def interaction_response_message_get(self, interaction):
        """
        Gets the given `interaction`'s source response message.
        
        This method is a coroutine.
        
        Parameters
        ----------
        interaction : ``InteractionEvent``
            Interaction, what's source response message will be deleted.
        
        Returns
        -------
        message : ``Message``
            The created message.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `interaction` was not given as ``InteractionEvent``.
            - If the client's application is not yet synced.
        """
        application_id = self.application.id
        if __debug__:
            if application_id == 0:
                raise AssertionError(
                    'The client\'s application is not yet synced.'
                )
        
        if __debug__:
            if not isinstance(interaction, InteractionEvent):
                raise AssertionError(
                    f'`interaction` can be `{InteractionEvent.__name__}`, got '
                    f'{interaction.__class__.__name__}; {interaction!r}.'
                )
        
        message_data = await self.http.interaction_response_message_get(application_id, interaction.id,
            interaction.token)
        
        return Message(message_data)
    
    
    async def interaction_followup_message_create(self, interaction, content=None, *, allowed_mentions=...,
            components=None,  embed=None, file=None, show_for_invoking_user_only=False, suppress_embeds=False,
            tts=False):
        """
        Sends a followup message with the given interaction.
        
        This method is a coroutine.
        
        Parameters
        ----------
        interaction : ``InteractionEvent``
            Interaction to create followup message with.
        
        content : `None`, `str`, ``EmbedBase``, `Any` = `True`, Optional
            The message's content if given. If given as `str` or empty string, then no content will be sent, meanwhile
            if any other non `str`, ``EmbedBase`` is given, then will be casted to string.
            
            If given as ``EmbedBase``, then is sent as the message's embed.
        
        allowed_mentions : `None`, `str`, ``UserBase``, ``Role``, `list` of (`str`, ``UserBase``, ``Role`` )
                , Optional (Keyword only)
            Which user or role can the message ping (or everyone). Check ``parse_allowed_mentions`` for details.
        

        components : `None`, ``ComponentBase``, (`tuple`, `list`) of (``ComponentBase``, (`tuple`, `list`) of
                ``ComponentBase``) = `None`, Optional (Keyword only)
            Components attached to the message.
            
            > `components` do not count towards having any content in the message.
        
        embed : `None`, ``EmbedBase``, `list` of ``EmbedBase`` = `None`, Optional (Keyword only)
            The embedded content of the message.
            
            If `embed` and `content` parameters are both given as  ``EmbedBase``, then `TypeError` is raised.
        
        file : `None`, `Any` = `None`, Optional
            A file to send. Check ``create_file_form`` for details.
        
        show_for_invoking_user_only : `bool` = `False`, Optional (Keyword only)
            Whether the sent message should only be shown to the invoking user. Defaults to `False`.
            
            If given as `True` only the message's content, embeds and components will be processed by Discord.
        
        suppress_embeds : `bool` = `False`, Optional (Keyword only)
            Whether the message's embeds should be suppressed initially.
        
        tts : `bool` = `False`, Optional (Keyword only)
            Whether the message is text-to-speech. Defaults to `False`.
        
        
        Returns
        -------
        message : `None`, ``Message``
            Returns `None` if there is nothing to send.
        
        Raises
        ------
        TypeError
            - If `allowed_mentions` contains an element of invalid type.
            - If `embed` was not given neither as ``EmbedBase`` nor as `list`, `tuple` of ``EmbedBase``-s.
            - `content` parameter was given as ``EmbedBase``, meanwhile `embed` parameter was given as well.
            - If invalid file type would be sent.
            - If `components` type is incorrect.
        ValueError
            - If `allowed_mentions`'s elements' type is correct, but one of their value is invalid.
            - If more than `10` files would be sent.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `interaction` was not given as ``InteractionEvent``.
            - If the client's application is not yet synced.
            - If `tts` was not given as `bool`.
            - If `show_for_invoking_user_only` was not given as `bool`.
            - If `embed` contains a non ``EmbedBase`` element.
            - If both `content` and `embed` fields are embeds.
            - If `suppress_embeds` is not `bool`.
        """
        if __debug__:
            if not isinstance(interaction, InteractionEvent):
                raise AssertionError(
                    f'`interaction` can be `{InteractionEvent.__name__}`, got '
                    f'{interaction.__class__.__name__}; {interaction!r}.'
                )
        
        
        application_id = self.application.id
        if __debug__:
            if application_id == 0:
                raise AssertionError(
                    'The client\'s application is not yet synced.'
                )
        
        content, embed = validate_content_and_embed(content, embed, False)
        
        components = get_components_data(components, False)
        
        if __debug__:
            if not isinstance(show_for_invoking_user_only, bool):
                raise AssertionError(
                    f'`show_for_invoking_user_only` can be `bool`, got '
                    f'{show_for_invoking_user_only.__class__.__name__}; {show_for_invoking_user_only!r}.'
                )
            
            if not isinstance(suppress_embeds, bool):
                raise AssertionError(
                    f'`suppress_embeds` can be `bool`, got {suppress_embeds.__class__.__name__}; {suppress_embeds!r}.'
                )
            
            if not isinstance(tts, bool):
                raise AssertionError(
                    f'`tts` can be `bool`, got {tts.__class__.__name__}; {tts!r}.'
                )
        
        # Build payload
        
        message_data = {}
        contains_content = False
        
        if (content is not None):
            message_data['content'] = content
            contains_content = True
        
        if (embed is not None):
            message_data['embeds'] = [embed.to_data() for embed in embed]
            contains_content = True
        
        if (allowed_mentions is not ...):
            message_data['allowed_mentions'] = parse_allowed_mentions(allowed_mentions)
        
        if (components is not None):
            message_data['components'] = components
        
        if tts:
            message_data['tts'] = True
        
        flags = 0
        
        if show_for_invoking_user_only:
            flags |= MESSAGE_FLAG_VALUE_INVOKING_USER_ONLY
        
        if suppress_embeds:
            flags |= MESSAGE_FLAG_VALUE_SUPPRESS_EMBEDS
        
        if flags:
            message_data['flags'] = flags
        
        message_data = add_file_to_message_data(message_data, file, contains_content, False)
        if message_data is None:
            return
        
        async with InteractionResponseContext(interaction, False, show_for_invoking_user_only):
            message_data = await self.http.interaction_followup_message_create(application_id, interaction.id,
                interaction.token, message_data)
        
        message = interaction.channel._create_new_message(message_data)
        try_resolve_interaction_message(message, interaction)
        return message
    
    
    async def interaction_followup_message_edit(self, interaction, message, content=..., *, embed=..., file=...,
            allowed_mentions=..., components=...):
        """
        Edits the given interaction followup message.
        
        This method is a coroutine.
        
        Parameters
        ----------
        interaction : ``InteractionEvent``
            Interaction with what the followup message was sent with.
        
        message : ``Message``, ``MessageRepr``, `int`
            The interaction followup's message to edit.
        
        content : `None`, `str`, ``EmbedBase``, `Any`, Optional
            The new content of the message.
            
            If given as `str` then the message's content will be edited with it. If given as any non ``EmbedBase``
            instance, then it will be cased to string first.
            
            By passing it as empty string, you can remove the message's content.
            
            If given as ``EmbedBase``, then the message's embeds will be edited with it.
        
        embed : `None`, ``EmbedBase``, `list` of ``EmbedBase``, Optional (Keyword only)
            The new embedded content of the message. By passing it as `None`, you can remove the old.
            
            If `embed` and `content` parameters are both given as  ``EmbedBase``, then `TypeError` is raised.
        
        file : `None`, `Any`, Optional (Keyword only)
            A file or files to send. Check ``create_file_form`` for details.
        
        allowed_mentions : `None`,  `str`, ``UserBase``, ``Role``, `list` of (`str`, ``UserBase``, ``Role`` )
                , Optional (Keyword only)
            Which user or role can the message ping (or everyone). Check ``parse_allowed_mentions``
            for details.
        
        components : `None`, ``ComponentBase``, (`tuple`, `list`) of (``ComponentBase``, (`tuple`, `list`) of
                ``ComponentBase``), Optional (Keyword only)
            Components attached to the message.
            
            Pass it as `None` remove the actual ones.
        
        Raises
        ------
        TypeError
            - If `allowed_mentions` contains an element of invalid type.
            - If `embed` was not given neither as ``EmbedBase`` nor as `list`, `tuple` of ``EmbedBase``-s.
            - If `content` parameter was given as ``EmbedBase``, meanwhile `embed` parameter was given as well.
            - If `message` was not given neither as ``Message``, ``MessageRepr``  or `int`.
        ValueError
            If `allowed_mentions`'s elements' type is correct, but one of their value is invalid.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `interaction` was not given as ``InteractionEvent``.
            - If the client's application is not yet synced.
            - If `embed` contains a non ``EmbedBase`` element.
            - If both `content` and `embed` fields are embeds.
        
        Notes
        -----
        Cannot editing interaction messages, which were created with `show_for_invoking_user_only=True`:
        
        ```
        DiscordException Not Found (404), code=10008: Unknown Message
        ```
        """
        application_id = self.application.id
        if __debug__:
            if application_id == 0:
                raise AssertionError(
                    'The client\'s application is not yet synced.'
                )
        
        if __debug__:
            if not isinstance(interaction, InteractionEvent):
                raise AssertionError(
                    f'`interaction` can be `{InteractionEvent.__name__}`, got '
                    f'{interaction.__class__.__name__}; {interaction!r}.'
                )
        
        # Detect message id
        # 1.: Message
        # 2.: int (str)
        # 3.: MessageRepr
        # 5.: raise
        
        if isinstance(message, Message):
            message_id = message.id
        else:
            message_id = maybe_snowflake(message)
            if (message_id is not None):
                pass
            elif isinstance(message, MessageRepr):
                # Cannot check author id, skip
                message_id = message.id
            else:
                raise TypeError(
                    f'`message` can be `{Message.__name__}`, `{MessageRepr.__name__}`, `int`, got '
                    f'{message.__class__.__name__}, {message!r}.'
                )
        
        content, embed = validate_content_and_embed(content, embed, True)
        
        components = get_components_data(components, True)
        
        # Build payload
        message_data = {}
        
        # Discord docs say, content can be nullable, but nullable content is just ignored.
        if (content is not ...):
            message_data['content'] = content
        
        if (embed is not ...):
            if (embed is not None):
                embed = [embed.to_data() for embed in embed]
            
            message_data['embeds'] = embed
        
        if (allowed_mentions is not ...):
            message_data['allowed_mentions'] = parse_allowed_mentions(allowed_mentions)
        
        if (components is not ...):
            message_data['components'] = components
        
        message_data = add_file_to_message_data(message_data, file, True, True)
        
        async with InteractionResponseContext(interaction, False, False):
            # We receive the new message data, but we do not update the message, so dispatch events can get the
            # difference.
            await self.http.interaction_followup_message_edit(application_id, interaction.id, interaction.token,
                message_id, message_data)
    
    
    async def interaction_followup_message_delete(self, interaction, message):
        """
        Deletes an interaction's followup message.
        
        This method is a coroutine.
        
        Parameters
        ----------
        interaction : ``InteractionEvent``
            Interaction with what the followup message was sent with.
        message : ``Message``, ``MessageRepr``, `int`
            The interaction followup's message to edit.
        
        Raises
        ------
        TypeError
            If `message` was not given neither as ``Message``, ``MessageRepr``  or `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `interaction` was not given as ``InteractionEvent``.
            - If the client's application is not yet synced.
        """
        application_id = self.application.id
        if __debug__:
            if application_id == 0:
                raise AssertionError(
                    'The client\'s application is not yet synced.'
                )
        
        if __debug__:
            if not isinstance(interaction, InteractionEvent):
                raise AssertionError(
                    f'`interaction` can be `{InteractionEvent.__name__}`, got '
                    f'{interaction.__class__.__name__}; {interaction!r}.'
                )
        
        # Detect message id
        # 1.: Message
        # 2.: int (str)
        # 3.: MessageRepr
        # 5.: raise
        
        if isinstance(message, Message):
            message_id = message.id
        else:
            message_id = maybe_snowflake(message)
            if (message_id is not None):
                pass
            elif isinstance(message, MessageRepr):
                # Cannot check author id, skip
                message_id = message.id
            else:
                raise TypeError(
                    f'`message` can be `{Message.__name__}`, `{MessageRepr.__name__}`, `int`, got '
                    f'{message.__class__.__name__}; {message!r}.'
                )
        
        await self.http.interaction_followup_message_delete(application_id, interaction.id, interaction.token,
            message_id)
    
    
    async def interaction_followup_message_get(self, interaction, message_id):
        """
        Gets a previously sent message with an interaction.
        
        This method is a coroutine.
        
        Parameters
        ----------
        interaction : ``InteractionEvent``
            Interaction with what the followup message was sent with.
        message_id : `int`
            The webhook's message's identifier to get.
        
        Returns
        -------
        message : ``Message``
        
        Raises
        ------
        TypeError
            - If `message_id` was not given as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `interaction` was not given as ``InteractionEvent``.
            - If the client's application is not yet synced.
        """
        application_id = self.application.id
        if __debug__:
            if application_id == 0:
                raise AssertionError(
                    'The client\'s application is not yet synced.'
                )
        
        if __debug__:
            if not isinstance(interaction, InteractionEvent):
                raise AssertionError(
                    f'`interaction` can be `{InteractionEvent.__name__}`, got '
                    f'{interaction.__class__.__name__}; {interaction!r}.'
                )
        
        message_id_value = maybe_snowflake(message_id)
        if message_id_value is None:
            raise TypeError(
                f'`message_id` can be `int`, got {message_id.__class__.__name__}; {message_id!r}.'
            )
        
        message_data = await self.http.interaction_followup_message_get(application_id, interaction.id,
            interaction.token, message_id)
        
        return Message(message_data)
    
    # Sticker
    
    async def sticker_get(self, sticker, *, force_update=False):
        """
        Gets an sticker by it's id. If the sticker is already loaded updates it.
        
        This method is a coroutine.
        
        Parameters
        ----------
        sticker : ``Sticker``, `int`
            The sticker, who will be requested.
        force_update : `bool` = `False`, Optional (Keyword only)
            Whether the sticker should be requested even if it supposed to be up to date.
        
        Returns
        -------
        sticker : ``Sticker``
        
        Raises
        ------
        TypeError
            If `sticker` was not given neither as ``Sticker``, neither as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        TypeError
            If `sticker` was not given as ``Sticker``, nor as `int`.
        """
        sticker, sticker_id = get_sticker_and_id(sticker)
        if (sticker is not None) and (not sticker.partial) and (not force_update):
            return sticker
        
        data = await self.http.sticker_get(sticker_id)
        if (sticker is None):
            sticker = Sticker(data)
        else:
            sticker._update_from_partial(data)
        
        return sticker
    
    
    async def sticker_pack_get(self, sticker_pack, *, force_update=False):
        """
        Gets the sticker packs. If the sticker-packs are already loaded, updates them.
        
        This method is a coroutine.
        
        Parameters
        ----------
        sticker_pack : ``StickerPack``, `int`
            The sticker pack' identifier.
        force_update : `bool` = `False`, Optional (Keyword only)
            Whether the sticker-pack should be requested even if it supposed to be up to date.
        
        Returns
        -------
        sticker_packs : `list` of ``StickerPack``
        
        Raises
        ------
        TypeError
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        sticker_pack, sticker_pack_id = get_sticker_pack_and_id(sticker_pack)
        
        if (sticker_pack is None) or force_update:
            sticker_pack_data = await self.http.sticker_pack_get(sticker_pack_id)
            sticker_pack = StickerPack._create_and_update(sticker_pack_data)
        
        return sticker_pack
    
    
    async def sticker_pack_get_all(self, *, force_update=False):
        """
        Gets the sticker packs. If the sticker-packs are already loaded, updates them.
        
        This method is a coroutine.
        
        Parameters
        ----------
        force_update : `bool` = `False`, Optional (Keyword only)
            Whether the sticker-packs should be requested even if it supposed to be up to date.
        
        Returns
        -------
        sticker_packs : `list` of ``StickerPack``
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        if force_update or (not STICKER_PACK_CACHE.synced):
            data = await self.http.sticker_pack_get_all()
            sticker_pack_datas = data['sticker_packs'] # Discord pls.
            if force_update:
                sticker_packs = [StickerPack._create_and_update(sticker_pack_data) for sticker_pack_data in
                    sticker_pack_datas]
            else:
                sticker_packs = [StickerPack(sticker_pack_data) for sticker_pack_data in sticker_pack_datas]
            
            STICKER_PACK_CACHE.set(sticker_packs)
        else:
            sticker_packs = STICKER_PACK_CACHE.value
        
        return sticker_packs
    
    
    async def sticker_guild_get(self, guild, sticker, *, force_update=False):
        """
        Gets the specified sticker from the respective guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The respective guild.
        sticker : ``Sticker``, `int`
            The sticker to get.
        force_update : `bool` = `False`, Optional (Keyword only)
            Whether the sticker should be requested even if it supposed to be up to date.
        
        Raises
        ------
        TypeError
            If `sticker` was not given neither as ``Sticker``, neither as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        TypeError
            - If `sticker` was not given as ``Sticker``, nor as `int`.
            - If `guild` was not given as ``Guild``, nor as `int`.
        """
        sticker, sticker_id = get_sticker_and_id(sticker)
        if (sticker is not None) and (not sticker.partial) and (not force_update):
            return sticker
        
        guild_id = get_guild_id(guild)
        
        data = await self.http.sticker_guild_get(guild_id, sticker_id)
        if (sticker is None):
            sticker = Sticker(data)
        else:
            sticker._update_from_partial(data)
        
        return sticker
    
    
    async def sticker_guild_create(self, guild, name, image, emoji_representation, description=None, *, reason=None):
        """
        Creates a sticker in the guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild to create the sticker in.
        name : `str`
            The sticker's name. It's length can be in range [2:32]
        emoji_representation : ``Emoji``, `str`
            The emoji representation of the sticker. Used as a tag for the sticker.
        image : `bytes-like`
            The sticker's image in bytes.
        description : `None`, `str` = `None`, Optional
            The sticker's representation. It's length can be in range [0:100]
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Will show up at the respective guild's audit logs.
        
        Returns
        -------
        sticker : ``Sticker``
            The created sticker.
        
        Raises
        ------
        TypeError
            - If `emoji_representation` is neither `str` nor ``Emoji``.
            - If `guild` is neither ``Guild`` nor `int`.
        ValueError
            If `image`s media type is neither `image/png` nor `application/json`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `name` is not `str`.
            - If `name`'s length is out of range [2:32].
            - If `description` is neither `None`, `str`.
            - If `description`'s length is out of range [0:100].
            - If `emoji_representation` is a custom ``Emoji``.
        """
        guild_id = get_guild_id(guild)
        
        if __debug__:
            if not isinstance(name, str):
                raise AssertionError(
                    f'`name` can be `str`, got {name.__class__.__name__}; {name!r}.'
                )
        
            name_length = len(name)
            if (name_length < 2) or (name_length > 32):
                raise AssertionError(
                    f'`name` length can be in range [2:32], got {name_length!r}; {name!r}.'
                )
        
        if __debug__:
            if (description is not None):
                if (not isinstance(description, str)):
                    raise AssertionError(
                        f'`description` can be `str`, got {description.__class__.__name__}; {description!r}.'
                    )
                
                description_length = len(description)
                if (description_length > 100):
                    raise AssertionError(
                        f'`description` length can be in range [0:100], got {description_length!r}; {description!r}.'
                    )
        
        if (description is not None) and (not description):
            description = None
        
        if isinstance(emoji_representation, str):
            tag = emoji_representation
        elif isinstance(emoji_representation, Emoji):
            if __debug__:
                if emoji_representation.is_custom_emoji():
                    raise AssertionError(
                        f'Only unicode (builtin) emojis can be used as tags, got {emoji_representation!r}.'
                    )
            
            tag = emoji_representation.name
        else:
            raise TypeError(
                f'`emoji_representation` can be `str`, `{Emoji.__name__}`, got '
                f'{emoji_representation.__class__.__name__}; {emoji_representation!r}.'
            )
        
        if __debug__:
            if not isinstance(image, (bytes, bytearray, memoryview)):
                raise TypeError(
                    f'`image` can be `None`, `bytes-like`, got {image.__class__.__name__}; {reprlib.repr(image)}.'
                )
        
        media_type = get_image_media_type(image)
        if media_type not in VALID_STICKER_IMAGE_MEDIA_TYPES:
            raise ValueError(
                f'Invalid `image` type: {media_type}, got {reprlib.repr(image)}.'
            )
        
        extension = MEDIA_TYPE_TO_EXTENSION[media_type]
        
        form_data = Formdata()
        form_data.add_field('name', name)
        
        if (description is not None):
            form_data.add_field('description', description)
        
        form_data.add_field('tags', tag)
        
        form_data.add_field('file', image, filename=f'file.{extension}', content_type=media_type)
        
        sticker_data = await self.http.sticker_guild_create(guild_id, form_data, reason)
        
        return Sticker(sticker_data)
    
    
    async def sticker_guild_edit(self, sticker, *, name=..., emoji_representation=..., description=..., reason=None):
        """
        Edits the given guild bound sticker,
        
        This method is a coroutine.
        
        Parameters
        ----------
        sticker : ``Sticker``, `int`
            The respective sticker.
        name : `str`, Optional (keyword only)
            New name of the sticker. It's length can be in range [2:32].
        emoji_representation : ``Emoji``, `str`, Optional (keyword Only)
            The new emoji representation of the sticker. Used as a tag for the sticker.
        description : `None`, `str`, Optional (Keyword only)
            New description for the sticker. It's length can be in range [0:100].
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Will show up at the respective guild's audit logs.
        
        Raises
        ------
        TypeError
            - If `sticker` is neither ``Sticker``, nor `int`.
            - If `emoji_representation` is neither `str` nor ``Emoji``.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - Non guild bound sticker cannot be edited.
            - If `name` is not `str`.
            - If `name`'s length is out of range [2:32].
            - If `description` is neither `None`, `str`.
            - If `description`'s length is out of range [0:100].
            - If `emoji_representation` is a custom ``Emoji``.
        """
        sticker = await self.sticker_get(sticker)
        
        if __debug__:
            if not sticker.guild_id:
                raise AssertionError(
                    f'Non guild bound sticker cannot be edited, got {sticker!r}.'
                )
        
        if (name is ...):
            name = sticker.name
        else:
            if __debug__:
                if not isinstance(name, str):
                    raise AssertionError(
                        f'`name` can be `str`, got {name.__class__.__name__}; {name!r}.'
                    )
            
                name_length = len(name)
                if (name_length < 2) or (name_length > 32):
                    raise AssertionError(
                        f'`name` length can be in range [2:32], got {name_length!r}; {name!r}.'
                    )
        
        if (emoji_representation is ...):
            tag = ', '.join(sticker.tags)
        else:
            if isinstance(emoji_representation, str):
                tag = emoji_representation
            elif isinstance(emoji_representation, Emoji):
                if __debug__:
                    if emoji_representation.is_custom_emoji():
                        raise AssertionError(
                            f'Only unicode (builtin) emojis can be used as tags, got {emoji_representation!r}.'
                        )
                
                tag = emoji_representation.name
            else:
                raise TypeError(
                    f'`emoji_representation` can be `str`, `{Emoji.__name__}`, got '
                    f'{emoji_representation.__class__.__name__}; {emoji_representation!r}.'
                )
        
        if (description is ...):
            description = sticker.description
        else:
            if __debug__:
                if (description is not None):
                    if (not isinstance(description, str)):
                        raise AssertionError(
                            f'`description` can be `None`, `str`, got {description.__class__.__name__}; '
                            f'{description!r}.'
                        )
            
                    description_length = len(description)
                    if (description_length > 100):
                        raise AssertionError(
                            f'`description` length can be in range [0:100], got {description_length!r}; '
                            f'{description!r}.'
                        )
            
            if (description is None):
                description = ''
        
        data = {
            'name': name,
            'tags': tag,
            'description': description,
        }
        
        await self.http.sticker_guild_edit(sticker.guild_id, sticker.id, data, reason)
    
    
    async def sticker_guild_delete(self, sticker, *, reason=None):
        """
        Deletes the sticker.
        
        This method is a coroutine.
        
        Parameters
        ----------
        sticker : ``Sticker``, `int`
            The sticker to delete.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Will show up at the respective guild's audit logs.
        
        Raises
        ------
        TypeError
            If `sticker` is neither ``Sticker``, nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            Non guild bound sticker cannot be edited.
        """
        sticker = await self.sticker_get(sticker)
        
        if __debug__:
            if not sticker.guild_id:
                raise AssertionError(
                    f'Non guild bound sticker cannot be edited, got {sticker!r}.'
                )
        
        await self.http.sticker_guild_delete(sticker.guild_id, sticker.id, reason)
    
    
    async def guild_sync_stickers(self, guild):
        """
        Syncs the given guild's stickers with the wrapper.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, what's stickers will be synced.
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as ``Guild`` nor as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild, guild_id = get_guild_and_id(guild)
        
        data = await self.http.sticker_guild_get_all(guild_id)
        
        if guild is None:
            guild = create_partial_guild_from_id(guild_id)
        
        guild._sync_stickers(data)
    
    
    # Relationship related
    
    async def relationship_delete(self, relationship):
        """
        Deletes the given relationship.
        
        This method is a coroutine.
        
        Parameters
        ----------
        relationship : ``Relationship``, ``ClientUserBase``, `int`
            The relationship to delete. Also can be given the respective user with who the client hast he relationship
            with.

        Raises
        ------
        TypeError
            If `relationship` was not given neither as ``Relationship``, ``ClientUserBase`` not as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        This endpoint is available only for user accounts.
        """
        if isinstance(relationship, Relationship):
            user_id = relationship.user.id
        elif isinstance(relationship, ClientUserBase):
            user_id = relationship.id
        else:
            user_id = maybe_snowflake(relationship)
            if user_id is None:
                raise TypeError(
                    f'`relationship` can be `{Relationship.__name__}`, `{ClientUserBase.__name__}`, `int`, got '
                    f'{relationship.__class__.__name__}; {relationship!r}.'
                )
        
        await self.http.relationship_delete(user_id)
    
    
    async def relationship_create(self, user, relationship_type=None):
        """
        Creates a relationship with the given user.
        
        This method is a coroutine.
        
        Parameters
        ----------
        user : ```ClientUserBase``, `int`
            The user with who the relationship will be created.
        relationship_type : `None`, ``RelationshipType``, `int` = `None`, Optional
            The type of the relationship. Defaults to `None`.
        
        Raises
        ------
        TypeError
            - If `user` is not given neither as ``ClientUserBase``, `int`.
            - If `relationship_type` was not given neither as `None`, ``RelationshipType`` neither as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        This endpoint is available only for user accounts.
        """
        user_id = get_user_id(user)
        
        if relationship_type is None:
            relationship_type_value = None
        elif isinstance(relationship_type, RelationshipType):
            relationship_type_value = relationship_type.value
        elif isinstance(relationship_type, int):
            relationship_type_value = relationship_type
        else:
            raise TypeError(
                f'`relationship_type` can be `None`, `{RelationshipType.__name__}`, `int`'
                f', got {relationship_type.__class__.__name__}; {relationship_type!r}.'
            )
        
        data = {}
        if (relationship_type_value is not None):
            data['type'] = relationship_type_value
        
        await self.http.relationship_create(user_id, data)
    
    
    async def relationship_friend_request(self, user):
        """
        Sends a friend request to the given user.
        
        This method is a coroutine.
        
        Parameters
        ----------
        user : ```ClientUserBase``, `int`
            The user, who will receive the friend request.
        
        Raises
        ------
        TypeError
            If `user` was not given neither as ```ClientUserBase``, `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        This endpoint is available only for user accounts.
        """
        user, user_id = get_user_and_id(user)
        if (user is None):
            user = await self.user_get(user_id)
        
        data = {
            'username': user.name,
            'discriminator': str(user.discriminator)
        }
        
        await self.http.relationship_friend_request(data)
    
    
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
        if self.is_bot:
            data = await self.http.client_application_get()
            application = self.application
            old_application_id = application.id
            application = application._create_update(data, False)
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
                if self.is_bot:
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
        self._gateway_url = gateway_url = f'{data["url"]}?encoding=json&v={API_VERSION}&compress=zlib-stream'
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
        self._gateway_url = f'{data["url"]}?encoding=json&v={API_VERSION}&compress=zlib-stream'
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
    
    
    async def hypesquad_house_change(self, house):
        """
        Changes the client's hypesquad house.
        
        This method is a coroutine.
        
        Parameters
        ----------
        house : `int`, ``HypesquadHouse``
            The hypesquad house to join.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Raises
        ------
        TypeError
            `house` was not given as `int`  neither as ``HypesquadHouse``.
        
        Notes
        -----
        User account only.
        """
        if isinstance(house, HypesquadHouse):
            house_id = house.value
        elif isinstance(house, int):
            house_id = house
        else:
            raise TypeError(
                f'`house` can be `int`, `{HypesquadHouse.__name__}`, got {house.__class__.__name__}; {house!r}.'
            )
        
        await self.http.hypesquad_house_change({'house_id': house_id})
    
    
    async def hypesquad_house_leave(self):
        """
        Leaves the client from it's current hypesquad house.
        
        This method is a coroutine.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        User account only.
        """
        await self.http.hypesquad_house_leave()
    
    
    def start(self):
        """
        Starts the clients's connecting to Discord. If the client is already running, raises `RuntimeError`.
        
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
            
            await KOKORO.render_exception_async(err, before, after)
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
        
        if self.is_bot:
            task = Task(self.update_application_info(), KOKORO)
            if __debug__:
                task.__silence__()
        
        # Check it twice, because meanwhile logging on, connect calls are not limited
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
                        await KOKORO.render_exception_async(
                            err,
                            [
                                'Ignoring unexpected outer Task or coroutine cancellation at ',
                                repr(self),
                                '._connect:\n',
                            ],
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
                                await KOKORO.render_exception_async(
                                    err,
                                    [
                                        'Ignoring unexpected outer Task or coroutine cancellation at ',
                                        repr(self),
                                        '._connect:\n',
                                    ],
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
                await KOKORO.render_exception_async(
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
                )
        
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
    
    
    async def join_voice(self, channel):
        """
        Joins a voice client to the channel. If there is an already existing voice client at the respective guild,
        moves it.
        
        If not every library is installed, raises `RuntimeError`, or if the voice client fails to connect raises
        `TimeoutError`.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``ChannelVoiceBase``, `tuple` (`int`, `int`)
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
        TypeError
            If `channel` was not given neither as ``ChannelVoiceBase`` nor as `tuple` (`int`, `int`).
        """
        if isinstance(channel, ChannelVoiceBase):
            guild_id = channel.guild_id
            channel_id = channel.id
        else:
            snowflake_pair = maybe_snowflake_pair(channel)
            if snowflake_pair is None:
                raise TypeError(
                    f'`channel` can be `{ChannelVoiceBase.__name__}`, `tuple` (`int`, `int`), got '
                    f'{channel.__class__.__name__}; {channel!r}.'
                )
            
            guild_id, channel_id = snowflake_pair
        
        try:
            voice_client = self.voice_clients[guild_id]
        except KeyError:
            voice_client = await VoiceClient(self, guild_id, channel_id)
        else:
            if voice_client.channel_id != channel_id:
                gateway = self.gateway_for(guild_id)
                await gateway.change_voice_state(guild_id, channel_id)
        
        return voice_client
    
    
    async def join_speakers(self, channel, *, request=False):
        """
        Request to speak or joins the client as a speaker inside of a stage channel. The client must be in the stage
        channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``ChannelStage``
            The stage channel to join.
        request : `bool` = `False`, Optional (Keyword only)
            Whether the client should only request to speak.
        
        Raises
        ------
        TypeError
            If `channel` was not given neither as ``ChannelStage`` nor as `tuple` (`int`, `int`).
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        if isinstance(channel, ChannelStage):
            guild_id = channel.guild_id
            channel_id = channel.id
        else:
            snowflake_pair = maybe_snowflake_pair(channel)
            if snowflake_pair is None:
                raise TypeError(
                    f'`channel` can be `{ChannelStage.__name__}`, `tuple`(`int`, `int`), got '
                    f'{channel.__class__.__name__}; {channel!r}.'
                )
            
            guild_id, channel_id = snowflake_pair
        
        if request:
            timestamp = datetime_to_timestamp(datetime.utcnow())
        else:
            timestamp = None
        
        data = {
            'suppress': False,
            'request_to_speak_timestamp': timestamp,
            'channel_id': channel_id
        }
        
        await self.http.voice_state_client_edit(guild_id, data)
    
    
    async def join_audience(self, channel):
        """
        Moves the client to the audience inside of the stage channel. The client must be in the stage channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``ChannelStage``, `tuple` (`int`, `int`)
            The stage channel to join.
        
        Raises
        ------
        RuntimeError
            If `channel` is partial.
        TypeError
            If `channel` was not given neither as ``ChannelStage`` nor as `tuple` (`int`, `int`).
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        if isinstance(channel, ChannelStage):
            guild_id = channel.guild_id
            channel_id = channel.id
        else:
            snowflake_pair = maybe_snowflake_pair(channel)
            if snowflake_pair is None:
                raise TypeError(
                    f'`channel` can be `{ChannelStage.__name__}`, `tuple`(`int`, `int`) , got '
                    f'{channel.__class__.__name__}; {channel!r}.'
                )
            
            guild_id, channel_id = snowflake_pair
        
        
        data = {
            'suppress': True,
            'channel_id': channel_id
        }
        
        await self.http.voice_state_client_edit(guild_id, data)
    
    
    async def wait_for(self, event_name, check, timeout=None):
        """
        O(n) event waiter with massive overhead compared to other optimized event waiters.
        
        This method is a coroutine.
        
        Parameters
        ----------
        event_name : `str`
            The respective event's name.
        check : `callable`
            Check, what tells that the waiting is over.
            
            If the `check` returns `True` the received `args` are passed to the waiter future and returned by the
            method. However if the check returns any non `bool` value, then that object is passed next to `args` and
            returned as well.
        
        timeout : `None`, `float` = `None`, Optional
            Timeout after `TimeoutError` is raised and the waiting is cancelled.
        
        Returns
        -------
        result : `Any`
            Parameters passed to the `check` and the value returned by the `check` if it's type is not `bool`.
        
        Raised
        ------
        TimeoutError
            Timeout occurred.
        BaseException
            Any exception raised by `check`.
        """
        wait_for_handler = self.events.get_handler(event_name, WaitForHandler)
        if wait_for_handler is None:
            wait_for_handler = WaitForHandler()
            self.events(wait_for_handler, name=event_name)
        
        future = Future(KOKORO)
        wait_for_handler.waiters[future] = check
        
        if (timeout is not None):
            future_or_timeout(future, timeout)
        
        try:
            return await future
        finally:
            waiters = wait_for_handler.waiters
            del waiters[future]
            
            if not waiters:
                self.events.remove(wait_for_handler, name=event_name)
    
    
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
            self.ready_state = ready_state = ReadyState(self)
        
        ready_state.shard_ready(self, guild_datas, shard_id)
    
    
    async def _request_members(self, guild_id):
        """
        Requests the members of the given guild. Called when the client joins a guild and user caching is enabled
        (so by default).
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild_id : ``int``
            The guild, what's members will be requested.
        """
        event_handler = self.events.guild_user_chunk
        
        self._user_chunker_nonce = nonce = self._user_chunker_nonce + 1
        nonce = nonce.__format__('0>16x')
        
        event_handler.waiters[nonce] = waiter = MassUserChunker()
        
        data = {
            'op': GATEWAY_OPERATION_CODE_REQUEST_MEMBERS,
            'd': {
                'guild_id': guild_id,
                'query': '',
                'limit': 0,
                'presences': CACHE_PRESENCE,
                'nonce': nonce
            },
        }
        
        gateway = self.gateway_for(guild_id)
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
        expected value or if timeout occurs, returns an empty list instead of raising.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``
            The guild, what's members will be requested.
        name : `str`
            The received user's name or nick should start with this string.
        limit : `int` = `1`, Optional
            The amount of users to received. Limited to `100`.
        
        Returns
        -------
        users : `list` of ``ClientUserBase``
        
        Raises
        ------
        TypeError
            - If `guild` was not given neither as ``Guild`` nor as `int`.
        AssertionError
            - If `limit` is not `int`.
            - If `limit` is out of the expected range [1:100].
            - If `name` is not `str`.
            - If `name` length is out of the expected range [1:32].
        """
        if isinstance(guild, Guild):
            guild_id = guild.id
        else:
            guild_id = maybe_snowflake(guild)
            if guild_id is None:
                raise TypeError(
                    f'`guild` can be `{Guild.__name__}`, `int`, got {guild.__class__.__name__}; {guild!r}.'
                )
        
        if __debug__:
            if not isinstance(limit, int):
                raise AssertionError(
                    f'`limit` can be `int`, got {limit.__class__.__name__}; {limit!r}.'
                )
            
            if limit < 1 or limit > 100:
                raise AssertionError(
                    f'`limit` is out of the expected range [1:100], got {limit!r}.'
                )
            
            if not isinstance(name, str):
                raise AssertionError(
                    f'`name` can be `str`, got {name.__class__.__name__}; {name!r}.'
                )
            
            name_length = len(name)
            if name_length < 1 or name_length > 32:
                raise AssertionError(
                    f'`name` length can be in range [1:32], got {name_length!r}; {name!r}.'
                )
        
        event_handler = self.events.guild_user_chunk
        
        self._user_chunker_nonce = nonce = self._user_chunker_nonce + 1
        nonce = nonce.__format__('0>16x')
        
        event_handler.waiters[nonce] = waiter = SingleUserChunker()
        
        data = {
            'op': GATEWAY_OPERATION_CODE_REQUEST_MEMBERS,
            'd': {
                'guild_id': guild_id,
                'query': name,
                'limit': limit,
                'presences': CACHE_PRESENCE,
                'nonce': nonce,
            },
        }
        
        gateway = self.gateway_for(guild_id)
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
        if (not self.is_bot):
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
        guild = message.guild
        if guild is None:
            voice_client = None
        else:
            voice_client = self.voice_clients.get(guild.id, None)
        return voice_client
    
    def get_guild(self, name, default=None):
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
            | banner_color          | `None`, ``Color``   |
            +-----------------------+-----------------------+
            | discriminator         | `int`                 |
            +-----------------------+-----------------------+
            | email                 | `None`, `str`       |
            +-----------------------+-----------------------+
            | flags                 | ``UserFlag``          |
            +-----------------------+-----------------------+
            | locale                | `str                  |
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
        
        
        locale = parse_locale(data)
        if self.locale != locale:
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
        
        self.locale = parse_locale(data)
    
    
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
            self.guild_profiles[guild.id] = GuildProfile(data)
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
            self.guild_profiles[guild.id] = GuildProfile(data)
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
        return [rs for rs in self.relationships.values() if rs.type is type_]
    
    
    @property
    def blocked(self):
        """
        Returns the client's blocked relationships.
        
        Returns
        -------
        relationships : `list` of ``Relationship`` objects
        """
        type_ = RelationshipType.blocked
        return [rs for rs in self.relationships.values() if rs.type is type_]
    
    
    @property
    def received_requests(self):
        """
        Returns the received friend requests of the client.
        
        Returns
        -------
        relationships : `list` of ``Relationship`` objects
        """
        type_ = RelationshipType.pending_incoming
        return [rs for rs in self.relationships.values() if rs.type is type_]
    
    
    @property
    def sent_requests(self):
        """
        Returns the sent friend requests of the client.
        
        Returns
        -------
        relationships : `list` of ``Relationship`` objects
        """
        type_ = RelationshipType.pending_outgoing
        return [rs for rs in self.relationships.values() if rs.type is type_]
    
    
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
