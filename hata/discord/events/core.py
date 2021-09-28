__all__ = ()

import warnings
from itertools import chain

try:
    from _weakref import WeakSet
except ImportError:
    from weakref import WeakSet

from ...backend.export import export
from ...backend.futures import Task

from ..core import KOKORO

from .intent import DISPATCH_EVENT_TO_INTENTS, INTENT_SHIFT_MISSING_EVENT, INTENT_SHIFT_DEFAULT_EVENT

PARSERS = {}

EVENT_HANDLER_EXPECTED_ARGUMENT_COUNTS = {}
EVENT_HANDLER_NAME_TO_PARSER_NAMES = {}

REGISTERED_CLIENTS = WeakSet()
PARSER_SETTINGS = {}

async def DEFAULT_EVENT_HANDLER(*args):
    """
    Default event handler what is set under events if there is no specified event handler to use.
    
    This function is a coroutine.
    
    Parameters
    ----------
    *args : Positional parameters
    """
    pass

def _iter_name(name):
    """
    Iterates the given dispatch event name.
    
    This function is a generator.
    
    Parameters
    ----------
    name : `str` or `tuple` of (`str` or ...)
        The name or names of the dispatch events.
    
    Yields
    ------
    name : `str`
    """
    if name is None:
        pass
    elif isinstance(name, tuple):
        for name in name:
            yield from _iter_name(name)
    else:
        yield name


def add_event_handler(name, value, parser):
    """
    Adds a new event-name argcount parser names relation to the event system core instance.
    
    Parameters
    ----------
    name : `str`
        The name of the event.
    value : `int`
        The amount of parameters what the parser passes the respective event.
    parser : `str` or (`tuple` of `str`)
        The name of events, which might call the respective event.
    """
    parser = tuple(_iter_name(parser))
    
    EVENT_HANDLER_EXPECTED_ARGUMENT_COUNTS[name] = value
    EVENT_HANDLER_NAME_TO_PARSER_NAMES[name] = parser


def get_event_parser_parameter_count(name):
    """
    Returns the amount of parameters, what the events would pass to the respective event.
    
    Parameters
    ----------
    name : `str`
        The event's name.
    
    Returns
    -------
    parameter_count : `int`
        The amount of parameters, what to the respective event would be passed.
    
    Raises
    ------
    LookupError
        There is no event defined with the specific name.
    """
    try:
        parameter_count = EVENT_HANDLER_EXPECTED_ARGUMENT_COUNTS[name]
    except KeyError:
        raise LookupError(f'Invalid Event name: `{name!r}`.') from None
    
    return parameter_count

add_event_handler('error', 3, None,)
add_event_handler('launch', 1, None,)
add_event_handler('shutdown', 1, None,)
add_event_handler('voice_client_ghost', 2, None,)
add_event_handler('voice_client_join', 2, None,)
add_event_handler('voice_client_move', 3, None,)
add_event_handler('voice_client_leave', 3, None,)
add_event_handler('voice_client_update', 3, None,)
add_event_handler('voice_client_shutdown', 1, None,)

