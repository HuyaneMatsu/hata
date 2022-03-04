__all__ = ('GuildWidget', 'GuildWidgetChannel', 'GuildWidgetUser',)

from scarletio import cached_property

from ..bases import DiscordEntity
from ..http import urls as module_urls
from ..user import Status

from .guild import Guild


class GuildWidgetUser(DiscordEntity):
    """
    Represents an user object sent with a ``GuildWidget``'s data.
    
    Attributes
    ----------
    id : `int`
        The unique identifier number of the guild widget user. Can be between `0` and `99`.
    activity_name : `None`, `str`
        The guild widget user's activity's name if applicable.
    avatar_url : `None`, `str`
        The guild widget user's avatar url if applicable.
    discriminator : `int`
        The guild widget user's discriminator.
    name : `str`
        The guild widget user's name.
    status : ``Status``
        The guild widget user's status.
    """
    __slots__ = ('activity_name', 'avatar_url', 'discriminator', 'name', 'status')
    
    def __init__(self, data):
        """
        Creates a new guild widget user from the data received from Discord.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Guild widget user data received with ``GuildWidget``'s.
        """
        self.name = data['username']
        self.id = int(data['id'])
        self.discriminator = int(data['discriminator'])
        self.avatar_url = data['avatar_url']
        self.status = Status.get(data['status'])
        try:
            activity_data = data['game']
        except KeyError:
            activity_name = None
        else:
            activity_name = activity_data['name']
        
        self.activity_name = activity_name
    
    
    @property
    def full_name(self):
        """
        The user's name with it's discriminator.
        
        Returns
        -------
        full_name : `str`
        """
        return f'{self.name}#{self.discriminator:0>4}'
    
    
    @property
    def mention(self):
        """
        The mention of the user.
        
        Returns
        -------
        mention : `str`
        """
        return f'<@{self.id}>'
    
    @property
    def mention_nick(self):
        """
        The mention to the user's nick.
        
        Returns
        -------
        mention : `str`
        
        Notes
        -----
        It actually has nothing to do with the user's nickname > <.
        """
        return f'<@!{self.id}>'
    
    
    def __repr__(self):
        """Returns the representation of the guild widget user."""
        return f'<{self.__class__.__name__} id={self.id}, name={self.full_name!r}>'


class GuildWidgetChannel(DiscordEntity):
    """
    Represents a ``GuildWidget``'s channel.
    
    Attributes
    ----------
    id : `int`
        The unique identifier number of the guild widget channel.
    name : `str`
        The channel's name.
    position : `int`
        The channel's position.
    """
    __slots__ = ('name', 'position')
    
    def __init__(self, data):
        """
        Creates a new guild widget channel from the data received from Discord.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Guild widget channel data received with ``GuildWidget``'s.
        """
        self.id = int(data['id'])
        self.name = data['name']
        self.position = data['name']
    
    
    @property
    def mention(self):
        """
        The channel's mention.
        
        Returns
        -------
        mention : `str`
        """
        return f'<#{self.id}>'
    
    
    def __repr__(self):
        """Returns the guild widget channel's representation."""
        return f'<{self.__class__.__name__} id={self.id}, name={self.name!r}>'
    
    
    def __gt__(self, other):
        """
        Whether this guild widget channel has greater (visible) position than the other at their respective guild.
        """
        if type(self) is type(other):
            if self.position > other.position:
                return True
            
            if self.position == other.position:
                if self.id > other.id:
                    return True
            
            return False
        
        return NotImplemented
    
    def __ge__(self, other):
        """
        Whether this guild widget channel has greater or equal (visible) position than the other at their respective
        guild.
        """
        if type(self) is type(other):
            if self.position > other.position:
                return True
            
            if self.position == other.position:
                if self.id >= other.id:
                    return True
            
            return False
        
        return NotImplemented
    
    def __le__(self, other):
        """
        Whether this guild widget channel has lower or equal (visible) position than the other at their respective
        guild.
        """
        if type(self) is type(other):
            if self.position < other.position:
                return True
            
            if self.position == other.position:
                if self.id <= other.id:
                    return True
            
            return False
        
        return NotImplemented
    
    def __lt__(self, other):
        """
        Whether this guild widget channel has lower (visible) position than the other at their respective guild.
        """
        if type(self) is type(other):
            if self.position < other.position:
                return True
            
            if self.position == other.position:
                if self.id < other.id:
                    return True
            
            return False
        
        return NotImplemented

class GuildWidget(DiscordEntity):
    """
    Represents a ``Guild``'s widget.
    
    Attributes
    ----------
    _cache : `dict` of (`str`, `Any`) items
        Internal cache used by cached properties.
    _data : `dict` of (`str`, `Any`) items
        The data sent by Discord and used by the cached properties of the guild widget instances.
    guild : ``Guild``
        The owner guild of the widget.
    """
    __slots__ = ('_cache', '_data', 'guild',)
    
    def __init__(self, data):
        """
        Creates a new guild widget.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            The requested guild widget data.
        """
        self.guild = Guild.precreate(int(data['id']), name=data['name'])
        self._data = data
        self._cache = {}
    
    json_url = property(module_urls.guild_widget_json_url)
    
    @property
    def id(self):
        """
        The unique identifier number of the guild widget's guild.
        
        Returns
        -------
        id : `int`
        """
        return self.guild.id
    
    @property
    def name(self):
        """
        The name of the guild widget's guild.
        
        Returns
        -------
        name : `str`
        """
        return self.guild.name
    
    @property
    def invite_url(self):
        """
        The guild widget's invite url if applicable.
        
        Returns
        -------
        invite_url : `None`, `str`
        """
        return self._data.get('instant_invite', None)
    
    @property
    def approximate_online_count(self):
        """
        Estimated online count of the respective guild.
        
        Returns
        -------
        approximate_online_count : `int`
        """
        return self._data['presence_count']
    
    @cached_property
    def users(self):
        """
        Online users received with the guild widget.
        
        Returns
        -------
        users : `list` of ``GuildWidgetUser``
        """
        return [GuildWidgetUser(GWU_data) for GWU_data in self._data['members']]

    @cached_property
    def channels(self):
        """
        Voice channels received with the guild widget.
        
        Returns
        -------
        users : `list` of ``GuildWidgetChannel``
        """
        return [GuildWidgetChannel(GWC_data) for GWC_data in self._data['channels']]
    
    def __repr__(self):
        """Returns the representation of the guild widget."""
        return f'<{self.__class__.__name__} of guild {self.guild.name}>'
