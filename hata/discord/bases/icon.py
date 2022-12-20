__all__ = (
    'ICON_TYPE_ANIMATED', 'ICON_TYPE_NONE', 'ICON_TYPE_STATIC', 'Icon', 'IconType', 'IconSlot', 'PreinstancedBase'
)

import reprlib, sys, warnings
from base64 import b64encode

from scarletio import DOCS_ENABLED, RichAttributeErrorBaseType, copy_docs, docs_property, include

from .place_holder import PlaceHolder
from .preinstanced import Preinstance as P, PreinstancedBase

get_image_media_type = include('get_image_media_type')


class IconDetailsBase(RichAttributeErrorBaseType):
    """
    Stores details of an icon.
    """
    __slots__ = ()
    
    allowed_postfixes = PlaceHolder(
        None,
        """
        Returns allowed postfixes.
        
        Returns
        -------
        allowed_postfixes : `None`, `frozenset` of `str`
        """
    )
    
    data = PlaceHolder(
        None,
        """
        Returns the icon's raw data.
        
        Returns
        -------
        data : `None`, `bytes-like`
        """
    )
    
    default_postfix = PlaceHolder(
        '',
        """
        Returns the icon's default postfix.
        
        Returns
        -------
        default_postfix : `str`
        """
    )
    
    prefix = PlaceHolder(
        '',
        """
        Returns the icon's prefix.
        
        Returns
        -------
        prefix : `str`
        """
    )
    
    media_type = PlaceHolder(
        '',
        """
        Returns the icon's media type.
        
        Returns
        -------
        media_type : `str`
        """
    )
    
    def __repr__(self):
        """Returns the icon details' representation."""
        return f'<{self.__class__.__name__}>'
        

class IconDetailsPreinstanced(IconDetailsBase):
    """
    Represents details about a preinstanced icon type.
    
    Attributes
    ----------
    allowed_postfixes : `None`, `frozenset` of `str`
        The allowed postfixes.
    default_postfix : `str`
        Default postfix used when building an url with the icon.
    prefix : `str`
        Prefix used when building an url with the icon.
    """
    __slots__ = ('allowed_postfixes', 'default_postfix', 'prefix')
    
    def __init__(self, allowed_postfixes, default_postfix, prefix):
        """
        Creates a new icon type detail for storing information for a preinstanced icon type.
        
        Parameters
        ----------
        allowed_postfixes : `None`, `frozenset` of `str`
            The allowed postfixes.
        default_postfix : `str`
            Default postfix used when building an url with the icon.
        prefix : `str`
            Prefix used when building an url with the icon.
        """
        self.allowed_postfixes = allowed_postfixes
        self.default_postfix = default_postfix
        self.prefix = prefix
    
    
    @copy_docs(IconDetailsBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' allowed_postfixes = ')
        repr_parts.append(repr(self.allowed_postfixes))
        
        repr_parts.append(', default_postfix = ')
        repr_parts.append(repr(self.default_postfix))
        
        repr_parts.append(', prefix = ')
        repr_parts.append(repr(self.prefix))
        
        repr_parts.append('>')
        return ''.join(repr_parts)


class IconDetailsCustom(IconDetailsBase):
    """
    Represents details fo a custom icon type.
    
    Attributes
    ----------
    data : `None`, `bytes-like`
        Icon payload.
    media_type : `str`
        The icon's data's media type.
    """
    __slots__ = ('data', 'media_type')
    
    def __init__(self, data, media_type):
        """
        Creates a new custom icon type detail.
        
        Parameters
        ----------
        data : `None`, `bytes-like`
            The icon's raw data.
        media_type : `str`
            The icon's media type.
        """
        self.data = data
        self.media_type = media_type
    
    
    @copy_docs(IconDetailsBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' data[length] = ')
        repr_parts.append(repr(len(self.data)))
        
        repr_parts.append(', media_type = ')
        repr_parts.append(repr(self.media_type))
        
        repr_parts.append('>')
        return ''.join(repr_parts)


