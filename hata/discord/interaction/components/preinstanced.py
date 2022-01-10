__all__ = ('ButtonStyle', 'ComponentType', 'TextInputStyle')

from scarletio import export

from ...bases import Preinstance as P, PreinstancedBase


@export
class ComponentType(PreinstancedBase):
    """
    Represents a component's type.
    
    Attributes
    ----------
    name : `str`
        The name of the component type.
    value : `int`
        The identifier value the component type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``ComponentType``) items
        Stores the predefined ``ComponentType``-s. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The component type's type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the component types.
    
    Every predefined component type can be accessed as class attribute as well:
    
    +-----------------------+---------------+-------+
    | Class attribute name  | Name          | Value |
    +=======================+===============+=======+
    | none                  | none          | 0     |
    +-----------------------+---------------+-------+
    | row                   | row           | 1     |
    +-----------------------+---------------+-------+
    | button                | button        | 2     |
    +-----------------------+---------------+-------+
    | select                | select        | 3     |
    +-----------------------+---------------+-------+
    | text_input            | text input    | 4     |
    +-----------------------+---------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    none = P(0, 'none')
    row = P(1, 'row')
    button = P(2, 'button')
    select = P(3, 'select')
    text_input = P(4, 'text input')
    

class ButtonStyle(PreinstancedBase):
    """
    Represents a button component's style.
    
    Attributes
    ----------
    name : `str`
        The name of the button style.
    value : `int`
        The identifier value the button style
    
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
    | violet                | violet        | 1     |
    +-----------------------+---------------+-------+
    | gray                  | gray          | 2     |
    +-----------------------+---------------+-------+
    | green                 | green         | 3     |
    +-----------------------+---------------+-------+
    | red                   | red           | 4     |
    +-----------------------+---------------+-------+
    | link                  | link          | 5     |
    +-----------------------+---------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    none = P(0, 'none')
    violet = P(1, 'violet')
    gray = P(2, 'gray')
    green = P(3, 'green')
    red = P(4, 'red')
    link = P(5, 'link')


class TextInputStyle(PreinstancedBase):
    """
    Represents a text input component's type.
    
    Attributes
    ----------
    name : `str`
        The name of the text input style.
    value : `int`
        The identifier value the text input style
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``ButtonStyle``) items
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
    | short                 | short         | 1     |
    +-----------------------+---------------+-------+
    | paragraph             | paragraph     | 2     |
    +-----------------------+---------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    none = P(0, 'none')
    short = P(1, 'short')
    paragraph = P(2, 'paragraph')
