import sys
from platform import platform as get_platform
from .. import __package__ as PACKAGE_NAME, __version__ as VERSION

NAME = 'version'
USAGE = 'v | version'

HELP = (
    f'Prints out hata\'s version.\n'
)

def __main__():
    output_parts = []
    
    output_parts.append(PACKAGE_NAME[0].upper())
    output_parts.append(PACKAGE_NAME[1:])
    output_parts.append(' version: ')
    output_parts.append(VERSION)
    output_parts.append('\n')
    
    output_parts.append('Platform: ')
    output_parts.append(get_platform())
    output_parts.append('\n')
    
    implementation = sys.implementation
    
    output_parts.append('Python implementation: ')
    output_parts.append(implementation.name)
    output_parts.append('\n')
    
    version = implementation.version
    
    output_parts.append('Python version: ')
    output_parts.append(str(version[0]))
    output_parts.append('.')
    output_parts.append(str(version[1]))
    
    if version[3] == 'final':
        output_parts.append(' final')
    
    output_parts.append('\n')
    
    output = ''.join(output_parts)
    
    sys.stdout.write(output)
