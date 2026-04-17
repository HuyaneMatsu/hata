from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...client_platform_configuration import ClientPlatformConfiguration

from ..embedded_activity_configuration import EmbeddedActivityConfiguration
from ..preinstanced import OrientationLockState, PlatformType

from .test__EmbeddedActivityConfiguration__constructor import _assert_fields_set


def test__EmbeddedActivityConfiguration__copy():
    """
    Tests whether ``EmbeddedActivityConfiguration.copy`` works as intended.
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
    preview_video_asset_id = 202312020010
    
    configuration = EmbeddedActivityConfiguration(
        age_gated = age_gated,
        client_platform_configurations = client_platform_configurations,
        content_security_policy_exceptions_exist = content_security_policy_exceptions_exist,
        default_orientation_lock_state = default_orientation_lock_state,
        default_tablet_orientation_lock_state = default_tablet_orientation_lock_state,
        position = position,
        preview_video_asset_id = preview_video_asset_id,
    )
    
    copy = configuration.copy()
    _assert_fields_set(configuration)
    vampytest.assert_is_not(copy, configuration)
    
    vampytest.assert_eq(configuration, copy)


def test__EmbeddedActivityConfiguration__copy_with__no_fields():
    """
    Tests whether ``EmbeddedActivityConfiguration.copy_with`` works as intended.
    
    Case: No fields given.
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
    preview_video_asset_id = 202312020011
    
    configuration = EmbeddedActivityConfiguration(
        age_gated = age_gated,
        client_platform_configurations = client_platform_configurations,
        content_security_policy_exceptions_exist = content_security_policy_exceptions_exist,
        default_orientation_lock_state = default_orientation_lock_state,
        default_tablet_orientation_lock_state = default_tablet_orientation_lock_state,
        position = position,
        preview_video_asset_id = preview_video_asset_id,
    )
    
    copy = configuration.copy_with()
    _assert_fields_set(configuration)
    vampytest.assert_is_not(copy, configuration)
    
    vampytest.assert_eq(configuration, copy)


