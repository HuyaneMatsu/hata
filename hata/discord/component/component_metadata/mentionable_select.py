__all__ = ('ComponentMetadataMentionableSelect', )

from .entity_select_base import ComponentMetadataEntitySelectBase


class ComponentMetadataMentionableSelect(ComponentMetadataEntitySelectBase):
    """
    mentionable (User and role) select component metadata.
    
    Attributes
    ----------
    custom_id : `None | str`
        Custom identifier to detect which component was used by the user.
    
    default_values : ``None | tuple<EntitySelectDefaultValue>``
        Entities presented in the select by default.
    
    enabled : `bool`
        Whether the component is enabled.
    
    max_values : `int
        The maximal amount of options to select.
    
    min_values : `int`
        The minimal amount of options to select.
    
    placeholder : `None | str`
        Placeholder text of the select.
    """
    __slots__ = ()
