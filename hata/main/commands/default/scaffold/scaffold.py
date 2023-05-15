__all__ = ()

from os import mkdir as create_directory
from os.path import join as join_paths

from scarletio import get_short_executable

from ..... import __package__ as PACKAGE_NAME

from ....core.helpers import render_main_call_into

from .helpers import create_directory_recursive
from .naming import get_bot_constant_name, get_bot_display_name, get_bot_module_name, get_bot_variable_name


def create_gitignore_file(directory_path):
    """
    Creates a `/{project_name}/.gitignore` file.
    
    Parameters
    ----------
    directory_path : `str`
        Path to the file's directory.
    """
    with open(join_paths(directory_path, '.gitignore'), 'w') as file:
        file.write(
            f'# Generic\n'
            f'*.env\n'
            f'*.venv\n'
            f'\n'
            f'# Python\n'
            f'*.pyc\n'
            f'__pycache__/\n'
            f'\n'
            f'# Editor\n'
            f'.idea\n'
            f'\n'
            f'# Data files\n'
            f'*.pickle\n'
            f'*.sqlite3\n'
            f'\n'
            f'# Hata\n'
            f'.profiles/\n'
        )


def create_pyproject_toml_file(directory_path, project_name):
    """
    Creates a `/pyproject.toml` file`.
    
    Parameters
    ----------
    directory_path : `str`
        Path to the file's directory.
    project_name : `str`
        The project's name.
    """
    with open(join_paths(directory_path, 'pyproject.toml'), 'w') as file:
        file.write(
            f'[project]\n'
            f'name = \'{project_name}\'\n'
            f'\n'
            f'dependencies = [\n'
            f'    \'hata\',\n'
            f'    \'hata\[all]\',\n'
            f']\n'
            f'readme = \'README.md\'\n'
            f'requires-python = \'>=3.6\'\n'
            f'\n'
            f'dynamic = [\'version\', \'description\', \'optional-dependencies\']\n'
            f'\n'
            f'[build-system]\n'
            f'build-backend = \'setuptools.build_meta\'\n'
            f'requires = [\'setuptools\',\'setuptools-scm\']\n'
            f'\n'
            f'[project.scripts]\n'
            f'{project_name} = \'{project_name}.cli:main\'\n'
        )


def build_dot_env_file_content(bot_names):
    """
    Builds the content of `/{project_name}/.env` file.
    
    Parameters
    ----------
    bot_names : `list` of `str`
        The bots' names.
    
    Returns
    -------
    content : `str`
    """
    content_parts = []
    
    for bot_name in bot_names:
        bot_constant_name = get_bot_constant_name(bot_name)
        content_parts.append(bot_constant_name)
        content_parts.append('_TOKEN=\n')
    
    return ''.join(content_parts)


def create_dot_env_file(directory_path, bot_names):
    """
    Creates a `/{project_name}/.env` file.
    
    Parameters
    ----------
    directory_path : `str`
        Path to the file's directory.
    bot_names : `list` of `str`
        The bots' names.
    """
    with open(join_paths(directory_path, '.env'), 'w') as file:
        file.write(build_dot_env_file_content(bot_names))


def render_readme_section_project_into(into, project_name):
    """
    Renders the `README.md`'s `project` section.
    
    Parameters
    ----------
    into : `list` of `str`
        Content parts to render into.
    project_name : `str`
        The project's name.
    
    Returns
    -------
    into : `list` of `str`
    """
    project_display_name = get_bot_display_name(project_name)
    
    into.append('# ')
    into.append(project_display_name)
    
    into.append(
        '\n'
        '\n'
        'A '
    )
    into.append(PACKAGE_NAME)
    into.append(
        ' discord application generated using its `scaffold` command:\n'
        '```sh\n'
        '$ '
    )
    render_main_call_into(into, with_parameters = True)
    into.append(
        '\n'
        '```\n'
    )
    
    return into


