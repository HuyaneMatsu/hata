__all__ = ('ApplicationCommandOptionType', 'ApplicationCommandPermissionOverwriteType', 'ButtonStyle',
    'ComponentType', 'InteractionType', )

import warnings

from ...backend.export import export

from ..bases import PreinstancedBase, Preinstance as P


class ApplicationCommandOptionType(PreinstancedBase):
    """
    Represents an application command options' type.
    
    Attributes
    ----------
    name : `str`
        The name of the application command option type.
    value : `int`
        The identifier value the application command option type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``ApplicationCommandOptionType``) items
        Stores the predefined ``ApplicationCommandOptionType`` instances. These can be accessed with their `value` as
        key.
    VALUE_TYPE : `type` = `int`
        The application command option types' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the application command option types.
    
    Every predefined application command option type. can be accessed as class attribute as well:
    
    +-----------------------+-------------------+-------+
    | Class attribute name  | Name              | Value |
    +=======================+===================+=======+
    | none                  | none              | 0     |
    +-----------------------+-------------------+-------+
    | sub_command           | sub_command       | 1     |
    +-----------------------+-------------------+-------+
    | sub_command_group     | sub_command_group | 2     |
    +-----------------------+-------------------+-------+
    | string                | string            | 3     |
    +-----------------------+-------------------+-------+
    | integer               | integer           | 4     |
    +-----------------------+-------------------+-------+
    | boolean               | boolean           | 5     |
    +-----------------------+-------------------+-------+
    | user                  | user              | 6     |
    +-----------------------+-------------------+-------+
    | channel               | channel           | 7     |
    +-----------------------+-------------------+-------+
    | role                  | role              | 8     |
    +-----------------------+-------------------+-------+
    | mentionable           | mentionable       | 9     |
    +-----------------------+-------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    none = P(0, 'none',)
    sub_command = P(1, 'sub_command',)
    sub_command_group = P(2, 'sub_command_group',)
    string = P(3, 'string',)
    integer = P(4, 'integer',)
    boolean = P(5, 'boolean',)
    user = P(6, 'user',)
    channel = P(7, 'channel',)
    role = P(8, 'role',)
    mentionable = P(9, 'mentionable',)

@export
class InteractionType(PreinstancedBase):
    """
    The type of an interaction.
    
    Attributes
    ----------
    name : `str`
        The name of the interaction type.
    value : `int`
        The identifier value the interaction type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``InteractionType``) items
        Stores the predefined ``InteractionType`` instances. These can be accessed with their `value` as
        key.
    VALUE_TYPE : `type` = `int`
        The application command option types' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the interaction types.
    
    Every predefined interaction type. can be accessed as class attribute as well:
    
    +-----------------------+-----------------------+-------+
    | Class attribute name  | Name                  | Value |
    +=======================+=======================+=======+
    | none                  | none                  | 0     |
    +-----------------------+-----------------------+-------+
    | ping                  | ping                  | 1     |
    +-----------------------+-----------------------+-------+
    | application_command   | application_command   | 2     |
    +-----------------------+-----------------------+-------+
    | message_component     | message_component     | 3     |
    +-----------------------+-----------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    none = P(0, 'none')
    ping = P(1, 'ping')
    application_command = P(2, 'application_command')
    message_component = P(3, 'message_component')


class ApplicationCommandPermissionOverwriteType(PreinstancedBase):
    """
    Represents an application command's permission's type.
    
    Attributes
    ----------
    name : `str`
        The name of the application command permission overwrite type.
    value : `int`
        The identifier value the application command permission overwrite type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``ApplicationCommandPermissionOverwriteType``) items
        Stores the predefined ``ApplicationCommandPermissionOverwriteType`` instances. These can be accessed with their
        `value` as key.
    VALUE_TYPE : `type` = `int`
        The application command permission overwrite types' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the application command permission overwrite types.
    
    Every predefined application command permission overwrite type can be accessed as class attribute as well:
    
    +-----------------------+-------+-------+
    | Class attribute name  | Name  | Value |
    +=======================+=======+=======+
    | none                  | none  | 0     |
    +-----------------------+-------+-------+
    | role                  | role  | 1     |
    +-----------------------+-------+-------+
    | user                  | user  | 2     |
    +-----------------------+-------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    none = P(0, 'none',)
    role = P(1, 'role',)
    user = P(2, 'user',)


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
        Stores the predefined ``ComponentType`` instances. These can be accessed with their `value` as key.
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
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    none = P(0, 'none')
    row = P(1, 'row')
    button = P(2, 'button')
    select = P(3, 'select')
    

class ButtonStyle(PreinstancedBase):
    """
    Represents a component's type.
    
    Attributes
    ----------
    name : `str`
        The name of the button style.
    value : `int`
        The identifier value the button style
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``ButtonStyle``) items
        Stores the predefined ``ButtonStyle`` instances. These can be accessed with their `value` as key.
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
    
    
    @property
    def primary(self):
        """
        Deprecated, please use `.violet` instead. Will be removed in 2021 july.
        """
        warnings.warn(
            f'`{self.__class__.__name__}.primary` is deprecated, and will be removed in 2021 july. '
            f'Please use `{self.__class__.__name__}.violet` instead.',
            FutureWarning)
        
        return self.violet
    
    
    @property
    def secondary(self):
        """
        Deprecated, please use `.gray` instead. Will be removed in 2021 july.
        """
        warnings.warn(
            f'`{self.__class__.__name__}.secondary` is deprecated, and will be removed in 2021 july. '
            f'Please use `{self.__class__.__name__}.gray` instead.',
            FutureWarning)
        
        return self.gray
    
    
    @property
    def success(self):
        """
        Deprecated, please use `.green` instead. Will be removed in 2021 july.
        """
        warnings.warn(
            f'`{self.__class__.__name__}.success` is deprecated, and will be removed in 2021 july. '
            f'Please use `{self.__class__.__name__}.green` instead.',
            FutureWarning)
        
        return self.green
    
    
    @property
    def destructive(self):
        """
        Deprecated, please use `.red` instead. Will be removed in 2021 july.
        """
        warnings.warn(
            f'`{self.__class__.__name__}.destructive` is deprecated, and will be removed in 2021 july. '
            f'Please use `{self.__class__.__name__}.red` instead.',
            FutureWarning)
        
        return self.red
