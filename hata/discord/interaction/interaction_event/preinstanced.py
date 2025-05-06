__all__ = ('InteractionType',)

from scarletio import export

from ...bases import Preinstance as P, PreinstancedBase

from ..interaction_metadata import (
    InteractionMetadataApplicationCommand, InteractionMetadataApplicationCommandAutocomplete, InteractionMetadataBase,
    InteractionMetadataFormSubmit, InteractionMetadataMessageComponent
)


@export
class InteractionType(PreinstancedBase, value_type = int):
    """
    The type of an interaction.
    
    Attributes
    ----------
    metadata_type : `type<InteractionMetadataBase>`
        The interaction's respective metadata type.
    
    name : `str`
        The name of the interaction type.
    
    value : `int`
        The identifier value the interaction type.
    
    Type Attributes
    ---------------
    Every predefined interaction type can be accessed as type attribute as well:
    
    +-----------------------------------+-----------------------------------+-------+---------------------------------------------------+
    | Type attribute name               | Name                              | Value | Metadata type                                     |
    +===================================+===================================+=======+===================================================+
    | none                              | none                              | 0     | InteractionMetadataBase                           |
    +-----------------------------------+-----------------------------------+-------+---------------------------------------------------+
    | ping                              | ping                              | 1     | InteractionMetadataBase                           |
    +-----------------------------------+-----------------------------------+-------+---------------------------------------------------+
    | application_command               | application_command               | 2     | InteractionMetadataApplicationCommand             |
    +-----------------------------------+-----------------------------------+-------+---------------------------------------------------+
    | message_component                 | message_component                 | 3     | InteractionMetadataMessageComponent               |
    +-----------------------------------+-----------------------------------+-------+---------------------------------------------------+
    | application_command_autocomplete  | application_command_autocomplete  | 4     | InteractionMetadataApplicationCommandAutocomplete |
    +-----------------------------------+-----------------------------------+-------+---------------------------------------------------+
    | form_submit                       | form_submit                       | 5     | InteractionMetadataFormSubmit                     |
    +-----------------------------------+-----------------------------------+-------+---------------------------------------------------+
    """
    __slots__ = ('metadata_type',)
    
    def __new__(cls, value, name = None, metadata_type = None):
        """
        Creates an interaction type.
        
        Parameters
        ----------
        value : `int`
            The Discord side identifier value of the interaction type.
        
        name : `None | str` = `None`
            The default name of the interaction type.
        
        metadata_type : `None | type<InteractionMetadataBase>`
            The interaction type's respective metadata type.
        """
        if metadata_type is None:
            metadata_type = InteractionMetadataBase
        
        self = PreinstancedBase.__new__(cls, value, name)
        self.metadata_type = metadata_type
        return self
    
    
    none = P(0, 'none', InteractionMetadataBase)
    ping = P(1, 'ping', InteractionMetadataBase)
    application_command = P(2, 'application_command', InteractionMetadataApplicationCommand)
    message_component = P(3, 'message_component', InteractionMetadataMessageComponent)
    application_command_autocomplete = P(
        4, 'application_command_autocomplete', InteractionMetadataApplicationCommandAutocomplete
    )
    form_submit = P(5, 'form_submit', InteractionMetadataFormSubmit)
