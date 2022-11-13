__all__ = ('CommandCategory',)

from scarletio import RichAttributeErrorBaseType, WeakReferer

from .function import CommandFunction
from .helpers import command_sort_key, normalize_command_name
from .render_constants import BOX_TITLE_SUB_COMMANDS
from .rendering_helpers import render_sub_command_box_into, render_usage_line_into
from .result import (
    COMMAND_RESULT_CODE_CATEGORY_EMPTY, COMMAND_RESULT_CODE_CATEGORY_REQUIRES_PARAMETER,
    COMMAND_RESULT_CODE_CATEGORY_UNKNOWN_SUB_COMMAND, CommandResult
)


class CommandCategory(RichAttributeErrorBaseType):
    """
    Command line command category.
    
    Attributes
    ----------
    _command_categories : `None`, `dict` of (`str`, ``CommandCategory``) items
        Sub commands of the command.
    _command_function : `None`, ``CommandFunction``
        Command to call, if sub command could not be detected.
    _parent_reference : `None`, ``WeakReferer``
        Weakreference to the command category's parent.
    _self_reference : `None`, ``WeakReferer``
        Weakreference to the category itself.
    name : `None`, `str`
        The sub command category's name.
    """
    __slots__ = (
        '__weakref__', '_command_categories', '_command_function', '_parent_reference', '_self_reference', 'name'
    )
    
    def __new__(cls, parent, name):
        """
        Creates a new command line command category.
        
        Parameters
        ----------
        parent : ``Command``, ``CommandCategory``
            The parent command or command category.
        name : `None`, `str`
            The command category's name.
        """
        if (name is not None):
            name = normalize_command_name(name)
        
        self = object.__new__(cls)
        self.name = name
        self._command_function = None
        self._command_categories = None
        self._self_reference = None
        self._parent_reference = parent._self_reference
        
        self._self_reference = WeakReferer(self)
        
        return self
    
    
    def __repr__(self):
        """Returns the command category's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        name = self.name
        if (name is not None):
            repr_parts.append(' name=')
            repr_parts.append(repr(name))
            
            field_added = True
        else:
            field_added = False
        
        command_function = self._command_function
        if (command_function is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' command_function=')
            repr_parts.append(repr(command_function))
        
        sub_categories = [*self.iter_sub_categories()]
        if sub_categories:
            if not field_added:
                repr_parts.append(',')
            
            repr_parts.append(', sub_categories={')
            
            index = 0
            limit = len(sub_categories)
            
            while True:
                sub_category = sub_categories[index]
                
                index += 1
                repr_parts.append(repr(sub_category))
                
                if index == limit:
                    break
                
                repr_parts.append(', ')
            
            repr_parts.append('}')
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def register_command_category(self, name):
        """
        Registers a sub command to the command.
        
        Parameters
        ----------
        name : `str`
            The name of the sub-command.
        
        Returns
        -------
        sub_command : ``CommandCategory``
        """
        sub_command = CommandCategory(self, name)
        sub_commands = self._command_categories
        if (sub_commands is None):
            sub_commands = {}
            self._command_categories = sub_commands
        
        sub_commands[sub_command.name] = sub_command
        return sub_command
    
    
    def register_command_function(self, function, name, description):
        """
        Parameters
        ----------
        function : `callable`
            The function to call when the command is used.
        name : `str`
            The command's name.
        description : `None`, `str`
            The command's description.
        
        Returns
        -------
        command_function : CommandFunction
        """
        self_name = self.name
        if self_name is None:
            parent_name = self.get_parent_name()
            if parent_name is None:
                direct_register = False
            elif name == parent_name:
                direct_register = True
            else:
                direct_register = False
        
        else:
            if self_name == name:
                direct_register = True
            else:
                direct_register = False
        
        if direct_register:
            command_function = CommandFunction(self, function, name, description)
            self._command_function = command_function
            return command_function
        
        
        category = self.register_command_category(name)
        return category.register_command_function(function, name, description)
    
    
    def get_parent(self):
        """
        Returns the parent category of the command.
        
        Returns
        -------
        parent : `None`, ``Command``, ``CommandCategory``
        """
        parent_reference = self._parent_reference
        if (parent_reference is not None):
            return parent_reference()
    
    
    def get_parent_name(self):
        """
        Returns the category's parent's name.
        
        Returns
        -------
        name : `None`, `str`
        """
        parent = self.get_parent()
        if (parent is not None):
            return parent.name
    
    
    def _trace_back_name(self):
        """
        Traces back to the source name of the command.
        
        This method is an iterable generator.
        
        Yields
        ------
        name : `str`
        
        Returns
        -------
        parent_name : `str`, `None`
        """
        parent_name = None
        
        parent = self.get_parent()
        if (parent is not None):
            parent_name = yield from parent._trace_back_name()
                
        
        name = self.name
        if (name is not None):
            yield name
        
        if (name is None):
            return parent_name
        
        return name
    
    
    def invoke(self, parameters, index):
        """
        Calls the command line command category.
        
        Parameters
        ----------
        parameters : `list` of `str`
            Command line parameters.
        index : `int`
            The index of the first parameter trying to process.
        
        Returns
        -------
        command_result : ``CommandResult``
        """
        command_categories = self._command_categories
        if (command_categories is None):
            command_function = self._command_function
            if (command_function is not None):
                return command_function.invoke(parameters, index)
            
            return CommandResult(
                COMMAND_RESULT_CODE_CATEGORY_EMPTY,
                self,
            )
            
        
        if index >= len(parameters):
            command_function = self._command_function
            if (command_function is not None):
                return command_function.invoke(parameters, index)
            
            return CommandResult(
                COMMAND_RESULT_CODE_CATEGORY_REQUIRES_PARAMETER,
                self,
            )
        
        command_name = parameters[index]
        if command_name.startswith('-'):
            command_category = None
        else:
            command_category = command_categories.get(normalize_command_name(command_name), None)
        
        if (command_category is not None):
            return command_category.invoke(parameters, index + 1)
        
        command_function = self._command_function
        if (command_function is not None):
            return command_function.invoke(parameters, index)
        
        return CommandResult(
            COMMAND_RESULT_CODE_CATEGORY_UNKNOWN_SUB_COMMAND,
            self,
            command_name,
        )
    
    
    def iter_sub_categories(self):
        """
        Iterates over the sub categories of the category.
        
        This method is an iterable generator.
        
        Yields
        ------
        sub_category : ``CommandCategory``
        """
        command_categories = self._command_categories
        if (command_categories is not None):
            yield from command_categories.values()
    
    
    def iter_sub_category_names(self):
        """
        Iterates over the sub-category names of the category.
        
        This method is an iterable generator.
        
        Yields
        ------
        sub_category_name : `str`
        """
        for sub_category in self.iter_sub_categories():
            name = sub_category.name
            if (name is not None):
                yield name
    
    
    def has_sub_categories(self):
        """
        Returns whether the category has sub-categories.
        
        Yields
        ------
        has_sub_categories : `bool`
        """
        return (self._command_categories is not None)
    
    
    def walk_usage(self):
        """
        Walks over the usage of the command category.
        
        This method is an iterable generator.
        
        Yields
        -------
        usage : `str`
        """
        for into in self.walk_usage_into([]):
            yield ''.join(into)
            into.clear()
    
    
    def get_direct_usage(self, *sub_command_stack):
        """
        Returns the direct usage of the command category for the given sub-command stack.
        
        Parameters
        ----------
        *sub_command_stack : `str`
            Sub command stack to get the direct usage for.
        
        Returns
        -------
        usage : `str`
        """
        return ''.join(self.render_direct_usage_into([], *sub_command_stack))
    
    
    def render_direct_usage_into(self, into, *sub_command_stack):
        """
        Renders the direct usage of the command category for the given sub-command stack.
        
        Parameters
        ----------
        into : `list` of `str`
            The list to render the usage into.
        *sub_command_stack : `str`
            Sub command stack to get the direct usage for.
        
        Returns
        -------
        into : `list` of `str`
        """
        if sub_command_stack:
            command_categories = self._command_categories
            if (command_categories is None):
                category = None
            else:
                category = command_categories.get(normalize_command_name(sub_command_stack[0]), None)
        else:
            category = None
        
        if (category is None):
            command_function = self._command_function
            if (command_function is not None):
                return command_function.render_usage_into(into)
            
            return self.render_partial_usage_into(into)
        
        return category.render_direct_usage_into(into, *sub_command_stack[1:])
    
    
    def walk_usage_into(self, into):
        """
        Walks over the usage of the command category and renders it to the given list.
        
        This method is an iterable generator.
        
        Parameters
        ----------
        into : `list` of `str`
            The list to render the usage into.
        
        Yields
        ------
        into : `list` of `str`
        
        Returns
        -------
        into : `list` of `str`
        """
        command_function = self._command_function
        if (command_function is not None):
            into = command_function.render_usage_into(into)
            yield into
        
        for command_category in sorted(self.iter_sub_categories(), key = command_sort_key):
            into = yield from command_category.walk_usage_into(into)
        
        return into
    
    
    def render_partial_usage(self):
        """
        Renders the command category's partial usage.
        
        Returns
        -------
        usage : `str`
        """
        return ''.join(self.render_partial_usage_into([]))
    
    
    def render_partial_usage_into(self, into):
        """
        Renders the command category's partial usage into the given list.
        
        Parameters
        ----------
        into : `list` of `str`
            The list to render the usage into.
        
        Returns
        -------
        into : `list` of `str`
        """
        into = render_usage_line_into(into, self._trace_back_name())
        into.append(' ...')
        
        sub_command_names = [*self.iter_sub_category_names()]
        sub_command_line_length = max((len(sub_command_name) for sub_command_name in sub_command_names), default = 0)
        
        line_length = 0
        if sub_command_line_length:
            line_length = max(sub_command_line_length, len(BOX_TITLE_SUB_COMMANDS))
        
        if sub_command_line_length:
            into.append('\n\n')
            into = render_sub_command_box_into(into, sub_command_names, line_length)
        
        return into
    
    
    def iter_command_functions(self):
        """
        Iterates over the command functions of the command category.
        
        This method is an iterable generator.
        
        Yields
        ------
        command_function : ``CommandFunction``
        """
        command_function = self._command_function
        if (command_function is not None):
            yield command_function
        
        for sub_category in self.iter_sub_categories():
            yield from sub_category.iter_command_functions()
