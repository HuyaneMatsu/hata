__all__ = ('ComponentType',)

import warnings

from scarletio import class_property

from ...bases import Preinstance as P, PreinstancedBase

from ..component_metadata import (
    ComponentMetadataBase, ComponentMetadataButton, ComponentMetadataChannelSelect, ComponentMetadataMentionableSelect,
    ComponentMetadataRoleSelect, ComponentMetadataRow, ComponentMetadataStringSelect, ComponentMetadataTextInput,
    ComponentMetadataUserSelect
)


class ComponentType(PreinstancedBase):
    """
    Represents a component's type.
    
    Attributes
    ----------
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
    
    +-----------------------+-----------------------+-------+
    | Class attribute name  | Name                  | Value |
    +=======================+=======================+=======+
    | none                  | none                  | 0     |
    +-----------------------+-----------------------+-------+
    | row                   | row                   | 1     |
    +-----------------------+-----------------------+-------+
    | button                | button                | 2     |
    +-----------------------+-----------------------+-------+
    | string_select         | string select         | 3     |
    +-----------------------+-----------------------+-------+
    | text_input            | text input            | 4     |
    +-----------------------+-----------------------+-------+
    | user_select           | user select           | 5     |
    +-----------------------+-----------------------+-------+
    | role_select           | role select           | 6     |
    +-----------------------+-----------------------+-------+
    | mentionable_select    | mentionable select    | 7     |
    +-----------------------+-----------------------+-------+
    | channel_select        | channel select        | 8     |
    +-----------------------+-----------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ('metadata_type', )
    

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
        self.metadata_type = ComponentMetadataBase
        
        return self
    
    
    def __init__(self, value, name, metadata_type):
        """
        Creates a new component type and stores it at the class's `.INSTANCES` class attribute as well.
        
        Parameters
        ----------
        value : `int`
            The Discord side identifier value of the channel type.
        name : `str`
            The default name of the channel type.
        metadata_type : `None`, `type<ComponentMetadataBase>`
            The component type's respective metadata type.
        """
        self.value = value
        self.name = name
        self.metadata_type = metadata_type
        
        self.INSTANCES[value] = self
    
    
    none = P(0, 'none', ComponentMetadataBase)
    row = P(1, 'row', ComponentMetadataRow)
    button = P(2, 'button', ComponentMetadataButton)
    string_select = P(3, 'string select', ComponentMetadataStringSelect)
    text_input = P(4, 'text input', ComponentMetadataTextInput)
    user_select = P(5, 'user select', ComponentMetadataUserSelect)
    role_select = P(6, 'role select', ComponentMetadataRoleSelect)
    mentionable_select = P(7, 'mentionable select', ComponentMetadataMentionableSelect)
    channel_select = P(8, 'channel select', ComponentMetadataChannelSelect)
    
    
    @class_property
    def select(cls):
        """
        `.select` is deprecated and will be removed in 2023 January. Please use `.string_select` instead.
        """
        warnings.warn(
            (
                f'`{cls.__name__}.select` is deprecated and will be removed in 2023 January. '
                f'Please use `.string_select` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        return cls.string_select
