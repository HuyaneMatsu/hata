import sys
from . import __package__ as PACKAGE_NAME

PACKAGE = __import__(PACKAGE_NAME)

SYSTEM_DEFAULT_PARAMETER = 'i'

SCRIPT_NAMES = {
    'i': 'interpreter',
    'interpreter': 'interpreter',
    
    'v': 'version',
    'version': 'version',
}

assert SYSTEM_DEFAULT_PARAMETER in SCRIPT_NAMES


def no_script_found():
    output_parts = ['No main function is added for: ']
    
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
    
    output = ''.join(output_parts)
    
    sys.stderr.write(output)


def __main__():
    system_parameters = sys.argv
    if len(system_parameters) < 2:
        system_parameter = SYSTEM_DEFAULT_PARAMETER
    else:
        system_parameter = system_parameters[1]
    
    try:
        script_name = SCRIPT_NAMES[system_parameter]
    except KeyError:
        return no_script_found
    
    __import__(f'{PACKAGE_NAME}.main.{script_name}')
    return getattr(PACKAGE.main, script_name).__main__


if __name__ == '__main__':
    # Do tail call.
    __main__()()
