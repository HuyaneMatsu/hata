__all__ = ('CommandBaseApplicationCommand',)

from scarletio import copy_docs

from .....discord.interaction import ApplicationCommand, ApplicationCommandTargetType
from .....discord.interaction.application_command.constants import APPLICATION_COMMAND_PERMISSION_OVERWRITE_MAX

from ...utils import SYNC_ID_GLOBAL, SYNC_ID_NON_GLOBAL, UNLOADING_BEHAVIOUR_DELETE, UNLOADING_BEHAVIOUR_INHERIT

from ..command_base import CommandBase


class CommandBaseApplicationCommand(CommandBase):
    """
    Base class for ``Slasher``'s application commands.
    
    Attributes
    ----------
    _exception_handlers : `None`, `list` of `CoroutineFunction`
        Exception handlers added with ``.error`` to the interaction handler.
        
        Same as ``Slasher._exception_handlers``.
    
    _parent_reference : `None`, ``WeakReferer`` to ``Slasher``
        Reference to the slasher application command's parent.
    
    name : `str`
        Application command name. It's length can be in range [1:32].
    
    _permission_overwrites : `None`, `dict` of (`int`, `list` of ``ApplicationCommandPermissionOverwrite``)
        Permission overwrites applied to the slash command.

    _registered_application_command_ids : `None`, `dict` of (`int`, `int`) items
        The registered application command ids, which are matched by the command's schema.
        
        If empty set as `None`, if not then the keys are the respective guild's id and the values are the application
        command id.
    
    _schema : `None`, ``ApplicationCommand``
        Internal slot used by the ``.get_schema`` method.
    
    _unloading_behaviour : `int`
        Behaviour what describes what should happen when the command is removed from the slasher.
        
        Can be any of the following:
        
        +-------------------------------+-------+
        | Respective name               | Value |
        +-------------------------------+-------+
        | UNLOADING_BEHAVIOUR_DELETE    | 0     |
        +-------------------------------+-------+
        | UNLOADING_BEHAVIOUR_KEEP      | 1     |
        +-------------------------------+-------+
        | UNLOADING_BEHAVIOUR_INHERIT   | 2     |
        +-------------------------------+-------+
    
    allow_by_default : `None`, `bool`
        Whether the command is enabled by default for everyone who has `use_application_commands` permission.

    guild_ids : `None`, `set` of `int`
        The ``Guild``'s id to which the command is bound to.
    
    is_global : `bool`
        Whether the command is a global command.
        
        Guild commands have ``.guild_ids`` set as `None`.
    
    required_permissions : `None`, ``Permission``
        The required permissions to use the application command inside of a guild.
    
    Class Attributes
    ----------------
    COMMAND_COMMAND_NAME : `str`
        The command's name defining parameter's name.
    COMMAND_PARAMETER_NAMES : `tuple` of `str`
        All parameters names accepted by ``.__new__``
    COMMAND_NAME_NAME : `str`
        The command's "command" defining parameter's name.
    
    description : `None` = `None`
        The command's description.
        
        Subclasses might overwrite it.
    
    target : ``ApplicationCommandTargetType`` = `ApplicationCommandTargetType.none`
        The command's target type.
        
        Subclasses might overwrite it.
    """
    __slots__ = (
        '_permission_overwrites', '_registered_application_command_ids', '_schema', '_unloading_behaviour',
        'allow_by_default', 'allow_in_dm', 'guild_ids', 'is_default', 'is_global',
        'required_permissions',
    )
    
    COMMAND_PARAMETER_NAMES = (
        *CommandBase.COMMAND_PARAMETER_NAMES,
        'delete_on_unload',
        'guild',
        'is_global',
        'required_permissions',
    )
    
    description = None
    target = ApplicationCommandTargetType.none
    
    @copy_docs(CommandBase.copy)
    def copy(self):
        new = CommandBase.copy(self)
        
        # _permission_overwrites
        permission_overwrites = self._permission_overwrites
        if (permission_overwrites is not None):
            permission_overwrites = {
                guild_id: permission_overwrite.copy() for
                guild_id, permission_overwrite in permission_overwrites.items()
            }
        new._permission_overwrites = permission_overwrites
        
        # _registered_application_command_ids
        new._registered_application_command_ids = None
        
        # _schema
        new._schema = None
        
        # _unloading_behaviour
        new._unloading_behaviour = self._unloading_behaviour
        
        # allow_by_default
        new.allow_by_default = self.allow_by_default
        
        # allow_in_dm
        new.allow_in_dm = self.allow_in_dm
        
        # guild_ids
        guild_ids = self.guild_ids
        if (guild_ids is not None):
            guild_ids = guild_ids.copy()
        new.guild_ids = guild_ids
        
        # is_global
        new.is_global = self.is_global
        
        # required_permissions
        new.required_permissions = self.required_permissions
        
        return new
    
    
    @copy_docs(CommandBase.__hash__)
    def __hash__(self):
        hash_value = CommandBase.__hash__(self)
        
        # _permission_overwrites
        permission_overwrites = self._permission_overwrites
        if (permission_overwrites is not None):
            
            hash_value ^= len(permission_overwrites) << 8
            
            for permission_overwrite in permission_overwrites:
                hash_value ^= hash(permission_overwrite)
        
        # _registered_application_command_ids
        # Internal Field
        
        # _unloading_behaviour
        hash_value ^= (self._unloading_behaviour + 1) << 12
        
        # allow_by_default
        allow_by_default = self.allow_by_default
        if (allow_by_default is not None):
            hash_value ^= allow_by_default << 16
        
        # allow_by_default
        allow_in_dm = self.allow_in_dm
        if (allow_in_dm is not None):
            hash_value ^= allow_in_dm << 17
        
        # guild_ids
        guild_ids = self.guild_ids
        if (guild_ids is not None):
            hash_value ^= len(guild_ids) << 18
            
            for guild_id in guild_ids:
                hash_value ^= guild_id
        
        # required_permissions
        required_permissions = self.required_permissions
        if (required_permissions is not None):
            hash_value ^= required_permissions
        
        return hash_value
    
    
    @copy_docs(CommandBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        if not CommandBase._is_equal_same_type(self, other):
            return False
        
        # _permission_overwrites
        if self._permission_overwrites != other._permission_overwrites:
            return False
        
        # _registered_application_command_ids
        # Internal field

        # _unloading_behaviour
        if self._unloading_behaviour != other._unloading_behaviour:
            return False
        
        # allow_by_default
        if self.allow_by_default != other.allow_by_default:
            return False
        
        # allow_in_dm
        if self.allow_in_dm != other.allow_in_dm:
            return False
        
        # guild_ids
        if self.guild_ids != other.guild_ids:
            return False
        
        # is_global
        if self.is_global != other.is_global:
            return False
        
        # required_permissions
        if self.required_permissions != other.required_permissions:
            return False
        
        return True
    
    
    @copy_docs(CommandBase._cursed_repr_builder)
    def _cursed_repr_builder(self):
        for repr_parts in CommandBase._cursed_repr_builder(self):
            
            repr_parts.append(', type=')
            guild_ids = self.guild_ids
            if guild_ids is None:
                if self.is_global:
                    type_name = 'global'
                else:
                    type_name = 'non-global'
            else:
                type_name = 'guild bound'
            
            repr_parts.append(type_name)
            
            yield repr_parts
            
            allow_by_default = self.allow_by_default
            if (allow_by_default is not None):
                repr_parts.append(', allow_by_default=')
                repr_parts.append(repr(allow_by_default))
            
            allow_in_dm = self.allow_in_dm
            if (allow_in_dm is not None):
                repr_parts.append(', allow_in_dm=')
                repr_parts.append(repr(allow_in_dm))
            
            required_permissions = self.required_permissions
            if (required_permissions is not None):
                repr_parts.append(', required_permissions=')
                repr_parts.append(repr(required_permissions))
            
            unloading_behaviour = self._unloading_behaviour
            if unloading_behaviour != UNLOADING_BEHAVIOUR_INHERIT:
                repr_parts.append(', unloading_behaviour=')
                if unloading_behaviour == UNLOADING_BEHAVIOUR_DELETE:
                    unloading_behaviour_name = 'delete'
                else:
                    unloading_behaviour_name = 'keep'
                
                repr_parts.append(unloading_behaviour_name)
            
            if (guild_ids is not None):
                repr_parts.append(', guild_ids=')
                repr_parts.append(repr(guild_ids))
    
    
    async def invoke_auto_completion(self, client, interaction_event, auto_complete_option):
        """
        Calls the auto completion function of the slasher application command.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client who received the event.
        interaction_event : ``InteractionEvent``
            The received interaction event.
        auto_complete_option : ``ApplicationCommandAutocompleteInteraction``
            The option to autocomplete.
        """
        pass
    
    # ---- Utility ----
    
    def get_real_command_count(self):
        """
        Gets the real command count of the command. This includes every sub attached to it as well.
        
        Returns
        -------
        real_command_count: `int`
        """
        return 1
    
    @property
    def interactions(self):
        """
        Enables you to add sub-commands or sub-categories to the command.
        
        Raises
        ------
        RuntimeError
            The ``CommandBaseApplicationCommand`` is not a category.
        """
        raise RuntimeError(
            f'The {self.__class__.__name__} is not a category.'
        )
    
    
    def autocomplete(self, parameter_name, *parameter_names, function=None):
        """
        Registers an auto completer function to the application command.
        
        Can be used as a decorator, as:
        
        ```py
        @bot.interactions(is_global=True)
        async def buy(
            item: ('str', 'Select an item to buy.'),
        ):
            return 'Great success.'
        
        AUTO_COMPLETE_CHOICES = (
            'cake',
            'shrimp fry',
        )
        
        @buy.autocomplete('item')
        async def autocomplete_item_parameter(value):
            if value is None:
                return AUTO_COMPLETE_CHOICES[:20]
            
            value = value.lower()
            
            return [choice for choice in AUTO_COMPLETE_CHOICES if choice.startswith(value)]
        ```
        
        Parameters
        ----------
        parameter_name : `str`
            The parameter's name.
        *parameter_names : `str`
            Additional parameter names to autocomplete
        function : `None`, `async-callable` = `None`, Optional (Keyword only)
            The function to register as auto completer.
        
        Returns
        -------
        function / wrapper : `async-callable`, `functools.partial`
            The registered function if given or a wrapper to register the function with.
        
        Raises
        ------
        RuntimeError
            - If the parameter already has a auto completer defined.
            - If the application command function has no parameter named, like `parameter_name`.
            - If the parameter cannot be auto completed.
        TypeError
            If `function` is not an asynchronous.
        """
        raise RuntimeError(
            f'{self.__class__.__name__} is not auto-completable.'
        )
    
    
    # ---- Permission overwrites ----

    def add_permission_overwrite(self, guild_id, permission_overwrite):
        """
        Adds an overwrite to the slash command.
        
        Parameters
        ----------
        guild_id : `int`
            The guild's id where the overwrite will be applied.
        permission_overwrite : ``ApplicationCommandPermissionOverwrite``, `None`
            The permission overwrite to add
        
        Raises
        ------
        AssertionError
            - Each command in each guild can have up to `10` overwrite, which is already reached.
        """
        permission_overwrites = self._permission_overwrites
        if permission_overwrites is None:
            self._permission_overwrites = permission_overwrites = {}
        
        permission_overwrites_for_guild = permission_overwrites.get(guild_id, None)
        
        if __debug__:
            if (
                (permission_overwrites_for_guild is not None) and
                (len(permission_overwrites_for_guild) >= APPLICATION_COMMAND_PERMISSION_OVERWRITE_MAX)
            ):
                raise AssertionError(
                    f'`Each command in each guild can have up to '
                    f'{APPLICATION_COMMAND_PERMISSION_OVERWRITE_MAX} permission overwrites which is already reached.'
                )
        
        if (permission_overwrites_for_guild is not None) and (permission_overwrite is not None):
            target_id = permission_overwrite.target_id
            for index in range(len(permission_overwrites_for_guild)):
                iter_permission_overwrites = permission_overwrites_for_guild[index]
                
                if iter_permission_overwrites.target_id != target_id:
                    continue
                
                if permission_overwrite.allow == iter_permission_overwrites.allow:
                    return
                
                del permission_overwrites_for_guild[index]
                
                if permission_overwrites_for_guild:
                    return
                
                permission_overwrites[guild_id] = None
                return
        
        if permission_overwrite is None:
            if permission_overwrites_for_guild is None:
                permission_overwrites[guild_id] = None
        else:
            if permission_overwrites_for_guild is None:
                permission_overwrites[guild_id] = permission_overwrites_for_guild = []
            
            permission_overwrites_for_guild.append(permission_overwrite)
    
    
    def get_permission_overwrites_for(self, guild_id):
        """
        Returns the slash command's permissions overwrites for the given guild.
        
        Returns
        -------
        permission_overwrites : `None`, `list` of ``ApplicationCommandPermissionOverwrite``
            Returns `None` instead of an empty list.
        """
        permission_overwrites = self._permission_overwrites
        if (permission_overwrites is not None):
            return permission_overwrites.get(guild_id, None)
    
    # ---- Sync ----
    
    def _get_permission_sync_ids(self):
        """
        Gets the permission overwrite guild id-s which should be synced.
        
        Returns
        -------
        permission_sync_ids : `set` of `int`
        """
        permission_sync_ids = set()
        guild_ids = self.guild_ids
        # If the command is guild bound, sync it in every guild, if not, then sync it in every guild where it has an
        # a permission overwrite.
        if (guild_ids is None):
            permission_overwrites = self._permission_overwrites
            if (permission_overwrites is not None):
                permission_sync_ids.update(permission_overwrites.keys())
        else:
            permission_sync_ids.update(guild_ids)
        
        return permission_sync_ids


    def _register_guild_and_application_command_id(self, guild_id, application_command_id):
        """
        Registers an application command's identifier to the ``SlashCommand`.
        
        Parameters
        ----------
        application_command_id : `int`
            The application command's identifier.
        guild_id : `int`
            The guild where the application command is in.
        """
        registered_application_command_ids = self._registered_application_command_ids
        if registered_application_command_ids is None:
            registered_application_command_ids = self._registered_application_command_ids = {}
        
        registered_application_command_ids[guild_id] = application_command_id
    
    
    def _unregister_guild_and_application_command_id(self, guild_id, application_command_id):
        """
        Unregisters an application command's identifier from the ``SlashCommand`.
        
        Parameters
        ----------
        guild_id : `int`
            The guild's id, where the application command is in.
        application_command_id : `int`
            The application command's identifier.
        """
        registered_application_command_ids = self._registered_application_command_ids
        if registered_application_command_ids is not None:
            try:
                maybe_application_command_id = registered_application_command_ids[guild_id]
            except KeyError:
                pass
            else:
                if maybe_application_command_id == application_command_id:
                    del registered_application_command_ids[guild_id]
                    
                    if not registered_application_command_ids:
                        self._registered_application_command_ids = None
    
    
    def _pop_command_id_for(self, guild_id):
        """
        Pops the given application command id from the command for the respective guild.
        
        Parameters
        ----------
        guild_id : `int`
            A guild's identifier.
        
        Returns
        -------
        application_command_id : `int`
            The popped application command's identifier. Returns `0` if nothing is matched.
        """
        registered_application_command_ids = self._registered_application_command_ids
        if registered_application_command_ids is None:
            application_command_id = 0
        else:
            application_command_id = registered_application_command_ids.pop(guild_id, 0)
        
        return application_command_id
    
    
    def _iter_application_command_ids(self):
        """
        Iterates over all the registered application command id-s added to the slash command.
        
        This method is a generator, what should be used inside of a `for` loop.
        
        Yields
        ------
        application_command_id : `int`
        """
        registered_application_command_ids = self._registered_application_command_ids
        if (registered_application_command_ids is not None):
            yield from registered_application_command_ids.values()
    
    
    def _exhaust_application_command_ids(self):
        """
        Iterates over all the registered application command id-s added to the slash command and removes them.
        
        This method is a generator, what should be used inside of a `for` loop.
        
        Yields
        ------
        application_command_id : `int`
        """
        registered_application_command_ids = self._registered_application_command_ids
        if (registered_application_command_ids is not None):
            while registered_application_command_ids:
                guild_id, application_command_id = registered_application_command_ids.popitem()
                yield application_command_id
            
            self._registered_application_command_ids = None
    
    
    def _iter_sync_ids(self):
        """
        Iterates over all the respective sync ids of the command. If the command is a guild bound command, then will
        iterate over it's guild's id-s.
        
        This method is a generator, what should be used inside of a `for` loop.
        
        Yields
        ------
        sync_id : `int`
        """
        if self.is_global:
            yield SYNC_ID_GLOBAL
            return
        
        guild_ids = self.guild_ids
        if guild_ids is None:
            yield SYNC_ID_NON_GLOBAL
            return
        
        yield from guild_ids
    
    
    def _iter_guild_ids(self):
        """
        Iterates over all the guild identifiers used by the command.
        
        Yields
        ------
        guild_id : `int`
        """
        registered_application_command_ids = self._registered_application_command_ids
        if registered_application_command_ids is not None:
            for sync_id in registered_application_command_ids:
                if sync_id > (1 << 22):
                    yield sync_id
    
    # ---- Schema ----

    def get_schema(self):
        """
        Returns an application command schema representing the slash command.
        
        Returns
        -------
        schema : ``ApplicationCommand``
        """
        schema = self._schema
        if schema is None:
            schema = self._schema = self.as_schema()
        
        return schema
    
    
    def as_schema(self):
        """
        Creates a new application command schema representing the slash command.
        
        Returns
        -------
        schema : ``ApplicationCommand``
        """
        schema = ApplicationCommand(
            self.name,
            self.description,
            allow_by_default = self.allow_by_default,
            allow_in_dm = self.allow_in_dm,
            options = self._get_schema_options(),
            required_permissions = self.required_permissions,
            target_type = self.target,
        )
        
        parent_reference = self._parent_reference
        if (parent_reference is not None):
            parent = parent_reference()
            if (parent is not None):
                schema.apply_translation(parent._translation_table)
        
        return schema
    
    
    def _get_schema_options(self):
        """
        Gets the schema options for the application command.
        
        Returns
        -------
        application_command_options : `None`, `list` of ``ApplicationCommandOption``
        """
        return None