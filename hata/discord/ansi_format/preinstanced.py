__all__ = ('AnsiBackgroundColor', 'AnsiForegroundColor', 'AnsiTextDecoration', )

from ..bases import Preinstance as P, PreinstancedBase
from ..color import Color


class AnsiTextDecoration(PreinstancedBase, value_type = int):
    """
    Represents an ansi text decoration.
    
    Attributes
    ----------
    name : `str`
        The name of the text decoration.
    
    value : `int`
        The unique identifier of the text decoration.
    
    Type Attributes
    ---------------
    Each text decoration is stored as a type attribute:
    
    +-----------------------+-----------+-----------------------+
    | Class Attribute name  | value     | name                  |
    +=======================+===========+=======================+
    | none                  | 0         | none                  |
    +-----------------------+-----------+-----------------------+
    | bold                  | 1         | bold                  |
    +-----------------------+-----------+-----------------------+
    | underline             | 4         | underline             |
    +-----------------------+-----------+-----------------------+
    """
    __slots__ = ()
    
    none = P(0, 'none')
    bold = P(1, 'bold')
    underline = P(4, 'underline')


class AnsiFormatColor(PreinstancedBase, base_type = True, value_type = int):
    """
    Represents an ansi color format code.
    
    Attributes
    ----------
    color : ``Color``
        The real color value.
    
    color_name : `str`
        A more accurate name of the color.
    
    name : `str`
        The default name of the format color.
    
    value : `int`
        The unique identifier of the format color.
    """
    __slots__ = ('color', 'color_name')
    
    def __new__(cls, value, name = None, color = ..., color_name = None):
        """
        Creates a new format color.
        
        Parameters
        ----------
        value : `str`
            The unique identifier of the format color.
        
        name : `None | str` = `None`, Optional
            The format color's name.
        
        color : ``Color``, Optional
            The real color value.
        
        color_name : `None | str` = `None`, Optional
            The color's name.
        """
        if color is ...:
            color = Color()
        
        if name is None:
            name = cls.NAME_DEFAULT
        
        if color_name is None:
            color_name = name
        
        self = PreinstancedBase.__new__(cls, value, name)
        self.color = color
        self.color_name = color_name
        return self


class AnsiBackgroundColor(AnsiFormatColor):
    """
    Represents an ansi background color code.
    
    Attributes
    ----------
    color : ``Color``
        The real color value.
    
    color_name : `str`
        A more accurate name of the color.
    
    name : `str`
        The default name of the format color.
    
    value : `int`
        The unique identifier of the format color.
    
    Type Attributes
    ---------------
    Each background color is stored as a type attribute:
    
    +-----------------------+-----------+-----------------------+-----------+-------------------+-------------------------------+
    | Class Attribute name  | value     | name                  | color     | color name        | Additional notes              |
    +=======================+===========+=======================+===========+===================+===============================+
    | black                 | 40        | black                 | 002b36    | daintree          | Dark cyan, almost black.      |
    +-----------------------+-----------+-----------------------+-----------+-------------------+-------------------------------+
    | red                   | 41        | red                   | 0xcb4b16  | orange roughy     | Bright ~ brick red.           |
    +-----------------------+-----------+-----------------------+-----------+-------------------+-------------------------------+
    | marble_blue_cyan      | 42        | marble blue cyan      | 0x586e75  | cutty sark        | Looks gray to me.             |
    +-----------------------+-----------+-----------------------+-----------+-------------------+-------------------------------+
    | marble_blue           | 43        | marble blue           | 0x657b83  | pale sky          | Looks gray to me.             |
    +-----------------------+-----------+-----------------------+-----------+-------------------+-------------------------------+
    | gray                  | 44        | gray                  | 0x657b83  | oslo gray         | Looks gray to me.             |
    +-----------------------+-----------+-----------------------+-----------+-------------------+-------------------------------+
    | blue                  | 45        | blue                  | 0x6c71c4  | blue marguerite   | Blue-violet                   |
    +-----------------------+-----------+-----------------------+-----------+-------------------+-------------------------------+
    | silver                | 46        | silver                | 0x93a1a1  | pewter            | Looks gray to me.             |
    +-----------------------+-----------+-----------------------+-----------+-------------------+-------------------------------+
    | white                 | 47        | old lace              | 0xfdf6e3  | old lace          | Pale yellow-orange.           |
    +-----------------------+-----------+-----------------------+-----------+-------------------+-------------------------------+
    """
    __slots__ = ()
    
    INSTANCES = {}
    
    black = P(40, 'black', Color(0x002b36), 'daintree')
    red = P(41, 'red', Color(0xcb4b16), 'orange roughy')
    marble_blue_cyan = P(42, 'marble blue cyan', Color(0x586e75), 'cutty sark')
    marble_blue = P(43, 'marble blue', Color(0x657b83), 'pale sky')
    gray = P(44, 'gray', Color(0x839496), 'oslo gray')
    blue = P(45, 'blue', Color(0x6c71c4), 'blue marguerite')
    silver = P(46, 'silver', Color(0x93a1a1), 'pewter')
    white = P(47, 'white', Color(0xfdf6e3), 'old lace')


