from .helpers import *
from .naming import *
from .scaffold import *


__all__ = (
    *helpers.__all__,
    *naming.__all__,
    *scaffold.__all__,
)


import sys
from os.path import join as join_paths

from ....core import register

from .helpers import _validate_bot, _validate_project_name, _validate_name
from .naming import get_project_module_name
from .scaffold import create_project_structure


@register
def scaffold(
    name: str,
    *bot: str,
    project_name : str = None,
):
    """
    Scaffolds a new project.
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
    
    project_module_name = get_project_module_name(project_name)
    
    create_project_structure(directory_path, project_module_name, bot_names)
    sys.stdout.write(
        f'Project {project_module_name} created.\n'
        f'Please check {join_paths(directory_path, "README.md")} about whats next.\n'
    )
