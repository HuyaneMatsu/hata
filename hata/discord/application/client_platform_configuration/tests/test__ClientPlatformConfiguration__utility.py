from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..client_platform_configuration import ClientPlatformConfiguration
from ..preinstanced import LabelType, ReleasePhase

from .test__ClientPlatformConfiguration__constructor import _assert_fields_set


def test__ClientPlatformConfiguration__copy():
    """
    Tests whether ``ClientPlatformConfiguration.copy`` works as intended.
    """
    label_type = LabelType.new
    labelled_until = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    release_phase = ReleasePhase.global_launch
    
    configuration = ClientPlatformConfiguration(
        label_type = label_type,
        labelled_until = labelled_until,
        release_phase = release_phase,
    )
    
    copy = configuration.copy()
    _assert_fields_set(configuration)
    vampytest.assert_is_not(copy, configuration)
    
    vampytest.assert_eq(configuration, copy)


def test__ClientPlatformConfiguration__copy_with__no_fields():
    """
    Tests whether ``ClientPlatformConfiguration.copy_with`` works as intended.
    
    Case: No fields given.
    """
    label_type = LabelType.new
    labelled_until = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    release_phase = ReleasePhase.global_launch
    
    configuration = ClientPlatformConfiguration(
        label_type = label_type,
        labelled_until = labelled_until,
        release_phase = release_phase,
    )
    
    copy = configuration.copy_with()
    _assert_fields_set(configuration)
    vampytest.assert_is_not(copy, configuration)
    
    vampytest.assert_eq(configuration, copy)


def test__ClientPlatformConfiguration__copy_with__all_fields():
    """
    Tests whether ``ClientPlatformConfiguration.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_label_type = LabelType.new
    old_labelled_until = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    old_release_phase = ReleasePhase.global_launch
    
    new_label_type = LabelType.updated
    new_labelled_until = DateTime(2017, 5, 16, tzinfo = TimeZone.utc)
    new_release_phase = ReleasePhase.global_launch # we only have 1 instance
    
    configuration = ClientPlatformConfiguration(
        label_type = old_label_type,
        labelled_until = old_labelled_until,
        release_phase = old_release_phase,
    )
    
    copy = configuration.copy_with(
        label_type = new_label_type,
        labelled_until = new_labelled_until,
        release_phase = new_release_phase,
    )
    _assert_fields_set(configuration)
    vampytest.assert_is_not(copy, configuration)
    
    vampytest.assert_is(copy.label_type, new_label_type)
    vampytest.assert_eq(copy.labelled_until, new_labelled_until)
    vampytest.assert_is(copy.release_phase, new_release_phase)
