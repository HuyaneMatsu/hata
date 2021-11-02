import sys
from os.path import dirname as get_directory_name, realpath as get_real_path, join as join_paths, \
    normpath as normalize_path, expanduser as get_user_home_directory
from os import getcwd as get_current_work_directory

try:
    from . import __package__ as PACKAGE_NAME
except ImportError:
    # If we have hata not setuped
    PACKAGE_NAME = sys.path[0]
    
    sys.path.append(
        normalize_path(
            join_paths(
                get_directory_name(
                    get_real_path(
                        join_paths(
                            get_current_work_directory(),
                            get_user_home_directory(__file__),
                        )
                    )
                ),
                '..',
            )
        )
    )


PACKAGE = __import__(PACKAGE_NAME)

SYSTEM_DEFAULT_PARAMETER = 'i'

COMMAND_NAMES = tuple(sorted((
    'help',
    'interpreter',
    'version',
)))

COMMAND_MAP = {
    'h': 'help',
    'help': 'help',
    
    'i': 'interpreter',
    'interpreter': 'interpreter',
    
    'v': 'version',
    'version': 'version',
}

assert SYSTEM_DEFAULT_PARAMETER in COMMAND_MAP


def command_not_found():
    from hata.backend.utils import get_short_executable
    
    output_parts = ['No command is added for: ']
    
    system_parameter = sys.argv
    
    index = 1
    length = len(system_parameter)
    
    while True:
        output_parts.append(repr(system_parameter[index]))
        index += 1
        if index == length:
            break
        
        output_parts.append(', ')
        continue
    
    output_parts.append('\n')
    output_parts.append('Try using "$')
    output_parts.append(get_short_executable())
    output_parts.append(' ')
    output_parts.append(PACKAGE_NAME)
    output_parts.append(' help" for more information\n.')
    
    output = ''.join(output_parts)
    
    sys.stderr.write(output)


def __main__():
    system_parameters = sys.argv
    if len(system_parameters) < 2:
        system_parameter = SYSTEM_DEFAULT_PARAMETER
    else:
        system_parameter = system_parameters[1].lower()
    
    try:
        command_name = COMMAND_MAP[system_parameter]
    except KeyError:
        return command_not_found
    
    __import__(f'{PACKAGE_NAME}.main.{command_name}')
    return getattr(PACKAGE.main, command_name).__main__


if __name__ == '__main__':
    # Do tail call.
    __main__()()
