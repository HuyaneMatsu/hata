__all__ = ('ActivityMetadataBase',)

from scarletio import RichAttributeErrorBaseType

from ...bases import PlaceHolder

from .flags import ActivityFlag


def _pop_empty_name(keyword_parameters):
    """
    Pops empty name from the given keyword parameters.

    Parameters
    ----------
    keyword_parameters : `dict` of (`str`, `object`) items
        Keyword parameters passed to ``Activity.__new__``
    """
    try:
        name = keyword_parameters['name']
    except KeyError:
        pass
    else:
        if (name is None) or (not name):
            del keyword_parameters['name']


class ActivityMetadataBase(RichAttributeErrorBaseType):
    """
    Base class for activity metadatas.
    """
    __slots__ = ()
    
    def __new__(cls):
        """
        Creates a new activity metadata.
        
        Raises
        ------
        TypeError
            - If a parameter's type is unexpected.
        ValueError
           - If an parameter's value is unexpected.
        """
        return object.__new__(cls)
    
    
    @classmethod
    def from_keyword_parameters(cls, keyword_parameters):
        """
        Creates a new activity metadata from the given keyword parameters.
        
        Parameters
        ----------
        keyword_parameters : `dict` of (`str`, `object`) items
            Keyword parameters passed to ``Activity.__new__``
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is unexpected.
        ValueError
           - If an parameter's value is unexpected.
        """
        _pop_empty_name(keyword_parameters)
        return cls()
        
    
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
        data : `dict` of (`str`, `object`) items
            Activity data received from Discord.
        
        Returns
        -------
        self : `instance<cls>`
        """
        return object.__new__(cls)
    
    

    def to_data(self, *, defaults = False, include_internals = False, user = False):
        """
        Converts the activity metadata to json serializable dictionary, which can be sent with bot account to change
        activity.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with their default values should be included as well.
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields, like id-s should be present as well.
        user : `bool` = `False`, Optional (Keyword only)
            Whether not only bot compatible fields should be included.
        
        Returns
        -------
        activity_data : `dict` of (`str`, `object`) items
        """
        return {}
    
    
    def _update_attributes(self, data):
        """
        Updates the activity metadata by overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Data received from Discord.
        """
        pass
    
    
    def _difference_update_attributes(self, data):
        """
        Updates the activity metadata and returns the changes in a `dict` of (`attribute-name`, `old-value`) items.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Data received from Discord.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `object`) items
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
    
    
    def copy(self):
        """
        Copies the activity metadata.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        return object.__new__(type(self))
    
    
    def copy_with(self):
        """
        Copies the activity metadata with the given fields.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is unexpected.
        ValueError
           - If an parameter's value is unexpected.
        """
        return self.copy()
    
    
    def copy_with_keyword_parameters(self, keyword_parameters):
        """
        Copies the activity metadata with the given keyword parameters
        
        Parameters
        ----------
        keyword_parameters : `dict` of (`str`, `object`) items
            Keyword parameters passed to ``Activity.__new__``
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is unexpected.
        ValueError
           - If an parameter's value is unexpected.
        """
        _pop_empty_name(keyword_parameters)
        return self.copy_with()
    
    
    application_id = PlaceHolder(
        0,
        """
        Returns the activity's application id.
        
        Returns
        -------
        application_id : `int`
        """
    )
    
    
    assets = PlaceHolder(
        None,
        """
        Returns the activity's assets.
        
        Returns
        -------
        assets : `None`, ``ActivityAssets``
        """
    )
    
    
    created_at = PlaceHolder(
        None,
        """
        Returns when the activity was created.
        
        Returns
        -------
        created_at : `datetime`
        """
    )
    
    
    details = PlaceHolder(
        None,
        """
        Returns the activity's details.
        
        Returns
        -------
        assets : `None`, `str`
        """
    )

    
    
    emoji = PlaceHolder(
        None,
        """
        Returns the emoji of the activity. If it has no emoji, then set as `None`.
        
        Returns
        -------
        emoji : `None`, ``Emoji``
        """
    )
    
    
    flags = PlaceHolder(
        ActivityFlag(),
        """
        Returns the activity's flags.
        
        Returns
        -------
        assets : ``ActivityFlag``
        """
    )
    
    
    id = PlaceHolder(
        0,
        """
        Returns the activity's id.
        
        Returns
        -------
        id : `int`
        """
    )
    
    
    name = PlaceHolder(
        '',
        """
        Returns the activity's name.
        
        Returns
        -------
        name : `str`
        """
    )
    
    
    party = PlaceHolder(
        None,
        """
        Returns the activity's party.
        
        Returns
        -------
        party : `None`, ``ActivityParty``
        """
    )
    
    
    secrets = PlaceHolder(
        None,
        """
        Returns the activity's secrets.
        
        Returns
        -------
        secrets : `None`, ``ActivitySecrets``
        """
    )
    
    
    session_id = PlaceHolder(
        None,
        """
        Returns the activity's session identifier.
        
        Returns
        -------
        session_id : `None`, `str`
        """
    )

    
    state = PlaceHolder(
        None,
        """
        Returns the activity's state.
        
        > If the activity has ``.emoji`` it appears next to it.
        
        Returns
        -------
        state : `None`, `str`
        """
    )
    
    
    sync_id = PlaceHolder(
        None,
        """
        Returns the activity's sync identifier.
        
        Returns
        -------
        sync_id : `None`, `str`
        """
    )
    
    
    timestamps = PlaceHolder(
        None,
        """
        Returns the activity's timestamps.
        
        Returns
        -------
        timestamps : `None`, ``ActivityTimestamps``
        """
    )
    
    
    url = PlaceHolder(
        None,
        """
        Returns the activity's url.
        
        Returns
        -------
        url : `None`, `str`
        """
    )