def render_readme_section_scaffold(into):
    """
    Renders the `README.md`'s `scaffold` section.
    
    Parameters
    ----------
    into : `list` of `str`
        Content parts to render into.
    
    Returns
    -------
    into : `list` of `str`
    """
    into.append('## What is ')
    into.append(PACKAGE_NAME)
    into.append(
        ' scaffold?\n'
        '\n'
    )
    into.append(PACKAGE_NAME.capitalize())
    into.append(
        ' scaffold is used to automatically create a basic structure for your application.\n'
        'This includes code, configuration files, and other necessary files and assets.\n'
        '\n'
        'Even tho scaffold command is helpful to get a head start when building your application, it is still\n'
        'important to remember that the generated code should be always reviewed and modified as needed to ensure\n'
        'that it meets the requirements.\n'
    )
    
    return into


def render_readme_section_structure_into(into, project_name, bot_names):
    """
    Renders the `README.md`'s `structure` section.
    
    Parameters
    ----------
    into : `list` of `str`
        Content parts to render into.
    project_name : `str`
        The project's name.
    project_name : `str`
        The project's name.
    
    Returns
    -------
    into : `list` of `str`
    """
    render_readme_section_structure_directory_into(into, project_name, bot_names)
    into.append('\n')
    render_readme_section_structure_gitignore_into(into)
    into.append('\n')
    render_readme_section_structure_readme_into(into)
    into.append('\n')
    render_readme_section_structure_pyproject(into)
    into.append('\n')
    render_readme_section_structure_project(into, project_name)
    into.append('\n')
    render_readme_section_structure_dot_env(into, project_name)
    into.append('\n')
    render_readme_section_structure_project_init(into, project_name)
    into.append('\n')
    render_readme_section_structure_main(into, project_name)
    into.append('\n')
    render_readme_section_structure_cli(into, project_name)
    into.append('\n')
    render_readme_section_structure_bots(into, project_name)
    into.append('\n')
    render_readme_section_structure_bots_init(into, project_name, bot_names)
    for bot_name in bot_names:
        into.append('\n')
        render_readme_section_structure_bot(into, project_name, bot_name)
    into.append('\n')
    render_readme_section_structure_plugins(into, project_name)
    into.append('\n')
    render_readme_section_structure_plugins_init(into, project_name)
    
    return into


def render_readme_section_structure_directory_into(into, project_name, bot_names):
    """
    Renders the `README.md`'s `structure` section's directory part.
    
    Parameters
    ----------
    into : `list` of `str`
        Content parts to render into.
    project_name : `str`
        The project's name.
    project_name : `str`
        The project's name.
    
    Returns
    -------
    into : `list` of `str`
    """
    into.append(
        '## Directory structure\n'
        '\n'
        '```\n'
        'root\n'
        '├─ .gitignore\n'
        '├─ README.md\n'
        '├─ pyproject.toml\n'
        '└─ '
    )
    into.append(project_name)
    into.append(
        '\n'
        '    ├─ .env\n'
        '    ├─ __init__.py\n'
        '    ├─ __main__.py\n'
        '    ├─ cli.py\n'
        '    ├─ bots\n'
        '    │   ├─ __init__.py\n'
    )
    for bot_name, reversed_index in zip(bot_names, reversed(range(len(bot_names)))):
        bot_module_name = get_bot_module_name(bot_name)
        into.append('    │   ')
        into.append('├' if reversed_index else '└')
        into.append('─ ')
        into.append(bot_module_name)
        into.append('.py\n')
    into.append(
        '    └─ plugins\n'
        '        └─ __init__.py\n'
        '```\n'
    )
    
    return into


def render_readme_section_structure_gitignore_into(into):
    """
    Renders the `README.md`'s `structure ./gitignore` section.
    
    Parameters
    ----------
    into : `list` of `str`
        Content parts to render into.
    
    Returns
    -------
    into : `list` of `str`
    """
    into.append(
        '### ./gitignore\n'
        '\n'
        'A gitignore file specifies intentionally untracked files that Git should ignore. Files already tracked by\n'
        'Git are not affected, so make sure after updating it you `git add ".gitignore"` before anything else. Each\n'
        'line in a gitignore file specifies a pattern.\n'
    )
    
    return into


def render_readme_section_structure_readme_into(into):
    """
    Renders the `README.md`'s `structure ./README.md` section.
    
    Parameters
    ----------
    into : `list` of `str`
        Content parts to render into.
    
    Returns
    -------
    into : `list` of `str`
    """
    into.append(
        '### ./README.md\n'
        '\n'
        'A README file is an essential guide that gives a detailed description of your project.\n'
    )
    
    return into


