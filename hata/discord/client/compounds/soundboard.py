__all__ = ()

import reprlib
from base64 import b64encode

from scarletio import Compound

from ...http import DiscordHTTPClient
from ...payload_building import build_create_payload, build_edit_payload
from ...soundboard import SoundboardSound
from ...soundboard.soundboard_sound.utils import SOUNDBOARD_SOUND_FIELD_CONVERTERS

from ..request_helpers import (
    get_guild_id, get_soundboard_sound_and_guild_id_and_id, get_soundboard_sound_guild_id_and_id
)


class ClientCompoundSoundBoardEndpoints(Compound):
    
    http : DiscordHTTPClient
    
    async def soundboard_sound_get_all_default(self):
        """
        Requests the default soundboard sounds.
        
        This method is a coroutine.
        
        Returns
        -------
        sounds : `list` of ``SoundboardSound``
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        sound_datas = await self.http.soundboard_sound_get_all_default()
        return [SoundboardSound.from_data(sound_data) for sound_data in sound_datas]
    
    
    async def soundboard_sound_create(
        self, guild, sound, soundboard_sound_template = None, *, reason = None, **keyword_parameters
    ):
        """
        Creates a soundboard sound at the given guild.
        
        This function is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild where the soundboard sound will be created.
        
        sound : `bytes-like`
            The sound to add. Expected to be in `mp3` format.
        
        soundboard_sound_template : `None`, ``SoundboardSound`` = `None`, Optional
            soundboard sound entity to use as a template.
        
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the guild's audit logs.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters to create the soundboard_sound with.
        
        Other Parameters
        ----------------
        emoji : `None`, ``Emoji``, Optional (Keyword only)
            Emoji assigned to the sound.
        
        name : `str`, Optional (Keyword only)
            The name of the sound.
        
        volume : `float`, Optional (Keyword only)
            The volume of the sound to play as.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id = get_guild_id(guild)
        
        if not isinstance(sound, (bytes, bytearray, memoryview)):
            raise TypeError(
                f'`sound_data` can be `bytes-like`, got {sound.__class__.__name__}; {reprlib.repr(sound)}.'
            )
        
        data = build_create_payload(soundboard_sound_template, SOUNDBOARD_SOUND_FIELD_CONVERTERS, keyword_parameters)
        data['sound'] = 'data:audio/mp3;base64,' + b64encode(sound).decode('ascii')
        
        sound_data = await self.http.soundboard_sound_create(guild_id, data, reason)
        return SoundboardSound.from_data(sound_data)
    
    
    async def soundboard_sound_edit(
        self, soundboard_sound, soundboard_sound_template = None, *, reason = None, **keyword_parameters
    ):
        """
        Edits the soundboard sound with the given parameters.
        
        This method is a coroutine.
        
        Parameters
        ----------
        soundboard_sound : ``SoundboardSound``, `tuple` (`int`, `int`)
            The soundboard sound to edit.
        
        soundboard_sound_template : `None`, ``SoundboardSound`` = `None`, Optional
            Soundboard sound entity to use as a template.
        
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the guild's audit logs.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters to create the soundboard sound with.
        
        Other Parameters
        ----------------
        emoji : `None`, ``Emoji``, Optional (Keyword only)
            Emoji assigned to the sound.
        
        name : `str`, Optional (Keyword only)
            The name of the sound.
        
        volume : `float`, Optional (Keyword only)
            The volume of the sound to play as.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        soundboard_sound, guild_id, soundboard_sound_id = get_soundboard_sound_and_guild_id_and_id(soundboard_sound)
        
        data = build_edit_payload(
            soundboard_sound, soundboard_sound_template, SOUNDBOARD_SOUND_FIELD_CONVERTERS, keyword_parameters
        )
        
        if data:
            await self.http.soundboard_sound_edit(guild_id, soundboard_sound_id, data, reason)
    
    
    async def soundboard_sound_delete(self, soundboard_sound, *, reason = None):
        """
        Deletes the given soundboard_sound.
        
        This method is a coroutine.
        
        Parameters
        ----------
        soundboard_sound : ``SoundboardSound``, `tuple` (`int`, `int`)
            The soundboard sound to delete
        
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        TypeError
            If `soundboard_sound` was not given neither as ``SoundboardSound`` nor as `tuple` of (`int`, `int`).
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id, soundboard_sound_id = get_soundboard_sound_guild_id_and_id(soundboard_sound)
        await self.http.soundboard_sound_delete(guild_id, soundboard_sound_id, reason)
    
    # Not a thing (yet?)
    '''
    async def soundboard_sound_get(self, soundboard_sound, *, force_update = False):
        """
        Requests the specified soundboard sound.
        
        This method is a coroutine.
        
        Parameters
        ----------
        soundboard_sound : ``SoundboardSound``, `tuple` (`int`, `int`)
            The soundboard_sound to get, or a `guild-id`, `soundboard-sound-id` tuple representing it.
        
        force_update : `bool` = `False`, Optional (Keyword only)
            Whether the scheduled event should be requested even if it supposed to be up to date.
        
        Returns
        -------
        soundboard_sound : ``SoundboardSound``
        
        Raises
        ------
        TypeError
            - If `soundboard_sound`'s type is neither ``SoundboardSound``, nor `tuple` (`int`, `int`).
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        soundboard_sound, guild_id, soundboard_sound_id = get_soundboard_sound_and_guild_id_and_id(soundboard_sound)
        
        soundboard_sound_data = await self.http.soundboard_sound_get(guild_id, soundboard_sound_id)
        
        if (soundboard_sound is None) or force_update or soundboard_sound.partial:
            soundboard_sound, is_created = SoundboardSound.from_data_is_created(soundboard_sound_data)
            if not is_created:
                soundboard_sound._set_attributes(soundboard_sound_data, False)
        
        else:
            soundboard_sound = SoundboardSound.from_data(soundboard_sound_data)
        
        return soundboard_sound
    '''
