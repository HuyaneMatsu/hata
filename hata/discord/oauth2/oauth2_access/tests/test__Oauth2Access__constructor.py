from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..oauth2_access import Oauth2Access
from ..preinstanced import Oauth2Scope


def _assert_fields_set(oauth2_access):
    """
    Asserts whether every fields are set of the given oauth2 access.
    
    Parameters
    ----------
    oauth2_access : ``Oauth2Access``
        The oauth2 access to check.
    """
    vampytest.assert_instance(oauth2_access, Oauth2Access)
    vampytest.assert_instance(oauth2_access.access_token, str)
    vampytest.assert_instance(oauth2_access.created_at, DateTime)
    vampytest.assert_instance(oauth2_access.expires_after, int)
    vampytest.assert_instance(oauth2_access.redirect_url, str)
    vampytest.assert_instance(oauth2_access.refresh_token, str)
    vampytest.assert_instance(oauth2_access.scopes, tuple, nullable = True)


def test__Oauth2Access__new__0():
    """
    Tests whether ``Oauth2Access.__new__`` works as intended.
    
    Case: No fields given.
    """
    oauth2_access = Oauth2Access()
    _assert_fields_set(oauth2_access)


def test__Oauth2Access__new__1():
    """
    Tests whether ``Oauth2Access.__new__`` works as intended.
    
    Case: All fields given.
    """
    access_token = 'immortal'
    created_at = DateTime(2016, 5, 4, tzinfo = TimeZone.utc)
    expires_after = 69
    redirect_url = 'https://orindance.party/'
    refresh_token = 'smoke'
    scopes = [Oauth2Scope.bot]
    
    oauth2_access = Oauth2Access(
        access_token = access_token,
        created_at = created_at,
        expires_after = expires_after,
        redirect_url = redirect_url,
        refresh_token = refresh_token,
        scopes = scopes,
    )
    _assert_fields_set(oauth2_access)
    
    vampytest.assert_eq(oauth2_access.access_token, access_token)
    vampytest.assert_eq(oauth2_access.created_at, created_at)
    vampytest.assert_eq(oauth2_access.expires_after, expires_after)
    vampytest.assert_eq(oauth2_access.redirect_url, redirect_url)
    vampytest.assert_eq(oauth2_access.refresh_token, refresh_token)
    vampytest.assert_eq(oauth2_access.scopes, tuple(scopes))