add_event_handler('ready', 1, 'READY',)
add_event_handler('client_edit', 2, 'USER_UPDATE',)
add_event_handler('message_create', 2, 'MESSAGE_CREATE',)
add_event_handler('message_delete', 2, ('MESSAGE_DELETE', 'MESSAGE_DELETE_BULK') ,)
add_event_handler('message_edit', 3, 'MESSAGE_UPDATE',)
add_event_handler('embed_update', 3, 'MESSAGE_UPDATE',)
add_event_handler('reaction_add', 2, 'MESSAGE_REACTION_ADD',)
add_event_handler('reaction_clear', 3, 'MESSAGE_REACTION_REMOVE_ALL',)
add_event_handler('reaction_delete', 2, 'MESSAGE_REACTION_REMOVE',)
add_event_handler('reaction_delete_emoji', 4, 'MESSAGE_REACTION_REMOVE_EMOJI',)
add_event_handler('user_edit', 3, 'PRESENCE_UPDATE',)
add_event_handler('user_presence_update', 3, 'PRESENCE_UPDATE',)
add_event_handler('guild_user_edit', 4, 'GUILD_MEMBER_UPDATE',)
add_event_handler('channel_delete', 2, ('CHANNEL_DELETE', 'THREAD_DELETE'),)
add_event_handler('channel_edit', 3, ('CHANNEL_UPDATE', 'THREAD_UPDATE'),)
add_event_handler('channel_create', 2, ('CHANNEL_CREATE', 'THREAD_CREATE'),)
add_event_handler('channel_pin_update', 2, 'CHANNEL_PINS_UPDATE',)
add_event_handler('channel_group_user_add', 3, 'CHANNEL_RECIPIENT_ADD',)
add_event_handler('channel_group_user_delete', 3, 'CHANNEL_RECIPIENT_REMOVE',)
add_event_handler('emoji_create', 2, 'GUILD_EMOJIS_UPDATE',)
add_event_handler('emoji_delete', 2, 'GUILD_EMOJIS_UPDATE',)
add_event_handler('emoji_edit', 3, 'GUILD_EMOJIS_UPDATE',)
add_event_handler('sticker_create', 2, 'GUILD_STICKERS_UPDATE',)
add_event_handler('sticker_delete', 2, 'GUILD_STICKERS_UPDATE',)
add_event_handler('sticker_edit', 3, 'GUILD_STICKERS_UPDATE',)
add_event_handler('guild_user_add', 3, 'GUILD_MEMBER_ADD',)
add_event_handler('guild_user_delete', 4, 'GUILD_MEMBER_REMOVE',)
add_event_handler('guild_join_reject', 3, 'GUILD_JOIN_REQUEST_DELETE',)
add_event_handler('guild_create', 2, 'GUILD_CREATE',)
add_event_handler('guild_edit', 2, 'GUILD_UPDATE',)
add_event_handler('guild_delete', 3, 'GUILD_DELETE',)
add_event_handler('guild_ban_add', 3, 'GUILD_BAN_ADD',)
add_event_handler('guild_ban_delete', 3, 'GUILD_BAN_REMOVE',)
add_event_handler('guild_user_chunk', 2, 'GUILD_MEMBERS_CHUNK',)
add_event_handler('integration_create', 3, 'INTEGRATION_CREATE',)
add_event_handler('integration_delete', 4, 'INTEGRATION_DELETE',)
add_event_handler('integration_edit', 3, 'INTEGRATION_UPDATE',)
add_event_handler('integration_update', 2, 'GUILD_INTEGRATIONS_UPDATE',)
add_event_handler('role_create', 2, 'GUILD_ROLE_CREATE',)
add_event_handler('role_delete', 3, 'GUILD_ROLE_DELETE',)
add_event_handler('role_edit', 3, 'GUILD_ROLE_UPDATE',)
add_event_handler('webhook_update', 2, 'WEBHOOKS_UPDATE',)
add_event_handler('user_voice_join', 2, 'VOICE_STATE_UPDATE',)
add_event_handler('user_voice_leave', 3, 'VOICE_STATE_UPDATE',)
add_event_handler('user_voice_update', 3, 'VOICE_STATE_UPDATE',)
add_event_handler('user_voice_move', 3, 'VOICE_STATE_UPDATE',)
add_event_handler('typing', 4, 'TYPING_START',)
add_event_handler('invite_create', 2, 'INVITE_CREATE',)
add_event_handler('invite_delete', 2, 'INVITE_DELETE',)
add_event_handler('relationship_add', 2, 'RELATIONSHIP_ADD',)
add_event_handler('relationship_change', 3, 'RELATIONSHIP_ADD',)
add_event_handler('relationship_delete', 2, 'RELATIONSHIP_REMOVE',)
add_event_handler('gift_update', 3, 'GIFT_CODE_UPDATE',)
add_event_handler('interaction_create', 2, 'INTERACTION_CREATE',)
add_event_handler('application_command_create', 3, 'APPLICATION_COMMAND_CREATE',)
add_event_handler('application_command_update', 4, 'APPLICATION_COMMAND_UPDATE',)
add_event_handler('application_command_delete', 3, 'APPLICATION_COMMAND_DELETE',)
add_event_handler('application_command_permission_update', 2, 'APPLICATION_COMMAND_PERMISSIONS_UPDATE',)
add_event_handler('stage_create', 2, 'STAGE_INSTANCE_CREATE',)
add_event_handler('stage_edit', 3, 'STAGE_INSTANCE_UPDATE',)
add_event_handler('stage_delete', 2, 'STAGE_INSTANCE_DELETE',)
add_event_handler('thread_user_add', 4, ('THREAD_MEMBER_UPDATE', 'THREAD_MEMBERS_UPDATE'),)
add_event_handler('thread_user_delete', 3, ('THREAD_MEMBER_UPDATE', 'THREAD_MEMBERS_UPDATE'),)
add_event_handler('voice_server_update', 2, 'VOICE_SERVER_UPDATE',)


