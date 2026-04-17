import vampytest

from ...application_install_parameters import ApplicationInstallParameters

from ..application_integration_type_configuration import ApplicationIntegrationTypeConfiguration


def _assert_fields_set(configuration):
    """
    Asserts whether every attributes are set of the given application install parameters.
    
    Parameters
    ----------
    configuration : ``ApplicationIntegrationTypeConfiguration``
    """
    vampytest.assert_instance(configuration, ApplicationIntegrationTypeConfiguration)
    vampytest.assert_instance(configuration.install_parameters, ApplicationInstallParameters, nullable = True)


def test__ApplicationIntegrationTypeConfiguration__new__no_fields():
    """
    Tests whether ``ApplicationIntegrationTypeConfiguration.__new__`` works as intended.
    
    Case: No parameters.
    """
    configuration = ApplicationIntegrationTypeConfiguration()
    _assert_fields_set(configuration)


def test__ApplicationIntegrationTypeConfiguration__new__all_fields():
    """
    Tests whether ``ApplicationIntegrationTypeConfiguration.__new__`` works as intended.
    
    Case: Give all parameters.
    """
    install_parameters = ApplicationInstallParameters(permissions = 8)
    
    configuration = ApplicationIntegrationTypeConfiguration(
        install_parameters = install_parameters,
    )
    
    _assert_fields_set(configuration)
    vampytest.assert_eq(configuration.install_parameters, install_parameters)


def test__ApplicationIntegrationTypeConfiguration__create_empty():
    """
    Tests whether ``ApplicationIntegrationTypeConfiguration.create_empty`` works as intended.
    """
    configuration = ApplicationIntegrationTypeConfiguration._create_empty()
    
    _assert_fields_set(configuration)
