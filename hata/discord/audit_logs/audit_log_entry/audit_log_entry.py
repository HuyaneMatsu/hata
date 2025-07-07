__all__ = ('AuditLogEntry', )

from ...bases import DiscordEntity
from ...core import GUILDS
from ...precreate_helpers import process_precreate_parameters_and_raise_extra
from ...user import create_partial_user_from_id

from ..conversion_helpers.helpers import _hash_dict

from .fields import (
    parse_changes, parse_details, parse_guild_id, parse_id, parse_reason, parse_target_id, parse_type, parse_user_id,
    put_changes, put_details, put_guild_id, put_id, put_reason, put_target_id,
    put_type, put_user_id, validate_changes, validate_details, validate_guild_id, validate_id,
    validate_parent, validate_reason, validate_target_id, validate_type, validate_user_id
)
from .preinstanced import AuditLogEntryType


PRECREATE_FIELDS = {
    'guild': ('guild_id', validate_guild_id),
    'guild_id': ('guild_id', validate_guild_id),
    'reason': ('reason', validate_reason),
    'user': ('user_id', validate_user_id),
    'user_id': ('user_id', validate_user_id),
    'target_id': ('target_id', validate_target_id),
}


class AuditLogEntry(DiscordEntity):
    """
    Represents an entry of an audit log.
    
    Attributes
    ----------
    _parent_reference : `None`, ``WeakReferer`` to ``AuditLog``
        Reference to the audit log entry keys' parent.
    
    changes : `None | dict<str, AuditLogChange>`
        The changes of the entry.
    
    details : `None | dict<str, object>`
        Additional information for the specific action types.
    
    guild_id : `int`
        The source guild's identifier.
    
    id : `int`
        The unique identifier number of the entry.
    
    reason : `None`, `str`
        The reason provided with the logged action.
    
    target_id : `int`
        The entry's target's identifier.
        
        If no target is provided, this value defaults to `0`.
    
    type : ``AuditLogEntryType``
        The logged event's type.
    
    user_id : `int`
        The user's identifier who triggered the event.
    """
    __slots__ = ('_parent_reference', 'changes', 'details', 'guild_id', 'reason', 'target_id', 'type', 'user_id',)
    
    
    def __new__(
        cls,
        *,
        changes = ...,
        details = ...,
        entry_type = ...,
        guild_id = ...,
        reason = ...,
        target_id = ...,
        user_id = ...,
    ):
        """
        Creates a new audit log entry with the given fields.
        
        Parameters
        ----------
        changes : `None | iterable<AuditLogChange>`, Optional (Keyword only)
            The changes of the entry.
        
        details : `None | dict<str, object>`, Optional (Keyword only)
            Additional information for the specific action types.
        
        entry_type : ``AuditLogEntryType``, `int`, Optional (Keyword only)
            The logged event's type.
        
        guild_id : `int`, `None`, ``Guild``, Optional (Keyword only)
            The source guild's identifier.
        
        reason : `None`, `str`, Optional (Keyword only)
            The reason provided with the logged action.
        
        target_id : `int`, Optional (Keyword only)
            The entry's target's identifier.
        
        user_id : `int`, ``None | ClientUserBase```, Optional (Keyword only)
            The user's identifier who triggered the event.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # entry_type
        if entry_type is ...:
            entry_type = AuditLogEntryType.none
        else:
            entry_type = validate_type(entry_type)
        
        # changes
        if changes is ...:
            changes = None
        else:
            changes = validate_changes(changes, entry_type = entry_type)
        
        # details
        if details is ...:
            details = None
        else:
            details = validate_details(details, entry_type = entry_type)
        
        # guild_id
        if guild_id is ...:
            guild_id = 0
        else:
            guild_id = validate_guild_id(guild_id)
        
        # reason
        if reason is ...:
            reason = None
        else:
            reason = validate_reason(reason)
        
        # target_id
        if target_id is ...:
            target_id = 0
        else:
            target_id = validate_target_id(target_id)
        
        # user_id
        if user_id is ...:
            user_id = 0
        else:
            user_id = validate_user_id(user_id)
        
        # Construct
        self = object.__new__(cls)
        self._parent_reference = None
        self.changes = changes
        self.details = details
        self.guild_id = guild_id
        self.id = 0
        self.reason = reason
        self.target_id = target_id
        self.type = entry_type
        self.user_id = user_id
        return self
    
        
    @classmethod
    def from_data(cls, data, parent = None):
        """
        Creates an audit log entry, from entry data sent inside of an ``AuditLog``'s data and from the audit itself.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Data received from Discord.
        
        parent : `None`, ``AuditLog`` = `None`, Optional
            The parent of the entry that contains the respective guild, the included users, webhooks and the
            integrations, etc... to work with.
        
        Returns
        -------
        self : `instance<cls>`
            Returns `None` if Discord is derping like hell.
        """
        # type
        entry_type = parse_type(data)
        if entry_type is AuditLogEntryType.none:
            return
        
        # guild_id
        guild_id = parse_guild_id(data, parent)
        
        # parent reference
        if parent is None:
            parent_reference = None
        else:
            parent_reference = parent._get_self_reference()
        
        # Construct
        self = object.__new__(cls)
        self._parent_reference = parent_reference
        self.changes = parse_changes(data, entry_type)
        self.details = parse_details(data, entry_type)
        self.guild_id = guild_id
        self.id = parse_id(data)
        self.reason = parse_reason(data)
        self.target_id = parse_target_id(data)
        self.type = entry_type
        self.user_id = parse_user_id(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Serialises the audit log entry.
        
        Parameters
        ----------
        defaults : `bool`, Optional (Keyword only)
            Whether fields with their default values should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        entry_type = self.type
        put_changes(self.changes, data, defaults, entry_type = entry_type)
        put_details(self.details, data, defaults, entry_type = entry_type)
        put_guild_id(self.guild_id, data, defaults)
        put_id(self.id, data, defaults)
        put_reason(self.reason, data, defaults)
        put_target_id(self.target_id, data, defaults)
        put_type(entry_type, data, defaults)
        put_user_id(self.user_id, data, defaults)
        return data
    
    
    @classmethod
    def precreate(cls, entry_id, *, changes = ..., details = ..., entry_type = ..., parent = ..., **keyword_parameters):
        """
        Creates a new audit log entry with the given fields.
        
        Parameters
        ----------
        entry_id : `int`
            The entry's unique identifier.
        
        changes : `None | iterable<AuditLogChange>`, Optional (Keyword only)
            The changes of the entry.
        
        details : `None | dict<str, object>`, Optional (Keyword only)
            Additional information for the specific action types.
        
        entry_type : ``AuditLogEntryType``, `int`, Optional (Keyword only)
            The logged event's type.
        
        parent : `None | AuditLog`, Optional (Keyword only)
            The parent audit log for the entry.
        
        **keyword_parameters : Keyword Parameters
            Additional keyword parameters.
        
        Other Parameters
        ----------------
        
        guild : `int`, ``None | Guild``, Optional (Keyword only)
            Alternative for `guild_id`.
        
        guild_id : `int`, `None`, ``Guild``, Optional (Keyword only)
            The source guild's identifier.
        
        reason : `None`, `str`, Optional (Keyword only)
            The reason provided with the logged action.
        
        target_id : `int`, Optional (Keyword only)
            The entry's target's identifier.
        
        user : `int`, ``None | ClientUserBase```, Optional (Keyword only)
            Alternative for `user_id`.
        
        user_id : `int`, ``None | ClientUserBase```, Optional (Keyword only)
            The user's identifier who triggered the event.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        entry_id = validate_id(entry_id)
        
        # entry_type
        if entry_type is ...:
            entry_type = AuditLogEntryType.none
        else:
            entry_type = validate_type(entry_type)
        
        # changes
        if changes is ...:
            changes = None
        else:
            changes = validate_changes(changes, entry_type = entry_type)
        
        # details
        if details is ...:
            details = None
        else:
            details = validate_details(details, entry_type = entry_type)
        
        # parent
        if parent is ...:
            parent = None
        else:
            parent = validate_parent(parent)
        
        # keyword_parameters
        if keyword_parameters:
            processed = process_precreate_parameters_and_raise_extra(keyword_parameters, PRECREATE_FIELDS)
        else:
            processed = None
        
        # Get parent reference
        if parent is None:
            parent_reference = None
        else:
            parent_reference = parent._get_self_reference()
        
        # Construct
        self = object.__new__(cls)
        self._parent_reference = parent_reference
        self.changes = changes
        self.details = details
        self.guild_id = 0
        self.id = entry_id
        self.reason = None
        self.target_id = 0
        self.type = entry_type
        self.user_id = 0
        
        # Set processed fields
        if (processed is not None):
            for name, value in processed:
                setattr(self, name, value)
        
        return self
    
    
    def copy(self):
        """
        Copies the audit log entry.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new._parent_reference = None
        
        changes = self.changes
        if (changes is not None):
            changes = changes.copy()
        new.changes = changes
        
        details = self.details
        if (details is not None):
            details = details.copy()
        new.details = details
        
        new.guild_id = self.guild_id
        new.id = 0
        new.reason = self.reason
        new.target_id = self.target_id
        new.type = self.type
        new.user_id = self.user_id
        return new
    
    
    def copy_with(
        self, 
        *,
        changes = ...,
        details = ...,
        entry_type = ...,
        guild_id = ...,
        reason = ...,
        target_id = ...,
        user_id = ...,
    ):
        """
        Copies the audit log entry with the given fields.
        
        Parameters
        ----------
        changes : `None | iterable<AuditLogChange>`, Optional (Keyword only)
            The changes of the entry.
        
        details : `None | dict<str, object>`, Optional (Keyword only)
            Additional information for the specific action types.
        
        entry_type : ``AuditLogEntryType``, `int`, Optional (Keyword only)
            The logged event's type.
        
        guild_id : `int`, `None`, ``Guild``, Optional (Keyword only)
            The source guild's identifier.
        
        reason : `None`, `str`, Optional (Keyword only)
            The reason provided with the logged action.
        
        target_id : `int`, Optional (Keyword only)
            The entry's target's identifier.
        
        user_id : `int`, ``None | ClientUserBase```, Optional (Keyword only)
            The user's identifier who triggered the event.
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # We yeet old changes and details on `target_type` mismatch.
        # entry_type
        if entry_type is ...:
            entry_type = self.type
            target_type_mismatch = False
        else:
            entry_type = validate_type(entry_type)
            target_type_mismatch = self.type.target_type is not entry_type.target_type
        
        # changes
        if changes is ...:
            if target_type_mismatch:
                changes = None
            else:
                changes = self.changes
                if (changes is not None):
                    changes = changes.copy()
        else:
            changes = validate_changes(changes, entry_type = entry_type)
        
        # details
        if details is ...:
            if target_type_mismatch:
                details = None
            else:
                details = self.details
                if (details is not None):
                    details = details.copy()
        else:
            details = validate_details(details, entry_type = entry_type)
        
        # guild_id
        if guild_id is ...:
            guild_id = self.guild_id
        else:
            guild_id = validate_guild_id(guild_id)
        
        # reason
        if reason is ...:
            reason = self.reason
        else:
            reason = validate_reason(reason)
        
        # target_id
        if target_id is ...:
            target_id = self.target_id
        else:
            target_id = validate_target_id(target_id)
        
        # user_id
        if user_id is ...:
            user_id = self.user_id
        else:
            user_id = validate_user_id(user_id)
        
        # Construct
        self = object.__new__(type(self))
        self._parent_reference = None
        self.changes = changes
        self.details = details
        self.guild_id = guild_id
        self.id = 0
        self.reason = reason
        self.target_id = target_id
        self.type = entry_type
        self.user_id = user_id
        return self
    
    
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
        target_converter = self.type.target_type.target_converter
        if (target_converter is not None):
            return target_converter(self)
    
    
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
        guild : ``None | Guild``
        """
        guild_id = self.guild_id
        if guild_id:
            return GUILDS.get(guild_id, None)
    
    
    @property
    def user(self):
        """
        Returns the user who triggered the event's creation.
        
        Returns
        -------
        user : ``None | ClientUserBase``
            Returns ˙None` if not an user triggered it.
        """
        user_id = self.user_id
        if user_id:
            return create_partial_user_from_id(user_id)
    
    
    def __repr__(self):
        """Returns the representation of the audit log entry."""
        repr_parts = ['<', self.__class__.__name__]
        
        # id
        entry_id = self.id
        if entry_id:
            repr_parts.append(' id = ')
            repr_parts.append(repr(entry_id))
            repr_parts.append(',')
        
        # type
        entry_type = self.type
        repr_parts.append(' type = ')
        repr_parts.append(entry_type.name)
        repr_parts.append(' ~ ')
        repr_parts.append(repr(entry_type.value))
        
        # user_id
        user_id = self.user_id
        if user_id:
            repr_parts.append(', user_id = ')
            repr_parts.append(repr(user_id))
        
        # guild_id
        guild_id = self.guild_id
        if guild_id:
            repr_parts.append(', guild_id = ')
            repr_parts.append(repr(guild_id))
        
        # target_id
        target_id = self.target_id
        if target_id:
            repr_parts.append(', target_id = ')
            repr_parts.append(repr(target_id))
        
        # changes
        changes = self.changes
        if (changes is not None):
            repr_parts.append(', changes = ')
            repr_parts.append(repr(changes))
        
        # details
        details = self.details
        if (details is not None):
            repr_parts.append(', details = ')
            repr_parts.append(repr(details))
        
        # reason
        reason = self.reason
        if reason is not None:
            repr_parts.append(', reason = ')
            repr_parts.append(repr(reason))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two audit log entries are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def __ne__(self, other):
        """Returns whether the two audit log entries are not equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return not self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Returns whether the two audit log entries are equal.
        
        Parameters
        ----------
        other : `instance<type<self>>`
            The other instance. Must be the same type as self.
        
        Returns
        -------
        is_equal : `bool`
        """
        # id
        self_id = self.id
        other_id = other.id
        if self_id and other_id and self_id != other_id:
            return False
        
        # changes
        if self.changes != other.changes:
            return False
        
        # details
        if self.details != other.details:
            return False
        
        # guild_id
        if self.guild_id != other.guild_id:
            return False
        
        # reason
        if self.reason != other.reason:
            return False
        
        # target_id
        if self.target_id != other.target_id:
            return False
        
        # type
        if self.type is not other.type:
            return False
        
        # user_id
        if self.user_id != other.user_id:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the audit log entry's hash value."""
        hash_value = 0
        
        # id
        hash_value ^= hash(self.id)
        
        # changes
        changes = self.changes
        if (changes is not None):
            hash_value ^= _hash_dict(changes)
        
        # details
        details = self.details
        if (details is not None):
            hash_value ^= _hash_dict(details)
        
        # guild_id
        hash_value ^= self.guild_id
        
        # reason
        reason = self.reason
        if (reason is not None):
            hash_value ^= hash(reason)
        
        # target_id
        hash_value ^= self.target_id
        
        # type
        hash_value ^= hash(self.type)
        
        # user_id:
        hash_value ^= self.user_id
        
        return hash_value
    
    
    def get_change(self, attribute_name):
        """
        Gets the audit log entry's change for the given `attribute_name`.
        
        Parameters
        ----------
        attribute_name : `str`
            The change by its attribute name to get.
        
        Returns
        -------
        change : `None`, ``AuditLogChange``
        """
        changes = self.changes
        if (changes is not None):
            return changes.get(attribute_name, None)
    
    
    def iter_changes(self):
        """
        Iterates over the changes of the audit log entry.
        
        This method is an iterable generator.
        
        Yields
        ------
        change : ``AuditLogChange``
        """
        changes = self.changes
        if (changes is not None):
            yield from changes.values()
    
    
    def get_detail(self, name):
        """
        Gets the audit log entry's detail for the given `name`.
        
        Parameters
        ----------
        name : `str`
            The detail's name.
        
        Returns
        -------
        change : `None | object`
        """
        details = self.details
        if (details is not None):
            return details.get(name, None)
    
    
    def iter_details(self):
        """
        Iterates over the details of the audit log entry.
        
        This method is an iterable generator.
        
        Yields
        ------
        detail : `(str, object)`
        """
        details = self.details
        if (details is not None):
            yield from details.items()
    
    
    def _link_parent_soft(self, parent):
        """
        Links the given parent to the entry if self is not linked yet.
        
        Parameters
        ----------
        parent : ``AuditLog`
            The parent to link.
        """
        if self.parent is None:
            self._parent_reference = parent._get_self_reference()
    
    
    def _link_parent_hard(self, parent):
        """
        Links the given parent to the entry even if self is already linked.
        
        Parameters
        ----------
        parent : ``AuditLog`
            The parent to link.
        """
        self._parent_reference = parent._get_self_reference()