def render_readme_section_structure_pyproject(into):
    """
    Renders the `README.md`'s `structure ./pyproject.toml` section.
    
    Parameters
    ----------
    into : `list` of `str`
        Content parts to render into.
    
    Returns
    -------
    into : `list` of `str`
    """
    into.append(
        '### ./pyproject.toml\n'
        '\n'
        'A text file that specifies what build dependencies your package needs.\n'
    )
    
    return into


def render_readme_section_structure_project(into, project_name):
    """
    Renders the `README.md`'s `structure ./{project_name}/` section.
    
    Parameters
    ----------
    into : `list` of `str`
        Content parts to render into.
    project_name : `str`
        The project's name.
    
    Returns
    -------
    into : `list` of `str`
    """
    into.append('### ./')
    into.append(project_name)
    into.append(
        '/\n'
        '\n'
        'The directory that contains your discord application.\n'
    )
    
    return into


def render_readme_section_structure_dot_env(into, project_name):
    """
    Renders the `README.md`'s `structure ./{project_name}/.env` section.
    
    Parameters
    ----------
    into : `list` of `str`
        Content parts to render into.
    project_name : `str`
        The project's name.
    
    Returns
    -------
    into : `list` of `str`
    """
    into.append('### ./')
    into.append(project_name)
    into.append(
        '/.env\n'
        '\n'
        'A `.env` file is a text file containing key - value pairs of environment variables. This file is normally\n'
        'included with a project, but not committed to source.\n'
        '\n'
        '`.env` files are used to store sensitive credentials. Your discord applications\' tokens are loaded from\n'
        'here too, so make sure it is populated correctly before starting your project.\n'
    )
    
    return into


def render_readme_section_structure_project_init(into, project_name):
    """
    Renders the `README.md`'s `structure ./{project_name}/__init__.py` section.
    
    Parameters
    ----------
    into : `list` of `str`
        Content parts to render into.
    project_name : `str`
        The project's name.
    
    Returns
    -------
    into : `list` of `str`
    """
    into.append('### ./')
    into.append(project_name)
    into.append(
        '/\\_\\_init\\_\\_.py\n'
        '\n'
        'This is a special python file that is used to indicate that the directory should be treated as package.\n'
        'It defines what can be directly imported from your package. Leaving it completely empty is also fine.\n'
    )
    
    return into


def render_readme_section_structure_main(into, project_name):
    """
    Renders the `README.md`'s `structure ./{project_name}/__main__.py` section.
    
    Parameters
    ----------
    into : `list` of `str`
        Content parts to render into.
    project_name : `str`
        The project's name.
    
    Returns
    -------
    into : `list` of `str`
    """
    executable_name = get_short_executable()
    
    into.append('### ./')
    into.append(project_name)
    into.append(
        '/\\_\\_main\\_\\_.py\n'
        '\n'
        'Often a python program is executed using `$ '
    )
    into.append(executable_name)
    into.append(
        ' project.py`. If your program is inside of a directory\n'
        'that has a `__main__.py` file then it can be ran using `$ '
    )
    into.append(executable_name)
    into.append(' -m project`.\n')
    
    return into


def render_readme_section_structure_cli(into, project_name):
    """
    Renders the `README.md`'s `structure ./{project_name}/cli.py` section.
    
    Parameters
    ----------
    into : `list` of `str`
        Content parts to render into.
    project_name : `str`
        The project's name.
    
    Returns
    -------
    into : `list` of `str`
    """
    into.append('### ./')
    into.append(project_name)
    into.append(
        '/cli.py\n'
        '\n'
        'Contains the *command line interface* code, basically the main function is defined here.\n'
    )
    
    return into


def render_readme_section_structure_bots(into, project_name):
    """
    Renders the `README.md`'s `structure ./{project_name}/bots/` section.
    
    Parameters
    ----------
    into : `list` of `str`
        Content parts to render into.
    project_name : `str`
        The project's name.
    
    Returns
    -------
    into : `list` of `str`
    """
    into.append('### ./')
    into.append(project_name)
    into.append(
        '/bots/\n'
        '\n'
        'This directory contains the bots ran by your discord application.\n'
    )
    
    return into


