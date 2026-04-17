__all__ = ('ApplicationCommandOptionType',)

from ...bases import Preinstance as P, PreinstancedBase

from ..application_command_option_metadata import (
    ApplicationCommandOptionMetadataBase, ApplicationCommandOptionMetadataChannel,
    ApplicationCommandOptionMetadataFloat, ApplicationCommandOptionMetadataInteger,
    ApplicationCommandOptionMetadataNested, ApplicationCommandOptionMetadataParameter,
    ApplicationCommandOptionMetadataString, ApplicationCommandOptionMetadataSubCommand
)


class ApplicationCommandOptionType(PreinstancedBase, value_type = int):
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
    
    Type Attributes
    ---------------
    Every predefined application command option type can be accessed as type attribute as well:
    
    +-----------------------+-------------------+-------+---------------------------------------------------+
    | Type attribute name   | Name              | Value | Metadata type                                     |
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
    __slots__ = ('metadata_type',)
    
    def __new__(cls, value, name = None, metadata_type = None):
        """
        Creates a new application command option type.
        
        Parameters
        ----------
        value : `int`
            The Discord side identifier value of the application command option type.
        
        name : `None | str` = `None`, Optional
            The default name of the application command option type.
        
        metadata_type : `None | type<ApplicationCommandOptionMetadataBase>` = `None`, Optional
            The option type's respective metadata type.
        """
        if metadata_type is None:
            metadata_type = ApplicationCommandOptionMetadataBase
        
        self = PreinstancedBase.__new__(cls, value, name)
        self.metadata_type = metadata_type
        return self
    
    
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
