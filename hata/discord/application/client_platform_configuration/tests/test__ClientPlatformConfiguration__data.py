from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..client_platform_configuration import ClientPlatformConfiguration
from ..preinstanced import LabelType, ReleasePhase

from .test__ClientPlatformConfiguration__constructor import _assert_fields_set


def test__ClientPlatformConfiguration__from_data():
    """
    Tests whether ``ClientPlatformConfiguration.from_data`` works as intended.
    """
    label_type = LabelType.new
    labelled_until = DateTime(2016, 5, 14)
    release_phase = ReleasePhase.global_launch
    
    data = {
        'label_type': label_type.value,
        'label_until': datetime_to_timestamp(labelled_until),
        'release_phase': release_phase.value,
    }
    
    configuration = ClientPlatformConfiguration.from_data(data)
    _assert_fields_set(configuration)
    
    vampytest.assert_is(configuration.label_type, label_type)
    vampytest.assert_eq(configuration.labelled_until, labelled_until)
    vampytest.assert_is(configuration.release_phase, release_phase)


def test__ClientPlatformConfiguration__to_data():
    """
    Tests whether ``ClientPlatformConfiguration.to_data`` works as intended.
    
    Case: include defaults.
    """
    label_type = LabelType.new
    labelled_until = DateTime(2016, 5, 14)
    release_phase = ReleasePhase.global_launch
    
    configuration = ClientPlatformConfiguration(
        label_type = label_type,
        labelled_until = labelled_until,
        release_phase = release_phase,
    )
    
    expected_output = {
        'label_type': label_type.value,
        'label_until': datetime_to_timestamp(labelled_until),
        'release_phase': release_phase.value,
    }
    
    vampytest.assert_eq(
        configuration.to_data(defaults = True),
        expected_output,
    )
