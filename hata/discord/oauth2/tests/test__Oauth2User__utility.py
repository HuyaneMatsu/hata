import vampytest

from .. import Oauth2Access, Oauth2User, Oauth2Scope


def _get_access_data():
    return {
        'access_token': 'a',
        'refresh_token': 'b',
        'expires_in': 1,
        'scope': 'bot identify email',
    }


def _get_user_data():
    return {
        'id': '202208270006'
    }


def test__Oauth2User__has_scope():
    """
    Returns whether ``Oauth2User.has_scope` works as intended.
    
    Case: just call it and watch it burn
    """
    data = _get_access_data()
    
    scope = Oauth2Scope.bot
    data['scope'] = scope.value
    
    user = Oauth2User.from_data(_get_user_data(), Oauth2Access.from_data(data, ''))
    
    vampytest.assert_eq(user.has_scope(scope), True)
