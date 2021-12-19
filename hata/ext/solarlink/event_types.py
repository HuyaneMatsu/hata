__all__ = ('TrackEndEvent', 'TrackExceptionEvent', 'TrackStartEvent', 'TrackStuckEvent', 'PlayerWebsocketClosedEvent')

import reprlib

from scarletio import copy_docs
from ...discord.bases.event_types import EventBase


class TrackStartEvent(EventBase):
    """
    Represents an event when the track is started.
    
    Attributes
    ----------
    player : ``SolarPlayerBase``
        The player associated with the event.
    track : ``ConfiguredTrack``
        The started track.
    """
    __slots__ = ('player', 'track', )
    
    def __new__(cls, player, track):
        """
        Creates a new ``TrackStartEvent`` event from the given parameters.
        
        Parameters
        ----------
        player : ``SolarPlayerBase``
            The player associated with the event.
        track : ``ConfiguredTrack``
            The started track.
        """
        self = object.__new__(cls)
        self.player = player
        self.track = track
        return self
    
    
    @copy_docs(EventBase.__repr__)
    def __repr__(self):
        repr_parts = []
        
        repr_parts.append('<')
        repr_parts.append(self.__class__.__name__)
        
        repr_parts.append(' player=')
        repr_parts.append(repr(self.player))
        
        repr_parts.append(', track=')
        repr_parts.append(repr(self.track))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    @copy_docs(EventBase.__len__)
    def __len__(self):
        return 2
    
    
    @copy_docs(EventBase.__iter__)
    def __iter__(self):
        yield self.player
        yield self.track
    
    
    @copy_docs(EventBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.player != other.player:
            return False
        
        if self.track != other.track:
            return False
        
        return True
    
    
    @copy_docs(EventBase.__hash__)
    def __hash__(self):
        return hash(self.player)^hash(self.track)


class TrackEndEvent(EventBase):
    """
    Represents an event when the track is ended.
    
    Attributes
    ----------
    player : ``SolarPlayerBase``
        The player associated with the event.
    reason : `None` or `str`
        The reason why the track ended.
    track : ``ConfiguredTrack``
        The started track.
    """
    __slots__ = ('player', 'reason', 'track', )
    
    def __new__(cls, player, track, reason):
        """
        Creates a new ``TrackEndEvent`` event from the given parameters.
        
        Parameters
        ----------
        player : ``SolarPlayerBase``
            The player associated with the event.
        reason : `None` or `str`
            The reason why the track ended.
        track : ``ConfiguredTrack``
            The started track.
        """
        self = object.__new__(cls)
        self.player = player
        self.track = track
        self.reason = reason
        return self
    
    
    @copy_docs(EventBase.__repr__)
    def __repr__(self):
        repr_parts = []
        
        repr_parts.append('<')
        repr_parts.append(self.__class__.__name__)
        
        repr_parts.append(' player=')
        repr_parts.append(repr(self.player))
        
        repr_parts.append(', track=')
        repr_parts.append(repr(self.track))
        
        reason = self.reason
        if (reason is not None):
            repr_parts.append(', reason=')
            repr_parts.append(reprlib.repr(reason))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    @copy_docs(EventBase.__len__)
    def __len__(self):
        return 3
    
    
    @copy_docs(EventBase.__iter__)
    def __iter__(self):
        yield self.player
        yield self.track
        yield self.reason
    
    
    @copy_docs(EventBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.player != other.player:
            return False
        
        if self.reason != other.reason:
            return False
        
        if self.track != other.track:
            return False
        
        return True
    
    
    @copy_docs(EventBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # player
        hash_value ^= hash(self.player)
        
        # reason
        reason = self.reason
        if (reason is not None):
            hash_value ^= hash(reason)
        
        # track
        hash_value ^= hash(self.track)
        
        return hash_value


class TrackStuckEvent(EventBase):
    """
    Represents an event when the currently playing track is stuck.
    
    It usually is not a lavalink issue, but an issue with the stream.
    
    Attributes
    ----------
    player : ``SolarPlayerBase``
        The player associated with the event.
    threshold : `float`
        The amount of time till the time is stuck in seconds.
    track : ``ConfiguredTrack``
        The stucking track.
    """
    __slots__ = ('player', 'threshold', 'track', )
    
    def __new__(cls, player, track, threshold):
        """
        Creates a new ``TrackStuckEvent`` event from the given parameters.
        
        Parameters
        ----------
        player : ``SolarPlayerBase``
            The player associated with the event.
        track : ``ConfiguredTrack``
            The stucking track.
        threshold : `float`
            The amount of time till the time is stuck in seconds.
        """
        self = object.__new__(cls)
        self.player = player
        self.track = track
        self.threshold = threshold
        return self
    
    
    @copy_docs(EventBase.__repr__)
    def __repr__(self):
        repr_parts = []
        
        repr_parts.append('<')
        repr_parts.append(self.__class__.__name__)
        
        repr_parts.append(' player=')
        repr_parts.append(repr(self.player))
        
        repr_parts.append(', track=')
        repr_parts.append(repr(self.track))
        
        repr_parts.append(', threshold=')
        repr_parts.append(self.threshold.__format__('.3f'))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    @copy_docs(EventBase.__len__)
    def __len__(self):
        return 3
    
    
    @copy_docs(EventBase.__iter__)
    def __iter__(self):
        yield self.player
        yield self.track
        yield self.threshold
    
    
    @copy_docs(EventBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.player != other.player:
            return False
        
        if self.threshold != other.threshold:
            return False
        
        if self.track != other.track:
            return False
        
        return True
    
    
    @copy_docs(EventBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # player
        hash_value ^= hash(self.player)
        
        # threshold
        hash_value ^= hash(self.threshold)
        
        # track
        hash_value ^= hash(self.track)
        
        return hash_value


class TrackExceptionEvent(EventBase):
    """
    Represents an event when exception occurs when playing a track.
    
    It usually is not a lavalink issue, but an issue with the stream.
    
    Attributes
    ----------
    player : ``SolarPlayerBase``
        The player associated with the event.
    reason : `str`
        Error reason.
    track : ``ConfiguredTrack``
        The stucking track.
    """
    __slots__ = ('player', 'reason', 'track', )
    
    def __new__(cls, player, track, reason):
        """
        Creates a new ``TrackExceptionEvent`` event from the given parameters.
        
        Parameters
        ----------
        player : ``SolarPlayerBase``
            The player associated with the event.
        track : ``ConfiguredTrack``
            The stucking track.
        reason : `str`
            Error reason.
        """
        self = object.__new__(cls)
        self.player = player
        self.track = track
        self.reason = reason
        return self
    
    
    @copy_docs(EventBase.__repr__)
    def __repr__(self):
        repr_parts = []
        
        repr_parts.append('<')
        repr_parts.append(self.__class__.__name__)
        
        repr_parts.append(' player=')
        repr_parts.append(repr(self.player))
        
        repr_parts.append(', track=')
        repr_parts.append(repr(self.track))
        
        repr_parts.append(', reason=')
        repr_parts.append(reprlib.repr(self.reason))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    @copy_docs(EventBase.__len__)
    def __len__(self):
        return 3
    
    
    @copy_docs(EventBase.__iter__)
    def __iter__(self):
        yield self.player
        yield self.track
        yield self.reason
    
    
    @copy_docs(EventBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.player != other.player:
            return False
        
        if self.reason != other.reason:
            return False
        
        if self.track != other.track:
            return False
        
        return True
    
    
    @copy_docs(EventBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # player
        hash_value ^= hash(self.player)
        
        # reason
        reason = self.reason
        if (reason is not None):
            hash_value ^= hash(reason)
        
        # track
        hash_value ^= hash(self.track)
        
        return hash_value


class PlayerWebsocketClosedEvent(EventBase):
    """
    Represents an event when a player's websocket is disconnected from a guild.
    
    It usually is not a lavalink issue, but an issue with the stream.
    
    Attributes
    ----------
    by_remote : `bool`
        Whether the websocket was closed remotely.
    code : `int`
        Websocket close code.
    player : ``SolarPlayerBase``
        The player associated with the event.
    reason : `None` or `str`
        Websocket close reason.
    """
    __slots__ = ('by_remote', 'code', 'player', 'reason', )
    
    def __new__(cls, player, code, reason, by_remote):
        """
        Creates a new ``PlayerWebsocketClosedEvent`` event from the given parameters.
        
        Parameters
        ----------
        player : ``SolarPlayerBase``
            The player associated with the event.
        code : `int`
            Websocket close code.
        reason : `None` or `str`
            Websocket close reason.
        by_remote : `bool`
            Whether the websocket was closed remotely.
        """
        self = object.__new__(cls)
        self.player = player
        self.code = code
        self.reason = reason
        self.by_remote = by_remote
        return self
    
    
    @copy_docs(EventBase.__repr__)
    def __repr__(self):
        repr_parts = []
        
        repr_parts.append('<')
        repr_parts.append(self.__class__.__name__)
        
        repr_parts.append(' player=')
        repr_parts.append(repr(self.player))
        
        repr_parts.append(', code=')
        repr_parts.append(repr(self.code))
        
        reason = self.reason
        if (reason is not None):
            repr_parts.append(', reason=')
            repr_parts.append(reprlib.repr(reason))
        
        by_remote = self.by_remote
        if by_remote:
            repr_parts.append(', by_remote=')
            repr_parts.append(repr(by_remote))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    @copy_docs(EventBase.__len__)
    def __len__(self):
        return 4
    
    
    @copy_docs(EventBase.__iter__)
    def __iter__(self):
        yield self.player
        yield self.code
        yield self.reason
        yield self.by_remote
    
    
    @copy_docs(EventBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.by_remote != other.by_remote:
            return False
        
        if self.code != other.code:
            return False
        
        if self.player != other.player:
            return False
        
        if self.reason != other.reason:
            return False
        
        return True
    
    
    @copy_docs(EventBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # by_remote
        hash_value ^= self.by_remote
        
        # code
        hash_value ^= (self.code<<8)
        
        # player
        hash_value ^= hash(self.player)
        
        # reason
        reason = self.reason
        if (reason is not None):
            hash_value ^= hash(reason)
        
        return hash_value
