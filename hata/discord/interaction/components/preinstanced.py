__all__ = ('ButtonStyle', 'ComponentType', 'TextInputStyle')

import warnings

from scarletio import class_property, export

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
    
    +-----------------------+-----------------------+-------+
    | Class attribute name  | Name                  | Value |
    +=======================+=======================+=======+
    | none                  | none                  | 0     |
    +-----------------------+-----------------------+-------+
    | row                   | row                   | 1     |
    +-----------------------+-----------------------+-------+
    | button                | button                | 2     |
    +-----------------------+-----------------------+-------+
    | select                | string select         | 3     |
    +-----------------------+-----------------------+-------+
    | text_input            | text input            | 4     |
    +-----------------------+-----------------------+-------+
    | user_select           | user select           | 5     |
    +-----------------------+-----------------------+-------+
    | role_select           | role select           | 6     |
    +-----------------------+-----------------------+-------+
    | mentionable_select    | mentionable select    | 7     |
    +-----------------------+-----------------------+-------+
    | channel_select        | channel select        | 8     |
    +-----------------------+-----------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    none = P(0, 'none')
    row = P(1, 'row')
    button = P(2, 'button')
    select = P(3, 'string select')
    text_input = P(4, 'text input')
    user_select = P(5, 'user select')
    role_select = P(6, 'role select')
    mentionable_select = P(7, 'mentionable select')
    channel_select = P(8, 'mentionable select')
    

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
    
    
    @class_property
    def violet(cls):
        """
        `.violet` is deprecated and will be removed in 2022 Aug. Please use `.blue` instead.
        """
        warnings.warn(
            (
                f'`{cls.__name__}.violet` is deprecated and will be removed in 2022 Aug. '
                f'Please use `.blue` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        return cls.blue


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
