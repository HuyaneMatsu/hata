__all__ = ()

from ... import Command

from scarletio.tools.asynchronous_interactive_console import AWAIT_NOTE

Command(
    'default',
    'help',
    'help',
    ['h'],
    'h | help *command*',
    'Either lists the available command, or shows the command\'s usage.',
)

Command(
    'default',
    'interpreter',
    'interpreter',
    ['i'],
    'i | interpreter',
    f'Runs asynchronous python interpreter through scarletio.\n{AWAIT_NOTE}',
)

Command(
    'default',
    'version',
    'version',
    ['v'],
    'v | version',
    'Prints out hata\'s version.'
)
