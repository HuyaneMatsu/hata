from hata import from_json, to_json
from os.path import exists, isfile as is_file
from os import getcwd as get_current_working_directory

from .checkout import checkout_list_structure, ELEMENT_TYPE_IDENTIFIER_STRING

KEY_BOT_DIRECTORIES = 'BOT_DIRECTORIES'

class ProjectSettings:
    """
    Project configuration.
    
    Parameters
    ----------
    bot_directories : `list` of `str`
        Directories of each bot folder.
    path : `str`
        Path to the project settings file.
    """
    __slots__ = ('bot_directories', 'path', )
    
    @classmethod
    def _from_path(cls, path):
        """
        Tries to create a project setting instance from the given directory.
        
        Parameters
        ----------
        path : `str`
            Path to the file.
        
        Returns
        -------
        self : ``ProjectSettings``
        
        Raises
        ------
        RuntimeError
            - If `path` refers to not a file.
            - Unexpected file content or structure.
        """
        if not exists(path):
            return cls._create_empty(path)
        
        if not is_file(path):
            raise RuntimeError(f'Settings path is not a file: {path!r}.')
        
        with open(path, 'r') as file:
            file_content = file.read()
        
        if not file_content:
            return cls._create_empty(path)
        
        try:
            json = from_json(file_content)
        except BaseException as err:
            raise RuntimeError(
                'Failed to decode settings file content.'
            ) from err
        
        if json is None:
            return cls._create_empty(path)
        
        
        if not isinstance(json, dict):
            raise RuntimeError(
                'Settings file structure incorrect, expected dictionary as root object.'
            )
        
        try:
            bot_directories = json[KEY_BOT_DIRECTORIES]
        except KeyError:
            bot_directories = None
        else:
            bot_directories = checkout_list_structure(
                bot_directories,
                'bot_directories',
                True,
                ELEMENT_TYPE_IDENTIFIER_STRING,
                False,
            )
        
        self = object.__new__(cls)
        self.path = path
        self.bot_directories = bot_directories
        return self
    
    
    @classmethod
    def _create_empty(cls, path):
        """
        Creates an empty project setting instance with default values set.
        
        Parameters
        ----------
        path : `str`
            Path to the file.
        """
        self = object.__new__(cls)
        self.path = path
        self.bot_directories = None
        return self
    
    
    def _save(self):
        """
        Saves the settings to it's respective path.
        """
        data = {}
        
        bot_directories = self.bot_directories
        if (bot_directories is not None):
            data[KEY_BOT_DIRECTORIES] = bot_directories
        
        raw_data = to_json(data)
        
        with open(self.path, 'w') as file:
            file.write(raw_data)


def load_settings_from_current_working_directory():
    """
    Loads the settings from teh current working directory.
    
    Returns
    -------
    project_settings : ``ProjectSettings``
    """
    return ProjectSettings._from_path(get_current_working_directory())
