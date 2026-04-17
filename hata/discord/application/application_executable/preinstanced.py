__all__ = ('OperationSystem',)

from ...bases import Preinstance as P, PreinstancedBase


class OperationSystem(PreinstancedBase, value_type = str):
    """
    Represents a ``ApplicationExecutable``'s operation system.
    
    Attributes
    ----------
    name : `str`
        The name of the operation system.
    
    value : `str`
        The Discord side identifier value of the os.
    
    Type Attributes
    ---------------
    Every predefined os can be accessed as type attribute as well:
    +-----------------------+---------------+-------------------+
    | Type attribute name   | name          | value             |
    +=======================+===============+===================+
    | none                  | none          | `''`              |
    +-----------------------+---------------+-------------------+
    | android               | android       | `'android'`       |
    +-----------------------+---------------+-------------------+
    | darwin                | darwin        | '`darwin'`        |
    +-----------------------+---------------+-------------------+
    | ios                   | ios           | `'ios'`           |
    +-----------------------+---------------+-------------------+
    | linux                 | linux         | '`linux`'         |
    +-----------------------+---------------+-------------------+
    | playstation           | playstation   | `'playstation'`   |
    +-----------------------+---------------+-------------------+
    | windows               | windows       | `'win32'`         |
    +-----------------------+---------------+-------------------+
    | xbox                  | xbox          | `'xbox'`          |
    +-----------------------+---------------+-------------------+
    """
    __slots__ = ()
    
    # predefined
    none = P('', 'none')
    android = P('android', 'android')
    darwin = P('darwin', 'darwin')
    ios = P('ios', 'ios')
    linux = P('linux', 'linux')
    playstation = P('playstation', 'playstation')
    windows = P('win32', 'windows')
    xbox = P('xbox', 'xbox')
