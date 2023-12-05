from datetime import datetime as DateTime

import vampytest

from ...client_platform_configuration import ClientPlatformConfiguration

from ..fields import put_client_platform_configurations_into
from ..preinstanced import PlatformType


def _iter_options():
    yield None, False, {'client_platform_config': {}, 'supported_platforms': []}
    yield None, True, {'client_platform_config': {}, 'supported_platforms': []}
    
    
    configuration_0 = ClientPlatformConfiguration(labelled_until = DateTime(2016, 5, 14))
    configuration_1 = ClientPlatformConfiguration(labelled_until = DateTime(2016, 6, 14))
    
    yield (
        {
            PlatformType.web: configuration_0,
            PlatformType.ios: configuration_1,
        },
        False,
        {
            'client_platform_config': {
                PlatformType.web.value: configuration_0.to_data(defaults = False),
                PlatformType.ios.value: configuration_1.to_data(defaults = False),
            },
            'supported_platforms': [PlatformType.ios.value, PlatformType.web.value],
        },
    )

    yield (
        {
            PlatformType.web: configuration_0,
            PlatformType.ios: configuration_1,
        },
        True,
        {
            'client_platform_config': {
                PlatformType.web.value: configuration_0.to_data(defaults = True),
                PlatformType.ios.value: configuration_1.to_data(defaults = True),
            },
            'supported_platforms': [PlatformType.ios.value, PlatformType.web.value],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_client_platform_configurations_into(input_value, defaults):
    """
    Tests whether ``put_client_platform_configurations_into`` works as intended.
    
    Parameters
    ----------
    input_value : `None | dict<PlatformType, ClientPlatformConfiguration>`
        The value to serialise.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_client_platform_configurations_into(input_value, {}, defaults)
