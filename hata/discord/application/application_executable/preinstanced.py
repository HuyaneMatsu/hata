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
    +-----------------------+-----------+---------------+
    | Type attribute name   | name      | value         |
    +=======================+===========+===============+
    | none                  | none      | `''`          |
    +-----------------------+-----------+---------------+
    | darwin                | darwin    | '`darwin'`    |
    +-----------------------+-----------+---------------+
    | linux                 | linux     | '`linux`'     |
    +-----------------------+-----------+---------------+
    | windows               | windows   | `'win32'`     |
    +-----------------------+-----------+---------------+
    """
    __slots__ = ()
    
    # predefined
    none = P('', 'none')
    darwin = P('darwin', 'darwin')
    linux = P('linux', 'linux')
    windows = P('win32', 'windows')