def test__EmbeddedActivityConfiguration__copy_with__all_fields():
    """
    Tests whether ``EmbeddedActivityConfiguration.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_age_gated = True
    old_client_platform_configurations = {
        PlatformType.web: ClientPlatformConfiguration(labelled_until = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)),
        PlatformType.ios: ClientPlatformConfiguration(labelled_until = DateTime(2016, 6, 14, tzinfo = TimeZone.utc)),
    }
    old_content_security_policy_exceptions_exist = False
    old_default_orientation_lock_state = OrientationLockState.unlocked
    old_default_tablet_orientation_lock_state = OrientationLockState.portrait
    old_position = 6
    old_preview_video_asset_id = 202312020012
    
    new_age_gated = False
    new_client_platform_configurations = {
        PlatformType.android: ClientPlatformConfiguration(labelled_until = DateTime(2016, 8, 14, tzinfo = TimeZone.utc)),
    }
    new_content_security_policy_exceptions_exist = True
    new_default_orientation_lock_state = OrientationLockState.portrait
    new_default_tablet_orientation_lock_state = OrientationLockState.landscape
    new_position = 7
    new_preview_video_asset_id = 202312020013
    
    
    configuration = EmbeddedActivityConfiguration(
        age_gated = old_age_gated,
        client_platform_configurations = old_client_platform_configurations,
        content_security_policy_exceptions_exist = old_content_security_policy_exceptions_exist,
        default_orientation_lock_state = old_default_orientation_lock_state,
        default_tablet_orientation_lock_state = old_default_tablet_orientation_lock_state,
        position = old_position,
        preview_video_asset_id = old_preview_video_asset_id,
    )
    
    copy = configuration.copy_with(
        age_gated = new_age_gated,
        client_platform_configurations = new_client_platform_configurations,
        content_security_policy_exceptions_exist = new_content_security_policy_exceptions_exist,
        default_orientation_lock_state = new_default_orientation_lock_state,
        default_tablet_orientation_lock_state = new_default_tablet_orientation_lock_state,
        position = new_position,
        preview_video_asset_id = new_preview_video_asset_id,
    )
    _assert_fields_set(configuration)
    vampytest.assert_is_not(copy, configuration)
    
    vampytest.assert_eq(copy.age_gated, new_age_gated)
    vampytest.assert_eq(copy.client_platform_configurations, new_client_platform_configurations)
    vampytest.assert_eq(copy.content_security_policy_exceptions_exist, new_content_security_policy_exceptions_exist)
    vampytest.assert_is(copy.default_orientation_lock_state, new_default_orientation_lock_state)
    vampytest.assert_is(copy.default_tablet_orientation_lock_state, new_default_tablet_orientation_lock_state)
    vampytest.assert_eq(copy.position, new_position)
    vampytest.assert_eq(copy.preview_video_asset_id, new_preview_video_asset_id)


def _iter_options__iter_supported_platforms():
    yield None, set()
    yield (
        {
            PlatformType.web: ClientPlatformConfiguration(labelled_until = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)),
            PlatformType.ios: ClientPlatformConfiguration(labelled_until = DateTime(2016, 6, 14, tzinfo = TimeZone.utc)),
        },
        {PlatformType.web, PlatformType.ios},
    )


@vampytest._(vampytest.call_from(_iter_options__iter_supported_platforms()).returning_last())
def test__EmbeddedActivityConfiguration__iter_supported_platforms(client_platform_configurations):
    """
    Tests whether ``EmbeddedActivityConfiguration.iter_supported_platforms`` works as intended.
    
    Parameters
    ----------
    client_platform_configurations : `None | dict<PlatformType, ClientPlatformConfiguration>`
        The embedded activity's configuration for each platform.
    
    Returns
    -------
    output : `set<PlatformType>`
    """
    configuration = EmbeddedActivityConfiguration(client_platform_configurations = client_platform_configurations)
    return {*configuration.iter_supported_platforms()}


def _iter_options__get_client_platform_configuration():
    configuration_0 = ClientPlatformConfiguration(labelled_until = DateTime(2016, 5, 14, tzinfo = TimeZone.utc))
    configuration_1 = ClientPlatformConfiguration(labelled_until = DateTime(2016, 6, 14, tzinfo = TimeZone.utc))
    
    yield None, PlatformType.web, None
    yield None, PlatformType.web.value, None
    
    yield (
        {
            PlatformType.web: configuration_0,
            PlatformType.ios: configuration_1,
        },
        PlatformType.android,
        None,
    )
    yield (
        {
            PlatformType.web: configuration_0,
            PlatformType.ios: configuration_1,
        },
        PlatformType.android.value,
        None,
    )

    yield (
        {
            PlatformType.web: configuration_0,
            PlatformType.ios: configuration_1,
        },
        PlatformType.web,
        configuration_0,
    )
    yield (
        {
            PlatformType.web: configuration_0,
            PlatformType.ios: configuration_1,
        },
        PlatformType.web.value,
        configuration_0,
    )


@vampytest._(vampytest.call_from(_iter_options__get_client_platform_configuration()).returning_last())
def test__EmbeddedActivityConfiguration__get_client_platform_configuration(client_platform_configurations, platform):
    """
    Tests whether ``EmbeddedActivityConfiguration.get_client_platform_configuration`` works as intended.
    
    Parameters
    ----------
    client_platform_configurations : `None | dict<PlatformType, ClientPlatformConfiguration>`
        The embedded activity's configuration for each platform.
    platform : `PlatformType | str`
        The platform to get the configuration for.
    
    Returns
    -------
    output : `set<PlatformType>`
    """
    configuration = EmbeddedActivityConfiguration(client_platform_configurations = client_platform_configurations)
    return configuration.get_client_platform_configuration(platform)
