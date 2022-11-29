import vampytest

from ....oauth2 import Oauth2Scope
from ....permission import Permission

from ..application_install_parameters import ApplicationInstallParameters


def _assert_is_every_attribute_set(application_install_parameters):
    """
    Asserts whether every attributes are set of the given application install parameters.
    
    Parameters
    ----------
    application_install_parameters : ``ApplicationInstallParameters``
    """
    vampytest.assert_instance(application_install_parameters, ApplicationInstallParameters)
    vampytest.assert_instance(application_install_parameters.permissions, Permission)
    vampytest.assert_instance(application_install_parameters.scopes, tuple, nullable = True)



def test__ApplicationInstallParameters__new__0():
    """
    Tests whether ``ApplicationInstallParameters.__new__`` works as intended.
    
    Case: No parameters.
    """
    application_install_parameters = ApplicationInstallParameters()
    _assert_is_every_attribute_set(application_install_parameters)


def test__ApplicationInstallParameters__new__1():
    """
    Tests whether ``ApplicationInstallParameters.__new__`` works as intended.
    
    Case: Give all parameters.
    """
    permissions = Permission(123)
    scopes = [Oauth2Scope.bot, Oauth2Scope.email]
    
    application_install_parameters = ApplicationInstallParameters(
        permissions = permissions,
        scopes = scopes,
    )
    
    _assert_is_every_attribute_set(application_install_parameters)
    vampytest.assert_eq(application_install_parameters.permissions, permissions)
    vampytest.assert_eq(application_install_parameters.scopes, tuple(scopes))
