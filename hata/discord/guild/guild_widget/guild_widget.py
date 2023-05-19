__all__ = ('GuildWidget',)

from ...bases import DiscordEntity
from ...http import urls as module_urls

from ..guild import Guild

from .fields import (
    parse_approximate_online_count, parse_channels, parse_id, parse_invite_url, parse_name, parse_users,
    put_approximate_online_count_into, put_channels_into, put_id_into, put_invite_url_into, put_name_into,
    put_users_into, validate_approximate_online_count, validate_channels, validate_id, validate_invite_url,
    validate_name, validate_users
)


class GuildWidget(DiscordEntity):
    """
    Represents a ``Guild``'s widget.
    
    Attributes
    ----------
    approximate_online_count : `int`
        Estimated count of the online users in the respective guild.
    channels : `None`, `tuple` of ``GuildWidgetChannel``
        Voice channels received with the guild widget.
    id : `int`
        The unique identifier number of the guild widget's guild.
    invite_url : `None`, `str`
        The guild widget's invite url if applicable.
    name : `str`
        The name of the guild widget's guild.
    users : `None`, `tuple` of ``GuildWidgetUser``
        Online users received with the guild widget.
    """
    __slots__ = ('approximate_online_count', 'channels', 'invite_url', 'name', 'users')
    
    def __new__(
        cls,
        *,
        approximate_online_count = ...,
        channels = ...,
        guild_id = ...,
        invite_url = ...,
        name = ...,
        users = ...,
    ):
        """
        Creates a new guild widget from the given fields.
        
        Parameters
        ----------
        approximate_online_count : `int`, Optional (Keyword only)
            Estimated count of the online users in the respective guild.
        channels : `None`, `iterable` of ``GuildWidgetChannel``, Optional (Keyword only)
            Voice channels received with the guild widget.
        id : `int`, Optional (Keyword only)
            The unique identifier number of the guild widget's guild.
        invite_url : `None`, `str`, Optional (Keyword only)
            The guild widget's invite url if applicable.
        name : `str`, Optional (Keyword only)
            The name of the guild widget's guild.
        users : `None`, `iterable` of ``GuildWidgetUser``, Optional (Keyword only)
            Online users received with the guild widget.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # approximate_online_count
        if approximate_online_count is ...:
            approximate_online_count = 0
        else:
            approximate_online_count = validate_approximate_online_count(approximate_online_count)
        
        # channels
        if channels is ...:
            channels = None
        else:
            channels = validate_channels(channels)
        
        # guild_id
        if guild_id is ...:
            guild_id = 0
        else:
            guild_id = validate_id(guild_id)
        
        # invite_url
        if invite_url is ...:
            invite_url = None
        else:
            invite_url = validate_invite_url(invite_url)
        
        # name
        if name is ...:
            name = ''
        else:
            name = validate_name(name)
        
        # users
        if users is ...:
            users = None
        else:
            users = validate_users(users)
        
        # Construct
        self = object.__new__(cls)
        self.approximate_online_count = approximate_online_count
        self.channels = channels
        self.id = guild_id
        self.invite_url = invite_url
        self.name = name
        self.users = users
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new guild widget from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            The requested guild widget data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.approximate_online_count = parse_approximate_online_count(data)
        self.channels = parse_channels(data)
        self.id = parse_id(data)
        self.invite_url = parse_invite_url(data)
        self.name = parse_name(data)
        self.users = parse_users(data)
        return self
    
    
    def to_data(self, * , defaults = False):
        """
        Serializes the guild widget.
        
        Parameters
        ----------
        defaults : `bool`
            Whether fields of their default value should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        put_approximate_online_count_into(self.approximate_online_count, data, defaults)
        put_channels_into(self.channels, data, defaults)
        put_id_into(self.id, data, defaults)
        put_invite_url_into(self.invite_url, data, defaults)
        put_name_into(self.name, data, defaults)
        put_users_into(self.users, data, defaults)
        return data
    
    
    def __repr__(self):
        """Returns the representation of the guild widget."""
        return f'<{self.__class__.__name__} id = {self.id!r}, name = {self.name!r}>'
    
    
    def __hash__(self):
        """Returns the has value of the guild widget."""
        hash_value = 0
        
        # approximate_online_count
        hash_value ^= self.approximate_online_count
        
        # channels
        channels = self.channels
        if (channels is not None):
            hash_value ^= len(channels) << 8
            
            for channel in channels:
                hash_value ^= hash(channel)
        
        # id
        hash_value ^= self.id
        
        # invite_url
        invite_url = self.invite_url
        if (invite_url is not None):
            hash_value ^= hash(invite_url)
        
        # name
        hash_value ^= hash(self.name)
        
        # users
        users = self.users
        if (users is not None):
            hash_value ^= len(users) << 12
            
            for user in users:
                hash_value ^= hash(user)
        
        return hash_value
    
    def __eq__(self, other):
        """Returns whether the two guild widget are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def __ne__(self, other):
        """Returns whether the two guild widget are not equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return not self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Returns whether the two types are equal.
        
        Helper method for ``.__eq__``
        
        Parameters
        ----------
        other : `instance<type<self>>`
            The other instance. Must be from the same type.
        
        Returns
        -------
        is_equal : `bool`
        """
        # approximate_online_count
        if self.approximate_online_count != other.approximate_online_count:
            return False
        
        # channels
        if self.channels != other.channels:
            return False
        
        # id
        if self.id != other.id:
            return False
        
        # invite_url
        if self.invite_url != other.invite_url:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        # status
        if self.users != other.users:
            return False
        
        return True
    
    
    def copy(self):
        """
        Copies the guild widget.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.approximate_online_count = self.approximate_online_count
        
        channels = self.channels
        if (channels is not None):
            channels = (*(channel.copy() for channel in channels),)
        new.channels = channels
        
        new.id = self.id
        new.invite_url = self.invite_url
        new.name = self.name
        
        users = self.users
        if (users is not None):
            users = (*(user.copy() for user in users),)
        new.users = users
        
        return new
    
    
    def copy_with(
        self,
        *,
        approximate_online_count = ...,
        channels = ...,
        guild_id = ...,
        invite_url = ...,
        name = ...,
        users = ...,
    ):
        """
        Copies the guild widget from the given parameters.
        
        Parameters
        ----------
        approximate_online_count : `int`, Optional (Keyword only)
            Estimated count of the online users in the respective guild.
        channels : `None`, `iterable` of ``GuildWidgetChannel``, Optional (Keyword only)
            Voice channels received with the guild widget.
        id : `int`, Optional (Keyword only)
            The unique identifier number of the guild widget's guild.
        invite_url : `None`, `str`, Optional (Keyword only)
            The guild widget's invite url if applicable.
        name : `str`, Optional (Keyword only)
            The name of the guild widget's guild.
        users : `None`, `iterable` of ``GuildWidgetUser``, Optional (Keyword only)
            Online users received with the guild widget.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # approximate_online_count
        if approximate_online_count is ...:
            approximate_online_count = self.approximate_online_count
        else:
            approximate_online_count = validate_approximate_online_count(approximate_online_count)
        
        # channels
        if channels is ...:
            channels = self.channels
            if (channels is not None):
                channels = (*(channel.copy() for channel in channels),)
        else:
            channels = validate_channels(channels)
        
        # guild_id
        if guild_id is ...:
            guild_id = self.id
        else:
            guild_id = validate_id(guild_id)
        
        # invite_url
        if invite_url is ...:
            invite_url = self.invite_url
        else:
            invite_url = validate_invite_url(invite_url)
        
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # users
        if users is ...:
            users = self.users
            if (users is not None):
                users = (*(user.copy() for user in users),)
        else:
            users = validate_users(users)
        
        # Construct
        new = object.__new__(type(self))
        new.approximate_online_count = approximate_online_count
        new.channels = channels
        new.id = guild_id
        new.invite_url = invite_url
        new.name = name
        new.users = users
        return new
    
    
    json_url = property(module_urls.guild_widget_json_url)
    
    
    @property
    def guild(self):
        """
        Returns the parent guild of the widget. If it is not in cache creates a new one.
        
        Returns
        -------
        guild : ``Guild``
        """
        return Guild.precreate(self.id, name = self.name)
    
    
    def iter_channels(self):
        """
        Iterates over the widget channels.
        
        This method is an iterable generator.
        
        Yields
        ------
        channel : ``GuildWidgetChannel``
        """
        channels = self.channels
        if channels is not None:
            yield from channels
    
    
    def iter_users(self):
        """
        Iterates over the widget users.
        
        This method is an iterable generator.
        
        Yields
        ------
        user : ``GuildWidgetUser``
        """
        users = self.users
        if users is not None:
            yield from users
