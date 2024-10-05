__all__ = ()

from os import environ as environmental_variables, getcwd as get_current_working_directory
from os.path import dirname as get_directory_name, isfile as is_file, join as join_paths
from sys import _getframe as get_frame

try:
    from os import environb as environmental_variables_binary
except ImportError:
    environmental_variables_binary = None

from scarletio import RichAttributeErrorBaseType

from .parsing import parse_variables


MODULE_FRAME_NAME = '<module>'


def find_launched_location():
    """
    Finds the file that was launched.
    
    Returns
    -------
    location : `None`, `str`
    """
    frame = get_frame()
    
    last_named_location = None
    
    while True:
        frame = frame.f_back
        if frame is None:
            break
        
        # They might falsely name frames with auto generated functions, so check variables as well
        if (frame.f_code.co_name != MODULE_FRAME_NAME):
            continue
        
        frame_global = frame.f_globals
        # Try to not compare locals with globals if we are inside of a function.
        if (frame.f_locals is not frame_global):
            continue
        
        location = frame_global.get('__file__', None)
        if location is None:
            module_specification = frame_global.get('__spec__', None)
            if module_specification is not None:
                location = module_specification.origin
        
        if location is not None:
            last_named_location = location
    
    return last_named_location


def find_dot_env_file_in_launched_location():
    """
    Tries to find dotenv file to load where the project is located.
    
    Returns
    -------
    file_path : `None`, `str`
    """
    location = find_launched_location()
    if (location is not None):
        file_path = join_paths(get_directory_name(location), '.env')
        if is_file(file_path):
            return file_path


def find_dot_env_file_in_current_working_directory():
    """
    Tries to find dotenv file to load where the program was started at.
    
    Returns
    -------
    file_path : `None`, `str`
    """
    location = get_current_working_directory()
    if (location is not None):
        if is_file(location):
            location = get_directory_name(location)
        
        file_path = join_paths(location, '.env')
        if is_file(file_path):
            return file_path


class DotEnvResult(RichAttributeErrorBaseType):
    """
    Represents result of loading a `.env` file or just content.
    
    Attributes
    ----------
    file_path : `str`
        Path to the loaded file.
    parser_failure_info : `None`, ``ParserFailureInfo``
        Failure info if parsing failed.
    variables : `dict<str, None | str>`
        The loaded environmental variables.
    """
    __slots__ = ('file_path', 'parser_failure_info', 'variables')
    
    def __new__(cls, variables, parser_failure_info, file_path):
        """
        Creates a new dot-env result.
        
        Parameters
        ----------
        variables : `dict<str, None | str>`
            The loaded environmental variables.
        parser_failure_info : `None`, ``ParserFailureInfo``
            Failure info if parsing failed.
        file_path : `str`
            Path to the loaded file.
        """
        self = object.__new__(cls)
        self.variables = variables
        self.parser_failure_info = parser_failure_info
        self.file_path = file_path
        return self
    
    
    def insert_to_environmental_variables(self):
        """
        Inserts the parsed variables into the environmental ones. If the variable already exists, will not overwrite it.
        
        Returns
        -------
        self : `instance<type<self>>`
        """
        for key, value in self.variables.items():
            if value is None:
                value = ''
            
            environmental_variables.setdefault(key, value)
            if (environmental_variables_binary is not None):
                environmental_variables_binary.setdefault(key.encode(), value.encode())
        
        return self
    
    
    def raise_if_failed(self):
        """
        Raises an exception with a reason why loading failed.
        
        Returns
        -------
        self : `instance<type<self>>`
        
        Raises
        ------
        SyntaxError
        """
        parser_failure_info = self.parser_failure_info
        if (parser_failure_info is not None):
            raise SyntaxError(
                parser_failure_info.get_error_message(),
                (
                    self.file_path,
                    parser_failure_info.line_index + 1,
                    parser_failure_info.index + 1,
                    parser_failure_info.line,
                ),
            )
        
        return self
    
    
    def __repr__(self):
        """Returns the dot env result's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' variables: ')
        repr_parts.append(repr(len(self.variables)))
        
        parser_failure_info = self.parser_failure_info
        if (parser_failure_info is not None):
            repr_parts.append(', parser_failure_info = ')
            repr_parts.append(repr(parser_failure_info))
        
        file_path = self.file_path
        if (file_path is not None):
            repr_parts.append(' file_path = ')
            repr_parts.append(repr(file_path))
        
        repr_parts.append('>')
        return ''.join(repr_parts)


def load_dot_env(value, file_path = None):
    """
    Loads the `.env` variables from the given content
    
    Parameters
    ----------
    value : `str`
        The value to parse.
    file_path : `None`, `str`
        File path to show u
    
    Returns
    -------
    dot_env_result : ``DotEnvResult``
    """
    variables, parser_failure_info = parse_variables(value)
    return DotEnvResult(variables, parser_failure_info, file_path)


def load_dot_env_from_file(file_path):
    """
    Loads the `.env` file from the given path.
    
    Parameters
    ----------
    file_path : `str`
        The path of the file to load.
    
    Returns
    -------
    dot_env_result : ``DotEnvResult``
    """
    with open(file_path, 'r') as file:
        value = file.read()
    
    return load_dot_env(value, file_path)
