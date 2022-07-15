__all__ = ()

from scarletio import RichAttributeErrorBaseType

from .render_constants import (
    BOX_BOTTOM, BOX_LEFT_BOT, BOX_LEFT_TOP, BOX_RIGHT_BOT, BOX_RIGHT_TOP, BOX_TOP, PARAMETER_COLUMN_SEPARATOR,
    PARAMETER_DEFAULT_PREFIX, PARAMETER_MODIFIER_SEPARATOR, PARAMETER_NOTE_SIGN_OPTIONAL,
    PARAMETER_TYPE_IDENTIFIER_TO_REPRESENTATION
)


class ParameterRenderer(RichAttributeErrorBaseType):
    """
    Helper class for rendering parameter representation.
    
    Attributes
    ----------
    _default_representation : `None`, `str`
        The parameter's default value's representation.
    _default_representation_set : `bool`
        Whether ``._default_representation`` was already set.
    command_parameter : ``CommandParameter``
        The represented parameter.
    """
    __slots__ = ('_default_representation', '_default_representation_set', 'command_parameter',)
    
    def __new__(cls, command_parameter):
        """
        Creates a new parameter renderer instance.
        
        Parameters
        ----------
        command_parameter : ``CommandParameter``
            The represented parameter.
        """
        self = object.__new__(cls)
        self._default_representation = None
        self._default_representation_set = False
        self.command_parameter = command_parameter
        return self
    
    
    def get_name_length(self):
        """
        Gets the parameter's name's length.
        
        Returns
        -------
        name_length : `int`
        """
        command_parameter = self.command_parameter
        
        name_length = len(command_parameter.display_name)
        
        if command_parameter.is_modifier():
            name_length += 2
        
        elif not command_parameter.parameter.is_positional():
            name_length += 1
        
        return name_length
    
    
    def get_reverted_name_length(self):
        """
        Gets the reverted name of the option.
        
        Returns
        -------
        reverted_name_length : `int`
        """
        return self.get_name_length() + 3
    
    
    
    def get_name(self):
        """
        Returns the parameter's name.
        
        Returns
        -------
        name : `str`
        """
        command_parameter = self.command_parameter
        
        name = command_parameter.display_name
        
        if command_parameter.is_modifier():
            name = f'--{name}'
        elif not command_parameter.parameter.is_positional():
            name = f'-{name}'
        
        return name
    
    
    def get_reverted_name(self):
        """
        gets the reverted name of the parameter.
        
        Returns
        -------
        reverted_name : `str`
        """
        return f'--no-{self.command_parameter.display_name}'
    
    
    def get_type_name_length(self):
        """
        Returns the length of the parameter's type.
        
        Returns
        -------
        type_name_length : `int`
        """
        return len(self.get_type_name())
    
    
    def get_type_name(self):
        """
        Returns the type name of the parameter.
        
        Returns
        -------
        type_name : `str`
        """
        return PARAMETER_TYPE_IDENTIFIER_TO_REPRESENTATION[self.command_parameter.expected_type_identifier]
    
    
    def get_default_length(self):
        """
        Gets the parameter's default value's length.
        
        Returns
        -------
        default_length : `int`
        """
        default = self.get_default()
        if default is None:
            default_length = 0
        else:
            default_length = len(default)
        
        return default_length
    
    
    def get_default(self):
        """
        Gets the parameter's default value's representation.
        
        Returns
        -------
        default : `None`, `str`
        """
        if self._default_representation_set:
            return self._default_representation
        
        command_parameter = self.command_parameter
        parameter = command_parameter.parameter
        
        if parameter.has_default:
            if command_parameter.is_modifier():
                default_representation = command_parameter.display_name
                if not parameter.default:
                    default_representation = f'no-{default_representation}'
            else:
                default_representation = repr(parameter.default)
        else:
            default_representation = None
        
        self._default_representation_set = True
        self._default_representation = default_representation
        return default_representation
    
    
    def is_required(self):
        """
        Returns whether the parameter is required.
        
        Returns
        -------
        is_required : `bool`
        """
        return self.command_parameter.is_required()
    
    
    def get_note_sign(self):
        """
        Returns the note sign's length.
        
        Returns
        -------
        note_sign : `None`, `str`
        """
        if self.is_required():
            return PARAMETER_NOTE_SIGN_OPTIONAL
        
        return None
        
    
    def get_note_sign_length(self):
        """
        Returns the note sign's length.
        
        Returns
        -------
        note_sign_length : `int`
        """
        note_sign = self.get_note_sign()
        if note_sign is None:
            note_sign_length = 0
        else:
            note_sign_length = len(note_sign)
        
        return note_sign_length
    
    
    def get_generic_lengths(self):
        """
        Returns the parameter's lengths.
        
        Returns
        -------
        lengths : `tuple` of `int`
        """
        return (
            self.get_note_sign_length(),
            self.get_name_length(),
            self.get_type_name_length(),
            self.get_default_length(),
        )
    
    
    def get_modifier_lengths(self):
        """
        Gets the parameter's modifier form lengths.
        
        Returns
        -------
        lengths : `tuple` of `int`
        """
        return (
            self.get_name_length(),
            self.get_name_reverted_length(),
            self.get_default_length(),
        )
    
    
    def render_generic_into_with_lengths(self, into, lengths):
        """
        Renders the parameter into the given lost with the given lengths.
        
        > This rendering method is for generic parameters.
        
        Parameters
        ----------
        into : `list` of `str`
            The list to render the string parts into.
        lengths : `tuple` of `int`
            Lengths representing each column's width.
        
        Returns
        -------
        into : `list` of `str`
        """
        note_length, name_length, type_name_length, default_length = lengths
        
        if note_length:
            into = _render_part_into(into, self.get_note_sign(), note_length)
            into.append(PARAMETER_COLUMN_SEPARATOR)
        
        into = _render_part_into(into, self.get_name(), name_length)
        into.append(PARAMETER_COLUMN_SEPARATOR)
        into = _render_part_into(into, self.get_type_name(), type_name_length)
        
        if default_length:
            into.append(PARAMETER_COLUMN_SEPARATOR)
            default = self.get_default()
            into = _render_part_into(
                into, None if (default is None) else PARAMETER_DEFAULT_PREFIX, len(PARAMETER_DEFAULT_PREFIX)
            )
            into = _render_part_into(into, default, default_length)
        
        return into
    
    
    def render_modifier_into_with_lengths(self, into, lengths):
        """
        Renders the parameter into the given lost with the given lengths.
        
        > This rendering method is for modifier parameters.
        
        Parameters
        ----------
        into : `list` of `str`
            The list to render the string parts into.
        lengths : `tuple` of `int`
            Lengths representing each column's width.
        
        Returns
        -------
        into : `list` of `str`
        """
        name_length, reverted_name_length, default_length = lengths
        
        into = _render_part_into(into, self.get_name(), name_length)
        into.append(PARAMETER_MODIFIER_SEPARATOR)
        into = _render_part_into(into, self.reverted_name_length(), reverted_name_length)
        
        if default_length:
            into.append(PARAMETER_COLUMN_SEPARATOR)
            default = self.get_default()
            into = _render_part_into(
                into, None if (default is None) else PARAMETER_DEFAULT_PREFIX, len(PARAMETER_DEFAULT_PREFIX)
            )
            into = _render_part_into(into, default, default_length)
        
        return into


