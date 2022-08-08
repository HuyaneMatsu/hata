__all__ = ()

from scarletio.tools.asynchronous_interactive_console import (
    collect_package_local_variables, create_banner, create_exit_message, run_asynchronous_interactive_console
)
from scarletio.tools.asynchronous_interactive_console.console_helpers import AWAIT_NOTE

from .... import __package__ as PACKAGE_NAME

from ... import register


PACKAGE = __import__(PACKAGE_NAME)


@register(
    alters = 'i',
    description =  f'Runs asynchronous python interpreter through scarletio.\n{AWAIT_NOTE}',
)
def interpreter():
    run_asynchronous_interactive_console(
        collect_package_local_variables(PACKAGE),
        banner = create_banner(PACKAGE),
        exit_message = create_exit_message(PACKAGE),
    )
