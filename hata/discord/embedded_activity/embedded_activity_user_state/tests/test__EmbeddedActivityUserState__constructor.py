import vampytest

from ....user import ClientUserBase, User

from ..constants import SESSION_ID_LENGTH_MIN
from ..embedded_activity_user_state import EmbeddedActivityUserState


def _assert_fields_set(embedded_activity_user_state):
    """
    Asserts whether every fields are set of the given embedded activity user state.
    
    Parameters
    ----------
    embedded_activity_user_state : ``EmbeddedActivityUserState``
        The embedded activity user state to test.
    """
    vampytest.assert_instance(embedded_activity_user_state, EmbeddedActivityUserState)
    vampytest.assert_instance(embedded_activity_user_state.nonce, str, nullable = True)
    vampytest.assert_instance(embedded_activity_user_state.session_id, str)
    vampytest.assert_instance(embedded_activity_user_state.user, ClientUserBase)


def test__EmbeddedActivityUserState__new__no_fields():
    """
    Tests whether ``EmbeddedActivityUserState.__new__`` works as intended.
    
    Case: no fields given.
    """
    embedded_activity_user_state = EmbeddedActivityUserState()
    _assert_fields_set(embedded_activity_user_state)


def test__EmbeddedActivityUserState__new__all_fields():
    """
    Tests whether ``EmbeddedActivityUserState.__new__`` works as intended.
    
    Case: all fields given.
    """
    nonce = 'miau'
    session_id = 'a' * SESSION_ID_LENGTH_MIN
    user = User.precreate(202409010013)
    
    embedded_activity_user_state = EmbeddedActivityUserState(
        nonce = nonce,
        session_id = session_id,
        user = user,
    )
    _assert_fields_set(embedded_activity_user_state)
    
    vampytest.assert_eq(embedded_activity_user_state.nonce, nonce)
    vampytest.assert_eq(embedded_activity_user_state.session_id, session_id)
    vampytest.assert_is(embedded_activity_user_state.user, user)
