import vampytest

from ...oauth2_access import Oauth2Access, Oauth2Scope

from ..oauth2_user import Oauth2User


def test__Oauth2User__bot():
    """
    Tests whether ``Oauth2User.bot`` works as intended.
    """
    user = Oauth2User()
    output = user.bot
    vampytest.assert_instance(output, bool)
    vampytest.assert_false(output)


def test__Oauth2User__access_token():
    """
    Tests whether ``Oauth2User.access_token`` works as intended.
    """
    access_token = 'okuu'
    
    access = Oauth2Access(access_token = access_token)
    user = Oauth2User()
    user.access = access
    
    vampytest.assert_eq(user.access_token, access_token)


def test__Oauth2User__redirect_url():
    """
    Tests whether ``Oauth2User.redirect_url`` works as intended.
    """
    redirect_url = 'https://orindance.party/'
    
    access = Oauth2Access(redirect_url = redirect_url)
    user = Oauth2User()
    user.access = access
    
    vampytest.assert_eq(user.redirect_url, redirect_url)


def test__Oauth2User__refresh_token():
    """
    Tests whether ``Oauth2User.refresh_token`` works as intended.
    """
    refresh_token = 'okuu'
    
    access = Oauth2Access(refresh_token = refresh_token)
    user = Oauth2User()
    user.access = access
    
    vampytest.assert_eq(user.refresh_token, refresh_token)


def test__Oauth2User__scopes():
    """
    Tests whether ``Oauth2User.scopes`` works as intended.
    """
    scopes = (Oauth2Scope.bot, Oauth2Scope.email)
    
    access = Oauth2Access(scopes = scopes)
    user = Oauth2User()
    user.access = access
    
    vampytest.assert_eq(user.scopes, scopes)


def test__Oauth2User__has_scope():
    """
    Tests whether ``Oauth2User.has_scope`` works as intended.
    """
    scopes = (Oauth2Scope.bot, Oauth2Scope.email)
    
    access = Oauth2Access(scopes = scopes)
    user = Oauth2User()
    user.access = access
    
    vampytest.assert_true(user.has_scope(Oauth2Scope.email))
    vampytest.assert_false(user.has_scope(Oauth2Scope.rpc))


def test__Oauth2User__iter_scopes():
    """
    Tests whether ``Oauth2User.iter_scopes`` works as intended.
    """
    scopes = (Oauth2Scope.bot, Oauth2Scope.email)
    
    access = Oauth2Access(scopes = scopes)
    user = Oauth2User()
    user.access = access
    
    vampytest.assert_eq([*user.iter_scopes()], [*scopes])


def test__Oauth2User__renew():
    """
    Tests whether ``Oauth2User._renew`` works as intended.
    """
    access_token = 'immortal'
    
    data = {
        'access_token': access_token,
    }
    
    user = Oauth2User()
    user._renew(data)
    
    vampytest.assert_eq(user.access_token, access_token)
