__all__ = ('ActivityMetadataBase',)

from scarletio import RichAttributeErrorBaseType

from ..flags import ActivityFlag


ACTIVITY_DEFAULT_ATTRIBUTES = {
    'application_id': 0,
    'assets': None,
    'created_at': None,
    'details': None,
    'flags': ActivityFlag(),
    'emoji': None,
    'id': 0,
    'name': 'Unknown',
    'party': None,
    'secrets': None,
    'session_id': None,
    'state': None,
    'sync_id': None,
    'timestamps': None,
    'url': None,
}


class ActivityMetadataBase(RichAttributeErrorBaseType):
    """
    Base class for activity metadatas.
    """
    __slots__ = ()
    
    def __new__(cls, keyword_parameters):
        """
        Creates a new activity metadata.
        
        Parameters
        ----------
        keyword_parameters : `dict` of (`str`, `Any`) items
            Keyword parameters passed to ``Activity.__new__``
        
        Returns
        -------
        self : ``ActivityMetadataBase``
        
        Raises
        ------
        TypeError
            If any parameter's type is bad or if unexpected parameter is passed.
        ValueError
           If an parameter's type is good, but it's value is unacceptable.
        """
        # Remove empty name from `keyword_parameters` since that is the default name value and name is required.
        try:
            name = keyword_parameters['name']
        except KeyError:
            pass
        else:
            if (not name):
                del keyword_parameters['name']
        
        return object.__new__(cls)
    
    
    def __repr__(self):
        """Returns the activity metadata's representation."""
        return f'<{self.__class__.__name__}>'
    
    
    def __hash__(self):
        """Returns the activity metadata's hash value."""
        return 0
    
    
    def __eq__(self, other):
        """
        Returns whether the two activity metadatas are equal.
        """
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def __getattr__(self, attribute_name):
        """Returns the activity metadata's attribute if found."""
        try:
            return ACTIVITY_DEFAULT_ATTRIBUTES[attribute_name]
        except KeyError:
            pass
        
        return RichAttributeErrorBaseType.__getattr__(self, attribute_name)
    
    
    def _is_equal_same_type(self, other):
        """
        Returns whether the two types are equal.
        
        Helper method for ``.__eq__``
        
        Parameters
        ----------
        other : `type(self)`
            The other instance. Must be from the same type.
        
        Returns
        -------
        is_equal : `bool`
        """
        return True
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new activity metadata.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Activity data received from Discord.
        
        Returns
        -------
        self : ``ActivityMetadataBase``
        """
        return object.__new__(cls)
    
    

    def to_data(self):
        """
        Converts the activity metadata to json serializable dictionary, which can be sent with bot account to change
        activity.
        
        Returns
        -------
        activity_data : `dict` of (`str`, `Any`) items
        """
        return {}
    
    
    def to_data_user(self):
        """
        Converts the activity to json serializable dictionary, which can (?) be sent with user account to change
        activity.
        
        Returns
        -------
        activity_data : `dict` of (`str`, `Any`) items
        """
        return {}
    
    
    def to_data_full(self):
        """
        Converts the whole activity to a dictionary.
        
        Returns
        -------
        activity_data : `dict` of (`str`, `Any`) items
        """
        return {}
    
    
    def _update_attributes(self, data):
        """
        Updates the activity metadata by overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        """
        pass
    
    
    def _difference_update_attributes(self, data):
        """
        Updates the activity metadata and returns the changes in a `dict` of (`attribute-name`, `old-value`) items.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `Any`) items
            All item in the returned dict is optional.
        
        Returned Data Structure
        -----------------------
        +-------------------+-----------------------------------+
        | Keys              | Values                            |
        +===================+===================================+
        | assets            | `None`, ``ActivityAssets``        |
        +-------------------+-----------------------------------+
        | created_at        | `None`, `datetime`                |
        +-------------------+-----------------------------------+
        | details           | `None`, `str`                     |
        +-------------------+-----------------------------------+
        | emoji             | `None`, ``Emoji``                 |
        +-------------------+-----------------------------------+
        | flags             | ``ActivityFlag``                  |
        +-------------------+-----------------------------------+
        | name              | `str`                             |
        +-------------------+-----------------------------------+
        | metadata          | ``ActivityMetadataBase``          |
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
        return {}
