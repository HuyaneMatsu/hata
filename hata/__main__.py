import sys
from os import getcwd as get_current_work_directory
from os.path import (
    dirname as get_directory_name, expanduser as get_user_home_directory, join as join_paths,
    normpath as normalize_path, realpath as get_real_path
)


try:
    from . import __package__ as PACKAGE_NAME
except ImportError:
    # If we have hata not setupped
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

MAIN = __import__(f'{PACKAGE_NAME}.main').main

COMMAND_NAME_TO_COMMAND = MAIN.COMMAND_NAME_TO_COMMAND
find_commands = MAIN.find_commands

find_commands()

SYSTEM_DEFAULT_PARAMETER = 'i'

def command_not_found():
    from scarletio import get_short_executable
    
    output_parts = ['No command is added for: ']
    
    system_parameter = sys.argv
    
    length = len(system_parameter)
    if length > 2:
        index = 1
        
        while True:
            output_parts.append(repr(system_parameter[index]))
            index += 1
            if index == length:
                break
            
            output_parts.append(', ')
            continue
    else:
        output_parts.append('-')
    
    output_parts.append('\n')
    output_parts.append('Try using "$ ')
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
        command = COMMAND_NAME_TO_COMMAND[system_parameter]
    except KeyError:
        command_function = command_not_found
    
    else:
        command_function = command.get_command_function()
    
    return command_function()


if __name__ == '__main__':
    __main__()
