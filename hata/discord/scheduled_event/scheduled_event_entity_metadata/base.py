__all__ = ('ScheduledEventEntityMetadataBase',)

from scarletio import RichAttributeErrorBaseType

from ...bases import PlaceHolder
from ...user import create_partial_user_from_id


class ScheduledEventEntityMetadataBase(RichAttributeErrorBaseType):
    """
    Base class for ``ScheduledEvent``'s entity metadata.
    """
    __slots__ = ()
    
    def __new__(cls):
        """
        Creates a new entity metadata instance.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        return object.__new__(cls)
    
    
    @classmethod
    def from_keyword_parameters(cls, keyword_parameters):
        """
        Creates a new entity metadata instance from the given keyword_parameters.
        
        Parameters
        ----------
        keyword_parameters : `dict` of (`str`, `object`) items
            Additional keyword parameters passed to ``ScheduledEvent.__new__``
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        return cls()
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new scheduled event entity metadata instance from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Entity metadata structure.
        
        Returns
        -------
        self : `instance<cls>`
        """
        return object.__new__(cls)
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the entity metadata to json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with their default value should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        return {}
    
    
    @classmethod
    def _create_empty(cls):
        """
        Creates a scheduled event entity metadat instance with its attributes set with their default values.
        
        Returns
        -------
        self : `instance<cls>`
        """
        return object.__new__(cls)
    
    
    def __repr__(self):
        """Returns the entity metadata's representation."""
        return f'<{self.__class__.__name__}>'
    
    
    def __hash__(self):
        """Returns the entity metadata's hash value."""
        return 0
    
    
    def __eq__(self, other):
        """Returns whether the two entity metadatas equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Returns whether the two entity metadatas are equal.
        
        Parameters
        ----------
        other : `instance<type<self>>`
            The other instance. Must be from the same type.
        
        Returns
        -------
        is_equal : `bool`
        """
        return True
    
    
    def copy(self):
        """
        Copies the scheduled event entity metadata.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        return object.__new__(type(self))
    
    
    def copy_with(self):
        """
        Copies the scheduled event entity metadata with the given fields.
        
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
        return object.__new__(type(self))
    
    
    def copy_with_keyword_parameters(self, keyword_parameters):
        """
        Copies the scheduled event entity metadata with the given keyword parameters.
        
        Parameters
        ----------
        keyword_parameters : `dict` of (`str`, `object`) items
            Additional keyword parameters passed to ``ScheduledEvent.copy_with``
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
        return self.copy_with()
    
    
    location = PlaceHolder(
        None,
        """
        Returns the place where the event will take place.
        
        Returns
        -------
        location : `None`, `str`
        """
    )
    
    
    speaker_ids = PlaceHolder(
        None,
        """
        Returns the speakers' identifier of the stage channel.
        
        Returns
        -------
        speaker_ids : `None`, `tuple` of `int`
        """
    )
    
    
    def iter_speaker_ids(self):
        """
        Iterates over the speakers' identifiers of the stage channel.
        
        This method is an iterable generator.
        
        Yields
        ------
        speaker_id : `int`
        """
        speaker_ids = self.speaker_ids
        if (speaker_ids is not None):
            yield from speaker_ids
    
    
    @property
    def speakers(self):
        """
        Returns the speakers of the stage channel.
        
        Returns
        -------
        speakers : `None`, `tuple` of ``ClientUserBase``
        """
        speaker_ids = self.speaker_ids
        if (speaker_ids is not None):
            return (*(create_partial_user_from_id(speaker_id) for speaker_id in speaker_ids),)
    
    
    def iter_speakers(self):
        """
        Iterates over the speakers of the stage channel.
        
        This method is an iterable generator.
        
        Yields
        ------
        speakers : ``ClientUserBase``
        """
        speaker_ids = self.speaker_ids
        if (speaker_ids is not None):
            
            for speaker_id in speaker_ids:
                yield create_partial_user_from_id(speaker_id)
