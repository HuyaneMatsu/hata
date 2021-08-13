__all__ = ()

TYPE_IDENTIFIER_STR = 1
TYPE_IDENTIFIER_INT = 2
TYPE_IDENTIFIER_FLOAT = 3

TYPE_TYPE_STR = str
TYPE_TYPE_INT = int
TYPE_TYPE_FLOAT = float

TYPE_NAME_STR = 'str'
TYPE_NAME_INT = 'int'
TYPE_NAME_FLOAT = 'float'

TYPE_TYPE_TO_IDENTIFIER = {
    TYPE_TYPE_STR: TYPE_IDENTIFIER_STR,
    TYPE_TYPE_INT: TYPE_IDENTIFIER_INT,
    TYPE_TYPE_FLOAT: TYPE_IDENTIFIER_FLOAT,
}

TYPE_NAME_TO_IDENTIFIER = {
    TYPE_NAME_STR: TYPE_IDENTIFIER_STR,
    TYPE_NAME_INT: TYPE_IDENTIFIER_INT,
    TYPE_NAME_FLOAT: TYPE_IDENTIFIER_FLOAT,
}

# revert the relation
TYPE_IDENTIFIER_TO_NAME = {identifier: name for identifier, name in TYPE_NAME_TO_IDENTIFIER.items()}


def converter_parameter_to_str(value):
    """
    Converts the given value to string.
    
    Parameters
    ----------
    value : `str`
        The value to convert to string.
    
    Returns
    -------
    value : `None` or `str`
        Returns `None` if conversion failed.
    """
    return value


def converter_parameter_to_int(value):
    """
    Converts the given value to string.
    
    Parameters
    ----------
    value : `str`
        The value to convert to string.
    
    Returns
    -------
    value : `None` or `int`
        Returns `None` if conversion failed.
    """
    try:
        value = int(value)
    except ValueError:
        value = None
    
    return value


def converter_parameter_to_float(value):
    """
    Converts the given value to string.
    
    Parameters
    ----------
    value : `str`
        The value to convert to string.
    
    Returns
    -------
    value : `None` or `float`
        Returns `None` if conversion failed.
    """
    try:
        value = float(value)
    except ValueError:
        value = None
    
    return value

TYPE_IDENTIFIER_TO_CONVERTER = {
    TYPE_IDENTIFIER_STR: converter_parameter_to_str,
    TYPE_IDENTIFIER_INT: converter_parameter_to_int,
    TYPE_IDENTIFIER_FLOAT: converter_parameter_to_float,
}


def validate_command_line_parameter_expected_type_identifier(expected_type):
    """
    Validates ``CommandLineParameter``'s `expected_type` parameter.
    
    Parameters
    ----------
    expected_type : `None`, `str`, `type`
        Expected type by a command line parameter.
    
    Returns
    -------
    expected_type_identifier : `int`
        The type's identifier.
    
    Raises
    ------
    TypeError
        If `expected_type` is neither `None`, `str`, neither `type` instance.
    ValueError
        If `expected_type` is correct type, but it's value is incorrect and cannot identifier converter for it.
    """
    if expected_type is None:
        expected_type_identifier = TYPE_IDENTIFIER_STR
    
    elif isinstance(expected_type, str):
        try:
            expected_type_identifier = TYPE_NAME_TO_IDENTIFIER[expected_type]
        except KeyError:
            raise ValueError(f'`expected_type` value has no converter, got: {expected_type!r}.') from None
    
    elif isinstance(expected_type, type):
        try:
            expected_type_identifier = TYPE_TYPE_TO_IDENTIFIER[expected_type]
        except KeyError:
            raise ValueError(f'`expected_type` value has no converter, got: {expected_type!r}.') from None
    
    else:
        raise TypeError(f'`expected_type` can be either `None`, `str` or `type` instance, got '
            f'{expected_type.__class__.__name__}.')
    
    return expected_type_identifier


def validate_command_line_parameter_name(name):
    """
    Validates ``CommandLineParameter``'s `name` parameter.
    
    Parameters
    ----------
    name : `str`
        Name parameter to validate.
    
    Returns
    -------
    name : `str`
        The validated name parameter.
    
    Raises
    ------
    TypeError
        If `name` is not `str` instance.
    """
    if type(name) is str:
        pass
    elif isinstance(name, str):
        name = str(name)
    else:
        raise TypeError(f'`name` can be `str` instance, got {name.__class__.__name__}.')
    
    return name


