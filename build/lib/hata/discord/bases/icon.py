__all__ = ('ICON_TYPE_ANIMATED', 'ICON_TYPE_NONE', 'ICON_TYPE_STATIC', 'Icon', 'IconType', 'IconSlot',
    'PreinstancedBase', )

import sys

from ...backend.utils import DOCS_ENABLED, doc_property
from .preinstanced import PreinstancedBase, Preinstance as P

class IconType(PreinstancedBase):
    """
    Represents a Discord icon's type.
    
    Attributes
    ----------
    name : `str`
        The name of the icon type.
    value : `int`
        The identifier value the icon type.
        
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``IconType``) items
        Stores the predefined ``IconType`` instances. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The icon types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the icon types.
    
    Every predefined icon type can be accessed as class attribute as well:
    
    +-----------------------+---------------+-------+
    | Class attribute name  | name          | value |
    +=======================+===============+=======+
    | none                  | none          | 0     |
    +-----------------------+---------------+-------+
    | static                | static        | 1     |
    +-----------------------+---------------+-------+
    | animated              | animated      | 2     |
    +-----------------------+---------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    def __bool__(self):
        """Returns whether the icon's type is set."""
        if self.value:
            boolean = True
        else:
            boolean = False
        
        return boolean
    
    none = P(0, 'none')
    static = P(1, 'static')
    animated = P(2, 'animated')


ICON_TYPE_NONE = IconType.none
ICON_TYPE_STATIC = IconType.static
ICON_TYPE_ANIMATED = IconType.animated

class Icon:
    """
    Represents a Discord Icon.
    
    Attributes
    ----------
    hash : `int`
        The icon's hash value.
    type : ``IconType``
        The icon's type.
    """
    __slots__ = ('type', 'hash',)
    
    def __init__(self, icon_type, icon_hash):
        """
        Creates a new ``Icon`` object with the given attributes.
        
        Parameters
        ----------
        icon_type : ``IconType``
            The icon's type.
        icon_hash : `int`
            The icon's hash value.
        """
        self.type = icon_type
        self.hash = icon_hash
        
    @property
    def as_base16_hash(self):
        """
        Returns the discord side representation of the icon.
        
        Returns
        -------
        icon : `None` or `str`
        """
        icon_type = self.type
        if icon_type is ICON_TYPE_NONE:
            icon = None
        else:
            icon = self.hash.__format__('0>32x')
            if icon_type is ICON_TYPE_ANIMATED:
                icon = 'a_'+icon
        
        return icon
    
    hash_info_width = sys.hash_info.width
    if hash_info_width == 32:
        def __hash__(self):
            """Returns the icon's hash."""
            icon_type = self.type
            if icon_type is ICON_TYPE_NONE:
                hash_value = 0
            else:
                icon_hash = self.hash
                hash_value = (icon_hash>>96)^ \
                             ((icon_hash>>64)&((1<<32)-1))^ \
                             ((icon_hash>>32)&((1<<32)-1))^ \
                             (icon_hash&((1<<32)-1))
                
                if icon_type is ICON_TYPE_ANIMATED:
                    hash_value ^= ((1<<32)-1)
            
            return hash_value
    
    elif hash_info_width == 64:
        def __hash__(self):
            """Returns the icon's hash."""
            icon_type = self.type
            if icon_type is ICON_TYPE_NONE:
                hash_value = 0
            else:
                icon_hash = self.hash
                hash_value = (icon_hash>>64)^(icon_hash&((1<<64)-1))
                if icon_type is ICON_TYPE_ANIMATED:
                    hash_value ^= ((1<<64)-1)
            return hash_value
    
    else:
        def __hash__(self):
            """Returns the icon's hash."""
            icon_type = self.type
            if icon_type is ICON_TYPE_NONE:
                hash_value = 0
            else:
                hash_value = self.hash
                if icon_type is ICON_TYPE_ANIMATED:
                    hash_value ^= ((1<<128)-1)
            
            return hash_value
    
    del hash_info_width
    
    def __eq__(self, other):
        """Returns whether the two icons are equal."""
        if (type(self) is not type(other)):
            return NotImplemented
        
        icon_type = self.type
        if (icon_type is not other.type):
            return False
        
        if icon_type is ICON_TYPE_NONE:
            return True
        
        if self.hash == other.hash:
            return True
        
        return False
    
    def __repr__(self):
        """Returns the representation of the icon."""
        return f'{self.__class__.__name__}(type=ICON_TYPE_{self.type.name.upper()}, hash={self.hash})'
    
    def __iter__(self):
        """
        Unpacks the icon.
        
        This method is a generator.
        """
        yield self.type
        yield self.hash
    
    def __len__(self):
        """Length hinter (for unpacking if needed)."""
        return 2
    
    def __bool__(self):
        return (self.type is not ICON_TYPE_NONE)
    
    @classmethod
    def from_base16_hash(cls, icon):
        """
        Converts a discord icon hash value to an ``Icon`` object.
        
        Parameters
        ----------
        icon : `None` or `str`
        
        Returns
        -------
        self : ``Icon``
        """
        if icon is None:
            icon_type = ICON_TYPE_NONE
            icon_hash = 0
        else:
            if icon.startswith('a_'):
                icon = icon[2:]
                icon_type = ICON_TYPE_ANIMATED
            else:
                icon_type = ICON_TYPE_STATIC
            icon_hash = int(icon, 16)
        
        self = object.__new__(cls)
        self.type = icon_type
        self.hash = icon_hash
        return self


