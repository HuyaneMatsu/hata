# -*- coding: utf-8 -*-
__all__ = ('AuditLog', 'AuditLogEntry', 'AuditLogEvent', 'AuditLogIterator', 'AuditLogChange', )

from .others import VerificationLevel, ContentFilterLevel, Unknown, now_as_id, id_to_time, MessageNotificationLevel, \
    VoiceRegion, MFA
from .client_core import CHANNELS, USERS, ROLES, MESSAGES
from .permission import Permission
from .color import Color
from .user import User
from .webhook import Webhook
from .role import PermOW
from .integration import Integration
from .guild import SystemChannelFlag
from .bases import Icon

class AuditLogEvent(object):
    """
    Represents the event type of an ``AuditLogEntry``.
    
    Attributes
    ----------
    name : `str`
        The name of audit log event.
    value : `int`
        The Discord side identificator value of the audit log event.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``AuditLogEvent``) items
        Stores the predefined ``AuditLogEvent`` instances. These can be accessed with their `value` as key.
    
    Every predefined audit log event can be accessed as class attribute as well:
    
    +---------------------------+---------------------------+-------+
    | Class attribute name      | name                      | value |
    +===========================+===========================+=======+
    | GUILD_UPDATE              | GUILD_UPDATE              |  1    |
    +---------------------------+---------------------------+-------+
    | CHANNEL_CREATE            | CHANNEL_CREATE            | 10    |
    +---------------------------+---------------------------+-------+
    | CHANNEL_UPDATE            | CHANNEL_UPDATE            | 11    |
    +---------------------------+---------------------------+-------+
    | CHANNEL_DELETE            | CHANNEL_DELETE            | 12    |
    +---------------------------+---------------------------+-------+
    | CHANNEL_OVERWRITE_CREATE  | CHANNEL_OVERWRITE_CREATE  | 13    |
    +---------------------------+---------------------------+-------+
    | CHANNEL_OVERWRITE_UPDATE  | CHANNEL_OVERWRITE_UPDATE  | 14    |
    +---------------------------+---------------------------+-------+
    | CHANNEL_OVERWRITE_DELETE  | CHANNEL_OVERWRITE_DELETE  | 15    |
    +---------------------------+---------------------------+-------+
    | MEMBER_KICK               | MEMBER_KICK               | 20    |
    +---------------------------+---------------------------+-------+
    | MEMBER_PRUNE              | MEMBER_PRUNE              | 21    |
    +---------------------------+---------------------------+-------+
    | MEMBER_BAN_ADD            | MEMBER_BAN_ADD            | 22    |
    +---------------------------+---------------------------+-------+
    | MEMBER_BAN_REMOVE         | MEMBER_BAN_REMOVE         | 23    |
    +---------------------------+---------------------------+-------+
    | MEMBER_UPDATE             | MEMBER_UPDATE             | 24    |
    +---------------------------+---------------------------+-------+
    | MEMBER_ROLE_UPDATE        | MEMBER_ROLE_UPDATE        | 25    |
    +---------------------------+---------------------------+-------+
    | MEMBER_MOVE               | MEMBER_MOVE               | 26    |
    +---------------------------+---------------------------+-------+
    | MEMBER_DISCONNECT         | MEMBER_DISCONNECT         | 27    |
    +---------------------------+---------------------------+-------+
    | BOT_ADD                   | BOT_ADD                   | 28    |
    +---------------------------+---------------------------+-------+
    | ROLE_CREATE               | ROLE_CREATE               | 30    |
    +---------------------------+---------------------------+-------+
    | ROLE_UPDATE               | ROLE_UPDATE               | 31    |
    +---------------------------+---------------------------+-------+
    | ROLE_DELETE               | ROLE_DELETE               | 32    |
    +---------------------------+---------------------------+-------+
    | INVITE_CREATE             | INVITE_CREATE             | 40    |
    +---------------------------+---------------------------+-------+
    | INVITE_UPDATE             | INVITE_UPDATE             | 41    |
    +---------------------------+---------------------------+-------+
    | INVITE_DELETE             | INVITE_DELETE             | 42    |
    +---------------------------+---------------------------+-------+
    | WEBHOOK_CREATE            | WEBHOOK_CREATE            | 50    |
    +---------------------------+---------------------------+-------+
    | WEBHOOK_UPDATE            | WEBHOOK_UPDATE            | 51    |
    +---------------------------+---------------------------+-------+
    | WEBHOOK_DELETE            | WEBHOOK_DELETE            | 52    |
    +---------------------------+---------------------------+-------+
    | EMOJI_CREATE              | EMOJI_CREATE              | 60    |
    +---------------------------+---------------------------+-------+
    | EMOJI_UPDATE              | EMOJI_UPDATE              | 61    |
    +---------------------------+---------------------------+-------+
    | EMOJI_DELETE              | EMOJI_DELETE              | 62    |
    +---------------------------+---------------------------+-------+
    | MESSAGE_DELETE            | MESSAGE_DELETE            | 72    |
    +---------------------------+---------------------------+-------+
    | MESSAGE_BULK_DELETE       | MESSAGE_BULK_DELETE       | 73    |
    +---------------------------+---------------------------+-------+
    | MESSAGE_PIN               | MESSAGE_PIN               | 74    |
    +---------------------------+---------------------------+-------+
    | MESSAGE_UNPIN             | MESSAGE_UNPIN             | 75    |
    +---------------------------+---------------------------+-------+
    | INTEGRATION_CREATE        | INTEGRATION_CREATE        | 80    |
    +---------------------------+---------------------------+-------+
    | INTEGRATION_UPDATE        | INTEGRATION_UPDATE        | 81    |
    +---------------------------+---------------------------+-------+
    | INTEGRATION_DELETE        | INTEGRATION_DELETE        | 82    |
    +---------------------------+---------------------------+-------+
    """
    # class related
    INSTANCES = {}
    
    # object related
    __slots__ = ('name', 'value', )
    
    def __init__(self, value, name):
        """
        Creates an ``AuditLogEvent`` and stores it at the classe's `.INSTANCES` class attribute as well.
        
        Parameters
        ----------
        value : `int`
            The Discord side identificator value of the audit log event.
        name : `str`
            The name of audit log event.
        """
        self.value = value
        self.name = name
        
        self.INSTANCES[value] = self
    
    def __int__(self):
        """Returns the value of the audit log event."""
        return self.value
    
    def __hash__(self):
        """Returns the hash value of the audit log event, what equals to it's value."""
        return self.value
    
    def __str__(self):
        """Returns the name of the audit log event."""
        return self.name
    
    def __repr__(self):
        """Returns the representation of the audit log event."""
        return f'{self.__class__.__name__}(value={self.value}, name={self.name!r})'
    
    # predefined
    GUILD_UPDATE             = NotImplemented
    
    CHANNEL_CREATE           = NotImplemented
    CHANNEL_UPDATE           = NotImplemented
    CHANNEL_DELETE           = NotImplemented
    CHANNEL_OVERWRITE_CREATE = NotImplemented
    CHANNEL_OVERWRITE_UPDATE = NotImplemented
    CHANNEL_OVERWRITE_DELETE = NotImplemented
    
    MEMBER_KICK              = NotImplemented
    MEMBER_PRUNE             = NotImplemented
    MEMBER_BAN_ADD           = NotImplemented
    MEMBER_BAN_REMOVE        = NotImplemented
    MEMBER_UPDATE            = NotImplemented
    MEMBER_ROLE_UPDATE       = NotImplemented
    MEMBER_MOVE              = NotImplemented
    MEMBER_DISCONNECT        = NotImplemented
    BOT_ADD                  = NotImplemented
    
    ROLE_CREATE              = NotImplemented
    ROLE_UPDATE              = NotImplemented
    ROLE_DELETE              = NotImplemented
    
    INVITE_CREATE            = NotImplemented
    INVITE_UPDATE            = NotImplemented
    INVITE_DELETE            = NotImplemented
    
    WEBHOOK_CREATE           = NotImplemented
    WEBHOOK_UPDATE           = NotImplemented
    WEBHOOK_DELETE           = NotImplemented
    
    EMOJI_CREATE             = NotImplemented
    EMOJI_UPDATE             = NotImplemented
    EMOJI_DELETE             = NotImplemented
    
    MESSAGE_DELETE           = NotImplemented
    MESSAGE_BULK_DELETE      = NotImplemented
    MESSAGE_PIN              = NotImplemented
    MESSAGE_UNPIN            = NotImplemented
    
    INTEGRATION_CREATE       = NotImplemented
    INTEGRATION_UPDATE       = NotImplemented
    INTEGRATION_DELETE       = NotImplemented

