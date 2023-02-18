__all__ = ('ForumTagChange',)

from scarletio import RichAttributeErrorBaseType

from .fields import validate_added, validate_updated, validate_removed


class ForumTagChange(RichAttributeErrorBaseType):
    """
    Represents a user's changed forum tags.
    
    Attributes
    ----------
    added : `None`, `list` of ``ForumTag``
        The added forum tags to the respective user. Defaults to `None`.
    removed: `None`, `list` of ``ForumTag``
        The removed forum tags from the respective user. Defaults to `None`.
    updated : `None`, `list` of ``ForumTagUpdate``
        The updated forum tags of the respective user. Defaults to `None`.
    """
    __slots__ = ('added', 'updated', 'removed',)
    
    def __new__(cls, *, added = ..., removed = ..., updated = ...):
        """
        Creates a new forum tag change with the given parameters.
        
        Parameters
        ----------
        added : `None`, `iterable` of ``ForumTag``, Optional (Keyword only)
            The added forum tags to the user.
        removed: `None`, `iterable` of ``ForumTag``, Optional (Keyword only)
            The removed forum tags from the user.
        updated : `None`, `iterable` of ``ForumTagUpdate``, Optional (Keyword only)
            The updated forum tags of the user.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # added
        if added is ...:
            added = None
        else:
            added = validate_added(added)
        
        # removed
        if removed is ...:
            removed = None
        else:
            removed = validate_removed(removed)
        
        # updated
        if updated is ...:
            updated = None
        else:
            updated = validate_updated(updated)
        
        # Construct
        self = object.__new__(cls)
        self.added = added
        self.removed = removed
        self.updated = updated
        return self
    
    
    @classmethod
    def from_fields(cls, added, updated, removed):
        """
        Creates a new forum tag change with the given parameters.
        
        Parameters
        ----------
        added : `None`, `list` of ``ForumTag``
            The added forum tags to the user.
        updated : `None`, `list` of ``ForumTagUpdate``
            The updated forum tags of the user.
        removed: `None`, `list` of ``ForumTag``
            The removed forum tags from the user.
        """
        self = object.__new__(cls)
        self.added = added
        self.removed = removed
        self.updated = updated
        return self
    
    
    def __repr__(self):
        """Returns the representation of the forum tag change."""
        repr_parts = ['<',
            self.__class__.__name__,
        ]
        
        added = self.added
        if added is None:
            field_added = False
        else:
            repr_parts.append(' added = ')
            repr_parts.append(repr(added))
            field_added = True
        
        updated = self.updated
        if (updated is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' updated = ')
            repr_parts.append(repr(updated))
        
        removed = self.removed
        if (removed is not None):
            if field_added:
                repr_parts.append(',')
            
            repr_parts.append(' removed = ')
            repr_parts.append(repr(removed))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the forum tag change's hash value."""
        hash_value = 0
        
        added = self.added
        if (added is not None):
            hash_value ^= len(added)
            
            for forum_tag in added:
                hash_value ^= hash(forum_tag)
        
        removed = self.removed
        if (removed is not None):
            hash_value ^= len(removed) << 8
            
            for forum_tag in removed:
                hash_value ^= hash(forum_tag)
        
        updated = self.updated
        if (updated is not None):
            hash_value ^= len(updated) << 4
            
            for forum_tag_update in updated:
                hash_value ^= hash(forum_tag_update)
        
        return hash_value
    
    
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.added != other.added:
            return False
        
        if self.removed != other.removed:
            return False
        
        if self.updated != other.updated:
            return False
        
        return True
    
    
    def __len__(self):
        """Helper for unpacking if needed."""
        return 3
    
    
    def __iter__(self):
        """
        Unpacks the forum tag change.
        
        This method is a generator.
        """
        yield self.added
        yield self.updated
        yield self.removed
    
    
    def iter_added(self):
        """
        Iterates over the added forum tags.
        
        This method is an iterable generator.
        
        Yields
        ------
        added : ``ForumTag``
        """
        added = self.added
        if (added is not None):
            yield from added
    
    
    def iter_updated(self):
        """
        Iterates over the forum tag updates.
        
        This method is an iterable generator.
        
        Yields
        ------
        updated : ``ForumTagUpdate``
        """
        updated = self.updated
        if (updated is not None):
            yield from updated
    
    
    def iter_removed(self):
        """
        Iterates over the removed forum tags.
        
        This method is an iterable generator.
        
        Yields
        ------
        removed : ``ForumTag``
        """
        removed = self.removed
        if (removed is not None):
            yield from removed
    
    
    def copy(self):
        """
        Copies the forum tag change.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        added = self.added
        if (added is not None):
            added = [forum_tag.copy() for forum_tag in added]
        
        removed = self.removed
        if (removed is not None):
            removed = [forum_tag.copy() for forum_tag in removed]
        
        updated = self.updated
        if (updated is not None):
            updated = [forum_tag_update.copy() for forum_tag_update in updated]
        
        new = object.__new__(type(self))
        new.added = added
        new.updated = updated
        new.removed = removed
        return new
    
    
    def copy_with(self, *, added = ..., removed = ..., updated = ...):
        """
        Copies the forum tag change with the given fields.
        
        Parameters
        ----------
        added : `None`, `iterable` of ``ForumTag``, Optional (Keyword only)
            The added forum tags to the user.
        removed: `None`, `iterable` of ``ForumTag``, Optional (Keyword only)
            The removed forum tags from the user.
        updated : `None`, `iterable` of ``ForumTagUpdate``, Optional (Keyword only)
            The updated forum tags of the user.
        
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
        # added
        if added is ...:
            added = self.added
            if (added is not None):
                added = [forum_tag.copy() for forum_tag in added]
        else:
            added = validate_added(added)
        
        # removed
        if removed is ...:
            removed = self.removed
            if (removed is not None):
                removed = [forum_tag.copy() for forum_tag in removed]
        else:
            removed = validate_removed(removed)
        
        # updated
        if updated is ...:
            updated = self.updated
            if (updated is not None):
                updated = [forum_tag_update.copy() for forum_tag_update in updated]
        else:
            updated = validate_updated(updated)
        
        # Construct
        new = object.__new__(type(self))
        new.added = added
        new.removed = removed
        new.updated = updated
        return new
