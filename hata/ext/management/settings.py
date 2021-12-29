from scarletio import from_json, to_json
from os.path import exists, isfile as is_file, join as join_paths, isdir, isdir as is_directory
from os import getcwd as get_current_working_directory, listdir as list_directory

from .checkout import checkout_list_structure, ELEMENT_TYPE_IDENTIFIER_STRING

KEY_BOT_DIRECTORIES = 'BOT_DIRECTORIES'
SETTINGS_FILE_NAME = '.settings.json'


class ProjectSettings:
    """
    Project configuration.
    
    Parameters
    ----------
    bot_directories : `list` of `str`
        Directories of each bot folder.
    directory_path : `str`
        Path to the project settings file.
    """
    __slots__ = ('bot_directories', 'directory_path', )
    
    @classmethod
    def _from_path(cls, directory_path):
        """
        Tries to create a project setting instance from the given directory.
        
        Parameters
        ----------
        directory_path : `str`
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
        file_path = join_paths(directory_path, SETTINGS_FILE_NAME)
        
        if not exists(file_path):
            return cls._create_empty(file_path)
        
        if not is_file(file_path):
            raise RuntimeError(
                f'Settings path is not a file: {file_path!r}.'
            )
        
        with open(file_path, 'r') as file:
            file_content = file.read()
        
        if not file_content:
            return cls._create_empty(file_path)
        
        try:
            json = from_json(file_content)
        except BaseException as err:
            raise RuntimeError(
                'Failed to decode settings file content.'
            ) from err
        
        if json is None:
            return cls._create_empty(file_path)
        
        
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
        
        # Check bot directories to list only the existing ones.
        if (bot_directories is not None):
            bot_directories = set(bot_directories)
            directories = set()
            
            for name in list_directory(directory_path):
                path = join_paths(directory_path, name)
                if is_directory(path):
                    directories.add(name)
            
            bot_directories.intersection_update(directories)
            if bot_directories:
                bot_directories = list(bot_directories)
            else:
                bot_directories = None
        
        
        self = object.__new__(cls)
        self.directory_path = directory_path
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
        self.directory_path = path
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
        
        with open(join_paths(self.directory_path, SETTINGS_FILE_NAME), 'w') as file:
            file.write(raw_data)


def load_settings_from_current_working_directory():
    """
    Loads the settings from the current working directory.
    
    Returns
    -------
    project_settings : ``ProjectSettings``
    """
    return ProjectSettings._from_path(get_current_working_directory())
