__all__ = ('UnknownCrossMention', )

from scarletio import include

from ..bases import DiscordEntity
from ..core import CHANNELS, GUILDS
from ..utils import DATETIME_FORMAT_CODE


Channel = include('Channel')


class UnknownCrossMention(DiscordEntity):
    """
    Represents an unknown channel mentioned by a cross guild mention. These mentions are stored at ``Message``'s
    `.cross_mentions` attribute.
    
    Attributes
    ----------
    id : `int`
        The unique identifier number of the respective channel.
    guild_id : `int`
        The unique identifier number of the respective channel's guild.
    name : `str`
        The name of the respective channel.
    type : `int`
        The channel type value of the respective channel.
    """
    __slots__ = ('guild_id', 'name', 'type',)
    
    def __new__(cls, data):
        """
        Tries to find the referenced channel by `id`. If it fails creates and returns an ``UnknownCrossMention``
        instead.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Cross reference channel mention data.
        
        Returns
        -------
        channel : ``UnknownCrossMention``, ``Channel``
        """
        channel_id = int(data['id'])
        try:
            channel = CHANNELS[channel_id]
        except KeyError:
            channel = object.__new__(cls)
            channel.id = channel_id
            channel.guild_id = int(data['guild_id'])
            channel.type = data['type']
            channel.name = data['name']
        
        return channel
    
    
    def __gt__(self, other):
        """Returns whether this unknown cross mention's id is greater than the other's."""
        if (type(other) is not UnknownCrossMention) and (not isinstance(other, Channel)):
            return NotImplemented
        
        return self.id > other.id
    
    
    def __ge__(self, other):
        """Returns whether this unknown cross mention's id is greater or equal to the other's."""
        if (type(other) is not UnknownCrossMention) and (not isinstance(other, Channel)):
            return NotImplemented
        
        return self.id >= other.id
    
    
    def __eq__(self, other):
        """Returns whether this unknown cross mention's id is equal to the other's."""
        if (type(other) is not UnknownCrossMention) and (not isinstance(other, Channel)):
            return NotImplemented
        
        return self.id == other.id
    
    
    def __ne__(self, other):
        """Returns whether this unknown cross mention's id is not equal to the other's."""
        if (type(other) is not UnknownCrossMention) and (not isinstance(other, Channel)):
            return NotImplemented
        
        return self.id != other.id
    
    
    def __le__(self, other):
        """Returns whether this unknown cross mention's id is less or equal to the other's."""
        if (type(other) is not UnknownCrossMention) and (not isinstance(other, Channel)):
            return NotImplemented
        
        return self.id <= other.id
    
    
    def __lt__(self, other):
        """Returns whether this unknown cross mention's id is less than the other's."""
        if (type(other) is not UnknownCrossMention) and (not isinstance(other, Channel)):
            return NotImplemented
        
        return self.id < other.id
    
    
    def __format__(self, code):
        """
        Formats the unknown cross mention ina format string. Check ``Channel.__format__`` for available format
        codes.
        
        Parameters
        ----------
        code : `str`
            The option on based the result will be formatted.
        
        Returns
        -------
        unknown_cross_mention : `str`
        
        Raises
        ------
        ValueError
            Unknown format code.
        """
        if not code:
            return self.name
        
        if code == 'm':
            return f'<#{self.id}>'
        
        if code == 'd':
            return self.display_name
        
        if code == 'c':
            return format(self.created_at, DATETIME_FORMAT_CODE)
        
        raise ValueError(
            f'Unknown format code {code!r} for {self.__class__.__name__}; {self!r}. '
            f'Available format codes: {""!r}, {"c"!r}, {"d"!r}, {"m"!r}.'
        )
    
    
    @property
    def clients(self):
        """
        Returns the unknown cross mention's respective channel's clients, what is an empty `list` every time.
        
        Returns
        -------
        clients : `list` of ``Client``
        """
        return []
    
    
    @property
    def display_name(self):
        """
        Returns the unknown cross mention's respective channel's display name.
        
        Returns
        -------
        display_name : `str`
        """
        type_ = self.type
        name = self.name
        # Text or Store
        if type_ in (0, 5, 6, 9):
            return name.lower()
        
        # Voice
        if type == 2:
            return name.capitalize()
        
        # Category
        if type_ == 4:
            return name.upper()
        
        # Should not happen
        return name
    
    
    @property
    def guild(self):
        """
        Returns the unknown cross mention's respective channel's guild, what is `None` every time.
        
        Returns
        -------
        guild : `None`
        """
        return GUILDS.get(self.guild_id, None)
    
    
    @property
    def mention(self):
        """
        The unknown cross mention's respective channel's mention.
        
        Returns
        -------
        mention : `str`
        """
        return f'<#{self.id}>'
    
    
    @property
    def partial(self):
        """
        Unknown cross mentions represent a partial channel, so this property returns `True` every time.
        
        Returns
        -------
        partial : `bool`
        """
        return True
