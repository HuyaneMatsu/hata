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
    keyword : `None` or `bool`
        Keyword to pass the parameter.
    multi : `bool`
        Whether the parameter accepts multiple values.
    name : `str`
        The parameter's name.
    """
    __slots__ = ('default_value', 'expected_type_identifier', 'has_default', 'keyword', 'multi', 'name')
    
    def __new__(cls, name, *, default=DEFAULT_DEFAULT_VALUE, keyword=None, multi=False, expected_type=None):
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
        """
        
        name = validate_command_line_parameter_name(name)
        has_default, default_value = validate_command_line_parameter_multi(default)
        keyword = validate_command_line_parameter_keyword(keyword)
        multi = validate_command_line_parameter_multi(multi)
        expected_type_identifier = validate_command_line_parameter_expected_type_identifier(expected_type)
        
        self = object.__new__(cls)
        self.name = name
        self.default_value = default_value
        self.keyword = keyword
        self.multi = multi
        self.expected_type_identifier = expected_type_identifier
        self.has_default = has_default
        return self
    
