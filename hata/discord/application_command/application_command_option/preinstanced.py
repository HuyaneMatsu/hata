__all__ = ('ApplicationCommandOptionType',)

from ...bases import Preinstance as P, PreinstancedBase

from ..application_command_option_metadata import (
    ApplicationCommandOptionMetadataBase, ApplicationCommandOptionMetadataChannel,
    ApplicationCommandOptionMetadataFloat, ApplicationCommandOptionMetadataInteger,
    ApplicationCommandOptionMetadataNested, ApplicationCommandOptionMetadataParameter,
    ApplicationCommandOptionMetadataString, ApplicationCommandOptionMetadataSubCommand
)


class ApplicationCommandOptionType(PreinstancedBase):
    """
    Represents an application command option's type.
    
    Attributes
    ----------
    name : `str`
        The name of the application command option type.
    value : `int`
        The identifier value the application command option type.
    metadata_type : `type<ApplicationCommandOptionMetadataBase>`
        The option type's respective metadata type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``ApplicationCommandOptionType``) items
        Stores the predefined ``ApplicationCommandOptionType``-s. These can be accessed with their `value` as
        key.
    VALUE_TYPE : `type` = `int`
        The application command option types' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the application command option types.
    
    Every predefined application command option type can be accessed as class attribute as well:
    
    +-----------------------+-------------------+-------+---------------------------------------------------+
    | Class attribute name  | Name              | Value | Metadata type                                     |
    +=======================+===================+=======+===================================================+
    | none                  | none              | 0     | ``ApplicationCommandOptionMetadataBase``          |
    +-----------------------+-------------------+-------+---------------------------------------------------+
    | sub_command           | sub-command       | 1     | ``ApplicationCommandOptionMetadataSubCommand``    |
    +-----------------------+-------------------+-------+---------------------------------------------------+
    | sub_command_group     | sub-command group | 2     | ``ApplicationCommandOptionMetadataNested``        |
    +-----------------------+-------------------+-------+---------------------------------------------------+
    | string                | string            | 3     | ``ApplicationCommandOptionMetadataString``        |
    +-----------------------+-------------------+-------+---------------------------------------------------+
    | integer               | integer           | 4     | ``ApplicationCommandOptionMetadataInteger``       |
    +-----------------------+-------------------+-------+---------------------------------------------------+
    | boolean               | boolean           | 5     | ``ApplicationCommandOptionMetadataParameter``     |
    +-----------------------+-------------------+-------+---------------------------------------------------+
    | user                  | user              | 6     | ``ApplicationCommandOptionMetadataParameter``     |
    +-----------------------+-------------------+-------+---------------------------------------------------+
    | channel               | channel           | 7     | ``ApplicationCommandOptionMetadataChannel``       |
    +-----------------------+-------------------+-------+---------------------------------------------------+
    | role                  | role              | 8     | ``ApplicationCommandOptionMetadataParameter``     |
    +-----------------------+-------------------+-------+---------------------------------------------------+
    | mentionable           | mentionable       | 9     | ``ApplicationCommandOptionMetadataParameter``     |
    +-----------------------+-------------------+-------+---------------------------------------------------+
    | float                 | float             | 10    | ``ApplicationCommandOptionMetadataFloat``         |
    +-----------------------+-------------------+-------+---------------------------------------------------+
    | attachment            | attachment        | 11    | ``ApplicationCommandOptionMetadataParameter``     |
    +-----------------------+-------------------+-------+---------------------------------------------------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ('metadata_type',)
    

    @classmethod
    def _from_value(cls, value):
        """
        Creates a new application command option type with the given value.
        
        Parameters
        ----------
        value : `int`
            The application command option type's identifier value.
        
        Returns
        -------
        self : `instance<cls>`
            The created instance.
        """
        self = object.__new__(cls)
        self.name = cls.DEFAULT_NAME
        self.value = value
        self.metadata_type = ApplicationCommandOptionMetadataBase
        
        return self
    
    
    def __init__(self, value, name, metadata_type):
        """
        Creates a new application command option type and stores it at the class's `.INSTANCES` class attribute as well.
        
        Parameters
        ----------
        value : `int`
            The Discord side identifier value of the application command option type.
        name : `str`
            The default name of the application command option type.
        metadata_type : `type<ApplicationCommandOptionMetadataBase>`
            The option type's respective metadata type.
        """
        self.value = value
        self.name = name
        self.metadata_type = metadata_type
        
        self.INSTANCES[value] = self
    
    
    none = P(0, 'none', ApplicationCommandOptionMetadataBase)
    sub_command = P(1, 'sub-command', ApplicationCommandOptionMetadataSubCommand)
    sub_command_group = P(2, 'sub-command group', ApplicationCommandOptionMetadataNested)
    string = P(3, 'string', ApplicationCommandOptionMetadataString)
    integer = P(4, 'integer', ApplicationCommandOptionMetadataInteger)
    boolean = P(5, 'boolean', ApplicationCommandOptionMetadataParameter)
    user = P(6, 'user', ApplicationCommandOptionMetadataParameter)
    channel = P(7, 'channel', ApplicationCommandOptionMetadataChannel)
    role = P(8, 'role', ApplicationCommandOptionMetadataParameter)
    mentionable = P(9, 'mentionable', ApplicationCommandOptionMetadataParameter)
    float = P(10, 'float', ApplicationCommandOptionMetadataFloat)
    attachment = P(11, 'attachment', ApplicationCommandOptionMetadataParameter)