AuditLogEvent.GUILD_UPDATE             = AuditLogEvent( 1, 'GUILD_UPDATE')

AuditLogEvent.CHANNEL_CREATE           = AuditLogEvent(10, 'CHANNEL_CREATE')
AuditLogEvent.CHANNEL_UPDATE           = AuditLogEvent(11, 'CHANNEL_UPDATE')
AuditLogEvent.CHANNEL_DELETE           = AuditLogEvent(12, 'CHANNEL_DELETE')
AuditLogEvent.CHANNEL_OVERWRITE_CREATE = AuditLogEvent(13, 'CHANNEL_OVERWRITE_CREATE')
AuditLogEvent.CHANNEL_OVERWRITE_UPDATE = AuditLogEvent(14, 'CHANNEL_OVERWRITE_UPDATE')
AuditLogEvent.CHANNEL_OVERWRITE_DELETE = AuditLogEvent(15, 'CHANNEL_OVERWRITE_DELETE')

AuditLogEvent.MEMBER_KICK              = AuditLogEvent(20, 'MEMBER_KICK')
AuditLogEvent.MEMBER_PRUNE             = AuditLogEvent(21, 'MEMBER_PRUNE')
AuditLogEvent.MEMBER_BAN_ADD           = AuditLogEvent(22, 'MEMBER_BAN_ADD')
AuditLogEvent.MEMBER_BAN_REMOVE        = AuditLogEvent(23, 'MEMBER_BAN_REMOVE')
AuditLogEvent.MEMBER_UPDATE            = AuditLogEvent(24, 'MEMBER_UPDATE')
AuditLogEvent.MEMBER_ROLE_UPDATE       = AuditLogEvent(25, 'MEMBER_ROLE_UPDATE')
AuditLogEvent.MEMBER_MOVE              = AuditLogEvent(26, 'MEMBER_MOVE')
AuditLogEvent.MEMBER_DISCONNECT        = AuditLogEvent(27, 'MEMBER_DISCONNECT')
AuditLogEvent.BOT_ADD                  = AuditLogEvent(28, 'MEMBER_ROLE_UPDATE')

AuditLogEvent.ROLE_CREATE              = AuditLogEvent(30, 'ROLE_CREATE')
AuditLogEvent.ROLE_UPDATE              = AuditLogEvent(31, 'ROLE_UPDATE')
AuditLogEvent.ROLE_DELETE              = AuditLogEvent(32, 'ROLE_DELETE')

