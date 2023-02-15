__all__ = ('SlasherSnapshotType', )


from scarletio import RichAttributeErrorBaseType, copy_docs

from ..plugin_loader import BaseSnapshotType, PLUGIN_LOADER
from ..plugin_loader.snapshot.helpers import (
    _get_list_difference, _get_set_difference, _merge_list_groups, _merge_set_groups
)

from .slasher import Slasher
from .utils import RUNTIME_SYNC_HOOKS, SYNC_ID_NON_GLOBAL


class ApplicationCommandDifference(RichAttributeErrorBaseType):
    """
    Snapshot for application commands.
    
    Attributes
    ----------
    added_application_commands : `None`, `list` of ``CommandBaseApplicationCommand``
        The added application commands.
    removed_application_commands : `None`, `list` of ``CommandBaseApplicationCommand``
        The removed application commands.
    """
    __slots__ = ('added_application_commands', 'removed_application_commands',)
    
    def __new__(cls):
        """
        Creates a new application command snapshot.
        """
        self = object.__new__(cls)
        self.added_application_commands = None
        self.removed_application_commands = None
        return self
    
    def __repr__(self):
        """Returns the application command difference."""
        repr_parts = ['<', self.__class__.__name__]
        
        field_added = False
        
        added_application_commands = self.added_application_commands
        if (added_application_commands is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' added_application_commands=')
            repr_parts.append(repr(added_application_commands))
        
        removed_application_commands = self.removed_application_commands
        if (removed_application_commands is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' removed_application_commands=')
            repr_parts.append(repr(removed_application_commands))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __bool__(self):
        """Returns whether the difference contains any changes."""
        if (self.added_application_commands is not None):
            return True
        
        if (self.removed_application_commands is not None):
            return True
        
        return False
    
    
    def add(self, application_command):
        """
        Adds an application command to self.
        
        Parameters
        ----------
        application_command : ``CommandBaseApplicationCommand``
            The application command to add.
        """
        added_application_commands = self.added_application_commands
        if (added_application_commands is None):
            added_application_commands = []
            self.added_application_commands = added_application_commands
        
        removed_application_commands = self.removed_application_commands
        if (removed_application_commands is not None):
            try:
                removed_application_commands.remove(application_command)
            except ValueError:
                pass
            else:
                if not removed_application_commands:
                    self.removed_application_commands = None
        
        added_application_commands.append(application_command)
    
    
    def remove(self, application_command):
        """
        Removes the application command from self.
        
        Parameters
        ----------
        application_command : ``CommandBaseApplicationCommand``
            The application command to remove.
        """
        added_application_commands = self.added_application_commands
        if (added_application_commands is not None):
            try:
                added_application_commands.remove(application_command)
            except ValueError:
                pass
            else:
                if not added_application_commands:
                    self.added_application_commands = None
        
        removed_application_commands = self.removed_application_commands
        if (removed_application_commands is None):
            removed_application_commands = []
            self.removed_application_commands = removed_application_commands
        
        removed_application_commands.append(application_command)
    
    
    def iter_added_application_commands(self):
        """
        Iterates over the added application commands of the application command difference.
        
        This method is an iterable generator.
        
        Yields
        ------
        added_application_command : ``CommandBaseApplicationCommand``
        """
        added_application_commands = self.added_application_commands
        if (added_application_commands is not None):
            yield from added_application_commands
    
    
    def iter_removed_application_commands(self):
        """
        Iterates over the removed application commands of the application command difference.
        
        This method is an iterable generator.
        
        Yields
        ------
        removed_application_command : ``CommandBaseApplicationCommand``
        """
        removed_application_commands = self.removed_application_commands
        if (removed_application_commands is not None):
            yield from removed_application_commands
    
    
    def copy(self):
        """
        Copies the application command difference.
        
        Returns
        -------
        new : ``ApplicationCommandDifference``
        """
        added_application_commands = self.added_application_commands
        if (added_application_commands is not None):
            added_application_commands = added_application_commands.copy()
        
        removed_application_commands = self.removed_application_commands
        if (removed_application_commands is not None):
            removed_application_commands = removed_application_commands.copy()
        
        new = object.__new__(type(self))
        new.added_application_commands = added_application_commands
        new.removed_application_commands = removed_application_commands
        return new
    
    
    def revert_copy(self):
        """
        Revert copies the application command difference.
        
        Returns
        -------
        new : ``ApplicationCommandDifference``
        """
        added_application_commands = self.added_application_commands
        if (added_application_commands is not None):
            added_application_commands = added_application_commands.copy()
        
        removed_application_commands = self.removed_application_commands
        if (removed_application_commands is not None):
            removed_application_commands = removed_application_commands.copy()
        
        new = object.__new__(type(self))
        new.added_application_commands = removed_application_commands
        new.removed_application_commands = added_application_commands
        return new
    
    
    def _subtract(self, other):
        """
        Subtracts other from self.
        
        Parameters
        ----------
        other : ``ApplicationCommandDifference``
            The other difference to subtract from self.
        
        Returns
        -------
        new : ``ApplicationCommandDifference``
        """
        added_application_commands, removed_application_commands = _get_list_difference(
            _merge_list_groups(self.added_application_commands, other.removed_application_commands),
            _merge_list_groups(other.added_application_commands, self.removed_application_commands),
        )
        
        new = object.__new__(type(self))
        new.added_application_commands = added_application_commands
        new.removed_application_commands = removed_application_commands
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