def validate_command_line_parameter_keyword(keyword):
    """
    Validates ``CommandLineParameter``'s `keyword` parameter.
    
    Parameters
    ----------
    keyword : `None` or `str`
        Keyword parameter to validate.
    
    Returns
    -------
    keyword : `None` or `str`
        The validated keyword parameter.
    
    Raises
    ------
    TypeError
        If `keyword` is neither `None` nor `str` instance.
    """
    if keyword is None:
        pass
    elif type(keyword) is str:
        pass
    elif isinstance(keyword, str):
        keyword = str(keyword)
    else:
        raise TypeError(f'`keyword` can be given as `None` or `str` instance, got {keyword.__class__.__name__}.')
    
    return keyword


def validate_command_line_parameter_multi(multi):
    """
    Validates ``CommandLineParameter``'s `multi` parameter.
    
    Parameters
    ----------
    multi : `bool`
        Multi parameters to validate.
    
    Returns
    -------
    multi : `bool`
        Validated multi parameter.
    
    Raises
    ------
    TypeError
        If `multi` is not `bool` instance.
    """
    if type(multi) is bool:
        pass
    elif isinstance(multi, bool):
        multi = bool(multi)
    else:
        raise TypeError(f'`multi` can be `bool` instance, got {multi.__class__.__name__}.')
    
    return multi


DEFAULT_DEFAULT_VALUE = ...

def validate_command_line_parameter_default_value(default):
    """
    Validates ``CommandLineParameter``'s `default` parameter.
    
    Parameters
    ----------
    default : `Any`
        Default value.
    
    Returns
    -------
    has_default : `bool`
        Whether default value is given.
    default_value : `None` or `Any`
        Default value.
    """
    if default is DEFAULT_DEFAULT_VALUE:
        has_default = False
        default_value = None
    else:
        has_default = True
        default_value = default
    
    return has_default, default_value
    

def validate_command_line_parameter_modifier(modifier):
    """
    Validates ``CommandLineParameter``'s `modifier` parameter.
    
    Parameters
    ----------
    modifier : `bool`
        Multi parameters to validate.
    
    Returns
    -------
    modifier : `bool`
        Validated multi parameter.
    
    Raises
    ------
    TypeError
        If `modifier` is not `bool` instance.
    """
    if type(modifier) is bool:
        pass
    elif isinstance(modifier, bool):
        modifier = bool(modifier)
    else:
        raise TypeError(f'`multi` can be `bool` instance, got {modifier.__class__.__name__}.')
    
    return modifier


def validate_command_line_parameter_keyword_only(keyword_only):
    """
    Validates ``CommandLineParameter``'s `keyword_only` parameter.
    
    Parameters
    ----------
    keyword_only : `bool`
        Multi parameters to validate.
    
    Returns
    -------
    keyword_only : `bool`
        Validated multi parameter.
    
    Raises
    ------
    TypeError
        If `keyword_only` is not `bool` instance.
    """
    if type(keyword_only) is bool:
        pass
    elif isinstance(keyword_only, bool):
        keyword_only = bool(keyword_only)
    else:
        raise TypeError(f'`multi` can be `bool` instance, got {keyword_only.__class__.__name__}.')
    
    return keyword_only


