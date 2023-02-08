from datetime import datetime as DateTime

import vampytest

from ..oauth2_access import Oauth2Access
from ..preinstanced import Oauth2Scope

from .test__Oauth2Access__constructor import _assert_fields_set


def test__Oauth2Access__copy():
    """
    Tests whether ``Oauth2Access.copy`` works as intended.
    """
    access_token = 'immortal'
    created_at = DateTime(2016, 5, 4)
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
    copy = oauth2_access.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, oauth2_access)
    
    vampytest.assert_eq(copy, oauth2_access)


def test__Oauth2Access__copy_with__0():
    """
    Tests whether ``Oauth2Access.copy_with`` works as intended.
    
    Case: No fields given.
    """
    access_token = 'immortal'
    created_at = DateTime(2016, 5, 4)
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
    copy = oauth2_access.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, oauth2_access)
    
    vampytest.assert_eq(copy, oauth2_access)


def test__Oauth2Access__copy_with__1():
    """
    Tests whether ``Oauth2Access.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_access_token = 'immortal'
    old_created_at = DateTime(2016, 5, 4)
    old_expires_after = 69
    old_redirect_url = 'https://orindance.party/'
    old_refresh_token = 'smoke'
    old_scopes = [Oauth2Scope.bot]
    new_access_token = 'reach'
    new_created_at = DateTime(2016, 5, 5)
    new_expires_after = 10000
    new_redirect_url = 'https://www.astil.dev/'
    new_refresh_token = 'moon'
    new_scopes = [Oauth2Scope.bot, Oauth2Scope.email]
    
    oauth2_access = Oauth2Access(
        access_token = old_access_token,
        created_at = old_created_at,
        expires_after = old_expires_after,
        redirect_url = old_redirect_url,
        refresh_token = old_refresh_token,
        scopes = old_scopes,
    )
    copy = oauth2_access.copy_with(
        access_token = new_access_token,
        created_at = new_created_at,
        expires_after = new_expires_after,
        redirect_url = new_redirect_url,
        refresh_token = new_refresh_token,
        scopes = new_scopes,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, oauth2_access)
    
    vampytest.assert_eq(copy.access_token, new_access_token)
    vampytest.assert_eq(copy.created_at, new_created_at)
    vampytest.assert_eq(copy.expires_after, new_expires_after)
    vampytest.assert_eq(copy.redirect_url, new_redirect_url)
    vampytest.assert_eq(copy.refresh_token, new_refresh_token)
    vampytest.assert_eq(copy.scopes, tuple(new_scopes))


def test__Oauth2Access__iter_scopes():
    """
    Tests whether `Oauth2Access.iter_scopes` works as intended.
    """
    for input_value, expected_output in (
        (None, []),
        ([Oauth2Scope.bot], [Oauth2Scope.bot]),
        ([Oauth2Scope.bot, Oauth2Scope.email], [Oauth2Scope.bot, Oauth2Scope.email]),
    ):
        oauth2_access = Oauth2Access(scopes = input_value)
        vampytest.assert_eq([*oauth2_access.iter_scopes()], expected_output)


def test__Oauth2Access__has_scopes():
    """
    Tests whether `Oauth2Access.has_scopes` works as intended.
    """
    for input_value, scope, expected_output in (
        (None, Oauth2Scope.bot, False),
        ([Oauth2Scope.bot], Oauth2Scope.bot, True),
        ([Oauth2Scope.bot], Oauth2Scope.email, False),
    ):
        oauth2_access = Oauth2Access(scopes = input_value)
        vampytest.assert_eq(oauth2_access.has_scope(scope), expected_output)
