__all__ = ('CommandFunction',)

from scarletio import RichAttributeErrorBaseType

from .parameter import get_command_parameters_for
from .parameter_renderer import (
    ParameterRenderer, get_lengths, get_render_generic_line_length, get_render_modifier_line_length
)
from .parameter_result import ParameterResult
from .render_constants import (
    BOX_LEFT, BOX_RIGHT, BOX_TITLE_MODIFIER, BOX_TITLE_PARAMETER, BOX_TITLE_SUB_COMMANDS, NOTE_SIGN_DESCRIPTION
)
from .rendering_helpers import (
    render_box_end_into, render_box_line_adjustment_into, render_box_start_into, render_sub_command_box_into,
    render_usage_line_into
)
from .result import (
    COMMAND_RESULT_CODE_CALL, COMMAND_RESULT_CODE_PARAMETER_REQUIRED, COMMAND_RESULT_CODE_PARAMETER_UNEXPECTED,
    COMMAND_RESULT_CODE_PARAMETER_UNSATISFIED, CommandResult
)


class CommandFunction(RichAttributeErrorBaseType):
    """
    Command line function to call.
    
    Attributes
    ----------
    _function : `callable`
        The function to call.
    _parent_reference : `None`, ``WeakReferer``
        Weakreference to the command function's parent.
    _parameters : `list` of ``CommandParameter``
        Parameter parsers to call the command with.
    description : `None`, `str`
        The command's description.
    name : `str`
        The command's name.
    """
    __slots__ = (
        '_function', '_parent_reference', '_parameters', 'description', 'name',
    )
    
    def __new__(cls, parent, function, name, description):
        """
        Creates a new ``CommandFunction``.
        
        Parameters
        ----------
        parent : ``CommandCategory``
            The command's parent.
        function : `callable`
            The function to call when the command is used.
        name : `str`
            The command's name.
        description : `None`, `str`
            The command's description.
        """
        parameters = get_command_parameters_for(function)
        
        self = object.__new__(cls)
        self._function = function
        self._parameters = parameters
        self._parent_reference = parent._self_reference
        self.description = description
        self.name = name
        return self
    
    
    def __repr__(self):
        """Returns the command function's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' name=')
        repr_parts.append(repr(self.name))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def get_parent(self):
        """
        Returns the parent category of the command.
        
        Returns
        -------
        parent : `None`, ``CommandCategory``
        """
        parent_reference = self._parent_reference
        if (parent_reference is not None):
            return parent_reference()
    
    
    def iter_direct_sub_command_names(self):
        """
        gets the direct sub-command names of the command function.
        
        This method is an iterable generator.
        
        Yields
        ------
        sub_command_name : `str`
        """
        parent = self.get_parent()
        if (parent is not None):
            yield from parent.iter_sub_category_names()
    
    
    def _trace_back_name(self):
        """
        Traces back to the source name of the command.
        
        This method is an iterable generator.
        
        Yields
        ------
        name : `str`
        
        Returns
        -------
        parent_name : `None`
        """
        parent_name = None
        
        parent = self.get_parent()
        if (parent is not None):
            parent_name = yield from parent._trace_back_name()
        
        name = self.name
        if (parent_name is None) or (parent_name != name):
            yield name
        
        return None
    
    
    def invoke(self, parameters, index):
        """
        Calls the command line command.
        
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
        positional_parameters = []
        keyword_parameters = {}
        
        command_result = parse_parameters_into(
            parameters, index, self._parameters, positional_parameters, keyword_parameters
        )
        if (command_result is not None):
            return command_result
        
        
        return CommandResult(
            COMMAND_RESULT_CODE_CALL,
            self,
            positional_parameters,
            keyword_parameters,
        )
    
    
    def get_usage(self):
        """
        Returns the usage of the command function.
        
        Returns
        -------
        usage : `str`
        """
        return ''.join(self.render_usage_into([]))
    
    
    def render_usage_into(self, into):
        """
        Renders the command function's usage into the given list.
        
        Parameters
        ----------
        into : `list` of `str`
            The list to render the usage into.
        
        Returns
        -------
        into : `list` of `str`
        """
        
        # Display description
        
        description = self.description
        if (description is not None):
            into.append(description)
            into.append('\n\n')
        
        into = render_usage_line_into(into, self._trace_back_name())
        
        parameter_renderers = [ParameterRenderer(command_parameter) for command_parameter in self._parameters]
        
        modifier_field_added = False
        should_add_rest_field = False
        
        for parameter_renderer in parameter_renderers:
            if parameter_renderer.is_positional():
                into.append(' ')
                into.append(parameter_renderer.get_name().upper())
                continue
            
            if parameter_renderer.is_args():
                into.append(' [')
                into.append(parameter_renderer.get_name().upper())
                into.append('...]')
                continue
            
            if parameter_renderer.is_modifier():
                if modifier_field_added:
                    continue
                
                into.append(' [OPTIONS]')
                modifier_field_added = True
                continue
            
            should_add_rest_field = True
        
        if should_add_rest_field:
            into.append(' ...')
        
        parameters_generic = []
        parameters_modifier = []
        
        for parameter_renderer in parameter_renderers:
            if parameter_renderer.is_modifier():
                parameters_modifier.append(parameter_renderer)
            else:
                parameters_generic.append(parameter_renderer)
        
        sub_command_names = [*self.iter_direct_sub_command_names()]
        
        generic_lengths = get_lengths(parameters_generic, ParameterRenderer.get_generic_lengths)
        generic_line_length = get_render_generic_line_length(generic_lengths)
        modifier_lengths = get_lengths(parameters_modifier, ParameterRenderer.get_modifier_lengths)
        modifier_line_length = get_render_modifier_line_length(modifier_lengths)
        sub_command_line_length = max((len(sub_command_name) for sub_command_name in sub_command_names), default = 0)
        
        
        line_length = 0
        if generic_line_length:
            line_length = max(line_length, generic_line_length, len(BOX_TITLE_PARAMETER))
        if modifier_line_length:
            line_length = max(line_length, modifier_line_length, len(BOX_TITLE_MODIFIER))
        if sub_command_line_length:
            line_length = max(line_length, sub_command_line_length, len(BOX_TITLE_SUB_COMMANDS))
        
        field_added = False
        
        if generic_line_length:
            if not field_added:
                into.append('\n\n')
                field_added = True
            
            # Render line 1
            
            into = render_box_start_into(into, line_length, BOX_TITLE_PARAMETER)
            
            # Render line n
            for parameter in parameters_generic:
                into.append(BOX_LEFT)
                into = parameter.render_generic_into_with_lengths(into, generic_lengths)
                into = render_box_line_adjustment_into(into, generic_line_length, line_length)
                into.append(BOX_RIGHT)
                into.append('\n')
            
            # Render line -1
            into = render_box_end_into(into, line_length)
        
        
        if modifier_line_length:
            if not field_added:
                into.append('\n\n')
                field_added = True
            
            # Render line 1
            into = render_box_start_into(into, line_length, BOX_TITLE_MODIFIER)
            
            # Render line n
            for parameter in parameters_modifier:
                into.append(BOX_LEFT)
                into = parameter.render_modifier_into_with_lengths(into, modifier_lengths)
                into = render_box_line_adjustment_into(into, modifier_line_length, line_length)
                into.append(BOX_RIGHT)
                into.append('\n')
            
            # Render line -1
            into = render_box_end_into(into, line_length)
        
        
        if sub_command_line_length:
            if not field_added:
                into.append('\n\n')
                field_added = True
            
            into = render_sub_command_box_into(into, sub_command_names, line_length)
        
        
        # Collect signs
        note_signs = None
        
        for parameter_renderer in parameter_renderers:
            note_sign = parameter_renderer.get_note_sign()
            if (note_sign is not None):
                if note_signs is None:
                    note_signs = set()
                
                note_signs.add(note_sign)
        
        # Display note signs
        if (note_signs is not None):
            if not field_added:
                into.append('\n')
                field_added = True
            
            note_sign_adjustment = max(len(note_sign) for note_sign in note_signs) + 1
            for note_sign in sorted(note_signs):
                into.append('\n')
                into.append(note_sign)
                into.append(' ' * (note_sign_adjustment - len(note_sign)))
                into.append(NOTE_SIGN_DESCRIPTION[note_sign])
        
        return into
    
    
    def get_full_name(self):
        """
        Returns the command function's full name.
        
        Returns
        -------
        full_name : `str`
        """
        return ' '.join(self._trace_back_name())


