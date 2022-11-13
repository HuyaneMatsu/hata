__all__ = ('Stage',)

import reprlib

from scarletio import export, include

from ..bases import DiscordEntity
from ..channel import ChannelType, create_partial_channel_from_id
from ..core import STAGES
from ..scheduled_event import PrivacyLevel


Guild = include('Guild')
create_partial_guild_from_id = include('create_partial_guild_from_id')


@export
class Stage(DiscordEntity):
    """
    Represents an active stage instance of a stage channel.
    
    Attributes
    ----------
    id : `int`
        The stage instance's identifier.
    channel : ``Channel``
        The stage channel where the stage is active.
    discoverable : `bool`
        Whether the stage is discoverable.
    guild : ``Guild``
        The guild of the stage channel.
    invite_code : `None`, `str`
        Invite code to the stage's voice channel.
    privacy_level : ``PrivacyLevel``
        The privacy level of the stage.
    scheduled_event_id : `int`
        Whether the stage was started by a scheduled event.
    topic : `str`
        The topic of the stage. Can be empty string.
    """
    __slots__ = (
        '__weakref__', 'channel', 'discoverable', 'guild', 'invite_code', 'privacy_level', 'scheduled_event_id',
        'topic'
    )
    
    def __new__(cls, data):
        """
        Creates a new stage instance from the received data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Stage data.
        """
        stage_id = int(data['id'])
        try:
            self = STAGES[stage_id]
        except KeyError:
            self = object.__new__(cls)
            guild = create_partial_guild_from_id(int(data['guild_id']))
            
            self.channel = create_partial_channel_from_id(int(data['channel_id']), ChannelType.guild_stage, guild.id)
            self.guild = guild
            self.id = stage_id
            
            scheduled_event_id = data.get('guild_scheduled_event_id', None)
            if scheduled_event_id is None:
                scheduled_event_id = 0
            else:
                scheduled_event_id = int(scheduled_event_id)
            self.scheduled_event_id = scheduled_event_id
            
            self._update_attributes(data)
            
            stages = guild.stages
            if stages is None:
                stages = guild.stages = {}
            
            stages[stage_id] = self
            
            STAGES[stage_id] = self
        
        return self
    
    
    def __repr__(self):
        """Returns the stage's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
            ' channel = ',
            repr(self.channel),
            ', topic = ',
            reprlib.repr(self.topic),
            '>',
        ]
        
        return ''.join(repr_parts)
    
    
    def _update_attributes(self, data):
        """
        Updates the stage from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Stage data.
        """
        self.topic = data['topic']
        self.invite_code = data.get('invite_code', None)
        self.discoverable = not data.get('discoverable_disabled', False)
        self.privacy_level = PrivacyLevel.get(data.get('privacy_level', 2))
    
    
    def _difference_update_attributes(self, data):
        """
        Updates the stage from the given data and returns the changed attributes in `attribute-name` - `old-value`
        relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Stage data.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `Any`) items
            The changed attributes of the stage.
            
            Each item in the returned dictionary is optional.
        
        Returned Data Structure
        -----------------------
        +---------------+-----------------------+
        | Keys          | Values                |
        +===============+=======================+
        | discoverable  | `bool`                |
        +---------------+-----------------------+
        | invite_code   | `None`, `str`         |
        +---------------+-----------------------+
        | privacy_level | ``PrivacyLevel``      |
        +---------------+-----------------------+
        | topic         | `str`                 |
        +---------------+-----------------------+
        """
        old_attributes = {}
        
        topic = data['topic']
        if topic != self.topic:
            old_attributes['topic'] = self.topic
            self.topic = topic
        
        
        invite_code = data.get('invite_code', None)
        if invite_code != self.invite_code:
            old_attributes['invite_code'] = self.invite_code
            self.invite_code = invite_code
        
        
        discoverable = not data.get('discoverable_disabled', False)
        if discoverable != self.discoverable:
            old_attributes['discoverable'] = self.discoverable
            self.discoverable = discoverable
        
        
        privacy_level = PrivacyLevel.get(data.get('privacy_level', 2))
        if privacy_level is not self.privacy_level:
            old_attributes['privacy_level'] = self.privacy_level
            self.privacy_level = privacy_level
        
        return old_attributes
    
    
    def _delete(self):
        """
        Removes the stage's references.
        """
        guild = self.guild
        stages = guild.stages
        if (stages is not None):
            try:
                del stages[self.id]
            except KeyError:
                pass
            else:
                if not stages:
                    guild.stages = None
        
        try:
            del STAGES[self.id]
        except KeyError:
            pass
