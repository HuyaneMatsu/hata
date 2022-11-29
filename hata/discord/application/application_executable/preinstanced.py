__all__ = ('OperationSystem',)

from ...bases import Preinstance as P, PreinstancedBase


class OperationSystem(PreinstancedBase):
    """
    Represents a ``ApplicationExecutable``'s operation system.
    
    Attributes
    ----------
    name : `str`
        The name of state.
    value : `int`
        The Discord side identifier value of the os.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``Os``) items
        Stores the created os instances. This container is accessed when translating a Discord
        os' value to it's representation.
    VALUE_TYPE : `type` = `int`
        The os' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the oss.
    
    Every predefined os can be accessed as class attribute as well:
    +-----------------------+-----------+---------------+
    | Class attribute name  | name      | value         |
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
    INSTANCES = {}
    VALUE_TYPE = str
    
    __slots__ = ()
    
    # predefined
    none = P('', 'none')
    darwin = P('darwin', 'darwin')
    linux = P('linux', 'linux')
    windows = P('win32', 'windows')
