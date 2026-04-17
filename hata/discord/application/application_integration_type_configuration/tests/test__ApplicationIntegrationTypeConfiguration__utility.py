import vampytest

from ...application_install_parameters import ApplicationInstallParameters

from ..application_integration_type_configuration import ApplicationIntegrationTypeConfiguration

from .test__ApplicationIntegrationTypeConfiguration__constructor import _assert_fields_set


def test__ApplicationIntegrationTypeConfiguration__copy():
    """
    Tests whether ``ApplicationIntegrationTypeConfiguration.copy`` works as intended.
    """
    install_parameters = ApplicationInstallParameters(permissions = 8)
    
    configuration = ApplicationIntegrationTypeConfiguration(
        install_parameters = install_parameters,
    )
    
    copy = configuration.copy()
    _assert_fields_set(copy)
    vampytest.assert_eq(configuration, copy)
    vampytest.assert_is_not(configuration, copy)


def test__ApplicationIntegrationTypeConfiguration__copy_with__no_fields():
    """
    Tests whether ``ApplicationIntegrationTypeConfiguration.copy`` works as intended.
    
    Case: No fields given.
    """
    install_parameters = ApplicationInstallParameters(permissions = 8)
    
    configuration = ApplicationIntegrationTypeConfiguration(
        install_parameters = install_parameters,
    )
    
    copy = configuration.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_eq(configuration, copy)
    vampytest.assert_is_not(configuration, copy)


def test__ApplicationIntegrationTypeConfiguration__copy_with__all_fields():
    """
    Tests whether ``ApplicationIntegrationTypeConfiguration.copy`` works as intended.
    
    Case: All fields given.
    """
    old_install_parameters = ApplicationInstallParameters(permissions = 8)
    new_install_parameters = ApplicationInstallParameters(permissions = 123)
    
    configuration = ApplicationIntegrationTypeConfiguration(
        install_parameters = old_install_parameters,
    )
    
    copy = configuration.copy_with(
        install_parameters = new_install_parameters,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(configuration, copy)

    vampytest.assert_eq(copy.install_parameters, new_install_parameters)
