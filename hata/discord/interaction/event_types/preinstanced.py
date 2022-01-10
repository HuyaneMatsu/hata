__all__ = ('InteractionType',)

from scarletio import export

from ...bases import Preinstance as P, PreinstancedBase


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
        Stores the predefined ``InteractionType``-s. These can be accessed with their `value` as
        key.
    VALUE_TYPE : `type` = `int`
        The application command option types' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the interaction types.
    
    Every predefined interaction type can be accessed as class attribute as well:
    
    +-----------------------------------+-----------------------------------+-------+
    | Class attribute name              | Name                              | Value |
    +===================================+===================================+=======+
    | none                              | none                              | 0     |
    +-----------------------------------+-----------------------------------+-------+
    | ping                              | ping                              | 1     |
    +-----------------------------------+-----------------------------------+-------+
    | application_command               | application_command               | 2     |
    +-----------------------------------+-----------------------------------+-------+
    | message_component                 | message_component                 | 3     |
    +-----------------------------------+-----------------------------------+-------+
    | application_command_autocomplete  | application_command_autocomplete  | 4     |
    +-----------------------------------+-----------------------------------+-------+
    | form_submit                       | form_submit                       | 5     |
    +-----------------------------------+-----------------------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    none = P(0, 'none')
    ping = P(1, 'ping')
    application_command = P(2, 'application_command')
    message_component = P(3, 'message_component')
    application_command_autocomplete = P(4, 'application_command_autocomplete')
    form_submit = P(5, 'form_submit')
