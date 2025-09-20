__all__ = ('ComponentType',)

from scarletio import export

from ...bases import Preinstance as P, PreinstancedBase
from ...resolved.resolver.resolvers import (
    RESOLVER_CHANNEL, RESOLVER_MENTIONABLE, RESOLVER_ROLE, RESOLVER_STRING, RESOLVER_USER
)

from ..component_metadata import (
    ComponentMetadataAttachmentMedia, ComponentMetadataBase, ComponentMetadataButton, ComponentMetadataChannelSelect,
    ComponentMetadataContainer, ComponentMetadataLabel, ComponentMetadataMediaGallery,
    ComponentMetadataMentionableSelect, ComponentMetadataRoleSelect, ComponentMetadataRow, ComponentMetadataSection,
    ComponentMetadataSeparator, ComponentMetadataStringSelect, ComponentMetadataTextDisplay, ComponentMetadataTextInput,
    ComponentMetadataThumbnailMedia, ComponentMetadataUserSelect
)
from ..interaction_component_metadata import (
    InteractionComponentMetadataBase, InteractionComponentMetadataButton, InteractionComponentMetadataChannelSelect,
    InteractionComponentMetadataContainer, InteractionComponentMetadataLabel,
    InteractionComponentMetadataMentionableSelect, InteractionComponentMetadataRoleSelect,
    InteractionComponentMetadataRow, InteractionComponentMetadataSection, InteractionComponentMetadataStringSelect,
    InteractionComponentMetadataTextInput, InteractionComponentMetadataUserSelect
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
    nestable_into_label = True,
    holds_value_single = True,
    holds_value_multiple = True,
)


