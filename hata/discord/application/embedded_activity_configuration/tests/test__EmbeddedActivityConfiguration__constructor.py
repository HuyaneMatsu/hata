from datetime import datetime as DateTime

import vampytest

from ...client_platform_configuration import ClientPlatformConfiguration

from ..embedded_activity_configuration import EmbeddedActivityConfiguration
from ..preinstanced import OrientationLockState, PlatformType


def _assert_fields_set(configuration):
    """
    Asserts whether all fields are set of the given embedded activity configuration.
    
    Parameters
    ----------
    configuration : ``EmbeddedActivityConfiguration``
    """
    vampytest.assert_instance(configuration, EmbeddedActivityConfiguration)
    vampytest.assert_instance(configuration.age_gated, bool)
    vampytest.assert_instance(configuration.client_platform_configurations, dict, nullable = True)
    vampytest.assert_instance(configuration.content_security_policy_exceptions_exist, bool)
    vampytest.assert_instance(configuration.default_orientation_lock_state, OrientationLockState)
    vampytest.assert_instance(configuration.default_tablet_orientation_lock_state, OrientationLockState)
    vampytest.assert_instance(configuration.position, int)
    vampytest.assert_instance(configuration.preview_video_asset_id, int)

def test__EmbeddedActivityConfiguration__new__no_fields():
    """
    Tests whether ``EmbeddedActivityConfiguration.__new__`` works as intended.
    
    Case: No fields given.
    """
    configuration = EmbeddedActivityConfiguration()
    _assert_fields_set(configuration)


def test__EmbeddedActivityConfiguration__new__all_fields():
    """
    Tests whether ``EmbeddedActivityConfiguration.__new__`` works as intended.
    
    Case: All fields given.
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
    preview_video_asset_id = 202312020003
    
    configuration = EmbeddedActivityConfiguration(
        age_gated = age_gated,
        client_platform_configurations = client_platform_configurations,
        content_security_policy_exceptions_exist = content_security_policy_exceptions_exist,
        default_orientation_lock_state = default_orientation_lock_state,
        default_tablet_orientation_lock_state = default_tablet_orientation_lock_state,
        position = position,
        preview_video_asset_id = preview_video_asset_id,
    )
    _assert_fields_set(configuration)
    
    vampytest.assert_eq(configuration.age_gated, age_gated)
    vampytest.assert_eq(configuration.client_platform_configurations, client_platform_configurations)
    vampytest.assert_eq(configuration.content_security_policy_exceptions_exist, content_security_policy_exceptions_exist)
    vampytest.assert_is(configuration.default_orientation_lock_state, default_orientation_lock_state)
    vampytest.assert_is(configuration.default_tablet_orientation_lock_state, default_tablet_orientation_lock_state)
    vampytest.assert_eq(configuration.position, position)
    vampytest.assert_eq(configuration.preview_video_asset_id, preview_video_asset_id)
