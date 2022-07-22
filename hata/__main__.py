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

__main__ = MAIN.execute_command_from_system_parameters
MAIN.maybe_find_commands()


if __name__ == '__main__':
    __main__()