class IconSlot:
    if DOCS_ENABLED:
        __class_doc__ = (
    """
    Internal icon slotter to represent an icon of a discord entity.
    
    Attributes
    ----------
    internal_name : `str`
        The internal name of the icon.
    discord_side_name : `str`
        The discord side name of the icon.
    added_instance_attributes : `tuple` of `str`
        The added instance attribute's name by the icon slot.
    added_class_attributes : `list` of `tuple` (`str`, `Any`)
        The added class attributes by the icon slot.
    
    Class Attributes
    ----------------
    _compile_globals : `dict` of (`str`, `Any`)
        Compile time globals for the generated functions.
    """)
        
        __instance_doc__ = (
    """
    Returns the respective icon.
    
    Returns
    -------
    icon : ``Icon``
    """)
        
        __doc__ = doc_property()
    
    __slots__ = ('internal_name', 'discord_side_name', 'added_instance_attributes', 'added_class_attributes')
    
    _compile_globals = {
        'ICON_TYPE_NONE': ICON_TYPE_NONE     ,
        'ICON_TYPE_STATIC': ICON_TYPE_STATIC   ,
        'ICON_TYPE_ANIMATED': ICON_TYPE_ANIMATED ,
        'Icon': Icon               ,
    }
    
    def __new__(cls, internal_name, discord_side_name, url_property, url_as_method, add_updater=True):
        """
        Creates an ``IconSlot`` with the given parameters.
        
        Parameters
        ----------
        internal_name : `str`
            The internal name of the icon.
        discord_side_name : `str`
            The discord side name of the icon.
        url_property : `None` or `function`
            A function what will be used as a property when accessing the icon' url.
        url_as_method : `None` or `function`
            A function what will be used a method when creating a formatted icon url.
        add_updater : `bool`, Optional
            Whether the icon slot should add updater methods to the class. Defaults to `True`.
        
        Returns
        -------
        self : ``IconSlot``
        """
        added_instance_attribute_name_hash = internal_name+'_hash'
        added_internal_attribute_name_type = internal_name+'_type'
        
        added_class_attributes = []
        if (url_property is not None):
            added_class_attributes.append((f'{internal_name}_url', property(url_property)))
        
        if (url_as_method is not None):
            added_class_attributes.append((f'{internal_name}_url_as', url_as_method))
        
        locals_ = {}
        func_name = f'_set_{internal_name}'
        exec(compile((
            f'def {func_name}(self, data):\n'
            f'    icon = data.get({discord_side_name!r}, None)\n'
            f''
            f'    if icon is None:\n'
            f'        icon_type = ICON_TYPE_NONE\n'
            f'        icon_hash = 0\n'
            f'    else:\n'
            f'        if icon.startswith(\'a_\'):\n'
            f'            icon = icon[2:]\n'
            f'            icon_type = ICON_TYPE_ANIMATED\n'
            f'        else:\n'
            f'            icon_type = ICON_TYPE_STATIC\n'
            f'        icon_hash = int(icon, 16)\n'
            f''
            f'    self.{added_internal_attribute_name_type} = icon_type\n'
            f'    self.{added_instance_attribute_name_hash} = icon_hash\n'
        ), f'<{cls.__name__}>', 'exec', optimize=2), cls._compile_globals, locals_)
        
        added_class_attributes.append((func_name, locals_[func_name]),)
        
        if add_updater:
            locals_ = {}
            func_name = f'_update_{internal_name}'
            exec(compile((
                f'def {func_name}(self, data, old_attributes):\n'
                f'    icon = data.get({discord_side_name!r}, None)\n'
                f''
                f'    if icon is None:\n'
                f'        icon_type = ICON_TYPE_NONE\n'
                f'        icon_hash = 0\n'
                f'    else:\n'
                f'        if icon.startswith(\'a_\'):\n'
                f'            icon = icon[2:]\n'
                f'            icon_type = ICON_TYPE_ANIMATED\n'
                f'        else:\n'
                f'            icon_type = ICON_TYPE_STATIC\n'
                f'        icon_hash = int(icon, 16)\n'
                f''
                f'    self_icon_type = self.{added_internal_attribute_name_type}\n'
                f'    self_icon_hash = self.{added_instance_attribute_name_hash}\n'
                f'    if (self_icon_type is not icon_type) or (self_icon_hash != icon_hash):\n'
                f'        old_attributes[{internal_name!r}] = Icon(self_icon_type, self_icon_hash)\n'
                f'        self.{added_internal_attribute_name_type} = icon_type\n'
                f'        self.{added_instance_attribute_name_hash} = icon_hash\n'
            ), f'<{cls.__name__}>', 'exec', optimize=2), cls._compile_globals, locals_)
            
            added_class_attributes.append((func_name, locals_[func_name]),)
        
        self = object.__new__(cls)
        self.internal_name = internal_name
        self.discord_side_name = discord_side_name
        self.added_instance_attributes = (added_internal_attribute_name_type, added_instance_attribute_name_hash)
        self.added_class_attributes = added_class_attributes
        return self
    
    def __set_slot__(self, attribute_name, class_attributes, class_slots):
        """Applies the changes of the icon slot on the class's attributes."""
        
        # Extend the slots of the class
        class_slots.update(self.added_instance_attributes)
        
        # Add the extra class attributes to the class
        for name, value in self.added_class_attributes:
            class_attributes[name] = value
    
    def __get__(self, obj, type_):
        """Returns self if called from class, meanwhile an ``Icon`` if called from an object."""
        if obj is None:
            return self
        
        icon_type_name, icon_hash_name = self.added_instance_attributes
        icon_type = getattr(obj, icon_type_name)
        icon_hash = getattr(obj, icon_hash_name)
        return Icon(icon_type, icon_hash)
    
    def __set__(self, obj, value):
        """Can't set attribute."""
        raise AttributeError('can\'t set attribute')
    
    def __delete__(self, obj):
        """Can't delete attribute."""
        raise AttributeError('can\'t delete attribute')
    
    def preconvert(self, kwargs, processable):
        """
        Used at preconverters to parse out from the passed kwargs the icon of the entity.
        
        Parameters
        ----------
        kwargs : `dict` of (`str`, `Any`) items
            Keyword parameters passed to the respective preconverter.
        processable : `list` of `tuple` (`str`, `Any`)
            A list of instance attributes which will be set when all the passed kwargs are validated.
        
        Raises
        ------
        TypeError
            If any of expected value's type is invalid.
        ValueError
            If any of the expected value's type is valid, but it's value is not.
        """
        icon_type_name, icon_hash_name = self.added_instance_attributes
        try:
            icon = kwargs.pop(self.internal_name)
        except KeyError:
            try:
                icon_hash = kwargs.pop(icon_hash_name)
            except KeyError:
                return
            
            if type(icon_hash) is int:
                pass
            elif isinstance(icon_hash, int):
                icon_hash = int(icon_hash)
            else:
                raise TypeError(f'`{icon_hash_name}` can be passed as `int` instance, got '
                    f'{icon_hash.__class__.__name__}.')
            
            if icon_hash < 0 or icon_hash > ((1<<128)-1):
                raise ValueError(f'`{icon_hash_name}` cannot be negative or longer than 128 bits, got {icon_hash}.')
            
            try:
                icon_type = kwargs.pop(icon_type_name)
            except KeyError:
                if icon_hash == 0:
                    icon_type = ICON_TYPE_NONE
                else:
                    icon_type = ICON_TYPE_STATIC
            else:
                if (type(icon_type) is not IconType):
                    raise TypeError(f'`{icon_type_name}` can be passed as `{IconType.__name__}` instance, got '
                        f'{icon_type.__class__.__name__}.')
                
                if (icon_type is ICON_TYPE_NONE) and icon_hash:
                    raise ValueError(f'If `{icon_type_name}` is passed as `ICON_TYPE_NONE`, then `{icon_hash_name}` '
                        f'can be passed only as `0`, meanwhile got `{icon_hash}`.')
            
        else:
            if icon is None:
                icon_type = ICON_TYPE_NONE
                icon_hash = 0
            elif type(icon) is Icon:
                icon_type = icon.type
                icon_hash = icon.hash
            elif isinstance(icon, str):
                if icon.startswith('a_'):
                    icon = icon[2:]
                    icon_type = ICON_TYPE_ANIMATED
                else:
                    icon_type = ICON_TYPE_STATIC
                icon_hash = int(icon, 16)
            else:
                raise TypeError(f'`{self.internal_name!r}` can be passed as `None`, `{Icon.__name__}` or as `str` '
                    f'instance, got {icon.__class__.__name__}.')
        
        processable[icon_type_name] = icon_type
        processable[icon_hash_name] = icon_hash
