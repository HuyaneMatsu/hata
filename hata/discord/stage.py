__all__ = ('Stage',)

import reprlib

from .bases import DiscordEntity
from .channel import ChannelStage
from .guild import Guild
from .preinstanced import StagePrivacyLevel

class Stage(DiscordEntity):
    """
    Represents an active stage instance of a stage channel.
    
    Attributes
    ----------
    id : `int`
        The stage instance's identifier.
    channel : ``ChannelStage``
        The stage channel where the stage is active.
    guild : ``Guild``
        The guild of the stage channel.
    privacy_level : ``StagePrivacyLevel``
        The privacy level of the stage.
    topic : `str`
        The topic of the stage. Can be empty string.
    """
    __slots__ = ('channel', 'guild', 'privacy_level', 'topic')
    def __new__(cls, data):
        """
        Creates a new stage instance from the received data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Stage data.
        """
        self = object.__new__(cls)
        self.channel = ChannelStage.precreate(int(data['channel_id']))
        self.guild = Guild.precreate(int(data['guild_id']))
        self.topic = data['topic']
        self.id = int(data['id'])
        self.privacy_level = StagePrivacyLevel.get(data['privacy_level'])
        return self
    
    def __repr__(self):
        """Returns the stage's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
            ' channel=',
            repr(self.channel),
            ', topic=',
            reprlib.repr(self.topic),
            '>',
        ]
        
        return ''.join(repr_parts)
