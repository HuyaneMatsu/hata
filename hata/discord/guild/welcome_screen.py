__all__ = ('WelcomeChannel', 'WelcomeScreen')

import reprlib

from ...backend.utils import BaseMethodDescriptor

from ..core import CHANNELS
from ..channel import ChannelText, ChannelBase
from ..emoji import Emoji, create_partial_emoji_from_data
from ..preconverters import preconvert_snowflake


class WelcomeScreen:
    """
    Represents a guild's welcome screen.
    
    Attributes
    ----------
    description : `None` or `str`
        Description, of what is the server about.
    welcome_channels : `None` or `tuple` of ``WelcomeChannel``
        The featured channels by the welcome screen.
    """
    __slots__ = ('description', 'welcome_channels', )
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new welcome screen instance from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Welcome screen data.
        """
        description = data.get('description', None)
        if (description is not None) and (not description):
            description = None
        
        welcome_channel_datas = data.get('welcome_channels', None)
        if (welcome_channel_datas is None) or (not welcome_channel_datas):
            welcome_channels = None
        else:
            welcome_channels = tuple(
                WelcomeChannel.from_data(welcome_channel_data) for welcome_channel_data in welcome_channel_datas
            )
        
        self = object.__new__(cls)
        self.description = description
        self.welcome_channels = welcome_channels
        return self
    
    
    def to_data(self):
        """
        Converts the welcome screen to a json serializable object.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        return {
            'description': self.description,
            'welcome_channels': [welcome_channel.to_data() for welcome_channel in self.welcome_channels],
        }
    
    def __repr__(self):
        """Returns the welcome screen's representation."""
        return (f'<{self.__class__.__name__} description={reprlib.repr(self.description)}, welcome_channels='
            f'{self.welcome_channels!r}>')
    
    def __hash__(self):
        """Returns the welcome screen's hash."""
        return hash(self.description) ^ hash(self.welcome_channels)
    
    def __eq__(self, other):
        """Returns whether the two welcome screens are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.description != other.description:
            return False
        
        if self.welcome_channels != other.welcome_channels:
            return False
        
        return True


class WelcomeChannel:
    """
    Represents a featured channel by a welcome screen.
    
    Attributes
    ----------
    description : `str`
        The channel's short description.
    channel_id : `int`
        The channel's id.
    emoji : ``Emoji``
        The emoji displayed before the `description`.
    """
    __slots__ = ('description', 'channel_id', 'emoji', )
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new welcome channel instance from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Welcome channel data.
        """
        self = object.__new__(cls)
        self.channel_id = int(data['channel_id'])
        self.description = data['description']
        self.emoji = create_partial_emoji_from_data(data)
        return self
    
    
    def to_data(self):
        """
        Converts the welcome channel to a json serializable object.
        
        Returns
        -------
        data : `str`
        """
        data = {
            'channel_id': self.channel.id,
            'description': self.description,
        }
        
        emoji = self.emoji
        if emoji.is_unicode_emoji():
            emoji_id = None
            emoji_name = emoji.unicode
        else:
            emoji_id = emoji.id
            emoji_name = emoji.name
        
        data['emoji_id'] = emoji_id
        data['emoji_name'] = emoji_name
        
        return data
    
    
    @BaseMethodDescriptor
    def custom(cls, base, **kwargs):
        """
        Creates a custom welcome channel. If called as a classmethod, then all parameters are required tho if called
        from an instance, then only those should be given, which you intent to modify.
        
        Parameters
        ----------
        **kwargs : keyword parameters
            Additional attributes of the created welcome channel.
        
        Other Parameters
        ----------------
        channel : ``ChannelTextBase`` or `int` instance, Optional
            The channel of the welcome screen.
        channel_id : `int`, optional
            Alias of `channel`, tho it accepts only snowflake.
            
            Mutually exclusive with the `channel` parameter.
        description : `str`, Optional
            Description of the welcome screen.
        emoji : ``Emoji``, Optional
            The emoji of the welcome screen.
        
        Returns
        -------
        self : ``WelcomeChannel``
        
        Raises
        ------
        TypeError
            - If `channel` parameter was given as a channel, but not as ``ChannelText`` instance.
            - If `channel` parameter was not given neither as ``ChannelText`` or `int` instance.
            - If `channel_id` was given but neither as `int` or `str` instance.
            - If `description` was not given as `str` instance.
            - If `emoji` was not given as ``Emoji`` instance.
        ValueError
            - If `channel` was given as `str` instance, but not convertable to `int`.
            - If `channel` was given as `int` instance, but out of the expected range.
            - If `channel_id` was given as `str` instance, but not convertable to `int`.
            - If `channel_id` was given as `int` instance, but out of the expected range.
            - If `description` was given as empty string.
        """
        while True:
            try:
                channel = kwargs.pop('channel')
            except KeyError:
                pass
            else:
                if isinstance(channel, ChannelText):
                    channel_id = channel.id
                elif isinstance(channel, ChannelBase):
                    raise TypeError(f'`channel` parameters can be given as {ChannelText.__name__} or `int` instance,'
                        f'got an other channel type, {channel.__class__.__name__}.')
                else:
                    channel_id = preconvert_snowflake(channel, 'channel')
                
                break
            
            try:
                channel_id = kwargs.pop('channel_id')
            except KeyError:
                pass
            else:
                channel_id = preconvert_snowflake(channel_id, 'channel_id')
                break
            
            if base is None:
                raise TypeError(f'`channel` or `channel_id` are required parameters if `{cls.__name__}.custom` is '
                    f'called as a classmethod.')
            
            channel_id = base.channel_id
            break
        
        try:
            description = kwargs.pop('description')
        except KeyError:
            if base is None:
                raise TypeError(f'`description` is a required parameter if `{cls.__name__}.custom` is called as a '
                    f'classmethod.') from None
            
            description = base.description
        else:
            if not isinstance(description, str):
                raise TypeError(f'`description` can be given as `str` instance, got {description.__class__.__name__}.')
            
            if not description:
                raise ValueError(f'`description` cannot be given as empty string.')
            
        try:
            emoji = kwargs.pop('emoji')
        except KeyError:
            if base is None:
                raise TypeError(f'`emoji` is a required parameter if `{cls.__name__}.custom` is called as a '
                    f'classmethod.') from None
            
            emoji = base.emoji
        else:
            if not isinstance(emoji, Emoji):
                raise TypeError(f'`emoji` can be given as `{Emoji.__name__}` instance, got {emoji.__class__.__name__}.')
        
        
        if kwargs:
            raise TypeError(f'Unused parameters: {", ".join(list(kwargs))}')
        
        self = object.__new__(cls)
        self.channel_id = channel_id
        self.description = description
        self.emoji = emoji
        
        return self
    
    
    @property
    def channel(self):
        """
        Returns the welcome channel's respective channel.
        
        Returns
        -------
        channel : ``ChannelText``
        """
        channel_id = self.channel_id
        try:
            channel = CHANNELS[channel_id]
        except KeyError:
            channel = ChannelText._from_partial_data(None, channel_id, None)
        
        return channel
    
    
    def __repr__(self):
        """Returns the welcome channel's representation."""
        return (f'<{self.__class__.__name__} channel_id={self.channel_id},  emoji={self.emoji!r}, description='
            f'{reprlib.repr(self.description)}>')
    
    
    def __hash__(self):
        """Returns the welcome channel's hash."""
        return self.channel_id ^ self.emoji.id ^ hash(self.description)
    
    
    def __eq__(self, other):
        """Returns whether the two welcome channels are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.channel_id != other.channel_id:
            return False
        
        if (self.emoji is not other.emoji):
            return False
        
        if self.description != other.description:
            return False
        
        return True
