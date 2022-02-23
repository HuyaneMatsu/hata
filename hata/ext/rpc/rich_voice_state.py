__all__ = ('RichVoiceState', )

from ...discord.user import User

from .user_voice_settings import AudioBalance


class RichVoiceState:
    """
    Rich voice state containing user, and it's voice state and other related attributes.
    
    Attributes
    ----------
    audio_balance : ``AudioBalance``
        The user's audio balance.
    deaf : `bool`
        Whether the user is deafen.
    is_speaker : `bool`
        Whether the user is suppressed inside of the voice channel.
        
        If the channel is a ``ChannelVoice``, it is always `False`, meanwhile it ``ChannelStage`` it can vary.
    mute : `bool`
        Whether the user is muted.
    nick : `None`, `str`
        The user's nickname in the guild if applicable.
    self_deaf : `bool`
        Whether the user muted everyone else.
    self_mute : `bool`
        Whether the user muted itself.
    user : ``ClientUserBase``
        The respective user.
    voice_state : ``VoiceState``
        The respective user state.
    volume : `float`
        The user's volume.
        
        Can be in range [0.0:2.0].
    """
    __slots__ = (
        'audio_balance', 'deaf', 'is_speaker', 'mute', 'nick', 'self_deaf', 'self_mute', 'user', 'volume'
    )
    
    def __repr__(self):
        """Returns the rich voice state's representation."""
        repr_parts = ['<', self.__class__.__name__, ' user=', repr(self.user), '>']
        return ''.join(repr_parts)
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new rich voice state instance from the given json data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Rich voice state data.
        
        Returns
        -------
        self : ``RichVoiceState``
        """
        self = object.__new__(cls)
        self.audio_balance = AudioBalance.from_data(data['pan'])
        self.deaf = data['deaf']
        self.is_speaker = not data.get('suppress', False)
        self.mute = data['mute']
        self.nick = data.get('nick', None)
        self.self_deaf = data['self_deaf']
        self.self_mute = data['self_mute']
        self.user = User.from_data(data['user'])
        self.volume = data['volume'] * 0.01
        return self
