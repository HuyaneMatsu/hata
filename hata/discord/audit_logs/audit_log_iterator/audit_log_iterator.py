__all__ = ('AuditLogIterator', )

from scarletio import RichAttributeErrorBaseType, Task, shield

from ...core import KOKORO
from ...utils import now_as_id

from ..audit_log import AuditLog

from .fields import validate_entry_type, validate_guild_id, validate_user_id


class AuditLogIterator(RichAttributeErrorBaseType):
    """
    An asynchronous iterator over a guild's audit logs.
    
    Attributes
    ----------
    _audit_log_entry_index : `int`
        The index of the entry in an audit to return next.
    
    _audit_log_index : `int`
        The index of the audit log to return entry from.
    
    _data : `dict<str, object>`
        Data to make request with.
    
    _load_one_task : ``None | Task<bool>``
        Synchronised task among consumers to request a new audit log.
    
    audit_logs : ``list<AuditLog>``
        The requested audit logs.
    
    client : ``Client``
        Client to request with.
    
    guild_id : `int`
        The respective guild's identifier.
    """
    __slots__ = (
        '_audit_log_entry_index', '_audit_log_index', '_data', '_load_one_task', 'audit_logs', 'client', 'guild_id'
    )
    
    def __new__(cls, client, guild_id, *, entry_type = ..., user_id = ...):
        """
        Creates an audit log iterator with the given parameters.
        
        Parameters
        ----------
        client : ``Client``
            The client, who will execute the api requests.
        
        guild_id : ``int | Guild``
            The guild what's audit logs will be requested.
        
        entry_type : ``AuditLogEntryType``, `int`, `None`, Optional
            Whether the audit logs should be filtered only on the given event.
        
        user_id : ``None | int | ClientUserBase``, Optional
            Whether the audit logs should be filtered only to those, which were created by the given user.
        """
        # guild_id
        guild_id = validate_guild_id(guild_id)
        
        # Build data
        data = {
            'limit': 100,
            'before': now_as_id(),
        }
        
        # entry_type
        if (entry_type is not ...):
            data['action_type'] = validate_entry_type(entry_type).value
        
        # user_id
        if (user_id is not ...):
            user_id = validate_user_id(user_id)
            if user_id:
                data['user_id'] = str(user_id)
        
        
        self = object.__new__(cls)
        self._audit_log_entry_index = 0
        self._audit_log_index = 0
        self._data = data
        self._load_one_task = None
        self.audit_logs = []
        self.client = client
        self.guild_id = guild_id
        
        return self
    
    
    async def _load_one_inner(self):
        """
        Loads a single audit log.
        
        This method is a coroutine.
        """
        client = self.client
        data = self._data
        
        audit_log_data = await client.api.audit_log_get_chunk(self.guild_id, data)
        audit_log = AuditLog.from_data(audit_log_data, self.guild_id)
        self.audit_logs.append(audit_log)
        
        audit_log_length = len(audit_log)
        if audit_log_length < 100:
            return False
        
        data['before'] = audit_log[-1].id
        return True
    
    
    async def _load_one_outer(self):
        """
        Loads a single audit log. Does synchronised ``._load_one_inner`` calls.
        
        This method is a coroutine.
        """
        load_one_task = self._load_one_task
        if load_one_task is None or load_one_task.is_done():
            load_one_task = Task(KOKORO, self._load_one_inner())
            self._load_one_task = load_one_task
        
        try:
            return await shield(load_one_task, KOKORO)
        finally:
            if load_one_task.is_done():
                self._load_one_task = None
    
    
    async def load_all(self):
        """
        Loads all not yet loaded audit logs of the audit log iterator's guild.
        
        This method is a coroutine.
        """
        while (await self._load_one_outer()):
            pass
    
    
    def transform(self):
        """
        Converts the audit log iterator to an audit log object.
        
        Returns
        -------
        audit_log : ``AuditLog``
        """
        return AuditLog.from_many(self.audit_logs)
    
    
    def __aiter__(self):
        """Returns self and resets the `.index`."""
        return self
    
    
    async def __anext__(self):
        """
        Yields the next entry of the audit log iterator.
        
        This method is a coroutine.
        """
        audit_logs = self.audit_logs
        
        # Use a while True loop, because if over 100 parallel iterations are done it may mean that some consumers will
        # not be satisfied from 1 pull.
        while True:
            audit_logs_length = len(audit_logs)
            audit_log_index = self._audit_log_index
            
            if audit_logs_length > audit_log_index:
                audit_log = audit_logs[audit_log_index]
                
                audit_log_entries_length = len(audit_log)
                audit_log_entry_index = self._audit_log_entry_index
                if audit_log_entry_index < audit_log_entries_length:
                    entry = audit_log[audit_log_entry_index]
                    self._audit_log_entry_index += 1
                    return entry
                
                if audit_log_entries_length < 100:
                    raise StopAsyncIteration
                
                self._audit_log_index += 1
                self._audit_log_entry_index = 0
            
            await self._load_one_outer()
    
    
    def __repr__(self):
        """Returns the audit log iterator's representation."""
        repr_parts = ['<', type(self).__name__]
        
        # client
        repr_parts.append(' client = ')
        repr_parts.append(repr(self.client))
        
        # guild_id
        repr_parts.append(', guild_id = ')
        repr_parts.append(repr(self.guild_id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
