from datetime import datetime as DateTime

import vampytest

from ...client_platform_configuration import ClientPlatformConfiguration

from ..fields import parse_client_platform_configurations
from ..preinstanced import PlatformType


def _iter_options():
    yield {}, None
    yield {'client_platform_config': {}}, None
    
    
    configuration_0 = ClientPlatformConfiguration(labelled_until = DateTime(2016, 5, 14))
    configuration_1 = ClientPlatformConfiguration(labelled_until = DateTime(2016, 6, 14))
    
    yield (
        {
            'client_platform_config': {
                PlatformType.web.value: configuration_0.to_data(),
                PlatformType.ios.value: configuration_1.to_data(),
            },
        },
        {
            PlatformType.web: configuration_0,
            PlatformType.ios: configuration_1,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_client_platform_configurations(input_data):
    """
    Tests whether ``parse_client_platform_configurations`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | dict<PlatformType, ClientPlatformConfiguration>`
    """
    return parse_client_platform_configurations(input_data)
