__all__ = ('AuditLogEntry', )

from ....env import ALLOW_DEBUG_MESSAGES
from ....utils.debug import call_debug_logger

from ...utils import id_to_datetime

from .change_converters.all_ import MERGED_CONVERTERS
from .change_converters.shared import convert_nothing
from .detail_converters import DETAIL_CONVERTERS, detail_converter_nothing
from .preinstanced import AuditLogEvent


class AuditLogEntry:
    """
    Represents an entry of an ``AuditLog``.
    
    Attributes
    ----------
    _parent_reference : ``WeakReferer`` to ``AuditLog``
        Reference to the audit log entry keys' parent.
    changes : `list` of ``AuditLogChange``
        The changes of the entry.
    details : `None`, `dict` of (`str`, `Any`) items
        Additional information for a specific action types.
    id : `int`
        The unique identifier number of the entry.
    reason : `None`, `str`
        The reason provided with the logged action.
    target_id : `int`
        The entry's target's identifier.
        
        If no target is provided, this value defaults to `0`.
    type : ``AuditLogEvent``
        The event type of the logged action.
    user : `None`, ``ClientUserBase``
        The user, who executed the logged action. If no user is provided then can be `None` as well.
    """
    __slots__ = ('_parent_reference', 'changes', 'details', 'id', 'reason', 'target_id', 'type', 'user',)
    
    def __new__(cls, data, parent):
        """
        Creates an audit log entry, from entry data sent inside of an ``AuditLog``'s data and from the audit itself.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        parent : ``AuditLog``
            The parent of the entry, what contains the respective guild, the included users, webhooks and the
            integrations, etc... to work with.
        
        Returns
        -------
        self : `None`, ``AuditLogEntry``
            Returns `None` if Discord is derping like hell.
        """
        raw_event_type = data.get('action_type', None)
        if (raw_event_type is None):
            return None
        
        self = object.__new__(cls)
        self._parent_reference = parent._get_self_reference()
        self.id = int(data['id'])
        
        event_type = AuditLogEvent.get(raw_event_type)
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
        return self._parent_reference()
    
    
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
