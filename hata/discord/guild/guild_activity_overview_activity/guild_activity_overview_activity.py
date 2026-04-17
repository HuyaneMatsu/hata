__all__ = ('GuildActivityOverviewActivity',)

from scarletio import RichAttributeErrorBaseType

from .fields import parse_level, parse_score, put_level, put_score, validate_level, validate_score
from .preinstanced import GuildActivityOverviewActivityLevel


class GuildActivityOverviewActivity(RichAttributeErrorBaseType):
    """
    Activity information inside of a guild activity overview.
    
    Attributes
    ----------
    level : ``GuildActivityOverviewActivityLevel``
        The activity's level.
    
    score : `int`
        Total accumulated score.
    """
    __slots__ = ('level', 'score')
    
    def __new__(cls, *, level = ..., score = ...):
        """
        Creates a new guild activity overview activity.
        
        Parameters
        ----------
        level : `None | GuildActivityOverviewActivityLevel | int`, Optional (Keyword only)
            The activity's level.
        
        score : `int`, Optional (Keyword only)
            Total accumulated score.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value in incorrect.
        """
        # level
        if level is ...:
            level = GuildActivityOverviewActivityLevel.none
        else:
            level = validate_level(level)
        
        # score
        if score is ...:
            score = 0
        else:
            score = validate_score(score)
        
        # Construct
        self = object.__new__(cls)
        self.level = level
        self.score = score
        return self
    
    
    @classmethod
    def _create_empty(cls):
        """
        Creates an empty activity overview activity.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.level = GuildActivityOverviewActivityLevel.none
        self.score = 0
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # level
        level = self.level
        repr_parts.append(' level = ')
        repr_parts.append(level.name)
        repr_parts.append(' ~ ')
        repr_parts.append(repr(level.value))
        
        # score
        repr_parts.append(', score = ')
        repr_parts.append(repr(self.score))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns hash(self)."""
        hash_value = 0
        
        # level
        hash_value ^= hash(self.level)
        
        # score
        hash_value ^= self.score
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        # level
        if self.level is not other.level:
            return False
        
        # score
        if self.score != other.score:
            return False
        
        return True
        
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new activity information.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Channel data receive from Discord.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.level = parse_level(data)
        self.score = parse_score(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Serializes the guild activity overview activity.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default field values should be included.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        put_level(self.level, data, defaults)
        put_score(self.score, data, defaults)
        return data
    
    
    def copy(self):
        """
        Copies the guild activity overview activity.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.level = self.level
        new.score = self.score
        return new
    
    
    def copy_with(self, *, level = ..., score = ...):
        """
        Copies the guild activity overview activity with the given fields.
        
        Parameters
        ----------
        level : `None | GuildActivityOverviewActivityLevel | int`, Optional (Keyword only)
            The activity's level.
        
        score : `int`, Optional (Keyword only)
            Total accumulated score.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value in incorrect.
        """
        # level
        if level is ...:
            level = self.level
        else:
            level = validate_level(level)
        
        # score
        if score is ...:
            score = self.score
        else:
            score = validate_score(score)
        
        # Construct
        new = object.__new__(type(self))
        new.level = level
        new.score = score
        return new
