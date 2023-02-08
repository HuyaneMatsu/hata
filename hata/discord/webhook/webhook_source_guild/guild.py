__all__ = ('WebhookSourceGuild', )

from scarletio import include

from ...bases import DiscordEntity, IconSlot
from ...http import urls as module_urls

from .fields import validate_id, validate_name, parse_id, parse_name, put_id_into, put_name_into


create_partial_guild_from_id = include('create_partial_guild_from_id')


class WebhookSourceGuild(DiscordEntity):
    """
    Entity representing a server type ``Webhook``'s guild.
    
    Attributes
    ----------
    id : `int`
        The unique identifier number of the guild.
    name : `str`
        The name of the guild.
    icon_hash : `int`
        The guild's icon's hash in `uint128`.
    icon_type : ``IconType``
        The guild's icon's type.
    """
    __slots__ = ('name',)
    
    icon = IconSlot(
        'icon',
        'icon',
        module_urls.guild_icon_url,
        module_urls.guild_icon_url_as,
    )
    
    def __new__(cls, *, guild_id = ..., icon = ..., name = ...):
        """
        Creates a new webhook source guild from the given fields.
        
        Parameters
        ----------
        guild_id : `int`, Optional (Keyword only)
            The guild's identifier.
        icon : `None`, ``Icon``, `str`, Optional (Keyword only)
            The guild's icon.
        name : `str`, Optional (Keyword only)
            The guild's name.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's type is incorrect.
        """
        # guild_id
        if guild_id is ...:
            guild_id = 0
        else:
            guild_id = validate_id(guild_id)
        
        # icon
        if icon is ...:
            icon = None
        else:
            icon = cls.icon.validate_icon(icon)
        
        # name
        if name is ...:
            name = ''
        else:
            name = validate_name(name)
        
        # Constructor
        self = object.__new__(cls)
        self.icon = icon
        self.id = guild_id
        self.name = name
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new webhook source guild from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Webhook source guild data.
        
        Returns
        -------
        new : `instance<cls>`
        """
        self = object.__new__(cls)
        self._set_icon(data)
        self.id = parse_id(data)
        self.name = parse_name(data)
        
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the webhook source guild to json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with their default value should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        type(self).icon.put_into(self.icon, data, defaults)
        put_id_into(self.id, data, defaults)
        put_name_into(self.name, data, defaults)
        return data
    
    
    @classmethod
    def from_guild(cls, guild):
        """
        Creates a new webhook source guild from the given guild.
        
        Parameters
        ----------
        guild : ``Guild``
            The respective guild instance.
        
        Returns
        -------
        self : ``WebhookSourceGuild``
        """
        self = object.__new__(cls)
        self.icon_hash = guild.icon_hash
        self.icon_type = guild.icon_type
        self.id = guild.id
        self.name = guild.name
        return self
    
    
    def __repr__(self):
        """Returns the webhook source guild's representation."""
        return f'<{self.__class__.__name__} id = {self.id!r}, name = {self.name!r}>'
    
    
    def __hash__(self):
        """Returns the webhook guild source's hash value."""
        hash_value = 0
        
        # icon
        hash_value ^= hash(self.icon)
        
        # id
        hash_value ^= self.id
        
        # name
        hash_value ^= hash(self.name)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two webhook source guilds are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def __ne__(self, other):
        """Returns whether the two webhook source guilds are not equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return not self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Returns whether self equals to other. `other` must be same type as self.
        
        Parameters
        ----------
        other : `instance<type<self>>`
            The other webhook source guild to compare self to.
        
        Returns
        -------
        is_equal : `bool`
        """
        # icon
        if self.icon_hash != other.icon_hash:
            return False
        if self.icon_type != other.icon_type:
            return False
        
        # id
        if self.id != other.id:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        return True
    
    
    @property
    def guild(self):
        """
        Returns the guild of the webhook source guild.
        
        If the guild is not cached, creates a new one.
        
        Returns
        -------
        guild : ``Guild``
        """
        guild = create_partial_guild_from_id(self.id)
        if guild.partial:
            guild.name = self.name
            guild.icon_hash = self.icon_hash
            guild.icon_type = self.icon_type
        
        return guild
    
    
    def copy(self):
        """
        Copies the webhook source guild.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.icon = self.icon
        new.id = self.id
        new.name = self.name
        return new
    
    
    def copy_with(self, *, guild_id = ..., icon = ..., name = ...):
        """
        Copies a new webhook source guild from the given fields.
        
        Parameters
        ----------
        guild_id : `int`, Optional (Keyword only)
            The guild's identifier.
        icon : `None`, ``Icon``, `str`, Optional (Keyword only)
            The guild's icon.
        name : `str`, Optional (Keyword only)
            The guild's name.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's type is incorrect.
        """
        # guild_id
        if guild_id is ...:
            guild_id = self.id
        else:
            guild_id = validate_id(guild_id)
        
        # icon
        if icon is ...:
            icon = self.icon
        else:
            icon = type(self).icon.validate_icon(icon)
        
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # Constructor
        new = object.__new__(type(self))
        new.icon = icon
        new.id = guild_id
        new.name = name
        return new
