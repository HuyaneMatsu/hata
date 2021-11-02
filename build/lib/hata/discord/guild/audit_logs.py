__all__ = ('AuditLog', 'AuditLogEntry', 'AuditLogIterator', 'AuditLogChange', )

import warnings

from ...env import API_VERSION

from ..utils import Unknown, now_as_id, id_to_datetime
from ..core import CHANNELS, USERS, ROLES, MESSAGES, SCHEDULED_EVENTS
from ..permission import Permission
from ..color import Color
from ..user import User, ClientUserBase
from ..webhook import Webhook
from ..permission import PermissionOverwrite
from ..integration import Integration
from ..bases import Icon, maybe_snowflake
from ..channel import VideoQualityMode, ChannelThread
from ..scheduled_event import ScheduledEventStatus, ScheduledEventEntityType, PrivacyLevel
from ..emoji import create_unicode_emoji

from .utils import create_partial_guild_from_id
from .guild import SystemChannelFlag, Guild
from .preinstanced import AuditLogEvent, VerificationLevel, ContentFilterLevel, MessageNotificationLevel, VoiceRegion, \
    MFA


class AuditLog:
    """
    Whenever an admin action is performed on the API, an audit log entry is added to the respective guild's audit
    logs. This class represents a requested  collections of these entries.
    
    Attributes
    ----------
    entries : `list` of ``AuditLogEntry``
        A list of audit log entries, what the audit log contains.
    guild : ``Guild``
        The audit logs' respective guild.
    integrations : `dict` of (`int`, ``Integration``) items
        A dictionary what contains the mentioned integrations by the audit log's entries. The keys are the `id`-s of
        the integrations, meanwhile the values are the integrations themselves.
    threads : `dict` of (`int`, ``ChannelThread``) items
        A dictionary containing the mentioned threads inside of the audit logs.
    users : `dict` of (`int`, ``ClientUserBase``) items
        A dictionary, what contains the mentioned users by the audit log's entries. The keys are the `id`-s of the
        users, meanwhile the values are the users themselves.
    webhooks : `dict` of (`int`, ``Webhook``) items
        A dictionary what contains the mentioned webhook by the audit log's entries. The keys are the `id`-s of the
        webhooks, meanwhile the values are the values themselves.
    """
    __slots__ = ('entries', 'guild', 'integrations', 'threads', 'users', 'webhooks')
    def __init__(self, data, guild):
        """
        Creates an ``AuditLog`` instance from the data received from Discord.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data received from Discord.
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
            webhook_datas = data['webhook']
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
        
        self.threads = threads = {}
        try:
            thread_datas = data['threads']
        except KeyError:
            pass
        else:
            for thread_data in thread_datas:
                thread = ChannelThread(thread_data, None, guild.id)
                threads[thread.id] = thread
        
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
        """Reversed iterator over the audit log's entries."""
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


