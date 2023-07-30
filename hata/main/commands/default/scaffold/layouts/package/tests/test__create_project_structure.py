from os.path import join as join_paths
from types import FunctionType

import vampytest

from ..structure import create_project_structure


def test__create_project_structure():
    """
    Tests whether ``create_project_structure`` works as intended.
    """
    created_paths = set()
    
    # Adjust `create_file`
    
    def create_file(directory_path, file_name, content):
        nonlocal created_paths
        created_paths.add(('f', join_paths(directory_path, file_name)))
    
    def create_directory(directory_path):
        nonlocal created_paths
        created_paths.add(('d', directory_path))
    
    # Mock all functions
    
    function_globals = create_project_structure.__globals__
    
    for variable_name, variable_value in function_globals.items():
        if (
            variable_name.startswith('create_') and
            variable_name not in ('create_directory', 'create_directory_recursive')
        ):
            function_globals[variable_name] = FunctionType(
                variable_value.__code__,
                {
                    **variable_value.__globals__,
                    'create_file': create_file,
                },
                variable_value.__name__,
                variable_value.__defaults__,
                variable_value.__closure__,
            )
    
    function_globals['create_directory'] = create_directory
    function_globals['create_directory_recursive'] = create_directory
    
    
    create_project_structure_copy = FunctionType(
        create_project_structure.__code__,
        function_globals,
        create_project_structure.__name__,
        create_project_structure.__defaults__,
        create_project_structure.__closure__,
    )
    
    input_root_directory_path = 'ayaya'
    input_project_name = 'satori'
    input_bot_names = ['red', 'heart']
    
    create_project_structure_copy(input_root_directory_path, input_project_name, input_bot_names)
    
    vampytest.assert_eq(
        created_paths,
        {
            ('d', join_paths(input_root_directory_path)),
            ('f', join_paths(input_root_directory_path, '.gitignore')),
            ('f', join_paths(input_root_directory_path, 'README.md')),
            ('f', join_paths(input_root_directory_path, 'pyproject.toml')),
            
            ('d', join_paths(input_root_directory_path, input_project_name)),
            ('f', join_paths(input_root_directory_path, input_project_name, '__init__.py')),
            ('f', join_paths(input_root_directory_path, input_project_name, '__main__.py')),
            ('f', join_paths(input_root_directory_path, input_project_name, '.env')),
            ('f', join_paths(input_root_directory_path, input_project_name, 'cli.py')),
            ('f', join_paths(input_root_directory_path, input_project_name, 'constants.py')),
            
            ('d', join_paths(input_root_directory_path, input_project_name, 'bots')),
            ('f', join_paths(input_root_directory_path, input_project_name, 'bots', '__init__.py')),
            *(
                ('f', join_paths(input_root_directory_path, input_project_name, 'bots', bot_name + '.py'))
                for bot_name in input_bot_names
            ),
            
            ('d', join_paths(input_root_directory_path, input_project_name, 'plugins')),
            ('f', join_paths(input_root_directory_path, input_project_name, 'plugins', '__init__.py')),
        },
    )