class IconType(PreinstancedBase):
    """
    Represents a Discord icon's type.
    
    Attributes
    ----------
    name : `str`
        The name of the icon type.
    value : `int`
        The identifier value the icon type.
    details : ``IconDetailsBase``
        Additional details describing the icon type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``IconType``) items
        Stores the predefined ``IconType``-s. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The icon types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the icon types.
    
    Every predefined icon type can be accessed as class attribute as well:
    
    +-----------------------+---------------+-------+-----------+-------------------+---------------------------------------+
    | Class attribute name  | Name          | Value | Prefix    | Default postfix   | Allowed Postfixes                     |
    +=======================+===============+=======+===========+===================+=======================================+
    | none                  | none          | 0     | `''`      | `''`              | `None`                                |
    +-----------------------+---------------+-------+-----------+-------------------|---------------------------------------+
    | static                | static        | 1     | `''`      | `'png'`           | `'jpg', 'jpeg', 'png', 'webp'`        |
    +-----------------------+---------------+-------+-----------+-------------------|---------------------------------------+
    | animated              | animated      | 2     | `'a_'`    | `'gif'`           | `'jpg', 'jpeg', 'png', 'webp', 'gif'` |
    +-----------------------+---------------+-------+-----------+-------------------+---------------------------------------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ('details',)
    
    
    @classmethod
    @copy_docs(PreinstancedBase._from_value)
    def _from_value(cls, value):
        raise NotImplementedError
    
    
    def __init__(self, value, name, prefix, default_postfix, allowed_postfixes):
        """
        Creates a new icon type with the given parameters and stores it at the type's `.INSTANCES`.
        
        Parameters
        ----------
        value : `str`
            The unique identifier of the icon type.
        name : `str`
            The icon type's name
        prefix : `str`
            Prefix used when building an url with the icon.
        default_postfix : `str`
            Default postfix used when building an url with the icon.
        allowed_postfixes : `None`, `frozenset` of `str`
            The allowed postfixes.
        """
        details = IconDetailsPreinstanced(allowed_postfixes, default_postfix, prefix)
        
        self.details = details
        self.name = name
        self.value = value
        
        self.INSTANCES[value] = self
    
    
    @classmethod
    def from_data(cls, data, name = 'icon'):
        """
        Creates a custom icon type holding actual raw data.
        
        Parameters
        ----------
        data : `bytes-like`
            The icon's raw data.
        name : `str` = `icon`, Optional
            The icon's name.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If `data` is not `bytes-like`.
        """
        if data is None:
            media_type = ''
        
        else:
            if not isinstance(data, (bytes, bytearray, memoryview)):
                raise TypeError(
                    f'`{name}` can be `None`, `bytes-like`, got {data.__class__.__name__}; {reprlib.repr(data)}'
                )
            
            media_type = get_image_media_type(data)
        
        details = IconDetailsCustom(data, media_type)
        
        
        self = PreinstancedBase.__new__(cls)
        self.details = details
        self.name = name
        self.value = -2
        return self
    
    
    def __bool__(self):
        """Returns whether the icon's type is set."""
        if (self.value > 0) or (self.data is not None):
            boolean = True
        else:
            boolean = False
        
        return boolean
    
    
    def __repr__(self):
        """Returns the icon detail's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' value = ')
        repr_parts.append(repr(self.value))
        
        repr_parts.append(', name = ')
        repr_parts.append(repr(self.name))
        
        repr_parts.append(', details = ')
        repr_parts.append(repr(self.details))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @property
    @copy_docs(IconDetailsBase.allowed_postfixes)
    def allowed_postfixes(self):
        return self.details.allowed_postfixes
    
    
    @property
    @copy_docs(IconDetailsBase.default_postfix)
    def default_postfix(self):
        return self.details.default_postfix
    
    
    @property
    @copy_docs(IconDetailsBase.prefix)
    def prefix(self):
        return self.details.prefix
    
    
    @property
    @copy_docs(IconDetailsBase.data)
    def data(self):
        return self.details.data
    
    
    @property
    def base_64_data(self):
        """
        Returns the icon's data in base 64 encoding.
        
        Returns
        -------
        data : `None`, `str`
        """
        data = self.data
        if data is not None:
            return ''.join(['data:', self.media_type, ';base64,', b64encode(data).decode('ascii')])
    
    
    @property
    @copy_docs(IconDetailsBase.media_type)
    def media_type(self):
        return self.details.media_type
    
    
    def allows_postfix(self, postfix):
        """
        Returns whether the icon type allows the given postfix.
        
        Parameters
        ----------
        postfix : `str`
            The postfix to check.
        
        Returns
        -------
        allows_postfix : `bool`
        """
        allowed_postfixes = self.allowed_postfixes
        if (allowed_postfixes is None):
            return False
        
        if (postfix not in allowed_postfixes):
            return False
        
        return True
    
    
    def can_create_url(self):
        """
        Returns whether it is possible to create url with the icon.
        
        Returns
        -------
        can_create_url : `bool`
        """
        return (self.allowed_postfixes is not None)
    
    
    none = P(0, 'none', '', '', None)
    static = P(1, 'static', '', 'png', frozenset(('jpg', 'jpeg', 'png', 'webp')))
    animated = P(2, 'animated', 'a_', 'gif', frozenset(('jpg', 'jpeg', 'png', 'webp', 'gif')))


ICON_TYPE_NONE = IconType.none
ICON_TYPE_STATIC = IconType.static
ICON_TYPE_ANIMATED = IconType.animated


class Icon(RichAttributeErrorBaseType):
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
        Deprecated and will be removed in 2023 February. Please use ``.as_base_16_hash`` instead.
        """
        warnings.warn(
            (
                f'`{self.__name__}.as_base16_hash` is deprecated and will be removed in 2023 February.'
                f'Please use `.as_base_16_hash` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        return self.as_base_16_hash
    
    
    @property
    def as_base_16_hash(self):
        """
        Returns the discord side representation of the icon.
        
        Returns
        -------
        icon : `None`, `str`
        """
        icon_type = self.type
        if icon_type is ICON_TYPE_NONE:
            icon = None
        
        else:
            icon = self.hash.__format__('0>32x')
            prefix = icon_type.prefix
            if prefix:
                icon = prefix + icon
        
        return icon
    
    
    @property
    def as_base_64_data(self):
        """
        Returns the base 64 version of the icon if applicable.
        
        Returns
        -------
        icon : `None`, `str`
        """
        return self.type.base_64_data
    
    
    hash_info_width = sys.hash_info.width
    if hash_info_width == 32:
        def __hash__(self):
            """Returns the icon's hash."""
            icon_type = self.type
            if icon_type is ICON_TYPE_NONE:
                hash_value = 0
            else:
                icon_hash = self.hash
                hash_value = (
                    (icon_hash >> 96) ^
                    ((icon_hash >> 64) & ((1 << 32) - 1)) ^
                    ((icon_hash >> 32) & ((1 << 32) - 1)) ^
                    (icon_hash & ((1 << 32) - 1))
                )
                
                if icon_type is ICON_TYPE_ANIMATED:
                    hash_value ^= ((1 << 32) - 1)
            
            return hash_value
    
    
    elif hash_info_width == 64:
        def __hash__(self):
            """Returns the icon's hash."""
            icon_type = self.type
            if icon_type is ICON_TYPE_NONE:
                hash_value = 0
            else:
                icon_hash = self.hash
                hash_value = (icon_hash >> 64) ^ (icon_hash & ((1 << 64) - 1))
                if icon_type is ICON_TYPE_ANIMATED:
                    hash_value ^= ((1 << 64) - 1)
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
                    hash_value ^= ((1 << 128) - 1)
            
            return hash_value
    
    del hash_info_width
    
    
    def __eq__(self, other):
        """Returns whether the two icons are equal."""
        if other is None:
            if self.type is not ICON_TYPE_NONE:
                return False
            
            if self.hash:
                return False
            
            return True
        
        elif type(self) is type(other):
            # Use `==` to compare value at the case of custom icons.
            if self.type != other.type:
                return False
            
            if self.hash != other.hash:
                return False
            
            return True
        
        elif isinstance(other, tuple):
            if len(other) != 2:
                return NotImplemented
            
            other_type, other_hash = other
            if not isinstance(other_type, IconType):
                return NotImplemented
            
            if not isinstance(other_hash, int):
                return NotImplemented
            
            if self.type != other_type:
                return False
            
            if self.hash != other_hash:
                return False
            
            return True
        
        return NotImplemented
    
    
    def __repr__(self):
        """Returns the representation of the icon."""
        return f'{self.__class__.__name__}(type = ICON_TYPE_{self.type.name.upper()}, hash = {self.hash})'
    
    
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
        icon : `None`, `str`
            Discord icon hash.
        
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
        
        __doc__ = docs_property()
    
    __slots__ = ('internal_name', 'discord_side_name', 'added_instance_attributes', 'added_class_attributes')
    
    _compile_globals = {
        'ICON_TYPE_NONE': ICON_TYPE_NONE,
        'ICON_TYPE_STATIC': ICON_TYPE_STATIC,
        'ICON_TYPE_ANIMATED': ICON_TYPE_ANIMATED,
        'Icon': Icon,
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
        url_property : `None`, `function`
            A function what will be used as a property when accessing the icon' url.
        url_as_method : `None`, `function`
            A function what will be used a method when creating a formatted icon url.
        add_updater : `bool` = `True`, Optional
            Whether the icon slot should add updater methods to the class.
        
        Returns
        -------
        self : ``IconSlot``
        """
        added_instance_attribute_name_hash = internal_name + '_hash'
        added_internal_attribute_name_type = internal_name + '_type'
        
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
    
    
    def __get__(self, attribute, type_):
        """Returns self if called from class, meanwhile an ``Icon`` if called from an object."""
        if attribute is None:
            return self
        
        icon_type_name, icon_hash_name = self.added_instance_attributes
        icon_type = getattr(attribute, icon_type_name)
        icon_hash = getattr(attribute, icon_hash_name)
        return Icon(icon_type, icon_hash)
    
    
    def __set__(self, instance, icon):
        """Can't set attribute."""
        if (icon is None):
            icon_type = ICON_TYPE_NONE
            icon_hash = 0
        
        elif isinstance(icon, Icon):
            icon_type, icon_hash = icon
        
        else:
            raise TypeError(
                f'`{instance.__class__.__name__}.{self.internal_name}` can only be `None`, `{Icon.__name__}`, '
                f'got {icon.__class__.__name__}; {icon!r}.'
            )
        
        icon_type_name, icon_hash_name = self.added_instance_attributes
        setattr(instance, icon_type_name, icon_type)
        setattr(instance, icon_hash_name, icon_hash)
    
    
    def __delete__(self, instance):
        """Can't delete attribute."""
        raise AttributeError(
            f'Can\'t delete `{instance.__class__.__name__}.{self.internal_name}`.'
        )
    
    
    def validate_icon(self, icon, *, allow_data = False):
        """
        Validates the given icon data.
        
        Parameters
        ----------
        icon : `None`, `bytes`, `bytearray`, `memoryview`, ``Icon``, `str`
            The icon to validate.
        allow_data : `bool` = `False`, Optional (Keyword only)
            Whether data parsing is allowed.
        
        Returns
        -------
        icon : `None`, ``Icon``
            The validated icon.
        
        Raises
        ------
        TypeError
            If `icon` field's type is incorrect.
        ValueError
            if `icon` has unexpected media type.
        """
        if icon is None:
            return None
        
        if isinstance(icon, Icon):
            return icon
        
        if isinstance(icon, str):
            if icon.startswith('a_'):
                icon = icon[2:]
                icon_type = ICON_TYPE_ANIMATED
            else:
                icon_type = ICON_TYPE_STATIC
            icon_hash = int(icon, 16)
            
            return Icon(icon_type, icon_hash)
        
        if not allow_data:
            raise TypeError(
                f'`{self.internal_name}` can be passed as `None`, `{Icon.__name__}`, `str` '
                f'(or bytes-like if allowed), got {icon.__class__.__name__}; {reprlib.repr(icon)}.'
            )
        
        icon_type = IconType.from_data(icon)
        if icon_type and (not icon_type.media_type):
            raise ValueError(
                f'`{self.internal_name}` received unknown media type; Got {reprlib.repr(icon_type.data)}.'
            )
        
        icon_hash = 0
        
        return Icon(icon_type, icon_hash)
    
    
    def parse_data_from_keyword_parameters(self, keyword_parameters):
        """
        Parses data from keyword parameters.
        
        Parameters
        ----------
        keyword_parameters : `dict` of (`str`, `Any`) items
            Keyword parameters passed to parse the icon from.
        
        Returns
        -------
        icon : `None`, ``Icon``
            The parsed out icon.
        
        Raises
        ------
        TypeError
            If `icon` field's type is incorrect.
        ValueError
            if `icon` has unexpected media type.
        """
        try:
            icon = keyword_parameters.pop(self.internal_name)
        except KeyError:
            return None
        
        return self.validate_icon(icon, allow_data = True)
    
    
    def parse_from_keyword_parameters(self, keyword_parameters, *, allow_data = False):
        """
        Parses the icon out from the given keyword parameters.
        
        Parameters
        ----------
        keyword_parameters : `dict` of (`str`, `Any`) items
            Keyword parameters passed to parse the icon from.
        allow_data : `bool` = `False`, Optional (Keyword only)
            Whether data parsing is allowed.
        
        Returns
        -------
        icon : `None`, ``Icon``
            The parsed out icon.
        
        Raises
        ------
        TypeError
            If any of expected value's type is invalid.
        ValueError
            If any of the expected value's type is valid, but it's value is not.
        """
        icon_type_name, icon_hash_name = self.added_instance_attributes
        try:
            icon = keyword_parameters.pop(self.internal_name)
        except KeyError:
            try:
                icon_hash = keyword_parameters.pop(icon_hash_name)
            except KeyError:
                return None
            
            if type(icon_hash) is int:
                pass
            
            elif isinstance(icon_hash, int):
                icon_hash = int(icon_hash)
            
            else:
                raise TypeError(
                    f'`{icon_hash_name}` can be `int`, got {icon_hash.__class__.__name__}; {icon_hash!r}.'
                )
            
            if icon_hash < 0 or icon_hash > ((1 << 128) - 1):
                raise ValueError(
                    f'`{icon_hash_name}` cannot be negative or longer than 128 bits, got {icon_hash!r}.'
                )
            
            try:
                icon_type = keyword_parameters.pop(icon_type_name)
            except KeyError:
                if icon_hash == 0:
                    icon_type = ICON_TYPE_NONE
                else:
                    icon_type = ICON_TYPE_STATIC
            else:
                if (type(icon_type) is not IconType):
                    raise TypeError(
                        f'`{icon_type_name}` can be `{IconType.__name__}`, got '
                        f'{icon_type.__class__.__name__}; {icon_type!r}.'
                    )
                
                if (icon_type is ICON_TYPE_NONE) and icon_hash:
                    raise ValueError(
                        f'If `{icon_type_name}` is passed as `ICON_TYPE_NONE`, then `{icon_hash_name}` '
                        f'can be passed only as `0`, meanwhile got `{icon_hash}`.'
                    )
            
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
            
            elif allow_data and isinstance(icon, (bytes, bytearray, memoryview)):
                icon_type = IconType.from_data(icon)
                icon_hash = 0
            
            else:
                raise TypeError(
                    f'`{self.internal_name}` can be passed as `None`, `{Icon.__name__}`, `str` '
                    f'(or bytes-like if allowed), got {icon.__class__.__name__}; {reprlib.repr(icon)}.'
                )
        
        return Icon(icon_type, icon_hash)
    
    
    def preconvert(self, keyword_parameters, processable):
        """
        Used at preconverters to parse out from the passed keyword_parameters the icon of the entity.
        
        Parameters
        ----------
        keyword_parameters : `dict` of (`str`, `Any`) items
            Keyword parameters passed to the respective preconverter.
        processable : `list` of `tuple` (`str`, `Any`)
            A list of instance attributes which will be set when all the passed keyword_parameters are validated.
        
        Raises
        ------
        TypeError
            If any of expected value's type is invalid.
        ValueError
            If any of the expected value's type is valid, but it's value is not.
        """
        icon = self.parse_from_keyword_parameters(keyword_parameters)
        if (icon is None):
            return
        
        icon_type, icon_hash = icon
        icon_type_name, icon_hash_name = self.added_instance_attributes
        
        processable.append((icon_type_name, icon_type))
        processable.append((icon_hash_name, icon_hash))
    
    
    def put_into(self, icon, data, defaults, *, as_data = False):
        """
        Puts the icon into the given data.
        
        Parameters
        ----------
        icon : ``Icon``
            The icon to serialize.
        data : `dict` of (`str`, `Any`) items
            The data put the icon into.
        defaults : `bool`
            Whether the `icon`'s value should be put even if it is the default value.
        as_data : `bool` = `False`, Optional (Keyword only)
            Whether we want the icon is data or in hash form.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        if icon is None:
            field_value = None
        
        else:
            if as_data:
                field_value = icon.as_base_64_data
            else:
                field_value = icon.as_base_16_hash
        
        if defaults or (field_value is not None):
            data[self.discord_side_name] = field_value
        
        return data
