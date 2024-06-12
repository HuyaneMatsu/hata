__all__ = ('ButtonStyle', 'SeparatorSpacingSize', 'TextInputStyle')

from ...bases import Preinstance as P, PreinstancedBase


class ButtonStyle(PreinstancedBase):
    """
    Represents a button component's style.
    
    Attributes
    ----------
    name : `str`
        The name of the button style.
    value : `int`
        The identifier value the button style.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``ButtonStyle``) items
        Stores the predefined ``ButtonStyle``-s. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The button style's type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the button styles.
    
    Every predefined button style can be accessed as class attribute as well:
    
    +-----------------------+---------------+-------+
    | Class attribute name  | Name          | Value |
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
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    none = P(0, 'none')
    blue = P(1, 'blue')
    gray = P(2, 'gray')
    green = P(3, 'green')
    red = P(4, 'red')
    link = P(5, 'link')
    subscription = P(6, 'subscription')


class TextInputStyle(PreinstancedBase):
    """
    Represents a text input component's style.
    
    Attributes
    ----------
    name : `str`
        The name of the text input style.
    value : `int`
        The identifier value the text input style.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``TextInputStyle``) items
        Stores the predefined ``TextInputStyle``-s. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The text input style's type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the text input styles.
    
    Every predefined text input style can be accessed as class attribute as well:
    
    +-----------------------+---------------+-------+
    | Class attribute name  | Name          | Value |
    +=======================+===============+=======+
    | none                  | none          | 0     |
    +-----------------------+---------------+-------+
    | small                 | small         | 1     |
    +-----------------------+---------------+-------+
    | large                 | large         | 2     |
    +-----------------------+---------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    none = P(0, 'none')
    short = P(1, 'short')
    paragraph = P(2, 'paragraph')


class SeparatorSpacingSize(PreinstancedBase):
    """
    Represents a separator component's spacing's size.
    
    Attributes
    ----------
    name : `str`
        The name of the separator spacing's size.
    value : `int`
        The identifier value the separator spacing's size.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``SeparatorSpacingSize``) items
        Stores the predefined ``SeparatorSpacingSize``-s. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The separator spacing's size's type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the separator spacing's sizes.
    
    Every predefined separator spacing's size can be accessed as class attribute as well:
    
    +-----------------------+---------------+-------+
    | Class attribute name  | Name          | Value |
    +=======================+===============+=======+
    | none                  | none          | 0     |
    +-----------------------+---------------+-------+
    | small                 | small         | 1     |
    +-----------------------+---------------+-------+
    | large                 | large         | 2     |
    +-----------------------+---------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    none = P(0, 'none')
    small = P(1, 'small')
    large = P(2, 'large')
