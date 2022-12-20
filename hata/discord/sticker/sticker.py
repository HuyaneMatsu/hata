__all__ = ('Sticker', )

from scarletio import include

from ..bases import DiscordEntity
from ..bases import instance_or_id_to_instance
from ..core import GUILDS, STICKERS, STICKER_PACKS
from ..http import urls as module_urls
from ..preconverters import (
    preconvert_bool, preconvert_int, preconvert_iterable_of_str, preconvert_preinstanced_type, preconvert_snowflake,
    preconvert_str
)
from ..user import User, ZEROUSER

from .preinstanced import StickerFormat, StickerType


Client = include('Client')

DEFAULT_SORT_VALUE = 0


class Sticker(DiscordEntity, immortal=True):
    """
    Represents a ``Message``'s sticker.
    
    Attributes
    ----------
    id : `int`
        The unique identifier number of the sticker.
    available : `bool`
        Whether the sticker is available.
    description : `None`, `str`
        The sticker's description.
    format : ``StickerFormat``
        The sticker's format.
    guild_id : `int`
        The guild's identifier to what the sticker is bound to. Defaults to `0` if the sticker is not bound to any
        guild.
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
        The user who uploaded the emoji. Defaults to ``ZEROUSER``.
    """
    __slots__ = (
        'available', 'description', 'format', 'guild_id', 'name', 'pack_id', 'sort_value', 'tags', 'type', 'user'
    )
    
    def __new__(cls, data):
        """
        Creates a new ``Sticker`` from the received data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Sticker data.
        """
        sticker_id = int(data['id'])
        
        try:
            self = STICKERS[sticker_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = sticker_id
            STICKERS[sticker_id] = self
            
            try:
                user_data = data['user']
            except KeyError:
                user = ZEROUSER
            else:
                user = User.from_data(user_data)
            self.user = user
        
        else:
            if not self.partial:
                if self.user is ZEROUSER:
                    try:
                        user_data = data['user']
                    except KeyError:
                        pass
                    else:
                        self.user = User.from_data(user_data)
                
                return self
        
        self._update_from_partial(data)
        
        return self
    
    
    @classmethod
    def _create_partial(cls, data):
        """
        Creates a sticker from the given partial ``Sticker`` data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Sticker data.
        
        Returns
        -------
        self : ``Sticker``
        """
        sticker_id = int(data['id'])
        
        try:
            self = STICKERS[sticker_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = sticker_id
            STICKERS[sticker_id] = self
            
            self.available = True
            self.description = None
            self.guild_id = 0
            self.pack_id = 0
            self.sort_value = DEFAULT_SORT_VALUE
            self.tags = None
            self.type = StickerType.none
            self.user = ZEROUSER
        else:
            if not self.partial:
                return self
        
        self.format = StickerFormat.get(data.get('format_type', 0))
        self.name = data['name']
        
        return self
    
    
    def to_partial_data(self):
        """
        Tries to convert the sticker to a json serializable dictionary representing a partial sticker.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`)
        """
        return {
            'id': str(self.id),
            'name': self.name,
            'format_type': self.format.value,
        }
    
        
    def _update_from_partial(self, data):
        """
        Updates a partial sticker with to not partial from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Sticker data.
        """
        self.format = StickerFormat.get(data.get('format_type', 0))
        
        pack_id = data.get('pack_id', None)
        if pack_id is None:
            pack_id = 0
        else:
            pack_id = int(pack_id)
        self.pack_id = pack_id
        
        guild_id = data.get('guild_id', None)
        if guild_id is None:
            guild_id = 0
        else:
            guild_id = int(guild_id)
        self.guild_id = guild_id
        
        self.type = StickerType.get(data.get('type', 0))
        
        self._update_attributes(data)
    
    
    def _update_attributes(self, data):
        """
        Updates the stickers with the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Sticker data.
        """
        description = data.get('description', None)
        if (description is not None) and (not description):
            description = None
        self.description = description
        
        self.name = data['name']
        self.sort_value = data.get('sort_value', DEFAULT_SORT_VALUE)
        
        tags = data.get('tags', None)
        if (tags is None) or (not tags):
            tags = None
        else:
            tags = frozenset(tags.split(', '))
        self.tags = tags
        
        self.available = data.get('available', True)
        
        # user
        try:
            user_data = data['user']
        except KeyError:
            pass
        else:
            self.user = User.from_data(user_data)
    
    
    def _difference_update_attributes(self, data):
        """
        Updates the sticker with the given data and returns the changed attributes in `attribute-name` - `old-value`
        relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Sticker data.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `Any`) items
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
        
        description = data.get('description', None)
        if (description is not None) and (not description):
            description = None
        if description != self.description:
            old_attributes['description'] = self.description
            self.description = description
        
        name = data['name']
        if name != self.name:
            old_attributes['name'] = self.name
            self.name = name
        
        sort_value = data.get('sort_value', DEFAULT_SORT_VALUE)
        if sort_value != self.sort_value:
            old_attributes['sort_value'] = self.sort_value
            self.sort_value = sort_value
        
        tags = data.get('tags', None)
        if (tags is None) or (not tags):
            tags = None
        else:
            tags = frozenset(tags.split(', '))
        if tags != self.tags:
            old_attributes['tags'] = self.tags
            self.tags = tags
        
        available = data.get('available', True)
        if self.available != available:
            old_attributes['available'] = self.available
            self.available = available
        
        return old_attributes
    
    
    def __repr__(self):
        """Returns the sticker's representation."""
        return f'<{self.__class__.__name__} id={self.id!r}, name={self.name!r}>'
    
    url = property(module_urls.sticker_url)
    url_as = module_urls.sticker_url_as
    
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
            if self.id >= other.id:
                return True
        
        return False
    
    def __le__(self, other):
        """Returns whether self is less or equal to other."""
        if type(self) is not type(other):
            return NotImplemented
        
        self_sort_value = self.sort_value
        other_sort_value = other.sort_value
        if self_sort_value < other_sort_value:
            return True
        
        if self_sort_value == other_sort_value:
            if self.id <= other.id:
                return True
        
        return False
    
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
    
    @property
    def partial(self):
        """
        Returns whether the sticker is partial.
        
        Returns
        -------
        partial : `bool`
        """
        pack_id = self.pack_id
        if pack_id:
            if pack_id in STICKER_PACKS:
                return False
            
            return True
        
        guild_id = self.guild_id
        if guild_id:
            try:
                guild = GUILDS[guild_id]
            except KeyError:
                return False
            else:
                return guild.partial
        
        return True
    
    
    @classmethod
    def precreate(cls, sticker_id, **kwargs):
        """
        Precreates the sticker by creating a partial one with the given parameters. When the sticker is loaded
        the precreated one will be picked up. If an already existing sticker would be precreated, returns that
        instead and updates that only, if that is partial.
        
        Parameters
        ----------
        sticker_id : `snowflake`
            The sticker's id.
        **kwargs : keyword parameters
            Additional predefined attributes for the sticker.
        
        Other Parameters
        ----------------
        available : `bool`, Optional (Keyword only)
             The sticker's ``.available``.
        description : `str`, Optional (Keyword only)
            The sticker's ``.name``. It's length can be in range [0:1024]
        format : ``StickerFormat``, Optional (Keyword only)
            The sticker's ``.format``.
        guild_id : `int`, Optional (Keyword only)
            The sticker's ``.guild_id``.
        name : `str`, Optional (Keyword only)
            The sticker's ``.name``. It's length can be in range [0:32].
        pack_id : `int`, Optional (Keyword only)
            The sticker's ``.pack_id``.
        sort_value : `int`, Optional (Keyword only)
            The sticker's ``.sort_value``.
        tags : `None`, `iterable` of `str`, Optional (Keyword only)
            The sticker's ``.tags``.
        type : ``StickerType``, Optional (Keyword only)
            The sticker's ``.type``.
        user : ``ClientUserBase``, Optional (Keyword only)
            The sticker's ``.user``.
        
        Returns
        -------
        self : ``Sticker``
        
        Raises
        ------
        TypeError
            If any parameter's type is bad or if unexpected parameter is passed.
        ValueError
            If an parameter's type is good, but it's value is unacceptable.
        """
        sticker_id = preconvert_snowflake(sticker_id, 'sticker_id')
        
        if kwargs:
            processable = []
            # There might be new bool fields coming out.
            for attribute_name in ('available',):
                try:
                    attribute_value = kwargs.pop(attribute_name)
                except KeyError:
                    pass
                else:
                    animated = preconvert_bool(attribute_value, attribute_name)
                    processable.append((attribute_name, animated))
            
            for attribute_name, lower_limit, upper_limit in (
                ('description', 0, 1024),
                ('name', 2, 32),
            ):
                
                try:
                    attribute_value = kwargs.pop('attribute_name')
                except KeyError:
                    pass
                else:
                    attribute_value = preconvert_str(attribute_value, attribute_name, lower_limit, upper_limit)
                    processable.append((attribute_name, attribute_value))
            
            for attribute_name, preinstanced_type in (
                ('format', StickerFormat),
                ('type', StickerType),
            ):
                try:
                    attribute_value = kwargs.pop(attribute_name)
                except KeyError:
                    pass
                else:
                    attribute_value = preconvert_preinstanced_type(attribute_value, attribute_name, preinstanced_type)
                    processable.append((attribute_name, attribute_value))
            
            for attribute_name in ('guild_id', 'pack_id'):
                try:
                    attribute_value = kwargs.pop(attribute_name)
                except KeyError:
                    pass
                else:
                    attribute_value = preconvert_snowflake(attribute_value, attribute_name)
                    processable.append((attribute_name, attribute_value))
            
            try:
                sort_value = kwargs.pop('sort_value')
            except KeyError:
                pass
            else:
                sort_value = preconvert_int(sort_value, 'sort_value', 0, (1 << 16) - 1)
                processable.append(('sort_value', sort_value))
            
            try:
                tags = kwargs.pop('tags')
            except KeyError:
                pass
            else:
                if (tags is not None):
                    tags = preconvert_iterable_of_str(tags, 'tags', 0, 256, 2, 32)
                    if tags:
                        tags = frozenset(tags)
                    else:
                        tags = None
                
                processable.append(('tags', tags))
            
            try:
                user = kwargs.pop('user')
            except KeyError:
                pass
            else:
                user = instance_or_id_to_instance(user, (User, Client), 'user')
                processable.append(('user', user))
            
            
            if kwargs:
                raise TypeError(f'Unused or unsettable attributes: {kwargs!r}.')
        
        else:
            processable = None
        
        
        try:
            self = STICKERS[sticker_id]
        except KeyError:
            self = cls._create_empty(sticker_id)
            STICKERS[sticker_id] = self
        else:
            if not self.partial:
                return self
        
        if (processable is not None):
            for name, value in processable:
                setattr(self, name, value)
        
        return self
    
    
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
        self : ``Sticker``
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
        self.sort_value = DEFAULT_SORT_VALUE
        self.tags = None
        self.type = StickerType.none
        self.user = ZEROUSER
        return self
    
    
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
