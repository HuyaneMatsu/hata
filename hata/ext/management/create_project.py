from os.path import abspath as get_absolute_path, join as join_paths, exists, isdir as is_directory, \
    isfile as is_file, getcwd as get_current_working_directory
from os import makedirs as make_directories

from dotenv import dotenv_values as load_into_dictionary

from .utils import render_exception

FILE_CONTENT_MANAGE_PY = (
"""# hata's command-line utility for administrative tasks.


def main():
    # Runs administrative tasks.
    try:
        from hata.ext.management import execute_command_from_system_parameters
    except ImportError as err:
        raise ImportError(
            'Couldn\'t import hata. Are you sure it\'s installed and available on your PYTHONPATH environment '
            'variable? Did you forget to activate a virtual environment?'
        ) from err
    
    execute_command_from_system_parameters()


if __name__ == '__main__':
    main()
"""
)

FILE_CONTENT_ENV = (
"""# Your environmental variables for non-public variables go here
"""
)

CONFIG_PY = (
"""# Configuration file for all bots running from the project.

SHARED_EXTENSIONS_DIRECTORY_NAME = 'shared_extensions'
"""
)

PROJECT_TEMPLATE = (
    (('manage.py', ), FILE_CONTENT_MANAGE_PY, ),
    (('.env', ), FILE_CONTENT_ENV, ),
    (('config.py', ), CONFIG_PY, ),
    (('shared_extensions', None), None, ),
    (('.project.json'), None, ),
)


def create_project(project_name, project_path):
    if not project_name.isidentifier():
        return f'Project name must be a valid identifier, got {project_name!r}.'
    
    if project_path is None:
        project_path = get_current_working_directory('.')
    
    project_directory = join_paths(project_path, project_name)
    
    try:
        make_directories(project_directory)
    except FileExistsError:
        return f'{project_directory!r} already exists'
    except OSError as err:
        return render_exception(err)
    
    for paths, file_content in PROJECT_TEMPLATE:
        paths_length = len(paths)
        
        file_name = paths[paths_length-1]
        
        if paths_length == 1:
            paths = None
        else:
            paths = paths[:paths_length-1]
        
        if (paths is None):
            folder_path = project_directory
        else:
            folder_path = join_paths(project_directory, *paths)
            make_directories(folder_path, exist_ok=True)
        
        if (file_name is not None):
            file_path = join_paths(folder_path, file_name)
            
            file = open(file_path, 'w')
            
            if (file_content is not None):
                file.write(file_content)
            
            file.close()
    
    return f'Project created at: {project_name!r}'
