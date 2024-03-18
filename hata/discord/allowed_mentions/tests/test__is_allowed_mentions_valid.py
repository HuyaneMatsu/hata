import vampytest

from ..proxy import AllowedMentionProxy
from ..utils import is_allowed_mentions_valid


def _iter_options():
    yield [], True
    yield set(), True
    yield (), True
    
    yield ['everyone', 'users', 'roles', 'replied_user', '!replied_user'], True
    yield ['koishi'], False
    
    yield AllowedMentionProxy(), True
    yield None, True
    yield object(), False
    yield 514, False


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__is_allowed_mentions_valid(input_value):
    """
    Tests whether ``is_allowed_mentions_valid`` work as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to test.
    
    Returns
    -------
    output : `bool`
    """
    output = is_allowed_mentions_valid(input_value)
    vampytest.assert_instance(output, bool)
    return output
