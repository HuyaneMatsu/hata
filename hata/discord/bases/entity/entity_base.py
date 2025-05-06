__all__ = ('DiscordEntity',)

from scarletio import RichAttributeErrorBaseType, include

from .discord_entity_meta import DiscordEntityMeta, ENTITY_ID_PLACEHOLDER


id_to_datetime = include('id_to_datetime')


class DiscordEntity(RichAttributeErrorBaseType, metaclass = DiscordEntityMeta):
    """
    Base type for Discord entities.
    
    Notes
    -----
    Inherit it with passing `immortal = True` to make the sub-types weakreferable.
    """
    id = ENTITY_ID_PLACEHOLDER
    
    __slots__ = ()
    
    @property
    def created_at(self):
        """
        When the entity was created.
        
        Returns
        -------
        created_at : `DateTime`
        """
        return id_to_datetime(self.id)
    
    
    def __hash__(self):
        """Returns the has value of the entity, what equals to it's id."""
        return self.id
    
    
    def __gt__(self, other):
        """Whether this entity's id is greater than the other's."""
        if type(self) is type(other):
            return self.id > other.id
        
        return NotImplemented
    
    
    def __ge__(self, other):
        """Whether this entity's id is greater or equal than the other's."""
        if type(self) is type(other):
            return self.id >= other.id
        
        return NotImplemented
    
    
    def __eq__(self, other):
        """Whether this entity's id is equal as the other's."""
        if type(self) is type(other):
            return self.id == other.id
        
        return NotImplemented
    
    
    def __ne__(self, other):
        """Whether this entity's id is not equal as the other's."""
        if type(self) is type(other):
            return self.id != other.id
        
        return NotImplemented
    
    
    def __le__(self, other):
        """Whether this entity's id is less or equal than the other's."""
        if type(self) is type(other):
            return self.id <= other.id
        
        return NotImplemented
    
    
    def __lt__(self, other):
        """Whether this entity's id is less than the other's."""
        if type(self) is type(other):
            return self.id < other.id
        
        return NotImplemented
