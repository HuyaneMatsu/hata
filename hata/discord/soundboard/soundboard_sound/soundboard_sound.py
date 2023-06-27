__all__ = ('SoundboardSound',)

from ...bases import DiscordEntity
from ...core import GUILDS, SOUNDBOARD_SOUNDS
from ...http import urls as module_urls
from ...precreate_helpers import process_precreate_parameters_and_raise_extra
from ...user import ZEROUSER, create_partial_user_from_id

from .constants import DEFAULT_SOUNDBOARD_SOUND_LIMIT
from .fields import (
    parse_available, parse_emoji, parse_guild_id, parse_id, parse_name, parse_user, parse_user_id, parse_volume,
    put_available_into, put_emoji_into, put_guild_id_into, put_id_into, put_name_into, put_user_id_into, put_user_into,
    put_volume_into, validate_available, validate_emoji, validate_guild_id, validate_id, validate_name,
    validate_user_id, validate_volume
)


PRECREATE_FIELDS = {
    'available': ('available', validate_available),
    'emoji': ('emoji', validate_emoji),
    'guild': ('guild_id', validate_guild_id),
    'guild_id': ('guild_id', validate_guild_id),
    'name': ('name', validate_name),
    'user': ('user_id', validate_user_id),
    'user_id': ('user_id', validate_user_id),
    'volume': ('volume', validate_volume),
}


