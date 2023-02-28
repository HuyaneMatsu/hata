__all__ = ('ApplicationCommandOptionMetadataFloat',)

from .numeric import ApplicationCommandOptionMetadataNumeric


class ApplicationCommandOptionMetadataFloat(ApplicationCommandOptionMetadataNumeric):
    """
    Float parameter application command option metadata.
    
    Attributes
    ----------
    autocomplete : `bool`
        Whether the option supports auto completion.
    
    choices : `None`, `tuple` of ``ApplicationCommandOptionChoice``
        Choices for the user to pick from.
    
    max_value : `None`, `float`
        The maximal value permitted for this option.
    
    min_value : `None`, `float`
        The minimum value permitted for this option.
    
    required : `bool`
        Whether the parameter is required. Defaults to `False`.
    """
    TYPE = float
    
    __slots__ = ()
