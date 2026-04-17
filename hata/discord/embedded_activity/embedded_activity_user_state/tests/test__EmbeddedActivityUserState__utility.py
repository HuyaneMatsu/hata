import vampytest

from ....user import User

from ..constants import SESSION_ID_LENGTH_MIN
from ..embedded_activity_user_state import EmbeddedActivityUserState

from .test__EmbeddedActivityUserState__constructor import _assert_fields_set


def test__EmbeddedActivityUserState__copy():
    """
    Tests whether ``EmbeddedActivityUserState.copy`` works as intended.
    """
    nonce = 'miau'
    session_id = 'a' * SESSION_ID_LENGTH_MIN
    user = User.precreate(202409010022)
    
    embedded_activity_user_state = EmbeddedActivityUserState(
        nonce = nonce,
        session_id = session_id,
        user = user,
    )
    
    copy = embedded_activity_user_state.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, embedded_activity_user_state)
    
    vampytest.assert_eq(copy, embedded_activity_user_state)


def test__EmbeddedActivityUserState__copy_with__no_fields():
    """
    Tests whether ``EmbeddedActivityUserState.copy_with`` works as intended.
    
    Case: No fields given.
    """
    nonce = 'miau'
    session_id = 'a' * SESSION_ID_LENGTH_MIN
    user = User.precreate(202409010023)
    
    embedded_activity_user_state = EmbeddedActivityUserState(
        nonce = nonce,
        session_id = session_id,
        user = user,
    )
    
    copy = embedded_activity_user_state.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, embedded_activity_user_state)
    
    vampytest.assert_eq(copy, embedded_activity_user_state)


def test__EmbeddedActivityUserState__copy_with__all_fields():
    """
    Tests whether ``EmbeddedActivityUserState.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_nonce = 'miau'
    old_session_id = 'a' * SESSION_ID_LENGTH_MIN
    old_user = User.precreate(202409010024)
        
    new_nonce = 'meow'
    new_session_id = 'b' * SESSION_ID_LENGTH_MIN
    new_user = User.precreate(202409010025)
    
    embedded_activity_user_state = EmbeddedActivityUserState(
        nonce = old_nonce,
        session_id = old_session_id,
        user = old_user,
    )
    
    copy = embedded_activity_user_state.copy_with(
        nonce = new_nonce,
        session_id = new_session_id,
        user = new_user,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, embedded_activity_user_state)
    
    vampytest.assert_ne(copy, embedded_activity_user_state)
    
    vampytest.assert_eq(copy.nonce, new_nonce)
    vampytest.assert_eq(copy.session_id, new_session_id)
    vampytest.assert_is(copy.user, new_user)
