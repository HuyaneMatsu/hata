import vampytest

from .. import Oauth2Access, Oauth2Scope


def _get_access_data():
    return {
        'access_token': 'a',
        'refresh_token': 'b',
        'expires_in': 1,
        'scopes': 'bot identify email',
    }


def test__Oauth2Access__has_scope_0():
    """
    Tests whether `Oauth2Access.has_scope` works as intended.
    
    Case : no data | Oauth2Scope
    """
    data = _get_access_data()
    data['scopes'] = ''
    
    access = Oauth2Access(data, '')
    scope = Oauth2Scope.bot
    
    vampytest.assert_eq(access.has_scope(scope), False)


def test__Oauth2Access__has_scope_1():
    """
    Tests whether `Oauth2Access.has_scope` works as intended.
    
    Case : no data | string
    """
    data = _get_access_data()
    data['scopes'] = ''
    
    access = Oauth2Access(data, '')
    scope = Oauth2Scope.bot
    
    vampytest.assert_eq(access.has_scope(scope.value), False)


def test__Oauth2Access__has_scope_2():
    """
    Tests whether `Oauth2Access.has_scope` works as intended.
    
    Case : no data | float
    """
    data = _get_access_data()
    data['scopes'] = ''
    
    access = Oauth2Access(data, '')
    
    with vampytest.assert_raises(TypeError):
        access.has_scope(12.6)


def test__Oauth2Access__has_scope_3():
    """
    Tests whether `Oauth2Access.has_scope` works as intended.
    
    Case : data | Oauth2Scope
    """
    data = _get_access_data()
    
    scope = Oauth2Scope.bot
    data['scopes'] = scope.value
    
    access = Oauth2Access(data, '')
    
    vampytest.assert_eq(access.has_scope(scope), True)


def test__Oauth2Access__has_scope_4():
    """
    Tests whether `Oauth2Access.has_scope` works as intended.
    
    Case : data | string
    """
    data = _get_access_data()
    
    scope = Oauth2Scope.bot
    data['scopes'] = scope.value
    
    access = Oauth2Access(data, '')
    
    vampytest.assert_eq(access.has_scope(scope.value), True)


def test__Oauth2Access__has_scope_5():
    """
    Tests whether `Oauth2Access.has_scope` works as intended.
    
    Case : data | float
    """
    data = _get_access_data()
    
    scope = Oauth2Scope.bot
    data['scopes'] = scope.value
    
    access = Oauth2Access(data, '')
    
    with vampytest.assert_raises(TypeError):
        access.has_scope(12.6)


def test__Oauth2Access__has_scope_6():
    """
    Tests whether `Oauth2Access.has_scope` works as intended.
    
    Case : data | Oauth2Scope | missing
    """
    data = _get_access_data()
    data['scopes'] = 'email'
    
    access = Oauth2Access(data, '')
    scope = Oauth2Scope.bot
    
    vampytest.assert_eq(access.has_scope(scope), False)
