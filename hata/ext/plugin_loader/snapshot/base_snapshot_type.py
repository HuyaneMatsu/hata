__all__ = ('BaseSnapshotType',)

from scarletio import RichAttributeErrorBaseType, WeakReferer


SNAPSHOT_TYPES = set()


class BaseSnapshotType(RichAttributeErrorBaseType):
    """
    Base class for snapshots.
    
    Attributes
    ----------
    _client_reference : `WeakReferer` to `Client`
        Weakreference to the owner client instance.
    _is_difference : `bool`
        Whether the snapshot is a difference.
    """
    __slots__ = ('_client_reference', '_is_difference')
    
    def __new__(cls, client):
        """
        Takes a snapshot.
        
        Parameters
        ----------
        client : ``Client``
            The client to take snapshot of.
        """
        client_reference = WeakReferer(client)
        
        self = object.__new__(cls)
        self._client_reference = client_reference
        self._is_difference = False
        return self
    
    
    def __repr__(self):
        """Returns the snapshot's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        client = self.client
        if (client is not None):
            repr_parts.append(' of ')
            repr_parts.append(repr(client))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __sub__(self, other):
        """Subtracts other from self."""
        if other is None:
            return self
        
        if type(self) is not type(other):
            return NotImplemented
        
        return self._extract(other)
    
    
    def _extract(self, other):
        """
        Extracts `other` from `self` returning a new snapshot, but this time a difference.
        
        Parameters
        ----------
        other : ``BaseSnapshotType``
            Other snapshot to extract from self.
        
        Returns
        -------
        difference : ``BaseSnapshotType``
        
        """
        if (self._is_difference != other._is_difference):
            raise RuntimeError(
                f'Only same kind of snapshot can be extracted, got self={self!r}; other={other!r}.'
            )
            
        new = object.__new__(type(self))
        new._client_reference = self._client_reference
        new._is_difference = True
        return new
    
    
    def __init_subclass__(cls):
        """
        Registers the subclasses as snapshot types.
        """
        SNAPSHOT_TYPES.add(cls)
    
    
    @property
    def client(self):
        """
        Returns the snapshot's client.
        """
        return self._client_reference()
    
    
    def is_revertible(self):
        """
        Returns whether self can be reverted.
        
        Returns
        -------
        is_revertible : `bool`
        """
        if not self._is_difference:
            return False
        
        if self._client_reference() is None:
            return False
        
        return True
    
    
    def revert(self):
        """
        Reverts the snapshot.
        """
        pass
    
    
    def __bool__(self):
        """Returns whether the snapshot contains any changes."""
        return False
