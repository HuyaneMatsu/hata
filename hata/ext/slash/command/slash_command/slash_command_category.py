__all__ = ('SlashCommandCategory',)

from scarletio import RichAttributeErrorBaseType, copy_docs, include

from .....discord.application_command import ApplicationCommandOption, ApplicationCommandOptionType
from .....discord.application_command.application_command.constants import (
    OPTIONS_MAX as APPLICATION_COMMAND_OPTIONS_MAX
)
from .....discord.client import Client
from .....discord.interaction import InteractionEvent

from ...constants import (
    APPLICATION_COMMAND_CATEGORY_DEEPNESS_MAX, APPLICATION_COMMAND_OPTION_TYPE_SUB_COMMAND,
    APPLICATION_COMMAND_OPTION_TYPE_SUB_COMMAND_CATEGORY
)
from ...exceptions import SlashCommandParameterConversionError, handle_command_exception
from ...interfaces.autocomplete import AutocompleteInterface
from ...interfaces.exception_handler import ExceptionHandlerInterface
from ...interfaces.nestable import NestableInterface
from ...interfaces.self_reference import SelfReferenceInterface

from ..command_base import CommandBase

from .helpers import _reset_parent_schema
from .slash_command_parameter_auto_completer import SlashCommandParameterAutoCompleter


Slasher = include('Slasher')
SlashCommand = include('SlashCommand')


