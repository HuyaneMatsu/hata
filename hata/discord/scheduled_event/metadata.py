__all__ = ('ScheduledEventEntityMetadata', 'StageEntityMetadata')

from ..user import ClientUserBase, create_partial_user_from_id
from ...backend.utils import copy_docs

class ScheduledEventEntityMetadata:
    """
    Base class for ``ScheduledEvent``'s entity metadata.
    """
    __slots__ = ()
    
    def __new__(cls):
        """
        Creates a new entity metadata instance.
        """
        raise NotImplemented
        
    def __repr__(self):
        """Returns the entity metadata's representation."""
        return f'<{self.__class__.__name__}>'
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new scheduled event entity metadata instance from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Entity metadata structure.
        
        Returns
        -------
        self : ``ScheduledEventEntityMetadata``
        """
        raise NotImplemented
    
    
    def to_data(self):
        """
        Converts the entity metadata to json serializable object.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        return {}


class StageEntityMetadata(ScheduledEventEntityMetadata):
    """
    Stage entity metadata of ``ScheduledEvent`` instances.
    
    Attributes
    ----------
    speaker_ids : `None` or `tuple` of `int`
        The speakers' identifier of the stage channel.
    """
    __slots__ = ('speaker_ids', )
    
    def __new__(cls, speakers):
        """
        Creates a new stage entity metadata for ``ScheduledEvent`` instances.
        
        Parameters
        ----------
        speaker : `None`, `int`, ``ClientUserBase``, `iterable` of (`int`, `ClientUserBase``)
            Speakers of the stage channel.
        
        Raises
        ------
        TypeError
            If `speakers` type is incorrect.
        """
        speaker_ids = None
        if speakers is None:
            pass
        elif isinstance(speakers, ClientUserBase):
            user_id = ClientUserBase.id
            speaker_ids = (user_id, )
        elif isinstance(speakers, int):
            if type(speakers) is int:
                user_id = speakers
            else:
                user_id = int(speakers)
            
            speaker_ids = (user_id, )
        
        else:
            iterator = getattr(type(speakers), '__iter__', None)
            if iterator is None:
                raise TypeError(f'`speakers` can be given as `None`, `int`, `{ClientUserBase.__name__}` or as a '
                    f'`tuple` of `int`, `{ClientUserBase.__name__}`, got {speakers.__class__.__name__}.')
            
            speaker_ids = []
            
            for speaker in iterator(speakers):
                if isinstance(speaker, ClientUserBase):
                    user_id = speaker.id
                elif type(speaker) is int:
                    user_id = speaker
                elif isinstance(speaker, int):
                    user_id = int(speaker)
                else:
                    raise TypeError(f'`speakers` contains a non `int`, or ``{ClientUserBase.__name__}`` instance, '
                        f'got {speaker.__class__.__name__}.')
                
                speaker_ids.append(user_id)
            
            if speaker_ids:
                speaker_ids.sort()
                speaker_ids = tuple(speaker_ids)
            else:
                speaker_ids = None
        
        self = object.__new__(cls)
        self.speaker_ids = speaker_ids
        return self
    
    
    @classmethod
    @copy_docs(ScheduledEventEntityMetadata.from_data)
    def from_data(cls, data):
        speaker_ids = data.get('speaker_ids', None)
        if (speaker_ids is None) or (not speaker_ids):
            speaker_ids = None
        else:
            speaker_ids = tuple(sorted(int(speaker_id) for speaker_id in speaker_ids))
        
        self = object.__new__(cls)
        self.speaker_ids = speaker_ids
        return self
    
    
    @classmethod
    @copy_docs(ScheduledEventEntityMetadata.to_data)
    def to_data(self, data):
        data = {}
        
        speaker_ids = self.speaker_ids
        if (speaker_ids is None):
            speaker_ids = ()
        data['speaker_ids'] = speaker_ids
        
        return data
    
    
    @property
    def speakers(self):
        """
        Returns the speakers of the stage channel.
        
        Returns
        -------
        speakers : `None` or `tuple` of ``ClientUserBase``
        """
        speaker_ids = self.speaker_ids
        if (speaker_ids is not None):
            return tuple(create_partial_user_from_id(speaker_id) for speaker_id in speaker_ids)
