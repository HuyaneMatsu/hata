__all__ = ('ActivityChange', 'ActivityUpdate',)

class ActivityChange:
    """
    Represents a user's changed activities.
    
    Attributes
    ----------
    added : `None`, `list` of ``ActivityBase``
        The added activities to the respective user. Defaults to `None`.
    updated : `None`, `list` of ``ActivityUpdate``
        The updated activities of the respective user. Defaults to `None`.
    removed: `None`, `list` of ``ActivityBase``
        The removed activities from the respective user. Defaults to `None`.
    """
    __slots__ = ('added', 'updated', 'removed',)
    
    def __init__(self, added, updated, removed):
        """
        Creates a new activity change with the given parameters.
        
        added : `None`, `list` of ``ActivityBase``
            The added activities to the user.
        updated : `None`, `list` of ``ActivityUpdate``
            The updated activities of the user.
        removed: `None`, `list` of ``ActivityBase``
            The removed activities from the user.
        """
        self.added = added
        self.updated = updated
        self.removed = removed
    
    def __repr__(self):
        """Returns the representation of the activity change."""
        repr_parts = ['<',
            self.__class__.__name__,
        ]
        
        added = self.added
        if added is None:
            field_added = False
        else:
            repr_parts.append(' added=')
            repr_parts.append(repr(added))
            field_added = True
        
        updated = self.updated
        if (updated is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' updated=')
            repr_parts.append(repr(updated))
        
        removed = self.removed
        if (removed is not None):
            if field_added:
                repr_parts.append(',')
            
            repr_parts.append(' removed=')
            repr_parts.append(repr(removed))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    def __len__(self):
        """Helper for unpacking if needed."""
        return 3
    
    def __iter__(self):
        """
        Unpacks the activity change.
        
        This method is a generator.
        """
        yield self.added
        yield self.updated
        yield self.removed


class ActivityUpdate:
    """
    Represents an updated activity with storing the activity and it's old updated attributes in a `dict`.
    
    Attributes
    ----------
    activity : ``ActivityBase``
        The updated activity.
    old_attributes : `dict` of (`str`, `Any`) items
        The changed attributes of the activity in `attribute-name` - `old-value` relation. Can contain any of the
        following items:
        
        +-------------------+-----------------------------------+
        | Keys              | Values                            |
        +===================+===================================+
        | application_id    | `int`                             |
        +-------------------+-----------------------------------+
        | assets            | `None`, ``ActivityAssets``        |
        +-------------------+-----------------------------------+
        | created_at        | `datetime`                        |
        +-------------------+-----------------------------------+
        | details           | `None`, `str`                     |
        +-------------------+-----------------------------------+
        | emoji             | `None`, ``Emoji``                 |
        +-------------------+-----------------------------------+
        | flags             | ``ActivityFlag``                  |
        +-------------------+-----------------------------------+
        | name              | `str`                             |
        +-------------------+-----------------------------------+
        | party             | `None`, ``ActivityParty``         |
        +-------------------+-----------------------------------+
        | secrets           | `None`, ``ActivitySecrets``       |
        +-------------------+-----------------------------------+
        | session_id        | `None`, `str`                     |
        +-------------------+-----------------------------------+
        | state             | `None`, `str`                     |
        +-------------------+-----------------------------------+
        | sync_id           | `None`, `str`                     |
        +-------------------+-----------------------------------+
        | timestamps        | `None`, `ActivityTimestamps``     |
        +-------------------+-----------------------------------+
        | url               | `None`, `str`                     |
        +-------------------+-----------------------------------+
    """
    __slots__ = ('activity', 'old_attributes',)
    
    def __init__(self, activity, old_attributes):
        """
        Creates a new activity change instance with the given parameters.
        
        activity : ``ActivityBase``
            The updated activity.
        old_attributes : `dict` of (`str`, `Any`) items
            The changed attributes of the activity.
        """
        self.activity = activity
        self.old_attributes = old_attributes
    
    def __repr__(self):
        """Returns the representation of the activity update."""
        return f'<{self.__class__.__name__} activity={self.activity!r} changes count={len(self.old_attributes)}>'
    
    def __len__(self):
        """Helper for unpacking if needed."""
        return 2
    
    def __iter__(self):
        """
        Unpacks the activity update.
        
        This method is a generator.
        """
        yield self.activity
        yield self.old_attributes
