__all__ = ('MessageActivity', )

from .preinstanced import MessageActivityType


class MessageActivity:
    """
    Might be sent with a ``Message``, if it has rich presence-related chat embeds.
    
    Attributes
    ----------
    party_id : `str`
        The message application's party's id. Can be empty string.
    type : ``MessageActivityType``
        The message application's type.
    """
    __slots__ = ('party_id', 'type',)
    
    def __init__(self, data):
        """
        Creates a new ``MessageActivity`` from message activity data included inside of a ``Message``'s data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Message activity data.
        """
        self.party_id = data.get('party_id', '')
        self.type = MessageActivityType.get(data['type'])

    def __eq__(self, other):
        """Returns whether the two message activities are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.type is not other.type:
            return False
        
        if self.party_id != other.party_id:
            return False
        
        return True
    
    def __repr__(self):
        """Returns the message activity's representation."""
        return f'<{self.__class__.__name__} type={self.type.name} ({self.type.value}), party_id={self.party_id!r}>'
    
    
    def to_data(self):
        """
        Tries to convert the message activity back to json serializable dictionary.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`)
        """
        return {
            'party_id': self.party_id,
            'type': self.type.value,
        }
