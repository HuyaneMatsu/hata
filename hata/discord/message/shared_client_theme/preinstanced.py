__all__ = ('SharedClientThemeBaseTheme',)

from ...bases import Preinstance as P, PreinstancedBase


class SharedClientThemeBaseTheme(PreinstancedBase, value_type = int):
    """
    Represents an shared theme's base type.
    
    Attributes
    ----------
    name : `str`
        The name of the type.
    
    value : `int`
        The Discord side identifier value of the type.
        
    Type Attributes
    ---------------
    Every predefined shared theme base type can be accessed as type attribute as well:
    
    +-----------------------+---------------+-------+
    | Type attribute name   | name          | Value |
    +=======================+===============+=======+
    | none                  | none          | 0     |
    +-----------------------+---------------+-------+
    | dark                  | dark          | 1     |
    +-----------------------+---------------+-------+
    | light                 | light         | 2     |
    +-----------------------+---------------+-------+
    | darker                | darker        | 3     |
    +-----------------------+---------------+-------+
    | midnight              | midnight      | 4     |
    +-----------------------+---------------+-------+
    """
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    dark = P(1, 'dark')
    light = P(2, 'light')
    darker = P(3, 'darker')
    midnight = P(4, 'midnight')
