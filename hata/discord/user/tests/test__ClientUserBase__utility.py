import vampytest

from ...client import Client

from .. import ClientUserBase


def test__ClientUserBase__from_client():
    """
    Issue: `AttributeError` in `ClientUserBase._from_client`.
    
    Could happen when the client had no thread profiles.
    """
    client = Client('token_20220718')
    try:
        vampytest.assert_is(client.thread_profiles, None)
        
        user = ClientUserBase._from_client(client)
        
        vampytest.assert_is(user.thread_profiles, None)
        vampytest.assert_eq(client.id, user.id)
    finally:
        client._delete()
        client = None
