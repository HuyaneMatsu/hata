from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..client_platform_configuration import ClientPlatformConfiguration
from ..preinstanced import LabelType, ReleasePhase


def test__ClientPlatformConfiguration__repr():
    """
    Tests whether ``ClientPlatformConfiguration.__repr__`` works as intended.
    """
    label_type = LabelType.new
    labelled_until = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    release_phase = ReleasePhase.global_launch
    
    configuration = ClientPlatformConfiguration(
        label_type = label_type,
        labelled_until = labelled_until,
        release_phase = release_phase,
    )
    
    vampytest.assert_instance(repr(configuration), str)


def test__ClientPlatformConfiguration__eq():
    """
    Tests whether ``ClientPlatformConfiguration.__repr__`` works as intended.
    """
    label_type = LabelType.new
    labelled_until = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    release_phase = ReleasePhase.global_launch
    
    keyword_parameters = {
        'label_type': label_type,
        'labelled_until': labelled_until,
        'release_phase': release_phase,
    }
    
    configuration_original = ClientPlatformConfiguration(**keyword_parameters)
    
    vampytest.assert_eq(configuration_original, configuration_original)
    
    for field_name, field_value in (
        ('label_type', LabelType.updated),
        ('labelled_until', DateTime(2017, 5, 14, tzinfo = TimeZone.utc)),
        # ('release_phase', ReleasePhase.global_launch),we only have 1 instance
    ):
        configuration_altered = ClientPlatformConfiguration(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(configuration_original, configuration_altered)


def test__ClientPlatformConfiguration__hash():
    """
    Tests whether ``ClientPlatformConfiguration.__hash__`` works as intended.
    """
    label_type = LabelType.new
    labelled_until = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    release_phase = ReleasePhase.global_launch
    
    configuration = ClientPlatformConfiguration(
        label_type = label_type,
        labelled_until = labelled_until,
        release_phase = release_phase,
    )
    
    vampytest.assert_instance(hash(configuration), int)