class SoundboardSound(DiscordEntity, immortal = True):
    """
    Represents a sound board sound.
    
    Attributes
    ----------
    _cache_user : `None`, ``ClientUserBase``
        Cache field used by the ``.user`` property.
    available : `bool`
        Whether the sound is available.
    emoji : `None`, ``Emoji``
        Emoji assigned to the sound.
    guild_id : `int`
        The guild's identifier to which the sound is added to. At the case of builtin sounds this is `0`.
    name : `str`
        The name of the sound.
    user_id : `int`
        The user's identifier who created the sound.
    volume : `float`
        The volume of the sound to play as.
    """
    __slots__ = ('_cache_user', 'available', 'emoji', 'guild_id', 'name', 'user_id', 'volume')
    
    def __new__(cls, *, available = ..., emoji = ..., name = ..., user_id = ..., volume = ...):
        """
        Creates a new sound board sound with the given fields.
        
        Parameters
        ----------
        available : `bool`, Optional (Keyword only)
            Whether the sound is available.
        emoji : `None`, ``Emoji``, Optional (Keyword only)
            Emoji assigned to the sound.
        name : `str`, Optional (Keyword only)
            The name of the sound.
        user_id : `int`, ``ClientUserBase``, Optional (Keyword only)
            The user or their identifier who created the sound.
        volume : `float`, Optional (Keyword only)
            The volume of the sound to play as.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # available
        if available is ...:
            available = True
        else:
            available = validate_available(available)
        
        # emoji
        if emoji is ...:
            emoji = None
        else:
            emoji = validate_emoji(emoji)
        
        # name
        if name is ...:
            name = ''
        else:
            name = validate_name(name)
        
        # user
        if user_id is ...:
            user_id = 0
        else:
            user_id = validate_user_id(user_id)
        
        # volume
        if volume is ...:
            volume = 1.0
        else:
            volume = validate_volume(volume)
        
        # Construct
        self = object.__new__(cls)
        self._cache_user = None
        self.available = available
        self.emoji = emoji
        self.guild_id = 0
        self.id = 0
        self.name = name
        self.user_id = user_id
        self.volume = volume
        return self
    
    
    @classmethod
    def from_data(cls, data, *, strong_cache = True):
        """
        Creates a new soundboard sound from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Sound data.
        strong_cache : `bool` = `True`, Optional (Keyword only)
            Whether the instance should be put into its strong cache.
        
        Returns
        -------
        self : `instance<cls>`
        """
        sound_id = parse_id(data)
        
        try:
            self = SOUNDBOARD_SOUNDS[sound_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = sound_id
            self._set_attributes(data)
            SOUNDBOARD_SOUNDS[sound_id] = self
        else:
            if strong_cache and (not self.partial):
                return self
            
            self._set_attributes(data)
        
        if strong_cache:
            try:
                guild = GUILDS[self.guild_id]
            except KeyError:
                pass
            else:
                soundboard_sounds = guild.soundboard_sounds
                if soundboard_sounds is None:
                    soundboard_sounds = {}
                    guild.soundboard_sounds = soundboard_sounds
                
                soundboard_sounds[sound_id] = self
            
        return self
    
    
    @classmethod
    def from_data_is_created(cls, data):
        """
        Creates a new soundboard sound from the given data.
        
        Also returns whether the instance was new (or partial) or already existed.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Sound data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        sound_id = parse_id(data)
        
        try:
            self = SOUNDBOARD_SOUNDS[sound_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = sound_id
            self._set_attributes(data)
            SOUNDBOARD_SOUNDS[sound_id] = self
        
        else:
            if not self.partial:
                return self, False
            
            self._set_attributes(data)
        
        try:
            guild = GUILDS[self.guild_id]
        except KeyError:
            pass
        else:
            soundboard_sounds = guild.soundboard_sounds
            if soundboard_sounds is None:
                soundboard_sounds = {}
                guild.soundboard_sounds = soundboard_sounds
            
            soundboard_sounds[sound_id] = self
        
        return self, True
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Converts the soundboard sound to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with the default values should be included as well.
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields, like id-s should be present as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        
        put_emoji_into(self.emoji, data, defaults)
        put_name_into(self.name, data, defaults)
        put_volume_into(self.volume, data, defaults)
        
        if include_internals:
            put_available_into(self.available, data, defaults)
            put_guild_id_into(self.guild_id, data, defaults)
            put_id_into(self.id, data, defaults)
            put_user_into(self.user, data, defaults)
            put_user_id_into(self.user_id, data, defaults)
        
        return data
    
    
    def _set_attributes(self, data):
        """
        Sets the soundboard's attributes excluding ``.id`` from from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Sound data.
        """
        self._cache_user = parse_user(data)
        self.guild_id = parse_guild_id(data)
        self.user_id = parse_user_id(data)
        
        self._update_attributes(data)
    
    
    def _update_attributes(self, data):
        """
        Updates the soundboard sound's modifiable attributes only.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Sound data.
        """
        self.available = parse_available(data)
        self.emoji = parse_emoji(data)
        self.name = parse_name(data)
        self.volume = parse_volume(data)
    
    
    def _difference_update_attributes(self, data):
        """
        Updates the soundboard sound's modifiable attributes only. Returns the changed attributes in a
        `attribute-name` - `old-value` relation.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Sound data.
        
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `object`) items
            All item in the returned dict is optional.
        
        Returned Data Structure
        -----------------------
        +-----------+-------------------+
        | Keys      | Values            |
        +===========+===================+
        | available | `bool`            |
        +-----------+-------------------+
        | emoji     | `None`, ``Emoji`` |
        +-----------+-------------------+
        | name      | `str`             |
        +-----------+-------------------+
        | volume    | `float`           |
        +-----------+-------------------+
        """
        old_attributes = {}
        
        # available
        available = parse_available(data)
        if (available != self.available):
            old_attributes['available'] = self.available
            self.available = available
        
        # emoji
        emoji = parse_emoji(data)
        if (emoji != self.emoji):
            old_attributes['emoji'] = self.emoji
            self.emoji = emoji
        
        # name
        name = parse_name(data)
        if (name != self.name):
            old_attributes['name'] = self.name
            self.name = name
        
        # volume
        volume = parse_volume(data)
        if (volume != self.volume):
            old_attributes['volume'] = self.volume
            self.volume = volume
        
        return old_attributes
    
    
    def __repr__(self):
        """Returns the soundboard sound's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' id = ')
        repr_parts.append(repr(self.id))
        
        repr_parts.append(', name = ')
        repr_parts.append(repr(self.name))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two soundboard sounds are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def __ne__(self, other):
        """Returns whether the two soundboard sounds are not equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return not self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Compares the soundboard sound's attributes to the other one's.
        
        Parameters
        ----------
        other : `instance<type<self>>`
            The other sound to compare self to.
            
            > Must have the same type as self.
        
        Returns
        -------
        is_equal : `bool`
        """
        # available
        if self.available != other.available:
            return False
        
        # emoji
        if self.emoji is not other.emoji:
            return False
        
        # guild_id -> skip
        # id -> skip
        
        # name
        if self.name != other.name:
            return False
        
        # user -> skip
        
        # user_id
        if self.user_id != other.user_id:
            return False
        
        # volume
        if self.volume != other.volume:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the soundboard sound's hash value."""
        team_id = self.id
        if team_id:
            return team_id
        
        return self._get_hash_partial()
    
    
    def _get_hash_partial(self):
        """
        Calculates the sound board sound's hash based on their fields.
        
        This method is called by ``.__hash__`` if the object has no ``.id`` set.
        
        Returns
        -------
        hash_value : `int`
        """
        hash_value = 0
        
        # available
        hash_value ^= self.available << 4
        
        # emoji
        emoji = self.emoji
        if (emoji is not None):
            hash_value ^= hash(emoji)
        
        # guild_id -> skip
        # id -> skip
        
        # name
        hash_value ^= hash(self.name)
        
        # user -> skip
        
        # user
        hash_value ^= self.user_id
        
        # volume
        hash_value ^= hash(self.volume)
        
        return hash_value
    
    
    @classmethod
    def _create_empty(cls, sound_id, guild_id = 0):
        """
        Crates a empty soundboard sound with its attributes set to their default values.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self._cache_user = None
        self.available = True
        self.emoji = None
        self.guild_id = guild_id
        self.id = sound_id
        self.name = ''
        self.user_id = 0
        self.volume = 1.0
        return self
    
    
    @classmethod
    def precreate(cls, sound_id, **keyword_parameters):
        """
        Creates a soundboard sound instance. If already exists, returns that.
        
        Parameters
        ----------
        sound_id : `int`
            The soundboard sound's identifier.
        **keyword_parameters : Keyword parameters
            Additional keyword parameters.
        
        Other Parameters
        ----------------
        available : `bool`, Optional (Keyword only)
            Whether the sound is available.
        emoji : `None`, ``Emoji``, Optional (Keyword only)
            Emoji assigned to the sound.
        guild : `int`, `None`, ``Guild``, Optional (Keyword only)
            Alternative of `guild_id`.
        guild_id : `int`, `None`, ``Guild``, Optional (Keyword only)
            The guild or its identifier to which the sound is added to.
        name : `str`, Optional (Keyword only)
            The name of the sound.
        user_id : `int`, ``ClientUserBase``, Optional (Keyword only)
            Alternative of `user`.
        user_id : `int`, ``ClientUserBase``, Optional (Keyword only)
            The user or their identifier who created the sound.
        volume : `float`, Optional (Keyword only)
            The volume of the sound to play as.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        sound_id = validate_id(sound_id)
        
        if keyword_parameters:
            processed = process_precreate_parameters_and_raise_extra(keyword_parameters, PRECREATE_FIELDS)
        else:
            processed = None
        
        try:
            self = SOUNDBOARD_SOUNDS[sound_id]
        except KeyError:
            self = cls._create_empty(sound_id)
            SOUNDBOARD_SOUNDS[sound_id] = self
        else:
            if (not self.partial):
                return self
        
        if (processed is not None):
            for item in processed:
                setattr(self, *item)
        
        return self
    
    
    def copy(self):
        """
        Copies the soundboard sound.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new._cache_user = self._cache_user
        new.available = self.available
        new.emoji = self.emoji
        new.guild_id = 0
        new.id = 0
        new.name = self.name
        new.user_id = self.user_id
        new.volume = self.volume
        return new
    
    
    def copy_with(self, *, available = ..., emoji = ..., name = ..., user_id = ..., volume = ...):
        """
        Copies the soundboard sound with the given parameters.
        
        Parameters
        ----------
        available : `bool`, Optional (Keyword only)
            Whether the sound is available.
        emoji : `None`, ``Emoji``, Optional (Keyword only)
            Emoji assigned to the sound.
        name : `str`, Optional (Keyword only)
            The name of the sound.
        user_id : `int`, ``ClientUserBase``, Optional (Keyword only)
            The user or their identifier who created the sound.
        volume : `float`, Optional (Keyword only)
            The volume of the sound to play as.
        
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
        # available
        if available is ...:
            available = self.available
        else:
            available = validate_available(available)
        
        # emoji
        if emoji is ...:
            emoji = self.emoji
        else:
            emoji = validate_emoji(emoji)
        
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # user
        if user_id is ...:
            user_id = self.user_id
            user = self._cache_user
        else:
            user_id = validate_user_id(user_id)
            user = None
        
        # volume
        if volume is ...:
            volume = self.volume
        else:
            volume = validate_volume(volume)
        
        # Construct
        new = object.__new__(type(self))
        new._cache_user = user
        new.available = available
        new.emoji = emoji
        new.guild_id = 0
        new.id = 0
        new.name = name
        new.user_id = user_id
        new.volume = volume
        return new
    
    
    @property
    def partial(self):
        """
        Returns whether the sound is partial.
        
        Returns
        -------
        partial : `bool
        """
        guild_id = self.guild_id
        if not guild_id:
            return True
        
        try:
            guild = GUILDS[guild_id]
        except KeyError:
            return True
        
        soundboard_sounds = guild.soundboard_sounds
        if soundboard_sounds is None:
            return True
        
        if self.id not in soundboard_sounds:
            return True
        
        return guild.partial
    
    
    def _delete(self):
        """
        Removes the soundboard sound's references.
        """
        try:
            guild = GUILDS[self.guild_id]
        except KeyError:
            pass
        else:
            soundboard_sounds = guild.soundboard_sounds
            if (soundboard_sounds is not None):
                try:
                    del soundboard_sounds[self.id]
                except KeyError:
                    pass
                else:
                    if not soundboard_sounds:
                        guild.soundboard_sounds = None
    
    
    url = property(module_urls.soundboard_sound_url)
    
    
    @property
    def guild(self):
        """
        Returns the guild to which the sound is added to.
        
        Returns
        -------
        guild : `None`, ``Guild``
        """
        guild_id = self.guild_id
        if guild_id:
            return GUILDS.get(guild_id, None)
    
    
    @property
    def user(self):
        """
        Returns the user who created the sound.
        
        Returns
        -------
        user : ``ClientUserBase``
        """
        user = self._cache_user
        if (user is not None):
            return user
        
        user_id = self.user_id
        if not user_id:
            return ZEROUSER
        
        user = create_partial_user_from_id(user_id)
        self._cache_user = user
        return user

    
    def is_custom_sound(self):
        """
        Returns whether the soundboard sound is a custom sound.
        
        Returns
        -------
        is_custom_sound : `bool`
        """
        sound_id = self.id
        return sound_id == 0 or sound_id >= DEFAULT_SOUNDBOARD_SOUND_LIMIT
    
    
    def is_default_sound(self):
        """
        Returns whether the soundboard sound is a default sound.
        
        Returns
        -------
        is_default_sound : `bool`
        """
        sound_id = self.id
        return sound_id != 0 and sound_id < DEFAULT_SOUNDBOARD_SOUND_LIMIT
