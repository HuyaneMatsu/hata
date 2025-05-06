__all__ = ('ComponentType',)

from scarletio import export

from ...bases import Preinstance as P, PreinstancedBase

from ..component_metadata import (
    ComponentMetadataAttachmentMedia, ComponentMetadataBase, ComponentMetadataButton, ComponentMetadataChannelSelect,
    ComponentMetadataContainer, ComponentMetadataMediaGallery, ComponentMetadataMentionableSelect,
    ComponentMetadataRoleSelect, ComponentMetadataRow, ComponentMetadataSection, ComponentMetadataSeparator,
    ComponentMetadataStringSelect, ComponentMetadataTextDisplay, ComponentMetadataTextInput,
    ComponentMetadataThumbnailMedia, ComponentMetadataUserSelect
)

from .flags import ComponentTypeLayoutFlag


COMPONENT_TYPE_LAYOUT_FLAGS_ALL = ComponentTypeLayoutFlag().update_by_keys(
    allowed_in_message = True,
    allowed_in_form = True,
    top_level = True,
    nestable_into_row = True,
    nestable_into_container = True,
    nestable_into_section = True,
    section_thumbnail = True,
    version_1 = True,
    version_2 = True,
)


@export
class ComponentType(PreinstancedBase, value_type = int):
    """
    Represents a component's type.
    
    Attributes
    ----------
    layout_flags : ``ComponentTypeLayoutFlag``
        Flags about the component's layout information.
    
    metadata_type : ``type<ComponentMetadataBase>``
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
    | section               | section                       | 9     |
    +-----------------------+-------------------------------+-------+
    | text_display          | text display                  | 10    |
    +-----------------------+-------------------------------+-------+
    | thumbnail_media       | thumbnail media               | 11    |
    +-----------------------+-------------------------------+-------+
    | media_gallery         | media gallery                 | 12    |
    +-----------------------+-------------------------------+-------+
    | attachment_media      | attachment media              | 13    |
    +-----------------------+-------------------------------+-------+
    | separator             | separator                     | 14    |
    +-----------------------+-------------------------------+-------+
    | ???                   | ???                           | 15    |
    +-----------------------+-------------------------------+-------+
    | ???                   | activity content inventory    | 16    |
    +-----------------------+-------------------------------+-------+
    | container             | container                     | 17    |
    +-----------------------+-------------------------------+-------+
    """
    __slots__ = ('layout_flags', 'metadata_type', )
    
    
    def __new__(cls, value, name = None, metadata_type = None, layout_flags = ...):
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
        ComponentTypeLayoutFlag().update_by_keys(
            allowed_in_message = True,
            allowed_in_form = True,
            top_level = True,
            nestable_into_container = True,
            version_1 = True,
        ),
    )
    
    button = P(
        2,
        'button',
        ComponentMetadataButton,
        ComponentTypeLayoutFlag().update_by_keys(
            allowed_in_message = True,
            nestable_into_row = True,
            section_thumbnail = True,
            version_1 = True,
        ),
    )
    
    string_select = P(
        3,
        'string select',
        ComponentMetadataStringSelect,
        ComponentTypeLayoutFlag().update_by_keys(
            allowed_in_message = True,
            nestable_into_row = True,
            version_1 = True,
        ),
    )
    
    text_input = P(
        4,
        'text input',
        ComponentMetadataTextInput,
        ComponentTypeLayoutFlag().update_by_keys(
            allowed_in_form = True,
            nestable_into_row = True,
            version_1 = True,
        ),
    )
    
    user_select = P(
        5,
        'user select',
        ComponentMetadataUserSelect,
        ComponentTypeLayoutFlag().update_by_keys(
            allowed_in_message = True,
            nestable_into_row = True,
            version_1 = True,
        ),
    )
    
    role_select = P(
        6,
        'role select',
        ComponentMetadataRoleSelect,
        ComponentTypeLayoutFlag().update_by_keys(
            allowed_in_message = True,
            nestable_into_row = True,
            version_1 = True,
        ),
    )
    
    mentionable_select = P(
        7,
        'mentionable select',
        ComponentMetadataMentionableSelect,
        ComponentTypeLayoutFlag().update_by_keys(
            allowed_in_message = True,
            nestable_into_row = True,
            version_1 = True,
        ),
    )
    
    channel_select = P(
        8,
        'channel select',
        ComponentMetadataChannelSelect,
        ComponentTypeLayoutFlag().update_by_keys(
            allowed_in_message = True,
            nestable_into_row = True,
            version_1 = True,
        ),
    )
    
    section = P(
        9,
        'section',
        ComponentMetadataSection,
        ComponentTypeLayoutFlag().update_by_keys(
            allowed_in_message = True,
            top_level = True,
            nestable_into_container = True,
            version_2 = True,
        ),
    )
    
    text_display = P(
        10,
        'text display',
        ComponentMetadataTextDisplay,
        ComponentTypeLayoutFlag().update_by_keys(
            allowed_in_message = True,
            top_level = True,
            nestable_into_container = True,
            nestable_into_section = True,
            version_2 = True,
        ),
    )
    
    thumbnail_media = P(
        11,
        'thumbnail media',
        ComponentMetadataThumbnailMedia,
        ComponentTypeLayoutFlag().update_by_keys(
            allowed_in_message = True,
            section_thumbnail = True,
            version_2 = True,
        ),
    )
    
    media_gallery = P(
        12,
        'media gallery',
        ComponentMetadataMediaGallery,
        ComponentTypeLayoutFlag().update_by_keys(
            allowed_in_message = True,
            top_level = True,
            nestable_into_container = True,
            version_2 = True,
        ),
    )
    
    attachment_media = P(
        13,
        'attachment media',
        ComponentMetadataAttachmentMedia,
        ComponentTypeLayoutFlag().update_by_keys(
            allowed_in_message = True,
            top_level = True,
            nestable_into_container = True,
            version_2 = True,
        ),
    )
    
    separator = P(
        14,
        'separator',
        ComponentMetadataSeparator,
        ComponentTypeLayoutFlag().update_by_keys(
            allowed_in_message = True,
            top_level = True,
            nestable_into_container = True,
            version_2 = True,
        ),
    )
    
    # 15 ???
    
    # 16 ???
    
    container = P(
        17,
        'container',
        ComponentMetadataContainer,
        ComponentTypeLayoutFlag().update_by_keys(
            allowed_in_message = True,
            top_level = True,
            version_2 = True,
        ),
    )
