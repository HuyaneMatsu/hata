__all__ = ()

from ...field_parsers import (
    bool_parser_factory, entity_id_parser_factory, int_parser_factory, preinstanced_parser_factory
)
from ...field_putters import (
    entity_id_putter_factory, force_bool_putter_factory, int_putter_factory, preinstanced_putter_factory
)
from ...field_validators import (
    bool_validator_factory, entity_id_validator_factory, int_conditional_validator_factory,
    preinstanced_validator_factory
)

from ..client_platform_configuration import ClientPlatformConfiguration

from .preinstanced import OrientationLockState, PlatformType


# age_gated

parse_age_gated = bool_parser_factory('requires_age_gate', False)
put_age_gated_into = force_bool_putter_factory('requires_age_gate')
validate_age_gated = bool_validator_factory('age_gated', False)


# client_platform_configurations

def parse_client_platform_configurations(data):
    """
    Parses out client platform configurations from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Embedded activity configuration data.
    
    Returns
    -------
    client_platform_configurations : `None | dict<PlatformType, ClientPlatformConfiguration>`
    """
    configuration_datas = data.get('client_platform_config', None)
    if (configuration_datas is None) or (not configuration_datas):
        return None
    
    return {
        PlatformType.get(platform_value): ClientPlatformConfiguration.from_data(configuration_data)
        for platform_value, configuration_data in configuration_datas.items()
    }
        

def put_client_platform_configurations_into(client_platform_configurations, data, defaults):
    """
    Puts the activity timestamps start into the given data.
    
    Parameters
    ----------
    client_platform_configurations : `None | dict<PlatformType, ClientPlatformConfiguration>`
        Client configurations by platform.
    data : `dict<str, object>`
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    configuration_datas = {}
    supported_platforms = []
    
    if (client_platform_configurations is not None):
        for platform, client_platform_configuration in client_platform_configurations.items():
            configuration_datas[platform.value] = client_platform_configuration.to_data(defaults = defaults)
            supported_platforms.append(platform.value)
    
    supported_platforms.sort()
    
    data['client_platform_config'] = configuration_datas
    data['supported_platforms'] = supported_platforms
    
    return data


def validate_client_platform_configurations(client_platform_configurations):
    """
    Validates the given client platform configurations.
    
    Parameters
    ----------
    client_platform_configurations : `None | dict<PlatformType | int, ClientPlatformConfiguration>`
        Client configurations by platform.
    
    Returns
    -------
    client_platform_configurations : `None | dict<PlatformType, ClientPlatformConfiguration>`
    
    Raises
    ------
    TypeError
        - If a parameter's type is incorrect.
    ValueError
        - If a parameter's value is incorrect.
    """
    if client_platform_configurations is None:
        return None
    
    if not isinstance(client_platform_configurations, dict):
        raise TypeError(
            f'`client_platform_configurations` can be `None | dict<{PlatformType.__name__} | '
            f'{PlatformType.VALUE_TYPE.__name__}, {ClientPlatformConfiguration.__name__}`, got '
            f'{type(client_platform_configurations).__name__}; {client_platform_configurations!r}.'
        )
    
    validated = None
    
    for key, value in client_platform_configurations.items():
        if isinstance(key, PlatformType):
            pass
        elif isinstance(key, PlatformType.VALUE_TYPE):
            key = PlatformType.get(key)
        else:
            raise TypeError(
                f'`client_platform_configurations` keys can be `{PlatformType.__name__} | '
                f'{PlatformType.VALUE_TYPE.__name__}`, got {type(key).__name__}; {key!r}.'
            )
        
        if not isinstance(value, ClientPlatformConfiguration):
            raise TypeError(
                f'`client_platform_configurations` values can be `{ClientPlatformConfiguration.__name__}`, got '
                f'{type(value).__name__}; {value!r}.'
            )
        
        if validated is None:
            validated = {}
        
        validated[key] = value
    
    return validated


# content_security_policy_exceptions_exist

parse_content_security_policy_exceptions_exist = bool_parser_factory('has_csp_exception', False)
put_content_security_policy_exceptions_exist_into = force_bool_putter_factory('has_csp_exception')
validate_content_security_policy_exceptions_exist = bool_validator_factory(
    'content_security_policy_exceptions_exist', False
)


# default_orientation_lock_state

parse_default_orientation_lock_state = preinstanced_parser_factory(
    'default_orientation_lock_state', OrientationLockState, OrientationLockState.none
)
put_default_orientation_lock_state_into = preinstanced_putter_factory('default_orientation_lock_state')
validate_default_orientation_lock_state = preinstanced_validator_factory(
    'default_orientation_lock_state', OrientationLockState
)


# default_tablet_orientation_lock_state

parse_default_tablet_orientation_lock_state = preinstanced_parser_factory(
    'tablet_default_orientation_lock_state', OrientationLockState, OrientationLockState.none
)
put_default_tablet_orientation_lock_state_into = preinstanced_putter_factory('tablet_default_orientation_lock_state')
validate_default_tablet_orientation_lock_state = preinstanced_validator_factory(
    'default_tablet_orientation_lock_state', OrientationLockState
)


# position

parse_position = int_parser_factory('shelf_rank', 0)
put_position_into = int_putter_factory('shelf_rank')
validate_position = int_conditional_validator_factory(
    'position',
    0,
    (lambda position : position >= 0),
    '>= 0',
)

# preview_video_asset_id

parse_preview_video_asset_id = entity_id_parser_factory('activity_preview_video_asset_id')
put_preview_video_asset_id_into = entity_id_putter_factory('activity_preview_video_asset_id')
validate_preview_video_asset_id = entity_id_validator_factory('preview_video_asset_id')

