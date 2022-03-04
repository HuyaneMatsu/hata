from scarletio.tools.asynchronous_interactive_console import (
    AWAIT_NOTE, collect_package_local_variables, create_banner, create_exit_message,
    run_asynchronous_interactive_console
)

from .. import __package__ as PACKAGE_NAME


PACKAGE = __import__(PACKAGE_NAME)

NAME = 'interpreter'
USAGE = 'i | interpreter'

HELP = f'Runs asynchronous python interpreter through scarletio.\n{AWAIT_NOTE}\n'


def __main__():
    run_asynchronous_interactive_console(
        collect_package_local_variables(PACKAGE),
        banner = create_banner(PACKAGE),
        exit_message = create_exit_message(PACKAGE),
    )
