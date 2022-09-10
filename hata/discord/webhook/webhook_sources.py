__all__ = ('WebhookSourceChannel', 'WebhookSourceGuild', )

from scarletio import include

from ..bases import DiscordEntity, IconSlot
from ..http import urls as module_urls


ChannelMetadataGuildBase = include('ChannelMetadataGuildBase')
ChannelType = include('ChannelType')
create_partial_channel_from_id = include('create_partial_channel_from_id')
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
    
    def __new__(cls, data):
        """
        Creates a new ``WebhookSourceGuild`` from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Webhook source guild data.
        """
        guild_id = int(data['id'])
        
        self = object.__new__(cls)
        self._set_icon(data)
        self.name = data['name']
        self.id = guild_id
        
        return self
    
    
    @classmethod
    def _from_guild(cls, guild):
        """
        Creates a new ``WebhookSourceGuild`` from the given guild.
        
        Parameters
        ----------
        guild : ``Guild``
            The respective guild instance.
        
        Returns
        -------
        self : ``WebhookSourceGuild``
        """
        self = object.__new__(cls)
        
        self.id = guild.id
        self.name = guild.name
        self.icon_hash = guild.icon_hash
        self.icon_type = guild.icon_type
        
        return self
    
    
    def __repr__(self):
        """Returns the webhook source guild's representation."""
        return f'<{self.__class__.__name__} id={self.id!r}, name={self.name!r}>'
    
    
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


class WebhookSourceChannel(DiscordEntity):
    """
    Entity representing a server type ``Webhook``'s channel.
    
    Attributes
    ----------
    id : `int`
        The unique identifier number of the channel.
    name : `str`
        The name of the channel.
    """
    __slots__ = ('name',)
    
    icon = IconSlot(
        'icon',
        'icon',
        module_urls.guild_icon_url,
        module_urls.guild_icon_url_as,
    )
    
    def __new__(cls, data):
        """
        Creates a new ``WebhookSourceChannel`` from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Webhook source channel data.
        """
        guild_id = int(data['id'])
        
        self = object.__new__(cls)
        self.name = data['name']
        self.id = guild_id
        
        return self
    
    
    @classmethod
    def _from_channel(cls, channel):
        """
        Creates a new ``WebhookSourceChannel`` from the given channel.
        
        Parameters
        ----------
        channel : ``Channel``
            The respective channel instance.
        
        Returns
        -------
        self : ``WebhookSourceChannel``
        """
        self = object.__new__(cls)
        
        self.id = channel.id
        self.name = channel.name
        
        return self
    
    
    def __repr__(self):
        """Returns the webhook source channel's representation."""
        return f'<{self.__class__.__name__} id={self.id!r}, name={self.name!r}>'
    
    
    @property
    def channel(self):
        """
        Returns the channel of the webhook source channel.
        
        If the channel is not cached, creates a new one.
        
        Returns
        -------
        channel : ``Channel``
        """
        channel = create_partial_channel_from_id(self.id, ChannelType.guild_announcements, 0)
        
        if channel.partial:
            metadata = channel.metatdata
            if isinstance(metadata, ChannelMetadataGuildBase):
                metadata.name = self.name
        
        return channel
