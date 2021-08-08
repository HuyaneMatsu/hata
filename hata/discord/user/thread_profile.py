__all__ = ('ThreadProfile', 'thread_user_create', 'thread_user_delete', 'thread_user_pop', 'thread_user_update')

from datetime import datetime

from ...backend.export import include

from ..utils import timestamp_to_datetime

from .flags import ThreadProfileFlag

create_partial_role_from_id = include('create_partial_role_from_id')
Client = include('Client')

def thread_user_create(thread_channel, user, thread_user_data):
    """
    Resolves the given thread user data.
    
    Parameters
    ----------
    thread_channel : ``ChannelThread``
        The respective thread.
    user : ``ClientUserBase``
        The respective user to add or update in the thread.
    thread_user_data : `dict` of (`str`, `Any`) items
        Received thread user data.
    
    Returns
    -------
    created : `bool`
        Whether a new thread profile was created.
    """
    thread_users = thread_channel.thread_users
    if thread_users is None:
        thread_users = thread_channel.thread_users = {}
    thread_users[user.id] = user
    
    thread_profiles = user.thread_profiles
    if thread_profiles is None:
        thread_profiles = user.thread_profiles = {}
    
    try:
        thread_profile = thread_profiles[thread_channel.id]
    except KeyError:
        thread_profiles[thread_channel.id] = ThreadProfile(thread_user_data)
        created = True
    else:
        thread_profile._update_attributes(thread_user_data)
        created = False
    
    return created


def thread_user_update(thread_channel, user, thread_user_data):
    """
    Resolves the given thread user update.
    
    Parameters
    ----------
    thread_channel : ``ChannelThread``
        The respective thread.
    user : ``ClientUserBase``
        The respective user to add or update in the thread.
    thread_user_data : `dict` of (`str`, `Any`) items
        Received thread user data.
    
    Returns
    -------
    old_attributes : `None` or `dict` of (`str`, `Any`) items
    """
    thread_users = thread_channel.thread_users
    if thread_users is None:
        thread_users = thread_channel.thread_users = {}
    thread_users[user.id] = user
    
    thread_profiles = user.thread_profiles
    if thread_profiles is None:
        thread_profiles = user.thread_profiles = {}
    
    try:
        thread_profile = thread_profiles[thread_channel.id]
    except KeyError:
        thread_profiles[thread_channel.id] = ThreadProfile(thread_user_data)
        return None
    
    old_attributes = thread_profile._update_attributes(thread_user_data)
    if not old_attributes:
        old_attributes = None
    
    return old_attributes


def thread_user_delete(thread_channel, user_id):
    """
    Removes the user for the given id from the thread's users.
    
    Parameters
    ----------
    thread_channel : ``ChannelThread``
        The respective thread.
    user_id : `int`
        The respective user's identifier.
    """
    thread_users = thread_channel.thread_users
    if (thread_users is not None):
        try:
            user = thread_users.pop(user_id)
        except KeyError:
            pass
        else:
            if not thread_users:
                thread_channel.thread_users = None
            
            thread_profiles = user.thread_profiles
            if (thread_profiles is not None):
                try:
                    del thread_profiles[thread_channel.id]
                except KeyError:
                    pass
                else:
                    if not thread_profiles:
                        user.thread_profiles = None


def thread_user_pop(thread_channel, user_id, me):
    """
    Removes and returns the user for the given id from the thread's users.
    
    Parameters
    ----------
    thread_channel : ``ChannelThread``
        The respective thread.
    user_id : `int`
        The respective user's identifier.
    me : ``Client``
        The client who pops the user.
    
    Returns
    -------
    popped : `None` or `tuple` (``ClientUserBase``, ``ThreadProfile``) item
        The removed user and it's profile if any.
    """
    thread_users = thread_channel.thread_users
    if (thread_users is not None):
        try:
            user = thread_users.pop(user_id)
        except KeyError:
            pass
        else:
            if not thread_users:
                thread_channel.thread_users = None
            
            thread_profiles = user.thread_profiles
            if (thread_profiles is not None):
                if isinstance(user, Client) and (user is not me):
                    thread_profile = thread_profiles.get(thread_channel.id, None)
                else:
                    try:
                        thread_profile = thread_profiles.pop(thread_channel.id)
                    except KeyError:
                        thread_profile = None
                    else:
                        if not thread_profiles:
                            user.thread_profiles = None
                        
                if (thread_profile is not None):
                    return user, thread_profile


class ThreadProfile:
    """
    Represents an user's profile inside of a thread channel.
    
    Attributes
    ----------
    joined_at : `datetime`
        The date when the user joined the thread.
    flags : ``ThreadProfileFlag``
        user specific settings of the profile.
    """
    __slots__ = ('joined_at', 'flags',)
    
    @property
    def created_at(self):
        """
        Returns ``.joined_at`` if set.
        
        Returns
        -------
        created_at : `datetime`
        """
        return self.joined_at
    
    def __init__(self, data):
        """
        Creates a new ``ThreadProfile`` instance from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received thread profile data.
        """
        self.joined_at = timestamp_to_datetime(data['join_timestamp'])
        
        self._update_attributes(data)
    
    def __repr__(self):
        """Returns the thread profile's representation."""
        return f'<{self.__class__.__name__}>'
    
    def _update_attributes(self, data):
        """
        Updates the thread profile with overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received thread profile data.
        """
        self.flags = ThreadProfileFlag(data['flags'])
    
    def _difference_update_attributes(self, data):
        """
        Updates the thread profile and returns it's changed attributes in a `dict` within `attribute-name` - `old-value`
        relation.
        
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
        
        +-------------------+-------------------------------+
        | Keys              | Values                        |
        +===================+===============================+
        | flags             | ``ThreadProfileFlag``         |
        +-------------------+-------------------------------+
        """
        old_attributes = {}
        
        flags = data.get('flags', 0)
        if self.flags != flags:
            old_attributes['flags'] = self.flags
            self.flags = ThreadProfileFlag(flags)
        
        return old_attributes
