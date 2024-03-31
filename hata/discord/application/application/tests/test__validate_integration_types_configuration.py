import vampytest

from ...application_install_parameters import ApplicationInstallParameters
from ...application_integration_type_configuration import ApplicationIntegrationTypeConfiguration


from ..fields import validate_integration_types_configuration
from ..preinstanced import ApplicationIntegrationType


def _iter_options__passing():
    configuration_0 = ApplicationIntegrationTypeConfiguration(
        install_parameters = ApplicationInstallParameters(permissions = 8),
    )
    configuration_1 = ApplicationIntegrationTypeConfiguration(
        install_parameters = ApplicationInstallParameters(permissions = 123),
    )
    
    yield None, None
    yield {}, None
    yield (
        {
            ApplicationIntegrationType.user_install: configuration_0,
            ApplicationIntegrationType.guild_install: configuration_1,
        },
    
        {
            ApplicationIntegrationType.user_install: configuration_0,
            ApplicationIntegrationType.guild_install: configuration_1,
        },
    )

    yield (
        {
            ApplicationIntegrationType.user_install.value: configuration_0,
        },
    
        {
            ApplicationIntegrationType.user_install: configuration_0,
        },
    )


def _iter_options__type_error():
    configuration_0 = ApplicationIntegrationTypeConfiguration(
        install_parameters = ApplicationInstallParameters(permissions = 8),
    )
    
    yield 12.6
    
    yield {12.6 : configuration_0}
    yield {
        ApplicationIntegrationType.user_install: 12.6
    }


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_integration_types_configuration(input_value):
    """
    Tests whether `validate_integration_types_configuration` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | dict<ApplicationIntegrationType, ApplicationIntegrationTypeConfiguration>`
    
    Raises
    ------
    TypeError
    """
    return validate_integration_types_configuration(input_value)