AuditLogEvent.INVITE_CREATE            = AuditLogEvent(40, 'INVITE_CREATE')
AuditLogEvent.INVITE_UPDATE            = AuditLogEvent(41, 'INVITE_UPDATE')
AuditLogEvent.INVITE_DELETE            = AuditLogEvent(42, 'INVITE_DELETE')

AuditLogEvent.WEBHOOK_CREATE           = AuditLogEvent(50, 'WEBHOOK_CREATE')
AuditLogEvent.WEBHOOK_UPDATE           = AuditLogEvent(51, 'WEBHOOK_UPDATE')
AuditLogEvent.WEBHOOK_DELETE           = AuditLogEvent(52, 'WEBHOOK_DELETE')

AuditLogEvent.EMOJI_CREATE             = AuditLogEvent(60, 'EMOJI_CREATE')
AuditLogEvent.EMOJI_UPDATE             = AuditLogEvent(61, 'EMOJI_UPDATE')
AuditLogEvent.EMOJI_DELETE             = AuditLogEvent(62, 'EMOJI_DELETE')

AuditLogEvent.MESSAGE_DELETE           = AuditLogEvent(72, 'MESSAGE_DELETE')
AuditLogEvent.MESSAGE_BULK_DELETE      = AuditLogEvent(73, 'MESSAGE_BULK_DELETE')
AuditLogEvent.MESSAGE_PIN              = AuditLogEvent(74, 'MESSAGE_PIN')
AuditLogEvent.MESSAGE_UNPIN            = AuditLogEvent(75, 'MESSAGE_UNPIN')

AuditLogEvent.INTEGRATION_CREATE       = AuditLogEvent(80, 'INTEGRATION_CREATE')
AuditLogEvent.INTEGRATION_UPDATE       = AuditLogEvent(81, 'INTEGRATION_UPDATE')
AuditLogEvent.INTEGRATION_DELETE       = AuditLogEvent(82, 'INTEGRATION_DELETE')

class AuditLog(object):
    """
    Whenever an admin action is performed on the API, an audit log entry is added to the respective guild's audit
    logs. This class represents a requested  collections of these entries.
    
    Attributes
    ----------
    guild : ``Guild``
        The audit logs' respective guild.
    entries : `list` of ``AuditLogEntry``
        A list of audit log entries, what the audit log contains.
    users : `dict` of (`int`, (``Client`` or ``User``)) items
        A dictionary, what contains the mentioned users by the audit log's entries. The keys are the `id`-s of the
        users, meanwhile the values are the users themselves.
    webhooks : `dict` of (`int`, ``Webhook``) items
        A dictionary what contains the mentioned webhook by the audit log's entries. The keys are the `id`-s of the
        webhooks, meanwhile the values are the values themselves.
    integrations : `dict` of (`int`, ``Integration``) items
        A dictionary what contains the mentioned integrations by the audit log's entries. The keys are the `id`-s of
        the integrations, meanwhile the values are the integrations themselves.
    """
    __slots__ = ('guild', 'entries', 'users', 'webhooks', 'integrations', )
    def __init__(self, data, guild):
        """
        Creates an ``AuditLog`` instance from the data received from Discord.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data recevied from Discord.
        guild : ``Guild``
            The respective guild of the audit logs.
        """
        self.guild = guild
        
        self.users = users = {}
        try:
            user_datas = data['users']
        except KeyError:
            pass
        else:
            for user_data in user_datas:
                user = User(user_data)
                users[user.id] = user
        
        self.webhooks = webhooks = {}
        try:
            webhook_datas=data['webhook']
        except KeyError:
            pass
        else:
            for webhook_data in webhook_datas:
                webhook = Webhook(webhook_data)
                webhooks[webhook.id] = webhook
        
        self.integrations = integrations = {}
        try:
            integration_datas = data['integrations']
        except KeyError:
            pass
        else:
            for integration_data in integration_datas:
                integration = Integration(integration_data)
                integrations[integration.id] = integration
        
        self.entries = entries = []
        try:
            entry_datas = data['audit_log_entries']
        except KeyError:
            pass
        else:
            for entry_data in entry_datas:
                entries.append(AuditLogEntry(entry_data, self))
    
    def __iter__(self):
        """Iterates over the audit log's entries."""
        return iter(self.entries)
    
    def __reversed__(self):
        """Reversed iterater over the audit log's antries."""
        return reversed(self.entries)
    
    def __len__(self):
        """Returns the amount of entries, what the audit lgo contain."""
        return len(self.entries)
    
    def __getitem__(self,index):
        """Returns the specific audit log entry at the given index."""
        return self.entries.__getitem__(index)
    
    def __repr__(self):
        """Returns the representation of the Audit log."""
        return f'<{self.__class__.__name__} of {self.guild.name}, length={len(self.entries)}>'

