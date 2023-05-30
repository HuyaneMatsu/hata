__all__ = ('SoundboardSoundsEvent',)

from scarletio import copy_docs

from ...bases import EventBase
from ...core import GUILDS

from .fields import parse_guild_id, parse_sounds, put_guild_id_into, put_sounds_into, validate_guild_id, validate_sounds


class SoundboardSoundsEvent(EventBase):
    """
    Represents a soundboard sound event sent to a voice channel.
    
    Attributes
    ----------
    guild_id : `int`
        The guild's identifier that the event represents.
    sounds : `None`, `tuple` of ``SoundboardSound``
        The responded sounds.
    """
    __slots__ = ('guild_id', 'sounds')
    
    def __new__(
        cls,
        *,
        guild_id = ...,
        sounds = ...,
    ):
        """
        Creates a self soundboard sounds event
        
        Parameters
        ----------
        guild_id : `int`, ``Guild``, Optional (Keyword only)
            The guild's identifier that the event represents.
        sounds : `None`, `iterable` of ``SoundboardSound``, Optional (Keyword only)
            The responded sounds.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # guild_id
        if guild_id is ...:
            guild_id = 0
        else:
            guild_id = validate_guild_id(guild_id)
        
        # sounds
        if sounds is ...:
            sounds = None
        else:
            sounds = validate_sounds(sounds)
        
        # Construct
        self = object.__new__(cls)
        self.guild_id = guild_id
        self.sounds = sounds
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a soundboard sounds event from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Voice channel effect event data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        guild_id = parse_guild_id(data)
        
        try:
            guild = GUILDS[guild_id]
        except KeyError:
            pass
        else:
            old_sounds = [*guild.iter_soundboard_sounds()]
            guild.soundboard_sounds = None
            guild.soundboard_sounds_cached = True
        
        self = object.__new__(cls)
        self.guild_id = guild_id
        self.sounds = parse_sounds(data)
        
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the soundboard sounds event into a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default field values should be included.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        put_guild_id_into(self.guild_id, data, defaults)
        put_sounds_into(self.sounds, data, defaults)
        return data
    
    
    @copy_docs(EventBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' guild_id = ')
        repr_parts.append(repr(self.guild_id))
        
        repr_parts.append(', sounds = [')
        
        sounds = self.sounds
        if (sounds is not None):
            index = 0
            length = len(sounds)
            
            while True:
                sound = sounds[index]
                repr_parts.append(repr(sound))
                
                index += 1
                if index == length:
                    break
                    
                repr_parts.append(', ')
                continue
        
        repr_parts.append(']>')
        return ''.join(repr_parts)
    
    
    @copy_docs(EventBase.__len__)
    def __len__(self):
        return 2
    
    
    @copy_docs(EventBase.__iter__)
    def __iter__(self):
        yield self.guild_id
        yield self.sounds
        
    
    @copy_docs(EventBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        # guild_id
        if self.guild_id != other.guild_id:
            return False
        
        # sounds
        if self.sounds != other.sounds:
            return False
        
        return True
    
    
    @copy_docs(EventBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # guild_id
        hash_value ^= self.guild_id
        
        # sounds
        sounds = self.sounds
        if (sounds is not None):
            hash_value ^= len(sounds)
            
            for sound in sounds:
                hash_value ^= hash(sound)
        
        return hash_value
    
    
    def copy(self):
        """
        Copies the soundboard sounds event
        
        Returns
        -------
        new : `instance<type<new>>`
        """
        new = object.__new__(type(self))
        new.guild_id = self.guild_id
        sounds = self.sounds
        if (sounds is not None):
            sounds = (*(sound for sound in sounds),)
        new.sounds = sounds
        return new
    
    
    def copy_with(
        self,
        *,
        guild_id = ...,
        sounds = ...,
    ):
        """
        Copies new soundboard sounds event with the given fields.
        
        Parameters
        ----------
        guild_id : `int`, ``Guild``, Optional (Keyword only)
            The guild's identifier that the event represents.
        sounds : `None`, `iterable` of ``SoundboardSound``, Optional (Keyword only)
            The responded sounds.
        
        Returns
        -------
        new : `instance<type<new>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # guild_id
        if guild_id is ...:
            guild_id = self.guild_id
        else:
            guild_id = validate_guild_id(guild_id)
        
        # sounds
        if sounds is ...:
            sounds = self.sounds
            if (sounds is not None):
                sounds = (*(sound for sound in sounds),)
        else:
            sounds = validate_sounds(sounds)
        
        # Construct
        new = object.__new__(type(self))
        new.guild_id = guild_id
        new.sounds = sounds
        return new
    
    
    @property
    def guild(self):
        """
        Returns the soundboard sound event's guild. If the guild is not cached returns `None`.
        
        Returns
        -------
        guild : `None`, ``Guild``
        """
        guild_id = self.guild_id
        if guild_id:
            return GUILDS.get(guild_id, None)
    
    
    def iter_sounds(self):
        """
        Iterates over the sounds of the soundboard sounds event.
        
        This method is an iterable generator
        
        Yields
        ------
        sound : ``SoundboardSound``
        """
        sounds = self.sounds
        if (sounds is not None):
            yield from sounds
