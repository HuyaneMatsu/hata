__all__ = ('InviteStage', )

from ..user import User


class InviteStage:
    """
    Represents an invite's stage.
    
    Attributes
    ----------
    participant_count : `int`
        The numbers of participants of the stage.
    participants : `tuple` of ``ClientUserBase``
        The users inside of the stage.
    speaker_count : int`
        The number of speakers in the stage.
    topic : `None`, `str`
        The stage's topic if any.
    """
    __slots__ = ('participant_count', 'participants', 'speaker_count', 'topic',)
    
    
    def __new__(cls, data, guild_id):
        """
        Creates a new ``InviteStage`` from the given data.
        
        Parameters
        ----------
        data : `str`
            Data received from Discord.
        guild_id : `int`
            The respective guild's identifier.
        """
        guild_profile_datas = data['members']
        users = tuple(
            User.from_data(guild_profile_data['user'], guild_profile_datas, guild_id)
            for guild_profile_data in guild_profile_datas
        )
        
        topic = data['topic']
        if (topic is not None) and (not topic):
            topic = None
        
        self = object.__new__(cls)
        self.participant_count = data['participant_count']
        self.speaker_count = data['speaker_count']
        self.participants = users
        self.topic = topic
        
        return self
    
    
    def __repr__(self):
        """Returns the invite stage's representation."""
        return f'<{self.__class__.__name__}>'
