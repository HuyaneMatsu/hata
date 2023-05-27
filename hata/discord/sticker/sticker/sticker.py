__all__ = ('Sticker', )

import warnings

from ...bases import DiscordEntity
from ...core import GUILDS, STICKERS, STICKER_PACKS
from ...http import urls as module_urls
from ...precreate_helpers import process_precreate_parameters_and_raise_extra
from ...user import ZEROUSER
from ...utils import DATETIME_FORMAT_CODE

from .constants import SORT_VALUE_DEFAULT
from .fields import (
    parse_available, parse_description, parse_format, parse_guild_id, parse_id, parse_name, parse_pack_id,
    parse_sort_value, parse_tags, parse_type, parse_user, put_available_into, put_description_into, put_format_into,
    put_guild_id_into, put_id_into, put_name_into, put_pack_id_into, put_sort_value_into, put_tags_into, put_type_into,
    put_user_into, validate_available, validate_description, validate_format, validate_guild_id, validate_id,
    validate_name, validate_pack_id, validate_sort_value, validate_tags, validate_type, validate_user
)
from .preinstanced import StickerFormat, StickerType


PRECREATE_FIELDS = {
    'description': ('description', validate_description),
    'available': ('available', validate_available),
    'guild': ('guild_id', validate_guild_id),
    'guild_id': ('guild_id', validate_guild_id),
    'name': ('name', validate_name),
    'pack': ('pack_id', validate_pack_id),
    'pack_id': ('pack_id', validate_pack_id),
    'sticker_format': ('format', validate_format),
    'sticker_type': ('type', validate_type),
    'sort_value': ('sort_value', validate_sort_value),
    'tags': ('tags', validate_tags),
    'user': ('user', validate_user),
}

STICKER_TYPE_NONE = StickerType.none
STICKER_TYPE_STANDARD = StickerType.standard
STICKER_TYPE_GUILD = StickerType.guild