class PermissionOverwriteDifference(RichAttributeErrorBaseType):
    """
    Snapshot for permission overwrites.
    
    Attributes
    ----------
    added_permission_overwrites : `None`, `list` of ``ApplicationCommandPermissionOverwrite``
        The added permission overwrites.
    removed_permission_overwrites : `None`, `list` of ``ApplicationCommandPermissionOverwrite``
        The removed permission overwrites.
    """
    __slots__ = ('added_permission_overwrites', 'removed_permission_overwrites',)
    
    def __new__(cls):
        """
        Creates a new permission overwrite snapshot.
        """
        self = object.__new__(cls)
        self.added_permission_overwrites = None
        self.removed_permission_overwrites = None
        return self
    
    def __repr__(self):
        """Returns the permission overwrite difference."""
        repr_parts = ['<', self.__class__.__name__]
        
        field_added = False
        
        added_permission_overwrites = self.added_permission_overwrites
        if (added_permission_overwrites is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' added_permission_overwrites=')
            repr_parts.append(repr(added_permission_overwrites))
        
        removed_permission_overwrites = self.removed_permission_overwrites
        if (removed_permission_overwrites is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' removed_permission_overwrites=')
            repr_parts.append(repr(removed_permission_overwrites))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __bool__(self):
        """Returns whether the difference contains any changes."""
        if (self.added_permission_overwrites is not None):
            return True
        
        if (self.removed_permission_overwrites is not None):
            return True
        
        return False
    
    
    def add(self, permission_overwrite):
        """
        Adds an permission overwrite to self.
        
        Parameters
        ----------
        permission_overwrite : ``ApplicationCommandPermissionOverwrite``
            The permission overwrite to add.
        """
        added_permission_overwrites = self.added_permission_overwrites
        if (added_permission_overwrites is None):
            added_permission_overwrites = []
            self.added_permission_overwrites = added_permission_overwrites
        
        removed_permission_overwrites = self.removed_permission_overwrites
        if (removed_permission_overwrites is not None):
            try:
                removed_permission_overwrites.remove(permission_overwrite)
            except ValueError:
                pass
            else:
                if not removed_permission_overwrites:
                    self.removed_permission_overwrites = None
        
        added_permission_overwrites.append(permission_overwrite)
    
    
    def remove(self, permission_overwrite):
        """
        Removes the permission overwrite from self.
        
        Parameters
        ----------
        permission_overwrite : ``ApplicationCommandPermissionOverwrite``
            The permission overwrite to remove.
        """
        added_permission_overwrites = self.added_permission_overwrites
        if (added_permission_overwrites is not None):
            try:
                added_permission_overwrites.remove(permission_overwrite)
            except ValueError:
                pass
            else:
                if not added_permission_overwrites:
                    self.added_permission_overwrites = None
        
        removed_permission_overwrites = self.removed_permission_overwrites
        if (removed_permission_overwrites is None):
            removed_permission_overwrites = []
            self.removed_permission_overwrites = removed_permission_overwrites
        
        removed_permission_overwrites.append(permission_overwrite)
    
    
    def iter_added_permission_overwrites(self):
        """
        Iterates over the added permission overwrites of the permission overwrite difference.
        
        This method is an iterable generator.
        
        Yields
        ------
        added_permission_overwrite : ``ApplicationCommandPermissionOverwrite``
        """
        added_permission_overwrites = self.added_permission_overwrites
        if (added_permission_overwrites is not None):
            yield from added_permission_overwrites
    
    
    def iter_removed_permission_overwrites(self):
        """
        Iterates over the removed permission overwrites of the permission overwrite difference.
        
        This method is an iterable generator.
        
        Yields
        ------
        removed_permission_overwrite : ``ApplicationCommandPermissionOverwrite``
        """
        removed_permission_overwrites = self.removed_permission_overwrites
        if (removed_permission_overwrites is not None):
            yield from removed_permission_overwrites
    
    
    def copy(self):
        """
        Copies the permission overwrite difference.
        
        Returns
        -------
        new : ``PermissionOverwriteDifference``
        """
        added_permission_overwrites = self.added_permission_overwrites
        if (added_permission_overwrites is not None):
            added_permission_overwrites = added_permission_overwrites.copy()
        
        removed_permission_overwrites = self.removed_permission_overwrites
        if (removed_permission_overwrites is not None):
            removed_permission_overwrites = removed_permission_overwrites.copy()
        
        new = object.__new__(type(self))
        new.added_permission_overwrites = added_permission_overwrites
        new.removed_permission_overwrites = removed_permission_overwrites
        return new
    
    
    def revert_copy(self):
        """
        Revert copies the permission overwrite difference.
        
        Returns
        -------
        new : ``PermissionOverwriteDifference``
        """
        added_permission_overwrites = self.added_permission_overwrites
        if (added_permission_overwrites is not None):
            added_permission_overwrites = added_permission_overwrites.copy()
        
        removed_permission_overwrites = self.removed_permission_overwrites
        if (removed_permission_overwrites is not None):
            removed_permission_overwrites = removed_permission_overwrites.copy()
        
        new = object.__new__(type(self))
        new.added_permission_overwrites = removed_permission_overwrites
        new.removed_permission_overwrites = added_permission_overwrites
        return new
    
    
    def _subtract(self, other):
        """
        Subtracts other from self.
        
        Parameters
        ----------
        other : ``PermissionOverwriteDifference``
            The other difference to subtract from self.
        
        Returns
        -------
        new : ``PermissionOverwriteDifference``
        """
        added_permission_overwrites, removed_permission_overwrites = _get_list_difference(
            _merge_list_groups(self.added_permission_overwrites, other.removed_permission_overwrites),
            _merge_list_groups(other.added_permission_overwrites, self.removed_permission_overwrites),
        )
        
        new = object.__new__(type(self))
        new.added_permission_overwrites = added_permission_overwrites
        new.removed_permission_overwrites = removed_permission_overwrites
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


