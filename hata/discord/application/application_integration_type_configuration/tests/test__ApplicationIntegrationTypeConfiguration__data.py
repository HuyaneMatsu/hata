import vampytest

from ...application_install_parameters import ApplicationInstallParameters

from ..application_integration_type_configuration import ApplicationIntegrationTypeConfiguration

from .test__ApplicationIntegrationTypeConfiguration__constructor import _assert_fields_set


def test__ApplicationIntegrationTypeConfiguration__from_data():
    """
    Tests whether ``ApplicationIntegrationTypeConfiguration.from_data`` works as intended.
    """
    install_parameters = ApplicationInstallParameters(permissions = 8)
    
    data = {
        'oauth2_install_params': install_parameters.to_data(),
    }
    
    configuration = ApplicationIntegrationTypeConfiguration.from_data(data)
    _assert_fields_set(configuration)
    
    vampytest.assert_eq(configuration.install_parameters, install_parameters)

def test__ApplicationIntegrationTypeConfiguration__to_data():
    """
    Tests whether ``ApplicationIntegrationTypeConfiguration.to_data`` works as intended.
    
    Case: Include defaults.
    """
    install_parameters = ApplicationInstallParameters(permissions = 8)
    
    configuration = ApplicationIntegrationTypeConfiguration(
        install_parameters = install_parameters,
    )
    
    expected_output = {
        'oauth2_install_params': install_parameters.to_data(defaults = True),
    }
    
    vampytest.assert_eq(configuration.to_data(defaults = True), expected_output)
