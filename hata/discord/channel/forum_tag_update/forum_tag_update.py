__all__ = ('ForumTagUpdate',)

from itertools import count

from scarletio import RichAttributeErrorBaseType

from ..forum_tag import ForumTag

from .fields import validate_forum_tag, validate_old_attributes


class ForumTagUpdate(RichAttributeErrorBaseType):
    """
    Represents an updated forum tag with storing the forum tag and it's old updated attributes in a `dict`.
    
    Attributes
    ----------
    forum_tag : ``ForumTag``
        The updated forum tag.
    old_attributes : `dict` of (`str`, `object`) items
        The changed attributes of the forum tag in `attribute-name` - `old-value` relation. Can contain any of the
        following items:
        
        +-----------+-------------------+
        | Keys      | Values            |
        +===========+===================+
        | emoji     | `None`, ``Emoji`` |
        +-----------+-------------------+
        | name      | `str`             |
        +-----------+-------------------+
        | moderated | `bool`            |
        +-----------+-------------------+
    """
    __slots__ = ('forum_tag', 'old_attributes',)
    
    def __new__(cls, forum_tag = ..., old_attributes = ...):
        """
        Creates a new forum tag change instance with the given fields.
        
        Parameters
        ----------
        forum_tag : ``ForumTag``, Optional (Keyword only)
            The updated forum tag.
        old_attributes : `None`, `dict` of (`str`, `object`) items, Optional (Keyword only)
            The changed attributes of the forum tag.
        
        Raises
        ------
        TypeError
            - If a field's type is incorrect.
        """
        # forum_tag
        if forum_tag is ...:
            forum_tag = ForumTag()
        else:
            forum_tag = validate_forum_tag(forum_tag)
        
        # old_attributes
        if old_attributes is ...:
            old_attributes = {}
        else:
            old_attributes = validate_old_attributes(old_attributes)
        
        # Construct
        self = object.__new__(cls)
        self.forum_tag = forum_tag
        self.old_attributes = old_attributes
        return self
    
    
    @classmethod
    def from_fields(cls, forum_tag, old_attributes):
        """
        Creates a new forum tag change instance with the given fields.
        
        Parameters
        ----------
        forum_tag : ``ForumTag``
            The updated forum tag.
        old_attributes : `dict` of (`str`, `object`) items
            The changed attributes of the forum tag.
        
        Returns
        -------
        new : `instance<cls>`
        """
        self = object.__new__(cls)
        self.forum_tag = forum_tag
        self.old_attributes = old_attributes
        return self
    
    
    def __repr__(self):
        """Returns the representation of the forum tag update."""
        return f'<{self.__class__.__name__} changes: {len(self.old_attributes)!r}, forum_tag = {self.forum_tag!r}>'
    
    
    def __hash__(self):
        """Returns the forum tag update's hash value."""
        hash_value = 0
        
        # forum_tag
        hash_value ^= hash(self.forum_tag)
        
        # old_attributes
        old_attributes = self.old_attributes
        hash_value ^= len(old_attributes)
        
        for mask, key in zip(count(5, 7), sorted(old_attributes.keys())):
            hash_value ^= (mask | hash(key)) & hash(old_attributes[key])
        
        return hash_value
    
    
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.forum_tag != other.forum_tag:
            return False
        
        if self.old_attributes != other.old_attributes:
            return False
        
        return True
    
    
    def __len__(self):
        """Helper for unpacking if needed."""
        return 2
    
    
    def __iter__(self):
        """
        Unpacks the forum tag update.
        
        This method is a generator.
        """
        yield self.forum_tag
        yield self.old_attributes
    
    
    def copy(self):
        """
        Copies the forum_tag update.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.forum_tag = self.forum_tag.copy()
        new.old_attributes = self.old_attributes.copy()
        return new
    
    
    def copy_with(self, *, forum_tag = ..., old_attributes = ...):
        """
        Copies the forum tag change with the given fields.
        
        Parameters
        ----------
        forum_tag : ``ForumTag``, Optional (Keyword only)
            The updated forum_tag.
        old_attributes : `None`, `dict` of (`str`, `object`) items, Optional (Keyword only)
            The changed attributes of the forum tag.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a field's type is incorrect.
        """
        # forum_tag
        if forum_tag is ...:
            forum_tag = self.forum_tag.copy()
        else:
            forum_tag = validate_forum_tag(forum_tag)
        
        # old_attributes
        if old_attributes is ...:
            old_attributes = self.old_attributes.copy()
        else:
            old_attributes = validate_old_attributes(old_attributes)
        
        # Construct
        new = object.__new__(type(self))
        new.forum_tag = forum_tag
        new.old_attributes = old_attributes
        return new