class AuditLogIterator:
    """
    An async iterator over a guild's audit logs.
    
    Attributes
    ----------
    _data : `dict` of (`str`, `Any`) items
        Data to be sent to Discord when requesting an another audit log chunk. Contains some information, which are not
        stored by any attributes of the audit log iterator, these are the filtering `user` and `event` options.
    _index : `int`
        The next audit log entries index to yield.
    client : ``Client``
        The client, who will execute the api requests.
    entries : `list` of ``AuditLogEntry``
        A list of the already received audit log entries.
    guild : ``Guild``
        The audit log iterator's respective guild.
    integrations : `dict` of (`int`, ``Integration``) items
        A dictionary what contains the mentioned integrations by the audit log's entries. The keys are the `id`-s of
        the integrations, meanwhile the values are the integrations themselves.
    threads : `dict` of (`int`, ``ChannelThread``) items
        A dictionary containing the mentioned threads inside of the audit logs.
    users : `dict` of (`int`, ``ClientUserBase`` items
        A dictionary, what contains the mentioned users by the audit log's entries. The keys are the `id`-s of the
        users, meanwhile the values are the users themselves.
    webhooks : `dict` of (`int`, ``Webhook``) items
        A dictionary what contains the mentioned webhook by the audit log's entries. They keys are the `id`-s of the
        webhooks, meanwhile the values are the values themselves.
    """
    __slots__ = ('_data', '_index', 'client', 'entries', 'guild', 'integrations', 'threads', 'users', 'webhooks')
    
    async def __new__(cls, client, guild, user=None, event=None):
        """
        Creates an audit log iterator with the given parameters.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client, who will execute the api requests.
        guild : ``Guild`` or `int` instance
            The guild, what's audit logs will be requested.
        user : `None`, ``ClientUserBase`` or `int` instance, Optional
            Whether the audit logs should be filtered only to those, which were created by the given user.
        event : `None`, ``AuditLogEvent`` or `int` instance, Optional
            Whether the audit logs should be filtered only on the given event.
        
        Raises
        ------
        TypeError
            - If `guild` was not given neither as ``Guild``, nor as `int` instance.
            - If `user` was not given neither as `None`, ``ClientUserBase`` nor as `int` instance.
            - If `event` as not not given neither as `None`, ``AuditLogEvent`` nor as `int` instance.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        data = {
            'limit': 100,
            'before': now_as_id(),
        }
        
        if isinstance(guild, Guild):
            guild_id = guild.id
        else:
            guild_id = maybe_snowflake(guild)
            if guild_id is None:
                raise TypeError(f'`guild_or_discovery` can be `{Guild.__name__}` or `int` instance, got '
                    f'{guild.__class__.__name__}.')
            
            guild = None
        
        if (user is not None):
            if isinstance(user, ClientUserBase):
                user_id = user.id
            
            else:
                user_id = maybe_snowflake(user)
                if user_id is None:
                    raise TypeError(f'`user` can be given as `{ClientUserBase.__name__}` or `int` instance, '
                        f'got {user.__class__.__name__}.')
            
            data['user_id'] = user_id
        
        if (event is not None):
            if isinstance(event, AuditLogEvent):
                event_value = event.value
            elif isinstance(event, int):
                event_value = event
            else:
                raise TypeError(f'`event` can be given as `None`, `{AuditLogEvent.__name__}` or `int` instance, got '
                    f'{event.__class__.__name__}.')
            
            data['action_type'] = event_value
        
        if guild is None:
            log_data = await client.http.audit_log_get_chunk(guild_id, data)
            if guild is None:
                guild = create_partial_guild_from_id(guild_id)
        else:
            log_data = None
        
        self = object.__new__(cls)
        self._data = data
        self._index = 0
        self.client = client
        self.guild = guild
        self.entries = []
        self.users = {}
        self.webhooks = {}
        self.integrations = {}
        self.threads = {}
        
        if (log_data is not None):
            self._process_data(log_data)
        
        return self
    
    
    async def load_all(self):
        """
        Loads all not yet loaded audit logs of the audit log iterator's guild.
        
        This method is a coroutine.
        """
        entries = self.entries
        client = self.client
        http = client.http
        data = self._data
        
        while True:
            if entries:
                data['before'] = entries[-1].id
            
            log_data = await http.audit_log_get_chunk(self.guild.id, data)
            
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
        audit_log : ``AuditLog``
        """
        result = object.__new__(AuditLog)
        result.guild = self.guild
        result.entries = self.entries
        result.users = self.users
        result.webhooks = self.webhooks
        result.integrations = self.integrations
        result.threads = self.threads
        return result
    
    def __aiter__(self):
        """Returns self and resets the `.index`."""
        self._index = 0
        return self
    
    async def __anext__(self):
        """
        Yields the next entry of the audit log iterator.
        
        This method is a coroutine.
        """
        ln = len(self.entries)
        index = self._index
        
        if index < ln:
            self._index += 1
            return self.entries[index]
        
        if index%100:
            raise StopAsyncIteration
        
        data = self._data
        if ln:
            data['before'] = self.entries[ln-1].id
        
        log_data = await self.client.http.audit_log_get_chunk(self.guild.id, data)
        self._process_data(log_data)
        self._index += 1
        return self.entries[index]

    def __repr__(self):
        """Returns the representation of the audit log iterator."""
        return f'<{self.__class__.__name__} of {self.client.full_name} at {self.guild.name}>'
    
    def _process_data(self, data):
        """
        Processes a batch of audit log data received from Discord.
        
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
        
        
        try:
            users_data = data['users']
        except KeyError:
            pass
        else:
            users = self.users
            
            for user_data in users_data:
                user = User(user_data)
                users[user.id] = user
        
        
        try:
            webhooks_data = data['webhook']
        except KeyError:
            pass
        else:
            webhooks = self.webhooks
            
            for webhook_data in webhooks_data:
                webhook = Webhook(webhook_data)
                webhooks[webhook.id] = webhook
        
        
        try:
            integration_datas = data['integrations']
        except KeyError:
            pass
        else:
            integrations = self.integrations
            
            for integration_data in integration_datas:
                integration = Integration(integration_data)
                integrations[integration.id] = integration
        
        
        try:
            thread_datas = data['threads']
        except KeyError:
            pass
        else:
            threads = self.threads
            
            for thread_data in thread_datas:
                thread = ChannelThread(thread_data, None, self.guild.id)
                threads[thread.id] = thread
        
        entries = self.entries
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
        channel = Unknown('Channel', channel_id)
    return 'channel', channel


def convert_detail_message(key, value, all_):
    message_id = int(value)
    try:
        message = MESSAGES[message_id]
    except KeyError:
        message = Unknown('Message', message_id)
    
    return 'message', message


def convert_detail_amount(key, value, all_):
    return 'amount', int(value)


def convert_detail_permission_overwrite_target(key, value, all_):
    id_ = int(value)
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
        # permission_overwrite type can be only member and role, so if it is else,
        # the data is broken again
        return None
    
    return 'target', target

def convert_detail_permission_overwrite_processed(key, value, all_):
    return None

DETAIL_CONVERSIONS = {
    'delete_member_days': convert_detail_days,
    'members_removed': convert_detail_users_removed,
    'channel_id': convert_detail_channel,
    'message_id': convert_detail_message,
    'count': convert_detail_amount,
    'id': convert_detail_permission_overwrite_target,
    'type': convert_detail_permission_overwrite_processed,
    'role_name': convert_detail_permission_overwrite_processed,
}

del convert_detail_days
del convert_detail_users_removed
del convert_detail_channel
del convert_detail_message
del convert_detail_amount
del convert_detail_permission_overwrite_target
del convert_detail_permission_overwrite_processed


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
        target_id = int(target_id)
        try:
            target = parent.guild.roles[target_id]
        except KeyError:
            target = Unknown('Role', target_id)
    
    return target


def convert_invite(entry, parent, target_id):
    #every other data is at #change
    for change in entry.changes:
        if change.attribute_name != 'code':
            continue
        
        if entry.type is AuditLogEvent.invite_delete:
            code = change.before
        else:
            code = change.after
        break
    
    else:
        code = '' # malformed ?
    
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


def convert_integration(entry, parent, target_id):
    if target_id is None:
        target = None
    else:
        target_id = int(target_id)
        try:
            target = parent.integrations[target_id]
        except KeyError:
            target = Unknown('Integration', target_id)
    
    return target


def convert_sticker(entry, parent, target_id):
    if target_id is None:
        target = None
    else:
        target_id = int(target_id)
        try:
            target = parent.guild.stickers[target_id]
        except KeyError:
            target = Unknown('Sticker', target_id)
    
    return target


def convert_scheduled_event(entry, parent, target_id):
    if target_id is None:
        target = None
    else:
        target_id = int(target_id)
        try:
            target = SCHEDULED_EVENTS[target_id]
        except KeyError:
            target = Unknown('ScheduledEvent', target_id)
    
    return target


def convert_thread(entry, parent, target_id):
    if target_id is None:
        target = None
    else:
        target_id = int(target_id)
        try:
            target = parent.threads[target_id]
        except KeyError:
            target = Unknown('ChannelThread', target_id)
    
    return target


CONVERSIONS = {
    0: convert_guild,
    1: convert_channel,
    2: convert_user,
    3: convert_role,
    4: convert_invite,
    5: convert_webhook,
    6: convert_emoji,
    7: convert_message,
    8: convert_integration,
    9: convert_sticker,
    10: convert_scheduled_event,
    11: convert_thread,
}

del convert_guild
del convert_channel
del convert_user
del convert_role
del convert_invite
del convert_webhook
del convert_emoji
del convert_message
del convert_integration
del convert_sticker
del convert_scheduled_event
del convert_thread


class AuditLogEntry:
    """
    Represents an entry of an ``AuditLog``.
    
    Attributes
    ----------
    changes : `list` of ``AuditLogChange``
        The changes of the entry.
    details : `None` or `dict` of (`str`, `Any`) items
        Additional information for a specific action types.
    id : `int`
        The unique identifier number of the entry.
    reason : `None` or `str`
        The reason provided with the logged action.
    target : `None`, ``Guild``,  ``ChannelGuildBase`` instance, ``ClientUserBase``, ``Role``, ``Webhook``,
            ``Emoji``, ``Message``, ``Integration``, ``Sticker``, ``Unknown``
        The target entity of the logged action. If the entity is not found, it will be set as an ``Unknown`` instance.
        It can also happen, that target entity is not provided, then target will be set as `None`.
    type : ``AuditLogEvent``
        The event type of the logged action.
    user : `None`, ``ClientUserBase``
        The user, who executed the logged action. If no user is provided then can be `None` as well.
    """
    __slots__ = ('changes', 'details', 'id', 'reason', 'target', 'type', 'user',)
    
    def __init__(self, data, parent):
        """
        Creates an audit log entry, from entry data sent inside of an ``AuditLog``'s data and from the audit itself.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        parent : ``AuditLog`` or ``AuditLogIterator``
            The parent of the entry, what contains the respective guild, the included users, webhooks and the
            integrations to work with.
        """
        self.id = int(data['id'])
        self.type = AuditLogEvent.get(int(data['action_type']))
        
        options = data.get('options', None)
        if (options is None):
            details = None
        else:
            details = {}
            for key, value in options.items():
                result = DETAIL_CONVERSIONS.get(key, DETAIL_CONVERTER_DEFAULT)(key, value, options)
                if result is None:
                    continue
                
                key, value = result
                details[key] = value
            
            if not details:
                details = None
        
        self.details = details
        
        user_id = data.get('user_id', None)
        if user_id is None:
            user = None
        else:
            user = parent.users.get(int(user_id), None)
        self.user = user
        
        self.reason = data.get('reason', None)
        
        change_datas = data.get('changes', None)
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
        
        try:
            conversion = CONVERSIONS[self.type.value//10]
        except KeyError:
            target = None
        else:
            target = conversion(self, parent, data.get('target_id', None))
        self.target = target
    
    @property
    def created_at(self):
        """
        When the audit log entry was created.
        
        Returns
        -------
        created_at : `datetime`
        """
        return id_to_datetime(self.id)
    
    def __repr__(self):
        """Returns the representation of the audit log entry."""
        repr_parts = [
            '<', self.__class__.__name__,
            ' id=', repr(self.id),
            ', type=', self.type.name,
        ]
        
        repr_parts.append(', user=')
        user = self.user
        if user is None:
            user_repr = 'None'
        else:
            user_repr = user.full_name
        repr_parts.append(user_repr)
        
        repr_parts.append(', target=')
        repr_parts.append(repr(self.target))
        
        repr_parts.append(', change count=')
        changes = self.changes
        if changes is None:
            change_amount_repr = '0'
        else:
            change_amount_repr = repr(len(self.changes))
        repr_parts.append(change_amount_repr)
        
        reason = self.reason
        if reason is not None:
            repr_parts.append(', reason=')
            # use repr to escape special inserted characters
            repr_parts.append(repr(reason))
        
        details = self.details
        if details is not None:
            repr_parts.append(', details=')
            repr_parts.append(repr(details))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)


def transform_nothing(name, data):
    before = data.get('old_value', None)
    after = data.get('new_value', None)
    return AuditLogChange(name, before, after)


def transform_deprecated(name, data):
    return None


def transform_icon(name, data):
    if name == 'splash_hash':
        name = 'invite_splash'
    else:
        name = name[:-5]
    
    before = Icon.from_base16_hash(data.get('old_value', None))
    
    after = Icon.from_base16_hash(data.get('new_value', None))
    
    return AuditLogChange(name, before, after)


def transform_bool__separated(name, data):
    before = data.get('old_value', None)
    after = data.get('new_value', None)
    
    return AuditLogChange('separated', before, after)


def transform_channel(name, data):
    name = name[:-3]
    
    value = data.get('old_value', None)
    if value is None:
        before = None
    else:
        value = int(value)
        try:
            before = CHANNELS[value]
        except KeyError:
            before = Unknown('Channel', value)
    
    value = data.get('new_value', None)
    if value is None:
        after = None
    else:
        value = int(value)
        try:
            after = CHANNELS[value]
        except KeyError:
            after = Unknown('Channel', value)
    
    return AuditLogChange(name, before, after)


def transform_color(name, data):
    before = data.get('old_value', None)
    if (before is not None):
        before = Color(before)
    
    after = data.get('new_value', None)
    if (after is not None):
        after = Color(after)
    
    return AuditLogChange('color', before, after)


def transform_content_filter(name, data):
    before = data.get('old_value', None)
    if (before is not None):
        before = ContentFilterLevel.get(before)
    
    after = data.get('new_value', None)
    if (after is not None):
        after = ContentFilterLevel.get(after)
    
    return AuditLogChange('content_filter', before, after)


def transform_video_quality_mode(name, data):
    before = data.get('old_value', None)
    if (before is not None):
        before = VideoQualityMode.get(before)
    
    after = data.get('new_value', None)
    if (after is not None):
        after = VideoQualityMode.get(after)
    
    return AuditLogChange('video_quality_mode', before, after)


def transform_int__days(name, data):
    before = data.get('old_value', None)
    after = data.get('new_value', None)
    return AuditLogChange('days', before, after)


def transform_int__slowmode(name, data):
    before = data.get('old_value', None)
    after = data.get('new_value', None)
    return AuditLogChange('slowmode', before, after)


def transform_message_notification(name, data):
    before = data.get('old_value', None)
    if (before is not None):
        before = MessageNotificationLevel.get(before)
    
    after = data.get('new_value', None)
    if (after is not None):
        after = MessageNotificationLevel.get(after)
    
    return AuditLogChange('message_notification', before, after)


def transform_mfa(name, data):
    before = data.get('old_value', None)
    if (before is not None):
        before = MFA.get(before)
    
    after = data.get('new_value', None)
    if (after is not None):
        after = MFA.get(after)
    
    return AuditLogChange('mfa', before, after)


def transform_overwrites(name, data):
    before = data.get('old_value', None)
    if (before is not None):
        before = [PermissionOverwrite(overwrite_data) for overwrite_data in before]
    
    after = data.get('new_value', None)
    if (after is not None):
        after = [PermissionOverwrite(overwrite_data) for overwrite_data in after]
    
    return AuditLogChange('overwrites', before, after)


def transform_permission(name, data):
    if name.endswith('_new'):
        name = name[:-4]
    
    before = data.get('old_value', None)
    if (before is not None):
        before = Permission(before)
    
    after = data.get('new_value', None)
    if (after is not None):
        after = Permission(after)
    
    return AuditLogChange(name, before, after)


def transform_region(name, data):
    before = data.get('old_value', None)
    if (before is not None):
        before = VoiceRegion.get(before)
    
    after = data.get('new_value', None)
    if (after is not None):
        after = VoiceRegion.get(after)
    
    return AuditLogChange('region', before, after)


def transform_roles(name, data):
    roles = []
    if name == '$add':
        before = None
        after = roles
    else:
        before = roles
        after = None
    
    for element in data['new_value']:
        role_id = int(element['id'])
        try:
            role = ROLES[role_id]
        except KeyError:
            role = Unknown('Role', role_id, element['name'])
        roles.append(role)
    
    return AuditLogChange('role', before, after)


def transform_snowflake(name, data):
    before = data.get('old_value', None)
    if (before is not None):
        before = int(before)
    
    after = data.get('new_value', None)
    if (after is not None):
        after = int(after)
    
    return AuditLogChange(name, before, after)

def transform_str__vanity_code(name, data):
    before = data.get('old_value', None)
    after = data.get('new_value', None)
    return AuditLogChange('vanity_code', before, after)


def transform_system_channel_flags(name, data):
    before = data.get('old_value', None)
    if (before is not None):
        before = SystemChannelFlag(before)
    
    after = data.get('new_value', None)
    if (after is not None):
        after = SystemChannelFlag(after)
    
    return AuditLogChange('system_channel_flags', before, after)


def transform_type(name, data):
    # If we talk about permission overwrite, type can be `str` too, what we ignore
    before = data.get('old_value', None)
    if (before is not None) and isinstance(before, str):
        return None
    
    after = data.get('new_value', None)
    if (after is not None) and isinstance(after,  str):
        return None
    
    return AuditLogChange('type', before, after)


def transform_user(name, data):
    name = name[:-3]
    
    value = data.get('old_value', None)
    if value is None:
        before = None
    else:
        value = int(value)
        try:
            before = USERS[value]
        except KeyError:
            before = Unknown('User', value)
    
    value = data.get('new_value', None)
    if value is None:
        after = None
    else:
        value = int(value)
        try:
            after = USERS[value]
        except KeyError:
            after = Unknown('User', value)
    
    return AuditLogChange(name, before, after)


def transform_verification_level(name, data):
    before = data.get('old_value', None)
    if (before is not None):
        before = VerificationLevel.get(before)
    
    after = data.get('new_value', None)
    if (after is not None):
        after = VerificationLevel.get(after)
    
    return AuditLogChange('verification_level', before, after)


def transform_tags(name, data):
    before = data.get('old_value', None)
    if (before is None) or (not before):
        before = None
    else:
        before = frozenset(before.split(', '))
    
    after = data.get('new_value', None)
    if (after is None) or (not after):
        after = None
    else:
        after = frozenset(after.split(', '))
    
    return AuditLogChange('tags', before, after)


def transform_int__auto_archive_after(name, data):
    before = data.get('old_value', None)
    if (before is not None):
        before *= 60
    
    after = data.get('new_value', None)
    if (after is not None):
        after *= 60
    
    return AuditLogChange('auto_archive_after', before, after)


def transform_int__default_auto_archive_after(name, data):
    before = data.get('old_value', None)
    if (before is not None):
        before *= 60
    
    after = data.get('new_value', None)
    if (after is not None):
        after *= 60
    
    return AuditLogChange('default_auto_archive_after', before, after)


def transform_privacy_level(name, data):
    before = data.get('old_value', None)
    if (before is not None):
        before = PrivacyLevel.get(before)
    
    after = data.get('new_value', None)
    if (after is not None):
        after = PrivacyLevel.get(after)
    
    return AuditLogChange('privacy_level', before, after)


def transform_scheduled_event_status(name, data):
    before = data.get('old_value', None)
    if (before is not None):
        before = ScheduledEventStatus.get(before)
    
    after = data.get('new_value', None)
    if (after is not None):
        after = ScheduledEventStatus.get(after)
    
    return AuditLogChange('status', before, after)


def transform_scheduled_event_entity_type(name, data):
    before = data.get('old_value', None)
    if (before is not None):
        before = ScheduledEventEntityType.get(before)
    
    after = data.get('new_value', None)
    if (after is not None):
        after =  ScheduledEventEntityType.get(after)
    
    return AuditLogChange('entity_type', before, after)


def transform_snowflake_array(name, data):
    before = data.get('old_value', None)
    if (before is None) or (not before):
        before = None
    else:
        before = tuple(int(sub_value) for sub_value in before)
    
    after = data.get('new_value', None)
    if (after is None) or (not after):
        after = None
    else:
        after = tuple(int(sub_value) for sub_value in after)
    
    return AuditLogChange(name, before, after)


def transform_unicode_emoji(name, data):
    before = data.get('old_value', None)
    if (before is None):
        before = None
    else:
        before = create_unicode_emoji(before)
    
    after = data.get('new_value', None)
    if (after is None):
        after = None
    else:
        after = create_unicode_emoji(after)
    
    return AuditLogChange(name, before, after)


TRANSFORMERS = {
    '$add': transform_roles,
    '$remove': transform_roles,
    'account_id': transform_snowflake,
    'afk_channel_id': transform_snowflake,
    'allow': transform_deprecated if API_VERSION in (6, 7) else transform_permission,
    'allow_new': transform_permission if API_VERSION in (6, 7) else transform_deprecated,
    'application_id': transform_snowflake,
    # archived (bool)
    'auto_archive_duration': transform_int__auto_archive_after,
    'avatar_hash': transform_icon,
    'banner_hash': transform_icon,
    # bitrate (int)
    'channel_id': transform_channel,
    # code (str)
    'color': transform_color,
    # deaf (bool)
    # description (None or str)
    'default_message_notifications': transform_message_notification,
    'default_auto_archive_duration': transform_int__default_auto_archive_after,
    'deny': transform_deprecated if API_VERSION in (6, 7) else transform_permission,
    'deny_new': transform_permission if API_VERSION in (6, 7) else transform_deprecated,
    'discovery_splash_hash' : transform_icon,
    # enable_emoticons (bool)
    'entity_type': transform_scheduled_event_entity_type,
    # expire_behavior (int)
    # expire_grace_period (int)
    'explicit_content_filter':transform_content_filter,
    'hoist': transform_bool__separated,
    'icon_hash': transform_icon,
    'id': transform_snowflake,
    'inviter_id': transform_user,
    # locked (bool)
    # mentionable (bool)
    # max_age (int)
    # max_uses (int)
    'mfa_level': transform_mfa,
    # mute (mute)
    # name (str)
    # nick (None or str)
    # nsfw (bool)
    'owner_id': transform_user,
    # position (int)
    'privacy_level': transform_privacy_level,
    'prune_delete_days': transform_int__days,
    'permission_overwrites' : transform_overwrites,
    'permissions': transform_deprecated if API_VERSION in (6, 7) else transform_permission,
    'permissions_new': transform_permission if API_VERSION in (6, 7) else transform_deprecated,
    'public_updates_channel_id' : transform_snowflake,
    'rate_limit_per_user': transform_int__slowmode,
    'region': transform_region,
    'rules_channel_id': transform_snowflake,
    'sku_ids': transform_snowflake_array,
    'splash_hash': transform_icon,
    'status': transform_scheduled_event_status,
    'system_channel_id': transform_snowflake,
    'system_channel_flags': transform_system_channel_flags,
    'tags': transform_tags,
    # temporary (bool)
    # topic (str)
    'type': transform_type,
    'unicode_emoji': transform_unicode_emoji,
    # uses (int)
    'vanity_url_code': transform_str__vanity_code,
    'verification_level': transform_verification_level,
    'video_quality_mode': transform_video_quality_mode,
    'widget_channel_id': transform_snowflake,
    # widget_enabled (bool)
}

del transform_deprecated
del transform_icon
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
del transform_roles
del transform_snowflake
del transform_str__vanity_code
del transform_system_channel_flags
del transform_type
del transform_user
del transform_verification_level
del transform_video_quality_mode
del transform_tags
del transform_int__auto_archive_after
del transform_int__default_auto_archive_after
del transform_privacy_level
del transform_scheduled_event_status
del transform_scheduled_event_entity_type
del transform_snowflake_array
del transform_unicode_emoji


class AuditLogChange:
    """
    A change of an ``AuditLogEntry``.
    
    Attributes
    ----------
    after : `Any`
        The changed attribute's new value. Defaults to `None`.
    attribute_name : `str`
        The name of the changed attribute.
    before : `Any`
        The changed attribute's original value. Defaults to `None`.
    
    Notes
    -----
    The value of `before` and `after` depending on the value of `attr`. These are:
    
    +-------------------------------+-----------------------------------------------+
    | attribute_name                | before / after                                |
    +===============================+===============================================+
    | account_id                    | `None` or `int`                               |
    +-------------------------------+-----------------------------------------------+
    | afk_channel_id                | `int`                                         |
    +-------------------------------+-----------------------------------------------+
    | allow                         | `None` or ``Permission``                      |
    +-------------------------------+-----------------------------------------------+
    | application_id                | `None` or `int`                               |
    +-------------------------------+-----------------------------------------------+
    | archived                      | `None` or `bool`                              |
    +-------------------------------+-----------------------------------------------+
    | auto_archive_duration         | `None` or `int`                               |
    +-------------------------------+-----------------------------------------------+
    | avatar                        | `None` or ``Icon``                            |
    +-------------------------------+-----------------------------------------------+
    | banner                        | `None` or ``Icon``                            |
    +-------------------------------+-----------------------------------------------+
    | bitrate                       | `None` or `int`                               |
    +-------------------------------+-----------------------------------------------+
    | channel                       | `None` or ``ChannelGuildBase`` instance       |
    +-------------------------------+-----------------------------------------------+
    | code                          | `None` or `str`                               |
    +-------------------------------+-----------------------------------------------+
    | color                         | `None` or ``Color``                           |
    +-------------------------------+-----------------------------------------------+
    | content_filter                | `None` or ``ContentFilterLevel``              |
    +-------------------------------+-----------------------------------------------+
    | days                          | `None` or `int`                               |
    +-------------------------------+-----------------------------------------------+
    | deaf                          | `None` or `bool`                              |
    +-------------------------------+-----------------------------------------------+
    | description                   | `None` or `str`                               |
    +-------------------------------+-----------------------------------------------+
    | default_message_notifications | `None` or ``MessageNotificationLevel``        |
    +-------------------------------+-----------------------------------------------+
    | deny                          | `None` or ``Permission``                      |
    +-------------------------------+-----------------------------------------------+
    | discovery_splash              | `None` or ``Icon``                            |
    +-------------------------------+-----------------------------------------------+
    | enable_emoticons              | `None` or `bool`                              |
    +-------------------------------+-----------------------------------------------+
    | entity_type                   | `None` or ``ScheduledEventEntityType``        |
    +-------------------------------+-----------------------------------------------+
    | expire_behavior               | `None` or `int`                               |
    +-------------------------------+-----------------------------------------------+
    | expire_grace_period           | `None` or `int`                               |
    +-------------------------------+-----------------------------------------------+
    | icon                          | `None` or ``Icon``                            |
    +-------------------------------+-----------------------------------------------+
    | id                            | `None` or `int`                               |
    +-------------------------------+-----------------------------------------------+
    | invite_splash                 | `None` or ``Icon``                            |
    +-------------------------------+-----------------------------------------------+
    | inviter                       | `None`, ``ClientUserBase``                    |
    +-------------------------------+-----------------------------------------------+
    | mentionable                   | `None` or `bool`                              |
    +-------------------------------+-----------------------------------------------+
    | max_age                       | `None` or `int`                               |
    +-------------------------------+-----------------------------------------------+
    | max_uses                      | `None` or `int`                               |
    +-------------------------------+-----------------------------------------------+
    | message_notification          | `None` or ``MessageNotificationLevel``        |
    +-------------------------------+-----------------------------------------------+
    | mfa                           | `None` or ``MFA``                             |
    +-------------------------------+-----------------------------------------------+
    | mute                          | `None` or `bool`                              |
    +-------------------------------+-----------------------------------------------+
    | name                          | `None` or `str`                               |
    +-------------------------------+-----------------------------------------------+
    | nick                          | `None` or `str`                               |
    +-------------------------------+-----------------------------------------------+
    | nsfw                          | `None` or `bool`                              |
    +-------------------------------+-----------------------------------------------+
    | owner                         | `None`, ``ClientUserBase``                    |
    +-------------------------------+-----------------------------------------------+
    | position                      | `None` or `int`                               |
    +-------------------------------+-----------------------------------------------+
    | public_updates_channel_id     | `int`                                         |
    +-------------------------------+-----------------------------------------------+
    | overwrites                    | `None` or `list` of ``PermissionOverwrite``   |
    +-------------------------------+-----------------------------------------------+
    | permissions                   | `None` or ``Permission``                      |
    +-------------------------------+-----------------------------------------------+
    | privacy_level                 | `None` or ``PrivacyLevel``                    |
    +-------------------------------+-----------------------------------------------+
    | region                        | `None` or ``VoiceRegion``                     |
    +-------------------------------+-----------------------------------------------+
    | role                          | `None` or `list` of ``Role``                  |
    +-------------------------------+-----------------------------------------------+
    | rules_channel_id              | `int`                                         |
    +-------------------------------+-----------------------------------------------+
    | separated                     | `None` or `bool`                              |
    +-------------------------------+-----------------------------------------------+
    | slowmode                      | `None` or `int`                               |
    +-------------------------------+-----------------------------------------------+
    | sku_ids                       | `None` or `tuple` of `int`                    |
    +-------------------------------+-----------------------------------------------+
    | system_channel_id             | `int`                                         |
    +-------------------------------+-----------------------------------------------+
    | system_channel_flags          | `None` or ``SystemChannelFlag``               |
    +-------------------------------+-----------------------------------------------+
    | tags                          | `None` ot `frozenset` of `str`                |
    +-------------------------------+-----------------------------------------------+
    | temporary                     | `None` or `bool`                              |
    +-------------------------------+-----------------------------------------------+
    | topic                         | `None` or `str`                               |
    +-------------------------------+-----------------------------------------------+
    | type                          | `None` or `int`                               |
    +-------------------------------+-----------------------------------------------+
    | unicode_emoji                 | `None` or ``Emoji``                           |
    +-------------------------------+-----------------------------------------------+
    | uses                          | `None` or `int`                               |
    +-------------------------------+-----------------------------------------------+
    | vanity_code                   | `None` or `str`                               |
    +-------------------------------+-----------------------------------------------+
    | verification_level            | `None` or ``VerificationLevel``               |
    +-------------------------------+-----------------------------------------------+
    | widget_channel_id             | `int`                                         |
    +-------------------------------+-----------------------------------------------+
    | widget_enabled                | `None` or `bool`                              |
    +-------------------------------+-----------------------------------------------+
    """
    __slots__ = ('after', 'attribute_name', 'before', )
    
    def __init__(self, attribute_name, before, after):
        """
        Creates a new audit log change instance.
        
        Parameters
        ----------
        attribute_name : `str`
            The name of the changed attribute.
        after : `Any`
            The changed attribute's new value.
        before : `Any`
            The changed attribute's original value.
        """
        self.attribute_name = attribute_name
        self.before = before
        self.after = after
    
    def __repr__(self):
        """Returns the representation of the audit log change."""
        return (
            f'{self.__class__.__name__}('
                f'attribute_name={self.attribute_name!r}, '
                f'before={self.before!r}, '
                f'after={self.after!r}'
            f')'
        )
    
    @property
    def attr(self):
        warnings.warn(
            f'`{self.__class__.__name__}.attr` attribute is deprecated, and will be removed in 2021 November. '
            f'Please use `.attribute_name` instead.',
            FutureWarning)
        
        return self.attribute_name
