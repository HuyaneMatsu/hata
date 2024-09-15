import vampytest

from ....user import ClientUserBase, User

from ..constants import SESSION_ID_LENGTH_MIN
from ..embedded_activity_user_state import EmbeddedActivityUserState


def test__EmbeddedActivityUserState__repr():
    """
    Tests whether ``EmbeddedActivityUserState.__repr__`` works as intended.
    """
    nonce = 'miau'
    session_id = 'a' * SESSION_ID_LENGTH_MIN
    user = User.precreate(202409010018)
    
    embedded_activity_user_state = EmbeddedActivityUserState(
        nonce = nonce,
        session_id = session_id,
        user = user,
    )
    
    output = repr(embedded_activity_user_state)
    vampytest.assert_instance(output, str)


def test__EmbeddedActivityUserState__hash():
    """
    Tests whether ``EmbeddedActivityUserState.__hash__`` works as intended.
    """
    nonce = 'miau'
    session_id = 'a'* SESSION_ID_LENGTH_MIN
    user = User.precreate(202409010019)
    
    embedded_activity_user_state = EmbeddedActivityUserState(
        nonce = nonce,
        session_id = session_id,
        user = user,
    )
    
    output = hash(embedded_activity_user_state)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    nonce = 'miau'
    session_id = 'a' * SESSION_ID_LENGTH_MIN
    user = User.precreate(202409010020)
    
    keyword_parameters = {
        'nonce': nonce,
        'session_id': session_id,
        'user': user,
    }
    
    yield (
        {},
        {},
        True,
    )
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'nonce': 'meow',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'session_id': 'b' * SESSION_ID_LENGTH_MIN,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'user': User.precreate(202409010021),
        },
        False,
    )

@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__EmbeddedActivityUserState__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``EmbeddedActivityUserState.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    embedded_activity_user_state_0 = EmbeddedActivityUserState(**keyword_parameters_0)
    embedded_activity_user_state_1 = EmbeddedActivityUserState(**keyword_parameters_1)
    
    output = embedded_activity_user_state_0 == embedded_activity_user_state_1
    vampytest.assert_instance(output, bool)
    return output
