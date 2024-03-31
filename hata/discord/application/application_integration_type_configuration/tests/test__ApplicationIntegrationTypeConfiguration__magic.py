import vampytest

from ...application_install_parameters import ApplicationInstallParameters

from ..application_integration_type_configuration import ApplicationIntegrationTypeConfiguration


def test__ApplicationIntegrationTypeConfiguration__repr():
    """
    Tests whether ``ApplicationIntegrationTypeConfiguration.__repr__`` works as intended.
    """
    install_parameters = ApplicationInstallParameters(permissions = 8)
    
    configuration = ApplicationIntegrationTypeConfiguration(
        install_parameters = install_parameters,
    )
    
    vampytest.assert_instance(repr(configuration), str)


def test__ApplicationIntegrationTypeConfiguration__hash():
    """
    Tests whether ``ApplicationIntegrationTypeConfiguration.__hash__`` works as intended.
    """
    install_parameters = ApplicationInstallParameters(permissions = 8)
    
    configuration = ApplicationIntegrationTypeConfiguration(
        install_parameters = install_parameters,
    )
    
    vampytest.assert_instance(hash(configuration), int)


def test__ApplicationIntegrationTypeConfiguration__eq():
    """
    Tests whether ``ApplicationIntegrationTypeConfiguration.__eq__`` works as intended.
    """
    install_parameters = ApplicationInstallParameters(permissions = 8)
    
    keyword_parameters = {
        'install_parameters': install_parameters,
    }
    
    configuration = ApplicationIntegrationTypeConfiguration(**keyword_parameters)
    vampytest.assert_eq(configuration, configuration)
    vampytest.assert_ne(configuration, object())
    
    for field_name, field_value in (
        ('install_parameters', None),
    ):
        test_configuration = ApplicationIntegrationTypeConfiguration(
            **{**keyword_parameters, field_name: field_value}
        )
        vampytest.assert_ne(configuration, test_configuration)
