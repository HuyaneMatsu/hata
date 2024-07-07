from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...client_platform_configuration import ClientPlatformConfiguration

from ..fields import validate_client_platform_configurations
from ..preinstanced import PlatformType


def _iter_options__passing():
    yield None, None
    yield {}, None
    
    configuration_0 = ClientPlatformConfiguration(labelled_until = DateTime(2016, 5, 14, tzinfo = TimeZone.utc))
    configuration_1 = ClientPlatformConfiguration(labelled_until = DateTime(2016, 6, 14, tzinfo = TimeZone.utc))
    
    yield (
        {
            PlatformType.web: configuration_0,
            PlatformType.ios: configuration_1,
        },
        {
            PlatformType.web: configuration_0,
            PlatformType.ios: configuration_1,
        },
    )

    yield (
        {
            PlatformType.web.value: configuration_0,
        },
        {
            PlatformType.web: configuration_0,
        },
    )


def _iter_options__type_error():
    yield []
    
    yield 12.6
    
    yield {
        PlatformType.web: object(),
    }
    
    yield {
        object(): ClientPlatformConfiguration(labelled_until = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)),
    }


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_client_platform_configurations(input_value):
    """
    Tests whether ``validate_client_platform_configurations`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `None | dict<PlatformType, ClientPlatformConfiguration>`
    
    Raises
    ------
    TypeError
    """
    return validate_client_platform_configurations(input_value)
