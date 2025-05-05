__all__ = ('ButtonStyle', 'SeparatorSpacingSize', 'TextInputStyle')

from ...bases import Preinstance as P, PreinstancedBase


class ButtonStyle(PreinstancedBase, value_type = int):
    """
    Represents a button component's style.
    
    Attributes
    ----------
    name : `str`
        The name of the button style.
    
    value : `int`
        The identifier value the button style.
    
    Type Attributes
    ---------------
    Every predefined button style can be accessed as type attribute as well:
    
    +-----------------------+---------------+-------+
    | Type attribute name   | Name          | Value |
    +=======================+===============+=======+
    | none                  | none          | 0     |
    +-----------------------+---------------+-------+
    | blue                  | blue          | 1     |
    +-----------------------+---------------+-------+
    | gray                  | gray          | 2     |
    +-----------------------+---------------+-------+
    | green                 | green         | 3     |
    +-----------------------+---------------+-------+
    | red                   | red           | 4     |
    +-----------------------+---------------+-------+
    | link                  | link          | 5     |
    +-----------------------+---------------+-------+
    | subscription          | subscription  | 6     |
    +-----------------------+---------------+-------+
    """
    __slots__ = ()
    
    none = P(0, 'none')
    blue = P(1, 'blue')
    gray = P(2, 'gray')
    green = P(3, 'green')
    red = P(4, 'red')
    link = P(5, 'link')
    subscription = P(6, 'subscription')


class TextInputStyle(PreinstancedBase, value_type = int):
    """
    Represents a text input component's style.
    
    Attributes
    ----------
    name : `str`
        The name of the text input style.
    
    value : `int`
        The identifier value the text input style.
    
    Type Attributes
    ---------------
    Every predefined text input style can be accessed as type attribute as well:
    
    +-----------------------+---------------+-------+
    | Type attribute name   | Name          | Value |
    +=======================+===============+=======+
    | none                  | none          | 0     |
    +-----------------------+---------------+-------+
    | short                 | short         | 1     |
    +-----------------------+---------------+-------+
    | paragraph             | paragraph     | 2     |
    +-----------------------+---------------+-------+
    """
    __slots__ = ()
    
    none = P(0, 'none')
    short = P(1, 'short')
    paragraph = P(2, 'paragraph')


class SeparatorSpacingSize(PreinstancedBase, value_type = int):
    """
    Represents a separator component's spacing's size.
    
    Attributes
    ----------
    name : `str`
        The name of the separator spacing's size.
    
    value : `int`
        The identifier value the separator spacing's size.
    
    Type Attributes
    ---------------
    Every predefined separator spacing's size can be accessed as type attribute as well:
    
    +-----------------------+---------------+-------+
    | Type attribute name   | Name          | Value |
    +=======================+===============+=======+
    | none                  | none          | 0     |
    +-----------------------+---------------+-------+
    | small                 | small         | 1     |
    +-----------------------+---------------+-------+
    | large                 | large         | 2     |
    +-----------------------+---------------+-------+
    """
    __slots__ = ()
    
    none = P(0, 'none')
    small = P(1, 'small')
    large = P(2, 'large')
