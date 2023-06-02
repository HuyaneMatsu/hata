__all__ = ()

from scarletio import get_short_executable

from ....... import __package__ as PACKAGE_NAME

from ......core.helpers import render_main_call_into

from ...naming import get_bot_display_name, get_bot_module_name, get_bot_variable_name


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


def build_readme_content(project_name, bot_names):
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
