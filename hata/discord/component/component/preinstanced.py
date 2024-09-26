__all__ = ('ComponentType',)

from ...bases import Preinstance as P, PreinstancedBase

from ..component_metadata import (
    ComponentMetadataBase, ComponentMetadataButton, ComponentMetadataChannelSelect, ComponentMetadataMediaGallery,
    ComponentMetadataMentionableSelect, ComponentMetadataRoleSelect, ComponentMetadataRow,
    ComponentMetadataStringSelect, ComponentMetadataSeparator, ComponentMetadataText, ComponentMetadataTextInput,
    ComponentMetadataUserSelect
)

from .flags import ComponentTypeLayoutFlag


COMPONENT_TYPE_LAYOUT_FLAGS_ALL = ComponentTypeLayoutFlag().update_by_keys(top_level = True, nestable = True)


class ComponentType(PreinstancedBase):
    """
    Represents a component's type.
    
    Attributes
    ----------
    layout_flags : ``ComponentTypeLayoutFlag``
        Flags about the component's layout information.
    
    metadata_type : `type<ComponentMetadataBase>`
        Metadata type.
    
    name : `str`
        The name of the component type.
    
    value : `int`
        The identifier value the component type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``ComponentType``) items
        Stores the predefined ``ComponentType``-s. These can be accessed with their `value` as key.
    
    VALUE_TYPE : `type` = `int`
        The component type's type.
    
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the component types.
    
    Every predefined component type can be accessed as class attribute as well:
    
    +-----------------------+-------------------------------+-------+
    | Class attribute name  | Name                          | Value |
    +=======================+===============================+=======+
    | none                  | none                          | 0     |
    +-----------------------+-------------------------------+-------+
    | row                   | row                           | 1     |
    +-----------------------+-------------------------------+-------+
    | button                | button                        | 2     |
    +-----------------------+-------------------------------+-------+
    | string_select         | string select                 | 3     |
    +-----------------------+-------------------------------+-------+
    | text_input            | text input                    | 4     |
    +-----------------------+-------------------------------+-------+
    | user_select           | user select                   | 5     |
    +-----------------------+-------------------------------+-------+
    | role_select           | role select                   | 6     |
    +-----------------------+-------------------------------+-------+
    | mentionable_select    | mentionable select            | 7     |
    +-----------------------+-------------------------------+-------+
    | channel_select        | channel select                | 8     |
    +-----------------------+-------------------------------+-------+
    | ???                   | ???                           | 9     |
    +-----------------------+-------------------------------+-------+
    | text                  | text                          | 10    |
    +-----------------------+-------------------------------+-------+
    | ???                   | ???                           | 11    |
    +-----------------------+-------------------------------+-------+
    | media_gallery         | media gallery                 | 12    |
    +-----------------------+-------------------------------+-------+
    | ???                   | ???                           | 13    |
    +-----------------------+-------------------------------+-------+
    | separator             | separator                     | 14    |
    +-----------------------+-------------------------------+-------+
    | ???                   | ???                           | 15    |
    +-----------------------+-------------------------------+-------+
    | ???                   | activity content inventory    | 16    |
    +-----------------------+-------------------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ('layout_flags', 'metadata_type', )
    

    @classmethod
    def _from_value(cls, value):
        """
        Creates a new component type with the given value.
        
        Parameters
        ----------
        value : `int`
            The channel type's identifier value.
        
        Returns
        -------
        self : ``ChannelType``
            The created instance.
        """
        self = object.__new__(cls)
        self.name = cls.DEFAULT_NAME
        self.value = value
        self.layout_flags = COMPONENT_TYPE_LAYOUT_FLAGS_ALL
        self.metadata_type = ComponentMetadataBase
        
        return self
    
    
    def __init__(self, value, name, metadata_type, layout_flags):
        """
        Creates a new component type and stores it at the class's `.INSTANCES` class attribute as well.
        
        Parameters
        ----------
        value : `int`
            The Discord side identifier value of the channel type.
        
        name : `str`
            The default name of the channel type.
        
        metadata_type : `type<ComponentMetadataBase>`
            The component type's respective metadata type.
        
        layout_flags : ``ComponentTypeLayoutFlag``
            Flags about the component's layout information.
        """
        self.value = value
        self.name = name
        self.layout_flags = layout_flags
        self.metadata_type = metadata_type
        
        self.INSTANCES[value] = self
    
    
    none = P(
        0,
        'none',
        ComponentMetadataBase,
        ComponentTypeLayoutFlag(),
    )
    row = P(
        1,
        'row',
        ComponentMetadataRow,
        ComponentTypeLayoutFlag().update_by_keys(top_level = True),
    )
    button = P(
        2,
        'button',
        ComponentMetadataButton,
        ComponentTypeLayoutFlag().update_by_keys(nestable = True),
    )
    string_select = P(
        3,
        'string select',
        ComponentMetadataStringSelect,
        ComponentTypeLayoutFlag().update_by_keys(nestable = True),
    )
    text_input = P(
        4,
        'text input',
        ComponentMetadataTextInput,
        ComponentTypeLayoutFlag().update_by_keys(nestable = True),
    )
    user_select = P(
        5,
        'user select',
        ComponentMetadataUserSelect,
        ComponentTypeLayoutFlag().update_by_keys(nestable = True),
    )
    role_select = P(
        6,
        'role select',
        ComponentMetadataRoleSelect,
        ComponentTypeLayoutFlag().update_by_keys(nestable = True),
    )
    mentionable_select = P(
        7,
        'mentionable select',
        ComponentMetadataMentionableSelect,
        ComponentTypeLayoutFlag().update_by_keys(nestable = True),
    )
    channel_select = P(
        8,
        'channel select',
        ComponentMetadataChannelSelect,
        ComponentTypeLayoutFlag().update_by_keys(nestable = True),
    )
    
    # Not released, so we do not know their layout
    text = P(
        10,
        'text',
        ComponentMetadataText,
        COMPONENT_TYPE_LAYOUT_FLAGS_ALL,
    )
    media_gallery = P(
        12,
        'media gallery',
        ComponentMetadataMediaGallery,
        COMPONENT_TYPE_LAYOUT_FLAGS_ALL,
    )
    separator = P(
        14,
        'separator',
        ComponentMetadataSeparator,
        COMPONENT_TYPE_LAYOUT_FLAGS_ALL,
    )