@export
class ComponentType(PreinstancedBase, value_type = int):
    """
    Represents a component's type.
    
    Attributes
    ----------
    layout_flags : ``ComponentTypeLayoutFlag``
        Flags about the component's layout information.
    
    interaction_metadata_type : ``type<InteractionComponentMetadataBase>``
        Interaction component metadata type.
    
    iter_resolve : `None | GeneratorFunctionType`
        Iterative resolver function for resolving the values held by interaction components of this type.
    
    metadata_type : ``type<ComponentMetadataBase>``
        Metadata type.
    
    resolve : `None | FunctionType`
        Resolver function for resolving the values held by interaction components of this type.
    
    resolver : ``None | Resolver``
        The general resolver holding the resolve function for resolving the values held by interaction components of
        this type.
    
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
    | label                 | label                         | 18    |
    +-----------------------+-------------------------------+-------+
    """
    __slots__ = ('layout_flags', 'interaction_metadata_type', 'iter_resolve', 'metadata_type', 'resolve', 'resolver')
    
    
    def __new__(
        cls,
        value,
        name = None,
        *,
        interaction_metadata_type = ...,
        layout_flags = ...,
        metadata_type = ...,
        resolver = ...,
    ):
        """
        Creates a new component type.
        
        Parameters
        ----------
        value : `int`
            The Discord side identifier value of the channel type.
        
        name : `None | str` = `None`, Optional
            The default name of the channel type.
        
        interaction_metadata_type : ``type<InteractionComponentMetadataBase>``, Optional (Keyword only)
            The component type's respective interaction metadata type.
        
        layout_flags : ``ComponentTypeLayoutFlag``, Optional (Keyword only)
            Flags about the component's layout information.
        
        metadata_type : ``type<ComponentMetadataBase>``, Optional (Keyword only)
            The component type's respective metadata type.
        
        resolver : ``Resolver``, Optional (Keyword only)
            The general resolver holding the resolve function for resolving the values held by interaction components
            of this type.
        """
        if interaction_metadata_type is ...:
            interaction_metadata_type = InteractionComponentMetadataBase
        
        if layout_flags is ...:
            layout_flags = COMPONENT_TYPE_LAYOUT_FLAGS_ALL
        
        if metadata_type is ...:
            metadata_type = ComponentMetadataBase
        
        if resolver is ...:
            resolver = None
        
        while True:
            if (resolver is not None):
                if layout_flags.holds_value_single:
                    iter_resolve = resolver.iter_resolve_single
                    resolve = resolver.resolve_single
                    break
                
                if layout_flags.holds_value_multiple:
                    iter_resolve = resolver.iter_resolve_multiple
                    resolve = resolver.resolve_multiple
                    break
            
            iter_resolve = None
            resolve = None
            break
        
        self = PreinstancedBase.__new__(cls, value, name)
        self.layout_flags = layout_flags
        self.interaction_metadata_type = interaction_metadata_type
        self.iter_resolve = iter_resolve
        self.metadata_type = metadata_type
        self.resolve = resolve
        self.resolver = resolver
        return self
    
    
    none = P(
        0,
        'none',
        layout_flags = ComponentTypeLayoutFlag(),
    )
    
    row = P(
        1,
        'row',
        interaction_metadata_type = InteractionComponentMetadataRow,
        layout_flags = ComponentTypeLayoutFlag().update_by_keys(
            allowed_in_message = True,
            allowed_in_form = True,
            top_level = True,
            nestable_into_container = True,
            version_1 = True,
        ),
        metadata_type = ComponentMetadataRow,
    )
    
    button = P(
        2,
        'button',
        interaction_metadata_type = InteractionComponentMetadataButton,
        layout_flags = ComponentTypeLayoutFlag().update_by_keys(
            allowed_in_message = True,
            nestable_into_row = True,
            section_thumbnail = True,
            version_1 = True,
        ),
        metadata_type = ComponentMetadataButton,
    )
    
    string_select = P(
        3,
        'string select',
        interaction_metadata_type = InteractionComponentMetadataStringSelect,
        layout_flags = ComponentTypeLayoutFlag().update_by_keys(
            allowed_in_message = True,
            allowed_in_form = True,
            nestable_into_row = True,
            version_1 = True,
            nestable_into_label = True,
            holds_value_multiple = True,
        ),
        metadata_type = ComponentMetadataStringSelect,
        resolver = RESOLVER_STRING,
    )
    
    text_input = P(
        4,
        'text input',
        interaction_metadata_type = InteractionComponentMetadataTextInput,
        layout_flags = ComponentTypeLayoutFlag().update_by_keys(
            allowed_in_form = True,
            nestable_into_row = True,
            version_1 = True,
            nestable_into_label = True,
            holds_value_single = True,
        ),
        metadata_type = ComponentMetadataTextInput,
        resolver = RESOLVER_STRING,
    )
    
    user_select = P(
        5,
        'user select',
        interaction_metadata_type = InteractionComponentMetadataUserSelect,
        layout_flags = ComponentTypeLayoutFlag().update_by_keys(
            allowed_in_message = True,
            nestable_into_row = True,
            version_1 = True,
            nestable_into_label = True,
            holds_value_multiple = True,
        ),
        metadata_type = ComponentMetadataUserSelect,
        resolver = RESOLVER_USER,
    )
    
    role_select = P(
        6,
        'role select',
        interaction_metadata_type = InteractionComponentMetadataRoleSelect,
        layout_flags = ComponentTypeLayoutFlag().update_by_keys(
            allowed_in_message = True,
            nestable_into_row = True,
            version_1 = True,
            nestable_into_label = True,
            holds_value_multiple = True,
        ),
        metadata_type = ComponentMetadataRoleSelect,
        resolver = RESOLVER_ROLE,
    )
    
    mentionable_select = P(
        7,
        'mentionable select',
        interaction_metadata_type = InteractionComponentMetadataMentionableSelect,
        layout_flags = ComponentTypeLayoutFlag().update_by_keys(
            allowed_in_message = True,
            nestable_into_row = True,
            version_1 = True,
            nestable_into_label = True,
            holds_value_multiple = True,
        ),
        metadata_type = ComponentMetadataMentionableSelect,
        resolver = RESOLVER_MENTIONABLE,
    )
    
    channel_select = P(
        8,
        'channel select',
        interaction_metadata_type = InteractionComponentMetadataChannelSelect,
        layout_flags = ComponentTypeLayoutFlag().update_by_keys(
            allowed_in_message = True,
            nestable_into_row = True,
            version_1 = True,
            nestable_into_label = True,
            holds_value_multiple = True,
        ),
        metadata_type = ComponentMetadataChannelSelect,
        resolver = RESOLVER_CHANNEL,
    )
    
    section = P(
        9,
        'section',
        interaction_metadata_type = InteractionComponentMetadataSection,
        layout_flags = ComponentTypeLayoutFlag().update_by_keys(
            allowed_in_message = True,
            top_level = True,
            nestable_into_container = True,
            version_2 = True,
        ),
        metadata_type = ComponentMetadataSection,
    )
    
    text_display = P(
        10,
        'text display',
        layout_flags = ComponentTypeLayoutFlag().update_by_keys(
            allowed_in_message = True,
            allowed_in_form = True,
            top_level = True,
            nestable_into_container = True,
            nestable_into_section = True,
            version_2 = True,
        ),
        metadata_type = ComponentMetadataTextDisplay,
    )
    
    thumbnail_media = P(
        11,
        'thumbnail media',
        layout_flags = ComponentTypeLayoutFlag().update_by_keys(
            allowed_in_message = True,
            section_thumbnail = True,
            version_2 = True,
        ),
        metadata_type = ComponentMetadataThumbnailMedia,
    )
    
    media_gallery = P(
        12,
        'media gallery',
        layout_flags = ComponentTypeLayoutFlag().update_by_keys(
            allowed_in_message = True,
            top_level = True,
            nestable_into_container = True,
            version_2 = True,
        ),
        metadata_type = ComponentMetadataMediaGallery,
    )
    
    attachment_media = P(
        13,
        'attachment media',
        layout_flags = ComponentTypeLayoutFlag().update_by_keys(
            allowed_in_message = True,
            top_level = True,
            nestable_into_container = True,
            version_2 = True,
        ),
        metadata_type = ComponentMetadataAttachmentMedia,
    )
    
    separator = P(
        14,
        'separator',
        layout_flags = ComponentTypeLayoutFlag().update_by_keys(
            allowed_in_message = True,
            top_level = True,
            nestable_into_container = True,
            version_2 = True,
        ),
        metadata_type = ComponentMetadataSeparator,
    )
    
    # 15 ???
    
    # 16 ???
    
    container = P(
        17,
        'container',
        interaction_metadata_type = InteractionComponentMetadataContainer,
        layout_flags = ComponentTypeLayoutFlag().update_by_keys(
            allowed_in_message = True,
            top_level = True,
            version_2 = True,
        ),
        metadata_type = ComponentMetadataContainer,
    )
    
    label = P(
        18,
        'label',
        interaction_metadata_type = InteractionComponentMetadataLabel,
        layout_flags = ComponentTypeLayoutFlag().update_by_keys(
            allowed_in_form = True,
            top_level = True,
            version_2 = True,
        ),
        metadata_type = ComponentMetadataLabel,
    )