class AuditLogIterator(object):
    """
    An async iterator over a guild's audit logs.
    
    Attributes
    ----------
    guild : ``Guild``
        The audit log iterator's respective guild.
    entries : `list` of ``AuditLogEntry``
        A list of the already received audit log entries.
    users : `dict` of (`int`, (``Client`` or ``User``)) items
        A dictionary, what contains the mentioned users by the audit log's entries. The keys are the `id`-s of the
        users, meanwhile the values are the users themselves.
    webhooks : `dict` of (`int`, ``Webhook``) items
        A dictionaryy what contains the mentioned webhook by the audit log's entries. They keys are the `id`-s of the
        webhooks, meanwhile the values are the values themselves.
    integrations : `dict` of (`int`, ``Integration``) items
        A dictionary what contains the mentioned integrations by the audit log's entries. The keys are the `id`-s of
        the integrations, meanwhile the values are the integrations themselves.
    _data : `dict` of (`str`, `Any`) items
        Data to be sent to Discord when requesting an another audit log chunk. Contains some information, which are not
        stored by any attributes of the audit log iterator, these are the filtering `user` and `event` options.
    _index : `int`
        The next audit log entries index to yield.
    client : ``Client``
        The client, who will execute the api requests.
    """
    __slots__ = ('guild',  'entries', 'users', 'webhooks', 'integrations', '_data', '_index', 'client', )
    
    def __init__(self, client, guild, user=None, event=None):
        """
        Creates an audit log iterator with the given arguments.
        
        Parameters
        ----------
        client : ``Client``
            The client, who will execute the api requests.
        guild : ``Guild``
            The guild, what's audit logs will be requested.
        user : ``Client`` or ``User`` object, Optional
            Whether the audit logs should be filtered only to those, which were created by the given user.
        event : ``AuditLogEvent``, Optional
            Whether the audit logs should be filtered only on the given event.
        """
        
        data = {
            'limit' : 100,
            'before': now_as_id(),
                }
        
        if (user is not None):
            data['user_id'] = user.id
        
        if (event is not None):
            data['action_type'] = event.value
        
        self._data = data
        self._index = 0
        self.client = client
        self.guild = guild
        self.entries = []
        self.users = {}
        self.webhooks = {}
        self.integrations = {}
    
    async def load_all(self):
        """
        Loads all not yet loaded audit logs of the audit log iterator's guild.
        """
        entries = self.entries
        client = self.client
        http = client.http
        data = self._data
        
        while True:
            if entries:
                data['before'] = entries[-1].id
            
            log_data = await http.audit_logs(self.guild.id, data)
            
            try:
                self._process_data(log_data)
            except StopAsyncIteration:
                return
            
            if len(entries)%100:
                return
    
    def transform(self):
        """
        Converts the audit log iterator to an audit log object.
        
        Returns
        -------
        audit_log : ``AuiditLog``
        """
        result = object.__new__(AuditLog)
        result.guild = self.guild
        result.entries = self.entries
        result.users = self.users
        result.webhooks = self.webhooks
        result.integrations = self.integrations
        return result
    
    def __aiter__(self):
        """Returns self and resets the `.index`."""
        self._index=0
        return self
    
    async def __anext__(self):
        """Yields the next entry of the audit log iterator."""
        ln = len(self.entries)
        index = self._index
        
        if index < ln:
            self._index +=1
            return self.entries[index]
        
        if index%100:
            raise StopAsyncIteration
        
        data = self._data
        if ln:
            data['before'] = self.entries[ln-1].id
        
        log_data = await self.client.http.audit_logs(self.guild.id, data)
        self._process_data(log_data)
        self._index +=1
        return self.entries[index]

    def __repr__(self):
        """Returns the representation of the audit log iterator."""
        return f'<{self.__class__.__name__} of {self.client.full_name} at {self.guild.name}>'
    
    def _process_data(self, data):
        """
        Processes a batch of audit log data received from Disocrd.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        """
        try:
            entry_datas = data['audit_log_entries']
        except KeyError:
            raise StopAsyncIteration from None
        
        if not entry_datas:
            raise StopAsyncIteration
        
        users = self.users
        try:
            users_data = data['users']
        except KeyError:
            pass
        else:
            for user_data in users_data:
                user = User(user_data)
                users[user.id] = user
        
        webhooks = self.webhooks
        try:
            webhooks_data = data['webhook']
        except KeyError:
            pass
        else:
            for webhook_data in webhooks_data:
                webhook = Webhook(webhook_data)
                webhooks[webhook.id] = webhook
        
        integrations = self.integrations
        try:
            integration_datas = data['integrations']
        except KeyError:
            pass
        else:
            for integration_data in integration_datas:
                integration = Integration(integration_data)
                integrations[integration.id] = integration
        
        entries=self.entries
        for entry_data in entry_datas:
            entries.append(AuditLogEntry(entry_data, self))


def convert_detail_days(key, value, all_):
    return 'days', int(value)

def convert_detail_users_removed(key, value, all_):
    return 'users_removed', int(value)

def convert_detail_channel(key, value, all_):
    channel_id = int(value)
    try:
        channel = CHANNELS[channel_id]
    except KeyError:
        channel = Unknown('Channel',channel_id)
    return 'channel', channel

def convert_detail_message(key, value, all_):
    message_id = int(value)
    try:
        message = MESSAGES[message_id]
    except KeyError:
        message = Unknown('Message',message_id)
    
    return 'message', message

def convert_detail_amount(key, value, all_):
    return 'amount', int(value)

def convert_detail_permow_target(key, value, all_):
    id_=int(value)
    try:
        type_name = all_['type']
    except KeyError:
        # broken data
        return None
    
    if type_name == 'member':
        try:
            target = USERS[id_]
        except KeyError:
            target = Unknown('User', id_)
    
    elif type_name == 'role':
        try:
            target = ROLES[id_]
        except KeyError:
            target = Unknown('Role', id_, all_.get('name', ''))
    else:
        # permow type can be only member and role, so if it is else,
        # the data is broken again
        return None

def convert_detail_permow_processed(key, value, all_):
    return None