class AnsiForegroundColor(AnsiFormatColor):
    """
    Represents an ansi foreground color code.
    
    Attributes
    ----------
    color : ``Color``
        The real color value.
    
    color_name : `str`
        A more accurate name of the color.
    
    name : `str`
        The default name of the format color.
    
    value : `int`
        The unique identifier of the format color.
    
    Type Attributes
    ---------------
    Each foreground color is stored as a type attribute:
    
    +-----------------------+-----------+-----------------------+-----------+-------------------+-------------------------------+
    | Class Attribute name  | value     | name                  | color     | color name        | Additional notes              |
    +=======================+===========+=======================+===========+===================+===============================+
    | black                 | 30        | black                 | 0x073642  | tiber             | Dark cyan, almost black.      |
    +-----------------------+-----------+-----------------------+-----------+-------------------+-------------------------------+
    | red                   | 31        | red                   | 0xdc322f  | punch             | Red.                          |
    +-----------------------+-----------+-----------------------+-----------+-------------------+-------------------------------+
    | green                 | 32        | green                 | 0x859900  | limeade           | Darker lime shade.            |
    +-----------------------+-----------+-----------------------+-----------+-------------------+-------------------------------+
    | orange                | 33        | orange                | 0xb58900  | pirate gold       | Warm orange.                  |
    +-----------------------+-----------+-----------------------+-----------+-------------------+-------------------------------+
    | blue                  | 34        | blue                  | 0x268bd2  | curious blue      | Blue.                         |
    +-----------------------+-----------+-----------------------+-----------+-------------------+-------------------------------+
    | pink                  | 35        | pink                  | 0xd33682  | cerise            | Red-pink.                     |
    +-----------------------+-----------+-----------------------+-----------+-------------------+-------------------------------+
    | teal                  | 36        | teal                  | 0x2aa198  | jungle green      | Teal (greenish blue).         |
    +-----------------------+-----------+-----------------------+-----------+-------------------+-------------------------------+
    | white                 | 37        | white                 | 0xffffff  | white             | Black on bright theme.        |
    +-----------------------+-----------+-----------------------+-----------+-------------------+-------------------------------+
    """
    __slots__ = ()
    
    INSTANCES = {}
    
    black = P(30, 'black', Color(0x073642), 'tiber')
    red = P(31, 'red', Color(0xdc322f), 'punch')
    green = P(32, 'green', Color(0x859900), 'limeade')
    orange = P(33, 'orange', Color(0xb58900), 'pirate gold')
    blue = P(34, 'blue', Color(0x268bd2), 'curious blue')
    pink = P(35, 'pink', Color(0xd33682), 'cerise')
    teal = P(36, 'teal', Color(0x2aa198), 'jungle green')
    white = P(37, 'white', Color(0xffffff), 'white')
