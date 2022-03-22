from scarletio.tools.asynchronous_interactive_console import (
    collect_package_local_variables, create_banner, create_exit_message, run_asynchronous_interactive_console
)

from .... import __package__ as PACKAGE_NAME


PACKAGE = __import__(PACKAGE_NAME)

def __main__():
    run_asynchronous_interactive_console(
        collect_package_local_variables(PACKAGE),
        banner = create_banner(PACKAGE),
        exit_message = create_exit_message(PACKAGE),
    )
