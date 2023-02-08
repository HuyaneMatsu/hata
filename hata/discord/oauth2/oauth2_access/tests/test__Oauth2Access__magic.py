from datetime import datetime as DateTime

import vampytest

from ..oauth2_access import Oauth2Access
from ..preinstanced import Oauth2Scope


def test__Oauth2Access__repr():
    """
    Tests whether ``Oauth2Access.__repr__`` works as intended.
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
    
    vampytest.assert_instance(repr(oauth2_access), str)


def test__Oauth2Access__hash():
    """
    Tests whether ``Oauth2Access.__hash__`` works as intended.
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
    
    vampytest.assert_instance(hash(oauth2_access), int)


def test__Oauth2Access__eq():
    """
    Tests whether ``Oauth2Access.__eq__`` works as intended.
    """
    access_token = 'immortal'
    created_at = DateTime(2016, 5, 4)
    expires_after = 69
    redirect_url = 'https://orindance.party/'
    refresh_token = 'smoke'
    scopes = [Oauth2Scope.bot]
    
    keyword_parameters = {
        'access_token': access_token,
        'created_at': created_at,
        'expires_after': expires_after,
        'redirect_url': redirect_url,
        'refresh_token': refresh_token,
        'scopes': scopes,
    }
    
    oauth2_access = Oauth2Access(**keyword_parameters)
    vampytest.assert_eq(oauth2_access, oauth2_access)
    vampytest.assert_ne(oauth2_access, object())
    
    for field_name, field_value in (
        ('access_token', 'ashe'),
        ('created_at', DateTime(2016, 5, 5)),
        ('expires_after', 10000),
        ('redirect_url', 'https://www.astil.dev/'),
        ('refresh_token', 'of rogue'),
        ('scopes', [Oauth2Scope.bot, Oauth2Scope.email]),
    ):
        text_oauth2_access = Oauth2Access(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(oauth2_access, text_oauth2_access)
