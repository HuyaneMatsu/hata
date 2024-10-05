__all__ = ('create_project_structure',)

from os import mkdir as create_directory
from os.path import join as join_paths

from ....... import __package__ as PACKAGE_NAME

from ...helpers import create_directory_recursive
from ...naming import get_bot_constant_name, get_bot_module_name, get_bot_variable_name

from .readme_rendering import build_readme_content


def create_file(directory_path, file_name, content):
    """
    Creates a file at the given position described by `directory_path` and `file_name`.
    
    Parameters
    ----------
    directory_path : `str`
        Path to the file's directory.
    file_name : `str`
        The file's name.
    content : `str`
        The content to write.
    """
    with open(join_paths(directory_path, file_name), 'w', encoding = 'utf-8') as file:
        file.write(content)


def create_gitignore_file(directory_path):
    """
    Creates a `/{project_name}/.gitignore` file.
    
    Parameters
    ----------
    directory_path : `str`
        Path to the file's directory.
    """
    create_file(
        directory_path,
        '.gitignore',
        (
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
        ),
    )


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
    create_file(directory_path, 'README.md', build_readme_content(project_name, bot_names))


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
    create_file(
        directory_path,
        'pyproject.toml',
        (
            f'[project]\n'
            f'name = \"{project_name}\"\n'
            f'\n'
            f'dependencies = [\n'
            f'    \"{PACKAGE_NAME!s}\",\n'
            f'    \"{PACKAGE_NAME!s}[all]\",\n'
            f']\n'
            f'readme.file = "README.md"\n'
            f'readme.content-type = "text/markdown"\n'
            f'requires-python = \">=3.6\"\n'
            f'\n'
            f'dynamic = [\n'
            f'    \"version\",\n'
            f'    \"optional-dependencies\",\n'
            f']\n'
            f'\n'
            f'[build-system]\n'
            f'build-backend = \"setuptools.build_meta\"\n'
            f'requires = [\n'
            f'    \"setuptools\",\n'
            f'    \"setuptools-scm\"\n'
            f']\n'
            f'\n'
            f'[project.scripts]\n'
            f'# Allows doing: "$ {project_name!s}" from terminal after installed.\n'
            f'{project_name!s} = \"{project_name!s}.cli:main\"\n'
            f'\n'
            f'[tool.setuptools]\n'
            f'include-package-data = false\n'
            f'\n'
            f'# `packages` are the directories with that should be included when installed.\n'
            f'# Includes all the `.py` files by default and no other files.\n'
            f'# Should NOT include test directories.\n'
            f'packages = [\n'
            f'    \"{project_name!s}\",\n'
            f'    \"{project_name!s}.bots\",\n'
            f'    \"{project_name!s}.plugins\",\n'
            f']\n'
            f'\n'
            f'[tool.setuptools.package-data]\n'
            f'# Additional files that should be included when installing\n'
            f'# Example: include all `.png` files within `images` plugin\'s assets directory\n'
            f'# This directory also have to be added to `packages` to work.\n'
            f'# (this is not an actually created plugin, just an example):\n'
            f'# "{project_name!s}.plugins.images.assets" = ["*.png"]\n'
            f'# Example: include all `.txt` files:\n'
            f'# "*" = ["*.txt"]\n'
            f'\n'
            f'# References:\n'
            f'# - https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html\n'
            f'# - https://setuptools.pypa.io/en/latest/userguide/datafiles.html\n'
        ),
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
        content_parts.append('_TOKEN =\n')
    
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
    create_file(directory_path, '.env', build_dot_env_file_content(bot_names))


def create_project_init_file(directory_path):
    """
    Creates a `/{project_name}/__init__.py` file.
    
    Parameters
    ----------
    directory_path : `str`
        Path to the file's directory.
    """
    create_file(directory_path, '__init__.py', '__all__ = ()\n')


def create_cli_file(directory_path):
    """
    Creates a `/{project_name}/cli.py` file.
    
    Parameters
    ----------
    directory_path : `str`
        Path to the file's directory.
    """
    create_file(
        directory_path,
        'cli.py',
        (
            f'__all__ = (\'main\',)\n'
            f'\n'
            f'def main():\n'
            f'    try:\n'
            f'        from {PACKAGE_NAME!s}.main import execute_command_from_system_parameters\n'
            f'    except ImportError as err:\n'
            f'        raise ImportError(\n'
            f'            \'Couldn\\\'t import {PACKAGE_NAME!s}. \'\n'
            f'            \'Are you sure it\\\'s installed and available on your PYTHONPATH environment variable? \'\n'
            f'            \'Did you forget to activate a virtual environment?\'\n'
            f'        ) from err\n'
            f'\n'
            f'    from {PACKAGE_NAME!s}.ext.plugin_auto_reloader import start_auto_reloader, warn_auto_reloader_availability\n'
            f'    from {PACKAGE_NAME!s}.ext.plugin_loader import load_all_plugin, frame_filter, register_plugin\n'
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
            f'        raise SystemExit(1) from None\n'
            f'\n'
            f'    warn_auto_reloader_availability()\n'
            f'    start_auto_reloader()\n'
            f'\n'
            f'    execute_command_from_system_parameters()\n'
        ),
    )


def build_constants_file_content(bot_names):
    """
    Builds the content of the `/{project_name}/constants.py` file.
    
    Parameters
    ----------
    bot_names : `list` of `str`
        The bots' names.
    
    Returns
    -------
    content : `str`
    """
    content_parts = []
    
    # Header
    content_parts.append('__all__ = ()\n\n')
    
    # Imports
    content_parts.append('from ')
    content_parts.append(PACKAGE_NAME)
    content_parts.append('.env import EnvGetter\n\n\n')
    
    # Content
    content_parts.append('with EnvGetter() as env:\n')
    for bot_name in bot_names:
        constant_name = get_bot_constant_name(bot_name)
        
        content_parts.append('    ')
        content_parts.append(constant_name)
        content_parts.append('_TOKEN = env.get_str(\'')
        content_parts.append(constant_name)
        content_parts.append('_TOKEN\', raise_if_missing_or_empty = True)\n')
    
    return ''.join(content_parts)


def create_constants_file(directory_path, bot_names):
    """
    Creates a new `/{project_name}/constants.py` file.
    
    Parameters
    ----------
    directory_path : `str`
        Path to the file's directory.
    bot_names : `list` of `str`
        The bots' names.
    """
    create_file(directory_path, 'constants.py', build_constants_file_content(bot_names))


def create_main_file(directory_path):
    """
    Creates a `/{project_name}/__main__.py` file.
    
    Parameters
    ----------
    directory_path : `str`
        Path to the file's directory.
    """
    create_file(
        directory_path,
        '__main__.py',
        (
            f'__all__ = ()\n'
            f'\n'
            f'from .cli import main\n'
            f'\n'
            f'if __name__ == \'__main__\':\n'
            f'    main()\n'
        ),
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
    create_file(directory_path, '__init__.py', build_bots_init_file_content(bot_names))


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
    
    create_file(
        directory_path,
        bot_module_name + '.py',
        (
            f'__all__ = (\'{bot_variable_name}\',)\n'
            f'\n'
            f'from {PACKAGE_NAME!s} import Client\n'
            f'\n'
            f'from ..constants import {bot_constant_name}_TOKEN\n'
            f'\n'
            f'\n'
            f'{bot_variable_name} = Client(\n'
            f'    {bot_constant_name}_TOKEN,\n'
            f'    extensions = [\'slash\'],\n'
            f')\n'
        ),
    )


def create_plugins_init_file(directory_path):
    """
    Creates a `/{project_name}/plugins/__init__.py` file.
    
    Parameters
    ----------
    directory_path : `str`
        Path to the file's directory.
    """
    create_file(
        directory_path,
        '__init__.py',
        (
            f'from {PACKAGE_NAME!s}.ext.plugin_loader import mark_as_plugin_root_directory\n'
            f'\n'
            f'mark_as_plugin_root_directory()\n'
        ),
    )


def create_plugins_ping_command_file(directory_path):
    """
    Creates a `/{project_name}/plugins/ping.py` file.
    
    Parameters
    ----------
    directory_path : `str`
        Path to the file's directory.
    """
    create_file(
        directory_path,
        'ping.py',
        (
            f'from time import perf_counter\n'
            f'\n'
            f'from {PACKAGE_NAME!s} import ClientWrapper\n'
            f'\n'
            f'\n'
            f'ALL = ClientWrapper()\n'
            f'\n'
            f'\n'
            f'@ALL.interactions(is_global = True, wait_for_acknowledgement = True)\n'
            f'async def ping():\n'
            f'    \"\"\"HTTP ping-pong.\"\"\"\n'
            f'    start = perf_counter()\n'
            f'    yield\n'
            f'    delay = (perf_counter() - start) * 1000.0\n'
            f'\n'
            f'    yield f\'{{delay:.0f}} ms\'\n'
        ),
    )


def create_project_structure(root_directory_path, project_name, bot_names):
    """
    Creates a project with package layout.
    
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
    create_constants_file(project_directory_path, bot_names)
    
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
    create_plugins_ping_command_file(plugins_directory_path)