class SlasherSnapshotType(BaseSnapshotType):
    """
    Slasher extension snapshot.
    
    Attributes
    ----------
    added_component_commands : `None`, `set` of ``ComponentCommand``
        The added component commands
    added_form_submit_commands : `None, `set` of ``FormSubmitCommand``
        The added form submit commands.
    application_command_differences_by_guild_id : `dict` of (`int`, ``ApplicationCommandDifference``)
        The added & removed application commands by guild id.
    permission_overwrite_difference_by_guild_id : `dict` of (`int`, ``PermissionOverwriteDifference``)
        The added & removed application command permission overwrites by guild id.
    removed_component_commands : `None`, `set` of ``ComponentCommand``
        The removed component commands
    removed_form_submit_commands : `None, `set` of ``FormSubmitCommand``
        The removed form submit commands.
    """
    __slots__ = (
        'added_component_commands', 'added_form_submit_commands', 'application_command_differences_by_guild_id',
        'permission_overwrite_difference_by_guild_id', 'removed_component_commands', 'removed_form_submit_commands',
    )
    
    
    @copy_docs(BaseSnapshotType.__new__)
    def __new__(cls, client):
        application_command_differences_by_guild_id = {}
        permission_overwrite_difference_by_guild_id = {}
        
        slasher = getattr(client, 'slasher', None)
        if (slasher is None) or (not isinstance(slasher, Slasher)):
            added_component_commands = None
            added_form_submit_commands = None
        
        else:
            command_states = slasher._command_states
            
            for guild_id, command_state in command_states.items():
                application_command_difference = ApplicationCommandDifference()
                
                if guild_id == SYNC_ID_NON_GLOBAL:
                    active_commands = command_state._active
                    if (active_commands is not None):
                        for command in active_commands:
                            application_command_difference.add(command)
                    
                else:
                    changes = command_state._changes
                    if (changes is not None):
                        for added, command in changes:
                            if added:
                                application_command_difference.add(command)
                            else:
                                application_command_difference.remove(command)
                
                if application_command_difference:
                    application_command_differences_by_guild_id[guild_id] = application_command_difference
            
            added_component_commands = slasher._component_commands
            if added_component_commands:
                added_component_commands = added_component_commands.copy()
            else:
                added_component_commands = None
            
            added_form_submit_commands = slasher._form_submit_commands
            if added_form_submit_commands:
                added_form_submit_commands = added_form_submit_commands.copy()
            else:
                added_form_submit_commands = None
            
            # permission_overwrite_difference_by_guild_id
            guild_level_permission_overwrites = slasher._guild_level_permission_overwrites
            if guild_level_permission_overwrites is not None:
                for guild_id, permission_overwrites in guild_level_permission_overwrites.items():
                    permission_overwrite_difference = PermissionOverwriteDifference()
                    for permission_overwrite in permission_overwrites:
                        permission_overwrite_difference.add(permission_overwrite)
                    
                    if permission_overwrite_difference:
                        permission_overwrite_difference_by_guild_id[guild_id] = permission_overwrite_difference
        
        
        self = BaseSnapshotType.__new__(cls, client)
        
        self.added_component_commands = added_component_commands
        self.added_form_submit_commands = added_form_submit_commands
        self.application_command_differences_by_guild_id = application_command_differences_by_guild_id
        self.permission_overwrite_difference_by_guild_id = permission_overwrite_difference_by_guild_id
        self.removed_component_commands = None
        self.removed_form_submit_commands = None
        
        return self
    
    
    @copy_docs(BaseSnapshotType.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        client = self.client
        if (client is not None):
            repr_parts.append(' of ')
            repr_parts.append(repr(client))
        
        application_command_differences_by_guild_id = self.application_command_differences_by_guild_id
        if application_command_differences_by_guild_id:
            repr_parts.append(', application_command_differences_by_guild_id = ')
            repr_parts.append(repr(application_command_differences_by_guild_id))
        
        permission_overwrite_difference_by_guild_id = self.permission_overwrite_difference_by_guild_id
        if permission_overwrite_difference_by_guild_id:
            repr_parts.append(', permission_overwrite_difference_by_guild_id = ')
            repr_parts.append(repr(permission_overwrite_difference_by_guild_id))
        
        added_component_commands = self.added_component_commands
        if (added_component_commands is not None):
            repr_parts.append(', added_component_commands = ')
            repr_parts.append(repr(added_component_commands))
            
        removed_component_commands = self.removed_component_commands
        if (removed_component_commands is not None):
            repr_parts.append(', removed_component_commands = ')
            repr_parts.append(repr(removed_component_commands))
        
        added_form_submit_commands = self.added_form_submit_commands
        if (added_form_submit_commands is not None):
            repr_parts.append(', added_form_submit_commands = ')
            repr_parts.append(repr(added_form_submit_commands))
        
        removed_form_submit_commands = self.removed_form_submit_commands
        if (removed_form_submit_commands is not None):
            repr_parts.append(', removed_form_submit_commands = ')
            repr_parts.append(repr(removed_form_submit_commands))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(BaseSnapshotType._extract)
    def _extract(self, other):
        self_application_command_differences_by_guild_id = self.application_command_differences_by_guild_id
        other_application_command_differences_by_guild_id = other.application_command_differences_by_guild_id
        
        new_application_command_differences_by_guild_id = {}
        
        for guild_id in {
            *self_application_command_differences_by_guild_id.keys(),
            *other_application_command_differences_by_guild_id.keys(),
        }:
            new_application_command_difference = (
                self_application_command_differences_by_guild_id.get(guild_id, None) -
                other_application_command_differences_by_guild_id.get(guild_id, None)
            )
            
            if new_application_command_difference:
                new_application_command_differences_by_guild_id[guild_id] = new_application_command_difference
        
        
        self_permission_overwrite_difference_by_guild_id = self.permission_overwrite_difference_by_guild_id
        other_permission_overwrite_difference_by_guild_id = other.permission_overwrite_difference_by_guild_id
        
        new_permission_overwrite_difference_by_guild_id = {}
        
        for guild_id in {
            *self_permission_overwrite_difference_by_guild_id.keys(),
            *other_permission_overwrite_difference_by_guild_id.keys(),
        }:
            new_application_command_difference = (
                self_permission_overwrite_difference_by_guild_id.get(guild_id, None) -
                other_permission_overwrite_difference_by_guild_id.get(guild_id, None)
            )
            
            if new_application_command_difference:
                new_permission_overwrite_difference_by_guild_id[guild_id] = new_application_command_difference
        
        
        added_component_commands, removed_component_commands = _get_set_difference(
            _merge_set_groups(self.added_component_commands, other.removed_component_commands),
            _merge_set_groups(other.added_component_commands, self.removed_component_commands),
        )
        
        added_form_submit_commands, removed_form_submit_commands = _get_set_difference(
            _merge_set_groups(self.added_form_submit_commands, other.removed_form_submit_commands),
            _merge_set_groups(other.added_form_submit_commands, self.removed_form_submit_commands),
        )
        
        new = BaseSnapshotType._extract(self, other)
        
        new.added_component_commands = added_component_commands
        new.added_form_submit_commands = added_form_submit_commands
        new.application_command_differences_by_guild_id = new_application_command_differences_by_guild_id
        new.permission_overwrite_difference_by_guild_id = new_permission_overwrite_difference_by_guild_id
        new.removed_component_commands = removed_component_commands
        new.removed_form_submit_commands = removed_form_submit_commands
        
        client = self.client
        if client.running and client.application.id:
            slasher = getattr(client, 'slasher', None)
            if (slasher is not None):
                PLUGIN_LOADER.add_done_callback_unique(slasher.sync)
        
        return new
    
    
    @copy_docs(BaseSnapshotType.revert)
    def revert(self):
        BaseSnapshotType.revert(self)
        
        client = self.client
        if client is None:
            return

        slasher = getattr(client, 'slasher', None)
        if (slasher is None) or (not isinstance(slasher, Slasher)):
            return
        
        for application_command_difference in self.application_command_differences_by_guild_id.values():
            for application_command in application_command_difference.iter_added_application_commands():
                slasher._remove_application_command(application_command)
            
            for application_command in application_command_difference.iter_removed_application_commands():
                slasher._add_application_command(application_command)
        
        for guild_id, permission_overwrite_difference in self.permission_overwrite_difference_by_guild_id.items():
            for permission_overwrite in permission_overwrite_difference.iter_added_permission_overwrites():
                slasher._remove_permission_overwrite_for_guild(guild_id, permission_overwrite)
            
            for permission_overwrite in permission_overwrite_difference.iter_removed_permission_overwrites():
                slasher._add_permission_overwrites_for_guild(guild_id, permission_overwrite)
        
        
        added_component_commands = self.added_component_commands
        if (added_component_commands is not None):
            for component_command in added_component_commands:
                slasher._remove_component_command(component_command)
        
        
        removed_component_commands = self.removed_component_commands
        if (removed_component_commands is not None):
            for component_command in removed_component_commands:
                slasher._add_component_command(component_command)
        
        added_form_submit_commands = self.added_form_submit_commands
        if (added_form_submit_commands is not None):
            for form_submit_command in added_form_submit_commands:
                slasher._remove_form_submit_command(form_submit_command)
        
        removed_form_submit_commands = self.removed_form_submit_commands
        if (removed_form_submit_commands is not None):
            for form_submit_command in removed_form_submit_commands:
                slasher._add_form_submit_command(form_submit_command)
    
    
    @copy_docs(BaseSnapshotType.__bool__)
    def __bool__(self):
        if (self.added_component_commands is not None):
            return True
        
        if (self.added_form_submit_commands is not None):
            return True
        
        if self.application_command_differences_by_guild_id:
            return True
        
        if self.permission_overwrite_difference_by_guild_id:
            return True
        
        if (self.removed_component_commands is not None):
            return True
        
        if (self.removed_form_submit_commands is not None):
            return True
        
        return False


def runtime_sync_hook_is_executing_extension(client):
    """
    Runtime sync hook to check whether a slash command should be registered and synced instantly when added or removed.
    
    Parameters
    ----------
    client : ``Client``
        The respective client of the ``Slasher``.
    """
    return not PLUGIN_LOADER.is_processing_plugin()

RUNTIME_SYNC_HOOKS.append(runtime_sync_hook_is_executing_extension)
