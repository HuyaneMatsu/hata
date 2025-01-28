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


class ComponentType(PreinstancedBase, value_type = int):
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
    
    Type Attributes
    ---------------
    Every predefined component type can be accessed as type attribute as well:
    
    +-----------------------+-------------------------------+-------+
    | Type attribute name   | Name                          | Value |
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
    __slots__ = ('layout_flags', 'metadata_type', )
    
    
    def __new__(cls, value, name= None, metadata_type = None, layout_flags = ...):
        """
        Creates a new component type.
        
        Parameters
        ----------
        value : `int`
            The Discord side identifier value of the channel type.
        
        name : `None | str` = `None`, Optional
            The default name of the channel type.
        
        metadata_type : `None | type<ComponentMetadataBase>` = `None`, Optional
            The component type's respective metadata type.
        
        layout_flags : ``ComponentTypeLayoutFlag``, Optional
            Flags about the component's layout information.
        """
        if metadata_type is None:
            metadata_type = ComponentMetadataBase
        
        if layout_flags is ...:
            layout_flags = COMPONENT_TYPE_LAYOUT_FLAGS_ALL
        
        self = PreinstancedBase.__new__(cls, value, name)
        self.layout_flags = layout_flags
        self.metadata_type = metadata_type
        return self
    
    
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
