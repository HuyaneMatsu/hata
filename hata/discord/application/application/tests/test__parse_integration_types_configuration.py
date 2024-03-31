import vampytest

from ...application_install_parameters import ApplicationInstallParameters
from ...application_integration_type_configuration import ApplicationIntegrationTypeConfiguration

from ..fields import parse_integration_types_configuration
from ..preinstanced import ApplicationIntegrationType


def _iter_options():
    configuration_0 = ApplicationIntegrationTypeConfiguration(
        install_parameters = ApplicationInstallParameters(permissions = 8),
    )
    configuration_1 = ApplicationIntegrationTypeConfiguration(
        install_parameters = ApplicationInstallParameters(permissions = 123),
    )
    
    yield {}, None
    yield {'integration_types_config': None}, None
    yield {'integration_types_config': {}}, None
    yield (
        {
            'integration_types_config': {
                str(ApplicationIntegrationType.user_install.value) : configuration_0.to_data(),
                str(ApplicationIntegrationType.guild_install.value) : configuration_1.to_data(),
            },
        },
        {
            ApplicationIntegrationType.user_install: configuration_0,
            ApplicationIntegrationType.guild_install: configuration_1,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_integration_types_configuration(input_data):
    """
    Tests whether ``parse_integration_types_configuration`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | dict<ApplicationIntegrationType, ApplicationIntegrationTypeConfiguration>`
    """
    return parse_integration_types_configuration(input_data)