def render_readme_section_structure_bots_init(into, project_name, bot_names):
    """
    Renders the `README.md`'s `structure ./{project_name}/bots/__init__.py` section.
    
    Parameters
    ----------
    into : `list` of `str`
        Content parts to render into.
    project_name : `str`
        The project's name.
    bot_names : `list` of `str`
        The bots' names.
    
    Returns
    -------
    into : `list` of `str`
    """
    bot_name = bot_names[0]
    bot_variable_name = get_bot_variable_name(bot_name)
    
    into.append('### ./')
    into.append(project_name)
    into.append(
        '/bots/\\_\\_init\\_\\_.py\n'
        '\n'
        'Imports the defined bots in the directory.\n'
        '\n'
        'To import a bot from here do either:\n'
        '```py\n'
        'from '
    )
    into.append(project_name)
    into.append('.bots import ')
    into.append(bot_variable_name)
    into.append(
        ' # absolute import\n'
        '```\n'
        'or\n'
        '```py\n'
        'from ..bots import '
    )
    into.append(bot_variable_name)
    into.append(
        ' # relative import\n'
        '```\n'
    )
    
    return into


def render_readme_section_structure_bot(into, project_name, bot_name):
    """
    Renders the `README.md`'s `structure ./{project_name}/bots/{bot_name}.py` section.
    
    Parameters
    ----------
    into : `list` of `str`
        Content parts to render into.
    project_name : `str`
        The project's name.
    bot_name : `str`
        The bot's name.
    
    Returns
    -------
    into : `list` of `str`
    """
    bot_display_name = get_bot_display_name(bot_name)
    bot_module_name = get_bot_module_name(bot_name)
    
    into.append('### ./')
    into.append(project_name)
    into.append('/bots/')
    into.append(bot_module_name)
    into.append(
        '.py\n'
        '\n'
    )
    into.append(bot_display_name)
    into.append(
        ' is initialized here and should be configured here too. As in which intents and extensions it uses.\n'
        'This file should also define all core functionality that is required by plugins to correctly integrate.\n'
    )
    
    return into


def render_readme_section_structure_plugins(into, project_name):
    """
    Renders the `README.md`'s `structure ./{project_name}/bots/plugins/` section.
    
    Parameters
    ----------
    into : `list` of `str`
        Content parts to render into.
    project_name : `str`
        The project's name.
    
    Returns
    -------
    into : `list` of `str`
    """
    into.append('### ./')
    into.append(project_name)
    into.append(
        '/plugins/\n'
        '\n'
        'Plugins are components of the application that add a specific functionality to it.\n'
        'They are modules, meaning they can be added or removed as required without modifying the core codebase.\n'
        '\n'
        'Plugins can be defined in both standalone file or in package format as well:\n'
        '```\n'
        'plugins\n'
        '├─ __init__.py\n'
        '└─ my_plugin_0.py\n'
        '└─ my_plugin_1\n'
        '    ├─ __init__.py\n'
        '    └─ file_n.py\n'
        '```\n'
    )
    
    return into


def render_readme_section_structure_plugins_init(into, project_name):
    """
    Renders the `README.md`'s `structure ./{project_name}/bots/plugins/__init__.py` section.
    
    Parameters
    ----------
    into : `list` of `str`
        Content parts to render into.
    project_name : `str`
        The project's name.
    
    Returns
    -------
    into : `list` of `str`
    """
    into.append('### ./')
    into.append(project_name)
    into.append(
        '/plugins/\_\_init\_\_.py\n'
        '\n'
        'This `__init__.py` is required for cross-plugin imports.\n'
        '\n'
        'The difference between this and other `__init__.py` files in a plugin directory is that here we mark the\n'
        'directory as a plugin root, meaning this file will NOT stop additional files (or directories) to be\n'
        'identified as plugins.\n'
    )
    
    return into



def render_readme_section_install(into):
    """
    Renders the `README.md`'s `install` section.
    
    Parameters
    ----------
    into : `list` of `str`
        Content parts to render into.
    
    Returns
    -------
    into : `list` of `str`
    """
    executable_name = get_short_executable()
    
    into.append(
        '## Install\n'
        '\n'
        '```\n'
        '$ '
    )
    into.append(executable_name)
    into.append(
        ' -m pip install .\n'
        '```\n'
    )
    
    return into


