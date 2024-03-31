import vampytest

from ...application_install_parameters import ApplicationInstallParameters
from ...application_integration_type_configuration import ApplicationIntegrationTypeConfiguration

from ..fields import put_integration_types_configuration_into
from ..preinstanced import ApplicationIntegrationType


def _iter_options():
    configuration_0 = ApplicationIntegrationTypeConfiguration(
        install_parameters = ApplicationInstallParameters(permissions = 8),
    )
    configuration_1 = ApplicationIntegrationTypeConfiguration(
        install_parameters = ApplicationInstallParameters(permissions = 123),
    )
    
    
    yield None, False, {'integration_types_config': {}}
    yield None, True, {'integration_types_config': {}}
    yield (
        {
            ApplicationIntegrationType.user_install: configuration_0,
            ApplicationIntegrationType.guild_install: configuration_1,
        },
        False,
        {
            'integration_types_config': {
                str(ApplicationIntegrationType.user_install.value) : configuration_0.to_data(),
                str(ApplicationIntegrationType.guild_install.value) : configuration_1.to_data(),
            },
        },
    )
    yield (
        {
            ApplicationIntegrationType.user_install: configuration_0,
            ApplicationIntegrationType.guild_install: configuration_1,
        },
        True,
        {
            'integration_types_config': {
                str(ApplicationIntegrationType.user_install.value) : configuration_0.to_data(defaults = True),
                str(ApplicationIntegrationType.guild_install.value) : configuration_1.to_data(defaults = True),
            },
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_integration_types_configuration_into(input_value, defaults):
    """
    Tests whether ``put_integration_types_configuration_into`` is working as intended.
    
    Parameters
    ----------
    input_value : `None | dict<ApplicationIntegrationType, ApplicationIntegrationTypeConfiguration>`
        Value to serialize.
    defaults : `bool`
        Whether fields with their default value should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_integration_types_configuration_into(input_value, {}, defaults)
