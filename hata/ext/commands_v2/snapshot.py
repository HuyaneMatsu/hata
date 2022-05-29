__all__ = ('CommandsV2SnapshotType',)

from scarletio import copy_docs

from ..plugin_loader import BaseSnapshotType
from ..plugin_loader.snapshot.helpers import  _get_set_difference, _merge_set_groups

from .command_processor import CommandProcessor


class CommandsV2SnapshotType(BaseSnapshotType):
    """
    Commands extension snapshot.
    
    Attributes
    ----------
    _client_reference : `WeakReferer` to `Client`
        Weakreference to the owner client instance.
    _is_difference : `bool`
        Whether the snapshot is a difference.
    added_categories : `None`, `set` of ``Category``
        Added categories.
    added_commands : `None`, `set` of ``Command``
        Added commands.
    removed_categories : `None`, `set` of ``Category``
        Removed categories.
    removed_commands : `None`, `set` of ``Command``
        Removed commands.
    """
    __slots__ = ('added_categories', 'added_commands', 'removed_categories', 'removed_commands',)
    
    @copy_docs(BaseSnapshotType.__new__)
    def __new__(cls, client):
        command_processor = getattr(client, 'command_processor', None)
        if (command_processor is None) or (not isinstance(command_processor, CommandProcessor)):
            added_categories = None
            added_commands = None
        
        else:
            category_name_to_category = command_processor.category_name_to_category
            if category_name_to_category:
                added_categories = set(category_name_to_category.values())
            else:
                added_categories = None
            
            commands = command_processor.commands
            if commands:
                added_commands = commands.copy()
            else:
                added_commands = None
        
        self = BaseSnapshotType.__new__(cls, client)
        
        self.added_categories = added_categories
        self.added_commands = added_commands
        self.removed_categories = None
        self.removed_commands = None
        
        return self
    

    @copy_docs(BaseSnapshotType.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        client = self.client
        if (client is not None):
            repr_parts.append(' of ')
            repr_parts.append(repr(client))
        
        added_categories = self.added_categories
        if (added_categories is not None):
            repr_parts.append(', added_categories=')
            repr_parts.append(repr(added_categories))
        
        removed_categories = self.removed_categories
        if (removed_categories is not None):
            repr_parts.append(', removed_categories=')
            repr_parts.append(repr(removed_categories))
        
        added_commands = self.added_commands
        if (added_commands is not None):
            repr_parts.append(', added_commands=')
            repr_parts.append(repr(added_commands))
        
        removed_commands = self.removed_commands
        if (removed_commands is not None):
            repr_parts.append(', removed_commands=')
            repr_parts.append(repr(removed_commands))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    @copy_docs(BaseSnapshotType._extract)
    def _extract(self, other):
        added_categories, removed_categories = _get_set_difference(
            _merge_set_groups(self.added_categories, other.removed_categories),
            _merge_set_groups(other.added_categories, self.removed_categories),
        )
        
        added_commands, removed_commands = _get_set_difference(
            _merge_set_groups(self.added_commands, other.removed_commands),
            _merge_set_groups(other.added_commands, self.removed_commands),
        )
        
        new = BaseSnapshotType._extract(self, other)
        
        new.added_categories = added_categories
        new.added_commands = added_commands
        new.removed_categories = removed_categories
        new.removed_commands = removed_commands
        
        return new
    
    
    @copy_docs(BaseSnapshotType.revert)
    def revert(self):
        BaseSnapshotType.revert(self)
        
        client = self.client
        if client is None:
            return
        
        command_processor = getattr(client, 'command_processor', None)
        if (command_processor is None) or (not isinstance(command_processor, CommandProcessor)):
            return
        
        added_commands = self.added_commands
        if (added_commands is not None):
            for command in added_commands:
                command_processor._remove_command(command)
                
        removed_commands = self.removed_commands
        if (removed_commands is not None):
            for command in removed_commands:
                command_processor._add_command(command)
        
        
        added_categories = self.added_categories
        if (added_categories is not None):
            for category in added_categories:
                command_processor._remove_category(category)
        
        
        removed_categories = self.removed_categories
        if (removed_categories is not None):
            for category in removed_categories:
                command_processor._add_category(category)
    
    
    @copy_docs(BaseSnapshotType.__bool__)
    def __bool__(self):
        if (self.added_categories is not None):
            return True
        
        if (self.added_commands is not None):
            return True
        
        if (self.removed_categories is not None):
            return True
        
        if (self.removed_commands is not None):
            return True
        
        return False
