import vampytest

from ....oauth2 import Oauth2Scope
from ....permission import Permission

from ..application_install_parameters import ApplicationInstallParameters


def test__ApplicationInstallParameters__repr():
    """
    Tests whether ``ApplicationInstallParameters.__repr__`` works as intended.
    """
    permissions = Permission(123)
    scopes = [Oauth2Scope.bot, Oauth2Scope.email]
    
    application_install_parameters = ApplicationInstallParameters(
        permissions = permissions,
        scopes = scopes,
    )
    
    vampytest.assert_instance(repr(application_install_parameters), str)


def test__ApplicationInstallParameters__hash():
    """
    Tests whether ``ApplicationInstallParameters.__hash__`` works as intended.
    """
    permissions = Permission(123)
    scopes = [Oauth2Scope.bot, Oauth2Scope.email]
    
    application_install_parameters = ApplicationInstallParameters(
        permissions = permissions,
        scopes = scopes,
    )
    
    vampytest.assert_instance(hash(application_install_parameters), int)


def test__ApplicationInstallParameters__eq():
    """
    Tests whether ``ApplicationInstallParameters.__eq__`` works as intended.
    """
    permissions = Permission(123)
    scopes = [Oauth2Scope.bot, Oauth2Scope.email]
    
    keyword_parameters = {
        'permissions': permissions,
        'scopes': scopes,
    }
    
    application_install_parameters = ApplicationInstallParameters(**keyword_parameters)
    vampytest.assert_eq(application_install_parameters, application_install_parameters)
    vampytest.assert_ne(application_install_parameters, object())
    
    for field_name, field_value in (
        ('permissions', Permission(333)),
        ('scopes', None),
    ):
        test_application_install_parameters = ApplicationInstallParameters(
            **{**keyword_parameters, field_name: field_value}
        )
        vampytest.assert_ne(application_install_parameters, test_application_install_parameters)
