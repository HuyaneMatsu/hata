__all__ = ('AuditLogEntry', )

from ...env import ALLOW_DEBUG_MESSAGES
from ...utils.debug import call_debug_logger

from ..core import GUILDS
from ..user import create_partial_user_from_id
from ..utils import id_to_datetime

from .change_converters.all_ import MERGED_CONVERTERS
from .change_converters.shared import convert_nothing
from .detail_converters import DETAIL_CONVERTERS, detail_converter_nothing
from .preinstanced import AuditLogEvent


class AuditLogEntry:
    """
    Represents an entry of an audit log.
    
    Attributes
    ----------
    _parent_reference : `None`, ``WeakReferer`` to ``AuditLog``
        Reference to the audit log entry keys' parent.
    changes : `list` of ``AuditLogChange``
        The changes of the entry.
    details : `None`, `dict` of (`str`, `object`) items
        Additional information for a specific action types.
    guild_id : `int`
        The source guild's identifier.
    id : `int`
        The unique identifier number of the entry.
    reason : `None`, `str`
        The reason provided with the logged action.
    target_id : `int`
        The entry's target's identifier.
        
        If no target is provided, this value defaults to `0`.
    type : ``AuditLogEvent``
        The event type of the logged action.
    user_id : `int`
        The user's identifier who triggered the event.
    """
    __slots__ = ('_parent_reference', 'changes', 'details', 'guild_id', 'id', 'reason', 'target_id', 'type', 'user_id',)
    
    def __new__(cls, data, parent = None):
        """
        Creates an audit log entry, from entry data sent inside of an ``AuditLog``'s data and from the audit itself.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Data received from Discord.
        
        parent : `None`, ``AuditLog`` = `None`, Optional
            The parent of the entry that contains the respective guild, the included users, webhooks and the
            integrations, etc... to work with.
        
        Returns
        -------
        self : `None`, ``AuditLogEntry``
            Returns `None` if Discord is derping like hell.
        """
        # event type
        raw_event_type = data.get('action_type', None)
        if (raw_event_type is None):
            return None
        
        event_type = AuditLogEvent.get(raw_event_type)
        
        # guild_id
        if parent is None:
            guild_id = data.get('guild_id', None)
            if guild_id is None:
                guild_id = 0
            else:
                guild_id = int(guild_id)
        else:
            guild_id = parent.guild_id
        
        # parent reference
        if parent is None:
            parent_reference = None
        else:
            parent_reference = parent._get_self_reference()
        
        
        self = object.__new__(cls)
        self.guild_id = guild_id
        self._parent_reference = parent_reference
        self.id = int(data['id'])
        
        self.type = event_type
        
        options = data.get('options', None)
        if (options is None):
            details = None
        else:
            details = {}
            for key, value in options.items():
                result = DETAIL_CONVERTERS.get(key, detail_converter_nothing)(key, value)
                if result is None:
                    continue
                
                key, value = result
                details[key] = value
            
            if not details:
                details = None
        
        self.details = details
        
        user_id = data.get('user_id', None)
        if user_id is None:
            user_id = 0
        else:
            user_id = int(user_id)
        self.user_id = user_id
        
        self.reason = data.get('reason', None)
        
        change_datas = data.get('changes', None)
        if (change_datas is None):
            changes = None
        else:
            changes = []
            change_converters = event_type.target_type.change_converters
            
            for change_data in change_datas:
                try:
                    key = change_data['key']
                except KeyError: # malformed?
                    continue
                
                try:
                    converter = change_converters[key]
                except KeyError:
                    if ALLOW_DEBUG_MESSAGES:
                        call_debug_logger(
                            (
                                f'Unknown Dispatch event change key: {key!r}\n'
                                f'- Change data: {data!r}\n'
                                f'- Event type: {event_type!r}'
                            ),
                            True,
                        )
                    
                    converter = MERGED_CONVERTERS.get(key, convert_nothing)
                
                change = converter(key, change_data)
                if (change is not None):
                    changes.append(change)
            
            if not changes:
                changes = None
        
        self.changes = changes
        
        target_id = data.get('target_id', None)
        if target_id is None:
            target_id = 0
        else:
            target_id = int(target_id)
        
        self.target_id = target_id
        return self
    
    
    @property
    def created_at(self):
        """
        When the audit log entry was created.
        
        Returns
        -------
        created_at : `datetime`
        """
        return id_to_datetime(self.id)
    
    
    @property
    def target(self):
        """
        Tries to resolve the target entity of the audit log entry.
        
        If the entity is not cached, returns `None`.
        
        Returns
        -------
        target : `None`, ``Guild``,  ``Channel``, ``ClientUserBase``, ``Role``, ``Webhook``,
            ``Emoji``, ``Message``, ``Integration``, ``Sticker``, ``Stage``, ``ScheduledEvent``
        """
        return self.type.target_type.target_converter(self)
    
    
    @property
    def parent(self):
        """
        Returns the entry's parent audit log.
        
        Returns
        -------
        parent : `None`, ``AuditLog``
        """
        parent_reference = self._parent_reference
        if (parent_reference is not None):
            return parent_reference()
    
    
    @property
    def guild(self):
        """
        Returns the audit log's guild.
        
        Returns
        -------
        guild : `None`, ``Guild``
        """
        return GUILDS.get(self.guild_id, None)
    
    
    @property
    def user(self):
        """
        Returns the user who triggered the event's creation.
        
        Returns
        -------
        user : `None`, ``ClientUserBase``
            Returns ˙None` if not an user triggered it.
        """
        user_id = self.user_id
        if user_id:
            return create_partial_user_from_id(user_id)
    
    
    def __repr__(self):
        """Returns the representation of the audit log entry."""
        repr_parts = [
            '<', self.__class__.__name__,
            ' id = ', repr(self.id),
            ', type = ', self.type.name,
        ]
        
        repr_parts.append(', user = ')
        repr_parts.append(repr(self.user))
        
        repr_parts.append(', target = ')
        repr_parts.append(repr(self.target))
        
        repr_parts.append(', change count = ')
        changes = self.changes
        if changes is None:
            change_amount_repr = '0'
        else:
            change_amount_repr = repr(len(self.changes))
        repr_parts.append(change_amount_repr)
        
        reason = self.reason
        if reason is not None:
            repr_parts.append(', reason = ')
            # use repr to escape special inserted characters
            repr_parts.append(repr(reason))
        
        details = self.details
        if details is not None:
            repr_parts.append(', details = ')
            repr_parts.append(repr(details))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