DETAIL_CONVERSIONS = {
    'delete_member_days': convert_detail_days,
    'members_removed'   : convert_detail_users_removed,
    'channel_id'        : convert_detail_channel,
    'message_id'        : convert_detail_message,
    'count'             : convert_detail_amount,
    'id'                : convert_detail_permow_target,
    'type'              : convert_detail_permow_processed,
    'role_name'         : convert_detail_permow_processed,
        }

del convert_detail_days
del convert_detail_users_removed
del convert_detail_channel
del convert_detail_message
del convert_detail_amount
del convert_detail_permow_target
del convert_detail_permow_processed

def DETAIL_CONVERTER_DEFAULT(key, value, all_):
    return key, value


def convert_guild(entry, parent, target_id):
    return parent.guild

def convert_channel(entry, parent, target_id):
    if target_id is None:
        target = None
    else:
        target_id = int(target_id)
        try:
            target = parent.guild.channels[target_id]
        except KeyError:
            target = Unknown('Channel', target_id)
    
    return target

def convert_user(entry, parent, target_id):
    # target_id can be None for any reason
    if target_id is None:
        target = None
    else:
        target_id = int(target_id)
        try:
            target = parent.users[target_id]
        except KeyError:
            target = Unknown('User', target_id)
    
    return target

def convert_role(entry, parent, target_id):
    if target_id is None:
        target = None
    else:
        target = int(target_id)
        try:
            target = parent.guild.roles[target_id]
        except KeyError:
            target = Unknown('Role', target_id)
    
    return target

def convert_invite(entry, parent, target_id):
    #every other data is at #change
    for change in entry.changes:
        if change.attr!='code':
            continue
        
        if entry.type is AuditLogEvent.INVITE_DELETE:
            code = change.before
        else:
            code = change.after
        break
    
    else:
        code = '' #malformed ?
    
    return Unknown('Invite', code)
    
def convert_webhook(entry, parent, target_id):
    if target_id is None:
        target = None
    else:
        target_id = int(target_id)
        try:
            target = parent.webhooks[target_id]
        except KeyError:
            target = Unknown('Webhook', target_id)
    
    return target

def convert_emoji(entry, parent, target_id):
    if target_id is None:
        target = None
    else:
        target_id = int(target_id)
        try:
            target = parent.guild.emojis[target_id]
        except KeyError:
            target = Unknown('Emoji', target_id)
    
    return target

def convert_message(entry, parent, target_id):
    if target_id is None:
        target = None
    else:
        target_id = int(target_id)
        try:
            target = MESSAGES[target_id]
        except KeyError:
            target = Unknown('Message', target_id)
    
    return target

def convert_integration(entry, parent,target_id):
    if target_id is None:
        target = None
    else:
        target_id = int(target_id)
        try:
            target = parent.integrations[target_id]
        except KeyError:
            target = Unknown('Integration', target_id)
    
    return target

CONVERSIONS = (
    convert_guild,
    convert_channel,
    convert_user,
    convert_role,
    convert_invite,
    convert_webhook,
    convert_emoji,
    convert_message,
    convert_integration,
        )

del convert_guild
del convert_channel
del convert_user
del convert_role
del convert_invite
del convert_webhook
del convert_emoji
del convert_message
del convert_integration