class ParserSettingOption:
    """
    Contains details about a dispatch event parser
    
    Parameters
    ----------
    intent_shift : `int`
        The event's intent's respective shift.
    name : `str`
        The parser's name(s) also known as the dispatch event's.
    """
    __slots__ = ('intent_shift', 'name')
    def __new__(cls, name):
        """
        Creates new ``ParserSettingOption`` instances from the given name.
        
        This method is a generator.
        
        Yields
        ------
        self : ``ParserSettingOption``
        """
        try:
            intent_shifts = DISPATCH_EVENT_TO_INTENTS[name]
        except KeyError:
            warnings.warn(
                f'Dispatch event parser {name!r} is not registered to any intent. '
                'Will always use optimized parser to dispatch it.',
                RuntimeWarning)
            
            intent_shifts = (INTENT_SHIFT_MISSING_EVENT,)
        
        for intent_shift in intent_shifts:
            self = object.__new__(cls)
            self.name = name
            self.intent_shift = intent_shift
            yield self
    
    def __repr__(self):
        """Returns the parser description's representation."""
        return f'<{self.__class__.__name__} name={self.name!r}, intent_shift={self.intent_shift!r}>'


class ParserSetting:
    """
    Stores the events for each dispatch events.
    
    Each dispatch event calls it corresponding parser, what can be 1 of up to 4 different events depending what is the
    optimal way of parsing that specific event. The called parser depends on the running client's intent values and
    whether they have a handler for the respective event. The parser are changed on change, so do not worry, there are
    no useless checks done every time a dispatch event is received.
    
    Attributes
    ----------
    options : `tuple` of ``ParserSettingOption``
        Options about the dispatch events handled by the parser.
    parser_cal_sc : `function`
        Single client parser what calculates the differences between the previous and the current state and calls
        the client's event.
    parser_cal_mc : `function`
        Multi client parser what calculates the differences between the previous and the current state and calls
        the clients' events.
    parser_opt_sc : `function`
        Single client optimized parser.
    parser_opt_mc : `function`
        Multi client optimized events.
    mention_count : `int`
        How much events of the running clients expect to be called by the respective parser. Used for `opt` - `cal`
        optimizations.
    client_count : `int`
        How much running clients expect the respective parser to call their events. Used in `sc` - `mc` optimizations.
    """
    __slots__ = ('options', 'parser_cal_sc',  'parser_opt_sc', 'parser_cal_mc', 'parser_opt_mc', 'mention_count', 'client_count',)
    def __new__(cls, names, parser_cal_sc, parser_cal_mc, parser_opt_sc, parser_opt_mc):
        """
        Creates a new parser defaults object with the given name and with the given events.
        
        The created parser defaults are stored at the class's `.all` attribute and also the default parser, so
        `parser_opt_sc` is set to the global `PARSERS` variable.
        
        Parameters
        ----------
        name : `tuple` of `str`
            The parser's name also known as the dispatch event's.
        parser_cal_sc : `function`
            Single client parser what calculates the differences between the previous and the current state and calls
            the client's event.
        parser_cal_mc : `function`
            Multi client parser what calculates the differences between the previous and the current state and calls
            the clients' events.
        parser_opt_sc : `function`
            Single client optimized parser.
        parser_opt_mc : `function`
            Multi client optimized events.
        """
        options = tuple(chain.from_iterable(ParserSettingOption(name) for name in names))
        
        self = object.__new__(cls)
        self.options = options
        self.parser_cal_sc = parser_cal_sc
        self.parser_cal_mc = parser_cal_mc
        self.parser_opt_sc = parser_opt_sc
        self.parser_opt_mc = parser_opt_mc
        self.mention_count = 0
        self.client_count = 0
        
        return self
    
    def add_mention(self, client):
        """
        If the client is already registered, mentions the respective parser defaults and optimizes the used events.
        
        Parameters
        ----------
        client : ``Client``
        """
        if client is None:
            return
        
        if client not in REGISTERED_CLIENTS:
            return
        
        for option in self.options:
            intent_shift = option.intent_shift
            if (intent_shift == INTENT_SHIFT_DEFAULT_EVENT):
                break
            
            if (client.intents>>intent_shift)&1:
                break
        
        else:
            return
        
        self.mention_count += 1
        self._recalculate()
    
    def remove_mention(self, client):
        """
        If the client is registered to the parser defaults, removes it's mention from the respective parser defaults
        and optimizes the used events.
        
        Parameters
        ----------
        client : ``Client``
        """
        if client is None:
            return
        
        if client not in REGISTERED_CLIENTS:
            return
        
        for description in self.options:
            intent_shift = description.intent_shift
            if (intent_shift == INTENT_SHIFT_DEFAULT_EVENT):
                break
            
            if (client.intents>>intent_shift)&1:
                break
        
        else:
            return
        
        self.mention_count -= 1
        self._recalculate()
    
    def _recalculate(self):
        """
        Chooses the optimal events for each dispatch event.
        """
        mention_count = self.mention_count
        client_count = self.client_count
        
        if mention_count == 0:
            if client_count < 2:
                parser = self.parser_opt_sc
            else:
                parser = self.parser_opt_mc
        else:
            if client_count < 2:
                parser = self.parser_cal_sc
            else:
                parser = self.parser_cal_mc
        
        for option in self.options:
            PARSERS[option.name] = parser