def get_render_generic_line_length(lengths):
    """
    Gets the output line length for the given `lengths` variable.
    
    > This utility function is for generic parameters.
    
    Parameters
    ----------
    lengths : `tuple` of `int`
        Lengths representing each column's width.
    
    Returns
    -------
    length : `int`
        The cumulate of the line.
    """
    length = 0
    
    note_length, name_length, type_name_length, default_length = lengths
    
    if note_length:
        length += note_length
        length += len(PARAMETER_COLUMN_SEPARATOR)
    
    length += name_length
    length += len(PARAMETER_COLUMN_SEPARATOR)
    length += type_name_length
    
    if default_length:
        length += len(PARAMETER_COLUMN_SEPARATOR)
        length += len(PARAMETER_DEFAULT_PREFIX)
        length += default_length
    
    return length


def get_render_modifier_line_length(lengths):
    """
    Gets the output line length for the given `lengths` variable.
    
    > This utility function is for modifier parameters.
        
    Parameters
    ----------
    lengths : `tuple` of `int`
        Lengths representing each column's width.
    
    Returns
    -------
    length : `int`
        The cumulate of the line.
    """
    length = 0
    
    name_length, reverted_name_length, default_length = lengths
    
    length += name_length
    length += len(PARAMETER_MODIFIER_SEPARATOR)
    length += reverted_name_length
    
    if default_length:
        length += len(PARAMETER_COLUMN_SEPARATOR)
        length += len(PARAMETER_DEFAULT_PREFIX)
        length += default_length
    
    return length


def merge_lengths(lengths_1, lengths_2):
    """
    Merges the given length tuples.
    
    
    Parameters
    ----------
    lengths_1 : `tuple` of `int`
        Length tuple 1.
    lengths_2 : `tuple` of `int`
        Length tuple 2.
    
    Returns
    -------
    length_tuple : `tuple` of `int`
    """
    return tuple(max(value_1, value_2) for value_1, value_2 in zip(lengths_1, lengths_2))


def _render_part_into(into, part, length):
    """
    Renders he given part into the given container on the specified length.
    
    Parameters
    ----------
    into : `list` of `str`
        The list of strings to render to.
    part : `None`, `str`
        The part to render.
    length : `int`
        The length to fill up.
    
    Returns
    -------
    into : `list` of `str`
    """
    adjust_length = length
    
    if (part is not None):
        into.append(part)
        adjust_length -= len(part)
    
    if adjust_length:
        into.append(' ' * adjust_length)
    
    return into


def render_box_start_into(into, line_length, title):
    """
    Renders box start into the given list.
    
    Parameters
    ----------
    into : `list` of `str`
        The list of strings to render to.
    line_length : `int`
        The expected length of the line.
    title : `str`
        Title of the box.
    
    Returns
    -------
    into : `list` of `str`
    """
    into.append(BOX_LEFT_TOP)
    into.append(title)
    
    line_adjust = line_length - len(title)
    if line_adjust > 0:
        into.append(BOX_TOP * line_adjust)
    
    into.append(BOX_RIGHT_TOP)
    into.append('\n')
    
    return into

def render_box_line_adjustment_into(into, line_length, title):
    """
    Renders box line adjustment into the given list.
    
    Parameters
    ----------
    into : `list` of `str`
        The list of strings to render to.
    line_length : `int`
        The expected length of the line.
    title : `str`
        Title of the box used for additional adjustments.
    
    Returns
    -------
    into : `list` of `str`
    """
    line_adjust = len(title) - line_length
    if line_adjust > 0:
        into.append(' ' * line_adjust)
    
    return into


def render_box_end_into(into, line_length, title):
    """
    Renders box end into the given list.
    
    Parameters
    ----------
    into : `list` of `str`
        The list of strings to render to.
    line_length : `int`
        The expected length of the line.
    title : `str`
        Title of the box used for additional adjustments.
    
    Returns
    -------
    into : `list` of `str`
    """
    into.append(BOX_LEFT_BOT)
    into.append(BOX_BOTTOM * max(line_length, len(title)))
    into.append(BOX_RIGHT_BOT)
    into.append('\n')
    
    return into