class AuditLogEntry(object):
    """
    Represents an entry of an ``AuditLog``.
    
    Attrbiutes
    ----------
    changes : `list` of ``AuditLogChange``
        The changes of the entry.
    details : `None` or `dict` of (`str`, `Any`) items
        Additional information for a specific action types.
    id : `int`
        The unique identificator number of the entry.
    reason : `None` or `str`
        The reason provided with the logged action.
    target : `None`, ``Guild``,  ``ChannelGuildBase`` instance, ``User``, ``Client``, ``Role``, ``Webhook``,
            ``Emoji``, ``Message``, ``Integration``, ``Unknown``
        The target entity of the logged action. If the entity is not found, it will be set as an ``Unknown`` instance.
        It can also happen, that target entity is not provided, then target will be set as `None`.
    type : ``AuditLogEvent``
        The event type of the logged action.
    user : `None`, ``Client``, ``User``
        The user, who executed the logged action. If no user is provided then can be `None` as well.
    """
    __slots__ = ('changes', 'details', 'id', 'reason', 'target', 'type', 'user',)
    def __init__(self, data, parent):
        """
        Creates an audit log entry, from entry data sent isnide of an ``AuditLog``'s data and from the audit itself.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data recevied from Discord.
        parent : ``AuditLog`` or ``AuditLogIterator``
            The parent of the entry, what contains the respective guild, the inclued users, webhooks and the
            integrations to work with.
        """
        self.id = int(data['id'])
        self.type = AuditLogEvent.INSTANCES[int(data['action_type'])]
        
        options = data.get('options')
        if (options is None):
            details = None
        else:
            details = {}
            for key,value in options.items():
                result=DETAIL_CONVERSIONS.get(key,DETAIL_CONVERTER_DEFAULT)(key,value,options)
                if result is None:
                    continue
                
                key, value=result
                details[key]=value
            
            if not details:
                details = None
        
        self.details=details
        
        user_id = data.get('user_id')
        if user_id is None:
            user = None
        else:
            user = parent.users.get(int(user_id))
        self.user = user
        
        self.reason = data.get('reason')
        
        change_datas = data.get('changes')
        if (change_datas is None):
            changes = None
        else:
            changes = []
            for change_data in change_datas:
                try:
                    key = change_data['key']
                except KeyError: #malformed?
                    continue
                
                change = TRANSFORMERS.get(key, transform_nothing)(key, change_data)
                if (change is not None):
                    changes.append(change)
            
            if not changes:
                changes = None
        
        self.changes = changes
        
        self.target = CONVERSIONS[self.type.value//10](self, parent, data.get('target_id', None))
    
    @property
    def created_at(self):
        """
        When the audit log entry was created.
        
        Returns
        -------
        created_at : `datetime`
        """
        return id_to_time(self.id)
    
    def __repr__(self):
        """Returns the representation of the audit log entry."""
        result = [
            '<',self.__class__.__name__,
            ' id=',repr(self.id),
            ', type=',self.type.name,
                ]
        
        result.append(', user=')
        user = self.user
        if user is None:
            user_repr = 'None'
        else:
            user_repr = user.full_name
        result.append(user_repr)
        
        result.append(', target=')
        result.append(repr(self.target))
        
        result.append(', change count=')
        changes = self.changes
        if changes is None:
            change_amount_repr = '0'
        else:
            change_amount_repr = repr(len(self.changes))
        result.append(change_amount_repr)
        
        reason = self.reason
        if reason is not None:
            result.append(', reason=')
            # use repr to escape special inserted characters
            result.append(repr(reason))
        
        details = self.details
        if details is not None:
            result.append(', details=')
            result.append(repr(details))
        
        result.append('>')
        
        return ''.join(result)
    
def PermOW_from_logs(data):
    self = object.__new__(PermOW)
    id_ = int(data['id'])
    if data['type'] == 'role':
        try:
            target = ROLES[id_]
        except KeyError:
            target = Unknown('Role', id_)
    else:
        try:
            target = USERS[id_]
        except KeyError:
            target = Unknown('User', id_)
    
    self.target = target
    self.allow = data['allow']
    self.deny = data['deny']

    return self

def transform_nothing(name, data):
    change = AuditLogChange()
    change.attr = name
    change.before = data.get('old_value')
    change.after = data.get('new_value')
    return change

def transform_deprecated(name, data):
    return None

def tranfrom_icon(name, data):
    change = AuditLogChange()
    if name == 'splash_hash':
        name = 'invite_splash'
    else:
        name = name[:-5]
    change.attr = name
    
    change.before = Icon.from_base16_hash(data.get('old_value'))
    
    change.after = Icon.from_base16_hash(data.get('new_value'))
    
    return change

def transform_bool__separated(name, data):
    change = AuditLogChange()
    change.attr = 'separated'
    change.before = data.get('old_value')
    change.after = data.get('new_value')
    return change

def transform_channel(name, data):
    change = AuditLogChange()
    change.attr = name[:-3]
    
    value = data.get('old_value')
    if value is None:
        change.before=None
    else:
        value = int(value)
        try:
            before = CHANNELS[value]
        except KeyError:
            before = Unknown('Channel', value)
        change.before = before
    
    value = data.get('new_value')
    if value is None:
        change.after = None
    else:
        value = int(value)
        try:
            after = CHANNELS[value]
        except KeyError:
            after = Unknown('Channel', value)
        change.after = after
    
    return change

def transform_color(name, data):
    change = AuditLogChange()
    change.attr = 'color'
    value = data.get('old_value')
    change.before = None if value is None else Color(value)
    value = data.get('new_value')
    change.after = None if value is None else Color(value)
    return change

def transform_content_filter(name, data):
    change = AuditLogChange()
    change.attr = 'content_filter'
    value = data.get('old_value')
    change.before = None if value is None else ContentFilterLevel.INSTANCES[value]
    value = data.get('new_value')
    change.after = None if value is None else ContentFilterLevel.INSTANCES[value]
    return change

def transform_int__days(name, data):
    change = AuditLogChange()
    change.attr = 'days'
    change.before = data.get('old_value')
    change.after = data.get('new_value')
    return change

def transform_int__slowmode(name, data):
    change = AuditLogChange()
    change.attr = 'slowmode'
    change.before = data.get('old_value')
    change.after = data.get('new_value')
    return change

def transform_message_notification(name, data):
    change  =AuditLogChange()
    change.attr = 'message_notification'
    before = data.get('old_value')
    change.before = None if before is None else MessageNotificationLevel.INSTANCES[before]
    after = data.get('new_value')
    change.after = None if before is None else MessageNotificationLevel.INSTANCES[after]
    return change

def transform_mfa(name, data):
    change = AuditLogChange()
    change.attr = 'mfa'
    before = data.get('old_value')
    change.before = None if before is None else MFA.INSTANCES[before]
    after = data.get('new_value')
    change.after = None if before is None else MFA.INSTANCES[after]
    return change

def transform_overwrites(name, data):
    change = AuditLogChange()
    change.attr = 'overwrites'
    value = data.get('old_value')
    change.before = None if value is None else [PermOW_from_logs(ow_data) for ow_data in value]
    value = data.get('new_value')
    change.after = None if value is None else [PermOW_from_logs(ow_data) for ow_data in value]
    return change

def transform_permission(name, data):
    change = AuditLogChange()
    
    if name.endswith('_new'):
        name = name[:-4]
    
    change.attr = name
    value = data.get('old_value')
    change.before = None if value is None else Permission(value)
    value = data.get('new_value')
    change.after = None if value is None else Permission(value)
    return change

def transform_region(name, data):
    change = AuditLogChange()
    change.attr = 'region'
    before = data.get('old_value')
    change.before = None if before is None else VoiceRegion.get(before)
    after = data.get('new_value')
    change.after = None if before is None else VoiceRegion.get(after)
    return change

def transform_role(name, data):
    change = AuditLogChange()
    change.attr = 'role'
    roles = []
    if name == '$add':
        before = None
        after = roles
    else:
        before = roles
        after = None
    
    change.before = before
    change.after = after
    
    for element in data['new_value']:
        role_id = int(element['id'])
        try:
            role = ROLES[role_id]
        except KeyError:
            role = Unknown('Role', role_id, element['name'])
        roles.append(role)

    return change

def transform_snowfalke(name, data):
    change = AuditLogChange()
    change.attr = name
    value = data.get('old_value')
    change.before = None if value is None else int(value)
    value = data.get('new_value')
    change.after = None if value is None else int(value)
    return change

def transform_str__vanity_code(name, data):
    change = AuditLogChange()
    change.attr = 'vanity_code'
    change.before = data.get('old_value')
    change.after = data.get('new_value')
    return change

def transform_system_channel_flags(name, data):
    change = AuditLogChange()
    change.attr = 'system_channel_flags'
    before = data.get('old_value')
    change.before = None if before is None else SystemChannelFlag(before)
    after = data.get('new_value')
    change.after = None if before is None else SystemChannelFlag(after)
    return change

def transform_type(name, data):
    # if we talk about permission overwrite, type can be `str` too,
    # what we ignore
    before = data.get('old_value')
    if type(before) is str:
        return
    
    after = data.get('new_value')
    if type(after) is str:
        return
    
    change = AuditLogChange()
    change.attr = 'type'
    change.before = before
    change.after = after
    return change

def transform_user(name, data):
    change = AuditLogChange()
    change.attr = name[:-3]
    value = data.get('old_value')
    if value is None:
        before = None
    else:
        value = int(value)
        try:
            before = USERS[value]
        except KeyError:
            before = Unknown('User', value)
    change.before = before
    
    value = data.get('new_value')
    if value is None:
        after = None
    else:
        value = int(value)
        try:
            after = USERS[value]
        except KeyError:
            after = Unknown('User', value)
    change.after = after
    
    return change

def transform_verification_level(name, data):
    change = AuditLogChange()
    change.attr = 'verification_level'
    value = data.get('old_value')
    change.before = None if value is None else VerificationLevel.value[value]
    value = data.get('new_value')
    change.after = None if value is None else VerificationLevel.value[value]
    return change

TRANSFORMERS = {
    '$add'                  : transform_role,
    '$remove'               : transform_role,
    'account_id'            : transform_snowfalke,
    'afk_channel_id'        : transform_channel,
    'allow'                 : transform_deprecated,
    'allow_new'             : transform_permission,
    'application_id'        : transform_snowfalke,
    'avatar_hash'           : tranfrom_icon,
    'banner_hash'           : tranfrom_icon,
    # bitrate (int)
    'channel_id'            : transform_channel,
    # code (str)
    'color'                 : transform_color,
    # deaf (bool)
    # description (None or str)
    'default_message_notifications':transform_message_notification,
    'deny'                  : transform_deprecated,
    'deny_new'              : transform_permission,
    'discovery_splash_hash' : tranfrom_icon,
    # enable_emoticons (bool)
    # expire_behavior (int)
    # expire_grace_period (int)
    'explicit_content_filter':transform_content_filter,
    'hoist'                 : transform_bool__separated,
    'icon_hash'             : tranfrom_icon,
    'id'                    : transform_snowfalke,
    'inviter_id'            : transform_user,
    # mentionable (bool)
    # max_age (int)
    # max_uses (int)
    'mfa_level'             : transform_mfa,
    # mute (mute)
    # name (str)
    # nick (None or str)
    # nsfw (bool)
    'owner_id'              : transform_user,
    # position (int)
    'prune_delete_days'     : transform_int__days,
    'permission_overwrites' : transform_overwrites,
    'permissions'           : transform_deprecated,
    'permissions_new'       : transform_permission,
    'public_updates_channel_id' : transform_channel,
    'rate_limit_per_user'   : transform_int__slowmode,
    'region'                : transform_region,
    'rules_channel_id'      : transform_channel,
    'splash_hash'           : tranfrom_icon,
    'system_channel_id'     : transform_channel,
    'system_channel_flags'  : transform_system_channel_flags,
    # temporary (bool)
    # topic (str)
    'type'                  : transform_type,
    # uses (int)
    'vanity_url_code'       : transform_str__vanity_code,
    'verification_level'    : transform_verification_level,
    'widget_channel_id'     : transform_channel,
    # widget_enabled (bool)
        }

del transform_deprecated
del tranfrom_icon
del transform_bool__separated
del transform_channel
del transform_color
del transform_content_filter
del transform_int__days
del transform_int__slowmode
del transform_message_notification
del transform_mfa
del transform_overwrites
del transform_permission
del transform_region
del transform_role
del transform_snowfalke
del transform_str__vanity_code
del transform_system_channel_flags
del transform_type
del transform_user
del transform_verification_level


class AuditLogChange(object):
    """
    A change of an ``AuditLogEntry``.
    
    Attributes
    ----------
    attr : `str`
        The name of the attribute, what changed of the target entity.
    before : `Any`
        The changed attribute's original value. Defaults to `None`.
    after : `Any`
        The changed attribute's new value. Defaults to `None`.
    
    Notes
    -----
    The value of `before` and `after` depenind on the value of `attr`. These are:
    
    +---------------------------+-------------------------------------------+
    | attr                      | before / after                            |
    +===========================+===========================================+
    | account_id                | `None` or `int`                           |
    +---------------------------+-------------------------------------------+
    | afk_channel               | `None` or ``ChannelVoice``                |
    +---------------------------+-------------------------------------------+
    | allow                     | `None` or ``Permission``                  |
    +---------------------------+-------------------------------------------+
    | application_id            | `None` or `int`                           |
    +---------------------------+-------------------------------------------+
    | avatar                    | `None` or ``Icon``                        |
    +---------------------------+-------------------------------------------+
    | bannner                   | `None` or ``Icon``                        |
    +---------------------------+-------------------------------------------+
    | bitrate                   | `None` or `int`                           |
    +---------------------------+-------------------------------------------+
    | channel                   | `None` or ``ChannelGuildBase`` instance   |
    +---------------------------+-------------------------------------------+
    | code                      | `None` or `str`                           |
    +---------------------------+-------------------------------------------+
    | color                     | `None` or ``Color``                       |
    +---------------------------+-------------------------------------------+
    | content_filter            | `None` or ``ContentFilterLevel``          |
    +---------------------------+-------------------------------------------+
    | days                      | `None` or `int`                           |
    +---------------------------+-------------------------------------------+
    | deaf                      | `None` or `bool`                          |
    +---------------------------+-------------------------------------------+
    | description               | `None` or `str`                           |
    +---------------------------+-------------------------------------------+
    | deny                      | `None` or ``Permission``                  |
    +---------------------------+-------------------------------------------+
    | discovery_splash          | `None` or ``Icon``                        |
    +---------------------------+-------------------------------------------+
    | enable_emoticons          | `None` or `bool`                          |
    +---------------------------+-------------------------------------------+
    | expire_behavior           | `None` or `int`                           |
    +---------------------------+-------------------------------------------+
    | expire_grace_period       | `None` or `int`                           |
    +---------------------------+-------------------------------------------+
    | icon                      | `None` or ``Icon``                        |
    +---------------------------+-------------------------------------------+
    | id                        | `None` or `int`                           |
    +---------------------------+-------------------------------------------+
    | invite_splash             | `None` or ``Icon``                        |
    +---------------------------+-------------------------------------------+
    | inviter                   | `None`, ``User`` or ``Client``            |
    +---------------------------+-------------------------------------------+
    | mentionable               | `None` or `bool`                          |
    +---------------------------+-------------------------------------------+
    | max_age                   | `None` or `int`                           |
    +---------------------------+-------------------------------------------+
    | max_uses                  | `None` or `int`                           |
    +---------------------------+-------------------------------------------+
    | message_notification      | `None` or ``MessageNotificationLevel``    |
    +---------------------------+-------------------------------------------+
    | mfa                       | `None` or ``MFA``                         |
    +---------------------------+-------------------------------------------+
    | mute                      | `None` or `bool`                          |
    +---------------------------+-------------------------------------------+
    | name                      | `None` or `str`                           |
    +---------------------------+-------------------------------------------+
    | nick                      | `None` or `str`                           |
    +---------------------------+-------------------------------------------+
    | nsfw                      | `None` or `bool`                          |
    +---------------------------+-------------------------------------------+
    | owner                     | `None`, ``User`` or ``Client``            |
    +---------------------------+-------------------------------------------+
    | position                  | `None` or `int`                           |
    +---------------------------+-------------------------------------------+
    | public_updates_channel    | `None` or ``ChannelText``                 |
    +---------------------------+-------------------------------------------+
    | overwrites                | `None` or `list` of ``PermOW``            |
    +---------------------------+-------------------------------------------+
    | permissions               | `None` or ``Permission``                  |
    +---------------------------+-------------------------------------------+
    | region                    | `None` or ``VoiceRegion``                 |
    +---------------------------+-------------------------------------------+
    | role                      | `None` or `list` of ``Role``              |
    +---------------------------+-------------------------------------------+
    | rules_channel             | `None` or ``ChannelText``                 |
    +---------------------------+-------------------------------------------+
    | separated                 | `None` or `bool`                          |
    +---------------------------+-------------------------------------------+
    | slowmode                  | `None` or `int`                           |
    +---------------------------+-------------------------------------------+
    | system_channel            | `None` or ``ChannelText``                 |
    +---------------------------+-------------------------------------------+
    | system_channel_flags      | `None` or ``SystemChannelFlag``           |
    +---------------------------+-------------------------------------------+
    | temporary                 | `None` or `bool`                          |
    +---------------------------+-------------------------------------------+
    | topic                     | `None` or `str`                           |
    +---------------------------+-------------------------------------------+
    | type                      | `None` or `int`                           |
    +---------------------------+-------------------------------------------+
    | uses                      | `None` or `int`                           |
    +---------------------------+-------------------------------------------+
    | vanity_code               | `None` or `str`                           |
    +---------------------------+-------------------------------------------+
    | verification_level        | `None` or ``VerificationLevel``           |
    +---------------------------+-------------------------------------------+
    | widget_channel            | `None` or ``ChannelText``                 |
    +---------------------------+-------------------------------------------+
    | widget_enabled            | `None` or `bool`                          |
    +---------------------------+-------------------------------------------+
    """
    __slots__ = ('attr', 'before', 'after', )
    
    def __repr__(self):
        """Returns the representation of the audit log change."""
        return f'{self.__class__.__name__}(attr={self.attr!r}, before={self.before!r}, after={self.after!r})'
