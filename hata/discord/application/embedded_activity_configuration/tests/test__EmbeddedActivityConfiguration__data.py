from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...client_platform_configuration import ClientPlatformConfiguration

from ..embedded_activity_configuration import EmbeddedActivityConfiguration
from ..preinstanced import OrientationLockState, PlatformType

from .test__EmbeddedActivityConfiguration__constructor import _assert_fields_set


def test__EmbeddedActivityConfiguration__from_data():
    """
    Tests whether ``EmbeddedActivityConfiguration.from_data`` works as intended.
    """
    age_gated = True
    client_platform_configurations = {
        PlatformType.web: ClientPlatformConfiguration(labelled_until = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)),
        PlatformType.ios: ClientPlatformConfiguration(labelled_until = DateTime(2016, 6, 14, tzinfo = TimeZone.utc)),
    }
    content_security_policy_exceptions_exist = False
    default_orientation_lock_state = OrientationLockState.unlocked
    default_tablet_orientation_lock_state = OrientationLockState.portrait
    position = 6
    preview_video_asset_id = 202312020004
    
    data = {
        'requires_age_gate': age_gated,
        'client_platform_config': {
            platform.value: client_configuration.to_data(defaults = True)
            for platform, client_configuration in client_platform_configurations.items()
        },
        'has_csp_exception': content_security_policy_exceptions_exist,
        'default_orientation_lock_state': default_orientation_lock_state.value,
        'tablet_default_orientation_lock_state': default_tablet_orientation_lock_state.value,
        'shelf_rank': position,
        'activity_preview_video_asset_id': str(preview_video_asset_id),
    }
    
    configuration = EmbeddedActivityConfiguration.from_data(data)
    _assert_fields_set(configuration)
    
    vampytest.assert_eq(configuration.age_gated, age_gated)
    vampytest.assert_eq(configuration.client_platform_configurations, client_platform_configurations)
    vampytest.assert_eq(configuration.content_security_policy_exceptions_exist, content_security_policy_exceptions_exist)
    vampytest.assert_is(configuration.default_orientation_lock_state, default_orientation_lock_state)
    vampytest.assert_is(configuration.default_tablet_orientation_lock_state, default_tablet_orientation_lock_state)
    vampytest.assert_eq(configuration.position, position)
    vampytest.assert_eq(configuration.preview_video_asset_id, preview_video_asset_id)


def test__EmbeddedActivityConfiguration__to_data():
    """
    Tests whether ``EmbeddedActivityConfiguration.to_data`` works as intended.
    
    Case: include defaults.
    """
    age_gated = True
    client_platform_configurations = {
        PlatformType.web: ClientPlatformConfiguration(labelled_until = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)),
        PlatformType.ios: ClientPlatformConfiguration(labelled_until = DateTime(2016, 6, 14, tzinfo = TimeZone.utc)),
    }
    content_security_policy_exceptions_exist = False
    default_orientation_lock_state = OrientationLockState.unlocked
    default_tablet_orientation_lock_state = OrientationLockState.portrait
    position = 6
    preview_video_asset_id = 202312020005
    
    configuration = EmbeddedActivityConfiguration(
        age_gated = age_gated,
        client_platform_configurations = client_platform_configurations,
        content_security_policy_exceptions_exist = content_security_policy_exceptions_exist,
        default_orientation_lock_state = default_orientation_lock_state,
        default_tablet_orientation_lock_state = default_tablet_orientation_lock_state,
        position = position,
        preview_video_asset_id = preview_video_asset_id,
    )
    
    expected_output = {
        'requires_age_gate': age_gated,
        'client_platform_config': {
            platform.value: client_configuration.to_data(defaults = True)
            for platform, client_configuration in client_platform_configurations.items()
        },
        'supported_platforms': sorted(platform.value for platform in client_platform_configurations.keys()),
        'has_csp_exception': content_security_policy_exceptions_exist,
        'default_orientation_lock_state': default_orientation_lock_state.value,
        'tablet_default_orientation_lock_state': default_tablet_orientation_lock_state.value,
        'shelf_rank': position,
        'activity_preview_video_asset_id': str(preview_video_asset_id),
    }
    
    vampytest.assert_eq(
        configuration.to_data(defaults = True),
        expected_output,
    )
