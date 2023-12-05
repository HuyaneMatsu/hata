from datetime import datetime as DateTime

import vampytest

from ...client_platform_configuration import ClientPlatformConfiguration

from ..embedded_activity_configuration import EmbeddedActivityConfiguration
from ..preinstanced import OrientationLockState, PlatformType


def test__EmbeddedActivityConfiguration__repr():
    """
    Tests whether ``EmbeddedActivityConfiguration.__repr__`` works as intended.
    """
    age_gated = True
    client_platform_configurations = {
        PlatformType.web: ClientPlatformConfiguration(labelled_until = DateTime(2016, 5, 14)),
        PlatformType.ios: ClientPlatformConfiguration(labelled_until = DateTime(2016, 6, 14)),
    }
    content_security_policy_exceptions_exist = False
    default_orientation_lock_state = OrientationLockState.unlocked
    default_tablet_orientation_lock_state = OrientationLockState.portrait
    position = 6
    preview_video_asset_id = 202312020006
    
    configuration = EmbeddedActivityConfiguration(
        age_gated = age_gated,
        client_platform_configurations = client_platform_configurations,
        content_security_policy_exceptions_exist = content_security_policy_exceptions_exist,
        default_orientation_lock_state = default_orientation_lock_state,
        default_tablet_orientation_lock_state = default_tablet_orientation_lock_state,
        position = position,
        preview_video_asset_id = preview_video_asset_id,
    )
    
    vampytest.assert_instance(repr(configuration), str)


def test__EmbeddedActivityConfiguration__eq():
    """
    Tests whether ``EmbeddedActivityConfiguration.__repr__`` works as intended.
    """
    age_gated = True
    client_platform_configurations = {
        PlatformType.web: ClientPlatformConfiguration(labelled_until = DateTime(2016, 5, 14)),
        PlatformType.ios: ClientPlatformConfiguration(labelled_until = DateTime(2016, 6, 14)),
    }
    content_security_policy_exceptions_exist = False
    default_orientation_lock_state = OrientationLockState.unlocked
    default_tablet_orientation_lock_state = OrientationLockState.portrait
    position = 6
    preview_video_asset_id = 202312020007
    
    keyword_parameters = {
        'age_gated': age_gated,
        'client_platform_configurations': client_platform_configurations,
        'content_security_policy_exceptions_exist': content_security_policy_exceptions_exist,
        'default_orientation_lock_state': default_orientation_lock_state,
        'default_tablet_orientation_lock_state': default_tablet_orientation_lock_state,
        'position': position,
        'preview_video_asset_id': preview_video_asset_id,
    }
    
    configuration_original = EmbeddedActivityConfiguration(**keyword_parameters)
    
    vampytest.assert_eq(configuration_original, configuration_original)
    
    for field_name, field_value in (
        ('age_gated', False),
        ('client_platform_configurations', None),
        ('content_security_policy_exceptions_exist', True),
        ('default_orientation_lock_state', OrientationLockState.portrait),
        ('default_tablet_orientation_lock_state', OrientationLockState.landscape),
        ('position', 7),
        ('preview_video_asset_id', 202312020008),
    ):
        configuration_altered = EmbeddedActivityConfiguration(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(configuration_original, configuration_altered)


def test__EmbeddedActivityConfiguration__hash():
    """
    Tests whether ``EmbeddedActivityConfiguration.__hash__`` works as intended.
    """
    age_gated = True
    client_platform_configurations = {
        PlatformType.web: ClientPlatformConfiguration(labelled_until = DateTime(2016, 5, 14)),
        PlatformType.ios: ClientPlatformConfiguration(labelled_until = DateTime(2016, 6, 14)),
    }
    content_security_policy_exceptions_exist = False
    default_orientation_lock_state = OrientationLockState.unlocked
    default_tablet_orientation_lock_state = OrientationLockState.portrait
    position = 6
    preview_video_asset_id = 202312020009
    
    configuration = EmbeddedActivityConfiguration(
        age_gated = age_gated,
        client_platform_configurations = client_platform_configurations,
        content_security_policy_exceptions_exist = content_security_policy_exceptions_exist,
        default_orientation_lock_state = default_orientation_lock_state,
        default_tablet_orientation_lock_state = default_tablet_orientation_lock_state,
        position = position,
        preview_video_asset_id = preview_video_asset_id,
    )
    
    vampytest.assert_instance(hash(configuration), int)
