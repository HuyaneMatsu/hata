from .helpers import *
from .naming import *
from .scaffold import *


__all__ = (
    *helpers.__all__,
    *naming.__all__,
    *scaffold.__all__,
)


import sys

from ....core import register

from .helpers import _validate_bot, _validate_name
from .scaffold import create_project_structure


@register
def scaffold(
    name: str,
    *bot: str,
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
    
    create_project_structure(directory_path, bot_names)
    sys.stdout.write('Project created.\n')
