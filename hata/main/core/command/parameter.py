__all__ = ('CommandParameter', 'get_command_parameters_for',)

from scarletio import CallableAnalyzer, RichAttributeErrorBaseType


TYPE_IDENTIFIER_STR = 1
TYPE_IDENTIFIER_INT = 2
TYPE_IDENTIFIER_FLOAT = 3
TYPE_IDENTIFIER_BOOL = 4

TYPE_TYPE_STR = str
TYPE_TYPE_INT = int
TYPE_TYPE_FLOAT = float
TYPE_TYPE_BOOL = bool

TYPE_NAME_STR = 'str'
TYPE_NAME_INT = 'int'
TYPE_NAME_FLOAT = 'float'
TYPE_NAME_BOOL = 'bool'

TYPE_TYPE_TO_IDENTIFIER = {
    TYPE_TYPE_STR: TYPE_IDENTIFIER_STR,
    TYPE_TYPE_INT: TYPE_IDENTIFIER_INT,
    TYPE_TYPE_FLOAT: TYPE_IDENTIFIER_FLOAT,
    TYPE_TYPE_BOOL: TYPE_IDENTIFIER_BOOL
}

TYPE_NAME_TO_IDENTIFIER = {
    TYPE_NAME_STR: TYPE_IDENTIFIER_STR,
    TYPE_NAME_INT: TYPE_IDENTIFIER_INT,
    TYPE_NAME_FLOAT: TYPE_IDENTIFIER_FLOAT,
    TYPE_NAME_BOOL: TYPE_IDENTIFIER_BOOL,
}


# revert the relation
TYPE_IDENTIFIER_TO_NAME = {identifier: name for name, identifier in TYPE_NAME_TO_IDENTIFIER.items()}


def parameter_value_converter_str(value):
    """
    Converts the given value to string.
    
    Parameters
    ----------
    value : `str`
        The value to convert to string.
    
    Returns
    -------
    value : `None`, `str`
        Returns `None` if conversion failed.
    """
    return value


def parameter_value_converter_int(value):
    """
    Converts the given value to int.
    
    Parameters
    ----------
    value : `str`
        The value to convert to string.
    
    Returns
    -------
    value : `None`, `int`
        Returns `None` if conversion failed.
    """
    try:
        value = int(value)
    except ValueError:
        value = None
    
    return value


def parameter_value_converter_float(value):
    """
    Converts the given value to float.
    
    Parameters
    ----------
    value : `str`
        The value to convert to string.
    
    Returns
    -------
    value : `None`, `float`
        Returns `None` if conversion failed.
    """
    try:
        value = float(value)
    except ValueError:
        value = None
    
    return value


def parameter_value_converter_bool(value):
    """
    Converts the given value to bool.
    
    Parameters
    ----------
    value : `bool`, `str`
        The value to convert to string.
    
    Returns
    -------
    value : `None`, `bool`
        Returns `None` if conversion failed.
    """
    if isinstance(value, bool):
        return value
    
    if isinstance(value, str):
        value = value.lower()
        if value == 'true':
            return True
        
        if value == 'false':
            return False
        
        return None
    
    return None


TYPE_IDENTIFIER_TO_CONVERTER = {
    TYPE_IDENTIFIER_STR: parameter_value_converter_str,
    TYPE_IDENTIFIER_INT: parameter_value_converter_int,
    TYPE_IDENTIFIER_FLOAT: parameter_value_converter_float,
    TYPE_IDENTIFIER_BOOL: parameter_value_converter_bool,
}


class CommandParameter(RichAttributeErrorBaseType):
    """
    Represents a command line command's parameter.
    
    Attributes
    ----------
    display_name : `str`
        The display name of the parameter.
    expected_type_identifier : `int`
        Internal identifier for the expected type accepted by the command.
    parameter : ``Parameter``
        The command function's parameter.
    """
    __slots__ = ('display_name', 'expected_type_identifier', 'parameter',)
    
    def __new__(cls, parameter):
        """
        Creates a new command line parameter.
        
        Parameters
        ----------
        parameter : ``Parameter``
            The respective function's parameter.
        
        Raises
        ------
        LookupError
            Could not match the parameter's annotation.
        TypeError
            Unhandled annotation type.
        ValueError
            Not allowed parameter specification.
        """
        if parameter.has_annotation:
            annotation = parameter.annotation
            
            if isinstance(annotation, str):
                try:
                    expected_type_identifier = TYPE_NAME_TO_IDENTIFIER[annotation]
                except KeyError:
                    raise LookupError(
                        f'Annotation has no converter. Got: {annotation!r}.'
                    ) from None
                    
            elif isinstance(annotation, type):
                try:
                    expected_type_identifier = TYPE_TYPE_TO_IDENTIFIER[annotation]
                except KeyError:
                    raise LookupError(
                        f'Annotation has no converter. Got: {annotation!r}.'
                    ) from None
            
            else:
                raise TypeError(
                    f'Annotation of unexpected type Got {annotation!r}.'
                )
        
        else:
            expected_type_identifier = TYPE_IDENTIFIER_STR
        
        if parameter.is_positional() and expected_type_identifier == TYPE_IDENTIFIER_BOOL:
            raise ValueError(
                f'Not allowed parameter specification. Positional parameters cannot be annotated as bool.'
                f'Got: parameter={parameter!r}'
            )
        
        display_name = '-'.join(parameter.name.replace('_', ' ').split())
        
        self = object.__new__(cls)
        self.display_name = display_name
        self.expected_type_identifier = expected_type_identifier
        self.parameter = parameter
        return self
    
    
    def __repr__(self):
        """Returns the command line parameter's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' ')
        repr_parts.append(self.display_name)
        
        repr_parts.append(', parameter=')
        repr_parts.append(repr(self.parameter))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def get_converter(self):
        """
        Gets converter of the specified parameter type.
        
        Returns
        -------
        converter : `FunctionType`
        """
        return TYPE_IDENTIFIER_TO_CONVERTER[self.expected_type_identifier]
    
    
    def is_modifier(self):
        """
        Returns whether the parameter is a modifier parameter.
        
        Returns
        -------
        is_modifier : `bool`
        """
        return self.expected_type_identifier == TYPE_IDENTIFIER_BOOL
    
    
    def is_required(self):
        """
        Returns whether the parameter is required.
        """
        parameter = self.parameter
        if parameter.has_default:
            return False
        
        if parameter.is_args() or parameter.is_kwargs():
            return False
        
        return True


def get_command_parameters_for(function):
    """
    Gets the command parameter
    """
    analyzer = CallableAnalyzer(function)
    
    command_line_parameters = []
    
    for parameter in analyzer.iter_non_reserved_parameters():
        command_line_parameter = CommandParameter(parameter)
        command_line_parameters.append(command_line_parameter)
    
    return command_line_parameters
