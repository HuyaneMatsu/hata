import vampytest

from ....oauth2 import Oauth2Scope
from ....permission import Permission

from ..application_install_parameters import ApplicationInstallParameters

from .test__ApplicationInstallParameters__constructor import _assert_fields_set


def test__ApplicationInstallParameters__from_data():
    """
    Tests whether ``ApplicationInstallParameters.from_data`` works as intended.
    """
    permissions = Permission(123)
    scopes = [Oauth2Scope.bot, Oauth2Scope.email]
    
    data = {
        'permissions': format(permissions, 'd'),
        'scopes': [scope.value for scope in scopes],
    }
    
    application_install_parameters = ApplicationInstallParameters.from_data(data)
    _assert_fields_set(application_install_parameters)
    
    vampytest.assert_eq(application_install_parameters.permissions, permissions)
    vampytest.assert_eq(application_install_parameters.scopes, tuple(scopes))


def test__ApplicationInstallParameters__to_data():
    """
    Tests whether ``ApplicationInstallParameters.to_data`` works as intended.
    
    Case: Include defaults.
    """
    permissions = Permission(123)
    scopes = [Oauth2Scope.bot, Oauth2Scope.email]
    
    application_install_parameters = ApplicationInstallParameters(
        permissions = permissions,
        scopes = scopes,
    )
    
    expected_output = {
        'permissions': format(permissions, 'd'),
        'scopes': [scope.value for scope in scopes],
    }
    
    vampytest.assert_eq(application_install_parameters.to_data(defaults = True), expected_output)