class Sticker(DiscordEntity, immortal = True):
    """
    Represents a ``Message``'s sticker.
    
    Attributes
    ----------
    available : `bool`
        Whether the sticker is available.
    description : `None`, `str`
        The sticker's description.
    format : ``StickerFormat``
        The sticker's format.
    guild_id : `int`
        The guild's identifier to what the sticker is bound to. Defaults to `0` if the sticker is not bound to any
        guild.
    id : `int`
        The unique identifier number of the sticker.
    name : `str`
        The sticker's name.
    pack_id : `int`
        The unique identifier number of the pack from the sticker is. Defaults to `0` if the sticker is not bound to
        any pack.
    sort_value : `int`
        Value used to sort the stickers.
    tags : None`, `frozenset` of `str`
        Tags of the sticker if applicable.
    type : ``StickerType``
        The sticker's type.
    user : ``ClientUserBase``
        The user who uploaded the sticker. Defaults to ``ZEROUSER``.
    """
    __slots__ = (
        'available', 'description', 'format', 'guild_id', 'name', 'pack_id', 'sort_value', 'tags', 'type', 'user'
    )
    
    def __new__(
        cls,
        *,
        available = ...,
        description = ...,
        name = ...,
        pack_id = ...,
        sort_value = ...,
        sticker_format = ...,
        sticker_type = ...,
        tags = ...,
        user = ...,
    ):
        """
        Creates a partial sticker with the given fields.
        
        Parameters
        ----------
        available : `bool`, Optional (Keyword only)
            Whether the sticker is available.
        description : `None`, `str`, Optional (Keyword only)
            The sticker's description.
        name : `str`, Optional (Keyword only)
            The sticker's name.
        pack_id : `int`, ``StickerPack``, Optional (Keyword only)
            The unique identifier number of the pack from the sticker is.
        sort_value : `int`, Optional (Keyword only)
            Value used to sort the stickers.
        sticker_format : ``StickerFormat``, `int`, Optional (Keyword only)
            The sticker's format.
        sticker_type : ``StickerType``, `int`, Optional (Keyword only)
            The sticker's type.
        tags : None`, `iterable` of `str`, Optional (Keyword only)
            Tags of the sticker if applicable.
        user : ``ClientUserBase``, Optional (Keyword only)
            The user who uploaded the sticker.
        
        Raises
        ------
        TypeError
            - A parameter's type is incorrect.
        ValueError
            - A parameter's value is incorrect.
        """
        # available
        if available is ...:
            available = True
        else:
            available = validate_available(available)
        
        # description
        if description is ...:
            description = None
        else:
            description = validate_description(description)
        
        # name
        if name is ...:
            name = ''
        else:
            name = validate_name(name)
        
        # pack_id
        if pack_id is ...:
            pack_id = 0
        else:
            pack_id = validate_pack_id(pack_id)
        
        # sort_value
        if sort_value is ...:
            sort_value = SORT_VALUE_DEFAULT
        else:
            sort_value = validate_sort_value(sort_value)
        
        # sticker_format
        if sticker_format is ...:
            sticker_format = StickerFormat.none
        else:
            sticker_format = validate_format(sticker_format)
        
        # sticker_type
        if sticker_type is ...:
            sticker_type = StickerType.none
        else:
            sticker_type = validate_type(sticker_type)
        
        # tags
        if tags is ...:
            tags = None
        else:
            tags = validate_tags(tags)
        
        # user
        if user is ...:
            user = ZEROUSER
        else:
            user = validate_user(user)
    
        # Construct
        self = object.__new__(cls)
        self.available = available
        self.description = description
        self.format = sticker_format
        self.guild_id = 0
        self.id = 0
        self.name = name
        self.pack_id = pack_id
        self.sort_value = sort_value
        self.tags = tags
        self.type = sticker_type
        self.user = user
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new sticker from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Sticker data.
        
        Returns
        -------
        sticker : `instance<cls>`
        """
        sticker_id = parse_id(data)
        
        try:
            self = STICKERS[sticker_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = sticker_id
            self._set_attributes(data)
            
            STICKERS[sticker_id] = self
            
        else:
            if not self.partial:
                # Set user if received
                user = parse_user(data)
                if user is not ZEROUSER:
                    self.user = user
                
                return self
            
            self._set_attributes(data)
        
        # Do not register, since that ruins `client.events.sticker__create` after a `client.sticker_create` call.
        # guild_id = self.guild_id
        # if guild_id:
        #     try:
        #         guild = GUILDS[guild_id]
        #     except KeyError:
        #         pass
        #     else:
        #         guild.stickers[sticker_id] = self
        
        return self
    
    
    @classmethod
    def from_partial_data(cls, data):
        """
        Creates a sticker from the given partial sticker data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Sticker data.
        
        Returns
        -------
        sticker : `instance<cls>`
        """
        warnings.warn(
            (
                f'`{cls.__name__}.from_partial_data` is deprecate and will be removed in 2023 December. '
                f'Please use `create_partial_sticker_data` instead.'
            ),
            FutureWarning,
        )
        
        sticker_id = parse_id(data)
        
        try:
            self = STICKERS[sticker_id]
        except KeyError:
            self = cls._create_empty(sticker_id)
            STICKERS[sticker_id] = self
        else:
            if not self.partial:
                return self
        
        self.format = parse_format(data)
        self.name = parse_name(data)
        
        return self
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Converts the sticker to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        
        put_description_into(self.description, data, defaults)
        put_name_into(self.name, data, defaults)
        put_tags_into(self.tags, data, defaults)
        
        if include_internals:
            put_available_into(self.available, data, defaults)
            put_sort_value_into(self.sort_value, data, defaults)
            put_format_into(self.format, data, defaults)
            put_guild_id_into(self.guild_id, data, defaults)
            put_id_into(self.id, data, defaults)
            put_pack_id_into(self.pack_id, data, defaults)
            put_sort_value_into(self.sort_value, data, defaults)
            put_type_into(self.type, data, defaults)
            put_user_into(self.user, data, defaults, include_internals = include_internals)
        
        return data
    

    def to_partial_data(self):
        """
        Tries to convert the sticker to a json serializable dictionary representing a partial sticker.
        
        Returns
        -------
        data : `dict` of (`str`, `object`)
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.to_partial_data` is deprecate and will be removed in 2023 December. '
                f'Please use `create_partial_sticker_data` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        data = {}
        put_format_into(self.format, data, True)
        put_id_into(self.id, data, True)
        put_name_into(self.name, data, True)
        return data
    

    @classmethod
    def precreate(cls, sticker_id, **keyword_parameters):
        """
        Precreates the sticker by creating a partial one with the given parameters. When the sticker is loaded
        the precreated one will be picked up. If an already existing sticker would be precreated, returns that
        instead and updates that only, if that is partial.
        
        Parameters
        ----------
        sticker_id : `int`
            The sticker's identifier.
        **keyword_parameters : keyword parameters
            Additional predefined attributes for the sticker.
        
        Other Parameters
        ----------------
        available : `bool`, Optional (Keyword only)
            Whether the sticker is available.
        description : `None`, `str`, Optional (Keyword only)
            The sticker's description.
        guild : ``Guild``, `int`, Optional (Keyword only)
            Alternative for `guild_id`.
        guild_id : ``Guild``, `int`, Optional (Keyword only)
             The sticker's guild's identifier.
        name : `str`, Optional (Keyword only)
            The sticker's name.
        pack : `int`, ``StickerPack``, Optional (Keyword only)
            Alternative for `pack_id`.
        pack_id : `int`, ``StickerPack``, Optional (Keyword only)
            The unique identifier number of the pack from the sticker is.
        sort_value : `int`, Optional (Keyword only)
            Value used to sort the stickers.
        sticker_format : ``StickerFormat``, `int`, Optional (Keyword only)
            The sticker's format.
        sticker_type : ``StickerType``, `int`, Optional (Keyword only)
            The sticker's type.
        tags : None`, `iterable` of `str`, Optional (Keyword only)
            Tags of the sticker if applicable.
        user : ``ClientUserBase``, Optional (Keyword only)
            The user who uploaded the sticker.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - Extra parameter(s) given.
            - A parameter's type is incorrect.
        ValueError
            - A parameter's value is incorrect.
        """
        sticker_id = validate_id(sticker_id)

        if keyword_parameters:
            processed = process_precreate_parameters_and_raise_extra(keyword_parameters, PRECREATE_FIELDS)
        else:
            processed = None
        
        try:
            self = STICKERS[sticker_id]
        except KeyError:
            self = cls._create_empty(sticker_id)
            STICKERS[sticker_id] = self
        else:
            if not self.partial:
                return self
        
        if (processed is not None):
            for name, value in processed:
                setattr(self, name, value)
        
        return self
    
    
    def __repr__(self):
        """Returns the sticker's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        sticker_id = self.id
        if sticker_id:
            repr_parts.append(' id = ')
            repr_parts.append(repr(self.id))
            repr_parts.append(',')
        
        repr_parts.append(' name = ')
        repr_parts.append(repr(self.name))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    

    def __format__(self, code):
        """
        Formats the sticker in a format string.
        
        Parameters
        ----------
        code : `str`
            The option on based the result will be formatted.
        
        Returns
        -------
        sticker : `str`
        
        Raises
        ------
        ValueError
            Unknown format code.
        
        Examples
        --------
        ```py
        >>> from hata import Sticker, now_as_id
        >>> sticker = Sticker.precreate(now_as_id(), name = 'nice')
        >>> sticker
        <Sticker id = 712359434843586560, name = 'nice'>
        >>> # no code returns the sticker's name.
        >>> f'{sticker}'
        'nice'
        >>> # 'c' stands for created at.
        >>> f'{sticker:c}'
        '2020.05.19-17:42:04'
        ```
        """
        if not code:
            return self.name
        
        if code == 'c':
            return format(self.created_at, DATETIME_FORMAT_CODE)
        
        raise ValueError(
            f'Unknown format code {code!r} for {self.__class__.__name__}; {self!r}. '
            f'Available format codes: {""!r}, {"c"!r}.'
        )
    
    def __hash__(self):
        """Returns the sticker's hash."""
        sticker_id = self.id
        if sticker_id:
            return sticker_id
        
        return self._get_hash_partial()
    
    
    def _get_hash_partial(self):
        """
        Returns a partial sticker's hash value.
        
        Returns
        -------
        hash_value : `int`
        """
        hash_value = 0
        
        # available
        hash_value ^= self.available
        
        # description
        description = self.description
        if (description is not None):
            hash_value ^= hash(description)
        
        # format
        hash_value ^= self.format.value << 1
        
        # name
        name = self.name
        if (description is None) or (description != name):
            hash_value ^= hash(name)
        
        # pack_id
        hash_value ^= self.pack_id
        
        # sort_value
        hash_value ^= self.sort_value << 5
        
        # tags
        tags = self.tags
        if (tags is not None):
            hash_value ^= len(tags) << 9
            
            for tag in tags:
                hash_value ^= hash(tag)
        
        # type
        hash_value ^= self.type.value << 13
        
        # user
        hash_value ^= hash(self.user)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two stickers are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def __ne__(self, other):
        """Returns whether the two stickers are not equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return not self._is_equal_same_type(other)
    
    
    def __gt__(self, other):
        """Returns whether self is greater than other."""
        if type(self) is not type(other):
            return NotImplemented
        
        self_sort_value = self.sort_value
        other_sort_value = other.sort_value
        if self_sort_value > other_sort_value:
            return True
        
        if self_sort_value == other_sort_value:
            if self.id > other.id:
                return True
        
        return False
    
    def __ge__(self, other):
        """Returns whether self is greater or equal to other."""
        if type(self) is not type(other):
            return NotImplemented
        
        self_sort_value = self.sort_value
        other_sort_value = other.sort_value
        if self_sort_value > other_sort_value:
            return True
        
        if self_sort_value == other_sort_value:
            if self.id > other.id:
                return True
        
        return self._is_equal_same_type(other)
    
    
    def __le__(self, other):
        """Returns whether self is less or equal to other."""
        if type(self) is not type(other):
            return NotImplemented
        
        self_sort_value = self.sort_value
        other_sort_value = other.sort_value
        if self_sort_value < other_sort_value:
            return True
        
        if self_sort_value == other_sort_value:
            if self.id < other.id:
                return True
        
        return self._is_equal_same_type(other)
    
    
    def __lt__(self, other):
        """Returns whether self is less than other."""
        if type(self) is not type(other):
            return NotImplemented
        
        self_sort_value = self.sort_value
        other_sort_value = other.sort_value
        if self_sort_value < other_sort_value:
            return True
        
        if self_sort_value == other_sort_value:
            if self.id < other.id:
                return True
        
        return False
    
    
    def _is_equal_same_type(self, other):
        """
        Returns whether the two stickers are equal. `self` and `other` must be the same type.
        
        Parameters
        ----------
        other : `instance<type<self>>`
            The other sticker.
        
        Returns
        -------
        is_equal : `bool`
        """
        self_id = self.id
        other_id = other.id
        if (self_id and other_id):
            return self_id == other_id
        
        # available
        if (self.available != other.available):
            return False
        
        # description
        if (self.description != other.description):
            return False
        
        # format
        if (self.format is not other.format):
            return False
        
        # guild_id
        # Skip | non-partial
        
        # name
        if (self.name != other.name):
            return False
        
        # pack_id
        if (self.pack_id != other.pack_id):
            return False
        
        # sort_value
        if (self.sort_value != other.sort_value):
            return False
        
        # tags
        if (self.tags != other.tags):
            return False
        
        # type
        if (self.type is not other.type):
            return False
        
        # user
        if (self.user != other.user):
            return False
        
        return True
    

    @property
    def partial(self):
        """
        Returns whether the sticker is partial.
        
        Returns
        -------
        partial : `bool`
        """
        sticker_type = self.type
        if sticker_type is STICKER_TYPE_NONE:
            return True
        
        sticker_id = self.id
        if not sticker_id:
            return True
        
        if sticker_type is STICKER_TYPE_GUILD:
            guild_id = self.guild_id
            if not guild_id:
                return True
            
            try:
                guild = GUILDS[guild_id]
            except KeyError:
                return True
            
            if self.id not in guild.stickers:
                return True
            
            return guild.partial
        
        if sticker_type is STICKER_TYPE_STANDARD:
            pack_id = self.pack_id
            if not pack_id:
                return True
            
            try:
                sticker_pack = STICKER_PACKS[pack_id]
            except KeyError:
                return True
            
            return (not sticker_pack.has_sticker(self))
        
        return True
    
    
    url = property(module_urls.sticker_url)
    url_as = module_urls.sticker_url_as
    
    
    def _set_attributes(self, data):
        """
        Sets the attributes of the sticker from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Sticker data.
        """
        self.format = parse_format(data)
        self.guild_id = parse_guild_id(data)
        self.pack_id = parse_pack_id(data)
        self.type = parse_type(data)
        self.user = ZEROUSER
        
        self._update_attributes(data)
    
    
    def _update_attributes(self, data):
        """
        Updates the stickers with the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Sticker data.
        """
        self.available = parse_available(data)
        self.description = parse_description(data)
        self.name = parse_name(data)
        self.sort_value = parse_sort_value(data)
        self.tags = parse_tags(data)
        
        # set user if applicable
        user = parse_user(data)
        if user is not ZEROUSER:
            self.user = user
    
    
    def _difference_update_attributes(self, data):
        """
        Updates the sticker with the given data and returns the changed attributes in `attribute-name` - `old-value`
        relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Sticker data.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `object`) items
            All item in the returned dictionary is optional.
            
            +-----------------------+-----------------------------------+
            | Keys                  | Values                            |
            +=======================+===================================+
            | available             | `bool`                            |
            +-----------------------+-----------------------------------+
            | description           | `None`, `str`                     |
            +-----------------------+-----------------------------------+
            | name                  | `str`                             |
            +-----------------------+-----------------------------------+
            | sort_value            | `int`                             |
            +-----------------------+-----------------------------------+
            | tags                  | `None`  or `frozenset` of `str`   |
            +-----------------------+-----------------------------------+
        """
        old_attributes = {}
        
        available = parse_available(data)
        if self.available != available:
            old_attributes['available'] = self.available
            self.available = available
        
        description = parse_description(data)
        if description != self.description:
            old_attributes['description'] = self.description
            self.description = description
        
        name = parse_name(data)
        if name != self.name:
            old_attributes['name'] = self.name
            self.name = name
        
        sort_value = parse_sort_value(data)
        if sort_value != self.sort_value:
            old_attributes['sort_value'] = self.sort_value
            self.sort_value = sort_value
        
        tags = parse_tags(data)
        if tags != self.tags:
            old_attributes['tags'] = self.tags
            self.tags = tags
        
        # set user if applicable
        user = parse_user(data)
        if user is not ZEROUSER:
            self.user = user
        
        return old_attributes
    
    
    @classmethod
    def _create_empty(cls, sticker_id):
        """
        Creates an empty sticker with the given identifier.
        
        Parameters
        ----------
        sticker_id : `int`
            The sticker's identifier.
        
        Returns
        -------
        self : `instance<cls>`
            The created sticker.
        """
        self = object.__new__(cls)
        self.id = sticker_id
        self.available = True
        self.description = None
        self.format = StickerFormat.none
        self.guild_id = 0
        self.name = ''
        self.pack_id = 0
        self.sort_value = SORT_VALUE_DEFAULT
        self.tags = None
        self.type = StickerType.none
        self.user = ZEROUSER
        return self
    
    
    def copy(self):
        """
        Copies the sticker returning a partial one.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.available = self.available
        new.description = self.description
        new.format = self.format
        new.guild_id = 0
        new.id = 0
        new.name = self.name
        new.pack_id = self.pack_id
        new.sort_value = self.sort_value
        tags = self.tags
        if (tags is not None):
            tags = frozenset(iter(tags))
        new.tags = tags
        new.type = self.type
        new.user = self.user
        return new
    
    
    def copy_with(
        self,
        *,
        available = ...,
        description = ...,
        name = ...,
        pack_id = ...,
        sort_value = ...,
        sticker_format = ...,
        sticker_type = ...,
        tags = ...,
        user = ...,
    ):
        """
        Copies the sticker with the given fields.
        
        Parameters
        ----------
        available : `bool`, Optional (Keyword only)
            Whether the sticker is available.
        description : `None`, `str`, Optional (Keyword only)
            The sticker's description.
        name : `str`, Optional (Keyword only)
            The sticker's name.
        pack_id : `int`, ``StickerPack``, Optional (Keyword only)
            The unique identifier number of the pack from the sticker is.
        sort_value : `int`, Optional (Keyword only)
            Value used to sort the stickers.
        sticker_format : ``StickerFormat``, `int`, Optional (Keyword only)
            The sticker's format.
        sticker_type : ``StickerType``, `int`, Optional (Keyword only)
            The sticker's type.
        tags : None`, `iterable` of `str`, Optional (Keyword only)
            Tags of the sticker if applicable.
        user : ``ClientUserBase``, Optional (Keyword only)
            The user who uploaded the sticker.
        
        Raises
        ------
        TypeError
            - A parameter's type is incorrect.
        ValueError
            - A parameter's value is incorrect.
        """
        # available
        if available is ...:
            available = self.available
        else:
            available = validate_available(available)
        
        # description
        if description is ...:
            description = self.description
        else:
            description = validate_description(description)
        
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # pack_id
        if pack_id is ...:
            pack_id = self.pack_id
        else:
            pack_id = validate_pack_id(pack_id)
        
        # sort_value
        if sort_value is ...:
            sort_value = self.sort_value
        else:
            sort_value = validate_sort_value(sort_value)
        
        # sticker_format
        if sticker_format is ...:
            sticker_format = self.format
        else:
            sticker_format = validate_format(sticker_format)
        
        # sticker_type
        if sticker_type is ...:
            sticker_type = self.type
        else:
            sticker_type = validate_type(sticker_type)
        
        # tags
        if tags is ...:
            tags = self.tags
            if (tags is not None):
                tags = frozenset(iter(tags))
        else:
            tags = validate_tags(tags)
        
        # user
        if user is ...:
            user = self.user
        else:
            user = validate_user(user)
        
        # Construct
        new = object.__new__(type(self))
        new.available = available
        new.description = description
        new.format = sticker_format
        new.guild_id = 0
        new.id = 0
        new.name = name
        new.pack_id = pack_id
        new.sort_value = sort_value
        new.tags = tags
        new.type = sticker_type
        new.user = user
        return new
    
    
    @property
    def guild(self):
        """
        Returns the sticker's guild if cached.
        
        Returns
        -------
        guild : ``Guild``
        """
        guild_id = self.guild_id
        if guild_id:
            return GUILDS.get(guild_id, None)
    
    
    def iter_tags(self):
        """
        Iterates over the tags of the sticker.
        
        This method is an iterable generator.
        
        Yields
        ------
        tag : `str`
        """
        tags = self.tags
        if (tags is not None):
            yield from tags
    
    
    def has_tag(self, tag):
        """
        Returns whether the sticker has the given tag.
        
        Parameters
        ----------
        tag : `str`
            The tag to check for.
        
        Returns
        -------
        has_tag : `bool`
        """
        tags = self.tags
        if (tags is None):
            return False
        
        return (tag in self.tags)
