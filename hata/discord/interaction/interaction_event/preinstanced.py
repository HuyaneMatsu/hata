__all__ = ('InteractionType',)

from scarletio import export

from ...bases import Preinstance as P, PreinstancedBase

from ..interaction_metadata import (
    InteractionMetadataApplicationCommand, InteractionMetadataApplicationCommandAutocomplete, InteractionMetadataBase,
    InteractionMetadataFormSubmit, InteractionMetadataMessageComponent
)


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
    metadata_type : `type<InteractionMetadataBase>`
        The interaction's respective metadata type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``InteractionType``) items
        Stores the predefined ``InteractionType``-s. These can be accessed with their `value` as
        key.
    VALUE_TYPE : `type` = `int`
        The application command option types' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the interaction types.
    
    Every predefined interaction type can be accessed as class attribute as well:
    
    +-----------------------------------+-----------------------------------+-------+---------------------------------------------------+
    | Class attribute name              | Name                              | Value | Metadata type                                     |
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
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ('metadata_type',)
    

    @classmethod
    def _from_value(cls, value):
        """
        Creates a new interaction type with the given value.
        
        Parameters
        ----------
        value : `int`
            The interaction type's identifier value.
        
        Returns
        -------
        self : ``InteractionType``
            The created instance.
        """
        self = object.__new__(cls)
        self.name = cls.DEFAULT_NAME
        self.value = value
        self.metadata_type = InteractionMetadataBase
        
        return self
    
    
    def __init__(self, value, name, metadata_type):
        """
        Creates an ``InteractionType`` and stores it at the class's `.INSTANCES` class attribute as well.
        
        Parameters
        ----------
        value : `int`
            The Discord side identifier value of the interaction type.
        name : `str`
            The default name of the interaction type.
        metadata_type : `None`, `type<InteractionMetadataBase>`
            The interaction type's respective metadata type.
        """
        self.value = value
        self.name = name
        self.metadata_type = metadata_type
        
        self.INSTANCES[value] = self
    
    
    none = P(0, 'none', InteractionMetadataBase)
    ping = P(1, 'ping', InteractionMetadataBase)
    application_command = P(2, 'application_command', InteractionMetadataApplicationCommand)
    message_component = P(3, 'message_component', InteractionMetadataMessageComponent)
    application_command_autocomplete = P(
        4, 'application_command_autocomplete', InteractionMetadataApplicationCommandAutocomplete
    )
    form_submit = P(5, 'form_submit', InteractionMetadataFormSubmit)