def render_readme_section_cli(into, project_name):
    """
    Renders the `README.md`'s `cli` section.
    
    Parameters
    ----------
    into : `list` of `str`
        Content parts to render into.
    
    Returns
    -------
    into : `list` of `str`
    """
    executable_name = get_short_executable()
    
    into.append(
        '## Running CLI\n'
        '\n'
        '```\n'
        '$ '
    )
    into.append(executable_name)
    into.append(' -m ')
    into.append(project_name)
    into.append(
        ' help\n'
        '```\n'
        'or\n'
        '```\n'
        '$ '
    )
    into.append(project_name)
    into.append(
        ' help\n'
        '```\n'
    )
    
    return into


def create_readme_content(project_name, bot_names):
    """
    Creates the content of the `/README.md`  file.
    
    Parameters
    ----------
    project_name : `str`
        The project's name.
    bot_names : `list` of `str`
        The bots' names.
    
    Returns
    -------
    content : `str`
    """
    content_parts = []
    render_readme_section_project_into(content_parts, project_name)
    content_parts.append('\n')
    render_readme_section_scaffold(content_parts)
    content_parts.append('\n')
    render_readme_section_structure_into(content_parts, project_name, bot_names)
    content_parts.append('\n')
    render_readme_section_install(content_parts)
    content_parts.append('\n')
    render_readme_section_cli(content_parts, project_name)
    return ''.join(content_parts)


def create_readme_file(directory_path, project_name, bot_names):
    """
    Creates a `/README.md` file.
    
    Parameters
    ----------
    directory_path : `str`
        Path to the file's directory.
    project_name : `str`
        The project's name.
    bot_names : `list` of `str`
        The bots' names.
    """
    with open(join_paths(directory_path, 'README.md'), 'w') as file:
        file.write(create_readme_content(project_name, bot_names))


def create_project_init_file(directory_path):
    """
    Creates a `/{project_name}/__init__.py` file.
    
    Parameters
    ----------
    directory_path : `str`
        Path to the file's directory.
    """
    with open(join_paths(directory_path, '__init__.py'), 'w') as file:
        file.write(
            f'__all__ = ()\n'
        )


def create_cli_file(directory_path):
    """
    Creates a `/{project_name}/cli.py` file.
    
    Parameters
    ----------
    directory_path : `str`
        Path to the file's directory.
    """
    with open(join_paths(directory_path, 'cli.py'), 'w') as file:
        file.write(
            f'__all__ = (\'main\',)\n'
            f'\n'
            f'def main():\n'
            f'    try:\n'
            f'        from hata.main import execute_command_from_system_parameters\n'
            f'    except ImportError as err:\n'
            f'        raise ImportError(\n'
            f'            \'Couldn\\\'t import {PACKAGE_NAME}. \'\n'
            f'            \'Are you sure it\\\'s installed and available on your PYTHONPATH environment variable? \'\n'
            f'            \'Did you forget to activate a virtual environment?\'\n'
            f'        ) from err\n'
            f'\n'
            f'    from hata.ext.plugin_auto_reloader import start_auto_reloader, warn_auto_reloader_availability\n'
            f'    from hata.ext.plugin_loader import load_all_plugin, frame_filter, register_plugin\n'
            f'    from scarletio import get_event_loop, write_exception_sync\n'
            f'\n'
            f'    from . import bots\n'
            f'\n'
            f'    register_plugin(f\'{{__spec__.parent}}.plugins\')\n'
            f'\n'
            f'    try:\n'
            f'        load_all_plugin()\n'
            f'    except BaseException as err:\n'
            f'        write_exception_sync(err, filter = frame_filter)\n'
            f'        get_event_loop().stop()\n'
            f'        raise SystemExit from None\n'
            f'\n'
            f'    warn_auto_reloader_availability()\n'
            f'    start_auto_reloader()\n'
            f'\n'
            f'    execute_command_from_system_parameters()\n'
        )


def create_main_file(directory_path):
    """
    Creates a `/{project_name}/__main__.py` file.
    
    Parameters
    ----------
    directory_path : `str`
        Path to the file's directory.
    """
    with open(join_paths(directory_path, '__main__.py'), 'w') as file:
        file.write(
            f'__all__ = ()\n'
            f'\n'
            f'from .cli import main\n'
            f'\n'
            f'if __name__ == \'__main__\':\n'
            f'    main()\n'
        )


