__all__ = ('AuditLogIterator', )

from ..bases import maybe_snowflake
from ..guild import Guild
from ..user import ClientUserBase
from ..utils import now_as_id

from .audit_log import AuditLog
from .audit_log_entry import AuditLogEntry
from .preinstanced import AuditLogEvent


class AuditLogIterator(AuditLog):
    """
    An async iterator over a guild's audit logs.
    
    Attributes
    ----------
    _self_reference : `None` or ``WeakReferer`` to ``AuditLog``
        Weak reference to the audit log itself.
    application_commands : `dict` of (`int`, ``ApplicationCommand``) items
        A dictionary that contains the mentioned application commands by the audi log entries. The keys are the `id`-s
        of the application commands, meanwhile the values are the application commands themselves.
    auto_moderation_rules : `dict` of (`int`, ``ApplicationCommand``) items
        A dictionary that contains the auto moderation rules mentioned inside of the audit log entries. The keys
        are the `id`-s of the rules and the values are the rules themselves.
    entries : `list` of ``AuditLogEntry``
        A list of audit log entries that the audit log contains.
    guild_id : `int`
        The audit logs' respective guild's identifier.
    integrations : `dict` of (`int`, ``Integration``) items
        A dictionary that contains the mentioned integrations by the audit log's entries. The keys are the `id`-s of
        the integrations, meanwhile the values are the integrations themselves.
    scheduled_events : `dict` of (`int`, ``ScheduledEvent``) items
        A dictionary containing the scheduled events mentioned inside of the audit logs.
    threads : `dict` of (`int`, ``Channel``) items
        A dictionary containing the mentioned threads inside of the audit logs.
    users : `dict` of (`int`, ``ClientUserBase``) items
        A dictionary that contains the mentioned users by the audit log's entries. The keys are the `id`-s of the
        users, meanwhile the values are the users themselves.
    webhooks : `dict` of (`int`, ``Webhook``) items
        A dictionary that contains the mentioned webhook by the audit log's entries. The keys are the `id`-s of the
        webhooks, meanwhile the values are the values themselves.
    
    _data : `dict` of (`str`, `Any`) items
        Data to be sent to Discord when requesting an another audit log chunk. Contains some information, which are not
        stored by any attributes of the audit log iterator, these are the filtering `user` and `event` options.
    _index : `int`
        The next audit log entries index to yield.
    client : ``Client``
        The client, who will execute the api requests.
    """
    __slots__ = ('_data', '_index', 'client',)
    
    def __new__(cls, client, guild_id, user = None, event = None):
        """
        Creates an audit log iterator with the given parameters.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client, who will execute the api requests.
        guild_id : ``Guild``, `int`
            The guild what's audit logs will be requested.
        user : `None`, ``ClientUserBase``, `int` = `None`, Optional
            Whether the audit logs should be filtered only to those, which were created by the given user.
        event : `None`, ``AuditLogEvent``, `int` = `None`, Optional
            Whether the audit logs should be filtered only on the given event.
        
        Raises
        ------
        TypeError
            - If `guild` was not given neither as ``Guild``, nor as `int`.
            - If `user` was not given neither as `None`, ``ClientUserBase`` nor as `int`.
            - If `event` as not not given neither as `None`, ``AuditLogEvent`` nor as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        data = {
            'limit': 100,
            'before': now_as_id(),
        }
        
        if isinstance(guild_id, Guild):
            validated_guild_id = guild_id.id
        else:
            validated_guild_id = maybe_snowflake(guild_id)
            if guild_id is None:
                raise TypeError(
                    f'`guild_id` can be `{Guild.__name__}`, `int`, got '
                    f'{type(guild_id).__name__}; {guild_id!r}.'
                )
        
        if (user is not None):
            if isinstance(user, ClientUserBase):
                user_id = user.id
            
            else:
                user_id = maybe_snowflake(user)
                if user_id is None:
                    raise TypeError(
                        f'`user` can be `{ClientUserBase.__name__}`, `int`, got'
                        f'{user.__class__.__name__}; {user!r}.'
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
        
        self = AuditLog.__new__(cls, None, validated_guild_id)
        self._data = data
        self._index = 0
        self.client = client
        
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
            
            log_data = await http.audit_log_get_chunk(self.guild_id, data)
            
            if not self._populate(log_data):
                return
            
            if len(entries) % 100:
                return
    
    
    def transform(self):
        """
        Converts the audit log iterator to an audit log object.
        
        Returns
        -------
        audit_log : ``AuditLog``
        """
        audit_log = object.__new__(AuditLog)
        audit_log.application_commands = self.application_commands
        audit_log.auto_moderation_rules = self.auto_moderation_rules
        audit_log.entries = self.entries
        audit_log.guild_id = self.guild_id
        audit_log.integrations = self.integrations
        audit_log.scheduled_events = self.scheduled_events
        audit_log.threads = self.threads
        audit_log.users = self.users
        audit_log.webhooks = self.webhooks
        return audit_log
    
    
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
        
        if index % 100:
            raise StopAsyncIteration
        
        data = self._data
        if ln:
            data['before'] = self.entries[ln - 1].id
        
        log_data = await self.client.http.audit_log_get_chunk(self.guild_id, data)
        
        if not self._populate(log_data):
            raise StopAsyncIteration
        
        self._index += 1
        return self.entries[index]