class CommandLineParameter:
    """
    Command line parameter.
    
    Attributes
    ----------
    default_value : `None` or `Any`
        Default value to give if parameter was not passed.
    expected_type_identifier : `int`
        Identifier of the accepted type of the parameter.
    has_default : `bool`
        Whether the parameter has default value.
    modifier : `bool`
        Whether the parameter is a modifier.
    keyword : `None` or `bool`
        Keyword to pass the parameter.
    keyword_only : `bool`
        Whether the parameter is keyword only.
    multi : `bool`
        Whether the parameter accepts multiple values.
    name : `str`
        The parameter's name.
    """
    __slots__ = ('default_value', 'expected_type_identifier', 'has_default', 'modifier', 'keyword', 'keyword_only',
        'multi', 'name')
    
    def __new__(cls, name, *, default=DEFAULT_DEFAULT_VALUE, keyword=None, keyword_only=False, multi=False,
            expected_type=None, modifier=False):
        """
        Creates a new ``CommandLineParameter`` instance from the given parameters.
        
        Parameters
        ----------
        name : `str`
            The parameter's name.
        default : `Any`, Optional (Keyword only)
            Default value if the parameter is not present.
        keyword : `str`, Optional (Keyword only)
            Keyword to pass the parameter after if applicable.
        multi : `bool`
            Whether multiple parameters are accepted.
        expected_type : `None` or `str`, `type`, Optional (Keyword only)
            The expected type by the parameter. Defaults to `bool`.
        
        Raises
        ------
        TypeError
            - If `expected_type` is neither `None`, `str`, neither `type` instance.
            - If `name` is not `str` instance.
            - If `keyword` is neither `None` nor `str` instance.
            - If `multi` is not `bool` instance.
            - If `modifier` is not `bool` instance.
            - If `keyword_only` is not `bool` instance.
            - `default` and `modifier` parameters are mutually exclusive.
            - `keyword` parameter is required if `keyword_only` is `True`
            - Keyword parameters must have either `default` or `multi` parameters defined.
        ValueError
            If `expected_type` is correct type, but it's value is incorrect and cannot identifier converter for it.
        """
        name = validate_command_line_parameter_name(name)
        has_default, default_value = validate_command_line_parameter_multi(default)
        keyword = validate_command_line_parameter_keyword(keyword)
        multi = validate_command_line_parameter_multi(multi)
        expected_type_identifier = validate_command_line_parameter_expected_type_identifier(expected_type)
        modifier = validate_command_line_parameter_modifier(modifier)
        keyword_only = validate_command_line_parameter_keyword_only(keyword_only)
        
        if modifier:
            if has_default:
                raise TypeError(f'`default` and `modifier` parameters are mutually exclusive.')
            
            keyword_only = False
        
        else:
            if keyword_only:
                if (keyword is None):
                    raise TypeError(f'`keyword` parameter is required if `keyword_only` is `True`.')
            
                if (not has_default) and (not multi):
                    raise TypeError(f'Keyword parameters must have either `default` or `multi` parameters defined.')
        
        
        self = object.__new__(cls)
        self.name = name
        self.default_value = default_value
        self.keyword = keyword
        self.keyword_only = keyword_only
        self.multi = multi
        self.expected_type_identifier = expected_type_identifier
        self.has_default = has_default
        self.modifier = modifier
        return self
    
    
    def __repr__(self):
        """Returns the command line parameter's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' name=')
        repr_parts.append(repr(self.name))
        
        expected_type_name = TYPE_IDENTIFIER_TO_NAME[self.expected_type_identifier]
        repr_parts.append(', expected_type=')
        repr_parts.append(expected_type_name)
        
        if self.has_default:
            repr_parts.append(', default=')
            repr_parts.append(repr(self.default_value))
        
        keyword = self.keyword
        if (keyword is not None):
            repr_parts.append(', keyword=')
            repr_parts.append(repr(keyword))
        
        if self.multi:
            repr_parts.append(', multi=True')
        
        if self.modifier:
            repr_parts.append(', modifier=True')
        
        if self.keyword_only:
            repr_parts.append(', keyword_only=True')
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def is_positional_only(self):
        """
        Returns whether the command line parameter is a positional only parameter.
        
        Returns
        -------
        is_positional_only : `bool`
        """
        if self.modifier:
            is_positional_only = False
        else:
            if self.keyword is None:
                is_positional_only = True
            else:
                is_positional_only = False
        
        return is_positional_only
    
    
    def is_positional_or_keyword(self):
        """
        Returns whether the command line parameter is a positional or keyword.
        
        Returns
        -------
        is_positional_or_keyword : `bool`
        """
        if self.modifier:
            is_positional_or_keyword = False
        else:
            if self.keyword_only:
                is_positional_or_keyword = False
            else:
                if self.keyword is None:
                    is_positional_or_keyword = True
                else:
                    is_positional_or_keyword = False
        
        return is_positional_or_keyword
    
    
    def is_keyword_only(self):
        """
        Returns whether the parameter is keyword only.
        
        Returns
        -------
        is_keyword_only : `bool`
        """
        if self.modifier:
            is_keyword_only = False
        else:
            is_keyword_only = self.keyword_only
        
        return is_keyword_only
    
    
    def is_modifier(self):
        """
        Returns whether the command line parameter is a modifier parameter.
        
        Returns
        -------
        is_modifier : `bool`
        """
        return self.modifier


def normalize_command_name(command_name):
    """
    Normalises the given command name.
    
    Parameters
    ----------
    command_name : `str`
        The command name to normalize.
        
    """
    return command_name.lower().replace('_', '-')


class CommandLineCommand:
    """
    Attributes
    ----------
    _command_function : `None` or ``CommandLineCommandFunction``
        Command to call, if sub command could not be detected.
    _sub_commands : `None` or `dict` of (`str`, ``CommandLineCommand``) items
        Sub commands of the command.
    help : `str`
        Command help message.
    """
    __slots__ = ('_command_function', '_sub_commands', 'help', )
    
    def __new__(cls, name, help_):
        self = object.__new__(cls)
        self._command_function = None
        self._sub_commands = None
        self.help = None
        return self
    
    def register_sub_command(self, name):
        """
        Registers a sub command to the command.
        
        Parameters
        ----------
        name : `str`
            The name of the sub-command.
        
        Returns
        -------
        sub_command : ``CommandLineSubCommand``
        """
        sub_command = CommandLineSubCommand(name)
        sub_commands = self._sub_commands
        if (sub_commands is None):
            sub_commands = {}
            self._sub_commands = sub_commands
        
        sub_commands[sub_command.name] = sub_command
        return sub_command
    
    
    def register_command_function(self, function):
        """
        Parameters
        ----------
        function : `callable`
            The function to call when the command is used.
        
        Returns
        -------
        command_function : CommandLineCommandFunction
        """
        command_function = CommandLineCommandFunction(function)
        self._command_function = command_function
        return command_function


class CommandLineSubCommand:
    """
    Command line command category.
    
    Parameters
    ----------
    name : `str`
        The sub command category's name.
    """
    __slots__ = ('name',)
    def __new__(cls, name):
        name = normalize_command_name(name)
        
        self = object.__new__(cls)
        self.name = name
        self.

class CommandLineCommandFunction:
    """
    Command line function to call.
    
    Attributes
    ----------
    _function : `callable`
        The function to call.
    _parameters_keyword_only : `None` or `list` of ``CommandLineParameter``
        Keyword only parameters.
    _parameters_modifier : `None` or `list` of ``CommandLineParameter``
        Parameter modifiers.
    _parameters_positional_only : `None` or `list` of ``CommandLineParameter``
        Positional only parameters.
    _parameters_positional_or_keyword : `None` or `list` of ``CommandLineParameter``
        Positional only keyword only parameters.
    """
    __slots__ = ('_function', '_parameters_keyword_only', '_parameters_modifier', '_parameters_positional_only',
        '_parameters_positional_or_keyword')
    
    def __new__(cls, function):
        """
        Creates a new ``CommandLineCommandFunction`` instance.
        
        Parameters
        ----------
        function : `callable`
            The function to call when the command is used.
        """
        self = object.__new__(cls)
        self._function = function
        self._parameters_modifier = None
        self._parameters_positional_only = None
        self._parameters_keyword_only = None
        self._parameters_positional_or_keyword = None
        return self
    
    
    def add_parameter(self, parameter):
        """
        Adds a parameter to the command line command.
        
        Parameters
        ----------
        parameter : ``CommandLineParameter``
            The parameter to add.
        """
        if parameter.is_modifier():
            parameters_modifier = self._parameters_modifier
            if parameters_modifier is None:
                parameters_modifier = []
                self._parameters_modifier = parameters_modifier
            
            parameters_modifier.append(parameter)
        
        
        elif parameter.is_positional_only():
            if (self._parameters_keyword_only is not None) or (self._parameters_positional_or_keyword is not None):
                raise TypeError(f'Positional only parameter cannot be added after keyword, got: {parameter!r}.')
            
            parameters_positional_only = self._parameters_positional_only
            if (parameters_positional_only is None):
                parameters_positional_only = []
                self._parameters_positional_only = parameters_positional_only
            
            parameters_positional_only.append(parameter)
        
        elif parameter.is_positional_or_keyword():
            if (self._parameters_keyword_only is not None):
                raise TypeError(f'Positional or keyword only parameter cannot be added after keyword only, '
                    f'got: {parameter!r}.')
            
            parameters_positional_or_keyword = self._parameters_positional_or_keyword
            if (parameters_positional_or_keyword is None):
                parameters_positional_or_keyword = []
                self._parameters_positional_or_keyword = parameters_positional_or_keyword
            
            parameters_positional_or_keyword.append(parameter)
        
        elif parameter.is_keyword_only():
            parameters_keyword_only = self._parameters_keyword_only
            if (parameters_keyword_only is None):
                parameters_keyword_only = []
                self._parameters_keyword_only = parameters_keyword_only
            
            parameters_keyword_only.append(parameter)