def parse_parameters_into(parameter_values, start_index, command_parameters, positional_parameters, keyword_parameters):
    """
    Parameters
    ----------
    parameter_values : `list` of `str`
        Command line parameters.
    start_index : `int`
        The index of the first parameter trying to process.
    command_parameters : `list` of ``CommandParameter``
        Parameters of the respective command.
    positional_parameters : `list` of `Any`
        Positional parameters to call the respective function with.
    keyword_parameters : `dict` of (`str`, `Any`) items
        Keyword parameters to call the respective function with.
    
    Returns
    -------
    command_result : `None`, ``CommandResult``
        Returns a command result if failed.
    """
    parameter_values = parameter_values[start_index:]
    
    for parameter_value in parameter_values:
        if parameter_value.startswith('---'):
            return CommandResult(
                COMMAND_RESULT_CODE_PARAMETER_UNEXPECTED,
                parameter_value,
            )
    
    parameter_values.reverse()
    
    
    parameter_results = [ParameterResult(command_parameter) for command_parameter in command_parameters]
    
    while parameter_values:
        parameter_value = parameter_values.pop()
        
        if parameter_value.startswith('--'):
            parameter_name, parsed_value = parse_modifier_parameter_name(parameter_value)
            parameter_result = find_satisfiable_modifier_parameter_result_for(parameter_results, parameter_name)
            if (parameter_result is None):
                return CommandResult(
                    COMMAND_RESULT_CODE_PARAMETER_UNEXPECTED,
                    parameter_value,
                )
            
            command_result = parameter_result.feed(parsed_value)
            if (command_result is not None):
                return command_result
            
            continue
        
        
        if parameter_value.startswith('-'):
            parameter_name = re_normalise_parameter_name(parameter_value)
            parameter_result = find_satisfiable_keyword_parameter_result_for(
                parameter_results,
                parameter_name,
            )
            
            if (parameter_result is None):
                return CommandResult(
                    COMMAND_RESULT_CODE_PARAMETER_UNEXPECTED,
                    parameter_value,
                )
            
            if len(parameter_values) == 0:
                return CommandResult(
                    COMMAND_RESULT_CODE_PARAMETER_UNSATISFIED,
                    parameter_result.command_parameter,
                )
        
            command_result = parameter_result.feed_as(parameter_values.pop(), parameter_name)
            if (command_result is not None):
                return command_result
            
            continue
        
        
        parameter_result = find_next_satisfiable_positional_parameter_result(parameter_results)
        if (parameter_result is None):
            return CommandResult(
                COMMAND_RESULT_CODE_PARAMETER_UNEXPECTED,
                parameter_value,
            )
        
        command_result = parameter_result.feed(parameter_value)
        if (command_result is not None):
            return command_result
        
        continue
    
    
    for parameter_result in parameter_results:
        if not parameter_result.put_into(positional_parameters, keyword_parameters):
            return CommandResult(
                COMMAND_RESULT_CODE_PARAMETER_REQUIRED,
                parameter_result.command_parameter,
            )
    
    return None


