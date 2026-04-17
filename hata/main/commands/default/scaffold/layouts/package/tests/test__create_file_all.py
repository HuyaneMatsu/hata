import vampytest

from ..structure import (
    create_bot_file, create_bots_init_file, create_cli_file, create_constants_file, create_dot_env_file,
    create_gitignore_file, create_main_file, create_plugins_init_file, create_project_init_file,
    create_pyproject_toml_file, create_readme_file
)


@vampytest.call_with(create_gitignore_file, '.gitignore', ())
@vampytest.call_with(create_readme_file, 'README.md', ('satori', ['red', 'eye']))
@vampytest.call_with(create_pyproject_toml_file, 'pyproject.toml', ('satori',))
@vampytest.call_with(create_dot_env_file, '.env', (['red', 'eye'],))
@vampytest.call_with(create_project_init_file, '__init__.py', ())
@vampytest.call_with(create_cli_file, 'cli.py', ())
@vampytest.call_with(create_main_file, '__main__.py', ())
@vampytest.call_with(create_bots_init_file, '__init__.py', (['red', 'heart'],))
@vampytest.call_with(create_bot_file, 'red.py', ('red',))
@vampytest.call_with(create_plugins_init_file, '__init__.py', ())
@vampytest.call_with(create_bots_init_file, '__init__.py', (['red', 'heart'],))
@vampytest.call_with(create_constants_file, 'constants.py', (['red', 'heart'],))
def test__create_file_all(function, expected_file_name, parameters):
    """
    Tests whether the given `create_file` function works as intended.
    
    Parameters
    ----------
    function : `(str, *object) -> null`
        The file creator function to test.
    expected_file_name : `str`
        The file's name to expect.
    parameters : `tuple<object>`
        Parameters to pass to the function.
    """
    create_file_called = 0
    input_directory_path = 'ayaya'
    
    
    def create_file(directory_path, file_name, content):
        nonlocal input_directory_path
        nonlocal expected_file_name
        nonlocal create_file_called
        
        create_file_called += 1
        
        vampytest.assert_eq(directory_path, input_directory_path)
        vampytest.assert_eq(file_name, expected_file_name)
        vampytest.assert_instance(content, str)
    
    
    mocked = vampytest.mock_globals(function, create_file = create_file)
    mocked(input_directory_path, *parameters)
    
    vampytest.assert_eq(create_file_called, 1)
