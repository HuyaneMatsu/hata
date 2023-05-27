__all__ = ()

from scarletio import Compound

from ...http import DiscordHTTPClient
from ...soundboard import SoundBoardSound


class ClientCompoundSoundBoardEndpoints(Compound):
    
    http : DiscordHTTPClient
    
    async def soundboard_sound_get_all_default(self):
        """
        Requests the default soundboard sounds.
        
        This method is a coroutine.
        
        Returns
        -------
        sounds : `list` of ``SoundBoardSound``
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        sound_datas = await self.http.soundboard_sound_get_all_default()
        return [SoundBoardSound.from_data(sound_data) for sound_data in sound_datas]
