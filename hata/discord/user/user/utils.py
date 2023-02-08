__all__ = ('ZEROUSER', 'create_partial_user_from_id', )

from scarletio import export

from ...core import USERS

from .user import User


@export
def create_partial_user_from_id(user_id):
    """
    Creates a partial user from the given `user_id`. If the user already exists returns that instead.
    
    Parameters
    ----------
    user_id : `int`
        The unique identifier number of the user.
    
    Returns
    -------
    user : ``ClientUserBase``
    """
    try:
        return USERS[user_id]
    except KeyError:
        pass
    
    user = User._create_empty(user_id)
    USERS[user_id] = user
    return user


ZEROUSER = create_partial_user_from_id(0)
export(ZEROUSER, 'ZEROUSER')
