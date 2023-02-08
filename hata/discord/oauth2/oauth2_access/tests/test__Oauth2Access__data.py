import vampytest

from ..oauth2_access import Oauth2Access
from ..preinstanced import Oauth2Scope

from .test__Oauth2Access__constructor import _assert_fields_set


def test__Oauth2Access__from_data():
    """
    Tests whether ``Oauth2Access.from_data`` works as intended.
    """
    access_token = 'immortal'
    expires_after = 69
    redirect_url = 'https://orindance.party/'
    refresh_token = 'smoke'
    scopes = [Oauth2Scope.bot]
    
    data = {
        'access_token': access_token,
        'expires_in': expires_after,
        'refresh_token': refresh_token,
        'scope': ' '.join(scope.value for scope in scopes),
    }
    
    oauth2_access = Oauth2Access.from_data(data, redirect_url)
    _assert_fields_set(oauth2_access)
    
    vampytest.assert_eq(oauth2_access.access_token, access_token)
    vampytest.assert_eq(oauth2_access.expires_after, expires_after)
    vampytest.assert_eq(oauth2_access.redirect_url, redirect_url)
    vampytest.assert_eq(oauth2_access.refresh_token, refresh_token)
    vampytest.assert_eq(oauth2_access.scopes, tuple(scopes))


def test__Oauth2Access__to_data():
    """
    Tests whether ``Oauth2Access.to_data`` works as intended.
    """
    access_token = 'immortal'
    expires_after = 69
    refresh_token = 'smoke'
    scopes = [Oauth2Scope.bot]
    
    oauth2_access = Oauth2Access(
        access_token = access_token,
        expires_after = expires_after,
        refresh_token = refresh_token,
        scopes = scopes,
    )

    expected_output = {
        'access_token': access_token,
        'expires_in': expires_after,
        'refresh_token': refresh_token,
        'scope': ' '.join(scope.value for scope in scopes),
    }
    
    vampytest.assert_eq(
        oauth2_access.to_data(defaults = True),
        expected_output,
    )


def test__Oauth2Access__renew():
    """
    Tests whether ``Oauth2Access._renew`` works as intended.
    """
    access_token = 'immortal'
    expires_after = 69
    refresh_token = 'smoke'
    scopes = [Oauth2Scope.bot]
    
    data = {
        'access_token': access_token,
        'expires_in': expires_after,
        'refresh_token': refresh_token,
        'scope': ' '.join(scope.value for scope in scopes),
    }
    
    oauth2_access = Oauth2Access()
    oauth2_access._renew(data)
    
    vampytest.assert_eq(oauth2_access.access_token, access_token)
    vampytest.assert_eq(oauth2_access.expires_after, expires_after)
    vampytest.assert_eq(oauth2_access.refresh_token, refresh_token)
    vampytest.assert_eq(oauth2_access.scopes, tuple(scopes))
