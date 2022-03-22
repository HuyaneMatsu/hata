__all__ = ()

from ... import Command

from scarletio.tools.asynchronous_interactive_console import AWAIT_NOTE

Command(
    'default',
    'help',
    'help',
    frozenset(('h', 'help')),
    'h | help *command*',
    f'Either lists the available command, or shows the command\'s usage.\n',
)

Command(
    'default',
    'interpreter',
    'interpreter',
    frozenset(('i', 'interpreter')),
    'i | interpreter',
    f'Runs asynchronous python interpreter through scarletio.\n{AWAIT_NOTE}\n',
)

Command(
    'default',
    'version',
    'version',
    frozenset(('v', 'version')),
    'v | version',
    f'Prints out hata\'s version.\n'
)