class SlashCommandCategory(
    AutocompleteInterface,
    ExceptionHandlerInterface,
    NestableInterface,
    SelfReferenceInterface,
    RichAttributeErrorBaseType,
):
    """
    Represents an application command's backend implementation.
    
    Attributes
    ----------
    _auto_completers : `None | list<SlashCommandParameterAutoCompleter>`
        Auto completer functions by.
    
    _deepness : `int`
        How nested the category is.
    
    _exception_handlers : `None | list<CoroutineFunction>`
        Exception handlers added with ``.error`` to the interaction handler.
    
    _parent_reference : `None | WeakReferer<SelfReferenceInterface>`
        The parent slash command of the category if any.
    
    _self_reference : `None | WeakReferer<instance>`
        Back reference to the slasher application command category.
        
        Used by sub commands to access the parent entity.
    
    _sub_commands : `None | dict<str, SlashCommandFunction | SlashCommandCategory>`
        The sub-commands of the category.
    
    default : `bool`
        Whether the command is the default command in it's category.
    
    description : `str`
        The slash command's description.
    
    name : `str`
        The name of the slash sub-category.
    """
    __slots__ = (
        '__weakref__', '_auto_completers', '_deepness', '_exception_handlers', '_parent_reference',  '_self_reference',
        '_sub_commands', 'default', 'description', 'name'
    )
    
    def __new__(cls, name, description, default, deepness):
        """
        Creates a new slash command category.
        
        Parameters
        ----------
        name : `str`
            The name of the slash command.
        
        description : `str`
            The slash command's description.
        
        default : `bool`
            Whether the command is the default command in it's category.
        
        deepness : `int`
            How nested the category is.
        
        Raises
        ------
        RuntimeError
            Maximum deepness reached.
        """
        if deepness > APPLICATION_COMMAND_CATEGORY_DEEPNESS_MAX:
            raise RuntimeError('Maximum deepness reached. Cannot add anymore sub-category under sub-categories.')
        
        self = object.__new__(cls)
        self._auto_completers = None
        self._deepness = deepness
        self._exception_handlers = None
        self._parent_reference = None
        self._self_reference = None
        self._sub_commands = None
        self.default = default
        self.description = description
        self.name = name
        
        return self
    
    
    def __repr__(self):
        """Returns the slash command category's representation."""
        repr_parts = ['<', type(self).__name__]
        
        # name
        repr_parts.append(' name = ')
        repr_parts.append(repr(self.name))
        
        # description
        repr_parts.append(', description = ')
        repr_parts.append(repr(self.description))
        
        # default
        default = self.default
        if default:
            repr_parts.append(', default = ')
            repr_parts.append(repr(default))
        
        # _exception_handlers
        exception_handlers = self._exception_handlers
        if (exception_handlers is not None):
            repr_parts.append(', exception_handlers = ')
            repr_parts.append(repr(exception_handlers))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the slash command category's hash value."""
        hash_value = 0
        
        # _auto_completers
        auto_completers = self._auto_completers
        if (auto_completers is not None):
            hash_value ^= len(auto_completers)
            
            for auto_completer in auto_completers:
                hash_value ^= hash(auto_completer)
        
        # _deepness
        # Internal field
        
        # _exception_handlers
        exception_handlers = self._exception_handlers
        if (exception_handlers is not None):
            hash_value ^= len(exception_handlers) << 4
            
            for exception_handler in exception_handlers:
                try:
                    exception_handler_hash_value = hash(exception_handler)
                except TypeError:
                    exception_handler_hash_value = object.__hash__(exception_handler)
                hash_value ^= exception_handler_hash_value
        
        # _self_reference
        # Internal field
        
        # _sub_commands
        sub_commands = self._sub_commands
        if (sub_commands is not None):
            hash_value ^= len(sub_commands) << 8
            
            for sub_command in sub_commands:
                hash_value ^= hash(sub_command)
        
        # _parent_reference
        # Internal field
        
        # default
        hash_value ^= self.default << 12
        
        # description
        description = self.description
        hash_value ^= hash(description)
        
        # name
        name = self.name
        if name != description:
            hash_value ^= hash(name)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two slash commands categories are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # _auto_completers
        if self._auto_completers != other._auto_completers:
            return False
        
        # _deepness
        # Internal Field
        
        # _exception_handlers
        if self._exception_handlers != other._exception_handlers:
            return False
        
        # _self_reference
        # Internal Field
        
        # _sub_commands
        if self._sub_commands != other._sub_commands:
            return False
        
        # _parent_reference
        # Internal Field
        
        # default
        if self.default != other.default:
            return False
        
        # description
        if self.description != other.description:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        return True
    
    
    def __format__(self, code):
        """Formats the command in a format string."""
        if not code:
            return str(self)
        
        if code == 'm':
            return self.mention
        
        raise ValueError(
            f'Unknown format code {code!r} for {type(self).__name__}; {self!r}. '
            f'Available format codes: {""!r}, {"m"!r}.'
        )
    
    
    async def invoke(self, client, interaction_event, options):
        """
        Calls the slash command category.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client who received the event.
        
        interaction_event : ``InteractionEvent``
            The received interaction event.
        
        options : `None | list<InteractionEventChoice>`
            Options bound to the category.
        """
        sub_commands = self._sub_commands
        if sub_commands is None:
            return
        
        if (options is None) or len(options) != 1:
            return
        
        option = options[0]
        
        try:
            sub_command = sub_commands[option.name]
        except KeyError:
            pass
        else:
            await sub_command.invoke(client, interaction_event, option.options)
            return
        
        # Do not put this into the `except` branch.
        await handle_command_exception(
            self,
            client,
            interaction_event,
            SlashCommandParameterConversionError(
                None,
                option.name,
                'sub-command',
                [*sub_commands.keys()],
            )
        )
        return
    
    
    def copy(self):
        """
        Copies the slash command category.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        
        # _auto_completers
        auto_completers = self._auto_completers
        if (auto_completers is not None):
            auto_completers = auto_completers.copy()
        new._auto_completers = auto_completers
        
        # _deepness
        new._deepness = self._deepness
        
        # _exception_handlers
        exception_handlers = self._exception_handlers
        if (exception_handlers is not None):
            exception_handlers = exception_handlers.copy()
        new._exception_handlers = exception_handlers
        
        # _self_reference
        new._self_reference = None
        
        # _sub_commands
        sub_commands = self._ub_commands
        if (sub_commands is not None):
            sub_commands = {name: category.copy() for name, category in sub_commands.items()}
        new._sub_commands = sub_commands
        
        # _parent_reference
        new._parent_reference = None
        
        # default
        new.default = self.default
        
        # description
        new.description = self.description
        
        # name
        new.name = self.name
        
        return new
    
    
    async def invoke_auto_completion(self, client, interaction_event, auto_complete_option):
        """
        Calls the respective auto completion function of the command.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The respective client who received the event.
        interaction_event : ``InteractionEvent``
            The received interaction event.
        auto_complete_option : `InteractionMetadataApplicationCommandAutocomplete | InteractionOption`
            The option to autocomplete.
        """
        auto_complete_option_type = auto_complete_option.type
        if (
            (auto_complete_option_type is APPLICATION_COMMAND_OPTION_TYPE_SUB_COMMAND) or
            (auto_complete_option_type is APPLICATION_COMMAND_OPTION_TYPE_SUB_COMMAND_CATEGORY)
        ):
            options = auto_complete_option.options
            if (options is not None):
                option = options[0]
                sub_commands = self._sub_commands
                if (sub_commands is not None):
                    try:
                        sub_command = sub_commands[option.name]
                    except KeyError:
                        pass
                    else:
                        await sub_command.invoke_auto_completion(client, interaction_event, option)
    
    
    @copy_docs(NestableInterface._make_command_instance_from_parameters)
    def _make_command_instance_from_parameters(self, function, positional_parameters, keyword_parameters):
        return SlashCommand(function, *positional_parameters, **keyword_parameters)
    
    
    @copy_docs(NestableInterface._store_command_instance)
    def _store_command_instance(self, command):
        if isinstance(command, SlashCommand):
            instance = self._add_application_command(command)
            return True, instance
        
        return False, None
    
    
    def _add_application_command(self, command):
        """
        Adds a sub-command or sub-category to the slash command.
        
        Parameters
        ----------
        command : ``SlashCommand``
            The slash command to add.
        
        Returns
        -------
        as_sub_command : `SlashCommandFunction | SlashCommandCategory`
            The command as sub-command.
        
        Raises
        ------
        RuntimeError
            - The ``SlashCommand`` reached the maximal amount of children.
            - Cannot add anymore sub-category under sub-categories.
            - If the command to add is a default sub-command meanwhile the category already has one.
        """
        sub_commands = self._sub_commands
        if (
            (sub_commands is not None) and
            (len(sub_commands) == APPLICATION_COMMAND_OPTIONS_MAX) and
            (command.name not in sub_commands)
        ):
            raise RuntimeError(
                f'The {type(self).__name__} reached the maximal amount of children '
                f'({APPLICATION_COMMAND_OPTIONS_MAX}).'
            )
        
        as_sub_command = command.as_sub_command(self._deepness + 1)
        
        if (sub_commands is not None) and command.default:
            for sub_command in sub_commands.values():
                if sub_command.default and (sub_command.name != command.name):
                    raise RuntimeError(
                        f'{self!r} already has a default command.'
                    )
        
        as_sub_command._parent_reference = self.get_self_reference()
        
        if sub_commands is None:
            sub_commands = {}
            self._sub_commands = sub_commands
        
        sub_commands[command.name] = as_sub_command
        
        _reset_parent_schema(self)
        
        # Resolve auto completers recursively
        parent = self
        while True:
            auto_completers = parent._auto_completers
            if (auto_completers is not None):
                for auto_completer in auto_completers:
                    as_sub_command._try_resolve_auto_completer(auto_completer)
            
            if isinstance(parent, Slasher):
                break
            
            parent_reference = parent._parent_reference
            if (parent_reference is None):
                break
            
            parent = parent_reference()
            if (parent is None):
                break
        
        return as_sub_command
    
    
    @copy_docs(AutocompleteInterface._register_auto_completer)
    def _register_auto_completer(self, function, parameter_names):
        auto_completer = self._make_auto_completer(function, parameter_names)
        self._store_auto_completer(auto_completer)
        
        resolved = 0
        sub_commands = self._sub_commands
        if (sub_commands is not None):
            for sub_command in sub_commands.values():
                resolved += sub_command._try_resolve_auto_completer(auto_completer)
        
        if resolved:
            _reset_parent_schema(self)
        
        
        return auto_completer
    
    
    def _try_resolve_auto_completer(self, auto_completer):
        """
        Tries to register auto completer to the slasher application command function.
        
        Parameters
        ----------
        auto_completer : ``SlashCommandParameterAutoCompleter``
            The auto completer.
        
        Returns
        -------
        resolved : `int`
            The amount of parameters resolved.
        """
        resolved = 0
        
        sub_commands = self._sub_commands
        if (sub_commands is not None):
            for sub_command in sub_commands.values():
                 resolved += sub_command._try_resolve_auto_completer(auto_completer)
        
        return resolved    
    
    
    def as_option(self):
        """
        Returns the slash command category as an application command option.
        
        Returns
        -------
        option : ``ApplicationCommandOption``
        """
        sub_commands = self._sub_commands
        if sub_commands is None:
            options = None
        else:
            options = [sub_command.as_option() for name, sub_command in sorted(sub_commands.items())]
        
        return ApplicationCommandOption(
            self.name,
            self.description,
            ApplicationCommandOptionType.sub_command_group,
            options = options,
            default = self.default,
        )
    
    
    # ---- Mention ----
    
    @property
    @copy_docs(CommandBase.mention)
    def mention(self):
        return self._mention_recursive()
    
    
    def _mention_recursive(self, *sub_command_names):
        """
        Returns the application command category's mention.
        
        Called by ``.mention`` to include the sub-commands' names.
        
        Parameters
        ----------
        *sub_command_names : `str`
            Already included sub-command name stack to mention.
        
        Returns
        -------
        mention : `str`
        """
        parent_reference = self._parent_reference
        if parent_reference is None:
            parent = None
        else:
            parent = parent_reference()
        
        if parent is None:
            return ''
        
        return parent._mention_recursive(self.name, *sub_command_names)
    
    
    @copy_docs(CommandBase.mention_at)
    def mention_at(self, guild):
        return self._mention_at_recursive(guild)
    
    
    def _mention_at_recursive(self, guild, *sub_command_names):
        """
        Returns the application command category's mention.
        
        Called by ``.mention`` to include the sub-commands' names.
        
        Parameters
        ----------
        guild : `Guild | int`
            The guild to mention the command at.
        
        *sub_command_names : `str`
            Already included sub-command name stack to mention.
        
        Returns
        -------
        mention : `str`
        """
        parent_reference = self._parent_reference
        if parent_reference is None:
            parent = None
        else:
            parent = parent_reference()
        
        if parent is None:
            return ''
        
        return parent._mention_at_recursive(guild, self.name, *sub_command_names)