def re_normalise_parameter_name(parameter_name):
    """
    Re-normalises parameter name.
    
    Parameters
    ----------
    parameter_name : `str`
        The parameter name to normalise.
    
    Returns
    -------
    parameter_name : `str`
    """
    return '-'.join(parameter_name.replace('_', ' ').replace('-', ' ').split())


def parse_modifier_parameter_name(parameter_name):
    """
    Parses modifier type parameter.
    
    Parameters
    ----------
    parameter_name : `str`
        The parameter name to parse.
    
    Returns
    -------
    output_name : `str`
        The parameter's normalises and stripped name.
    output_value : `bool`
        The set value to the parameter.
    """
    parameter_name = re_normalise_parameter_name(parameter_name)
    if parameter_name.startswith('no-'):
        output_value = False
        output_name = parameter_name[len('no-'):]
    else:
        output_value = True
        output_name = parameter_name
    
    return output_name, output_value


def find_satisfiable_modifier_parameter_result_for(parameter_results, parameter_name):
    """
    Finds a satisfiable modifier parameter for the given nane.
    
    Parameters
    ----------
    parameter_results : `list` of ``ParameterResult``
        Parameter results to select from.
    parameter_name : `str`
        Parameter name to match.
    
    Returns
    -------
    parameter_result : ``ParameterResult``
        The matched parameter parse result.
    """
    for parameter_result in parameter_results:
        if (
            parameter_result.is_satisfiable() and
            parameter_result.matches_name(parameter_name) and
            parameter_result.is_modifier()
        ):
            return parameter_result


def find_satisfiable_keyword_parameter_result_for(parameter_results, parameter_name):
    """
    Finds a satisfiable keyword parameter for the given nane.
    
    Parameters
    ----------
    parameter_results : `list` of ``ParameterResult``
        Parameter results to select from.
    parameter_name : `str`
        Parameter name to match.
    
    Returns
    -------
    parameter_result : ``ParameterResult``
        The matched parameter parse result.
    """
    for parameter_result in parameter_results:
        if (
            parameter_result.is_satisfiable() and
            parameter_result.matches_name(parameter_name)
        ):
            return parameter_result


def find_next_satisfiable_positional_parameter_result(parameter_results):
    """
    Finds a satisfiable positional parameter for the given nane.
    
    Parameters
    ----------
    parameter_results : `list` of ``ParameterResult``
        Parameter results to select from.
    
    Returns
    -------
    parameter_result : ``ParameterResult``
        The matched parameter parse result.
    """
    for parameter_result in parameter_results:
        if (
            parameter_result.is_satisfiable() and
            parameter_result.is_positional()
        ):
            return parameter_result
