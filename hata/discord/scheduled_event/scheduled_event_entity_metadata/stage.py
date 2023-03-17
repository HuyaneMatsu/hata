__all__ = ('ScheduledEventEntityMetadataStage',)

from scarletio import copy_docs

from .base import ScheduledEventEntityMetadataBase
from .fields import parse_speaker_ids, put_speaker_ids_into, validate_speaker_ids


class ScheduledEventEntityMetadataStage(ScheduledEventEntityMetadataBase):
    """
    Stage entity metadata of ``ScheduledEvent``-s.
    
    Attributes
    ----------
    speaker_ids : `None`, `tuple` of `int`
        The speakers' identifier of the stage channel.
    """
    __slots__ = ('speaker_ids', )
    
    @copy_docs(ScheduledEventEntityMetadataBase.__new__)
    def __new__(cls, keyword_parameters):
        # speaker_ids
        try:
            speaker_ids = keyword_parameters.pop('speaker_ids')
        except KeyError:
            speaker_ids = None
        else:
            speaker_ids = validate_speaker_ids(speaker_ids)
        
        self = object.__new__(cls)
        self.speaker_ids = speaker_ids
        return self
    
    
    @classmethod
    @copy_docs(ScheduledEventEntityMetadataBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        self.speaker_ids = parse_speaker_ids(data)
        return self
    
    
    @copy_docs(ScheduledEventEntityMetadataBase.to_data)
    def to_data(self, *, defaults = False):
        data = {}
        put_speaker_ids_into(self.speaker_ids, data, defaults)
        return data
    
    
    @classmethod
    def _create_empty(cls):
        self = object.__new__(cls)
        self.speaker_ids = None
        return self
    
    
    @copy_docs(ScheduledEventEntityMetadataBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        speaker_ids = self.speaker_ids
        if (speaker_ids is not None):
            repr_parts.append(' speaker_ids = [')
            
            index = 0
            length = len(speaker_ids)
            
            while True:
                speaker_id = speaker_ids[index]
                repr_parts.append(repr(speaker_id))
                
                index += 1
                if index == length:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(']')
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(ScheduledEventEntityMetadataBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        speaker_ids = self.speaker_ids
        if (speaker_ids is not None):
            hash_value ^= len(speaker_ids)
            
            for speaker_id in speaker_ids:
                hash_value ^= speaker_id
        
        return hash_value
    
    
    @copy_docs(ScheduledEventEntityMetadataBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        if self.speaker_ids != other.speaker_ids:
            return False
        
        return True
    
    
    @copy_docs(ScheduledEventEntityMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        speaker_ids = self.speaker_ids
        if (speaker_ids is not None):
            speaker_ids = (*speaker_ids,)
        new.speaker_ids = speaker_ids
        return new
    
    
    @copy_docs(ScheduledEventEntityMetadataBase.copy)
    def copy_with(self, keyword_parameters):
        # speaker_ids
        try:
            speaker_ids = keyword_parameters.pop('speaker_ids')
        except KeyError:
            speaker_ids = self.speaker_ids
            if (speaker_ids is not None):
                speaker_ids = (*speaker_ids,)
        else:
            speaker_ids = validate_speaker_ids(speaker_ids)
        
        new = object.__new__(type(self))
        new.speaker_ids = speaker_ids
        return new
