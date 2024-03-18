import vampytest

from ...channel import Channel
from ...guild import Guild
from ...role import Role
from ...user import User


from ..utils import is_allowed_mentions_element_valid


def _iter_options():
    yield 'everyone', True
    yield 'users', True
    yield 'roles', True
    yield 'replied_user', True
    yield '!replied_user', True
    
    yield 'role', False
    yield 'user', False
    yield 'you', False
    yield 'koishi', False
    
    yield None, False
    yield object(), False
    yield 514, False
    
    yield User.precreate(202402140000), True
    yield Role.precreate(202402140001), True
    
    yield Channel.precreate(202402140002), False
    yield Guild.precreate(202402140003), False


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__is_allowed_mentions_element_valid(input_value):
    """
    Tests whether ``is_allowed_mentions_element_valid`` work as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to test.
    
    Returns
    -------
    output : `bool`
    """
    output = is_allowed_mentions_element_valid(input_value)
    vampytest.assert_instance(output, bool)
    return output
