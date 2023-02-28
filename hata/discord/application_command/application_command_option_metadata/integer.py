__all__ = ('ApplicationCommandOptionMetadataInteger',)

from .numeric import ApplicationCommandOptionMetadataNumeric


class ApplicationCommandOptionMetadataInteger(ApplicationCommandOptionMetadataNumeric):
    """
    Integer parameter application command option metadata.
    
    Attributes
    ----------
    autocomplete : `bool`
        Whether the option supports auto completion.
    
    choices : `None`, `tuple` of ``ApplicationCommandOptionChoice``
        Choices for the user to pick from.
    
    max_value : `None`, `int`
        The maximal value permitted for this option.
    
    min_value : `None`, `int`
        The minimum value permitted for this option.
    
    required : `bool`
        Whether the parameter is required. Defaults to `False`.
    """
    TYPE = int
    
    __slots__ = ()
