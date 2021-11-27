__all__ = ('FormSubmitCommand', )

try:
    # CPython
    from re import Pattern
except ImportError:
    # ChadPython (PyPy)
    from re import _pattern_type as Pattern

from functools import partial as partial_func

from ...discord.events.handling_helpers import route_value, Router, create_event_from_class, check_name, route_name

from .wrappers import SlasherCommandWrapper
from .utils import _check_maybe_route
from .converters import get_component_command_parameter_converters
from .responding import process_command_coroutine
from .exceptions import handle_command_exception, test_exception_handler, _register_exception_handler
from .custom_id_based_command import _validate_name, _validate_custom_ids, split_and_check_satisfaction, \
    CustomIdBasedCommand

COMPONENT_COMMAND_PARAMETER_NAMES = ('command', 'custom_id', 'name')

COMPONENT_COMMAND_NAME_NAME = 'name'
COMPONENT_COMMAND_COMMAND_NAME = 'command'


class FormSubmitCommand(CustomIdBasedCommand):
    pass