def build_bots_init_file_content(bot_names):
    """
    Builds the content of `/{project_name}/bots/__init__.py` file.
    
    Parameters
    ----------
    bot_names : `list` of `str`
        The bots' names.
    
    Returns
    -------
    content : `str`
    """
    content_parts = []
    
    bot_module_names = [get_bot_module_name(bot_name) for bot_name in bot_names]
    
    for bot_module_name in bot_module_names:
        content_parts.append('from .')
        content_parts.append(bot_module_name)
        content_parts.append(' import *\n')
    
    content_parts.append('\n\n__all__ = (\n')
    
    for bot_module_name in bot_module_names:
        content_parts.append('    *')
        content_parts.append(bot_module_name)
        content_parts.append('.__all__,\n')
    
    content_parts.append(')\n')
    
    return ''.join(content_parts)


def create_bots_init_file(directory_path, bot_names):
    """
    Creates a `/{project_name}/bots/__init__.py` file.
    
    Parameters
    ----------
    directory_path : `str`
        Path to the file's directory.
    bot_names : `list` of `str`
        The bots' names.
    """
    with open(join_paths(directory_path, '__init__.py'), 'w') as file:
        file.write(build_bots_init_file_content(bot_names))


def create_bot_file(directory_path, bot_name):
    """
    Creates a `/{project_name}/bots/{bot_name}.py` file.
    
    Parameters
    ----------
    directory_path : `str`
        Path to the file's directory.
    bot_name : `str`
        The bot's name.
    """
    bot_module_name = get_bot_module_name(bot_name)
    bot_variable_name = get_bot_variable_name(bot_name)
    bot_constant_name = get_bot_constant_name(bot_name)
    with open(join_paths(directory_path, bot_module_name + '.py'), 'w') as file:
        file.write(
            f'__all__ = (\'{bot_variable_name}\',)\n'
            f'\n'
            f'from hata import Client\n'
            f'from hata.env import get_str_env\n'
            f'\n'
            f'\n'
            f'{bot_variable_name} = Client(\n'
            f'    get_str_env(\'{bot_constant_name}_TOKEN\', raise_if_missing_or_empty = True)\n'
            f')\n'
        )


def create_plugins_init_file(directory_path):
    """
    Creates a `/{project_name}/plugins/__init__.py` file.
    
    Parameters
    ----------
    directory_path : `str`
        Path to the file's directory.
    """
    with open(join_paths(directory_path, '__init__.py'), 'w') as file:
        file.write(
            f'from hata.ext.plugin_loader import mark_as_plugin_root_directory\n'
            f'\n'
            f'mark_as_plugin_root_directory()\n'
        )


def create_project_structure(root_directory_path, project_name, bot_names):
    """
    Creates a project.
    
    Structure:
    ```
    root
    ├─ .gitignore
    ├─ README.md
    ├─ pyproject.toml
    └─ { project }
        ├─ .env
        ├─ __init__.py
        ├─ __main__.py
        ├─ cli.py
        ├─ bots
        │   ├─ __init__.py
        │   ├─ { bot_names[n] }.py
        │   └─ ...
        └─ plugins
            └─ __init__.py
    ```
    
    Parameters
    ----------
    root_directory_path : `str`
        The project's root directory's path.
    project_name : `str`
        The project's name.
    bot_names : `list` of `str`
        The bots' names.
    """
    # root
    create_directory_recursive(root_directory_path)
    
    create_gitignore_file(root_directory_path)
    create_readme_file(root_directory_path, project_name, bot_names)
    create_pyproject_toml_file(root_directory_path, project_name)
    
    # root / { project_name }
    project_directory_path = join_paths(root_directory_path, project_name)
    create_directory(project_directory_path)
    
    create_project_init_file(project_directory_path)
    create_main_file(project_directory_path)
    create_dot_env_file(project_directory_path, bot_names)
    create_cli_file(project_directory_path)
    
    # root / { project_name } / bots
    bots_directory_path = join_paths(project_directory_path, 'bots')
    create_directory(bots_directory_path)
    
    create_bots_init_file(bots_directory_path, bot_names)
    for bot_name in bot_names:
        create_bot_file(bots_directory_path, bot_name)
    
    # root / { project_name } / plugins
    plugins_directory_path = join_paths(project_directory_path, 'plugins')
    create_directory(plugins_directory_path)
    
    create_plugins_init_file(plugins_directory_path)
