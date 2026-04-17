__all__ = ('set_debug_logger', )

import sys

from .. import __package__ as PACKAGE_NAME


UNIQUE_MESSAGES = set()


def call_debug_logger(message, unique):
    """
    Calls debug logger if applicable.
    
    Parameters
    ----------
    message : `str`
        The message to show.
    unique : `bool`
        Whether the message should not be shown if already was.
    """
    if unique:
        if message in UNIQUE_MESSAGES:
            return
        
        UNIQUE_MESSAGES.add(message)
    
    _debug_logger(message)


def set_debug_logger(debug_logger):
    """
    Sets the given function as debug handler.
    
    Parameters
    ----------
    debug_logger : `callable`
        Any callable accepting 1 string parameter.
    """
    global _debug_logger
    _debug_logger = debug_logger


def default_debug_logger(message):
    """
    Default debug logger.
    
    Puts `DEBUG` prefix before each logged line and writes it to stdout.
    
    To set a new debug logger use ``set_debug_logger``.
    
    Parameters
    ----------
    message : `str`
        The message to show.
    """
    lines = message.splitlines()
    output_parts = []
    for line in lines:
        output_parts.append(PACKAGE_NAME)
        output_parts.append(' DEBUG: ')
        output_parts.append(line)
        output_parts.append('\n')
    
    output = ''.join(output_parts)
    
    sys.stdout.write(output)


_debug_logger = default_debug_logger
