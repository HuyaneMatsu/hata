__all__ = ('EventHandlerSnapshotType',)

from scarletio import RichAttributeErrorBaseType, copy_docs

from .helpers import _merge_list_groups, _get_list_difference
from .base_snapshot_type import BaseSnapshotType


class EventHandlerDifference(RichAttributeErrorBaseType):
    """
    Represents a difference between two event handlers.
    
    Attributes
    ----------
    added_event_handlers : `None`, `list` of `callable`
        The added event handlers.
    removed_event_handlers : `None`, `list` of `callable`
        The removed event handlers.
    """
    __slots__ = ('added_event_handlers', 'removed_event_handlers',)
    
    def __new__(cls):
        """
        Creates a new event handler difference.
        """
        self = object.__new__(cls)
        self.added_event_handlers = None
        self.removed_event_handlers = None
        
        return self
    
    
    def __repr__(self):
        """Returns the event handler difference."""
        repr_parts = ['<', self.__class__.__name__]
        
        field_added = False
        
        added_event_handlers = self.added_event_handlers
        if (added_event_handlers is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' added_event_handlers=')
            repr_parts.append(repr(added_event_handlers))
        
        removed_event_handlers = self.removed_event_handlers
        if (removed_event_handlers is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(',4 removed_event_handlers=')
            repr_parts.append(repr(removed_event_handlers))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __bool__(self):
        """Returns whether the difference contains any changes."""
        if (self.added_event_handlers is not None):
            return True
        
        if (self.removed_event_handlers is not None):
            return True
        
        return False
    
    
    def add(self, event_handler):
        """
        Adds an event handler to self.
        
        Parameters
        ----------
        event_handler : `callable`
            The event handler to add.
        """
        added_event_handlers = self.added_event_handlers
        if (added_event_handlers is None):
            added_event_handlers = []
            self.added_event_handlers = added_event_handlers
        
        removed_event_handlers = self.removed_event_handlers
        if (removed_event_handlers is not None):
            try:
                removed_event_handlers.remove(event_handler)
            except ValueError:
                pass
            else:
                if not removed_event_handlers:
                    self.removed_event_handlers = None
        
        added_event_handlers.append(event_handler)
    
    
    def remove(self, event_handler):
        """
        Removes the event handler from self.
        
        Parameters
        ----------
        event_handler : `callable`
            The event handler to remove.
        """
        added_event_handlers = self.added_event_handlers
        if (added_event_handlers is not None):
            try:
                added_event_handlers.remove(event_handler)
            except ValueError:
                pass
            else:
                if not added_event_handlers:
                    self.added_event_handlers = None
        
        removed_event_handlers = self.removed_event_handlers
        if (removed_event_handlers is None):
            removed_event_handlers = []
            self.removed_event_handlers = removed_event_handlers
        
        removed_event_handlers.append(event_handler)
    
    
    def iter_added_event_handlers(self):
        """
        Iterates over the added event handlers of the event handler difference.
        
        This method is an iterable generator.
        
        Yields
        ------
        added_event_handler : `callable`
        """
        added_event_handlers = self.added_event_handlers
        if (added_event_handlers is not None):
            yield from added_event_handlers
    
    
    def iter_removed_event_handlers(self):
        """
        Iterates over the removed event handlers of the event handler difference.
        
        This method is an iterable generator.
        
        Yields
        ------
        removed_event_handler : `callable`
        """
        removed_event_handlers = self.removed_event_handlers
        if (removed_event_handlers is not None):
            yield from removed_event_handlers
    
    
    def copy(self):
        """
        Copies the event handler difference.
        
        Returns
        -------
        new : ``EventHandlerDifference``
        """
        added_event_handlers = self.added_event_handlers
        if (added_event_handlers is not None):
            added_event_handlers = added_event_handlers.copy()
        
        removed_event_handlers = self.removed_event_handlers
        if (removed_event_handlers is not None):
            removed_event_handlers = removed_event_handlers.copy()
        
        new = object.__new__(type(self))
        new.added_event_handlers = added_event_handlers
        new.removed_event_handlers = removed_event_handlers
        return new
    
    
    def revert_copy(self):
        """
        Revert copies the event handler difference.
        
        Returns
        -------
        new : ``EventHandlerDifference``
        """
        added_event_handlers = self.added_event_handlers
        if (added_event_handlers is not None):
            added_event_handlers = added_event_handlers.copy()
        
        removed_event_handlers = self.removed_event_handlers
        if (removed_event_handlers is not None):
            removed_event_handlers = removed_event_handlers.copy()
        
        new = object.__new__(type(self))
        new.added_event_handlers = removed_event_handlers
        new.removed_event_handlers = added_event_handlers
        return new
    
    
    def _subtract(self, other):
        """
        Subtracts other from self.
        
        Parameters
        ----------
        other : ``EventHandlerDifference``
            The other difference to subtract from self.
        
        Returns
        -------
        new : ``EventHandlerDifference``
        """
        added_event_handlers, removed_event_handlers = _get_list_difference(
            _merge_list_groups(self.added_event_handlers, other.removed_event_handlers),
            _merge_list_groups(other.added_event_handlers, self.removed_event_handlers),
        )
        
        new = object.__new__(type(self))
        new.added_event_handlers = added_event_handlers
        new.removed_event_handlers = removed_event_handlers
        return new
    
    
    def __sub__(self, other):
        """Subtracts other from self."""
        if other is None:
            return self.copy()
        
        if type(self) is type(other):
            return self._subtract(other)
        
        return NotImplemented
    
    
    def __rsub__(self, other):
        """subtracts other from self."""
        if other is None:
            return self.revert_copy()
        
        if type(self) is type(other):
            return other._subtract(self)
        
        return NotImplemented


class EventHandlerSnapshotType(BaseSnapshotType):
    """
    Event handler snapshot.
    
    Attributes
    ----------
    _client_reference : `WeakReferer` to `Client`
        Weakreference to the owner client instance.
    _is_difference : `bool`
        Whether the snapshot is a difference.
    differences : `dict` of (`str`, `list` of `callable`) items
        The collected event handlers.
    """
    __slots__ = ('differences',)
    
    @copy_docs(BaseSnapshotType.__new__)
    def __new__(cls, client):
        differences = {}
        
        event_handler_manager = client.events
        for event_handler_name, event_handler in event_handler_manager.iter_event_names_and_handlers():
            try:
                difference = differences[event_handler_name]
            except KeyError:
                difference = EventHandlerDifference()
                differences[event_handler_name] = difference
            
            difference.add(event_handler)
        
        self = BaseSnapshotType.__new__(cls, client)
        self.differences = differences
        return self
    
    
    @copy_docs(BaseSnapshotType._extract)
    def _extract(self, other):
        new_differences = {}
        
        self_differences = self.differences
        other_difference = other.differences
        
        for event_handler_name in {*self_differences.keys(), *other_difference.keys()}:
            new_difference = \
                self_differences.get(event_handler_name, None) - other_difference.get(event_handler_name, None)
            
            if new_difference:
                new_differences[event_handler_name] = new_difference
        
        new = BaseSnapshotType._extract(self, other)
        new.differences = new_differences
        return new
    
    
    @copy_docs(BaseSnapshotType.revert)
    def revert(self):
        BaseSnapshotType.revert(self)
        
        client = self.client
        if client is None:
            return
        
        
        event_handler_manager = client.events
        for event_handler_name, difference in self.differences.items():
            for event_handler in difference.iter_added_event_handlers():
                event_handler_manager.remove(event_handler, name=event_handler_name, count=1)
            
            for event_handler in difference.iter_removed_event_handlers():
                event_handler_manager(event_handler, name=event_handler_name)
    
    
    @copy_docs(BaseSnapshotType.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        client = self.client
        if (client is not None):
            repr_parts.append(' of ')
            repr_parts.append(repr(client))
        
        
        differences = self.differences
        if differences:
            repr_parts.append(', differences=')
            repr_parts.append(repr(self.differences))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(BaseSnapshotType.__bool__)
    def __bool__(self):
        if self.differences:
            return True
        
        return False
