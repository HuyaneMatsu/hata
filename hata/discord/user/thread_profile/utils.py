__all__ = (
    'create_user_from_thread_user_data', 'thread_user_create', 'thread_user_delete', 'thread_user_difference_update',
    'thread_user_pop'
)

from scarletio import include

from ..user import User, create_partial_user_from_id

from .thread_profile import ThreadProfile

Client = include('Client')


def create_user_from_thread_user_data(thread_channel, thread_user_data):
    """
    Parses the user out from the given thread profile data.
    
    Parameters
    ----------
    thread_channel : ``Channel``
        The respective thread.
    thread_user_data : `dict` of (`str`, `object`) items
        Received thread profile data.
    
    Returns
    -------
    user : ``ClientUserBase``
    """
    try:
        guild_profile_data = thread_user_data['member']
    except KeyError:
        pass
    else:
        try:
            user_data = guild_profile_data['user']
        except KeyError:
            pass
        else:
            return User.from_data(user_data, guild_profile_data, thread_channel.guild_id)
    
    return create_partial_user_from_id(int(thread_user_data['user_id']))


def thread_user_create(thread_channel, user, thread_profile_data):
    """
    Resolves the given thread profile data.
    
    Parameters
    ----------
    thread_channel : ``Channel``
        The respective thread.
    user : ``ClientUserBase``
        The respective user to add or update in the thread.
    thread_profile_data : `dict` of (`str`, `object`) items
        Received thread profile data.
    
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
        thread_profiles[thread_channel.id] = ThreadProfile.from_data(thread_profile_data)
        created = True
    else:
        thread_profile._update_attributes(thread_profile_data)
        created = False
    
    return created


def thread_user_difference_update(thread_channel, user, thread_profile_data):
    """
    Resolves the given thread profile update.
    
    Parameters
    ----------
    thread_channel : ``Channel``
        The respective thread.
    user : ``ClientUserBase``
        The respective user to add or update in the thread.
    thread_profile_data : `dict` of (`str`, `object`) items
        Received thread profile data.
    
    Returns
    -------
    old_attributes : `None`, `dict` of (`str`, `object`) items
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
        thread_profiles[thread_channel.id] = ThreadProfile.from_data(thread_profile_data)
        return None
    
    old_attributes = thread_profile._difference_update_attributes(thread_profile_data)
    if not old_attributes:
        old_attributes = None
    
    return old_attributes


def thread_user_delete(thread_channel, user_id):
    """
    Removes the user for the given id from the thread's users.
    
    Parameters
    ----------
    thread_channel : ``Channel``
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
    thread_channel : ``Channel``
        The respective thread.
    user_id : `int`
        The respective user's identifier.
    me : ``Client``
        The client who pops the user.
    
    Returns
    -------
    popped : `None`, `tuple` (``ClientUserBase``, ``ThreadProfile``) item
        The removed user and it's profile if any.
    """
    thread_users = thread_channel.thread_users
    if (thread_users is not None):
        try:
            user = thread_users[user_id]
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
                    
                    # at the above condition we dont wanna pop obviously.
                    try:
                        del thread_users[user_id]
                    except KeyError:
                        pass
                    else:
                        if not thread_users:
                            thread_channel.thread_users = None
                
                if (thread_profile is not None):
                    return user, thread_profile
