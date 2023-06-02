__all__ = ()

import sys
from os.path import join as join_paths

from ....core import register

from .helpers import _validate_bot, _validate_layout, _validate_project_name, _validate_name
from .layouts import DEFAULT_LAYOUT, LAYOUT_DESCRIPTIONS, get_project_structure_builder
from .naming import get_project_module_name


def _build_scaffold_description():
    """
    Builds description of the `scaffold` command.
    
    Returns
    -------
    description : `str`
    """
    description_parts = []
    
    description_parts.append(
        'Scaffold can be used to automatically create a basic structure for your application.\n'
        'This includes code, configuration files, and other necessary files and assets.\n'
        '\n'
        'Available layouts:'
    )
    for index, (layout_name, layout_description) in enumerate(sorted(LAYOUT_DESCRIPTIONS.items()), 1):
        description_parts.append('\n\n')
        index_representation = str(index)
        description_parts.append(index_representation)
        description_parts.append('.: ')
        description_parts.append(layout_name.upper())
        
        underscore_length = len(index_representation) + 4 + len(layout_name)
        if layout_name == DEFAULT_LAYOUT:
            description_parts.append(' (default)')
            underscore_length += 10
        
        description_parts.append(':\n')
        description_parts.append('-' * underscore_length)
        description_parts.append('\n')
        
        description_parts.append(layout_description)
    
    description_parts.append('\n')
    return ''.join(description_parts)


@register(description = _build_scaffold_description())
def scaffold(
    name : str,
    *bot : str,
    project_name : str = None,
    layout : str = None,
):
    """
    Scaffolds a project.
    """
    directory_path, error_message = _validate_name(name)
    if error_message is not None:
        sys.stdout.write(error_message)
        return
    
    bot_names, error_message = _validate_bot(bot)
    if error_message is not None:
        sys.stdout.write(error_message)
        return
    
    project_name, error_message = _validate_project_name(project_name, name)
    if error_message is not None:
        sys.stdout.write(error_message)
        return
    
    layout, error_message = _validate_layout(layout)
    if error_message is not None:
        sys.stdout.write(error_message)
        return
    
    project_module_name = get_project_module_name(project_name)
    create_project_structure = get_project_structure_builder(layout)
    create_project_structure(directory_path, project_module_name, bot_names)
    sys.stdout.write(
        f'Project {project_module_name} created.\n'
        f'Note that scaffold command is experimental and will change in future updates.\n'
        f'Please check {join_paths(directory_path, "README.md")} about whats next.\n'
    )
