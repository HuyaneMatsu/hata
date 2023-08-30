import vampytest

from ....oauth2 import Oauth2Scope
from ....permission import Permission

from ..application_install_parameters import ApplicationInstallParameters

from .test__ApplicationInstallParameters__constructor import _assert_fields_set


def test__ApplicationInstallParameters__copy():
    """
    Tests whether ``ApplicationInstallParameters.copy`` works as intended.
    """
    permissions = Permission(123)
    scopes = [Oauth2Scope.bot, Oauth2Scope.email]
    
    application_install_parameters = ApplicationInstallParameters(
        permissions = permissions,
        scopes = scopes,
    )
    
    copy = application_install_parameters.copy()
    _assert_fields_set(copy)
    vampytest.assert_eq(application_install_parameters, copy)
    vampytest.assert_is_not(application_install_parameters, copy)


def test__ApplicationInstallParameters__copy_with__0():
    """
    Tests whether ``ApplicationInstallParameters.copy`` works as intended.
    
    Case: No parameters
    """
    permissions = Permission(123)
    scopes = [Oauth2Scope.bot, Oauth2Scope.email]
    
    application_install_parameters = ApplicationInstallParameters(
        permissions = permissions,
        scopes = scopes,
    )
    
    copy = application_install_parameters.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_eq(application_install_parameters, copy)
    vampytest.assert_is_not(application_install_parameters, copy)


def test__ApplicationInstallParameters__copy_with__1():
    """
    Tests whether ``ApplicationInstallParameters.copy`` works as intended.
    
    Case: No parameters
    """
    old_permissions = Permission(123)
    new_permissions = Permission(333)
    old_scopes = [Oauth2Scope.bot, Oauth2Scope.email]
    new_scopes = None
    
    application_install_parameters = ApplicationInstallParameters(
        permissions = old_permissions,
        scopes = old_scopes,
    )
    
    copy = application_install_parameters.copy_with(
        permissions = new_permissions,
        scopes = new_scopes,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(application_install_parameters, copy)

    vampytest.assert_eq(copy.permissions, new_permissions)
    vampytest.assert_is(copy.scopes, None)