def register_client(client):
    """
    Registers the given client as a running one. It means it's used events will be registered and their
    change will be handled to optimize the used events.
    
    Parameters
    ----------
    client : ``Client``
    """
    REGISTERED_CLIENTS.add(client)
    
    enabled_parsers = set()
    
    if client.is_bot:
        for parser_name in client.intents.iterate_parser_names():
            enabled_parsers.add(parser_name)
    else:
        for parser_name in PARSER_SETTINGS.keys():
            enabled_parsers.add(parser_name)
    
    for parser_name in enabled_parsers:
        parser_default = PARSER_SETTINGS[parser_name]
        parser_default.client_count +=1
        parser_default._recalculate()
    
    for event_name in EVENT_HANDLER_NAME_TO_PARSER_NAMES.keys():
        event = getattr(client.events, event_name)
        if event is DEFAULT_EVENT_HANDLER:
            continue
        
        parser_names = EVENT_HANDLER_NAME_TO_PARSER_NAMES[event_name]
        for parser_name in parser_names:
            if parser_name not in enabled_parsers:
                continue
            
            parser_default = PARSER_SETTINGS[parser_name]
            parser_default.mention_count +=1
            parser_default._recalculate()
            

def unregister_client(client):
    """
    Unregisters the given client, so it's event be unregistered and their change will not be handled anymore to
    optimize the used events.
    
    Parameters
    ----------
    client : ``Client``
    """
    try:
        REGISTERED_CLIENTS.remove(client)
    except ValueError:
        return
    
    enabled_parsers = set()
    
    if client.is_bot:
        for parser_name in client.intents.iterate_parser_names():
            enabled_parsers.add(parser_name)
    else:
        for parser_name in PARSER_SETTINGS.keys():
            enabled_parsers.add(parser_name)
    
    for parser_name in enabled_parsers:
        parser_default = PARSER_SETTINGS[parser_name]
        parser_default.client_count -= 1
        parser_default._recalculate()
    
    for event_name in EVENT_HANDLER_NAME_TO_PARSER_NAMES.keys():
        event = getattr(client.events, event_name)
        if event is DEFAULT_EVENT_HANDLER:
            continue
        
        parser_names = EVENT_HANDLER_NAME_TO_PARSER_NAMES[event_name]
        for parser_name in parser_names:
            if parser_name not in enabled_parsers:
                continue
            
            parser_default = PARSER_SETTINGS[parser_name]
            parser_default.mention_count -= 1
            parser_default._recalculate()
            continue


def add_parser(name, parser_cal_sc, parser_cal_mc, parser_opt_sc, parser_opt_mc):
    """
    Creates a new parser defaults object with the given name and with the given events.
    
    The created parser defaults are stored at the class's `.all` attribute and also the default parser, so
    `parser_opt_sc` is set to the global `PARSERS` variable.
    
    Parameters
    ----------
    name : `str` or `tuple` of (`str`, ...)
        The parser's name also known as the dispatch event's.
    parser_cal_sc : `function`
        Single client parser what calculates the differences between the previous and the current state and calls
        the client's event.
    parser_cal_mc : `function`
        Multi client parser what calculates the differences between the previous and the current state and calls
        the clients' events.
    parser_opt_sc : `function`
        Single client optimized parser.
    parser_opt_mc : `function`
        Multi client optimized events.
    
    Returns
    -------
    parser_setting : ``ParserSetting``
        The registered parser setting.
    """
    names = tuple(_iter_name(name))
    parser_setting = ParserSetting(names, parser_cal_sc, parser_cal_mc, parser_opt_sc, parser_opt_mc)
    
    for option in parser_setting.options:
        name = option.name
        PARSER_SETTINGS[name] = parser_setting
        PARSERS[name] = parser_opt_sc
    
    return parser_setting

def maybe_ensure_launch(client):
    """
    Calls `client.events.launch` if not yet called.
    
    Parameters
    ----------
    client : ``Client``
        The respective client.
    """
    events = client.events
    if not events._launch_called:
        events._launch_called = True
        
        event_handler = client.events.launch
        if (event_handler is not DEFAULT_EVENT_HANDLER):
            Task(event_handler(client), KOKORO)


@export
def trigger_voice_client_ghost_event(client, voice_state):
    """
    Triggers `Client.events.voice_client_ghost` if set.
    
    Parameters
    ----------
    client : ``Client``
        The respective client instance.
    voice_state : ``VoiceState``
        The client's ghost voice state.
    """
    event_handler = client.events.voice_client_ghost
    if (event_handler is not DEFAULT_EVENT_HANDLER):
        Task(event_handler(client, voice_state), KOKORO)
