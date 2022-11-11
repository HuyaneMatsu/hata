__all__ = ()

__doc__ = """
Contains the interaction response type's, which are the following:

+-------------------------------------------+-------+---------------+
| Respective name                           | Value | Notes         |
+===========================================+=======+===============+
| none                                      | 0     | -             |
+-------------------------------------------+-------+---------------+
| pong                                      | 1     | -             |
+-------------------------------------------+-------+---------------+
| acknowledge                               | 2     | Deprecated.   |
+-------------------------------------------+-------+---------------+
| message                                   | 3     | Deprecated.   |
+-------------------------------------------+-------+---------------+
| message_and_source                        | 4     | -             |
+-------------------------------------------+-------+---------------+
| source                                    | 5     | -             |
+-------------------------------------------+-------+---------------+
| component                                 | 6     | -             |
+-------------------------------------------+-------+---------------+
| component_message_edit                    | 7     | -             |
+-------------------------------------------+-------+---------------+
| application_command_autocomplete_result   | 8     | -             |
+-------------------------------------------+-------+---------------+
| form                                      | 9     | -             |
+-------------------------------------------+-------+---------------+
"""

none = 0
pong = 1
acknowledge = 2
message = 3
message_and_source = 4
source = 5
component = 6
component_message_edit = 7
application_command_autocomplete_result = 8
form = 9



__all__ = ('InteractionResponseType',)

from scarletio import export

from ...bases import Preinstance as P, PreinstancedBase


@export
class InteractionResponseType(PreinstancedBase):
    """
    The type of an interaction.
    
    Attributes
    ----------
    name : `str`
        The name of the interaction response type.
    value : `int`
        The identifier value the interaction response type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``InteractionResponseType``) items
        Stores the predefined ``InteractionResponseType``-s. These can be accessed with their `value` as
        key.
    VALUE_TYPE : `type` = `int`
        The application command option types' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the interaction response types.
    
    Every predefined interaction response type can be accessed as class attribute as well:
    
    +-------------------------------------------+-------------------------------------------+-------+-------------------------------+
    | Class attribute name                      | Name                                      | Value | Notes                         |
    +===========================================+===========================================+=======+===============================+
    | none                                      | none                                      | 0     | -                             |
    +-------------------------------------------+-------------------------------------------+-------+-------------------------------+
    | pong                                      | pong                                      | 1     | -                             |
    +-------------------------------------------+-------------------------------------------+-------+-------------------------------+
    | acknowledge                               | acknowledge                               | 2     | Deprecated.                   |
    +-------------------------------------------+-------------------------------------------+-------+-------------------------------+
    | message                                   | message                                   | 3     | Deprecated.                   |
    +-------------------------------------------+-------------------------------------------+-------+-------------------------------+
    | message_and_source                        | message and source                        | 4     | -                             |
    +-------------------------------------------+-------------------------------------------+-------+-------------------------------+
    | source                                    | source                                    | 5     | -                             |
    +-------------------------------------------+-------------------------------------------+-------+-------------------------------+
    | component                                 | component                                 | 6     | -                             |
    +-------------------------------------------+-------------------------------------------+-------+-------------------------------+
    | component_message_edit                    | component message edit                    | 7     | -                             |
    +-------------------------------------------+-------------------------------------------+-------+-------------------------------+
    | application_command_autocomplete_result   | application command autocomplete result   | 8     | -                             |
    +-------------------------------------------+-------------------------------------------+-------+-------------------------------+
    | form                                      | form                                      | 9     | -                             |
    +-------------------------------------------+-------------------------------------------+-------+-------------------------------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    none = P(0, 'none')
    pong = P(1, 'pong')
    acknowledge = P(2, 'acknowledge')
    message = P(3, 'message')
    message_and_source = P(4, 'message and source')
    source = P(5, 'source')
    component = P(6, 'component')
    component_message_edit = P(7, 'component message edit')
    application_command_autocomplete_result = P(8, 'application command autocomplete result')
    form = P(9, 'form')
