__all__ = ('ZEROUSER', 'create_partial_user_from_id', )

from functools import partial as partial_func

from scarletio import export

from ...core import USERS

from .fields import (
    put_avatar_decoration, put_banner_color, put_display_name, put_name,
    validate_avatar_decoration, validate_banner_color, validate_display_name, validate_name
)
from .orin_user_base import USER_BANNER
from .user import User
from .user_base import USER_AVATAR


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


USER_SELF_FIELD_CONVERTERS = {
    'avatar': (
        partial_func(USER_AVATAR.validate_icon, allow_data = True),
        partial_func(USER_AVATAR.put_into, as_data = True),
    ),
    'avatar_decoration': (validate_avatar_decoration, put_avatar_decoration),
    'banner': (
        partial_func(USER_BANNER.validate_icon, allow_data = True),
        partial_func(USER_BANNER.put_into, as_data = True),
    ),
    'banner_color': (validate_banner_color, put_banner_color),
    'display_name': (validate_display_name, put_display_name),
    'name': (validate_name, put_name),
}
