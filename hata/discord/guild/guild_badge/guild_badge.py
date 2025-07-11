__all__ = ('GuildBadge',)

from scarletio import export

from ...bases import IconSlot
from ...bases import Slotted
from ...core import GUILDS
from ...http.urls import build_guild_badge_icon_url, build_guild_badge_icon_url_as

from .fields import (
    parse_enabled, parse_guild_id, parse_tag, put_enabled, put_guild_id, put_tag, validate_enabled,
    validate_guild_id, validate_tag
)


@export
class GuildBadge(metaclass = Slotted):
    """
    Represents a user's guild badge.
    
    Attributes
    ----------
    enabled : `bool`
        Whether the user is displaying their primary guild's badge
    
    guild_id : `int`
        The unique identifier number of the respective guild.
    
    icon_hash : `int`
        The guild's badge's icon's hash in `uint128`.
    
    icon_type : ``IconType``
        The guild's badge's icon's type.
    
    tag : `str`
        The guild's badge's tag.
    """
    __slots__ = ('enabled', 'guild_id', 'tag')
    
    icon = IconSlot('icon', 'badge')
    
    def __new__(cls, *, enabled = ..., guild_id = ..., icon = ..., tag = ...):
        """
        Creates a new guild bade from the given fields.
        
        Parameters
        ----------
        enabled : `bool`, Optional (Keyword only)
            Whether the user is displaying their primary guild's badge.
        
        guild_id : `int`, Optional (Keyword only)
            The guild's identifier.
        
        icon : ``None | str | Icon``, Optional (Keyword only)
            The guild's badge's icon.
        
        tag : `str`, Optional (Keyword only)
            The guild's badge's tag.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's type is incorrect.
        """
        # enabled
        if enabled is ...:
            enabled = True
        else:
            enabled = validate_enabled(enabled)
        
        # guild_id
        if guild_id is ...:
            guild_id = 0
        else:
            guild_id = validate_guild_id(guild_id)
        
        # icon
        if icon is ...:
            icon = None
        else:
            icon = cls.icon.validate_icon(icon)
        
        # tag
        if tag is ...:
            tag = ''
        else:
            tag = validate_tag(tag)
        
        # Constructor
        self = object.__new__(cls)
        self.enabled = enabled
        self.guild_id = guild_id
        self.icon = icon
        self.tag = tag
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new user clan from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Data to deserialize.
        
        Returns
        -------
        new : `instance<cls>`
        """
        self = object.__new__(cls)
        self.enabled = parse_enabled(data)
        self.guild_id = parse_guild_id(data)
        self._set_icon(data)
        self.tag = parse_tag(data)
        
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the user clan to json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with their default value should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        put_enabled(self.enabled, data, defaults)
        put_guild_id(self.guild_id, data, defaults)
        type(self).icon.put_into(self.icon, data, defaults)
        put_tag(self.tag, data, defaults)
        return data
    
    
    def __repr__(self):
        """Returns the user clan's representation."""
        repr_parts = ['<', type(self).__name__]
        
        repr_parts.append(' guild_id = ')
        repr_parts.append(repr(self.guild_id))
        
        repr_parts.append(', tag = ')
        repr_parts.append(repr(self.tag))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the user clan's hash value."""
        hash_value = 0
        
        # enabled
        hash_value ^= self.enabled
        
        # guild_id
        hash_value ^= self.guild_id
        
        # icon
        hash_value ^= hash(self.icon)
        
        # tag
        hash_value ^= hash(self.tag)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two user clans are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # enabled
        if self.enabled != other.enabled:
            return False
        
        # guild_id
        if self.guild_id != other.guild_id:
            return False
        
        # icon
        if self.icon_hash != other.icon_hash:
            return False
        if self.icon_type != other.icon_type:
            return False
        
        # tag
        if self.tag != other.tag:
            return False
        
        return True
    
    
    @property
    def guild(self):
        """
        Returns the guild of the user clan.
        
        If the guild is not cached returns `None`.
        
        Returns
        -------
        guild : ``None | Guild``
        """
        guild_id = self.guild_id
        if guild_id:
            return GUILDS.get(guild_id, None)
    
    
    def copy(self):
        """
        Copies the user clan.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.enabled = self.enabled
        new.guild_id = self.guild_id
        new.icon = self.icon
        new.tag = self.tag
        return new
    
    
    def copy_with(self, *, enabled = ..., guild_id = ..., icon = ..., tag = ...):
        """
        Copies a new user clan from the given fields.
        
        Parameters
        ----------
        enabled : `bool`, Optional (Keyword only)
            Whether the user is displaying their primary guild's badge.
        
        guild_id : `int`, Optional (Keyword only)
            The guild's identifier.
        
        icon : ``None | str | Icon``, Optional (Keyword only)
            The guild's badge's icon.
        
        tag : `str`, Optional (Keyword only)
            The guild's badge's tag.
        
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
        # enabled
        if enabled is ...:
            enabled = self.enabled
        else:
            enabled = validate_enabled(enabled)
        
        # guild_id
        if guild_id is ...:
            guild_id = self.guild_id
        else:
            guild_id = validate_guild_id(guild_id)
        
        # icon
        if icon is ...:
            icon = self.icon
        else:
            icon = type(self).icon.validate_icon(icon)
        
        # tag
        if tag is ...:
            tag = self.tag
        else:
            tag = validate_tag(tag)
        
        # Constructor
        new = object.__new__(type(self))
        new.enabled = enabled
        new.guild_id = guild_id
        new.icon = icon
        new.tag = tag
        return new
    
    
    @property
    def icon_url(self):
        """
        Returns the guild badge's icon's url. If the guild badge has no icon, then returns `None`.
        
        Returns
        -------
        url : `None | str`
        """
        return build_guild_badge_icon_url(self.guild_id, self.icon_type, self.icon_hash)
    
    
    def icon_url_as(self, ext = None, size = None):
        """
        Returns the guild badge's icon's url. If the guild badge has no icon, then returns `None`.
        
        Parameters
        ----------
        ext : `None | str` = `None`, Optional
            The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
            If the guild has animated badge icon, it can be `'gif'` as well.
        
        size : `None | int` = `None`, Optional
            The preferred minimal size of the image's url.
        
        Returns
        -------
        url : `None | str`
        """
        return build_guild_badge_icon_url_as(self.guild_id, self.icon_type, self.icon_hash, ext, size)
